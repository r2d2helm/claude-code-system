# Commande: /obs-links suggest

Suggerer des connexions entre notes basees sur les tags et mots-cles communs.

## Syntaxe

```
/obs-links suggest [note] [options]
```

## Actions

### Suggerer des liens pour une note

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$TargetNote = $args[0]  # Nom de la note cible

# Lire la note cible
$Target = Get-ChildItem -Path $VaultPath -Recurse -Filter "$TargetNote.md" | Select-Object -First 1
$TargetContent = Get-Content $Target.FullName -Raw

# Extraire tags de la cible
$TargetTags = [regex]::Matches($TargetContent, '#[\w/-]+') | ForEach-Object { $_.Value }

# Chercher notes avec tags communs
$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" |
    Where-Object { $_.FullName -ne $Target.FullName }

$Suggestions = foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if ($Content) {
        $NoteTags = [regex]::Matches($Content, '#[\w/-]+') | ForEach-Object { $_.Value }
        $Common = $TargetTags | Where-Object { $_ -in $NoteTags }
        if ($Common.Count -gt 0) {
            [PSCustomObject]@{
                Note = $Note.BaseName
                CommonTags = $Common.Count
                Tags = ($Common -join ', ')
            }
        }
    }
}

$Suggestions | Sort-Object CommonTags -Descending | Select-Object -First 10
```

### Suggerer pour tout le vault

```powershell
# Trouver les paires de notes les plus similaires (par tags)
# sans lien existant entre elles
```

## Options

| Option | Description |
|--------|-------------|
| `--by-tags` | Similarite par tags (defaut) |
| `--by-title` | Similarite par mots du titre |
| `--limit N` | Limiter a N suggestions |

## Exemples

```powershell
/obs-links suggest C_Docker          # Suggestions pour la note C_Docker
/obs-links suggest --by-tags         # Suggestions pour tout le vault
```

## Voir Aussi

- `/obs-links unlinked` - Notes non liees
- `/obs-links fix` - Reparer liens casses
- `/obs-graph` - Analyse du graphe
