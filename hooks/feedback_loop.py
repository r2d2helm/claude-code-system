"""Stop hook: boucle de feedback explicite - la spirale encodee.

A la fin de chaque session significative, auto-genere:
- Ce qui a bien fonctionne (renforcement)
- Ce qui a mal fonctionne (correction)
- Ce qui a emerge d'inattendu (innovation)

Injecte le feedback de la session precedente au startup suivant.
Framework: B0[0] Evolution #6 - Double boucle auto-catalytique.
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import LOGS_DIR, CONFIG_DIR
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris

# Import memory_db (fail-open)
try:
    from lib.memory_db import insert_memory
    HAS_DB = True
except Exception:
    HAS_DB = False


def _load_config() -> dict:
    """Charge la section feedback_loop de memory_v2.yaml."""
    defaults = {
        "enabled": True,
        "auto_generate": True,
        "inject_previous_session": True,
        "max_feedback_chars": 500,
        "types": ["success", "correction", "emergence"],
    }
    try:
        config_path = CONFIG_DIR / "memory_v2.yaml"
        if config_path.exists():
            import yaml
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            fb = raw.get("feedback_loop", {})
            defaults.update(fb)
    except Exception:
        pass
    return defaults


def _extract_feedback(transcript_lines: list[str]) -> dict:
    """Extrait le feedback de la session depuis le transcript."""
    feedback = {
        "successes": [],
        "corrections": [],
        "emergences": [],
    }

    success_patterns = [
        r"parfait|excellent|exactement|bien joue|genial|bravo",
        r"ca (marche|fonctionne)|resolved|fixed|done",
        r"merci|super|top",
    ]

    correction_patterns = [
        r"non[,.]|pas comme ca|incorrect|wrong",
        r"corrige|recommence|reessaie|plutot",
        r"erreur|error|bug|fail",
    ]

    emergence_patterns = [
        r"interessant|revelat|inattendu|surprise",
        r"je (realise|comprends|vois)",
        r"emergence|convergence|insight|decouverte",
        r"bonne (question|idee|observation)",
    ]

    for line in transcript_lines:
        lower = line.lower()
        text_preview = line[:120].strip()

        if not text_preview or len(text_preview) < 10:
            continue

        for pat in success_patterns:
            if re.search(pat, lower):
                if text_preview not in feedback["successes"]:
                    feedback["successes"].append(text_preview)
                break

        for pat in correction_patterns:
            if re.search(pat, lower):
                if text_preview not in feedback["corrections"]:
                    feedback["corrections"].append(text_preview)
                break

        for pat in emergence_patterns:
            if re.search(pat, lower):
                if text_preview not in feedback["emergences"]:
                    feedback["emergences"].append(text_preview)
                break

    # Limiter a 3 par type
    for key in feedback:
        feedback[key] = feedback[key][:3]

    return feedback


def _format_feedback(feedback: dict) -> str:
    """Formate le feedback pour stockage."""
    parts = []

    if feedback["successes"]:
        parts.append("BIEN: " + " | ".join(feedback["successes"][:2]))

    if feedback["corrections"]:
        parts.append("CORRIGER: " + " | ".join(feedback["corrections"][:2]))

    if feedback["emergences"]:
        parts.append("EMERGE: " + " | ".join(feedback["emergences"][:2]))

    return "\n".join(parts) if parts else ""


def main():
    try:
        data = read_stdin_json()
    except Exception:
        return

    config = _load_config()
    if not config.get("enabled", True) or not config.get("auto_generate", True):
        return

    # Extraire le transcript
    transcript = data.get("transcript", [])
    if not transcript:
        return

    lines = []
    for entry in transcript[-150:]:
        if isinstance(entry, dict):
            msg = entry.get("message", "")
            if isinstance(msg, str):
                lines.append(msg)
            elif isinstance(msg, list):
                for part in msg:
                    if isinstance(part, dict) and part.get("type") == "text":
                        lines.append(part.get("text", ""))

    if len(lines) < 5:
        return

    feedback = _extract_feedback(lines)
    formatted = _format_feedback(feedback)

    if not formatted:
        return

    # Tronquer au max
    max_chars = config.get("max_feedback_chars", 500)
    formatted = formatted[:max_chars]

    # Stocker dans SQLite
    if HAS_DB:
        session_id = data.get("session_id", "unknown")
        try:
            insert_memory(
                session_id=session_id,
                mem_type="feedback_loop",
                content=formatted,
                importance=6.0,
                metadata=json.dumps({
                    "successes": len(feedback["successes"]),
                    "corrections": len(feedback["corrections"]),
                    "emergences": len(feedback["emergences"]),
                }),
            )
        except Exception:
            pass

    # Logger en JSONL
    log_entry = {
        "ts": now_paris(),
        "session_id": data.get("session_id", "unknown"),
        "feedback": feedback,
        "formatted": formatted,
    }
    try:
        append_jsonl(LOGS_DIR / "feedback-loop.jsonl", log_entry)
    except Exception:
        pass

    log_audit("feedback_loop", f"s={len(feedback['successes'])} c={len(feedback['corrections'])} e={len(feedback['emergences'])}")


if __name__ == "__main__":
    main()
