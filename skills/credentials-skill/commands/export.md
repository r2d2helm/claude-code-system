---
name: cred-export
description: Exporter le registre vers Bitwarden CSV, KeePass XML, JSON ou CSV
---

# /cred-export - Export Credentials

## Comportement

1. **Determiner le format** :
   - `/cred-export bitwarden` : Bitwarden CSV
   - `/cred-export keepass` : KeePass XML
   - `/cred-export json` : JSON structure
   - `/cred-export csv` : CSV generique

2. **Executer l'export** via :
   ```
   powershell.exe -File scripts/Export-Credentials.ps1 -Format "{format}"
   ```

3. **Generer le fichier** dans `data/exports/{format}_{timestamp}.{ext}`

4. **Bitwarden CSV** colonnes : folder, favorite, type, name, notes, fields, reprompt, login_uri, login_username, login_password, login_totp

5. **Ne jamais envoyer** le fichier exporte vers un service externe

## Format de sortie

```
# Export Credentials

- **Format** : {format}
- **Fichier** : data/exports/{filename}
- **Entries** : X credentials exportes
- **Taille** : X KB

Note: Le fichier contient des mots de passe en clair. Protegez-le adequatement.
```
