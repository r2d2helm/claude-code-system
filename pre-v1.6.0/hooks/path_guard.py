"""PreToolUse hook (Read/Write/Edit): protege les chemins sensibles.

Categories de regles:
- read_protected: exit 2 + block (acces refuse aux secrets)
- write_protected: exit 0 + decision block (confirmation pour chemins proteges)
- system_paths: exit 0 + decision block (confirmation pour fichiers systeme)
- aucune regle: exit 0 silencieux (allow)

Enregistre dans settings.json avec 3 matchers: Read, Write, Edit.
Le hook recoit tool_name dans stdin pour differencier.
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
_compiled_rules = None


def load_path_rules() -> dict:
    """Charge et compile les regles de protection des chemins depuis YAML."""
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
                # Fallback si PyYAML absent: pas de protection de chemins
                return {"read_protected": [], "write_protected": [], "system_paths": []}
    except Exception:
        return {"read_protected": [], "write_protected": [], "system_paths": []}

    # Compiler les regex pour les categories de chemins
    compiled = {}
    for category in ("read_protected", "write_protected", "system_paths", "auto_allow_patterns"):
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


def validate_path(tool_name: str, file_path: str) -> tuple:
    """Valide un chemin. Retourne (category, reason, pattern) ou ('allow', '', '')."""
    rules = load_path_rules()

    # Normaliser le chemin pour matcher les patterns
    try:
        resolved = str(Path(file_path).resolve())
    except Exception:
        resolved = file_path

    # Read: verifier read_protected (block hard)
    if tool_name == "Read":
        for rule in rules.get("read_protected", []):
            if rule["regex"].search(resolved):
                return "blocked", rule["reason"], rule["pattern"]

    # Write/Edit: verifier write_protected, puis auto_allow, puis system_paths
    if tool_name in ("Write", "Edit"):
        for rule in rules.get("write_protected", []):
            if rule["regex"].search(resolved):
                return "confirm", rule["reason"], rule["pattern"]
        for rule in rules.get("auto_allow_patterns", []):
            if rule["regex"].search(resolved):
                return "auto_allow", rule["reason"], rule["pattern"]
        for rule in rules.get("system_paths", []):
            if rule["regex"].search(resolved):
                return "confirm", rule["reason"], rule["pattern"]

    return "allow", "", ""


def main():
    try:
        input_data = read_stdin_json()
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        file_path = (
            tool_input.get("file_path", "")
            or tool_input.get("notebook_path", "")
        )

        if not file_path:
            sys.exit(0)

        category, reason, pattern = validate_path(tool_name, file_path)

        if category == "blocked":
            log_audit("path_guard", "blocked", {
                "tool": tool_name,
                "path": file_path[:200],
                "reason": reason,
                "pattern": pattern,
            })
            # Exit 2 = block l'operation
            print(json.dumps({
                "decision": "block",
                "reason": f"SECURITE: Acces refuse - {reason}",
            }))
            sys.exit(2)

        elif category == "confirm":
            log_audit("path_guard", "confirm", {
                "tool": tool_name,
                "path": file_path[:200],
                "reason": reason,
            })
            # Exit 0 + decision block = Claude Code demandera confirmation
            output_json({
                "decision": "block",
                "reason": f"ATTENTION: {reason}. Confirmation requise.",
            })
            sys.exit(0)

        elif category == "auto_allow":
            log_audit("path_guard", "auto_allow", {
                "tool": tool_name,
                "path": file_path[:200],
                "reason": reason,
            })
            # Auto-allow - pas de confirmation requise
            sys.exit(0)

        else:
            # Allow - pas d'output
            sys.exit(0)

    except SystemExit:
        raise
    except Exception as e:
        # Fail-open: log l'erreur mais laisse passer
        log_audit("path_guard", "error", {"error": str(e)})
        sys.exit(0)


if __name__ == "__main__":
    main()
