# Commande: /obs-backup

Sauvegarder le vault Obsidian.

## Syntaxe

```
/obs-backup [options]
```

## Comportement

Crée une archive ZIP du vault avec rotation automatique des sauvegardes.

## Script PowerShell

```powershell
param(
    [string]$VaultPath = "$env:USERPROFILE\Documents\Knowledge",
    [string]$BackupDir = "$env:USERPROFILE\Documents\Backups\Knowledge",
    [int]$KeepDays = 7,
    [switch]$ExcludeObsidian
)

$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$archiveName = "Knowledge_$timestamp.zip"

# Créer le dossier backup si nécessaire
if (-not (Test-Path $BackupDir)) {
    New-Item -Path $BackupDir -ItemType Directory -Force | Out-Null
}

$archivePath = Join-Path $BackupDir $archiveName

Write-Host ""
Write-Host "╔══════════════════════════════════════════════╗"
Write-Host "║     💾 BACKUP DU VAULT                        ║"
Write-Host "╠══════════════════════════════════════════════╣"
Write-Host "║                                              ║"
Write-Host "║  Source:  $VaultPath"
Write-Host "║  Dest:    $archivePath"
Write-Host "║                                              ║"

# Compter les fichiers
$files = Get-ChildItem -Path $VaultPath -Recurse -File
if ($ExcludeObsidian) {
    $files = $files | Where-Object { $_.FullName -notmatch '\.obsidian' }
}
$totalSize = ($files | Measure-Object -Property Length -Sum).Sum

Write-Host "║  Fichiers: $($files.Count)"
Write-Host "║  Taille:   $('{0:N1} MB' -f ($totalSize / 1MB))"
Write-Host "║                                              ║"

# Créer l'archive
Write-Host "║  ⏳ Compression en cours...                   ║"

if ($ExcludeObsidian) {
    # Exclure .obsidian
    $tempList = $files.FullName
    Compress-Archive -Path $tempList -DestinationPath $archivePath -CompressionLevel Optimal
} else {
    Compress-Archive -Path "$VaultPath\*" -DestinationPath $archivePath -CompressionLevel Optimal
}

$archiveSize = (Get-Item $archivePath).Length

Write-Host "║  ✅ Archive créée: $('{0:N1} MB' -f ($archiveSize / 1MB))"
Write-Host "║                                              ║"

# Rotation: supprimer les anciennes sauvegardes
$oldBackups = Get-ChildItem -Path $BackupDir -Filter "Knowledge_*.zip" |
    Sort-Object CreationTime -Descending |
    Select-Object -Skip $KeepDays

if ($oldBackups.Count -gt 0) {
    foreach ($old in $oldBackups) {
        Remove-Item $old.FullName -Force
    }
    Write-Host "║  🔄 Rotation: $($oldBackups.Count) anciens backups supprimés"
} else {
    Write-Host "║  🔄 Rotation: rien à supprimer"
}

# Lister les backups existants
$allBackups = Get-ChildItem -Path $BackupDir -Filter "Knowledge_*.zip" | Sort-Object CreationTime -Descending
Write-Host "║                                              ║"
Write-Host "║  📦 Backups disponibles: $($allBackups.Count)"
foreach ($b in $allBackups | Select-Object -First 5) {
    Write-Host "║    - $($b.Name) ($('{0:N1} MB' -f ($b.Length / 1MB)))"
}

Write-Host "║                                              ║"
Write-Host "╚══════════════════════════════════════════════╝"
```

## Options

| Option | Description |
|--------|-------------|
| `--dest=path` | Destination personnalisée |
| `--keep=N` | Nombre de backups à garder (défaut: 7) |
| `--exclude-obsidian` | Exclure le dossier .obsidian |
| `--incremental` | Backup incrémental (fichiers modifiés uniquement) |

## Exemples

```powershell
# Backup standard
/obs-backup

# Backup vers un autre disque
/obs-backup --dest="D:\Backups\Knowledge"

# Garder 14 jours
/obs-backup --keep=14

# Sans config Obsidian
/obs-backup --exclude-obsidian
```
