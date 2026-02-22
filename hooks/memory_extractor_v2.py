"""Stop hook v2: extraction heuristique de memoires.

Remplace memory_extractor.py avec 5 heuristiques rapides (pas de LLM):
1. Tool sequences (Read->erreur->Edit = pattern de fix)
2. Problem-solution pairs (erreur tool_result suivie d'explication)
3. Topic extraction (TF-IDF-like avec stopwords FR+EN)
4. Decisions ("I'll use X because..." apres exploration)
5. Facts (conventions recurrentes: encodage, nommage, chemins)

Ecrit dans SQLite (memory_db) + JSONL backup (backward compat).
Performance cible: < 2s pour 500 lignes de transcript.
"""

import sys
import json
import re
import hashlib
from pathlib import Path
from collections import Counter, deque
from datetime import datetime

# Ajouter le dossier hooks au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import LOGS_DIR, MEMORY_DIR, VAULT_PATH, CONFIG_DIR
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris

# Import memory_db (fail-open si absent)
try:
    from lib.memory_db import (
        upsert_session, insert_memory, upsert_fact,
        get_retrieved_memory_ids, boost_importance,
        update_retrieval_success, upsert_vector,
    )
    HAS_DB = True
except Exception:
    HAS_DB = False

# Import embeddings (fail-open si fastembed absent)
try:
    from lib.embeddings import is_available as _emb_available, embed_text, embedding_to_blob
    HAS_EMBEDDINGS = _emb_available()
except Exception:
    HAS_EMBEDDINGS = False


# ============================================================
# Configuration
# ============================================================

def _load_config() -> dict:
    """Charge memory_v2.yaml, retourne defaults si absent."""
    defaults = {
        "extraction": {
            "max_per_type": 5,
            "min_content_length": 30,
            "max_transcript_lines": 500,
            "importance_defaults": {
                "tool_sequence": 7.0,
                "problem_solution": 7.5,
                "decision": 6.5,
                "insight": 6.0,
                "pattern": 6.0,
            },
        },
        "signals": {
            "complexity": {"low": 5, "medium": 15, "high": 100},
            "duration": {"short": 300, "medium": 1800, "long": 86400},
            "error_threshold": 3,
        },
        "stopwords": {"fr": [], "en": []},
    }
    try:
        config_path = CONFIG_DIR / "memory_v2.yaml"
        if config_path.exists():
            import yaml
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            # Merge avec defaults
            for key in defaults:
                if key in raw:
                    if isinstance(defaults[key], dict) and isinstance(raw[key], dict):
                        defaults[key].update(raw[key])
                    else:
                        defaults[key] = raw[key]
    except Exception as e:
        import logging
        logging.warning("memory_extractor_v2: config load failed, using defaults: %s", e)
    return defaults


_CONFIG = None


def _get_config() -> dict:
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = _load_config()
    return _CONFIG


# ============================================================
# Transcript parsing (optimise)
# ============================================================

def parse_transcript_entries(transcript_path: str, max_lines: int = 500) -> list[dict]:
    """Parse les dernieres lignes du transcript en entrees structurees."""
    entries = []
    try:
        path = Path(transcript_path)
        if not path.exists():
            return entries
        lines = deque(maxlen=max_lines)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                lines.append(line)
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if isinstance(entry, dict):
                    entries.append(entry)
            except json.JSONDecodeError:
                continue
    except Exception:
        pass
    return entries


def _extract_assistant_text(entry: dict) -> str:
    """Extrait le texte d'un message assistant."""
    if entry.get("type") != "assistant":
        return ""
    message = entry.get("message")
    if not isinstance(message, dict):
        return ""
    content = message.get("content", [])
    if not isinstance(content, list):
        return ""
    parts = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text", ""))
    return " ".join(parts)


def _extract_tool_uses(entry: dict) -> list[dict]:
    """Extrait les tool_use d'un message assistant."""
    if entry.get("type") != "assistant":
        return []
    message = entry.get("message")
    if not isinstance(message, dict):
        return []
    content = message.get("content", [])
    if not isinstance(content, list):
        return []
    tools = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "tool_use":
            tools.append(block)
    return tools


def _is_error_result(entry: dict) -> bool:
    """Verifie si une entree est un tool_result avec erreur."""
    if entry.get("type") != "tool_result":
        return False
    content = str(entry.get("content", ""))
    return any(kw in content for kw in ("error", "Error", "ERROR", "FAIL", "Traceback", "Exception"))


