# Commande: /file-prefix

Ajouter un prefixe date ISO 8601 aux fichiers.

## Syntaxe

```
/file-prefix <chemin> [action] [options]
```

## Actions

### Ajouter le prefixe date

```powershell
$Path = $args[0]
$Files = Get-ChildItem -Path $Path -File | Where-Object { $_.Name -notmatch '^\d{4}-\d{2}-\d{2}' }

foreach ($File in $Files) {
    $Date = $File.LastWriteTime.ToString('yyyy-MM-dd')
    $NewName = "${Date}_$($File.Name)"
    Rename-Item -Path $File.FullName -NewName $NewName
    Write-Output "  $($File.Name) -> $NewName"
}
Write-Output "$($Files.Count) fichiers prefixes"
```

### Retirer le prefixe

```powershell
$Files = Get-ChildItem -Path $Path -File | Where-Object { $_.Name -match '^\d{4}-\d{2}-\d{2}_' }

foreach ($File in $Files) {
    $NewName = $File.Name -replace '^\d{4}-\d{2}-\d{2}_', ''
    Rename-Item -Path $File.FullName -NewName $NewName
}
```

### Mettre a jour le prefixe

```powershell
# Remplacer le prefixe existant par la date de modification actuelle
$Files = Get-ChildItem -Path $Path -File | Where-Object { $_.Name -match '^\d{4}-\d{2}-\d{2}_' }
foreach ($File in $Files) {
    $Date = $File.LastWriteTime.ToString('yyyy-MM-dd')
    $NewName = $File.Name -replace '^\d{4}-\d{2}-\d{2}', $Date
    if ($NewName -ne $File.Name) { Rename-Item -Path $File.FullName -NewName $NewName }
}
```

## Options

| Option | Description |
|--------|-------------|
| `add` | Ajouter prefixe (defaut) |
| `remove` | Retirer le prefixe |
| `update` | Mettre a jour avec date actuelle |
| `--dry-run` | Preview |

## Exemples

```powershell
/file-prefix C:\Users\r2d2\Documents add       # Ajouter prefixes
/file-prefix C:\Users\r2d2\Documents remove     # Retirer prefixes
/file-prefix C:\Users\r2d2\Downloads --dry-run  # Preview
```

## Voir Aussi

- `/file-rename` - Renommer selon convention
- `/file-normalize` - Normaliser les noms
