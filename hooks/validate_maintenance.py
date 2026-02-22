#!/usr/bin/env python3
"""Validation 3 niveaux du systeme de maintenance r2d2.

Niveau 1 - Structure : fichiers requis existent, configs parsent
Niveau 2 - Fonctionnel : Python valide, DB accessible, logs writable
Niveau 3 - Integration : orchestrateur dry-run, memory cycle, cache

Usage:
    python validate_maintenance.py              # Validation complete
    python validate_maintenance.py --level 1    # Structure seulement
    python validate_maintenance.py --json       # Sortie JSON

Invocable depuis /validate --maintenance
"""

import ast
import json
import sqlite3
import sys
import time
from pathlib import Path

# Paths
_HOOKS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_HOOKS_DIR))

from lib.paths import (
    HOOKS_DIR, LOGS_DIR, CONFIG_DIR, DATA_DIR,
    SKILLS_DIR, VAULT_PATH, MEMORY_DIR,
)


# ============================================================
# Level 1: Structure & Syntax
# ============================================================

def validate_structure() -> dict:
    """Verifie que tous les fichiers de maintenance existent et sont valides."""
    result = {"status": "PASS", "checks": [], "issues": []}

    # Required Python files
    required_python = [
        HOOKS_DIR / "maintenance_orchestrator.py",
        HOOKS_DIR / "memory_consolidator.py",
        HOOKS_DIR / "daily_reflect.py",
        HOOKS_DIR / "heartbeat.py",
        HOOKS_DIR / "heartbeat_checks.py",
        HOOKS_DIR / "load_context.py",
        HOOKS_DIR / "memory_extractor_v2.py",
        HOOKS_DIR / "prompt_analyzer.py",
        HOOKS_DIR / "security_validator.py",
        HOOKS_DIR / "path_guard.py",
        HOOKS_DIR / "error_capture.py",
        HOOKS_DIR / "notify_write.py",
        HOOKS_DIR / "notify_complete.py",
        HOOKS_DIR / "pre_compact_flush.py",
        HOOKS_DIR / "subagent_capture.py",
    ]

    required_libs = [
        HOOKS_DIR / "lib" / "paths.py",
        HOOKS_DIR / "lib" / "utils.py",
        HOOKS_DIR / "lib" / "memory_db.py",
        HOOKS_DIR / "lib" / "memory_retriever.py",
        HOOKS_DIR / "lib" / "memory_search.py",
        HOOKS_DIR / "lib" / "embeddings.py",
        HOOKS_DIR / "lib" / "context_cache.py",
    ]

    for f in required_python + required_libs:
        if f.exists():
            result["checks"].append({"file": f.name, "status": "OK"})
        else:
            result["issues"].append(f"MISSING: {f.relative_to(HOOKS_DIR)}")
            result["status"] = "FAIL"

    # Required config files
    required_configs = [
        CONFIG_DIR / "memory_v2.yaml",
        CONFIG_DIR / "security_rules.yaml",
        CONFIG_DIR / "router_rules.yaml",
        CONFIG_DIR / "memory_rules.yaml",
    ]

    for f in required_configs:
        if f.exists():
            # Try parse
            try:
                import yaml
                yaml.safe_load(f.read_text(encoding="utf-8"))
                result["checks"].append({"file": f.name, "status": "OK"})
            except ImportError:
                # yaml not available, just check existence
                result["checks"].append({"file": f.name, "status": "OK (no yaml)"})
            except Exception as e:
                result["issues"].append(f"PARSE ERROR: {f.name}: {str(e)[:100]}")
                result["status"] = "FAIL"
        else:
            result["issues"].append(f"MISSING CONFIG: {f.name}")
            result["status"] = "FAIL"

    # Required directories
    required_dirs = [LOGS_DIR, DATA_DIR, MEMORY_DIR, CONFIG_DIR]
    for d in required_dirs:
        if d.exists() and d.is_dir():
            result["checks"].append({"dir": d.name, "status": "OK"})
        else:
            result["issues"].append(f"MISSING DIR: {d.relative_to(HOOKS_DIR)}")
            result["status"] = "FAIL"

    # Knowledge Watcher structure
    kw_dir = SKILLS_DIR / "knowledge-watcher-skill"
    kw_files = [
        kw_dir / "config" / "config.json",
        kw_dir / "config" / "rules.json",
        kw_dir / "config" / "sources.json",
        kw_dir / "scripts" / "start-knowledge-watcher.sh",
        kw_dir / "scripts" / "invoke-queue-processor.sh",
    ]
    for f in kw_files:
        if f.exists():
            if f.suffix == ".json":
                try:
                    json.loads(f.read_text(encoding="utf-8"))
                    result["checks"].append({"file": f.name, "status": "OK"})
                except Exception as e:
                    result["issues"].append(f"PARSE ERROR: {f.name}: {str(e)[:100]}")
                    result["status"] = "FAIL"
            else:
                result["checks"].append({"file": f.name, "status": "OK"})
        else:
            result["issues"].append(f"MISSING KW: {f.name}")
            if result["status"] == "PASS":
                result["status"] = "WARN"

    return result


