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
| 3 | Batch | Browser bookmarks, VSCode, Scripts PS | Quotidien 6h |
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
    "obsidianVault": "C:\\Users\\r2d2\\Documents\\Knowledge",
    "claudeCli": "C:\\Users\\r2d2\\.local\\bin\\claude.exe"
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
| code | .ps1, .py, function, def | Code/{lang}/ |
| concept | pattern, architecture, principe | Concepts/ |
| troubleshooting | error, fix, solution | Références/Troubleshooting/ |
| project | \Projets\ | Projets/{name}/ |

## Intégration avec Autres Skills

| Skill | Intégration |
|-------|-------------|
| knowledge-skill | Évite doublons avec `/know-save` |
| obsidian-skill | `/obs-health` après batch |
| fileorg-skill | Organise Downloads avant capture |

## Prérequis

- Windows 11/Server 2025
- PowerShell 7.4+
- Claude CLI installé
- Obsidian vault configuré
