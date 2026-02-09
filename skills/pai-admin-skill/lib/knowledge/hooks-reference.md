# Référence Hooks PAI v2.5

## Vue d'ensemble

15 hooks, 12 bibliothèques partagées, 4 handlers spécialisés. Tous en TypeScript (Bun runtime).

## Types d'événements

| Événement | Quand | Exit codes |
|-----------|-------|------------|
| `PreToolUse` | Avant exécution outil | 0=allow, 2=block |
| `PostToolUse` | Après exécution outil | 0 toujours |
| `Stop` | Fin réponse agent principal | 0 toujours |
| `SubagentStop` | Fin réponse sous-agent | 0 toujours |
| `SessionStart` | Début session | 0 toujours |
| `SessionEnd` | Fin session | 0 toujours |
| `UserPromptSubmit` | Message utilisateur envoyé | 0 toujours |
| `PreCompact` | Avant compaction contexte | 0 toujours |

## Catalogue des 15 hooks

### SessionStart (3 hooks)

#### LoadContext.hook.ts
- **Rôle** : Injecter le CORE skill dans le contexte
- **Matcher** : `*` (tous)
- **Payload stdin** : `{ session_id, cwd }`
- **Sortie stdout** : Contenu SKILL.md à injecter
- **Exit** : 0

#### StartupGreeting.hook.ts
- **Rôle** : Afficher bannière PAI + notification vocale
- **Matcher** : `*`
- **Payload stdin** : `{ session_id }`
- **Action** : Appel Voice Server si actif
- **Exit** : 0

#### CheckVersion.hook.ts
- **Rôle** : Vérifier compatibilité version Claude Code
- **Matcher** : `*`
- **Payload stdin** : `{ session_id }`
- **Action** : Warning si version incompatible
- **Exit** : 0

### PreToolUse (1 hook)

#### SecurityValidator.hook.ts
- **Rôle** : Bloquer commandes dangereuses
- **Matchers** : `Bash`, `Edit`, `Write`, `Read`
- **Payload stdin** : `{ tool_name, tool_input: { command } }`
- **Patterns détectés** :
  - Tier CATASTROPHIC : `rm -rf /`, `dd if=/dev/zero of=/dev/sd*`, `mkfs`, `:(){ :|:& };:`
  - Tier DESTRUCTIVE : `rm -rf ~`, suppression répertoires système
  - Tier SUSPICIOUS : `chmod 777`, `curl | bash` (sans contexte PAI)
- **Exit** : 0 (allow) ou 2 (block + message warning stdout)
- **Fichier protections** : `.pai-protected.json` (chemins protégés additionnels)

### UserPromptSubmit (3 hooks)

#### UpdateTabTitle.hook.ts
- **Rôle** : Mettre à jour titre onglet terminal avec contexte tâche
- **Payload stdin** : `{ message }`
- **Action** : Extrait résumé 5 mots, met à jour titre via séquence escape
- **Exit** : 0

#### SetQuestionTab.hook.ts
- **Rôle** : Marquer onglet quand question AskUserQuestion
- **Matcher** : `AskUserQuestion` (sur PreToolUse)
- **Action** : Préfixe onglet avec indicateur question
- **Exit** : 0

#### ExplicitRatingCapture.hook.ts
- **Rôle** : Capturer notes explicites 1-10 dans le message
- **Payload stdin** : `{ message }`
- **Détection** : Pattern regex `\b([1-9]|10)\/10\b` ou "rate X"
- **Action** : Écriture dans MEMORY/Signals/ratings/
- **Exit** : 0

### Stop (7 hooks)

#### FormatEnforcer.hook.ts (anciennement FormatReminder)
- **Rôle** : Rappeler le format de réponse attendu
- **Action** : Injecte rappel format si réponse non conforme
- **Exit** : 0

#### StopOrchestrator.hook.ts
- **Rôle** : Coordonner tous les handlers post-réponse
- **Action** : Exécute séquentiellement les handlers dans `handlers/`
- **Exit** : 0

#### SessionSummary.hook.ts
- **Rôle** : Générer résumé de session
- **Action** : Écriture dans MEMORY/History/
- **Exit** : 0

#### QuestionAnswered.hook.ts
- **Rôle** : Tracker complétion questions
- **Matcher** : `AskUserQuestion` (sur PostToolUse)
- **Action** : Restaure titre onglet normal
- **Exit** : 0

#### AutoWorkCreation.hook.ts
- **Rôle** : Créer entrées de travail automatiquement
- **Action** : Écriture dans WORK/
- **Exit** : 0

#### WorkCompletionLearning.hook.ts
- **Rôle** : Extraire insights/apprentissages du travail complété
- **Action** : Écriture dans MEMORY/Learning/
- **Exit** : 0

#### ImplicitSentimentCapture.hook.ts
- **Rôle** : Analyser sentiment implicite
- **Payload** : Analyse du message utilisateur
- **Action** : Écriture dans MEMORY/Signals/sentiment/
- **Exit** : 0

### SubagentStop (1 hook)

#### AgentOutputCapture.hook.ts
- **Rôle** : Capturer sorties des sous-agents
- **Action** : Routage vers catégories dans history/raw-outputs/
- **Exit** : 0

## Bibliothèques partagées (lib/ - 12 fichiers)

| Fichier | Rôle |
|---------|------|
| `observability.ts` | Envoi événements au dashboard |
| `notifications.ts` | Notifications desktop (notify-send/osascript) |
| `identity.ts` | Lecture identité DA depuis settings.json |
| `voice.ts` | Appel Voice Server |
| `memory.ts` | Lecture/écriture MEMORY/ |
| `tab-title.ts` | Manipulation titre onglet terminal |
| `metadata-extraction.ts` | Extraction métadonnées agents |
| `file-utils.ts` | Utilitaires fichiers |
| `logging.ts` | Logging structuré |
| `config.ts` | Lecture configuration |
| `patterns.ts` | Patterns regex sécurité |
| `fail-safe.ts` | Wrappers try-catch fail-safe |

## Handlers spécialisés (handlers/ - 4 fichiers)

| Handler | Rôle |
|---------|------|
| `work-handler.ts` | Traitement entrées WORK |
| `learning-handler.ts` | Extraction apprentissages |
| `sentiment-handler.ts` | Analyse sentiment |
| `summary-handler.ts` | Génération résumés |

## Principes de conception

1. **Never Block** : Exit 0 toujours (sauf SecurityValidator qui peut exit 2)
2. **Fail Silently** : Erreurs loguées, jamais propagées
3. **Fast Execution** : Millisecondes, pas secondes
4. **Stdin/Stdout** : JSON in, texte/JSON out
5. **Composable** : Plusieurs hooks sur le même événement

## Configuration dans settings.json

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${PAI_DIR}/hooks/SecurityValidator.hook.ts"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "${PAI_DIR}/hooks/StartupGreeting.hook.ts" },
          { "type": "command", "command": "${PAI_DIR}/hooks/LoadContext.hook.ts" },
          { "type": "command", "command": "${PAI_DIR}/hooks/CheckVersion.hook.ts" }
        ]
      }
    ]
  }
}
```

## Diagnostic hooks

```bash
# Vérifier que les fichiers existent
ls -la $PAI_DIR/hooks/*.hook.ts

# Tester un hook manuellement
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | bun run $PAI_DIR/hooks/SecurityValidator.hook.ts

# Vérifier la config dans settings.json
cat $PAI_DIR/settings.json | jq '.hooks'
```
