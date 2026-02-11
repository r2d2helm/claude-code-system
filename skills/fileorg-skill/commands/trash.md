# Commande: /file-trash

Gerer la corbeille Windows.

## Syntaxe

```
/file-trash [action] [options]
```

## Actions

### Taille de la corbeille

```powershell
$Shell = New-Object -ComObject Shell.Application
$RecycleBin = $Shell.NameSpace(0xA)
$Items = $RecycleBin.Items()

$TotalSize = 0
foreach ($Item in $Items) {
    $TotalSize += $RecycleBin.GetDetailsOf($Item, 3) -replace '[^\d]', ''
}

Write-Output "Corbeille: $($Items.Count) elements"
Write-Output "Taille: $([math]::Round($TotalSize / 1MB, 1)) MB"
```

### Lister le contenu

```powershell
$Items | ForEach-Object {
    [PSCustomObject]@{
        Nom = $RecycleBin.GetDetailsOf($_, 0)
        Origine = $RecycleBin.GetDetailsOf($_, 1)
        Date = $RecycleBin.GetDetailsOf($_, 2)
        Taille = $RecycleBin.GetDetailsOf($_, 3)
    }
} | Format-Table -AutoSize
```

### Vider la corbeille

```powershell
Clear-RecycleBin -Force -ErrorAction SilentlyContinue
Write-Output "Corbeille videe"
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister le contenu |
| `size` | Taille de la corbeille |
| `empty` | Vider la corbeille |
| `restore` | Restaurer un element |

## Exemples

```powershell
/file-trash size           # Taille
/file-trash list           # Contenu
/file-trash empty          # Vider
```

## Voir Aussi

- `/file-clean` - Nettoyer fichiers temporaires
- `/file-old` - Fichiers anciens
