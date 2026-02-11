# Commande: /file-wizard

Assistant interactif pour organiser un dossier etape par etape.

## Syntaxe

```
/file-wizard <chemin> [options]
```

## Actions

### Etape 1 : Analyse du dossier

```powershell
$Path = $args[0]
$Files = Get-ChildItem -Path $Path -File
$Dirs = Get-ChildItem -Path $Path -Directory

$Extensions = $Files | Group-Object Extension | Sort-Object Count -Descending
$TotalSize = ($Files | Measure-Object -Property Length -Sum).Sum

Write-Output "=== ANALYSE: $Path ==="
Write-Output "Fichiers: $($Files.Count)"
Write-Output "Dossiers: $($Dirs.Count)"
Write-Output "Taille totale: $([math]::Round($TotalSize / 1MB, 1)) MB"
Write-Output ""
Write-Output "Extensions:"
$Extensions | ForEach-Object {
    "  $($_.Name): $($_.Count) fichiers"
}
```

### Etape 2 : Detection des problemes

```powershell
$Issues = @()

# Fichiers sans extension
$NoExt = $Files | Where-Object { -not $_.Extension }
if ($NoExt.Count -gt 0) { $Issues += "  - $($NoExt.Count) fichiers sans extension" }

# Noms avec espaces ou caracteres speciaux
$BadNames = $Files | Where-Object { $_.BaseName -match '[àâäéèêëîïôöùûüç\s@#$%&]' }
if ($BadNames.Count -gt 0) { $Issues += "  - $($BadNames.Count) noms avec caracteres speciaux/espaces" }

# Fichiers volumineux (>100MB)
$Large = $Files | Where-Object { $_.Length -gt 100MB }
if ($Large.Count -gt 0) { $Issues += "  - $($Large.Count) fichiers > 100 MB" }

# Doublons potentiels (meme taille + meme extension)
$PossibleDupes = $Files | Group-Object { "$($_.Length)-$($_.Extension)" } | Where-Object { $_.Count -gt 1 }
if ($PossibleDupes.Count -gt 0) { $Issues += "  - $($PossibleDupes.Count) groupes de doublons potentiels" }

# Fichiers anciens (>1 an)
$OldFiles = $Files | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-365) }
if ($OldFiles.Count -gt 0) { $Issues += "  - $($OldFiles.Count) fichiers non modifies depuis >1 an" }

if ($Issues.Count -eq 0) {
    Write-Output "Aucun probleme detecte!"
} else {
    Write-Output "Problemes detectes:"
    $Issues | ForEach-Object { Write-Output $_ }
}
```

### Etape 3 : Proposition d'organisation

```powershell
Write-Output "=== PLAN D'ORGANISATION ==="
Write-Output ""
Write-Output "Actions proposees:"
Write-Output "  1. Trier par type (extension) dans des sous-dossiers"
Write-Output "  2. Normaliser les noms (accents, espaces)"
Write-Output "  3. Archiver les fichiers anciens (>1 an)"
Write-Output "  4. Detecter et traiter les doublons"
Write-Output "  5. Nettoyer les fichiers temporaires"
Write-Output ""
Write-Output "Commandes correspondantes:"
Write-Output "  /file-sort $Path"
Write-Output "  /file-normalize $Path"
Write-Output "  /file-old $Path --archive"
Write-Output "  /file-duplicates $Path"
Write-Output "  /file-clean $Path"
```

### Etape 4 : Execution guidee

```powershell
# Creer un backup avant modification
$Timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$BackupDir = "$env:USERPROFILE\Documents\Backups\wizard_${Timestamp}"
Write-Output "Backup de securite: $BackupDir"

robocopy $Path $BackupDir /MIR /NFL /NDL /NJH /NJS /NP | Out-Null

Write-Output "Backup cree. Pret pour l'organisation."
Write-Output "Executer les commandes une par une avec confirmation."
```

## Options

| Option | Description |
|--------|-------------|
| `--auto` | Executer toutes les etapes automatiquement |
| `--step` | Mode pas-a-pas avec confirmation (defaut) |
| `--backup` | Creer un backup avant modification |
| `--dry-run` | Preview sans modification |

## Exemples

```powershell
/file-wizard C:\Users\r2d2\Downloads                   # Wizard complet
/file-wizard C:\Users\r2d2\Documents --dry-run          # Preview seulement
/file-wizard D:\Data --auto                             # Mode automatique
```

## Voir Aussi

- `/file-analyze` - Analyse detaillee
- `/file-organize` - Organisation par type
- `/file-audit` - Audit qualite
