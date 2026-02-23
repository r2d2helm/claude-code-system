#!/usr/bin/env python3
"""Heartbeat orchestrateur - monitoring proactif systeme.

Execute les probes sysadmin et stocke les resultats dans Memory v2.
Concu pour etre lance par cron toutes les 30 minutes.

Usage:
    python3 heartbeat.py              # Run complet
    python3 heartbeat.py --dry-run    # Affiche le rapport sans stocker
    python3 heartbeat.py --probe disk # Execute une seule probe

Inspire du Second Brain (Dynamous Community), adapte pour sysadmin Linux.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Assurer que lib/ est dans le path
_HOOKS_DIR = Path(__file__).resolve().parent
if str(_HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(_HOOKS_DIR))

from heartbeat_checks import ALL_PROBES, run_all_probes, _get_config
from lib.paths import LOGS_DIR
from lib.utils import append_jsonl


# ============================================================
# Memory v2 Integration
# ============================================================

def _store_heartbeat_memory(report: dict) -> None:
    """Stocke le rapport heartbeat dans Memory v2 comme memoire.

    - Alertes critiques/warning → memoire haute importance
    - Rapport normal → memoire basse importance
    """
    try:
        from lib.memory_db import insert_memory

        config = _get_config()
        importance = config.get("memory_importance", 5.0)
        importance_critical = config.get("memory_importance_critical", 8.0)

        # Determiner l'importance selon le statut
        if report["overall_status"] == "critical":
            imp = importance_critical
        elif report["overall_status"] == "warning":
            imp = (importance + importance_critical) / 2
        else:
            imp = importance

        # Construire le contenu de la memoire
        parts = [f"Heartbeat {report['overall_status'].upper()}"]
        for name, probe in report["probes"].items():
            parts.append(f"{name}: {probe['message']}")

        content = " | ".join(parts)

        # Tags bases sur les probes en alerte
        tags = ["heartbeat", report["overall_status"]]
        for alert in report.get("alerts", []):
            if "[CRITICAL]" in alert:
                tags.append("critical")
            elif "[WARNING]" in alert:
                tags.append("warning")

        session_id = f"heartbeat-{datetime.now().strftime('%Y%m%d-%H%M')}"

        insert_memory({
            "session_id": session_id,
            "type": "heartbeat",
            "content": content[:500],
            "importance_score": imp,
            "tags": tags,
            "source_context": "heartbeat.py",
        })

    except Exception as e:
        # Fail-open: log l'erreur mais ne crash pas
        print(f"[heartbeat] Memory storage failed (non-fatal): {e}", file=sys.stderr)


# ============================================================
# Logging
# ============================================================

def _log_heartbeat(report: dict) -> None:
    """Ajoute le rapport au log JSONL des heartbeats."""
    try:
        log_path = LOGS_DIR / "heartbeat.jsonl"
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        append_jsonl(log_path, {
            "timestamp": report["timestamp"],
            "overall_status": report["overall_status"],
            "alerts": report.get("alerts", []),
            "probes": {
                name: {"status": probe["status"], "message": probe["message"]}
                for name, probe in report["probes"].items()
            },
        })
    except Exception:
        pass


# ============================================================
# Formatage rapport
# ============================================================

def format_report(report: dict) -> str:
    """Formate le rapport pour affichage console."""
    lines = []
    status_icon = {"ok": "OK", "warning": "WARN", "critical": "CRIT", "error": "ERR"}

    lines.append(f"=== Heartbeat Report [{report['timestamp']}] ===")
    lines.append(f"Overall: {status_icon.get(report['overall_status'], '?')} ({report['overall_status']})")
    lines.append("")

    for name, probe in report["probes"].items():
        icon = status_icon.get(probe["status"], "?")
        lines.append(f"  [{icon}] {name}: {probe['message']}")

    if report.get("alerts"):
        lines.append("")
        lines.append("Alerts:")
        for alert in report["alerts"]:
            lines.append(f"  {alert}")

    return "\n".join(lines)


# ============================================================
# Main
# ============================================================

def main() -> int:
    """Point d'entree principal."""
    dry_run = "--dry-run" in sys.argv
    single_probe = None

    # Parse --probe <name>
    if "--probe" in sys.argv:
        idx = sys.argv.index("--probe")
        if idx + 1 < len(sys.argv):
            single_probe = sys.argv[idx + 1]

    if single_probe:
        # Executer une seule probe
        if single_probe not in ALL_PROBES:
            print(f"Probe inconnue: {single_probe}", file=sys.stderr)
            print(f"Probes disponibles: {', '.join(ALL_PROBES.keys())}", file=sys.stderr)
            return 1

        result = ALL_PROBES[single_probe]()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    # Executer toutes les probes
    report = run_all_probes()

    # Afficher le rapport
    print(format_report(report))

    if not dry_run:
        # Stocker en Memory v2
        _store_heartbeat_memory(report)
        # Logger en JSONL
        _log_heartbeat(report)
        print("\nReport stored in Memory v2 and heartbeat.jsonl")

    # Code de retour selon le statut
    if report["overall_status"] == "critical":
        return 2
    elif report["overall_status"] == "warning":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
