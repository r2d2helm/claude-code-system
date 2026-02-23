# /guardian-schedule

Configure la maintenance planifiee automatique du vault via cron.

## Usage

```
/guardian-schedule
/guardian-schedule --show
/guardian-schedule --remove
```

## Tiers de maintenance

| Tier | Frequence | Duree | Scope |
|------|-----------|-------|-------|
| Quick | Quotidien 08:00 | ~30s | Notes vides, liens casses |
| Cleanup | Dimanche 10:00 | ~2min | Orphelins, tags, frontmatter |
| Audit | 1er du mois 09:00 | ~5min | Rapport complet + metriques |

## Script

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$HOME/.claude/skills/vault-guardian-skill/scripts"
GUARDIAN_SCRIPT="$SCRIPT_DIR/invoke-vault-guardian.sh"
CRON_TAG="# vault-guardian-scheduled"
ACTION="${1:-install}"

show_schedule() {
  echo "=== VAULT GUARDIAN - MAINTENANCE PLANIFIEE ==="
  echo ""
  existing=$(crontab -l 2>/dev/null | grep "$CRON_TAG" || true)
  if [ -z "$existing" ]; then
    echo "Aucune tache planifiee trouvee."
  else
    echo "Taches actives :"
    echo "$existing" | while IFS= read -r line; do
      echo "  $line"
    done
  fi
  echo ""
}

remove_schedule() {
  echo "Suppression des taches vault-guardian..."
  crontab -l 2>/dev/null | grep -v "$CRON_TAG" | crontab -
  echo "Taches supprimees."
}

install_schedule() {
  echo "=== VAULT GUARDIAN - INSTALLATION MAINTENANCE ==="
  echo ""

  # Verifier que le script existe
  if [ ! -f "$GUARDIAN_SCRIPT" ]; then
    echo "ATTENTION: Script $GUARDIAN_SCRIPT introuvable."
    echo "Les entrees cron referenceront ce chemin."
    echo "Creez le script ou ajustez le chemin."
    echo ""
  fi

  # Retirer les anciennes entrees
  existing_cron=$(crontab -l 2>/dev/null | grep -v "$CRON_TAG" || true)

  # Nouvelles entrees cron
  new_cron="$existing_cron
# --- Vault Guardian - Maintenance planifiee --- $CRON_TAG
0 8 * * * $GUARDIAN_SCRIPT quick >> $HOME/.claude/hooks/logs/guardian-daily.log 2>&1 $CRON_TAG
0 10 * * 0 $GUARDIAN_SCRIPT fix >> $HOME/.claude/hooks/logs/guardian-weekly.log 2>&1 $CRON_TAG
0 9 1 * * $GUARDIAN_SCRIPT report >> $HOME/.claude/hooks/logs/guardian-monthly.log 2>&1 $CRON_TAG"

  echo "$new_cron" | crontab -

  echo "Taches installees :"
  echo ""
  echo "  TIER 1 - Quick Check (quotidien)"
  echo "  Cron:   0 8 * * *"
  echo "  Action: Verification rapide (notes vides, liens casses)"
  echo "  Duree:  ~30 secondes"
  echo "  Log:    ~/.claude/hooks/logs/guardian-daily.log"
  echo ""
  echo "  TIER 2 - Cleanup (hebdomadaire, dimanche)"
  echo "  Cron:   0 10 * * 0"
  echo "  Action: Auto-fix (orphelins, tags, frontmatter, status)"
  echo "  Duree:  ~2 minutes"
  echo "  Log:    ~/.claude/hooks/logs/guardian-weekly.log"
  echo ""
  echo "  TIER 3 - Audit (mensuel, 1er du mois)"
  echo "  Cron:   0 9 1 * *"
  echo "  Action: Rapport complet avec metriques et recommandations"
  echo "  Duree:  ~5 minutes"
  echo "  Log:    ~/.claude/hooks/logs/guardian-monthly.log"
  echo ""
  echo "Verifier avec : crontab -l | grep vault-guardian"
}

case "$ACTION" in
  --show|show)   show_schedule ;;
  --remove|remove) remove_schedule ;;
  install|*)     install_schedule ;;
esac

echo ""
echo "=== FIN CONFIGURATION ==="
```

## Entrees cron

```cron
# Tier 1 : Quick check quotidien a 08h00
0 8 * * * ~/.claude/skills/vault-guardian-skill/scripts/invoke-vault-guardian.sh quick

# Tier 2 : Cleanup hebdomadaire dimanche 10h00
0 10 * * 0 ~/.claude/skills/vault-guardian-skill/scripts/invoke-vault-guardian.sh fix

# Tier 3 : Audit mensuel le 1er a 09h00
0 9 1 * * ~/.claude/skills/vault-guardian-skill/scripts/invoke-vault-guardian.sh report
```

## Gestion

- `--show` : Afficher les taches planifiees actuelles
- `--remove` : Supprimer toutes les taches vault-guardian du crontab
- Sans argument : Installer les 3 tiers de maintenance
