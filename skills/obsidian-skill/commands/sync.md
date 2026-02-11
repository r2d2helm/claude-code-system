# Commande: /obs-sync

Synchroniser le vault avec un backup ou un depot Git.

## Syntaxe

```
/obs-sync [mode] [options]
```

## Actions

### Sync Git

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"

# Status
git -C $VaultPath status --short

# Commit et push
git -C $VaultPath add -A
git -C $VaultPath commit -m "vault: sync $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git -C $VaultPath push
```

### Sync backup (ZIP)

```powershell
$BackupDir = "$env:USERPROFILE\Documents\Backups\Knowledge"
$Timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$ZipPath = Join-Path $BackupDir "Knowledge_$Timestamp.zip"

if (-not (Test-Path $BackupDir)) { New-Item -ItemType Directory -Path $BackupDir -Force }

Compress-Archive -Path "$VaultPath\*" -DestinationPath $ZipPath -CompressionLevel Optimal
Write-Output "Backup: $ZipPath"

# Rotation : garder les 5 derniers
Get-ChildItem $BackupDir -Filter "Knowledge_*.zip" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -Skip 5 |
    Remove-Item -Force
```

### Comparer deux vaults

```powershell
$Source = "$env:USERPROFILE\Documents\Knowledge"
$Target = "D:\Backup\Knowledge"

# Fichiers differents
$SourceFiles = Get-ChildItem -Path $Source -Recurse -Filter "*.md"
$TargetFiles = Get-ChildItem -Path $Target -Recurse -Filter "*.md"

Compare-Object $SourceFiles $TargetFiles -Property Name, Length, LastWriteTime
```

## Options

| Option | Description |
|--------|-------------|
| `git` | Commit et push Git |
| `backup` | Creer un backup ZIP |
| `compare` | Comparer avec un backup |
| `--message` | Message de commit personnalise |

## Exemples

```powershell
/obs-sync git                           # Commit + push
/obs-sync backup                        # Backup ZIP
/obs-sync compare D:\Backup\Knowledge   # Comparer
```

## Voir Aussi

- `/obs-backup` - Backup complet
- `/obs-export` - Export en differents formats
