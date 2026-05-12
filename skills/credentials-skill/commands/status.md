---
name: cred-status
description: Dashboard synthese du registre de credentials
---

# /cred-status - Dashboard Credentials

## Comportement

1. **Lire l'index** `data/registry/_index.json`

2. **Calculer les metriques** :
   - Total credentials
   - Par category (monitoring, database, api, ssh, web, bot, infra, oauth)
   - Par VM
   - Par criticality
   - Par validation_status (ok, failed, untested, expired)
   - Rotations overdue (last_rotated + rotation_interval_days < today)
   - Rotations a venir (dans les 30 prochains jours)

3. **Lire le dernier audit** depuis `data/audit-history.json` si disponible

4. **Formater** un dashboard compact

## Format de sortie

```
# Credential Registry Dashboard

## Vue d'ensemble
- **Total** : X credentials
- **Score sante** : XX/100 (dernier audit: YYYY-MM-DD)

## Par categorie
| Category | Count | OK | Failed | Untested |
|----------|-------|----|--------|----------|
| monitoring | X | X | X | X |
| database | X | X | X | X |
| ... | ... | ... | ... | ... |

## Par VM
| VM | Count | Overdue |
|----|-------|---------|
| vm100 | X | X |
| vm103 | X | X |

## Alertes
- [OVERDUE] X credentials en retard de rotation
- [UNTESTED] X credentials jamais valides
- [FAILED] X credentials en echec de validation

## Prochaines rotations (30 jours)
| Service | Slug | Due Date |
|---------|------|----------|
```
