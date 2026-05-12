---
name: cred-audit
description: Rapport de compliance et score de sante des credentials
---

# /cred-audit - Audit Credentials

## Comportement

1. **Executer le score de sante** via `Measure-CredentialHealth.ps1` :
   ```
   powershell.exe -File scripts/Measure-CredentialHealth.ps1
   ```

2. **Calculer 4 axes** (25 points chacun, total /100) :
   - **Age** (/25) : penalite pour credentials jamais rotationnees ou > 90 jours
   - **Force** (/25) : longueur, complexite, entropie des mots de passe
   - **Couverture** (/25) : % de services decouverts qui sont dans le registre
   - **Fraicheur** (/25) : % de credentials valides recemment (< 7 jours)

3. **Generer les recommandations** par priorite

4. **Sauvegarder** le score dans `data/audit-history.json`

## Format de sortie

```
# Credential Audit Report

**Date** : YYYY-MM-DD
**Score Global** : XX/100

## Details du Score
| Axe | Score | Details |
|-----|-------|---------|
| Age | XX/25 | X credentials > 90 jours |
| Force | XX/25 | X passwords faibles |
| Couverture | XX/25 | X services non couverts |
| Fraicheur | XX/25 | X validations > 7 jours |

## Recommandations
1. [CRITICAL] Rotationner {slug} (age: X jours)
2. [HIGH] Valider {slug} (jamais teste)
3. [MEDIUM] Renforcer {slug} (password faible)

## Historique
| Date | Score |
|------|-------|
| YYYY-MM-DD | XX/100 |
```
