"""Stop hook: shim redirecting main() to memory_extractor_v2.py.

DEPRECATED: This file exists for backward compatibility only.
The actual main() implementation is in memory_extractor_v2.py which uses
SQLite (Memory v2) instead of JSONL-only storage.

Functions (extract_insights, create_vault_note, etc.) are preserved
from the repo v1.5 version for backward compatibility with tests.

Previous versions:
- _deprecated/memory_extractor_repo_v1.5.py (repo v1.5 JSONL version)
- _deprecated/memory_extractor_v1.py (original v1)
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
# PARTIE 2: Extraction d'insights et patterns (v1.5 legacy)
# ============================================================

# Hardcoded fallback patterns (utilises si YAML absent ou invalide)
_FALLBACK_INSIGHT_PATTERNS = [
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

_FALLBACK_PATTERN_PATTERNS = [
    re.compile(
        r"(?:always|never|must|should always|should never)"
        r"(.{20,150})", re.IGNORECASE
    ),
    re.compile(
        r"(?:convention|standard|pattern|best practice)\s*(?:is|:)"
        r"(.{20,150})", re.IGNORECASE
    ),
]

# Cache module-level pour les regles chargees
_cached_rules = None


def load_memory_rules() -> dict | None:
    """Charge les regles depuis config/memory_rules.yaml."""
    rules_file = CONFIG_DIR / "memory_rules.yaml"
    try:
        if not rules_file.exists():
            return None
        import yaml
        raw = yaml.safe_load(rules_file.read_text(encoding="utf-8")) or {}

        compiled = {"insights": [], "patterns": [], "signals": raw.get("signals", {})}
        for entry in raw.get("insights", []):
            try:
                compiled["insights"].append(re.compile(entry["pattern"], re.IGNORECASE))
            except (re.error, KeyError):
                continue
        for entry in raw.get("patterns", []):
            try:
                compiled["patterns"].append(re.compile(entry["pattern"], re.IGNORECASE))
            except (re.error, KeyError):
                continue
        return compiled
    except Exception:
        return None


def _get_rules() -> dict:
    """Retourne les regles compilees (YAML avec fallback hardcoded)."""
    global _cached_rules
    if _cached_rules is not None:
        return _cached_rules

    loaded = load_memory_rules()
    if loaded and loaded.get("insights"):
        _cached_rules = loaded
    else:
        _cached_rules = {
            "insights": _FALLBACK_INSIGHT_PATTERNS,
            "patterns": _FALLBACK_PATTERN_PATTERNS,
            "signals": {},
        }
    return _cached_rules


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

        from collections import deque
        lines = deque(maxlen=max_lines)
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                lines.append(line)

        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            if not isinstance(entry, dict):
                continue

            # Compter les erreurs dans les resultats d'outils
            if entry.get("type") == "tool_result":
                result_text = str(entry.get("content", ""))
                if any(kw in result_text for kw in ("error", "Error", "ERROR", "FAIL", "Traceback")):
                    errors_count += 1

            # Extraire texte des messages assistant
            if entry.get("type") != "assistant":
                continue

            message = entry.get("message")
            if not isinstance(message, dict):
                continue

            content = message.get("content", [])
            if not isinstance(content, list):
                continue

            for block in content:
                if not isinstance(block, dict) or block.get("type") != "text":
                    continue

                text = block.get("text", "")
                if len(text) < 30:
                    continue

                # Chercher des insights
                rules = _get_rules()
                for pattern in rules["insights"]:
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
                for pattern in rules["patterns"]:
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
    """Cree une note dans _Inbox/ pour un insight significatif."""
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
# Main: delegate to memory_extractor_v2.py
# ============================================================

def main():
    """Delegate to memory_extractor_v2 main()."""
    try:
        from memory_extractor_v2 import main as v2_main
        v2_main()
    except Exception:
        # Fail-open: si v2 echoue, exit silencieusement
        sys.exit(0)


if __name__ == "__main__":
    main()
