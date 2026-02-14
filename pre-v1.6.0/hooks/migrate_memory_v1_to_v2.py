"""Migration JSONL -> SQLite pour Memory v2.

Migre les donnees existantes:
- signals.jsonl -> sessions table
- insights.jsonl -> memories table (type=insight)
- patterns.jsonl -> memories table (type=pattern)

Deduplication par hash (insights/patterns) et par session_id+timestamp (signals).
Usage: python migrate_memory_v1_to_v2.py [--dry-run]
"""

import sys
import json
from pathlib import Path

# Ajouter hooks au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import MEMORY_DIR, DATA_DIR
from lib.memory_db import ensure_schema, upsert_session, insert_memory, DB_PATH


def load_jsonl(path: Path) -> list[dict]:
    """Charge un fichier JSONL, ignore les lignes invalides."""
    entries = []
    if not path.exists():
        return entries
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def deduplicate_signals(signals: list[dict]) -> list[dict]:
    """Garde le signal le plus recent par session_id."""
    by_session = {}
    for s in signals:
        sid = s.get("session_id", "unknown")
        existing = by_session.get(sid)
        if existing is None or s.get("timestamp", "") > existing.get("timestamp", ""):
            by_session[sid] = s
    return list(by_session.values())


def deduplicate_by_hash(entries: list[dict]) -> list[dict]:
    """Deduplication par hash."""
    seen = set()
    result = []
    for e in entries:
        h = e.get("hash", "")
        if h and h in seen:
            continue
        if h:
            seen.add(h)
        result.append(e)
    return result


def migrate(dry_run: bool = False):
    """Execute la migration."""
    print(f"=== Migration Memory v1 -> v2 ===")
    print(f"Source: {MEMORY_DIR}")
    print(f"Target: {DB_PATH}")
    print(f"Dry run: {dry_run}")
    print()

    # Charger les donnees v1
    signals = load_jsonl(MEMORY_DIR / "signals.jsonl")
    insights = load_jsonl(MEMORY_DIR / "insights.jsonl")
    patterns = load_jsonl(MEMORY_DIR / "patterns.jsonl")

    print(f"Signals bruts: {len(signals)}")
    print(f"Insights bruts: {len(insights)}")
    print(f"Patterns bruts: {len(patterns)}")
    print()

    # Dedupliquer
    signals = deduplicate_signals(signals)
    insights = deduplicate_by_hash(insights)
    patterns = deduplicate_by_hash(patterns)

    print(f"Signals dedupliques: {len(signals)}")
    print(f"Insights dedupliques: {len(insights)}")
    print(f"Patterns dedupliques: {len(patterns)}")
    print()

    if dry_run:
        print("[DRY RUN] Aucune ecriture effectuee.")
        return

    # Assurer le schema
    ensure_schema()

    # Migrer les sessions (depuis signals)
    sessions_ok = 0
    for s in signals:
        is_trivial = s.get("trivial", False)
        # Les anciens signaux n'ont pas de champ trivial explicite
        if "trivial" not in s:
            is_trivial = (
                s.get("complexity", 0) < 5
                and s.get("duration_s", 0) < 300
                and s.get("errors", 0) < 3
                and s.get("insights_count", 0) == 0
                and s.get("patterns_count", 0) == 0
            )

        session_data = {
            "id": s.get("session_id", "unknown"),
            "timestamp": s.get("timestamp", ""),
            "duration_s": s.get("duration_s", 0),
            "complexity": s.get("complexity", 0),
            "message_count": 0,  # Non dispo en v1
            "files_modified": s.get("files_modified", 0),
            "errors_count": s.get("errors", 0),
            "working_directory": "",
            "skills_used": [],
            "topics": [],
            "summary_json": {
                "insights_count": s.get("insights_count", 0),
                "patterns_count": s.get("patterns_count", 0),
            },
            "trivial": is_trivial,
            "success": s.get("errors", 0) < 3,
            "created_at": s.get("timestamp", ""),
        }
        upsert_session(session_data)
        sessions_ok += 1

    print(f"Sessions migrees: {sessions_ok}")

    # Migrer les insights
    insights_ok = 0
    for i in insights:
        content = i.get("content", "")
        if len(content) < 10:
            continue
        memory_data = {
            "session_id": i.get("session_id", "unknown"),
            "type": "insight",
            "content": content,
            "tags": [],
            "importance_score": 6.0,
            "created_at": i.get("timestamp", ""),
            "source_context": f"migrated_v1_hash:{i.get('hash', '')}",
        }
        insert_memory(memory_data)
        insights_ok += 1

    print(f"Insights migres: {insights_ok}")

    # Migrer les patterns
    patterns_ok = 0
    for p in patterns:
        content = p.get("content", "")
        if len(content) < 10:
            continue
        memory_data = {
            "session_id": p.get("session_id", "unknown"),
            "type": "pattern",
            "content": content,
            "tags": [],
            "importance_score": 5.0,
            "created_at": p.get("timestamp", ""),
            "source_context": f"migrated_v1_hash:{p.get('hash', '')}",
        }
        insert_memory(memory_data)
        patterns_ok += 1

    print(f"Patterns migres: {patterns_ok}")
    print()
    print(f"Migration terminee. Base: {DB_PATH}")
    print(f"Taille: {DB_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    migrate(dry_run=is_dry)
