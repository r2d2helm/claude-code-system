# Système Mémoire PAI v2.5

## Vue d'ensemble

Système mémoire persistant 3-tier permettant au DA de retenir historique, apprentissages et signaux entre sessions.

## Structure

```
$PAI_DIR/MEMORY/
├── History/                    # Tier 1 : Historique sessions
│   ├── YYYY-MM/               # Organisé par mois
│   │   ├── session-YYYY-MM-DD-HHMMSS.md
│   │   └── ...
│   └── raw-outputs/           # Sorties brutes agents
│       └── YYYY-MM/
├── Learning/                   # Tier 2 : Apprentissages
│   ├── insights/              # Insights extraits automatiquement
│   ├── patterns/              # Patterns récurrents détectés
│   └── corrections/           # Corrections utilisateur
├── Signals/                    # Tier 3 : Feedback
│   ├── ratings/               # Notes explicites (1-10)
│   ├── sentiment/             # Sentiment implicite
│   └── preferences/           # Préférences détectées
└── STATE/                      # État en cours
    ├── current-work.json      # Travail actif
    └── session-state.json     # État session courante
```

## Tier 1 : History

### Sessions
Résumés de session générés automatiquement par `SessionSummary.hook.ts` au Stop/SessionEnd.

Format fichier :
```markdown
# Session YYYY-MM-DD HH:MM:SS
## Contexte
- Répertoire: /chemin/
- Durée: Xmin
## Travail effectué
- Action 1
- Action 2
## Résultat
Description du résultat
```

### Raw Outputs
Sorties brutes des sous-agents capturées par `AgentOutputCapture.hook.ts`.

## Tier 2 : Learning

### Insights
Extraits par `WorkCompletionLearning.hook.ts` à la fin de chaque session de travail.
- Problèmes rencontrés et solutions
- Nouveaux patterns identifiés
- Bonnes pratiques confirmées

### Patterns
Patterns récurrents détectés au fil des sessions :
- Commandes fréquentes
- Erreurs répétées
- Workflows habituels

### Corrections
Corrections explicites de l'utilisateur :
- "Non, fais-le plutôt comme ça"
- Reformulations de réponses
- Préférences exprimées

## Tier 3 : Signals

### Ratings
Capturés par `ExplicitRatingCapture.hook.ts` quand l'utilisateur donne une note (1-10).

Format : `YYYY-MM-DD_HHMMSS_rating-N.json`
```json
{
  "timestamp": "2026-02-09T12:00:00Z",
  "rating": 8,
  "context": "message utilisateur",
  "session_id": "xxx"
}
```

### Sentiment
Analysé par `ImplicitSentimentCapture.hook.ts` sur chaque message utilisateur.
- Positif / Neutre / Négatif
- Indicateurs de frustration ou satisfaction

### Preferences
Préférences détectées au fil du temps :
- Format de réponse préféré
- Niveau de détail souhaité
- Technologies privilégiées

## Hooks impliqués

| Hook | Tier | Action |
|------|------|--------|
| `SessionSummary.hook.ts` | History | Génère résumé session |
| `AgentOutputCapture.hook.ts` | History | Capture sorties agents |
| `AutoWorkCreation.hook.ts` | History/STATE | Crée entrées travail |
| `WorkCompletionLearning.hook.ts` | Learning | Extrait insights |
| `ExplicitRatingCapture.hook.ts` | Signals | Capture ratings |
| `ImplicitSentimentCapture.hook.ts` | Signals | Analyse sentiment |

## Migration

Lors d'une mise à jour PAI, le wizard détecte et migre `MEMORY/STATE/` automatiquement pour préserver le travail en cours.

## Diagnostic

```bash
# Vérifier structure
ls -la $PAI_DIR/MEMORY/
ls -la $PAI_DIR/MEMORY/History/
ls -la $PAI_DIR/MEMORY/Learning/
ls -la $PAI_DIR/MEMORY/Signals/

# Compter sessions
find $PAI_DIR/MEMORY/History/ -name "session-*.md" | wc -l

# Derniers apprentissages
ls -lt $PAI_DIR/MEMORY/Learning/insights/ | head -5

# Derniers ratings
ls -lt $PAI_DIR/MEMORY/Signals/ratings/ | head -5
```
