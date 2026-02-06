# Commande: /file-archive

Archiver les fichiers anciens dans une structure par année.

## Syntaxe

```
/file-archive [chemin] [options]
```

## Comportement

Déplace les fichiers plus anciens qu'un seuil donné vers un dossier `_ARCHIVE/YYYY/` organisé par année de dernière modification.

## Script PowerShell

```powershell
param(
    [string]$Path = ".",
    [int]$OlderThanMonths = 12,
    [string]$ArchiveDir = "_ARCHIVE",
    [switch]$DryRun
)

$CutoffDate = (Get-Date).AddMonths(-$OlderThanMonths)
$Files = Get-ChildItem -Path $Path -File -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -lt $CutoffDate -and $_.FullName -notmatch '_ARCHIVE' }

$ArchivePath = Join-Path $Path $ArchiveDir
$Moved = 0
$TotalSize = 0

Write-Host ""
Write-Host "╔══════════════════════════════════════════════╗"
Write-Host "║     📦 ARCHIVAGE DE FICHIERS                  ║"
Write-Host "╠══════════════════════════════════════════════╣"
Write-Host "║                                              ║"
Write-Host "║  Source:   $Path"
Write-Host "║  Seuil:    > $OlderThanMonths mois ($($CutoffDate.ToString('yyyy-MM-dd')))"
Write-Host "║  Fichiers: $($Files.Count) à archiver"
Write-Host "║                                              ║"

if ($Files.Count -eq 0) {
    Write-Host "║  ✅ Aucun fichier à archiver                 ║"
    Write-Host "╚══════════════════════════════════════════════╝"
    return
}

foreach ($File in $Files) {
    $Year = $File.LastWriteTime.ToString("yyyy")
    $YearDir = Join-Path $ArchivePath $Year

    if ($DryRun) {
        Write-Host "[DRY RUN] $($File.Name) -> $ArchiveDir\$Year\"
    } else {
        if (-not (Test-Path $YearDir)) {
            New-Item -Path $YearDir -ItemType Directory -Force | Out-Null
        }
        $dest = Join-Path $YearDir $File.Name
        if (Test-Path $dest) {
            $dest = Join-Path $YearDir "$($File.BaseName)_$(Get-Date -Format 'HHmmss')$($File.Extension)"
        }
        Move-Item -Path $File.FullName -Destination $dest
    }
    $Moved++
    $TotalSize += $File.Length
}

Write-Host "║  $(if ($DryRun) { 'Simulé' } else { 'Archivé' }): $Moved fichiers ($('{0:N1} MB' -f ($TotalSize / 1MB)))"
Write-Host "║                                              ║"
Write-Host "╚══════════════════════════════════════════════╝"
```

## Options

| Option | Description |
|--------|-------------|
| `--older-than=N` | Mois d'ancienneté (défaut: 12) |
| `--dest=path` | Dossier d'archive personnalisé |
| `--dry-run` | Simuler sans déplacer |

## Exemples

```powershell
# Archiver les fichiers > 1 an
/file-archive Documents

# Archiver les fichiers > 6 mois (dry run)
/file-archive Downloads --older-than=6 --dry-run

# Archive personnalisée
/file-archive Documents --dest="D:\Archives"
```
