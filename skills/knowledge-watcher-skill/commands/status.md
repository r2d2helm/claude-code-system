# Commande: /kwatch-status

Affiche le dashboard de statut du Knowledge Watcher.

## Syntaxe

```
/kwatch-status [--json]
```

## Description

Affiche un tableau de bord complet avec l'état des watchers, les statistiques de la queue, et les dernières exécutions batch.

## Exécution

**IMPORTANT**: Exécute ce script bash pour afficher le statut:

```bash
SKILL_PATH="$HOME/.claude/skills/knowledge-watcher-skill"
bash "$SKILL_PATH/scripts/kw-status.sh"
```

## Exemple de sortie

```
╔══════════════════════════════════════════════════════════════╗
║            🔍 KNOWLEDGE WATCHER STATUS                       ║
╠══════════════════════════════════════════════════════════════╣
║  Status        : ✅ RUNNING
║  Started At    : 2026-02-05T10:30:00
║  PID           : 12345
╠══════════════════════════════════════════════════════════════╣
║  QUEUE                                                       ║
║  ├─ Total Items    : 5
║  ├─ Pending        : 3
║  └─ Max Size       : 100
╠══════════════════════════════════════════════════════════════╣
║  STATISTICS                                                  ║
║  ├─ Total Captured : 42
║  ├─ Processed      : 39
║  └─ Errors         : 0
╠══════════════════════════════════════════════════════════════╣
║  SOURCES                                                     ║
║  ├─ Enabled        : 5 / 10
║  └─ Vault Path     : ~/Documents/Knowledge
╠══════════════════════════════════════════════════════════════╣
║  LAST BATCH RUNS                                             ║
║  ├─ Tier 2 (hourly): 2026-02-05T10:00:00
║  ├─ Tier 3 (daily) : 2026-02-05T06:00:00
║  └─ Tier 4 (weekly): 2026-02-02T03:00:00
╚══════════════════════════════════════════════════════════════╝
```

## Options

| Option | Description |
|--------|-------------|
| `--json` | Sortie JSON pour intégration |

## Pour format JSON

```bash
SKILL_PATH="$HOME/.claude/skills/knowledge-watcher-skill"
bash "$SKILL_PATH/scripts/kw-status.sh" --json | jq .
```

## Interprétation

| Indicateur | Signification |
|------------|---------------|
| ✅ RUNNING | Watchers actifs |
| ⏹️ STOPPED | Watchers arrêtés |
| Pending | Items en attente de traitement |
| Errors | Échecs de traitement |