def _get_tool_result_text(entry: dict) -> str:
    """Extrait le texte d'un tool_result."""
    if entry.get("type") != "tool_result":
        return ""
    content = entry.get("content", "")
    if isinstance(content, str):
        return content[:500]
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return " ".join(parts)[:500]
    return str(content)[:500]


# ============================================================
# Heuristique 1: Tool sequences
# ============================================================

def extract_tool_sequences(entries: list[dict], max_results: int = 5) -> list[dict]:
    """Detecte les sequences Read->erreur->Edit (patterns de fix)."""
    sequences = []
    tool_history = deque(maxlen=50)  # (name, input_summary, index)

    for i, entry in enumerate(entries):
        tools = _extract_tool_uses(entry)
        for tool in tools:
            name = tool.get("name", "")
            inp = tool.get("input", {})
            summary = ""
            if name in ("Read", "Write", "Edit"):
                summary = inp.get("file_path", "")[:100]
            elif name == "Bash":
                summary = inp.get("command", "")[:80]
            elif name == "Grep":
                summary = inp.get("pattern", "")[:80]
            tool_history.append((name, summary, i))

        # Detecter pattern: Read -> erreur -> Edit sur meme fichier
        if _is_error_result(entry) and len(tool_history) >= 1:
            prev_tool = tool_history[-1] if tool_history else None
            if prev_tool and prev_tool[0] in ("Read", "Bash"):
                error_text = _get_tool_result_text(entry)[:200]
                for j in range(i + 1, min(i + 5, len(entries))):
                    fix_tools = _extract_tool_uses(entries[j])
                    for ft in fix_tools:
                        if ft.get("name") in ("Edit", "Write"):
                            fix_file = ft.get("input", {}).get("file_path", "")[:100]
                            content = f"Fix sequence: {prev_tool[0]}({prev_tool[1][:50]}) -> error -> {ft['name']}({fix_file[:50]})"
                            sequences.append({
                                "type": "tool_sequence",
                                "content": content,
                                "source_context": error_text[:200],
                            })
                            break
                    if len(sequences) >= max_results:
                        break

        if len(sequences) >= max_results:
            break

    return sequences


# ============================================================
# Heuristique 2: Problem-solution pairs
# ============================================================

def extract_problem_solutions(entries: list[dict], max_results: int = 5) -> list[dict]:
    """Detecte les paires erreur -> explication assistant."""
    pairs = []

    for i, entry in enumerate(entries):
        if not _is_error_result(entry):
            continue

        error_text = _get_tool_result_text(entry)[:200]

        for j in range(i + 1, min(i + 4, len(entries))):
            text = _extract_assistant_text(entries[j])
            if len(text) < 30:
                continue

            solution_indicators = [
                r"(?:the (?:issue|problem|error|bug) (?:is|was))\s+(.{20,200})",
                r"(?:fix(?:ed)?|resolv(?:ed|ing)|solv(?:ed|ing))\s+(?:by|with|this|the|it)\s+(.{20,200})",
                r"(?:because|the reason is)\s+(.{20,200})",
                r"(?:need(?:s|ed)? to|should|have to)\s+(.{20,200})",
            ]

            for pat_str in solution_indicators:
                match = re.search(pat_str, text, re.IGNORECASE)
                if match:
                    solution = match.group(0)[:200]
                    content = f"Problem: {error_text[:100]} | Solution: {solution}"
                    pairs.append({
                        "type": "problem_solution",
                        "content": content,
                        "source_context": error_text[:200],
                    })
                    break

            if pairs and pairs[-1].get("source_context") == error_text[:200]:
                break

        if len(pairs) >= max_results:
            break

    return pairs


# ============================================================
# Heuristique 3: Topic extraction (TF-IDF-like)
# ============================================================

