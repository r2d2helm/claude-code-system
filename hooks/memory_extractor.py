"""Stop hook etendu: capture metriques de session ET extrait des insights.

Remplace session_capture.py avec 3 parties:
1. Metriques de session (via lib/transcript.py)
2. Extraction d'insights et patterns depuis le transcript
3. Persistance dans data/memory/ et creation de notes vault si significatif
"""

import sys
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime

# Ajouter le dossier hooks au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import LOGS_DIR, MEMORY_DIR, VAULT_PATH, CONFIG_DIR
from lib.transcript import parse_transcript
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris


# ============================================================
# PARTIE 2: Extraction d'insights et patterns
# ============================================================

# Patterns compiles pour detecter des insights
INSIGHT_PATTERNS = [
    re.compile(
        r"(?:the (?:issue|problem|bug|error) was|root cause)"
        r"(.{20,200})", re.IGNORECASE
    ),
    re.compile(
        r"(?:fix(?:ed)?|resolved|solved|corrected)\s*(?:by|with|using|:)"
        r"(.{20,200})", re.IGNORECASE
    ),
    re.compile(
        r"(?:solution|workaround|fix)\s*(?:is|was|:)"
        r"(.{20,200})", re.IGNORECASE
    ),
    re.compile(
        r"(?:found that|discovered that|turns out)"
        r"(.{20,200})", re.IGNORECASE
    ),
    re.compile(
        r"(?:the trick is|key insight|important:)"
        r"(.{20,200})", re.IGNORECASE
    ),
]

PATTERN_PATTERNS = [
    re.compile(
        r"(?:always|never|must|should always|should never)"
        r"(.{20,150})", re.IGNORECASE
    ),
    re.compile(
        r"(?:convention|standard|pattern|best practice)\s*(?:is|:)"
        r"(.{20,150})", re.IGNORECASE
    ),
]


