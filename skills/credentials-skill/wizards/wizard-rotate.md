---
name: wizard-rotate
description: Rotation guidee multi-services avec planification et rollback
---

# Wizard Rotate - Rotation Groupee

## Questions

1. **Scope** : Quels credentials rotationner ?
   - Tous les overdue
   - Une categorie specifique
   - Une VM specifique
   - Selection manuelle

2. **Strategie** : Ordre de rotation ?
   - Par criticality (low first, critical last) - recommande
   - Par VM (une VM a la fois)
   - Par anciennete (plus ancien d'abord)

3. **Validation** : Tester apres chaque rotation ?
   - Oui, valider immediatement (plus lent, plus sur)
   - Non, valider en batch a la fin

## Processus

### Etape 1 : Planifier
1. Lister les credentials a rotationner
2. Calculer l'ordre selon la strategie choisie
3. Afficher le plan avec estimations

### Etape 2 : Pre-validation
Pour chaque credential dans le scope :
1. Verifier que la VM est accessible (SSH)
2. Verifier que le service est up
3. Identifier le fichier de config a modifier

### Etape 3 : Execution sequentielle
Pour chaque credential :
1. Generer un nouveau password (`New-SecurePassword.ps1`)
2. Sauvegarder l'ancien password (en memoire, pour rollback)
3. Deployer le nouveau password sur la VM
4. Redemarrer le service si necessaire
5. Si validation immediate : tester la connexion
6. Si OK : mettre a jour le registre + log rotation
7. Si FAIL : rollback automatique vers l'ancien password

### Etape 4 : Rapport final
- Resume de toutes les rotations
- Succes / echecs
- Score de sante avant/apres

## Rollback
- Chaque rotation est reversible pendant l'execution du wizard
- Ancien password conserve jusqu'a la fin du wizard
- En cas d'echec : restauration automatique + notification

## Format de sortie

```
# Rotation Report

## Plan execute
| # | Service | Slug | Status | New Password | Validated |
|---|---------|------|--------|-------------|-----------|
| 1 | Redis | redis | OK | ****...** | Yes |
| 2 | Beszel | beszel | OK | ****...** | Yes |
| 3 | Langfuse | langfuse | FAILED | - | Rolled back |

## Score de sante
- Avant : XX/100
- Apres : XX/100

## Prochaines rotations
| Service | Due Date |
|---------|----------|
```
