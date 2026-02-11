# Commande: /file-sort

Trier fichiers dans des sous-dossiers par type, date ou taille.

## Syntaxe

```
/file-sort <chemin> [mode] [options]
```

## Actions

### Trier par extension

```powershell
$Path = $args[0]
$Files = Get-ChildItem -Path $Path -File

$Files | Group-Object Extension | ForEach-Object {
    $Folder = Join-Path $Path ($_.Name.TrimStart('.').ToUpper())
    if (-not (Test-Path $Folder)) { New-Item -ItemType Directory -Path $Folder -Force | Out-Null }
    $_.Group | Move-Item -Destination $Folder
    Write-Output "  $($_.Name): $($_.Count) fichiers -> $($_.Name.TrimStart('.').ToUpper())/"
}
```

### Trier par date

```powershell
$Files | ForEach-Object {
    $DateFolder = $_.LastWriteTime.ToString('yyyy-MM')
    $Dest = Join-Path $Path $DateFolder
    if (-not (Test-Path $Dest)) { New-Item -ItemType Directory -Path $Dest -Force | Out-Null }
    Move-Item -Path $_.FullName -Destination $Dest
}
```

### Trier par taille

```powershell
$Files | ForEach-Object {
    $Size = switch ($_.Length) {
        { $_ -lt 1MB } { "Petit_<1MB" }
        { $_ -lt 100MB } { "Moyen_1-100MB" }
        default { "Gros_>100MB" }
    }
    $Dest = Join-Path $Path $Size
    if (-not (Test-Path $Dest)) { New-Item -ItemType Directory -Path $Dest -Force | Out-Null }
    Move-Item -Path $_.FullName -Destination $Dest
}
```

## Options

| Option | Description |
|--------|-------------|
| `by-type` | Par extension (defaut) |
| `by-date` | Par mois (YYYY-MM) |
| `by-size` | Par taille (petit/moyen/gros) |
| `--dry-run` | Preview sans deplacer |

## Exemples

```powershell
/file-sort C:\Users\r2d2\Downloads by-type        # Par extension
/file-sort C:\Users\r2d2\Downloads by-date        # Par mois
/file-sort C:\Users\r2d2\Desktop by-size --dry-run # Preview
```

## Voir Aussi

- `/file-organize` - Organisation avancee
- `/file-flatten` - Aplatir arborescence
