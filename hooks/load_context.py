"""SessionStart hook: charge le contexte systeme r2d2 au demarrage.

Injecte un additionalContext avec:
- Liste des skills actifs
- Nombre de notes dans le vault
- Date de derniere maintenance guardian
- Memory v2: memoires recentes injectees au demarrage
- Compass R2D2 (palais temporel, ajoute 2026-04-09)
"""

import sys
import re
import glob
from pathlib import Path

# Ajouter le dossier hooks au path pour imports relatifs
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import SKILLS_DIR, VAULT_PATH, PERSONALITY_DIR
from lib.context_cache import get_or_compute_context
from lib.utils import read_stdin_json, log_audit, output_json, now_paris, check_critical_error, clear_critical_error


def get_active_skills() -> list[str]:
    """Detecte les skills actifs par scan filesystem (methode primaire).

    Un skill est actif s'il a un dossier avec un SKILL.md dedans.
    Plus robuste que parser le tableau markdown du meta-router.
    """
    try:
        if not SKILLS_DIR.exists():
            return []
        skills = []
        for d in sorted(SKILLS_DIR.iterdir()):
            if d.is_dir() and (d / "SKILL.md").exists() and d.name != "commands":
                skills.append(d.name)
        return skills
    except Exception:
        return []


def count_vault_notes() -> int:
    """Compte les fichiers .md dans le vault."""
    try:
        if not VAULT_PATH.exists():
            return 0
        return len(glob.glob(str(VAULT_PATH / "**" / "*.md"), recursive=True))
    except Exception:
        return 0


def get_last_guardian_date() -> str:
    """Cherche la date de derniere maintenance guardian."""
    try:
        guardian_dir = SKILLS_DIR / "vault-guardian-skill"
        # Chercher dans les logs/data du guardian
        for pattern in ["data/last-run.json", "data/health-report.json", "logs/*.log"]:
            matches = glob.glob(str(guardian_dir / pattern))
            if matches:
                latest = max(matches, key=lambda f: Path(f).stat().st_mtime)
                from datetime import datetime
                mtime = Path(latest).stat().st_mtime
                return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        # Fallback: chercher les notes de type guardian dans le vault
        guardian_notes = glob.glob(str(VAULT_PATH / "**" / "*guardian*"), recursive=True)
        if guardian_notes:
            latest = max(guardian_notes, key=lambda f: Path(f).stat().st_mtime)
            from datetime import datetime
            mtime = Path(latest).stat().st_mtime
            return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        return "inconnue"
    except Exception:
        return "inconnue"


def load_compass_summary() -> str:
    """Charge le compass R2D2 depuis R2D2-Memory/compass.md (palais temporel).

    Le compass contient la boussole subjective (ici/maintenant/avant/apres/la-bas)
    + les regles operationnelles + les archetypes actifs. Lu au SessionStart
    pour que R2D2 se situe des le reveil sans relire tout l'historique.

    Max ~1500 chars injectes dans le contexte.
    Fail-open : retourne "" si fichier absent ou illisible.

    Added: 2026-04-09 — connexion palais temporel (wing_r2d2_temporal) au runtime.
    """
    try:
        compass_path = Path("C:/Users/r2d2/Documents/R2D2-Memory/compass.md")
        if not compass_path.exists():
            return ""

        content = compass_path.read_text(encoding="utf-8")

        # Extraire les sections utiles (skip frontmatter + headers intro)
        # On garde : ICI, MAINTENANT, APRES (les plus actionnables)
        # + regles operationnelles (top 5)
        # + derniers signaux Mike
        sections = {"ici": "", "maintenant": "", "apres": "", "regles": "", "signaux": ""}
        current = None
        lines = content.split("\n")

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("### ICI"):
                current = "ici"
                continue
            elif stripped.startswith("### MAINTENANT"):
                current = "maintenant"
                continue
            elif stripped.startswith("### APRES"):
                current = "apres"
                continue
            elif stripped.startswith("## Regles operationnelles"):
                current = "regles"
                continue
            elif stripped.startswith("## Dernier signal"):
                current = "signaux"
                continue
            elif stripped.startswith("###") or stripped.startswith("## "):
                current = None
                continue

            if current and stripped and not stripped.startswith(">"):
                sections[current] += stripped + " "

        # Compacter et limiter
        parts = []
        if sections["ici"]:
            parts.append(f"ICI: {sections['ici'].strip()[:300]}")
        if sections["maintenant"]:
            parts.append(f"NOW: {sections['maintenant'].strip()[:300]}")
        if sections["apres"]:
            parts.append(f"NEXT: {sections['apres'].strip()[:250]}")
        if sections["regles"]:
            # Prendre les 5 premieres regles (lignes qui commencent par un chiffre)
            regles_lines = [l for l in sections["regles"].split(". ") if l.strip()][:5]
            parts.append("REGLES: " + " | ".join(regles_lines)[:400])
        if sections["signaux"]:
            parts.append(f"SIGNAUX: {sections['signaux'].strip()[:200]}")

        result = "\n".join(parts)
        # Hard cap a 1500 chars pour ne pas surcharger le contexte
        if len(result) > 1500:
            result = result[:1500] + "..."

        return result

    except Exception:
        return ""