def extract_topics(entries: list[dict]) -> list[str]:
    """Extrait les topics principaux par frequence de mots significatifs."""
    config = _get_config()
    stopwords_fr = set(config.get("stopwords", {}).get("fr", []))
    stopwords_en = set(config.get("stopwords", {}).get("en", []))
    stopwords = stopwords_fr | stopwords_en

    word_freq = Counter()
    total_texts = 0

    for entry in entries:
        text = _extract_assistant_text(entry)
        if not text:
            continue
        total_texts += 1
        words = re.findall(r"\b[a-zA-Z_][\w.-]{2,}\b", text.lower())
        unique_words = set(words)
        for w in unique_words:
            if w not in stopwords and not w.startswith("http"):
                word_freq[w] += 1

    if total_texts == 0:
        return []

    threshold = max(2, total_texts * 0.8)
    topics = [
        word for word, count in word_freq.most_common(20)
        if count >= 2 and count < threshold
    ]

    return topics[:10]


# ============================================================
# Heuristique 4: Decisions
# ============================================================

def extract_decisions(entries: list[dict], max_results: int = 5) -> list[dict]:
    """Detecte les decisions apres exploration."""
    decisions = []
    decision_patterns = [
        re.compile(r"(?:I(?:'ll| will) (?:use|go with|choose|implement|create))\s+(.{10,200})", re.IGNORECASE),
        re.compile(r"(?:Let(?:'s| us) (?:use|go with|choose|implement|create))\s+(.{10,200})", re.IGNORECASE),
        re.compile(r"(?:The (?:best|right|correct) (?:approach|way|solution|method) is)\s+(.{10,200})", re.IGNORECASE),
        re.compile(r"(?:(?:I|We) (?:decided|chose|picked|selected) to)\s+(.{10,200})", re.IGNORECASE),
    ]

    for entry in entries:
        text = _extract_assistant_text(entry)
        if len(text) < 40:
            continue

        for pattern in decision_patterns:
            match = pattern.search(text)
            if match:
                decision_text = match.group(0)[:200]
                trivial_words = {"read", "tool", "write", "edit", "bash", "file", "check"}
                words = set(decision_text.lower().split())
                if len(words - trivial_words) > 3:
                    decisions.append({
                        "type": "decision",
                        "content": decision_text,
                        "source_context": text[:200] if len(text) > 200 else text,
                    })
                    break

        if len(decisions) >= max_results:
            break

    return decisions


# ============================================================
# Heuristique 5: Facts (conventions durables)
# ============================================================

def extract_facts(entries: list[dict]) -> list[dict]:
    """Detecte les conventions recurrentes (encodage, nommage, chemins)."""
    facts = {}
    fact_patterns = [
        (r"UTF-8\s+(?:sans|with(?:out)?)\s+BOM", "encoding/utf8", "UTF-8 sans BOM pour fichiers md/json"),
        (r"UTF-8\s+avec\s+BOM", "encoding/powershell", "UTF-8 avec BOM pour scripts PowerShell"),
        (r"(?:vault|Knowledge)\s+(?:path|dir|dossier)\s*(?:is|est|:)\s*(.{10,100})", "path/vault", None),
        (r"compatible?\s+PS\s*5\.1", "compat/powershell", "Scripts PS doivent etre compatibles PS 5.1"),
        (r"pas\s+de\s+\?\?|no\s+null\s+coalescing", "compat/powershell-syntax", "Pas de ?? en PowerShell 5.1"),
    ]

    for entry in entries:
        text = _extract_assistant_text(entry)
        if len(text) < 20:
            continue

        for pat_str, key, default_value in fact_patterns:
            match = re.search(pat_str, text, re.IGNORECASE)
            if match:
                value = default_value or match.group(0)[:200]
                facts[key] = {"key": key, "value": value}

    return list(facts.values())


# ============================================================
# Helpers
# ============================================================

