# Commande: /kwatch-logs

Affiche les logs du Knowledge Watcher.

## Syntaxe

```
/kwatch-logs [--lines=N] [--level=LEVEL] [--date=DATE]
```

## Description

Affiche les logs de capture et de traitement du Knowledge Watcher.

## Exécution

**Afficher les 50 dernières lignes:**

```bash
SKILL_PATH="$HOME/.claude/skills/knowledge-watcher-skill"
LOG_DIR="$SKILL_PATH/data/logs"
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/kwatch_$TODAY.log"

if [ -f "$LOG_FILE" ]; then
    tail -n 50 "$LOG_FILE"
else
    echo "No logs for today"
fi
```

## Options

| Option | Description | Défaut |
|--------|-------------|--------|
| `--lines=N` | Nombre de lignes | 50 |
| `--level=LEVEL` | Filtrer par niveau (INFO, WARN, ERROR) | all |
| `--date=DATE` | Date spécifique (YYYY-MM-DD) | today |

## Format des logs

```
[2026-02-05 10:30:45] [INFO] Started watcher for: Projets Actifs
[2026-02-05 10:31:12] [INFO] Added to queue: ~/Projets/script.sh
[2026-02-05 10:31:15] [INFO] Processed: script.sh → 2026-02-05_Script.md
[2026-02-05 10:32:00] [WARN] File too large: bigfile.txt
[2026-02-05 10:33:00] [ERROR] Claude CLI timeout
```

## Filtrer par niveau

**Erreurs seulement:**
```bash
grep '\[ERROR\]' "$LOG_FILE"
```

**Warnings et erreurs:**
```bash
grep -E '\[(WARN|ERROR)\]' "$LOG_FILE"
```

## Logs des jours précédents

```bash
DATE="2026-02-04"
LOG_FILE="$LOG_DIR/kwatch_$DATE.log"
tail -n 100 "$LOG_FILE"
```

## Lister les fichiers de log

```bash
ls -lt "$LOG_DIR"/*.log
```

## Rotation des logs

Les logs sont créés quotidiennement avec le format `kwatch_YYYY-MM-DD.log`.
Les anciens logs ne sont pas automatiquement supprimés - nettoyez manuellement si nécessaire.

## Exemple de sortie

```
[2026-02-05 08:00:01] [INFO] Knowledge Watcher started with 3 watchers (PID: 12345)
[2026-02-05 08:15:32] [INFO] Added to queue: ~/Projets/api/handler.sh
[2026-02-05 08:15:33] [INFO] Captured file (Changed): handler.sh
[2026-02-05 08:20:00] [INFO] Processed: handler.sh → Code/Bash/2026-02-05_handler.md
[2026-02-05 08:20:00] [INFO] Updated Daily Note with: [[2026-02-05_handler]]
[2026-02-05 09:00:00] [INFO] Scanned Downloads: found 3 files, added 2 to queue
[2026-02-05 09:00:15] [WARN] Duplicate detected, skipping: readme.md
```
