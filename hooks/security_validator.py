"""PreToolUse hook (Bash): valide les commandes contre les regles de securite.

Categories:
- blocked: exit 2 + message erreur (commande refusee)
- confirm: exit 0 + decision block (force confirmation utilisateur)
- alert: exit 0 + warning stderr (laisse passer)
- aucune regle: exit 0 silencieux (allow)
"""

import sys
import re
import json
from pathlib import Path

# Ajouter le dossier hooks au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import CONFIG_DIR
from lib.utils import read_stdin_json, log_audit, output_json

# Cache des regles compilees
_compiled_rules: dict | None = None


def load_rules() -> dict:
    """Charge et compile les regles de securite depuis YAML ou JSON."""
    global _compiled_rules
    if _compiled_rules is not None:
        return _compiled_rules

    rules_file = CONFIG_DIR / "security_rules.yaml"
    raw_rules = {}

    try:
        if rules_file.exists():
            try:
                import yaml
                raw_rules = yaml.safe_load(rules_file.read_text(encoding="utf-8")) or {}
            except ImportError:
                # Fallback JSON si PyYAML absent
                json_file = CONFIG_DIR / "security_rules.json"
                if json_file.exists():
                    raw_rules = json.loads(json_file.read_text(encoding="utf-8"))
    except Exception:
        return {"blocked": [], "confirm": [], "alert": []}

    # Compiler les regex
    compiled = {}
    for category in ("blocked", "confirm", "alert"):
        compiled[category] = []
        for rule in raw_rules.get(category, []):
            try:
                compiled[category].append({
                    "regex": re.compile(rule["pattern"], re.IGNORECASE),
                    "reason": rule["reason"],
                    "pattern": rule["pattern"],
                })
            except (re.error, KeyError):
                continue

    _compiled_rules = compiled
    return compiled


def validate_command(command: str) -> tuple[str, str, str]:
    """Valide une commande. Retourne (category, reason, pattern) ou ('allow', '', '')."""
    rules = load_rules()

    for category in ("blocked", "confirm", "alert"):
        for rule in rules[category]:
            if rule["regex"].search(command):
                return category, rule["reason"], rule["pattern"]

    return "allow", "", ""


def main():
    try:
        input_data = read_stdin_json()
        tool_input = input_data.get("tool_input", {})
        command = tool_input.get("command", "")

        if not command:
            sys.exit(0)

        category, reason, pattern = validate_command(command)

        if category == "blocked":
            log_audit("security_validator", "blocked", {
                "command": command[:200],
                "reason": reason,
                "pattern": pattern,
            })
            # Exit 2 = block la commande
            print(json.dumps({
                "decision": "block",
                "reason": f"SECURITE: Commande bloquee - {reason}",
            }))
            sys.exit(2)

        elif category == "confirm":
            log_audit("security_validator", "confirm", {
                "command": command[:200],
                "reason": reason,
            })
            # Exit 0 + decision block = Claude Code demandera confirmation
            output_json({
                "decision": "block",
                "reason": f"ATTENTION: {reason}. Confirmation requise.",
            })
            sys.exit(0)

        elif category == "alert":
            log_audit("security_validator", "alert", {
                "command": command[:200],
                "reason": reason,
            })
            # Warning sur stderr, laisse passer
            print(f"[hook:security] Alert: {reason}", file=sys.stderr)
            sys.exit(0)

        else:
            # Allow - pas d'output
            sys.exit(0)

    except SystemExit:
        raise
    except Exception as e:
        # Fail-open: log l'erreur mais laisse passer
        log_audit("security_validator", "error", {"error": str(e)})
        sys.exit(0)


if __name__ == "__main__":
    main()
