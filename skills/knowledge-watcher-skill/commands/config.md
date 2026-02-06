# Commande: /kwatch-config

Gérer la configuration du Knowledge Watcher.

## Syntaxe

```
/kwatch-config [show|edit|reset]
```

## Description

Affiche ou modifie la configuration du Knowledge Watcher.

## Sous-commandes

### /kwatch-config show (défaut)

Affiche la configuration actuelle:

```powershell
$SkillPath = "$env:USERPROFILE\.claude\skills\knowledge-watcher-skill"
$config = Get-Content "$SkillPath\config\config.json" | ConvertFrom-Json
$config | ConvertTo-Json -Depth 5
```

### /kwatch-config edit

Ouvre le fichier de configuration pour édition.

Chemin: `~\.claude\skills\knowledge-watcher-skill\config\config.json`

### /kwatch-config reset

Réinitialise la configuration par défaut.

## Fichiers de configuration

| Fichier | Description |
|---------|-------------|
| `config/config.json` | Configuration principale |
| `config/sources.json` | Définition des sources |
| `config/rules.json` | Règles de classification |

## Configuration principale (config.json)

```json
{
  "paths": {
    "obsidianVault": "C:\\Users\\r2d2\\Documents\\Knowledge",
    "claudeCli": "C:\\Users\\r2d2\\.local\\bin\\claude.exe",
    "queueFile": "...\\data\\queue.json",
    "stateFile": "...\\data\\state.json",
    "logDir": "...\\data\\logs"
  },
  "processing": {
    "claudeTimeout": 30000,
    "maxFileSize": 1048576,
    "deduplicationWindow": 86400000,
    "maxQueueSize": 100,
    "batchSize": 10
  },
  "output": {
    "defaultFolder": "_Inbox",
    "updateDailyNote": true,
    "createBacklinks": true,
    "language": "fr"
  },
  "watchers": {
    "enabled": true,
    "debounceMs": 1000,
    "ignorePatterns": ["*.tmp", "*.bak", "~$*", ".git", "node_modules"]
  }
}
```

## Paramètres clés

| Paramètre | Description |
|-----------|-------------|
| `claudeTimeout` | Timeout en ms pour Claude CLI (défaut: 30s) |
| `maxFileSize` | Taille max fichier en bytes (défaut: 1MB) |
| `deduplicationWindow` | Fenêtre de dédup en ms (défaut: 24h) |
| `maxQueueSize` | Limite de la queue (défaut: 100) |
| `updateDailyNote` | Mettre à jour la Daily Note |
| `debounceMs` | Délai anti-rebond watchers |

## Sources (sources.json)

Exemple d'ajout d'une source:

```json
{
  "id": "my-source",
  "name": "Ma Source",
  "tier": 2,
  "type": "directory",
  "enabled": true,
  "path": "C:\\Users\\r2d2\\MyFolder",
  "patterns": ["*.md", "*.txt"],
  "recursive": true,
  "processor": "GenericFileSource"
}
```

## Règles de classification (rules.json)

Exemple d'ajout d'une règle:

```json
{
  "id": "my-rule",
  "name": "Ma Règle",
  "priority": 75,
  "conditions": {
    "any": [
      { "field": "content", "contains": "my-keyword" }
    ]
  },
  "output": {
    "type": "custom",
    "folder": "MyFolder",
    "prefix": "{date}_",
    "template": null,
    "tags": ["custom"]
  }
}
```
