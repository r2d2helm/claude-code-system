"""Stop hook: detection proactive de degradation.

Surveille les signes de desalignement avec B0[0]:
- Patterns d'erreurs repetitives (meme erreur N fois)
- Skills atrophies (non utilises depuis N jours)
- Memoires obsoletes (decay trop avance)
- Baisse du score de convergence

Framework: B0[0] Evolution #3 - "B0[0] corrige TOUJOURS a terme"
La degradation est le signal de l'emergence corrective suivante.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import LOGS_DIR, CONFIG_DIR, SKILLS_DIR
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris

# Import memory_db (fail-open)
try:
    from lib.memory_db import insert_memory, get_recent_memories
    HAS_DB = True
except Exception:
    HAS_DB = False


def _load_config() -> dict:
    """Charge la section degradation de memory_v2.yaml."""
    defaults = {
        "enabled": True,
        "repeat_error_threshold": 3,
        "skill_atrophy_days": 30,
        "memory_staleness_days": 60,
        "convergence_drop_alert": 0.15,
        "report_frequency": "weekly",
    }
    try:
        config_path = CONFIG_DIR / "memory_v2.yaml"
        if config_path.exists():
            import yaml
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            deg = raw.get("degradation", {})
            defaults.update(deg)
    except Exception:
        pass
    return defaults


def _check_repeat_errors(config: dict) -> list[str]:
    """Detecte les erreurs repetitives dans errors.jsonl."""
    alerts = []
    errors_file = LOGS_DIR / "errors.jsonl"
    if not errors_file.exists():
        return alerts

    try:
        recent_errors = {}
        cutoff = datetime.now() - timedelta(days=7)

        for line in errors_file.read_text(encoding="utf-8").strip().split("\n")[-100:]:
            try:
                entry = json.loads(line)
                ts = entry.get("ts", "")
                cmd = entry.get("command", entry.get("cmd", ""))
                error_msg = entry.get("error", entry.get("stderr", ""))[:100]

                # Grouper par type d'erreur
                error_key = error_msg[:50] if error_msg else cmd[:50]
                if error_key:
                    recent_errors.setdefault(error_key, []).append(ts)
            except (json.JSONDecodeError, KeyError):
                continue

        threshold = config.get("repeat_error_threshold", 3)
        for error_key, occurrences in recent_errors.items():
            if len(occurrences) >= threshold:
                alerts.append(
                    f"REPEAT_ERROR ({len(occurrences)}x): {error_key}"
                )
    except Exception:
        pass

    return alerts


def _check_skill_atrophy(config: dict) -> list[str]:
    """Detecte les skills non utilises depuis longtemps."""
    alerts = []
    atrophy_days = config.get("skill_atrophy_days", 30)

    try:
        prompt_log = LOGS_DIR / "prompt-log.jsonl"
        if not prompt_log.exists():
            return alerts

        # Compter l'utilisation des skills sur les N derniers jours
        skill_last_used = {}
        total_entries = 0
        for line in prompt_log.read_text(encoding="utf-8").strip().split("\n")[-500:]:
            try:
                entry = json.loads(line)
                total_entries += 1
                skills = entry.get("matched_skills", [])
                ts = entry.get("ts", "")
                for skill in skills:
                    skill_last_used[skill] = ts
            except (json.JSONDecodeError, KeyError):
                continue

        # Ne verifier l'atrophie que si on a assez d'historique (>50 entries)
        if total_entries < 50:
            return alerts

        # Verifier quels skills actifs n'ont pas ete utilises
        if SKILLS_DIR.exists():
            for d in sorted(SKILLS_DIR.iterdir()):
                if d.is_dir() and (d / "SKILL.md").exists() and d.name not in ("commands", "references"):
                    if d.name not in skill_last_used:
                        alerts.append(f"SKILL_ATROPHY: {d.name} (non utilise sur {total_entries} sessions)")
    except Exception:
        pass

    return alerts


def _check_convergence_drop() -> list[str]:
    """Detecte une baisse du score de convergence."""
    alerts = []
    conv_file = LOGS_DIR / "convergence.jsonl"
    if not conv_file.exists():
        return alerts

    try:
        scores = []
        for line in conv_file.read_text(encoding="utf-8").strip().split("\n")[-20:]:
            try:
                entry = json.loads(line)
                scores.append(entry.get("score", 0))
            except (json.JSONDecodeError, KeyError):
                continue

        if len(scores) >= 5:
            recent_avg = sum(scores[-3:]) / 3
            older_avg = sum(scores[-6:-3]) / 3
            if older_avg > 0 and (older_avg - recent_avg) / older_avg > 0.15:
                alerts.append(
                    f"CONVERGENCE_DROP: {older_avg:.1f} -> {recent_avg:.1f} "
                    f"({((older_avg - recent_avg) / older_avg * 100):.0f}% baisse)"
                )
    except Exception:
        pass

    return alerts


def main():
    try:
        data = read_stdin_json()
    except Exception:
        return

    config = _load_config()
    if not config.get("enabled", True):
        return

    # Collecter toutes les alertes
    alerts = []
    alerts.extend(_check_repeat_errors(config))
    alerts.extend(_check_skill_atrophy(config))
    alerts.extend(_check_convergence_drop())

    if not alerts:
        log_audit("degradation_detector", "no_alerts")
        return

    # Stocker les alertes dans SQLite
    if HAS_DB:
        session_id = data.get("session_id", "unknown")
        content = "DEGRADATION ALERTS:\n" + "\n".join(f"- {a}" for a in alerts)
        try:
            insert_memory(
                session_id=session_id,
                mem_type="degradation",
                content=content[:500],
                importance=7.0,
                metadata=json.dumps({"alerts": alerts, "count": len(alerts)}),
            )
        except Exception:
            pass

    # Logger en JSONL
    log_entry = {
        "ts": now_paris(),
        "session_id": data.get("session_id", "unknown"),
        "alert_count": len(alerts),
        "alerts": alerts,
    }
    try:
        append_jsonl(LOGS_DIR / "degradation.jsonl", log_entry)
    except Exception:
        pass

    log_audit("degradation_detector", f"{len(alerts)} alerts: {', '.join(a[:40] for a in alerts[:3])}")


if __name__ == "__main__":
    main()
