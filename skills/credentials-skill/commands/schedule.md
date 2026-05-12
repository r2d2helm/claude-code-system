---
name: cred-schedule
description: Planifier et visualiser les rotations de credentials
---

# /cred-schedule - Calendrier de Rotation

## Comportement

1. **Lire l'index** et calculer les dates de rotation pour chaque credential :
   - Date due = last_rotated + rotation_interval_days
   - Status : overdue | due_soon (< 30 jours) | ok

2. **Afficher le calendrier** trie par date due (plus urgent en premier)

3. **Options** :
   - `/cred-schedule` : vue calendrier
   - `/cred-schedule --overdue` : seulement les retards
   - `/cred-schedule --next 30` : rotations dans les N prochains jours

4. **Mettre a jour** `data/rotation-schedule.json` avec les prochaines echeances

## Format de sortie

```
# Rotation Schedule

## Overdue (action requise)
| Service | Slug | Last Rotated | Due Date | Overdue By |
|---------|------|-------------|----------|------------|
| ... | ... | ... | ... | X jours |

## Due Soon (< 30 jours)
| Service | Slug | Due Date | Days Left |
|---------|------|----------|-----------|
| ... | ... | ... | X |

## On Track
| Service | Slug | Due Date | Days Left |
|---------|------|----------|-----------|
| ... | ... | ... | X |

## Statistiques
- Overdue : X
- Due soon : X
- On track : X
- Next rotation : {slug} dans X jours
```
