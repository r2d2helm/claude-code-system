# Commande: /file-flatten

Aplatir une arborescence trop profonde (>3 niveaux).

## Syntaxe

```
/file-flatten <chemin> [options]
```

## Actions

### Preview (dry-run)

```powershell
$Path = $args[0]
$MaxDepth = 3

$DeepFiles = Get-ChildItem -Path $Path -Recurse -File | Where-Object {
    $RelPath = $_.FullName.Replace($Path, '').TrimStart('\')
    ($RelPath -split '\\').Count -gt $MaxDepth
}

Write-Output "Fichiers a profondeur > $MaxDepth : $($DeepFiles.Count)"
$DeepFiles | ForEach-Object {
    $RelPath = $_.FullName.Replace($Path, '').TrimStart('\')
    Write-Output "  $RelPath"
}
```

### Executer l'aplatissement

```powershell
$DeepFiles | ForEach-Object {
    $RelPath = $_.FullName.Replace($Path, '').TrimStart('\')
    $Parts = $RelPath -split '\\'
    # Garder les 2 premiers niveaux + nom du fichier
    $NewPath = Join-Path $Path ($Parts[0..1] -join '\')
    if (-not (Test-Path $NewPath)) { New-Item -ItemType Directory -Path $NewPath -Force | Out-Null }
    Move-Item -Path $_.FullName -Destination (Join-Path $NewPath $_.Name)
    Write-Output "Deplace: $RelPath -> $($Parts[0..1] -join '\')\"
}

# Supprimer les dossiers vides
Get-ChildItem -Path $Path -Recurse -Directory |
    Where-Object { (Get-ChildItem $_.FullName).Count -eq 0 } |
    Remove-Item -Force
```

## Options

| Option | Description |
|--------|-------------|
| `--max-depth N` | Profondeur max (defaut: 3) |
| `--dry-run` | Preview sans deplacer |

## Exemples

```powershell
/file-flatten C:\Users\r2d2\Documents --dry-run       # Preview
/file-flatten C:\Users\r2d2\Documents --max-depth 2    # Aplatir a 2 niveaux
```

## Voir Aussi

- `/file-structure` - Creer une structure
- `/file-sort` - Trier des fichiers
