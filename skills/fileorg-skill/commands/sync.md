# Commande: /file-sync

Synchroniser deux dossiers (bidirectionnel).

## Syntaxe

```
/file-sync <source> <destination> [options]
```

## Actions

### Preview des differences

```powershell
$Source = $args[0]
$Dest = $args[1]

$SourceFiles = Get-ChildItem -Path $Source -Recurse -File
$DestFiles = Get-ChildItem -Path $Dest -Recurse -File

$SourceRel = $SourceFiles | ForEach-Object { $_.FullName.Replace($Source, '') }
$DestRel = $DestFiles | ForEach-Object { $_.FullName.Replace($Dest, '') }

$OnlyInSource = $SourceRel | Where-Object { $_ -notin $DestRel }
$OnlyInDest = $DestRel | Where-Object { $_ -notin $SourceRel }

Write-Output "Uniquement dans source: $($OnlyInSource.Count)"
Write-Output "Uniquement dans destination: $($OnlyInDest.Count)"
```

### Synchroniser (source -> destination)

```powershell
robocopy $Source $Dest /E /XO /XD ".git" "node_modules" /NFL /NDL
Write-Output "Synchronise: $Source -> $Dest"
```

### Synchroniser bidirectionnel

```powershell
# Source -> Dest (fichiers nouveaux/modifies)
robocopy $Source $Dest /E /XO /XD ".git" /NFL /NDL /NJH /NJS
# Dest -> Source (fichiers uniquement dans dest)
robocopy $Dest $Source /E /XO /XD ".git" /NFL /NDL /NJH /NJS
```

## Options

| Option | Description |
|--------|-------------|
| `--preview` | Afficher sans synchroniser |
| `--one-way` | Source -> Dest uniquement |
| `--two-way` | Bidirectionnel (defaut) |
| `--exclude` | Patterns a exclure |

## Exemples

```powershell
/file-sync C:\Projets D:\Backup --preview    # Preview
/file-sync C:\Projets D:\Backup --one-way    # Unidirectionnel
/file-sync C:\Data D:\Mirror                  # Bidirectionnel
```

## Voir Aussi

- `/file-mirror` - Miroir exact
- `/file-backup` - Sauvegarde
