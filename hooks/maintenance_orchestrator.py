#!/usr/bin/env python3
"""Orchestrateur de maintenance quotidienne unifie.

Coordonne les 3 composants de maintenance en un seul point d'entree:
1. Vault health check (guardian)
2. Knowledge Watcher status (index, queue, state)
3. Memory consolidation + daily reflection

Gere l'ordre d'execution, les dependances et le rapport unifie.
Concu pour etre invoque par /daily-maintenance ou par cron.

Usage:
    python3 maintenance_orchestrator.py              # Maintenance complete
    python3 maintenance_orchestrator.py --quick       # Health check rapide
    python3 maintenance_orchestrator.py --dry-run     # Rapport sans actions
"""

import json
import sys
import glob
import time
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ajouter hooks au path
_HOOKS_DIR = Path(__file__).resolve().parent
if str(_HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(_HOOKS_DIR))

from lib.paths import DATA_DIR, LOGS_DIR, VAULT_PATH, SKILLS_DIR
from lib.utils import now_paris, log_audit, append_jsonl


# ============================================================
# Configuration
# ============================================================

MAINTENANCE_LOG = LOGS_DIR / "maintenance.jsonl"
WATCHER_DATA = SKILLS_DIR / "knowledge-watcher-skill" / "data"


# ============================================================
# Phase 1: Vault Health Check
# ============================================================

def check_vault_health() -> dict:
    """Diagnostic rapide du vault Obsidian."""
    result = {
        "status": "ok",
        "total_notes": 0,
        "no_frontmatter": 0,
        "broken_links": 0,
        "orphans": 0,
    }

    try:
        if not VAULT_PATH.exists():
            result["status"] = "critical"
            result["message"] = "Vault path not found"
            return result

        md_files = glob.glob(str(VAULT_PATH / "**" / "*.md"), recursive=True)
        result["total_notes"] = len(md_files)

        # Quick frontmatter check
        no_fm = 0
        for f in md_files:
            try:
                with open(f, "r", encoding="utf-8", errors="replace") as fh:
                    first_line = fh.readline().strip()
                    if first_line != "---":
                        no_fm += 1
            except Exception:
                continue
        result["no_frontmatter"] = no_fm

        # Quick broken links check (sample)
        all_notes = {Path(f).stem for f in md_files}
        broken_count = 0
        import re
        wikilink_re = re.compile(r"\[\[([^\]|#]+)")
        for f in md_files[:100]:  # Sample for speed
            try:
                content = Path(f).read_text(encoding="utf-8", errors="replace")
                links = wikilink_re.findall(content)
                for link in links:
                    if link.strip() not in all_notes:
                        broken_count += 1
            except Exception:
                continue
        result["broken_links"] = broken_count

        if no_fm > len(md_files) * 0.1:
            result["status"] = "warning"
        if no_fm > len(md_files) * 0.3:
            result["status"] = "critical"

    except Exception as e:
        result["status"] = "error"
        result["message"] = str(e)[:200]

    return result


# ============================================================
# Phase 2: Knowledge Watcher Status
# ============================================================

def check_watcher_status() -> dict:
    """Verifie l'etat du Knowledge Watcher."""
    result = {
        "status": "ok",
        "queue_pending": 0,
        "index_notes": 0,
        "index_terms": 0,
        "state_hashes": 0,
    }

    try:
        # Queue
        queue_file = WATCHER_DATA / "queue.json"
        if queue_file.exists():
            queue = json.loads(queue_file.read_text(encoding="utf-8"))
            items = queue.get("items", [])
            pending = [i for i in items if i.get("status") == "pending"]
            result["queue_pending"] = len(pending)
            result["queue_total"] = len(items)
        else:
            result["queue_pending"] = 0

        # Index
        index_file = WATCHER_DATA / "notes-index.json"
        if index_file.exists():
            index = json.loads(index_file.read_text(encoding="utf-8"))
            result["index_terms"] = len(index)
            # Count unique note paths
            all_paths = set()
            for paths in index.values():
                if isinstance(paths, list):
                    all_paths.update(paths)
            result["index_notes"] = len(all_paths)

        # State
        state_file = WATCHER_DATA / "state.json"
        if state_file.exists():
            state = json.loads(state_file.read_text(encoding="utf-8"))
            if isinstance(state, dict):
                result["state_hashes"] = len(state)

        # Warn if queue is large
        if result["queue_pending"] > 20:
            result["status"] = "warning"

    except Exception as e:
        result["status"] = "error"
        result["message"] = str(e)[:200]

    return result


# ============================================================
# Phase 3: Memory Consolidation + Reflection
# ============================================================

def run_memory_maintenance(dry_run: bool = False) -> dict:
    """Execute la consolidation memoire et la reflection quotidienne."""
    result = {
        "status": "ok",
        "consolidation": {},
        "reflection": {},
    }

    try:
        # Consolidation
        from memory_consolidator import consolidate
        cons_report = consolidate(dry_run=dry_run)
        result["consolidation"] = cons_report.get("operations", {})
    except Exception as e:
        result["consolidation"] = {"error": str(e)[:200]}
        result["status"] = "warning"

    try:
        # Daily reflection
        from daily_reflect import reflect
        ref_report = reflect(days=1, dry_run=dry_run)
        result["reflection"] = {
            "memories_found": ref_report.get("memories_found", 0),
            "facts_found": ref_report.get("facts_found", 0),
        }
    except Exception as e:
        result["reflection"] = {"error": str(e)[:200]}
        if result["status"] == "ok":
            result["status"] = "warning"

    return result


