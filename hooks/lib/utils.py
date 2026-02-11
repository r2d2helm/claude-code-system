"""Fonctions utilitaires partagees pour les hooks Claude Code."""

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from .paths import LOGS_DIR

# Timezone Europe/Paris (UTC+1, UTC+2 en ete)
_PARIS_UTC_OFFSET = timedelta(hours=1)


def read_stdin_json() -> dict:
    """Lit stdin et parse le JSON. Retourne {} si erreur."""
    try:
        data = sys.stdin.read()
        if not data.strip():
            return {}
        return json.loads(data)
    except Exception:
        return {}


def now_paris() -> str:
    """Retourne datetime actuel en Europe/Paris ISO 8601.

    Approximation UTC+1 (CET). Pour la precision DST,
    il faudrait zoneinfo (Python 3.9+) mais on garde ca simple.
    """
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Paris")).isoformat()
    except Exception:
        # Fallback UTC+1 si zoneinfo/tzdata absent
        tz = timezone(_PARIS_UTC_OFFSET)
        return datetime.now(tz).isoformat()


def append_jsonl(path: Path, data: dict) -> None:
    """Append une ligne JSON a un fichier JSONL. Cree le parent si absent."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    except Exception:
        pass


def log_audit(hook_name: str, event: str, details: dict | None = None) -> None:
    """Ecrit une entree d'audit dans hooks-audit.jsonl."""
    entry = {
        "timestamp": now_paris(),
        "hook": hook_name,
        "event": event,
    }
    if details:
        entry["details"] = details
    append_jsonl(LOGS_DIR / "hooks-audit.jsonl", entry)


def output_json(data: dict) -> None:
    """Print JSON sur stdout pour Claude Code."""
    print(json.dumps(data, ensure_ascii=False))
