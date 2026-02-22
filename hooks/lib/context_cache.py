"""Cache fichier TTL pour les donnees de contexte partagees entre hooks.

Evite les scans redondants (skills, vault, router_rules) qui sont executes
par load_context.py (SessionStart) et prompt_analyzer.py (UserPromptSubmit).

Cache stocke dans hooks/data/.context_cache.json avec TTL configurable (defaut 5 min).
Chaque hook consulte le cache avant de scanner. Le premier a expirer regenere.
"""

import json
import time
from pathlib import Path

from .paths import DATA_DIR, SKILLS_DIR, VAULT_PATH, CONFIG_DIR

CACHE_PATH = DATA_DIR / ".context_cache.json"
CACHE_TTL_S = 300  # 5 minutes


def _is_cache_valid() -> bool:
    """Verifie si le cache existe et n'est pas expire."""
    try:
        if not CACHE_PATH.exists():
            return False
        age = time.time() - CACHE_PATH.stat().st_mtime
        return age < CACHE_TTL_S
    except Exception:
        return False


def get_cached_context() -> dict | None:
    """Retourne le cache si valide, None sinon."""
    if not _is_cache_valid():
        return None
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None


def update_cache(data: dict) -> None:
    """Ecrit les donnees dans le cache."""
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def get_or_compute_context() -> dict:
    """Retourne le contexte depuis le cache ou le recalcule.

    Donnees cachees: skills_list, skills_count, vault_note_count, router_rules.
    """
    cached = get_cached_context()
    if cached:
        return cached

    import glob

    # Skills
    skills = []
    try:
        if SKILLS_DIR.exists():
            for d in sorted(SKILLS_DIR.iterdir()):
                if d.is_dir() and (d / "SKILL.md").exists() and d.name != "commands":
                    skills.append(d.name)
    except Exception:
        pass

    # Vault notes count
    vault_count = 0
    try:
        if VAULT_PATH.exists():
            vault_count = len(glob.glob(str(VAULT_PATH / "**" / "*.md"), recursive=True))
    except Exception:
        pass

    # Router rules
    router_rules = {}
    try:
        rules_file = CONFIG_DIR / "router_rules.yaml"
        if rules_file.exists():
            import yaml
            router_rules = yaml.safe_load(rules_file.read_text(encoding="utf-8")) or {}
    except Exception:
        pass

    data = {
        "skills_list": skills,
        "skills_count": len(skills),
        "vault_note_count": vault_count,
        "router_rules": router_rules,
    }

    update_cache(data)
    return data
