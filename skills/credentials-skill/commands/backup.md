---
name: cred-backup
description: Sauvegarder le registre de credentials
---

# /cred-backup - Backup du Registre

## Comportement

1. **Creer une archive** du dossier `data/registry/` :
   - Destination : `C:\Users\r2d2\Documents\claude-config-backup\credentials\`
   - Format : `credentials-backup_{timestamp}.zip` ou copie directe du dossier

2. **Calculer les checksums** SHA256 de chaque fichier

3. **Generer un manifeste** `backup-manifest.json` avec :
   - Date de backup
   - Nombre de fichiers
   - Checksums
   - Taille totale

4. **Copier** vers le dossier backup

5. **Nettoyer** les anciens backups (garder les 5 derniers)

## Execution

```
powershell.exe -NoProfile -Command "
$src = '$HOME\.claude\skills\credentials-skill\data\registry'
$dst = '$HOME\Documents\claude-config-backup\credentials'
$ts = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupDir = Join-Path $dst \"backup_$ts\"
if (-not (Test-Path $dst)) { New-Item -ItemType Directory -Path $dst -Force }
Copy-Item -Path $src -Destination $backupDir -Recurse
"
```

## Format de sortie

```
# Credential Backup

- **Date** : YYYY-MM-DD HH:mm
- **Destination** : Documents/claude-config-backup/credentials/backup_{timestamp}/
- **Fichiers** : X
- **Taille** : X KB

## Checksums
| File | SHA256 |
|------|--------|
| beszel.md | abc123... |

## Retention
- Backups conserves : 5
- Plus ancien : YYYY-MM-DD
```