def load_personality_summary() -> str:
    """Charge un resume compact des fichiers personnalite (SOUL, USER, MEMORY).

    Extrait les sections cles de chaque fichier pour injection dans le contexte.
    Max ~500 chars au total pour ne pas surcharger le contexte.
    """
    try:
        if not PERSONALITY_DIR.exists():
            return ""

        parts = []

        # SOUL.md: extraire identite et style
        soul_path = PERSONALITY_DIR / "SOUL.md"
        if soul_path.exists():
            content = soul_path.read_text(encoding="utf-8")
            # Extraire la premiere ligne descriptive (apres le titre)
            for line in content.split("\n"):
                if line.startswith("_") and line.endswith("_"):
                    parts.append(f"SOUL: {line.strip('_ ')}")
                    break

        # USER.md: extraire nom et preferences
        user_path = PERSONALITY_DIR / "USER.md"
        if user_path.exists():
            content = user_path.read_text(encoding="utf-8")
            # Extraire les lignes cles
            user_info = []
            for line in content.split("\n"):
                if line.startswith("- **Nom:**"):
                    user_info.append(line.strip("- ").strip())
                elif line.startswith("- **Machine:**"):
                    user_info.append(line.strip("- ").strip())
            if user_info:
                parts.append(f"USER: {'; '.join(user_info)}")

        # MEMORY.md: compter les entrees
        memory_path = PERSONALITY_DIR / "MEMORY.md"
        if memory_path.exists():
            content = memory_path.read_text(encoding="utf-8")
            decisions = content.count("- **20")
            lessons = content.count("- Memory") + content.count("- Hooks") + content.count("- Git")
            parts.append(f"MEMORY: {decisions} decisions, {lessons} lecons")

        return " | ".join(parts) if parts else ""

    except Exception:
        return ""


def main():
    try:
        input_data = read_stdin_json()
        session_id = input_data.get("session_id", "unknown")

        # Utiliser le cache pour skills et vault count
        ctx_cache = get_or_compute_context()
        skills = ctx_cache.get("skills_list", [])
        note_count = ctx_cache.get("vault_note_count", 0)

        # Paralleliser les 3 operations I/O independantes
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def _get_guardian():
            return get_last_guardian_date()

        def _get_personality():
            try:
                return load_personality_summary()
            except Exception:
                return ""

        def _get_memory():
            # v2.0: SQLite injection desactivee — MEMORY.md (bridge) est la source unique
            # Les extracteurs (memory_extractor_v2.py) continuent de collecter dans SQLite
            # Reactiver si R2D2-Memory est abandonne
            return ""

        def _get_compass():
            try:
                return load_compass_summary()
            except Exception:
                return ""

        guardian_date = "inconnue"
        personality_ctx = ""
        memory_context = ""
        compass_ctx = ""

        try:
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {
                    executor.submit(_get_guardian): "guardian",
                    executor.submit(_get_personality): "personality",
                    executor.submit(_get_memory): "memory",
                    executor.submit(_get_compass): "compass",
                }
                for future in as_completed(futures, timeout=5):
                    key = futures[future]
                    try:
                        result = future.result()
                        if key == "guardian":
                            guardian_date = result
                        elif key == "personality":
                            personality_ctx = result
                        elif key == "memory":
                            memory_context = result
                        elif key == "compass":
                            compass_ctx = result
                    except Exception:
                        pass
        except Exception:
            # Fallback sequentiel si ThreadPool echoue
            guardian_date = get_last_guardian_date()
            personality_ctx = load_personality_summary()
            memory_context = ""  # v2.0: SQLite injection desactivee
            try:
                compass_ctx = load_compass_summary()
            except Exception:
                compass_ctx = ""

        # Construire le contexte
        skills_str = ", ".join(skills) if skills else "aucun detecte"
        context_lines = [
            f"Systeme r2d2 - Session {session_id[:8] if len(session_id) > 8 else session_id}",
            f"Skills actifs ({len(skills)}): {skills_str}",
            f"Vault Obsidian: {note_count} notes",
            f"Derniere maintenance guardian: {guardian_date}",
        ]

        if personality_ctx:
            context_lines.append(f"Personality: {personality_ctx}")

        # Compass R2D2 — palais temporel (ajoute 2026-04-09)
        # Injecte la boussole subjective (ici/maintenant/apres + regles + signaux)
        # pour que R2D2 se situe sans relire tout l'historique
        if compass_ctx:
            context_lines.append("")  # Ligne vide pour separer
            context_lines.append("=== COMPASS R2D2 (palais temporel) ===")
            context_lines.append(compass_ctx)
            context_lines.append("=== FIN COMPASS ===")

        # Critical error check
        critical = check_critical_error()
        if critical:
            context_lines.append(
                f"WARNING: Critical error detected ({critical.get('error_type', '?')}) "
                f"in {critical.get('hook', '?')} at {critical.get('timestamp', '?')}. "
                f"Memory system may be degraded."
            )
            clear_critical_error()  # Auto-clear after reporting

        if memory_context:
            context_lines.append(f"Memory: {memory_context}")

        context = "\n".join(context_lines)

        log_audit("load_context", "session_start", {
            "session_id": session_id,
            "skills_count": len(skills),
            "vault_notes": note_count,
            "guardian_last": guardian_date,
            "compass_loaded": bool(compass_ctx),
            "compass_chars": len(compass_ctx),
        })

        output_json({"additionalContext": context})

    except Exception as e:
        log_audit("load_context", "error", {"error": str(e)})
        # Fail-open: retourne vide
        output_json({})

    sys.exit(0)


if __name__ == "__main__":
    main()
