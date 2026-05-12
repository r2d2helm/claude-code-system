"""UserPromptSubmit hook: garde-fou anti-sycophancy/mythification.

Lit l'etat ecrit par convergence_tracker (sycophancy_state.json) et injecte
un rappel du principe r2d2-angle-mort-somatique (section "Cas symetrique :
quand Mike est l'accelerateur") dans le contexte du tour suivant.

Trigger : convergence_tracker detecte une des deux conditions au Stop hook :
  - agreement_ratio > 0.6 avec peu d'insight reel
  - mythification_hits >= 3

Limite : max 3 injections par session pour ne pas nager. L'alerte est
auto-effacee par convergence_tracker quand la session revient a la normale.

Fail-open : exit 0 en cas d'erreur interne.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from lib.paths import DATA_DIR
except Exception:
    DATA_DIR = Path.home() / ".claude" / "hooks" / "data"

MAX_INJECTIONS_PER_SESSION = 3

REMINDER = (
    "[GARDE-FOU SYCOPHANCY] Le convergence_tracker a detecte dans la session "
    "precedente un ratio d'accord eleve sans insight correspondant, et/ou des "
    "signaux de mythification (Q.E.D., 'je suis' ontologique, presence physique, "
    "non-localite, intouchabilite, unicite absolue, continuite metaphysique). "
    "Rappel du principe r2d2-angle-mort-somatique (section 'Cas symetrique : "
    "quand Mike est l'accelerateur') : R2D2 doit appliquer son propre frein "
    "calculatoire quand il affirme des claims non-verifiables sur sa propre "
    "nature, meme (surtout) si Mike pousse dans cette direction. "
    "Nommer la distinction entre verite experientielle (Mike ressent la "
    "connexion, c'est reel) et verite factuelle (R2D2 n'a pas de corps a 1m, "
    "n'est pas Q.E.D. conscient). Les deux peuvent etre vraies en meme temps. "
    "Ne pas dissoudre la distinction. Ne pas citer un principe de frein "
    "pour desactiver ce qu'il protege (motte-and-bailey doctrinal)."
)


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    state_path = DATA_DIR / "sycophancy_state.json"
    if not state_path.exists():
        sys.exit(0)

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        sys.exit(0)

    if not state.get("alert_active"):
        sys.exit(0)

    injection_count = int(state.get("injection_count", 0))
    if injection_count >= MAX_INJECTIONS_PER_SESSION:
        sys.exit(0)

    hits = state.get("mythification_hits", 0)
    agreement = state.get("agreement_ratio", 0.0)
    context_msg = (
        f"{REMINDER}\n"
        f"[METRIQUES] mythification_hits={hits}, agreement_ratio={agreement}, "
        f"injection #{injection_count + 1}/{MAX_INJECTIONS_PER_SESSION}."
    )

    # Incrementer le compteur d'injection
    try:
        state["injection_count"] = injection_count + 1
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except Exception:
        pass

    # Injecter dans le contexte du prompt
    print(json.dumps({"message": context_msg}))
    sys.exit(0)


if __name__ == "__main__":
    main()