def _content_hash(text: str) -> str:
    """Retourne un hash court pour deduplication."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]


def extract_insights(transcript_path: str, max_lines: int = 200) -> dict:
    """Extrait insights et patterns du transcript.

    Retourne { insights: [...], patterns: [...], errors_count: int }
    """
    insights = []
    patterns = []
    seen_hashes = set()
    errors_count = 0

    try:
        path = Path(transcript_path)
        if not path.exists():
            return {"insights": [], "patterns": [], "errors_count": 0}

        lines = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                lines.append(line)
                if len(lines) > max_lines:
                    lines.pop(0)

        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Compter les erreurs dans les resultats d'outils
            if entry.get("type") == "tool_result":
                result_text = str(entry.get("content", ""))
                if any(kw in result_text for kw in ("error", "Error", "ERROR", "FAIL", "Traceback")):
                    errors_count += 1

            # Extraire texte des messages assistant
            if entry.get("type") != "assistant":
                continue

            content = entry.get("message", {}).get("content", [])
            if not isinstance(content, list):
                continue

            for block in content:
                if not isinstance(block, dict) or block.get("type") != "text":
                    continue

                text = block.get("text", "")
                if len(text) < 30:
                    continue

                # Chercher des insights
                for pattern in INSIGHT_PATTERNS:
                    for match in pattern.finditer(text):
                        matched = match.group(0).strip()
                        h = _content_hash(matched)
                        if h not in seen_hashes:
                            seen_hashes.add(h)
                            insights.append({
                                "timestamp": now_paris(),
                                "type": "insight",
                                "content": matched[:300],
                                "hash": h,
                            })
                        if len(insights) >= 10:
                            break
                    if len(insights) >= 10:
                        break

                # Chercher des patterns techniques
                for pattern in PATTERN_PATTERNS:
                    for match in pattern.finditer(text):
                        matched = match.group(0).strip()
                        h = _content_hash(matched)
                        if h not in seen_hashes:
                            seen_hashes.add(h)
                            patterns.append({
                                "timestamp": now_paris(),
                                "type": "pattern",
                                "content": matched[:200],
                                "hash": h,
                            })
                        if len(patterns) >= 10:
                            break
                    if len(patterns) >= 10:
                        break

    except Exception:
        pass

    return {
        "insights": insights,
        "patterns": patterns,
        "errors_count": errors_count,
    }


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


def create_vault_note(insight: dict, session_id: str) -> None:
    """Cree une note dans _Inbox/ pour un insight significatif.

    Seulement si contenu > 50 chars et semble etre un fix ou decision.
    Verifie que le chemin cible est bien dans le vault attendu (path guard).
    """
    try:
        content = insight.get("content", "")
        if len(content) < 50:
            return

        inbox_dir = VAULT_PATH / "_Inbox"
        if not inbox_dir.exists():
            return

        # Path guard: verifier que inbox_dir est bien sous VAULT_PATH
        if not inbox_dir.resolve().is_relative_to(VAULT_PATH.resolve()):
            log_audit("memory_extractor", "path_guard_block", {
                "reason": "inbox_dir outside vault",
                "path": str(inbox_dir),
            })
            return

        # Generer un nom unique
        today = datetime.now().strftime("%Y-%m-%d")
        h = insight.get("hash", "000")[:6]
        note_name = f"{today}_insight_{h}.md"
        note_path = inbox_dir / note_name

        # Ne pas ecraser si existe deja
        if note_path.exists():
            return

        # Path guard: verifier que la note reste dans le vault
        if not note_path.resolve().is_relative_to(VAULT_PATH.resolve()):
            return

        frontmatter = (
            "---\n"
            f'title: "Auto-insight {h}"\n'
            f"date: {today}\n"
            "type: troubleshooting\n"
            "status: seedling\n"
            "tags:\n"
            "  - ai/auto-memory\n"
            f'source_session: "{session_id[:16]}"\n'
            "---\n\n"
        )

        body = f"# Auto-insight\n\n{content}\n\n"
        body += "> Note generee automatiquement par memory_extractor.py\n"

        note_path.write_text(frontmatter + body, encoding="utf-8")

    except Exception:
        pass


# ============================================================
# PARTIE 3: Main
# ============================================================

def main():
    try:
        input_data = read_stdin_json()
        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")

        # --- Partie 1: Metriques (identique a session_capture.py) ---
        metrics = {}
        if transcript_path:
            metrics = parse_transcript(transcript_path)

        session_summary = {
            "timestamp": now_paris(),
            "session_id": session_id,
            "metrics": metrics,
        }

        # Append dans session-log.jsonl (compatibilite)
        append_jsonl(LOGS_DIR / "session-log.jsonl", session_summary)

        # --- Partie 2: Extraction d'insights ---
        memory = {"insights": [], "patterns": [], "errors_count": 0}
        if transcript_path:
            memory = extract_insights(transcript_path)

        # Creer le dossier memory si absent
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)

        # Persister insights
        for insight in memory.get("insights", []):
            insight["session_id"] = session_id
            append_jsonl(MEMORY_DIR / "insights.jsonl", insight)
            # Creer note vault si significatif
            create_vault_note(insight, session_id)

        # Persister patterns
        for pattern in memory.get("patterns", []):
            pattern["session_id"] = session_id
            append_jsonl(MEMORY_DIR / "patterns.jsonl", pattern)

        # Persister signal de session
        duration_s = _compute_duration_s(
            metrics.get("first_timestamp", ""),
            metrics.get("last_timestamp", ""),
        )
        unique_tools = len(metrics.get("tools_used", {}))
        signal = {
            "timestamp": now_paris(),
            "session_id": session_id,
            "duration_s": duration_s,
            "complexity": unique_tools,
            "files_modified": len(metrics.get("files_modified", [])),
            "errors": memory.get("errors_count", 0),
            "insights_count": len(memory.get("insights", [])),
            "patterns_count": len(memory.get("patterns", [])),
        }
        append_jsonl(MEMORY_DIR / "signals.jsonl", signal)

        # --- Partie 3: Audit ---
        log_audit("memory_extractor", "session_end", {
            "session_id": session_id,
            "messages": metrics.get("message_count", 0),
            "tools": unique_tools,
            "files_modified": len(metrics.get("files_modified", [])),
            "insights": len(memory.get("insights", [])),
            "patterns": len(memory.get("patterns", [])),
            "errors": memory.get("errors_count", 0),
            "duration_s": duration_s,
        })

    except Exception as e:
        log_audit("memory_extractor", "error", {"error": str(e)})

    # Toujours exit 0 - logging silencieux
    sys.exit(0)


if __name__ == "__main__":
    main()