# ============================================================
# Level 2: Functional
# ============================================================

def validate_functional() -> dict:
    """Verifie que les composants fonctionnent individuellement."""
    result = {"status": "PASS", "checks": [], "issues": []}

    # AST parse all Python files
    python_files = list(HOOKS_DIR.glob("*.py")) + list((HOOKS_DIR / "lib").glob("*.py"))
    parse_ok = 0
    parse_fail = 0

    for f in python_files:
        if f.name.startswith("_") or f.name == "__init__.py":
            continue
        try:
            source = f.read_text(encoding="utf-8", errors="replace")
            ast.parse(source)
            parse_ok += 1
        except SyntaxError as e:
            parse_fail += 1
            result["issues"].append(f"SYNTAX ERROR: {f.name}:{e.lineno}: {e.msg}")
            result["status"] = "FAIL"

    result["checks"].append({
        "check": "Python AST parse",
        "status": "OK" if parse_fail == 0 else "FAIL",
        "ok": parse_ok,
        "fail": parse_fail,
    })

    # Memory DB integrity
    db_path = DATA_DIR / "memory.db"
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path), timeout=3.0)
            # Integrity check
            integrity = conn.execute("PRAGMA integrity_check").fetchone()
            if integrity[0] == "ok":
                result["checks"].append({"check": "SQLite integrity", "status": "OK"})
            else:
                result["issues"].append(f"DB INTEGRITY: {integrity[0]}")
                result["status"] = "FAIL"

            # Check tables exist
            tables = {row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()}
            expected_tables = {"sessions", "memories", "facts", "retrieval_log", "vectors"}
            missing = expected_tables - tables
            if missing:
                result["issues"].append(f"MISSING TABLES: {missing}")
                result["status"] = "FAIL"
            else:
                result["checks"].append({
                    "check": "DB tables",
                    "status": "OK",
                    "tables": len(tables),
                })

            # Record counts
            counts = {}
            for table in expected_tables & tables:
                try:
                    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                    counts[table] = count
                except Exception:
                    counts[table] = -1
            result["checks"].append({"check": "DB records", "counts": counts})

            conn.close()
        except Exception as e:
            result["issues"].append(f"DB ERROR: {str(e)[:200]}")
            result["status"] = "FAIL"
    else:
        result["issues"].append("MISSING: memory.db")
        result["status"] = "WARN"

    # Logs directory writable
    try:
        test_file = LOGS_DIR / ".validate_test"
        test_file.write_text("test", encoding="utf-8")
        test_file.unlink()
        result["checks"].append({"check": "Logs writable", "status": "OK"})
    except Exception as e:
        result["issues"].append(f"LOGS NOT WRITABLE: {e}")
        result["status"] = "FAIL"

    # Context cache functional
    try:
        from lib.context_cache import get_or_compute_context
        ctx = get_or_compute_context()
        if ctx and "skills_list" in ctx:
            result["checks"].append({
                "check": "Context cache",
                "status": "OK",
                "skills": len(ctx.get("skills_list", [])),
                "vault_notes": ctx.get("vault_note_count", 0),
            })
        else:
            result["issues"].append("Context cache returned empty data")
            result["status"] = "WARN"
    except Exception as e:
        result["issues"].append(f"CONTEXT CACHE ERROR: {str(e)[:100]}")
        result["status"] = "WARN"

    # Vault accessible
    if VAULT_PATH.exists():
        import glob
        note_count = len(glob.glob(str(VAULT_PATH / "**" / "*.md"), recursive=True))
        result["checks"].append({
            "check": "Vault accessible",
            "status": "OK",
            "notes": note_count,
        })
    else:
        result["issues"].append(f"VAULT NOT FOUND: {VAULT_PATH}")
        result["status"] = "WARN"

    return result


