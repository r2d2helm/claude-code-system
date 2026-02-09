# Schéma settings.json PAI v2.5

## Emplacement

`$PAI_DIR/settings.json` (par défaut `~/.claude/settings.json`)

## Schéma complet

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "paiVersion": "2.5",

  "env": {
    "PAI_DIR": "$HOME/.claude",
    "PROJECTS_DIR": "",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "80000",
    "BASH_DEFAULT_TIMEOUT_MS": "600000"
  },

  "contextFiles": [
    "skills/PAI/SKILL.md",
    "skills/PAI/SYSTEM/AISTEERINGRULES.md",
    "skills/PAI/USER/AISTEERINGRULES.md",
    "skills/PAI/USER/DAIDENTITY.md"
  ],

  "daidentity": {
    "name": "R2D2",
    "fullName": "R2D2 - Personal AI",
    "displayName": "R2D2",
    "color": "#3B82F6",
    "voiceId": "21m00Tcm4TlvDq8ikWAM",
    "voice": {
      "stability": 0.35,
      "similarity_boost": 0.80,
      "style": 0.90,
      "speed": 1.1,
      "use_speaker_boost": true,
      "volume": 0.8
    },
    "startupCatchphrase": "R2D2 here, ready to go."
  },

  "principal": {
    "name": "User",
    "timezone": "America/Los_Angeles"
  },

  "pai": {
    "repoUrl": "github.com/danielmiessler/PAI",
    "version": "2.5"
  },

  "techStack": {
    "terminal": "Kitty",
    "packageManager": "bun",
    "pythonPackageManager": "uv",
    "language": "TypeScript"
  },

  "permissions": {
    "allow": [
      "Bash", "Read", "Write", "Edit", "MultiEdit",
      "Glob", "Grep", "LS", "WebFetch", "WebSearch",
      "NotebookRead", "NotebookEdit", "TodoWrite",
      "ExitPlanMode", "Task", "Skill", "mcp__*"
    ],
    "deny": [],
    "ask": [
      "Bash(rm -rf /)", "Bash(rm -rf /:*)",
      "Bash(sudo rm -rf /)", "Bash(sudo rm -rf /:*)",
      "Bash(rm -rf ~)", "Bash(rm -rf ~:*)",
      "Bash(rm -rf ~/.claude)", "Bash(rm -rf ~/.claude:*)",
      "Bash(dd if=/dev/zero:*)", "Bash(mkfs:*)",
      "Bash(gh repo delete:*)",
      "Bash(git push --force:*)", "Bash(git push -f:*)",
      "Read(~/.ssh/id_*)", "Read(~/.ssh/*.pem)",
      "Read(~/.aws/credentials)", "Read(~/.gnupg/private*)",
      "Write(~/.claude/settings.json)",
      "Edit(~/.claude/settings.json)",
      "Write(~/.ssh/*)", "Edit(~/.ssh/*)"
    ],
    "defaultMode": "default"
  },

  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": [],

  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "${PAI_DIR}/hooks/SecurityValidator.hook.ts" }]
      },
      {
        "matcher": "Edit",
        "hooks": [{ "type": "command", "command": "${PAI_DIR}/hooks/SecurityValidator.hook.ts" }]
      },
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": "${PAI_DIR}/hooks/SecurityValidator.hook.ts" }]
      },
      {
        "matcher": "Read",
        "hooks": [{ "type": "command", "command": "${PAI_DIR}/hooks/SecurityValidator.hook.ts" }]
      },
      {
        "matcher": "AskUserQuestion",
        "hooks": [{ "type": "command", "command": "${PAI_DIR}/hooks/SetQuestionTab.hook.ts" }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "AskUserQuestion",
        "hooks": [{ "type": "command", "command": "${PAI_DIR}/hooks/QuestionAnswered.hook.ts" }]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          { "type": "command", "command": "${PAI_DIR}/hooks/WorkCompletionLearning.hook.ts" },
          { "type": "command", "command": "${PAI_DIR}/hooks/SessionSummary.hook.ts" }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          { "type": "command", "command": "${PAI_DIR}/hooks/FormatReminder.hook.ts" },
          { "type": "command", "command": "${PAI_DIR}/hooks/AutoWorkCreation.hook.ts" },
          { "type": "command", "command": "${PAI_DIR}/hooks/ExplicitRatingCapture.hook.ts" },
          { "type": "command", "command": "${PAI_DIR}/hooks/ImplicitSentimentCapture.hook.ts" },
          { "type": "command", "command": "${PAI_DIR}/hooks/UpdateTabTitle.hook.ts" }
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
    ],
    "Stop": [
      {
        "hooks": [{ "type": "command", "command": "${PAI_DIR}/hooks/StopOrchestrator.hook.ts" }]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [{ "type": "command", "command": "${PAI_DIR}/hooks/AgentOutputCapture.hook.ts" }]
      }
    ]
  },

  "statusLine": {
    "type": "command",
    "command": "${PAI_DIR}/statusline-command.sh"
  },

  "alwaysThinkingEnabled": true,
  "max_tokens": 4096
}
```

## Sections clés

### env
Variables d'environnement. `PAI_DIR` est critique — tous les chemins en dépendent.

### contextFiles
Fichiers chargés automatiquement au démarrage de session. L'ordre compte : SKILL.md d'abord, puis les steering rules.

### daidentity
Identité du DA (Digital Assistant). `name` est utilisé partout. `voiceId` = ID voix ElevenLabs.

### principal
Identité de l'utilisateur. `name` et `timezone` personnalisent les interactions.

### hooks
Configuration complète des 15 hooks. Chaque événement a un tableau de matchers avec hooks associés.

### permissions
Contrôle d'accès aux outils. `ask` force confirmation utilisateur.

## Fusion settings.json

Lors de l'installation PAI sur un système existant, il faut **fusionner** et non écraser :

### Sections à préserver de l'existant
- `mcpServers` : Configuration MCP existante
- Toute section custom ajoutée par l'utilisateur

### Sections PAI à ajouter/mettre à jour
- `paiVersion`, `env`, `contextFiles`, `daidentity`, `principal`
- `pai`, `techStack`, `hooks`, `statusLine`
- Fusionner `permissions` (ajouter les patterns ask PAI)

### Algorithme de fusion
```
1. Lire settings.json existant
2. Lire settings.json PAI template
3. Pour chaque clé PAI :
   - Si clé absente dans existant → ajouter
   - Si clé = "hooks" → fusionner (ajouter hooks PAI sans écraser existants)
   - Si clé = "permissions" → fusionner les tableaux
   - Si clé = "mcpServers" → PRÉSERVER l'existant intégralement
   - Sinon → valeur PAI (avec backup de l'ancienne)
4. Écrire résultat
```

## Validation

```bash
# Vérifier syntaxe JSON
cat $PAI_DIR/settings.json | jq . > /dev/null && echo "JSON valide" || echo "JSON INVALIDE"

# Vérifier PAI_DIR défini
cat $PAI_DIR/settings.json | jq '.env.PAI_DIR'

# Vérifier hooks enregistrés
cat $PAI_DIR/settings.json | jq '.hooks | keys'

# Vérifier contextFiles
cat $PAI_DIR/settings.json | jq '.contextFiles'

# Vérifier identité DA
cat $PAI_DIR/settings.json | jq '.daidentity.name'
```
