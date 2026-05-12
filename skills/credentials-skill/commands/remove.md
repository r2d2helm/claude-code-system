---
name: cred-remove
description: Supprimer un credential du registre (avec archivage)
---

# /cred-remove - Supprimer un Credential

## Comportement

1. **Lire le credential** `data/registry/{slug}.md` et afficher un resume

2. **Demander confirmation** explicite avant suppression

3. **Archiver** le fichier dans `data/registry/_archive/{slug}_{timestamp}.md`
   via le script PowerShell :
   ```
   powershell.exe -NoProfile -Command "Import-Module scripts/CredentialRegistry.psm1; Remove-CredentialEntry -Slug '{slug}'"
   ```

4. **Mettre a jour l'index** via Update-CredentialIndex

5. **Logger** l'action dans rotation-log.jsonl

## Format de sortie

```
# Credential supprime

- **Service** : {service}
- **Slug** : {slug}
- **Archive** : data/registry/_archive/{slug}_{timestamp}.md

Index mis a jour : X entries restantes.
```
