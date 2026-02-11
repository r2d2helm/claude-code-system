# Commande: /file-old

Trouver les fichiers anciens ou obsoletes.

## Syntaxe

```
/file-old <chemin> [options]
```

## Actions

### Lister les fichiers anciens

```powershell
$Path = $args[0]
$Days = 365  # Par defaut, fichiers > 1 an

$OldFiles = Get-ChildItem -Path $Path -Recurse -File |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$Days) } |
    Sort-Object LastWriteTime

Write-Output "Fichiers non modifies depuis $Days jours: $($OldFiles.Count)"
$TotalSize = ($OldFiles | Measure-Object -Property Length -Sum).Sum / 1MB

$OldFiles | Select-Object -First 20 | ForEach-Object {
    $Age = ((Get-Date) - $_.LastWriteTime).Days
    "  [$Age j] $($_.Name) ($([math]::Round($_.Length / 1KB, 1)) KB)"
}

Write-Output "`nTaille totale: $([math]::Round($TotalSize, 1)) MB"
```

### Archiver les anciens fichiers

```powershell
$ArchivePath = Join-Path $Path "_ARCHIVE\$(Get-Date -Format 'yyyy')"
if (-not (Test-Path $ArchivePath)) { New-Item -ItemType Directory -Path $ArchivePath -Force }

$OldFiles | Move-Item -Destination $ArchivePath
Write-Output "Archives: $($OldFiles.Count) fichiers -> $ArchivePath"
```

## Options

| Option | Description |
|--------|-------------|
| `--days N` | Age minimum en jours (defaut: 365) |
| `--archive` | Deplacer vers _ARCHIVE/ |
| `--delete` | Supprimer (avec confirmation) |
| `--dry-run` | Preview sans action |

## Exemples

```powershell
/file-old C:\Users\r2d2\Documents                  # >1 an
/file-old C:\Users\r2d2\Downloads --days 90         # >3 mois
/file-old C:\Users\r2d2\Documents --archive         # Archiver
```

## Voir Aussi

- `/file-archive` - Archiver fichiers
- `/file-clean` - Nettoyer
