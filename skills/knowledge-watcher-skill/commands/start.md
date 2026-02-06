# Commande: /kwatch-start

Démarre le Knowledge Watcher Agent.

## Syntaxe

```
/kwatch-start [--background]
```

## Description

Cette commande démarre les FileSystemWatchers pour les sources Tier 1 (temps réel) et active la surveillance automatique des fichiers.

## Exécution

**IMPORTANT**: Exécute ce script PowerShell:

```powershell
$SkillPath = "$env:USERPROFILE\.claude\skills\knowledge-watcher-skill"
& "$SkillPath\scripts\Start-KnowledgeWatcher.ps1"
```

## Options

| Option | Description |
|--------|-------------|
| `--background` | Exécuter en mode arrière-plan |

## Ce qui est surveillé (Tier 1)

| Source | Chemin | Patterns |
|--------|--------|----------|
| Claude History | `~\.claude\history.jsonl` | *.jsonl |
| Projets | `~\Projets` | *.md, *.ps1, *.py, *.json |
| Knowledge | `~\Documents\Knowledge` | *.md |

## Exemple de sortie

```
🚀 Starting Knowledge Watcher...
  ✅ Watching: Projets Actifs (C:\Users\r2d2\Projets)
  ✅ Watching: Knowledge Vault (C:\Users\r2d2\Documents\Knowledge)
  ✅ Watching: Claude History

✅ Knowledge Watcher started
   PID: 12345
   Watchers: 3

   Press Ctrl+C to stop...
```

## Après le démarrage

- Les fichiers modifiés dans les dossiers surveillés sont automatiquement capturés
- Utilisez `/kwatch-status` pour voir l'état
- Utilisez `/kwatch-process` pour traiter la queue
- Utilisez `/kwatch-stop` pour arrêter

## Prérequis

- PowerShell 7.4+
- Les chemins sources doivent exister
- Claude CLI installé pour les résumés IA
