---
name: cred-rotate
description: Rotation d un credential (generer, deployer, valider)
---

# /cred-rotate - Rotation de Credential

## Comportement

1. **Lire le credential** existant et afficher un resume

2. **Generer un nouveau mot de passe** via `New-SecurePassword.ps1` :
   ```
   powershell.exe -File scripts/New-SecurePassword.ps1 -Length 24
   ```

3. **Afficher la procedure de rotation** specifique au service (lire `references/rotation-procedures.md`)

4. **Guider l'execution** etape par etape :
   - a. Generer le nouveau password
   - b. Mettre a jour le fichier .env ou config sur la VM cible
   - c. Redemarrer le service (docker compose restart, systemctl restart, etc.)
   - d. Valider la connexion avec le nouveau password
   - e. Mettre a jour le registre (frontmatter : password, last_rotated)
   - f. Logger la rotation

5. **Chaque etape demande confirmation** avant de passer a la suivante

6. **Rollback** : si la validation echoue, proposer de restaurer l'ancien password

## Format de sortie

```
# Rotation : {service}

## Etape 1/6 : Generation
- Nouveau password : {new_password}
- Force : Excellent (92/100, ~148 bits)

## Etape 2/6 : Deploiement
- Cible : {vm} ({host})
- Fichier : {compose_path}/.env
- Commande : ssh {vm} "sed -i 's/OLD/NEW/' .env && docker compose restart"

## Etape 3/6 : Validation
- Test : {validation_method}
- Resultat : OK / FAILED

## Resultat
- Rotation reussie
- Registre mis a jour
- Log ajoute
```
