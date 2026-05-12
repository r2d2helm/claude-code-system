---
name: cred-discover
description: Scanner les VMs pour decouvrir des secrets non repertories
---

# /cred-discover - Decouverte de Credentials

## Comportement

1. **Determiner le scope** :
   - `/cred-discover` : toutes les VMs accessibles
   - `/cred-discover vm100` : une VM specifique
   - `/cred-discover --deep` : scan approfondi (plus lent)

2. **Executer le scan** via SSH sur chaque VM :
   ```
   powershell.exe -File scripts/Invoke-CredentialDiscovery.ps1 -VM "{vm}"
   ```

3. **Sources scannees** :
   - Fichiers `.env` dans les repertoires de compose
   - `docker inspect` des containers pour les variables d'environnement
   - Fichiers de config connus (nginx.conf, pg_hba.conf, etc.)
   - Docker secrets montees

4. **Comparer** avec le registre existant pour identifier :
   - Credentials inconnus (pas dans le registre)
   - Credentials modifies (valeur differente du registre)
   - Services non couverts

5. **Ne jamais afficher** les mots de passe decouverts en clair - juste signaler leur existence

## Format de sortie

```
# Credential Discovery Report

## VM scannees
| VM | Status | .env Files | Containers | Configs |
|----|--------|------------|------------|---------|
| vm100 | scanned | 3 | 6 | 2 |
| vm103 | scanned | 8 | 29 | 5 |

## Credentials trouves
| Source | Service | Type | In Registry? | Drift? |
|--------|---------|------|-------------|--------|
| .env | BESZEL_PASSWORD | password | Yes (beszel) | No |
| .env | POSTGRES_PASSWORD | password | No | - |
| docker | REDIS_URL | connection | No | - |

## Actions suggerees
1. [NEW] Ajouter {service} au registre (/cred-add)
2. [DRIFT] Mettre a jour {slug} - valeur differente (/cred-sync)
```
