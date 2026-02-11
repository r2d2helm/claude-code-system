# Commande: /obs-structure

Analyser la structure des dossiers du vault Obsidian.

## Syntaxe

```
/obs-structure [options]
```

## Actions

### Analyse de la structure

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"

# Stats par dossier
$Folders = Get-ChildItem -Path $VaultPath -Directory -Recurse |
    Where-Object { $_.FullName -notmatch '\.obsidian|\.git' }

foreach ($Folder in $Folders) {
    $Files = Get-ChildItem -Path $Folder.FullName -Filter "*.md" -File
    $RelPath = $Folder.FullName.Replace($VaultPath, '').TrimStart('\')
    $Depth = ($RelPath -split '\\').Count
    [PSCustomObject]@{
        Dossier = $RelPath
        Notes = $Files.Count
        Profondeur = $Depth
    }
} | Sort-Object Notes -Descending | Format-Table -AutoSize

# Profondeur maximale
$MaxDepth = ($Folders | ForEach-Object {
    ($_.FullName.Replace($VaultPath, '').TrimStart('\') -split '\\').Count
} | Measure-Object -Maximum).Maximum

Write-Output "`nProfondeur max: $MaxDepth niveaux"
Write-Output "Total dossiers: $($Folders.Count)"

# Alertes
$Deep = $Folders | Where-Object {
    ($_.FullName.Replace($VaultPath, '').TrimStart('\') -split '\\').Count -gt 3
}
if ($Deep.Count -gt 0) {
    Write-Warning "$($Deep.Count) dossiers avec profondeur > 3"
}
```

## Options

| Option | Description |
|--------|-------------|
| `--tree` | Affichage en arbre ASCII |
| `--depth N` | Limiter a N niveaux |
| `--empty` | Montrer les dossiers vides |

## Exemples

```powershell
/obs-structure                # Analyse complete
/obs-structure --tree         # Vue en arbre
/obs-structure --empty        # Dossiers vides
```

## Voir Aussi

- `/obs-health` - Diagnostic complet
- `/obs-stats` - Statistiques generales
