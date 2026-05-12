# Knowledge Watcher Skill

Agent de surveillance automatique pour capturer et transformer les données en notes Obsidian.

## Installation

Le skill est automatiquement chargé par Claude Code. Utilisez le wizard pour la configuration initiale :

```
/kwatch-wizard setup
```

## Utilisation Rapide

```bash
# Démarrer la surveillance
/kwatch-start

# Voir le statut et la queue
/kwatch-status

# Traiter manuellement la queue
/kwatch-process

# Arrêter la surveillance
/kwatch-stop
```

## Structure

```
knowledge-watcher-skill/
├── SKILL.md              # Documentation principale
├── commands/             # Commandes slash
│   ├── start.md
│   ├── stop.md
│   ├── status.md
│   ├── process.md
│   ├── config.md
│   └── logs.md
├── wizards/
│   ├── wizard-setup.md
│   └── wizard-sources.md
├── scripts/              # Scripts bash
│   ├── knowledge-watcher-lib.sh
│   ├── start-knowledge-watcher.sh
│   ├── stop-knowledge-watcher.sh
│   ├── invoke-queue-processor.sh
│   └── register-watcher-cron.sh
├── processors/           # Pipeline de traitement
│   ├── classifier.sh
│   ├── summarizer.sh
│   └── formatter.sh
├── sources/              # Parseurs de sources
│   ├── claude-history-source.sh
│   ├── browser-bookmarks-source.sh
│   └── generic-file-source.sh
├── config/               # Configuration
│   ├── config.json
│   ├── sources.json
│   └── rules.json
└── data/                 # Données runtime
    ├── queue.json
    └── state.json
```

## Configuration

Fichier `config/config.json` :

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| paths.obsidianVault | Chemin du vault Obsidian | ~/Documents/Knowledge |
| paths.claudeCli | Chemin vers Claude CLI | ~/.local/bin/claude |
| processing.claudeTimeout | Timeout Claude CLI (ms) | 30000 |
| processing.maxFileSize | Taille max fichier (bytes) | 1048576 |
| processing.deduplicationWindow | Fenêtre dedup (ms) | 86400000 |

## Tiers de Sources

| Tier | Sources | Mode |
|------|---------|------|
| 1 | Claude history, Projets/, Knowledge/ | Real-time |
| 2 | Downloads/, Formations/ | Batch horaire |
| 3 | Browser bookmarks, VSCode, Scripts | Batch quotidien |
| 4 | Archives/, Resources/ | Batch hebdo |

## Commandes

| Commande | Description |
|----------|-------------|
| `/kwatch-start` | Démarrer la surveillance |
| `/kwatch-stop` | Arrêter la surveillance |
| `/kwatch-status` | Voir dashboard |
| `/kwatch-process` | Traiter la queue |
| `/kwatch-config` | Gérer configuration |
| `/kwatch-logs` | Voir les logs |
| `/kwatch-wizard setup` | Configuration initiale |
| `/kwatch-wizard sources` | Gérer les sources |

## Logs

Les logs sont stockés dans `data/logs/` avec rotation quotidienne.
