# Commande: /obs-links fix

Reparer les liens casses du vault (cibles renommees, supprimees, typos).

## Syntaxe

```
/obs-links fix [options]
```

## Actions

### Detecter et reparer

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
$NoteNames = $Notes | ForEach-Object { $_.BaseName }
$Fixes = @()

foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $Content) { continue }
    $Links = [regex]::Matches($Content, '\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
    foreach ($Link in $Links) {
        $Target = $Link.Groups[1].Value
        if ($Target -notin $NoteNames) {
            # Chercher correspondance approximative
            $BestMatch = $NoteNames | Where-Object {
                $_ -like "*$Target*" -or $Target -like "*$_*"
            } | Select-Object -First 1
            $Fixes += [PSCustomObject]@{
                Source = $Note.Name
                BrokenLink = $Target
                Suggestion = if ($BestMatch) { $BestMatch } else { "(aucune)" }
            }
        }
    }
}

$Fixes | Format-Table -AutoSize
```

### Appliquer les corrections

```powershell
# Mode interactif : proposer chaque fix
foreach ($Fix in $Fixes) {
    if ($Fix.Suggestion -ne "(aucune)") {
        Write-Host "Dans $($Fix.Source): [[$($Fix.BrokenLink)]] -> [[$($Fix.Suggestion)]]"
        # Remplacer dans le fichier apres confirmation
    }
}
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Afficher sans corriger |
| `--auto` | Corriger automatiquement les correspondances exactes |
| `--remove` | Supprimer les liens sans correspondance |
| `--create` | Creer les notes manquantes |

## Exemples

```powershell
/obs-links fix                # Detecter et proposer corrections
/obs-links fix --dry-run      # Preview des corrections
/obs-links fix --auto         # Appliquer les correspondances evidentes
/obs-links fix --create       # Creer les notes manquantes
```

## Voir Aussi

- `/obs-links broken` - Lister les liens casses
- `/obs-links suggest` - Suggerer connexions
- `/obs-health` - Diagnostic complet
