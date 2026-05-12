#!/usr/bin/env python3
"""Reflection quotidienne - promotion et resume des memoires.

Revise les memoires des dernieres 24h et genere un resume quotidien.
Invoque egalement la consolidation (decay, merge, prune, promote).
Concu pour etre lance par cron une fois par jour.

Usage:
    python3 daily_reflect.py              # Reflection complete
    python3 daily_reflect.py --dry-run    # Rapport sans ecriture
    python3 daily_reflect.py --days 3     # Revue des N derniers jours

Aucune dependance externe (pas d'Agent SDK). Pure Python + Memory v2.
Inspire du Second Brain (Dynamous Community), adapte pour AdminSysteme.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Ajouter hooks au path
_HOOKS_DIR = Path(__file__).resolve().parent
if str(_HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(_HOOKS_DIR))

from lib.paths import DATA_DIR, LOGS_DIR
from lib.memory_db import get_recent_memories, get_high_confidence_facts, get_stats
from lib.utils import now_paris, log_audit, append_jsonl
from memory_consolidator import consolidate


# ============================================================
# Configuration
# ============================================================

DAILY_DIR = DATA_DIR / "daily"
REFLECT_LOG = LOGS_DIR / "daily-reflect.jsonl"


# ============================================================
# Collecte des memoires recentes
# ============================================================

def _collect_recent_memories(days: int = 1) -> list[dict]:
    """Recupere toutes les memoires des N derniers jours."""
    return get_recent_memories(
        days=days,
        min_importance=0.0,
        limit=100,
    )


def _collect_recent_facts() -> list[dict]:
    """Recupere les facts haute-confiance."""
    return get_high_confidence_facts(min_confidence=0.5, limit=20)


# ============================================================
# Generation du resume quotidien
# ============================================================

def _group_by_type(memories: list[dict]) -> dict[str, list[dict]]:
    """Groupe les memoires par type."""
    groups = {}
    for m in memories:
        mtype = m.get("type", "unknown")
        if mtype not in groups:
            groups[mtype] = []
        groups[mtype].append(m)
    return groups


def _format_daily_summary(memories: list[dict], facts: list[dict],
                          consolidation_report: dict, date_str: str) -> str:
    """Genere un resume quotidien en Markdown."""
    lines = [
        f"# Resume quotidien - {date_str}",
        f"",
        f"*Genere automatiquement par daily_reflect.py*",
        f"",
    ]

    # Stats globales
    stats = get_stats()
    lines.append("## Statistiques memoire")
    lines.append(f"- Memoires totales: {stats.get('memories_count', 0)}")
    lines.append(f"- Facts: {stats.get('facts_count', 0)}")
    lines.append(f"- Sessions: {stats.get('sessions_count', 0)}")
    lines.append("")

    # Memoires par type
    if memories:
        groups = _group_by_type(memories)
        lines.append(f"## Memoires recentes ({len(memories)} total)")
        lines.append("")

        type_labels = {
            "tool_sequence": "Sequences d'outils",
            "problem_solution": "Problemes resolus",
            "decision": "Decisions",
            "insight": "Insights",
            "pattern": "Patterns",
            "heartbeat": "Heartbeat monitoring",
            "pre_compact": "Contexte sauvegarde",
        }

        for mtype, mems in sorted(groups.items()):
            label = type_labels.get(mtype, mtype.capitalize())
            lines.append(f"### {label} ({len(mems)})")
            for m in mems[:5]:
                importance = m.get("importance_score", 0)
                content = m.get("content", "")[:120]
                lines.append(f"- [{importance:.0f}] {content}")
            if len(mems) > 5:
                lines.append(f"- ... et {len(mems) - 5} autres")
            lines.append("")

    # Facts
    if facts:
        lines.append(f"## Facts ({len(facts)})")
        for f in facts[:10]:
            lines.append(f"- **{f.get('key', '?')}**: {f.get('value', '')[:100]}")
        lines.append("")

    # Consolidation
    ops = consolidation_report.get("operations", {})
    lines.append("## Consolidation")
    for op_name, details in ops.items():
        if isinstance(details, dict):
            lines.append(f"- {op_name}: {details}")
        else:
            lines.append(f"- {op_name}: {details}")
    lines.append("")

    return "\n".join(lines)


# ============================================================
# Main
# ============================================================

def reflect(days: int = 1, dry_run: bool = False) -> dict:
    """Execute la reflection quotidienne. Retourne un rapport."""
    date_str = datetime.now().strftime("%Y-%m-%d")

    report = {
        "timestamp": now_paris(),
        "date": date_str,
        "dry_run": dry_run,
        "days_reviewed": days,
    }

    # 1. Collecter les memoires recentes
    memories = _collect_recent_memories(days=days)
    facts = _collect_recent_facts()
    report["memories_found"] = len(memories)
    report["facts_found"] = len(facts)

    # 2. Lancer la consolidation
    print(f"Running consolidation (dry_run={dry_run})...")
    consolidation_report = consolidate(dry_run=dry_run)
    report["consolidation"] = consolidation_report.get("operations", {})

    # 3. Generer le resume quotidien
    summary = _format_daily_summary(memories, facts, consolidation_report, date_str)
    report["summary_length"] = len(summary)

    # 4. Ecrire le fichier daily
    if not dry_run:
        DAILY_DIR.mkdir(parents=True, exist_ok=True)
        daily_path = DAILY_DIR / f"{date_str}.md"

        # Si le fichier existe deja, on append
        if daily_path.exists():
            existing = daily_path.read_text(encoding="utf-8")
            summary = existing + "\n\n---\n\n" + summary

        daily_path.write_text(summary, encoding="utf-8")
        report["daily_path"] = str(daily_path)
        print(f"Daily summary written to {daily_path}")

    # 5. Logger
    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        append_jsonl(REFLECT_LOG, {
            "timestamp": report["timestamp"],
            "date": date_str,
            "memories_found": len(memories),
            "facts_found": len(facts),
            "dry_run": dry_run,
        })
    except Exception:
        pass

    log_audit("daily_reflect", "reflection", {
        "date": date_str,
        "memories": len(memories),
        "facts": len(facts),
        "dry_run": dry_run,
    })

    return report


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    days = 1

    if "--days" in sys.argv:
        idx = sys.argv.index("--days")
        if idx + 1 < len(sys.argv):
            try:
                days = int(sys.argv[idx + 1])
            except ValueError:
                print("--days doit etre un entier", file=sys.stderr)
                return 1

    print(f"=== Daily Reflection ===")
    print(f"Days to review: {days}")
    print(f"Dry run: {dry_run}")
    print()

    report = reflect(days=days, dry_run=dry_run)

    print(f"\n--- Report ---")
    print(f"Memories found: {report['memories_found']}")
    print(f"Facts found: {report['facts_found']}")
    print(f"Summary length: {report['summary_length']} chars")

    if not dry_run and "daily_path" in report:
        print(f"Written to: {report['daily_path']}")

    print(f"\nConsolidation:")
    for op, details in report.get("consolidation", {}).items():
        print(f"  {op}: {details}")

    print("\nReflection terminee.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
