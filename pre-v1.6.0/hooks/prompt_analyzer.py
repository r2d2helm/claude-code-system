"""UserPromptSubmit hook: analyse les requetes utilisateur.

Detecte les commandes skill, mots-cles techniques, et classifie
le type de requete. Log dans prompt-log.jsonl.

IMPORTANT: Ne log PAS le message complet (vie privee).
Seulement preview (100 chars), type, et metadata.
"""

import sys
import re
from pathlib import Path

# Ajouter le dossier hooks au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import LOGS_DIR
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris

# Regex pour detecter les commandes skill (/prefix-action)
SKILL_COMMAND_RE = re.compile(r"/([\w][\w-]*)")

# Mots-cles techniques pour detection de domaine
TECHNICAL_KEYWORDS = {
    "docker", "proxmox", "windows", "linux", "vault",
    "obsidian", "backup", "deploy", "debug", "fix",
    "qet", "qelectrotech", "sop", "prp", "skill",
    "maintenance", "firewall", "network", "container",
    "vm", "lxc", "cluster", "ceph", "zfs",
    "git", "hook", "mcp", "agent", "router",
}

# Prefixes de questions en francais et anglais
QUESTION_STARTERS = (
    "pourquoi", "comment", "quoi", "quel", "quelle",
    "est-ce", "peut-on", "how", "what", "why", "where",
    "when", "which", "can", "does", "is",
)


def classify_message(message: str) -> str:
    """Classifie le message: command|question|instruction|debug."""
    stripped = message.strip()

    if stripped.startswith("/"):
        return "command"

    lower = stripped.lower()
    if "?" in stripped or lower.startswith(QUESTION_STARTERS):
        return "question"

    if any(kw in lower for kw in ("fix", "debug", "error", "bug", "crash", "traceback")):
        return "debug"

    return "instruction"


def main():
    try:
        input_data = read_stdin_json()
        session_id = input_data.get("session_id", "unknown")
        message = input_data.get("message", "")

        if not message:
            sys.exit(0)

        msg_type = classify_message(message)
        skills = SKILL_COMMAND_RE.findall(message)
        keywords = [kw for kw in TECHNICAL_KEYWORDS if kw in message.lower()]

        entry = {
            "timestamp": now_paris(),
            "session_id": session_id,
            "message_type": msg_type,
            "skills_detected": skills[:5],
            "keywords": keywords[:10],
            "message_length": len(message),
            "message_preview": message[:100],
        }

        append_jsonl(LOGS_DIR / "prompt-log.jsonl", entry)

        log_audit("prompt_analyzer", "user_input", {
            "type": msg_type,
            "skills": skills[:5],
            "keywords_count": len(keywords),
        })

        # Memory v2: injection contextuelle de memoires par prompt
        output = {}
        try:
            from lib.memory_retriever import retrieve_for_prompt
            memory_context = retrieve_for_prompt(message, session_id)
            if memory_context:
                output["additionalContext"] = memory_context
        except Exception:
            pass  # Fail-open

        if output:
            from lib.utils import output_json
            output_json(output)

    except Exception as e:
        log_audit("prompt_analyzer", "error", {"error": str(e)})

    # Toujours exit 0
    sys.exit(0)


if __name__ == "__main__":
    main()
