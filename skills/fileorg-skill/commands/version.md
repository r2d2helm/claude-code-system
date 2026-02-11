# Commande: /file-version

Gerer les versions de fichiers (v01, v02...).

## Syntaxe

```
/file-version <chemin> [action] [options]
```

## Actions

### Lister les versions

```powershell
$Path = $args[0]
$Files = Get-ChildItem -Path $Path -File | Where-Object { $_.BaseName -match '_v(\d+)' }

$Files | Group-Object { $_.BaseName -replace '_v\d+.*$', '' } | ForEach-Object {
    Write-Output "$($_.Name):"
    $_.Group | Sort-Object { [int]($_.BaseName | Select-String -Pattern 'v(\d+)').Matches[0].Groups[1].Value } |
        ForEach-Object { "  $($_.Name) ($($_.LastWriteTime.ToString('yyyy-MM-dd')))" }
}
```

### Incrementer la version

```powershell
$File = Get-Item $args[0]
if ($File.BaseName -match '_v(\d+)') {
    $CurrentVersion = [int]$Matches[1]
    $NextVersion = $CurrentVersion + 1
    $NewName = $File.BaseName -replace "_v$CurrentVersion", "_v$($NextVersion.ToString('D2'))"
    Copy-Item -Path $File.FullName -Destination (Join-Path $File.DirectoryName "$NewName$($File.Extension)")
    Write-Output "Nouvelle version: $NewName$($File.Extension)"
} else {
    $NewName = "$($File.BaseName)_v02$($File.Extension)"
    Rename-Item -Path $File.FullName -NewName "$($File.BaseName)_v01$($File.Extension)"
    Copy-Item -Path (Join-Path $File.DirectoryName "$($File.BaseName)_v01$($File.Extension)") `
              -Destination (Join-Path $File.DirectoryName $NewName)
    Write-Output "Versionne: v01 (original) + v02 (copie)"
}
```

### Nettoyer les anciennes versions

```powershell
$Files | Group-Object { $_.BaseName -replace '_v\d+.*$', '' } | ForEach-Object {
    $Sorted = $_.Group | Sort-Object { [int]($_.BaseName | Select-String -Pattern 'v(\d+)').Matches[0].Groups[1].Value } -Descending
    $ToDelete = $Sorted | Select-Object -Skip 2  # Garder les 2 dernieres
    $ToDelete | ForEach-Object { Write-Output "Supprimer: $($_.Name)" }
}
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister les fichiers versionnes |
| `bump` | Incrementer la version |
| `clean` | Supprimer anciennes versions |
| `--keep N` | Garder N versions (defaut: 2) |

## Exemples

```powershell
/file-version C:\Users\r2d2\Documents list      # Lister les versions
/file-version rapport.docx bump                  # v01 -> v02
/file-version C:\Users\r2d2\Documents clean      # Nettoyer
```

## Voir Aussi

- `/file-rename` - Renommer fichiers
- `/file-archive` - Archiver anciens fichiers