# ============================================================
# Level 3: Integration
# ============================================================

def validate_integration() -> dict:
    """Verifie que les composants fonctionnent ensemble."""
    result = {"status": "PASS", "checks": [], "issues": []}

    # Test 1: Maintenance orchestrator dry-run
    try:
        from maintenance_orchestrator import run_maintenance
        report = run_maintenance(quick=True, dry_run=True)

        overall = report.get("overall_status", "error")
        phases = report.get("phases", {})

        result["checks"].append({
            "check": "Orchestrator dry-run",
            "status": "OK" if overall != "critical" else "FAIL",
            "overall": overall,
            "phases": len(phases),
            "duration_s": report.get("duration_s", -1),
        })

        if overall == "critical":
            result["issues"].append(f"ORCHESTRATOR CRITICAL: {report.get('alerts', [])}")
            result["status"] = "FAIL"

    except Exception as e:
        result["issues"].append(f"ORCHESTRATOR ERROR: {str(e)[:200]}")
        result["status"] = "FAIL"

    # Test 2: Memory DB read + retriever import
    try:
        from lib.memory_db import ensure_schema, get_recent_memories, _get_connection
        ensure_schema()

        # Read test: can we query memories?
        recent = get_recent_memories(days=7, min_importance=0.0, limit=5)
        result["checks"].append({
            "check": "Memory DB read",
            "status": "OK",
            "recent_count": len(recent),
        })

        # Import retriever (validates the full chain)
        from lib.memory_retriever import retrieve_for_startup
        result["checks"].append({"check": "Memory retriever import", "status": "OK"})

    except Exception as e:
        result["issues"].append(f"MEMORY ERROR: {str(e)[:200]}")
        result["status"] = "FAIL"

    # Test 3: TF-IDF classifier availability
    try:
        clf_path = SKILLS_DIR / "knowledge-watcher-skill" / "processors" / "tfidf_classifier.py"
        if clf_path.exists():
            # Check if model is trained
            model_path = SKILLS_DIR / "knowledge-watcher-skill" / "data" / "tfidf-model.json"
            if model_path.exists():
                model = json.loads(model_path.read_text(encoding="utf-8"))
                result["checks"].append({
                    "check": "TF-IDF classifier",
                    "status": "OK",
                    "categories": model.get("categories", []),
                    "vocabulary": model.get("idf_size", 0),
                })
            else:
                result["checks"].append({
                    "check": "TF-IDF classifier",
                    "status": "WARN (not trained)",
                })
                result["issues"].append("TF-IDF model not trained yet")
        else:
            result["checks"].append({"check": "TF-IDF classifier", "status": "MISSING"})
            result["issues"].append("TF-IDF classifier not found")
    except Exception as e:
        result["issues"].append(f"TF-IDF CHECK ERROR: {str(e)[:100]}")

    # Test 4: Hooks config consistency
    try:
        import yaml
        config_files = list(CONFIG_DIR.glob("*.yaml")) + list(CONFIG_DIR.glob("*.yml"))
        all_valid = True
        for cf in config_files:
            try:
                yaml.safe_load(cf.read_text(encoding="utf-8"))
            except Exception as e:
                result["issues"].append(f"CONFIG INVALID: {cf.name}: {str(e)[:100]}")
                all_valid = False

        if all_valid:
            result["checks"].append({
                "check": "Config consistency",
                "status": "OK",
                "config_files": len(config_files),
            })
        else:
            result["status"] = "FAIL"
    except ImportError:
        result["checks"].append({"check": "Config consistency", "status": "SKIP (no yaml)"})

    return result


