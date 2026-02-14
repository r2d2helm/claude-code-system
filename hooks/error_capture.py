"""PostToolUse hook (Bash): capture erreurs et detecte les corrections.

Deux fonctions:
1. Log les commandes echouees (exit code != 0) dans errors.jsonl
2. Detecte les paires erreur→correction: quand une commande reussit
   sur le meme outil/base qu'une erreur recente, log la correction
   dans corrections.jsonl pour apprentissage.
"""

import json
import sys
from pathlib import Path

# Ajouter le dossier hooks au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import MEMORY_DIR
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris


def _get_base_command(command: str) -> str:
    """Extrait la commande de base (premier mot) pour comparaison."""
    parts = command.strip().split()
    return parts[0] if parts else ""


def _find_recent_error(base_cmd: str, session_id: str) -> dict | None:
    """Cherche une erreur recente avec la meme commande de base dans la session."""
    errors_file = MEMORY_DIR / "errors.jsonl"
    if not errors_file.exists():
        return None

    # Lire les 20 dernieres entrees (performant)
    recent = []
    try:
        with open(errors_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    recent.append(line)
                    if len(recent) > 20:
                        recent.pop(0)
    except Exception:
        return None

    # Chercher une erreur recente avec la meme commande de base
    for raw in reversed(recent):
        try:
            entry = json.loads(raw)
            if entry.get("session_id") != session_id:
                continue
            err_cmd = entry.get("command", "")
            if _get_base_command(err_cmd) == base_cmd:
                return entry
        except json.JSONDecodeError:
            continue

    return None


def main():
    try:
        input_data = read_stdin_json()
        session_id = input_data.get("session_id", "unknown")
        tool_input = input_data.get("tool_input", {})
        tool_result = input_data.get("tool_result", {})

        command = tool_input.get("command", "")
        if not command:
            sys.exit(0)

        # Check for error indicators in the result
        stdout = str(tool_result.get("stdout", ""))
        stderr = str(tool_result.get("stderr", ""))
        exit_code = tool_result.get("exit_code")

        # Detect errors: non-zero exit code or error keywords in output
        is_error = False
        error_type = ""

        if exit_code is not None and exit_code != 0:
            is_error = True
            error_type = f"exit_code_{exit_code}"
        elif any(kw in stderr.lower() for kw in ("error", "fatal", "traceback", "permission denied")):
            is_error = True
            error_type = "stderr_error"

        MEMORY_DIR.mkdir(parents=True, exist_ok=True)

        if is_error:
            entry = {
                "timestamp": now_paris(),
                "session_id": session_id,
                "command": command[:200],
                "error_type": error_type,
                "exit_code": exit_code,
                "stderr_preview": stderr[:300] if stderr else "",
            }
            append_jsonl(MEMORY_DIR / "errors.jsonl", entry)

            log_audit("error_capture", "bash_error", {
                "command": command[:100],
                "error_type": error_type,
            })

        else:
            # Commande reussie: chercher si elle corrige une erreur recente
            base_cmd = _get_base_command(command)
            if base_cmd:
                recent_error = _find_recent_error(base_cmd, session_id)
                if recent_error:
                    correction = {
                        "timestamp": now_paris(),
                        "session_id": session_id,
                        "error_command": recent_error.get("command", "")[:200],
                        "error_stderr": recent_error.get("stderr_preview", "")[:200],
                        "fix_command": command[:200],
                        "fix_stdout_preview": stdout[:200] if stdout else "",
                    }
                    append_jsonl(MEMORY_DIR / "corrections.jsonl", correction)

                    log_audit("error_capture", "correction_detected", {
                        "error_cmd": recent_error.get("command", "")[:80],
                        "fix_cmd": command[:80],
                    })

    except Exception as e:
        log_audit("error_capture", "error", {"error": str(e)})

    # Fail-open
    sys.exit(0)


if __name__ == "__main__":
    main()
