---
name: knowledge-watcher-skill
description: Surveillance automatique des sources de connaissances
prefix: /kwatch-*
---

# Knowledge Watcher Agent

Agent de surveillance qui monitore automatiquement les sources de données sur la machine et les transforme en notes structurées dans le vault Obsidian.

## Philosophie

> "La connaissance non capturée est la connaissance perdue." — PKM

Cet agent fonctionne en mode hybride : surveillance temps réel pour les sources critiques (conversations Claude, projets actifs) et traitement batch pour les archives et ressources moins urgentes.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 KNOWLEDGE WATCHER AGENT                     │
├─────────────────────────────────────────────────────────────┤
│  TIER 1 (Real-time)         TIER 2-4 (Batch)               │
│  ┌─────────────────┐        ┌─────────────────┐            │
│  │ FileSystem      │        │ Task Scheduler  │            │
│  │ Watcher         │        │ (hourly/daily)  │            │
│  └────────┬────────┘        └────────┬────────┘            │
│           └──────────┬───────────────┘                      │
│                      ▼                                      │
│           ┌─────────────────┐                               │
│           │  CAPTURE QUEUE  │  (JSON + dedup)               │
│           └────────┬────────┘                               │
│                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ CLASSIFIER → SUMMARIZER (Claude) → FORMATTER           ││
│  └─────────────────────────────────────────────────────────┘│
│                    ▼                                        │
│           ┌─────────────────┐                               │
│           │ OBSIDIAN VAULT  │                               │
│           └─────────────────┘                               │
└─────────────────────────────────────────────────────────────┘
```

## Sources de Données (Tiers)

| Tier | Mode | Sources | Fréquence |
|------|------|---------|-----------|
| 1 | Real-time | Claude history, Projets/, Knowledge/ | FileSystemWatcher |
| 2 | Batch | Downloads/, Formations/ | Toutes les heures |
| 3 | Batch | Browser bookmarks, VSCode, Scripts | Quotidien 6h |
| 4 | Batch | Archives/, Resources/ | Hebdo dimanche 3h |

## Commandes Slash

### Contrôle

| Commande | Description |
|----------|-------------|
| `/kwatch-start` | Démarrer tous les watchers |
| `/kwatch-stop` | Arrêter tous les watchers |
| `/kwatch-status` | Dashboard avec stats et queue |
| `/kwatch-process` | Traiter la queue manuellement |
| `/kwatch-config` | Gérer la configuration |
| `/kwatch-logs` | Voir les logs de capture |

### Wizards

| Commande | Description |
|----------|-------------|
| `/kwatch-wizard setup` | Configuration initiale guidée |
| `/kwatch-wizard sources` | Gérer les sources de données |

## Pipeline de Traitement

### 1. Capture
- FileSystemWatcher détecte les changements (Tier 1)
- Task Scheduler déclenche les scans batch (Tier 2-4)
- Les éléments sont ajoutés à la queue avec hash pour déduplication

### 2. Classification
- Analyse du contenu et des patterns
- Attribution automatique du type (conversation, code, concept, troubleshooting, project)
- Suggestion de tags basée sur les mots-clés

### 3. Résumé (Claude CLI)
- Appel à Claude pour générer un résumé en français
- Extraction des points clés
- Identification des concepts liés

### 4. Formatage
- Génération du fichier Markdown avec frontmatter YAML
- Application du template approprié
- Création des liens Obsidian (wikilinks)

### 5. Intégration
- Sauvegarde dans le dossier approprié du vault
- Mise à jour de la Daily Note
- Mise à jour de l'index si nécessaire

## Configuration

```json
{
  "paths": {
    "obsidianVault": "~/Documents/Knowledge",
    "claudeCli": "~/.local/bin/claude"
  },
  "processing": {
    "claudeTimeout": 30000,
    "maxFileSize": 1048576,
    "deduplicationWindow": 86400000
  }
}
```

## Règles de Classification

| Type | Patterns | Dossier |
|------|----------|---------|
| conversation | history.jsonl, User:, Assistant: | Conversations/ |
| code | .sh, .py, function, def | Code/{lang}/ |
| concept | pattern, architecture, principe | Concepts/ |
| troubleshooting | error, fix, solution | Références/Troubleshooting/ |
| project | Projets/ | Projets/{name}/ |

## Intégration avec Autres Skills

| Skill | Intégration |
|-------|-------------|
| knowledge-skill | Évite doublons avec `/know-save` |
| obsidian-skill | `/obs-health` après batch |
| fileorg-skill | Organise Downloads avant capture |

## Prérequis

### Linux (Ubuntu 24.04+)
- Ubuntu 24.04+ / Debian 12+
- inotify-tools (`sudo apt install inotify-tools`)
- jq (`sudo apt install jq`)
- bc (généralement pré-installé)
- Claude CLI installé
- Obsidian vault configuré

## Scripts

| Script | Description |
|--------|-------------|
| `start-knowledge-watcher.sh` | Démarre les watchers avec inotifywait |
| `stop-knowledge-watcher.sh` | Arrête les watchers |
| `build-notes-index.sh` | Construit l'index des notes |

### Utilisation

```bash
# Démarrer le watcher (foreground)
./scripts/start-knowledge-watcher.sh

# Démarrer en arrière-plan
./scripts/start-knowledge-watcher.sh --background

# Arrêter le watcher
./scripts/stop-knowledge-watcher.sh

# Construire l'index
./scripts/build-notes-index.sh [vault_path] [output_path]
```

### Tâches Planifiées (Crontab)

Les entrées crontab sont documentées dans `scripts/crontab-linux.md` :

| Tier | Crontab | Fréquence |
|------|---------|-----------|
| Tier 2 | `0 * * * *` | Toutes les heures |
| Tier 3 | `0 6 * * *` | Quotidien à 6h |
| Tier 4 | `0 3 * * 0` | Dimanche à 3h |

Voir `scripts/crontab-linux.md` pour les instructions d'installation complètes.
