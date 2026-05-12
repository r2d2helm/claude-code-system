"""UserPromptSubmit hook: Detection de frustration dans les messages.

Quand le prompt contient des marqueurs de frustration ("putain", "ca marche pas",
"wtf", "bordel", "merde"), injecte un contexte qui dit a Claude d'aller
droit au but (solution directe, pas de blabla).

Quand le prompt contient "continue" ou "finis", injecte "reprendre sans resumer".

Fail-open: exit 0 en cas d'erreur interne.
"""

import sys
import json
import re

FRUSTRATION_MARKERS = [
    r'\bputain\b', r'\bmerde\b', r'\bbordel\b', r'\bchiant\b',
    r'\bwtf\b', r'\bfuck\b', r'\bshit\b', r'\bdamn\b',
    r'ca marche pas', r'ca fonctionne pas', r'encore casse',
    r'toujours pas', r'je comprends pas', r'why.*not.*work',
    r'still broken', r'not working', r'doesn.t work',
]

CONTINUE_MARKERS = [
    r'^continue$', r'^finis$', r'^go$', r'^ok continue',
    r'^allez$', r'^next$', r'^suivant$',
]

COMPILED_FRUSTRATION = [re.compile(p, re.IGNORECASE) for p in FRUSTRATION_MARKERS]
COMPILED_CONTINUE = [re.compile(p, re.IGNORECASE) for p in CONTINUE_MARKERS]

def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    prompt = data.get("prompt", "")
    if not prompt:
        sys.exit(0)

    # Check frustration
    is_frustrated = any(p.search(prompt) for p in COMPILED_FRUSTRATION)
    if is_frustrated:
        print(json.dumps({
            "message": "[CONTEXTE] L'utilisateur est frustre. "
                      "Va DROIT AU BUT : diagnostic precis, solution concrete, pas de blabla. "
                      "Si tu as deja essaye quelque chose qui n'a pas marche, change d'approche."
        }))
        sys.exit(0)

    # Check continue
    is_continue = any(p.search(prompt.strip()) for p in COMPILED_CONTINUE)
    if is_continue:
        print(json.dumps({
            "message": "[CONTEXTE] Reprendre le travail en cours. "
                      "NE PAS resumer ce qui a ete fait. Continuer directement."
        }))
        sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()