def _content_hash(text: str) -> str:
    """Hash court pour deduplication."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]


def _compute_duration_s(first_ts: str, last_ts: str) -> int:
    """Calcule la duree en secondes entre deux timestamps."""
    if not first_ts or not last_ts:
        return 0
    try:
        fmt_patterns = [
            "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z",
        ]
        t1 = t2 = None
        for fmt in fmt_patterns:
            try:
                t1 = datetime.strptime(first_ts, fmt)
                break
            except ValueError:
                continue
        for fmt in fmt_patterns:
            try:
                t2 = datetime.strptime(last_ts, fmt)
                break
            except ValueError:
                continue
        if t1 and t2:
            return max(0, int((t2 - t1).total_seconds()))
    except Exception:
        pass
    return 0


# ============================================================
# Metrics from entries (single-pass, replaces lib/transcript)
# ============================================================

def _compute_metrics_from_entries(entries: list[dict]) -> dict:
    """Calcule les metriques depuis les entries deja parsees (evite double I/O)."""
    from collections import Counter
    tools_used = Counter()
    files_modified = set()
    bash_commands = []
    message_count = len(entries)
    first_timestamp = None
    last_timestamp = None

    for entry in entries:
        ts = entry.get("timestamp")
        if ts:
            if first_timestamp is None:
                first_timestamp = ts
            last_timestamp = ts

        if entry.get("type") != "assistant":
            continue
        content = entry.get("message", {}).get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            tool_name = block.get("name", "")
            tool_input = block.get("input", {})
            tools_used[tool_name] += 1
            if tool_name in ("Write", "Edit", "NotebookEdit"):
                fp = tool_input.get("file_path") or tool_input.get("notebook_path")
                if fp:
                    files_modified.add(fp)
            if tool_name == "Bash":
                cmd = tool_input.get("command", "")
                if cmd:
                    bash_commands.append(cmd[:100])

    return {
        "message_count": message_count,
        "tools_used": dict(tools_used),
        "files_modified": list(files_modified),
        "bash_commands_count": len(bash_commands),
        "bash_commands_sample": bash_commands[:10],
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
    }


# ============================================================
# Feedback loop
# ============================================================

def apply_feedback(session_id: str, success: bool) -> None:
    """Applique le feedback de la session aux memoires servies."""
    if not HAS_DB:
        return
    try:
        update_retrieval_success(session_id, success)
        if success:
            memory_ids = get_retrieved_memory_ids(session_id)
            for mid in memory_ids:
                boost_importance(mid, 0.5)
    except Exception:
        pass


# ============================================================
# Main
# ============================================================

def main():
    try:
        input_data = read_stdin_json()
        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")

        config = _get_config()
        ext_cfg = config.get("extraction", {})
        max_lines = ext_cfg.get("max_transcript_lines", 500)
        max_per_type = ext_cfg.get("max_per_type", 5)
        importance_defaults = ext_cfg.get("importance_defaults", {})

        # --- Partie 1+2: Parse transcript une seule fois ---
        entries = []
        if transcript_path:
            entries = parse_transcript_entries(transcript_path, max_lines)

        # Calculer metriques depuis les entries (evite double I/O)
        metrics = _compute_metrics_from_entries(entries)

        # Backward compat: session-log.jsonl
        session_summary = {
            "timestamp": now_paris(),
            "session_id": session_id,
            "metrics": metrics,
        }
        append_jsonl(LOGS_DIR / "session-log.jsonl", session_summary)

        # Compter les erreurs
        errors_count = sum(1 for e in entries if _is_error_result(e))

        # 5 heuristiques
        tool_sequences = extract_tool_sequences(entries, max_per_type)
        problem_solutions = extract_problem_solutions(entries, max_per_type)
        topics = extract_topics(entries)
        decisions = extract_decisions(entries, max_per_type)
        facts = extract_facts(entries)

        # Toutes les memoires extraites
        all_memories = []
        for mem in tool_sequences:
            mem["importance_score"] = importance_defaults.get("tool_sequence", 7.0)
            all_memories.append(mem)
        for mem in problem_solutions:
            mem["importance_score"] = importance_defaults.get("problem_solution", 7.5)
            all_memories.append(mem)
        for mem in decisions:
            mem["importance_score"] = importance_defaults.get("decision", 6.5)
            all_memories.append(mem)

        # --- Partie 3: Calcul metriques session ---
        duration_s = _compute_duration_s(
            metrics.get("first_timestamp", ""),
            metrics.get("last_timestamp", ""),
        )
        unique_tools = len(metrics.get("tools_used", {}))

        sig_cfg = config.get("signals", {})
        complexity_low = sig_cfg.get("complexity", {}).get("low", 5)
        duration_short = sig_cfg.get("duration", {}).get("short", 300)
        error_threshold = sig_cfg.get("error_threshold", 3)

        is_trivial = (
            unique_tools < complexity_low
            and duration_s < duration_short
            and errors_count < error_threshold
            and len(all_memories) == 0
        )

        session_success = errors_count < error_threshold

        # --- Partie 4: Persistance SQLite ---
        if HAS_DB:
            # Upsert session
            upsert_session({
                "id": session_id,
                "timestamp": now_paris(),
                "duration_s": duration_s,
                "complexity": unique_tools,
                "message_count": metrics.get("message_count", 0),
                "files_modified": len(metrics.get("files_modified", [])),
                "errors_count": errors_count,
                "working_directory": "",
                "skills_used": [],
                "topics": topics,
                "summary_json": {
                    "tools_used": metrics.get("tools_used", {}),
                    "bash_commands_sample": metrics.get("bash_commands_sample", [])[:5],
                },
                "trivial": is_trivial,
                "success": session_success,
                "created_at": now_paris(),
            })

            # Insert memories + embeddings (v3)
            for mem in all_memories:
                memory_id = insert_memory({
                    "session_id": session_id,
                    "type": mem["type"],
                    "content": mem["content"],
                    "tags": json.dumps(topics[:5]),
                    "importance_score": mem.get("importance_score", 5.0),
                    "created_at": now_paris(),
                    "source_context": mem.get("source_context", ""),
                })
                # v3: generer et stocker l'embedding si disponible
                if memory_id and HAS_EMBEDDINGS:
                    try:
                        embedding = embed_text(mem["content"])
                        if embedding:
                            blob = embedding_to_blob(embedding)
                            upsert_vector(memory_id, blob)
                    except Exception:
                        pass  # fail-open

            # Upsert facts
            for fact in facts:
                upsert_fact(fact["key"], fact["value"], confidence=0.5, session_id=session_id)

            # Feedback loop: boost memoires servies si session reussie
            apply_feedback(session_id, session_success)

        # --- Partie 5: Backward compat JSONL ---
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)

        # Signal
        signal = {
            "timestamp": now_paris(),
            "session_id": session_id,
            "duration_s": duration_s,
            "complexity": unique_tools,
            "files_modified": len(metrics.get("files_modified", [])),
            "errors": errors_count,
            "insights_count": len(problem_solutions),
            "patterns_count": len(tool_sequences) + len(decisions),
            "topics": topics[:5],
            "trivial": is_trivial,
        }
        append_jsonl(MEMORY_DIR / "signals.jsonl", signal)

        # Insights (backward compat)
        for mem in problem_solutions:
            append_jsonl(MEMORY_DIR / "insights.jsonl", {
                "timestamp": now_paris(),
                "type": "insight",
                "content": mem["content"][:300],
                "hash": _content_hash(mem["content"]),
                "session_id": session_id,
            })

        # Patterns (backward compat)
        for mem in tool_sequences + decisions:
            append_jsonl(MEMORY_DIR / "patterns.jsonl", {
                "timestamp": now_paris(),
                "type": "pattern",
                "content": mem["content"][:200],
                "hash": _content_hash(mem["content"]),
                "session_id": session_id,
            })

        # --- Partie 6: Audit ---
        log_audit("memory_extractor_v2", "session_end", {
            "session_id": session_id,
            "messages": metrics.get("message_count", 0),
            "tools": unique_tools,
            "files_modified": len(metrics.get("files_modified", [])),
            "memories_extracted": len(all_memories),
            "facts_extracted": len(facts),
            "topics": topics[:5],
            "errors": errors_count,
            "duration_s": duration_s,
            "trivial": is_trivial,
            "db_available": HAS_DB,
            "embeddings_available": HAS_EMBEDDINGS,
        })

        # --- Partie 7: Consolidation automatique (rate-limited) ---
        if HAS_DB:
            try:
                from lib.memory_db import purge_old_retrieval_logs
                purge_old_retrieval_logs(max_age_days=30)
                consolidation_marker = MEMORY_DIR / ".last_consolidation"
                should_consolidate = True
                if consolidation_marker.exists():
                    try:
                        marker_age = datetime.now().timestamp() - consolidation_marker.stat().st_mtime
                        if marker_age < 3600:
                            should_consolidate = False
                    except Exception:
                        pass
                if should_consolidate:
                    from memory_consolidator import consolidate
                    consolidate(dry_run=False)
                    consolidation_marker.write_text(now_paris(), encoding="utf-8")
            except Exception:
                pass

    except Exception as e:
        try:
            log_audit("memory_extractor_v2", "error", {"error": str(e)})
        except Exception:
            pass

    # Toujours exit 0 - fail-open
    sys.exit(0)


if __name__ == "__main__":
    main()
