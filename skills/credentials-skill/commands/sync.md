---
name: cred-sync
description: Comparer le registre avec les valeurs live sur les VMs
---

# /cred-sync - Synchronisation Registre vs Live

## Comportement

1. **Determiner le scope** :
   - `/cred-sync` : toutes les VMs
   - `/cred-sync vm100` : une VM specifique
   - `/cred-sync --fix` : corriger automatiquement les drifts

2. **Executer la comparaison** via :
   ```
   powershell.exe -File scripts/Sync-CredentialRegistry.ps1 -VM "{vm}"
   ```

3. **Pour chaque credential de la VM cible** :
   - Lire la valeur dans le registre
   - Lire la valeur live (SSH + grep .env, docker inspect)
   - Comparer (hash, pas les valeurs en clair dans le rapport)

4. **Classifier les resultats** :
   - IN_SYNC : valeurs identiques
   - DRIFT : valeurs differentes (registre != live)
   - MISSING_LIVE : dans le registre mais pas sur la VM
   - MISSING_REG : sur la VM mais pas dans le registre

5. **Si --fix** : proposer la mise a jour du registre avec les valeurs live

## Format de sortie

```
# Sync Report

## VM: {vm}

| Service | Slug | Status | Details |
|---------|------|--------|---------|
| Beszel | beszel | IN_SYNC | - |
| PostgreSQL | postgres | DRIFT | Password changed on VM |
| Redis | redis | MISSING_REG | Found in .env, not in registry |

## Summary
- In sync: X
- Drifted: X
- Missing (live): X
- Missing (registry): X
```
