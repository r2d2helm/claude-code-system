"""Fonctions utilitaires partagees pour les hooks Claude Code."""

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from .paths import LOGS_DIR


def read_stdin_json() -> dict:
    """Lit stdin et parse le JSON. Retourne {} si erreur."""
    try:
        data = sys.stdin.read()
        if not data.strip():
            return {}
        return json.loads(data)
    except Exception:
        return {}


def _compute_paris_offset(now_utc=None) -> timedelta:
    """Calcule dynamiquement l'offset Europe/Paris (CET/CEST).

    Regles EU DST: transition dernier dimanche de mars (01:00 UTC -> CEST +2)
    et dernier dimanche d'octobre (01:00 UTC -> CET +1).
    Parametre now_utc optionnel pour testabilite.
    """
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    year = now_utc.year
    # Dernier dimanche de mars
    mar31 = datetime(year, 3, 31, 1, 0, tzinfo=timezone.utc)
    march_switch = mar31 - timedelta(days=mar31.weekday() + 1) if mar31.weekday() != 6 else mar31
    # Dernier dimanche d'octobre
    oct31 = datetime(year, 10, 31, 1, 0, tzinfo=timezone.utc)
    october_switch = oct31 - timedelta(days=oct31.weekday() + 1) if oct31.weekday() != 6 else oct31
    if march_switch <= now_utc < october_switch:
        return timedelta(hours=2)  # CEST
    return timedelta(hours=1)  # CET


def now_paris() -> str:
    """Retourne datetime actuel en Europe/Paris ISO 8601.

    Utilise zoneinfo (Python 3.9+) pour gerer automatiquement CET/CEST.
    Fallback calcul dynamique DST si zoneinfo ou tzdata absent.
    """
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Paris")).isoformat()
    except Exception:
        # Fallback: calcul dynamique CET/CEST
        now_utc = datetime.now(timezone.utc)
        offset = _compute_paris_offset(now_utc)
        tz = timezone(offset)
        return now_utc.astimezone(tz).isoformat()


def append_jsonl(path: Path, data: dict) -> None:
    """Append une ligne JSON a un fichier JSONL. Cree le parent si absent."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    except Exception:
        pass


def log_audit(hook_name: str, event: str, details: dict | None = None,
              duration_ms: int | None = None) -> None:
    """Ecrit une entree d'audit dans hooks-audit.jsonl."""
    entry = {
        "timestamp": now_paris(),
        "hook": hook_name,
        "event": event,
    }
    if duration_ms is not None:
        entry["duration_ms"] = duration_ms
    if details:
        entry["details"] = details
    append_jsonl(LOGS_DIR / "hooks-audit.jsonl", entry)


def output_json(data: dict) -> None:
    """Print JSON sur stdout pour Claude Code."""
    print(json.dumps(data, ensure_ascii=False))


# ============================================================
# Critical error marker
# ============================================================

_CRITICAL_MARKER = Path(__file__).resolve().parent.parent / "data" / ".critical_error"


def mark_critical_error(hook_name: str, error_type: str, detail: str = "") -> None:
    """Ecrit un marker file pour signaler une erreur critique.

    Erreurs critiques: DB corruption, schema failure, permission denied sur data.
    Les hooks downstream consultent ce marker pour adapter leur comportement.
    """
    try:
        _CRITICAL_MARKER.parent.mkdir(parents=True, exist_ok=True)
        marker = {
            "timestamp": now_paris(),
            "hook": hook_name,
            "error_type": error_type,
            "detail": detail[:200],
        }
        _CRITICAL_MARKER.write_text(json.dumps(marker, ensure_ascii=False), encoding="utf-8")
        log_audit(hook_name, "critical_error", marker)
    except Exception:
        pass


def check_critical_error() -> dict | None:
    """Verifie si un marker d'erreur critique existe.

    Retourne le marker dict si present et recent (< 1h), None sinon.
    """
    try:
        if not _CRITICAL_MARKER.exists():
            return None
        # Ignorer les markers > 1h (auto-recovery)
        age_s = datetime.now(timezone.utc).timestamp() - _CRITICAL_MARKER.stat().st_mtime
        if age_s > 3600:
            _CRITICAL_MARKER.unlink(missing_ok=True)
            return None
        marker = json.loads(_CRITICAL_MARKER.read_text(encoding="utf-8"))
        return marker
    except Exception:
        return None


def clear_critical_error() -> None:
    """Supprime le marker d'erreur critique (apres resolution)."""
    try:
        _CRITICAL_MARKER.unlink(missing_ok=True)
    except Exception:
        pass
