# Commande: /file-backup

Sauvegarder un dossier avec structure (ZIP, copie, incremental).

## Syntaxe

```
/file-backup <source> [destination] [options]
```

## Actions

### Backup ZIP

```powershell
$Source = $args[0]
$Timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$Name = Split-Path $Source -Leaf
$ZipPath = "$env:USERPROFILE\Documents\Backups\${Name}_$Timestamp.zip"

$BackupDir = Split-Path $ZipPath
if (-not (Test-Path $BackupDir)) { New-Item -ItemType Directory -Path $BackupDir -Force }

Compress-Archive -Path "$Source\*" -DestinationPath $ZipPath -CompressionLevel Optimal
Write-Output "Backup: $ZipPath ($([math]::Round((Get-Item $ZipPath).Length / 1MB, 1)) MB)"
```

### Backup copie (robocopy)

```powershell
$Destination = $args[1]
robocopy $Source $Destination /MIR /XD ".git" "__pycache__" "node_modules" /XF "*.tmp" /NFL /NDL /NJH /NJS /NC /NS /NP
Write-Output "Copie miroir: $Source -> $Destination"
```

### Rotation des backups

```powershell
$BackupDir = "$env:USERPROFILE\Documents\Backups"
$KeepCount = 5
Get-ChildItem $BackupDir -Filter "${Name}_*.zip" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -Skip $KeepCount |
    Remove-Item -Force
```

## Options

| Option | Description |
|--------|-------------|
| `--zip` | Archive ZIP (defaut) |
| `--copy` | Copie miroir (robocopy) |
| `--keep N` | Garder N backups (defaut: 5) |

## Exemples

```powershell
/file-backup C:\Users\r2d2\Documents                   # Backup ZIP
/file-backup C:\Projets D:\Backup\Projets --copy        # Copie miroir
/file-backup C:\Data --keep 10                          # Garder 10 versions
```

## Voir Aussi

- `/file-sync` - Synchroniser deux dossiers
- `/file-mirror` - Miroir exact
