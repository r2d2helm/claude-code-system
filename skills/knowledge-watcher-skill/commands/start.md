# Commande: /kwatch-start

Démarre le Knowledge Watcher Agent.

## Syntaxe

```
/kwatch-start [--background]
```

## Description

Cette commande démarre les watchers inotifywait pour les sources Tier 1 (temps réel) et active la surveillance automatique des fichiers.

## Exécution

**IMPORTANT**: Exécute ce script bash:

```bash
SKILL_PATH="$HOME/.claude/skills/knowledge-watcher-skill"
bash "$SKILL_PATH/scripts/start-knowledge-watcher.sh"
```

## Options

| Option | Description |
|--------|-------------|
| `--background` | Exécuter en mode arrière-plan |

## Ce qui est surveillé (Tier 1)

| Source | Chemin | Patterns |
|--------|--------|----------|
| Claude History | `~/.claude/history.jsonl` | *.jsonl |
| Projets | `~/Projets` | *.md, *.sh, *.py, *.json |
| Knowledge | `~/Documents/Knowledge` | *.md |

## Exemple de sortie

```
🚀 Starting Knowledge Watcher...
  ✅ Watching: Projets Actifs (~/Projets)
  ✅ Watching: Knowledge Vault (~/Documents/Knowledge)
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

- inotify-tools installé (`sudo apt install inotify-tools`)
- Les chemins sources doivent exister
- Claude CLI installé pour les résumés IA
