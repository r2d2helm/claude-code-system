# Commande: /file-audit

Audit qualite du nommage et de l'organisation d'un dossier.

## Syntaxe

```
/file-audit <chemin> [options]
```

## Actions

### Audit rapide (score)

```powershell
$Path = $args[0]
$Files = Get-ChildItem -Path $Path -File
$Score = 100
$Issues = @()

# Nommage ISO (25 pts)
$NoDate = $Files | Where-Object { $_.Name -notmatch '^\d{4}-\d{2}-\d{2}' }
if ($NoDate.Count -gt $Files.Count * 0.5) { $Score -= 25; $Issues += "Plus de 50% sans date ISO" }

# Caracteres speciaux (10 pts)
$BadChars = $Files | Where-Object { $_.BaseName -match '[àâäéèêëîïôöùûüç\s@#$%&]' }
if ($BadChars.Count -gt 0) { $Score -= 10; $Issues += "$($BadChars.Count) fichiers avec caracteres speciaux" }

# Doublons potentiels (15 pts)
$Dupes = $Files | Group-Object { (Get-FileHash $_.FullName -Algorithm MD5).Hash } |
    Where-Object { $_.Count -gt 1 }
if ($Dupes.Count -gt 0) { $Score -= 15; $Issues += "$($Dupes.Count) groupes de doublons" }

# Profondeur (20 pts)
$MaxDepth = (Get-ChildItem -Path $Path -Recurse -Directory | ForEach-Object {
    ($_.FullName.Replace($Path, '') -split '\\').Count
} | Measure-Object -Maximum).Maximum
if ($MaxDepth -gt 4) { $Score -= 20; $Issues += "Profondeur > 4 niveaux ($MaxDepth)" }

# Dossiers vides (10 pts)
$EmptyDirs = Get-ChildItem -Path $Path -Recurse -Directory |
    Where-Object { (Get-ChildItem $_.FullName).Count -eq 0 }
if ($EmptyDirs.Count -gt 0) { $Score -= 10; $Issues += "$($EmptyDirs.Count) dossiers vides" }

Write-Output "SCORE: $Score/100"
Write-Output "Issues:"
$Issues | ForEach-Object { "  - $_" }
```

## Options

| Option | Description |
|--------|-------------|
| `--quick` | Score uniquement |
| `--full` | Rapport detaille |
| `--fix` | Proposer des corrections |

## Exemples

```powershell
/file-audit C:\Users\r2d2\Downloads              # Audit rapide
/file-audit C:\Users\r2d2\Documents --full        # Rapport complet
/file-audit C:\Users\r2d2\Desktop --fix           # Audit + corrections
```

## Voir Aussi

- `/file-normalize` - Normaliser les noms
- `/file-clean` - Nettoyer
- `/file-organize` - Organiser
