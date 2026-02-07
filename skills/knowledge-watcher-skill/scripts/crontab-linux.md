# Crontab Entries pour Knowledge Watcher (Linux)

Ce document contient les entrées crontab pour les tâches planifiées Tier 2-4 sur Linux.
Ces entrées remplacent les Windows Task Scheduler jobs de `scheduled/`.

## Installation

1. Éditer le crontab :
   ```bash
   crontab -e
   ```

2. Ajouter les entrées ci-dessous (adapter `SKILL_DIR` au chemin réel) :

## Entrées Crontab

```crontab
# ============================================================
# Knowledge Watcher - Scheduled Tasks (Linux)
# ============================================================

# Variables d'environnement
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
SKILL_DIR=/path/to/knowledge-watcher-skill

# ------------------------------------------------------------
# TIER 2 - Traitement Horaire (Downloads, Formations)
# Exécution: chaque heure à la minute 0
# ------------------------------------------------------------
0 * * * * cd "$SKILL_DIR" && ./scripts/tier2-hourly.sh >> "$SKILL_DIR/data/logs/tier2-$(date +\%Y-\%m-\%d).log" 2>&1

# ------------------------------------------------------------
# TIER 3 - Traitement Quotidien (Bookmarks, Scripts)
# Exécution: tous les jours à 6h00
# ------------------------------------------------------------
0 6 * * * cd "$SKILL_DIR" && ./scripts/tier3-daily.sh >> "$SKILL_DIR/data/logs/tier3-$(date +\%Y-\%m-\%d).log" 2>&1

# ------------------------------------------------------------
# TIER 4 - Traitement Hebdomadaire (Archives, Resources)
# Exécution: dimanche à 3h00
# ------------------------------------------------------------
0 3 * * 0 cd "$SKILL_DIR" && ./scripts/tier4-weekly.sh >> "$SKILL_DIR/data/logs/tier4-$(date +\%Y-\%m-\%d).log" 2>&1

# ------------------------------------------------------------
# Nettoyage des logs (optionnel)
# Supprime les logs de plus de 30 jours
# Exécution: dimanche à 4h00
# ------------------------------------------------------------
0 4 * * 0 find "$SKILL_DIR/data/logs" -name "*.log" -mtime +30 -delete 2>/dev/null
```

## Scripts Tier (à créer si besoin)

Les scripts `tier2-hourly.sh`, `tier3-daily.sh`, `tier4-weekly.sh` devraient :

1. Sourcer les utilitaires communs
2. Scanner les sources de leur tier
3. Ajouter les fichiers modifiés à la queue
4. Logger l'exécution

### Exemple minimal pour tier2-hourly.sh

```bash
#!/usr/bin/env bash
# tier2-hourly.sh - Traitement batch Tier 2
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="${SKILL_DIR}/data/logs"

log_message() {
    echo "$(date -Iseconds) [$1] $2"
}

log_message "INFO" "Tier 2 (Hourly) - Démarrage"

# Sources Tier 2 (Downloads, Formations)
SOURCES=(
    "$HOME/Downloads"
    "$HOME/Documents/Formations"
)

# Patterns à capturer
PATTERNS=("*.pdf" "*.md" "*.txt" "*.docx")

for source in "${SOURCES[@]}"; do
    if [[ -d "$source" ]]; then
        log_message "INFO" "Scanning: $source"
        # TODO: Implémenter le scan et l'ajout à la queue
    fi
done

log_message "INFO" "Tier 2 (Hourly) - Terminé"
```

## Vérification

```bash
# Lister les crontabs actifs
crontab -l

# Vérifier les logs
tail -f /path/to/knowledge-watcher-skill/data/logs/tier2-*.log
```

## Correspondance avec Windows Task Scheduler

| Script Windows | Script Linux | Fréquence |
|----------------|--------------|-----------|
| `KnowledgeWatcher-Tier2-Hourly.ps1` | `tier2-hourly.sh` | `0 * * * *` (chaque heure) |
| `KnowledgeWatcher-Tier3-Daily.ps1` | `tier3-daily.sh` | `0 6 * * *` (6h quotidien) |
| `KnowledgeWatcher-Tier4-Weekly.ps1` | `tier4-weekly.sh` | `0 3 * * 0` (3h dimanche) |

## Notes

- Les chemins doivent être adaptés à votre environnement Linux
- Si vous utilisez WSL, les chemins Windows sont accessibles via `/mnt/c/`, `/mnt/d/`, etc.
- Pour désactiver temporairement une tâche, commentez la ligne avec `#`
- Les logs sont créés dans `data/logs/` avec la date du jour
