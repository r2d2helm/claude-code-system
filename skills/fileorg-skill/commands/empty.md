# Commande: /file-empty

Trouver et supprimer les dossiers vides.

## Syntaxe

```
/file-empty [chemin] [action]
```

## Actions

### /file-empty [chemin]

Lister les dossiers vides :

```powershell
param(
    [string]$Path = ".",
    [switch]$Delete,
    [switch]$DryRun
)

$AllFolders = Get-ChildItem -Path $Path -Directory -Recurse -ErrorAction SilentlyContinue
$EmptyFolders = @()

# Trouver les dossiers vides (y compris ceux avec seulement des sous-dossiers vides)
# Parcourir de la profondeur la plus grande vers la racine
$sorted = $AllFolders | Sort-Object { $_.FullName.Length } -Descending

foreach ($folder in $sorted) {
    $items = Get-ChildItem $folder.FullName -Force -ErrorAction SilentlyContinue
    $hasFiles = $items | Where-Object { -not $_.PSIsContainer }
    $hasNonEmptyDirs = $items | Where-Object { $_.PSIsContainer -and $_.FullName -notin ($EmptyFolders | ForEach-Object { $_.FullName }) }

    if (-not $hasFiles -and -not $hasNonEmptyDirs) {
        $EmptyFolders += $folder
    }
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════╗"
Write-Host "║     📂 DOSSIERS VIDES                         ║"
Write-Host "╠══════════════════════════════════════════════╣"
Write-Host "║                                              ║"
Write-Host "║  Trouvés: $($EmptyFolders.Count) dossiers vides"
Write-Host "║                                              ║"

if ($EmptyFolders.Count -gt 0) {
    foreach ($ef in $EmptyFolders | Select-Object -First 20) {
        $rel = $ef.FullName.Replace((Resolve-Path $Path).Path, "").TrimStart("\")
        if ($Delete -and -not $DryRun) {
            Remove-Item $ef.FullName -Force -Recurse
            Write-Host "║  🗑️ Supprimé: $rel"
        } elseif ($DryRun) {
            Write-Host "║  [DRY RUN] $rel"
        } else {
            Write-Host "║  📂 $rel"
        }
    }
    if ($EmptyFolders.Count -gt 20) {
        Write-Host "║  ... et $($EmptyFolders.Count - 20) de plus"
    }
}

Write-Host "║                                              ║"
if (-not $Delete) {
    Write-Host "║  → Utiliser /file-empty delete pour supprimer║"
}
Write-Host "╚══════════════════════════════════════════════╝"
```

## Options

| Option | Description |
|--------|-------------|
| `delete` | Supprimer les dossiers vides |
| `--dry-run` | Simuler la suppression |
| `--include-hidden` | Inclure dossiers cachés |

## Exemples

```powershell
# Lister les dossiers vides
/file-empty Documents

# Supprimer les dossiers vides (dry run)
/file-empty Documents delete --dry-run

# Supprimer pour de vrai
/file-empty Documents delete
```