# ============================================================
# Phase 4: Skills Integrity
# ============================================================

def check_skills_integrity() -> dict:
    """Verification rapide de l'integrite des skills."""
    result = {
        "status": "ok",
        "total_skills": 0,
        "skills_ok": 0,
        "skills_missing_md": [],
    }

    try:
        if not SKILLS_DIR.exists():
            result["status"] = "critical"
            return result

        for d in sorted(SKILLS_DIR.iterdir()):
            if d.is_dir() and d.name not in ("commands", "__pycache__"):
                result["total_skills"] += 1
                if (d / "SKILL.md").exists():
                    result["skills_ok"] += 1
                else:
                    result["skills_missing_md"].append(d.name)

        if result["skills_missing_md"]:
            result["status"] = "warning"

    except Exception as e:
        result["status"] = "error"
        result["message"] = str(e)[:200]

    return result


# ============================================================
# Orchestrateur principal
# ============================================================

def run_maintenance(quick: bool = False, dry_run: bool = False) -> dict:
    """Execute la maintenance orchestree.

    Args:
        quick: Si True, seulement vault health + watcher status (pas de consolidation)
        dry_run: Si True, rapport sans ecriture

    Returns:
        Rapport complet de maintenance
    """
    start_time = time.time()
    report = {
        "timestamp": now_paris(),
        "mode": "quick" if quick else "full",
        "dry_run": dry_run,
        "phases": {},
        "overall_status": "ok",
        "alerts": [],
    }

    # Phases 1, 2, 4 en parallele (independantes)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(check_vault_health): "vault_health",
            executor.submit(check_watcher_status): "watcher_status",
            executor.submit(check_skills_integrity): "skills_integrity",
        }

        for future in as_completed(futures, timeout=30):
            phase_name = futures[future]
            try:
                phase_result = future.result()
                report["phases"][phase_name] = phase_result

                if phase_result.get("status") == "critical":
                    report["overall_status"] = "critical"
                    report["alerts"].append(f"[CRITICAL] {phase_name}")
                elif phase_result.get("status") == "warning":
                    if report["overall_status"] != "critical":
                        report["overall_status"] = "warning"
                    report["alerts"].append(f"[WARNING] {phase_name}")
            except Exception as e:
                report["phases"][phase_name] = {"status": "error", "message": str(e)[:200]}

    # Phase 3: Memory (sequentielle, seulement en mode full)
    if not quick:
        memory_result = run_memory_maintenance(dry_run=dry_run)
        report["phases"]["memory_maintenance"] = memory_result
        if memory_result.get("status") != "ok":
            report["alerts"].append(f"[{memory_result['status'].upper()}] memory_maintenance")

    report["duration_s"] = round(time.time() - start_time, 1)

    # Log
    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        append_jsonl(MAINTENANCE_LOG, {
            "timestamp": report["timestamp"],
            "mode": report["mode"],
            "overall_status": report["overall_status"],
            "duration_s": report["duration_s"],
            "alerts": report["alerts"],
        })
    except Exception:
        pass

    log_audit("maintenance_orchestrator", "maintenance_complete", {
        "mode": report["mode"],
        "status": report["overall_status"],
        "duration_s": report["duration_s"],
        "alerts_count": len(report["alerts"]),
    })

    return report


def format_report(report: dict) -> str:
    """Formate le rapport pour affichage console."""
    lines = []
    lines.append(f"MAINTENANCE QUOTIDIENNE - {report['timestamp'][:10]}")
    lines.append("=" * 50)
    lines.append("")

    # Status par phase
    status_icons = {"ok": "OK", "warning": "WARN", "critical": "FAIL", "error": "ERR"}

    for phase_name, phase_data in report.get("phases", {}).items():
        status = phase_data.get("status", "?")
        icon = status_icons.get(status, "?")
        label = phase_name.replace("_", " ").title()

        detail = ""
        if phase_name == "vault_health":
            detail = f"{phase_data.get('total_notes', '?')} notes, {phase_data.get('no_frontmatter', '?')} sans FM"
        elif phase_name == "watcher_status":
            detail = f"{phase_data.get('queue_pending', '?')} pending, {phase_data.get('index_notes', '?')} indexed"
        elif phase_name == "skills_integrity":
            detail = f"{phase_data.get('skills_ok', '?')}/{phase_data.get('total_skills', '?')} OK"
        elif phase_name == "memory_maintenance":
            cons = phase_data.get("consolidation", {})
            ref = phase_data.get("reflection", {})
            detail = f"memories={ref.get('memories_found', '?')}, facts={ref.get('facts_found', '?')}"

        lines.append(f"  {label:.<30} [{icon}] {detail}")

    lines.append("")
    lines.append(f"  Duration: {report.get('duration_s', '?')}s")
    lines.append(f"  Overall: {report.get('overall_status', '?').upper()}")

    if report.get("alerts"):
        lines.append("")
        lines.append("Alerts:")
        for alert in report["alerts"]:
            lines.append(f"  - {alert}")

    return "\n".join(lines)


# ============================================================
# Main
# ============================================================

def main() -> int:
    quick = "--quick" in sys.argv
    dry_run = "--dry-run" in sys.argv

    report = run_maintenance(quick=quick, dry_run=dry_run)
    print(format_report(report))

    return 0 if report["overall_status"] != "critical" else 1


if __name__ == "__main__":
    sys.exit(main())
