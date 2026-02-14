"""Consolidation periodique de la base memoire v2.

Operations:
1. Decay: reduit decay_score des memoires non accedees depuis N jours
2. Merge: fusionne les memoires similaires (>60% mots communs)
3. Prune: supprime les memoires a score effectif bas et agees
4. Promote: booste les memoires frequemment accedees
5. Resume: genere un resume des statistiques

Usage:
  python memory_consolidator.py              # Consolidation complete
  python memory_consolidator.py --dry-run    # Rapport sans modification
  python memory_consolidator.py --stats      # Stats uniquement
"""

import sys
import json
import re
from pathlib import Path

# Ajouter hooks au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import CONFIG_DIR, VAULT_PATH
from lib.memory_db import (
    apply_decay, prune_low_score, promote_frequently_accessed,
    get_all_memories_for_merge, merge_memories, get_stats,
    DB_PATH,
)
from lib.utils import now_paris, log_audit


# ============================================================
# Configuration
# ============================================================

def _load_consolidation_config() -> dict:
    """Charge la section consolidation de memory_v2.yaml."""
    defaults = {
        "decay_threshold_days": 7,
        "decay_factor": 0.9,
        "prune_min_score": 0.5,
        "prune_min_age_days": 30,
        "promote_min_access": 3,
        "promote_boost": 1.0,
        "merge_similarity_threshold": 0.6,
    }
    try:
        config_path = CONFIG_DIR / "memory_v2.yaml"
        if config_path.exists():
            import yaml
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            consolidation = raw.get("consolidation", {})
            for key in defaults:
                if key in consolidation:
                    defaults[key] = consolidation[key]
    except Exception:
        pass
    return defaults


# ============================================================
# Merge logic
# ============================================================

def _tokenize(text: str) -> set[str]:
    """Tokenise un texte en ensemble de mots significatifs."""
    words = re.findall(r"\b[a-zA-Z_][\w.-]{2,}\b", text.lower())
    stopwords = {"the", "a", "an", "is", "are", "was", "to", "of", "in", "for",
                 "on", "with", "and", "but", "or", "not", "le", "la", "les",
                 "de", "du", "des", "un", "une", "et", "en", "est"}
    return {w for w in words if w not in stopwords}


def _similarity(text_a: str, text_b: str) -> float:
    """Calcule la similarite Jaccard entre deux textes."""
    tokens_a = _tokenize(text_a)
    tokens_b = _tokenize(text_b)
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union) if union else 0.0


def find_merge_candidates(memories: list[dict], threshold: float = 0.6) -> list[tuple[int, int]]:
    """Trouve les paires de memoires similaires a fusionner.

    Retourne des paires (keep_id, remove_id) ou keep_id a le meilleur score.
    """
    candidates = []
    n = len(memories)

    for i in range(n):
        for j in range(i + 1, n):
            # Seulement merger le meme type
            if memories[i].get("type") != memories[j].get("type"):
                continue

            sim = _similarity(
                memories[i].get("content", ""),
                memories[j].get("content", ""),
            )
            if sim >= threshold:
                # Garder celui avec le meilleur score effectif
                score_i = (memories[i].get("importance_score", 5.0) *
                          memories[i].get("decay_score", 1.0))
                score_j = (memories[j].get("importance_score", 5.0) *
                          memories[j].get("decay_score", 1.0))

                if score_i >= score_j:
                    candidates.append((memories[i]["id"], memories[j]["id"]))
                else:
                    candidates.append((memories[j]["id"], memories[i]["id"]))

    return candidates


# ============================================================
# Main consolidation
# ============================================================

def consolidate(dry_run: bool = False) -> dict:
    """Execute la consolidation complete. Retourne un rapport."""
    config = _load_consolidation_config()
    report = {
        "timestamp": now_paris(),
        "dry_run": dry_run,
        "stats_before": get_stats(),
        "operations": {},
    }

    # 1. Decay
    if dry_run:
        report["operations"]["decay"] = "would apply decay (factor={}, threshold={}d)".format(
            config["decay_factor"], config["decay_threshold_days"])
    else:
        affected = apply_decay(
            days_threshold=config["decay_threshold_days"],
            decay_factor=config["decay_factor"],
        )
        report["operations"]["decay"] = {"affected": affected}

    # 2. Merge
    memories = get_all_memories_for_merge()
    merge_pairs = find_merge_candidates(memories, config["merge_similarity_threshold"])
    if dry_run:
        report["operations"]["merge"] = {
            "candidates": len(merge_pairs),
            "pairs_preview": [(k, r) for k, r in merge_pairs[:5]],
        }
    else:
        merged = 0
        # Eviter de supprimer un ID deja supprime
        removed_ids = set()
        for keep_id, remove_id in merge_pairs:
            if remove_id not in removed_ids and keep_id not in removed_ids:
                merge_memories(keep_id, remove_id)
                removed_ids.add(remove_id)
                merged += 1
        report["operations"]["merge"] = {"merged": merged}

    # 3. Prune
    if dry_run:
        report["operations"]["prune"] = "would prune (min_score={}, min_age={}d)".format(
            config["prune_min_score"], config["prune_min_age_days"])
    else:
        pruned = prune_low_score(
            min_effective_score=config["prune_min_score"],
            min_age_days=config["prune_min_age_days"],
        )
        report["operations"]["prune"] = {"pruned": pruned}

    # 4. Promote
    if dry_run:
        report["operations"]["promote"] = "would promote (min_access={}, boost={})".format(
            config["promote_min_access"], config["promote_boost"])
    else:
        promoted = promote_frequently_accessed(
            min_access=config["promote_min_access"],
            boost=config["promote_boost"],
        )
        report["operations"]["promote"] = {"promoted": promoted}

    report["stats_after"] = get_stats()

    # Log audit
    log_audit("memory_consolidator", "consolidation", {
        "dry_run": dry_run,
        "operations": report["operations"],
    })

    return report


def print_stats():
    """Affiche les statistiques de la base memoire."""
    stats = get_stats()
    print("=== Memory v2 Statistics ===")
    print(f"Database: {DB_PATH}")
    if DB_PATH.exists():
        print(f"Size: {DB_PATH.stat().st_size / 1024:.1f} KB")
    print(f"Sessions: {stats.get('sessions_count', 0)}")
    print(f"Memories: {stats.get('memories_count', 0)}")
    print(f"  By type: {stats.get('memories_by_type', {})}")
    print(f"  Avg effective score: {stats.get('avg_effective_score', 0)}")
    print(f"Facts: {stats.get('facts_count', 0)}")
    print(f"Retrievals: {stats.get('retrievals_count', 0)}")


def main():
    if "--stats" in sys.argv:
        print_stats()
        return

    dry_run = "--dry-run" in sys.argv
    print("=== Memory v2 Consolidation ===")
    print(f"Dry run: {dry_run}")
    print()

    report = consolidate(dry_run=dry_run)

    print("--- Stats Before ---")
    for k, v in report["stats_before"].items():
        print(f"  {k}: {v}")
    print()

    print("--- Operations ---")
    for op, details in report["operations"].items():
        print(f"  {op}: {details}")
    print()

    print("--- Stats After ---")
    for k, v in report["stats_after"].items():
        print(f"  {k}: {v}")
    print()

    print("Consolidation terminee.")


if __name__ == "__main__":
    main()