# ============================================================
# Report formatting
# ============================================================

def format_report(levels: dict) -> str:
    """Formate le rapport de validation."""
    lines = []
    lines.append("MAINTENANCE VALIDATION REPORT")
    lines.append("=" * 50)
    lines.append("")

    overall_status = "PASS"
    total_issues = 0

    for level_name, level_data in levels.items():
        status = level_data["status"]
        issues = level_data.get("issues", [])
        checks = level_data.get("checks", [])
        total_issues += len(issues)

        if status == "FAIL":
            overall_status = "FAIL"
        elif status == "WARN" and overall_status == "PASS":
            overall_status = "WARN"

        label = {
            "structure": "Niveau 1 - Structure",
            "functional": "Niveau 2 - Fonctionnel",
            "integration": "Niveau 3 - Integration",
        }.get(level_name, level_name)

        checks_ok = sum(1 for c in checks if c.get("status", "").startswith("OK"))
        lines.append(f"  {label:.<35} [{status:>4}] {checks_ok}/{len(checks)} checks OK")

        for issue in issues:
            lines.append(f"    - {issue}")

    lines.append("")
    lines.append(f"  Overall: {overall_status}")
    lines.append(f"  Issues:  {total_issues}")

    # Score
    score_map = {"PASS": 10, "WARN": 7, "FAIL": 3}
    scores = [score_map.get(l["status"], 0) for l in levels.values()]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
    lines.append(f"  Score:   {avg_score}/10")

    if total_issues > 0:
        lines.append("")
        lines.append("Recommandations:")
        for level_data in levels.values():
            for issue in level_data.get("issues", []):
                if "MISSING" in issue:
                    lines.append(f"  - Creer/restaurer: {issue.split(':')[-1].strip()}")
                elif "SYNTAX" in issue:
                    lines.append(f"  - Corriger: {issue}")
                elif "INTEGRITY" in issue:
                    lines.append(f"  - Reparer DB: PRAGMA integrity_check")

    return "\n".join(lines)


# ============================================================
# Main
# ============================================================

def run_validation(max_level: int = 3) -> dict:
    """Execute la validation jusqu'au niveau specifie."""
    results = {}

    results["structure"] = validate_structure()

    if max_level >= 2 and results["structure"]["status"] != "FAIL":
        results["functional"] = validate_functional()
    elif max_level >= 2:
        results["functional"] = {"status": "SKIP", "checks": [], "issues": ["Skipped: Level 1 failed"]}

    if max_level >= 3:
        results["integration"] = validate_integration()

    return results


def main() -> int:
    max_level = 3
    json_output = "--json" in sys.argv

    if "--level" in sys.argv:
        idx = sys.argv.index("--level")
        if idx + 1 < len(sys.argv):
            try:
                max_level = int(sys.argv[idx + 1])
            except ValueError:
                pass

    results = run_validation(max_level)

    if json_output:
        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))
    else:
        print(format_report(results))

    overall = all(r["status"] in ("PASS", "WARN", "SKIP") for r in results.values())
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
