---
name: cred-list
description: Lister et filtrer les credentials du registre
---

# /cred-list - Lister les Credentials

## Comportement

1. **Charger l'index** depuis `data/registry/_index.json` via le script PowerShell :
   ```
   powershell.exe -File scripts/CredentialRegistry.psm1
   ```
   Ou lire directement `_index.json` avec Read tool.

2. **Appliquer les filtres** si specifie :
   - `/cred-list` : tout afficher
   - `/cred-list monitoring` : filtrer par category
   - `/cred-list vm100` : filtrer par VM
   - `/cred-list --expired` : credentials avec validation_status = failed ou expired
   - `/cred-list --overdue` : rotation en retard (last_rotated + rotation_interval_days < today)

3. **Formater en tableau** trie par criticality (critical > high > medium > low)

4. **Masquer les mots de passe** par defaut (ne pas lire les fichiers individuels, juste l'index)

## Format de sortie

```
# Credential Registry (X entries)

## Filtres appliques : [category=monitoring | vm=vm100 | all]

| Service | Slug | Category | VM | Auth | Status | Last Rotated | Criticality |
|---------|------|----------|----|------|--------|--------------|-------------|
| Beszel Hub | beszel | monitoring | vm100 | password | OK | 2026-02-01 | high |
| ... | ... | ... | ... | ... | ... | ... | ... |

## Statistiques
- Total : X credentials
- Par category : monitoring (X), database (X), api (X), ...
- Validation : OK (X), failed (X), untested (X)
- Rotation overdue : X
```
