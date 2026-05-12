"""PostToolUse hook (Bash): Circuit breaker pour les appels API qui echouent en boucle.

Apres 3 echecs consecutifs sur la meme commande (curl, ssh, API calls),
injecte un warning pour suggerer un fallback au lieu de marteler.

Pattern inspire de Netflix Hystrix, adapte pour Claude Code.
Fail-open: exit 0 en cas d'erreur interne.
"""

import sys
import json
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / "data" / "circuit_breaker_state.json"

def load_state() -> dict:
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {"failures": {}, "tripped": {}}

def save_state(state: dict):
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except Exception:
        pass

def extract_target(command: str) -> str:
    """Extrait la cible (host/URL) d'une commande."""
    import re
    # curl URLs
    m = re.search(r'https?://([^\s/\'"]+)', command)
    if m:
        return m.group(1)
    # ssh targets
    m = re.search(r'ssh\s+\S+@(\S+)', command)
    if m:
        return m.group(1)
    return ""

def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    result = data.get("tool_result", {})
    command = data.get("tool_input", {}).get("command", "")
    is_error = result.get("is_error", False) or result.get("exit_code", 0) != 0

    target = extract_target(command)
    if not target:
        sys.exit(0)

    state = load_state()

    if is_error:
        state["failures"][target] = state["failures"].get(target, 0) + 1
        count = state["failures"][target]

        if count >= 3 and target not in state.get("tripped", {}):
            state["tripped"][target] = True
            save_state(state)
            # Warn via stderr (visible to user)
            print(f"CIRCUIT BREAKER: {target} a echoue {count} fois consecutives. "
                  f"Envisagez un fallback ou verifiez la connectivite avant de reessayer.",
                  file=sys.stderr)
            sys.exit(0)

        save_state(state)
    else:
        # Success: reset counter for this target
        if target in state["failures"]:
            del state["failures"][target]
        if target in state.get("tripped", {}):
            del state["tripped"][target]
        save_state(state)

    sys.exit(0)

if __name__ == "__main__":
    main()
