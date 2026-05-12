# Commande: /kwatch-stop

Arrête le Knowledge Watcher Agent.

## Syntaxe

```
/kwatch-stop
```

## Description

Cette commande arrête proprement tous les watchers en cours d'exécution et nettoie les ressources.

## Exécution

**IMPORTANT**: Exécute ce script bash:

```bash
SKILL_PATH="$HOME/.claude/skills/knowledge-watcher-skill"
bash "$SKILL_PATH/scripts/stop-knowledge-watcher.sh"
```

## Ce qui est arrêté

1. Les processus inotifywait actifs
2. Les jobs bash associés
3. Les fichiers PID et state

## Exemple de sortie

```
⏹️  Stopping Knowledge Watcher (PID: 12345)...
✅ Knowledge Watcher stopped
```

Ou si non actif:

```
ℹ️  Knowledge Watcher is not running
```

## Notes

- L'arrêt est gracieux (pas de perte de données)
- La queue n'est PAS effacée - les items en attente restent
- Pour reprendre, utilisez `/kwatch-start`
