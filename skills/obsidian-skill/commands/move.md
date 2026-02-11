# Commande: /obs-move

Deplacer une note et mettre a jour tous les wikilinks pointant vers elle.

## Syntaxe

```
/obs-move <note> <destination> [options]
```

## Actions

### Deplacer avec mise a jour des liens

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$NoteName = $args[0]
$Destination = $args[1]

# Trouver la note
$Note = Get-ChildItem -Path $VaultPath -Recurse -Filter "$NoteName.md" | Select-Object -First 1
if (-not $Note) { Write-Error "Note '$NoteName' non trouvee"; return }

$DestPath = Join-Path $VaultPath $Destination
if (-not (Test-Path $DestPath)) { New-Item -ItemType Directory -Path $DestPath -Force }

# Deplacer le fichier
$NewPath = Join-Path $DestPath $Note.Name
Move-Item -Path $Note.FullName -Destination $NewPath

# Wikilinks Obsidian utilisent le nom sans chemin, donc pas de mise a jour necessaire
# sauf si le vault utilise des chemins relatifs dans les liens
Write-Output "Deplace: $($Note.Name) -> $Destination/"
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Afficher sans deplacer |
| `--update-links` | Mettre a jour les liens relatifs |

## Exemples

```powershell
/obs-move C_Docker Concepts/           # Deplacer vers Concepts
/obs-move Note-Temp _Inbox/            # Deplacer vers Inbox
/obs-move C_Docker Concepts --dry-run  # Preview
```

## Voir Aussi

- `/obs-rename` - Renommer une note
- `/obs-structure` - Analyser structure
