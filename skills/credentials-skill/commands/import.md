---
name: cred-import
description: Importer des credentials depuis une source externe
---

# /cred-import - Import Credentials

## Comportement

1. **Detecter le format** du fichier source :
   - `/cred-import file.csv` : detection auto (Bitwarden CSV, KeePass CSV)
   - `/cred-import docker-compose.yml` : extraction depuis compose
   - `/cred-import vm100-credentials.md` : parsing du fichier plat legacy
   - `/cred-import .env` : parsing de variables d'environnement

2. **Executer l'import** via :
   ```
   powershell.exe -File scripts/Import-Credentials.ps1 -Source "{file}" -Format "{format}"
   ```

3. **Pour chaque credential trouve** :
   - Verifier si le slug existe deja dans le registre
   - Si doublon : demander merge / skip / overwrite
   - Si nouveau : creer l'entree avec le template

4. **Mettre a jour l'index** apres import

5. **Afficher un resume** des actions effectuees

## Format de sortie

```
# Import Results

- **Source** : {filename}
- **Format detecte** : {format}

| Service | Slug | Action | Status |
|---------|------|--------|--------|
| Beszel Hub | beszel | Created | OK |
| PostgreSQL | postgres | Skipped (exists) | - |
| ... | ... | ... | ... |

## Summary
- Imported: X new
- Skipped: X duplicates
- Errors: X
- Index updated
```
