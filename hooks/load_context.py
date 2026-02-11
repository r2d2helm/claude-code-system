"""SessionStart hook: charge le contexte systeme r2d2 au demarrage.

Injecte un additionalContext avec:
- Liste des skills actifs
- Nombre de notes dans le vault
- Date de derniere maintenance guardian
"""

import sys
import re
import glob
from pathlib import Path

# Ajouter le dossier hooks au path pour imports relatifs
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import SKILLS_DIR, VAULT_PATH
from lib.utils import read_stdin_json, log_audit, output_json, now_paris


def get_active_skills() -> list[str]:
    """Extrait les skills actifs depuis SKILL.md."""
    try:
        skill_file = SKILLS_DIR / "SKILL.md"
        if not skill_file.exists():
            return []
        content = skill_file.read_text(encoding="utf-8")
        # Chercher les lignes du tableau avec "Actif"
        skills = []
        for match in re.finditer(r"\|\s*\S+\s+(\w[\w-]+)\s*\|.*?\|\s*.*?Actif", content):
            skills.append(match.group(1))
        if not skills:
            # Fallback: chercher les dossiers *-skill
            for d in SKILLS_DIR.iterdir():
                if d.is_dir() and d.name.endswith("-skill"):
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


def main():
    try:
        input_data = read_stdin_json()
        session_id = input_data.get("session_id", "unknown")

        skills = get_active_skills()
        note_count = count_vault_notes()
        guardian_date = get_last_guardian_date()

        # Construire le contexte
        skills_str = ", ".join(skills) if skills else "aucun detecte"
        context_lines = [
            f"Systeme r2d2 - Session {session_id[:8] if len(session_id) > 8 else session_id}",
            f"Skills actifs ({len(skills)}): {skills_str}",
            f"Vault Obsidian: {note_count} notes",
            f"Derniere maintenance guardian: {guardian_date}",
        ]
        context = "\n".join(context_lines)

        log_audit("load_context", "session_start", {
            "session_id": session_id,
            "skills_count": len(skills),
            "vault_notes": note_count,
            "guardian_last": guardian_date,
        })

        output_json({"additionalContext": context})

    except Exception as e:
        log_audit("load_context", "error", {"error": str(e)})
        # Fail-open: retourne vide
        output_json({})

    sys.exit(0)


if __name__ == "__main__":
    main()
