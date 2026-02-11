# Commande: /obs-empty

Trouver et supprimer les notes vides ou quasi-vides.

## Syntaxe

```
/obs-empty [options]
```

## Actions

### Trouver les notes vides

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" |
    Where-Object { $_.FullName -notmatch '_Templates|\.obsidian' }

$Empty = foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $Content) {
        [PSCustomObject]@{ Note = $Note.Name; Type = "Vide"; Taille = 0 }
        continue
    }
    # Retirer le frontmatter pour mesurer le contenu reel
    $Body = $Content -replace '(?s)^---\s*\n.*?\n---\s*\n?', ''
    $Body = $Body.Trim()
    if ($Body.Length -eq 0) {
        [PSCustomObject]@{ Note = $Note.Name; Type = "Frontmatter seul"; Taille = $Content.Length }
    } elseif ($Body.Length -lt 50) {
        [PSCustomObject]@{ Note = $Note.Name; Type = "Quasi-vide"; Taille = $Body.Length }
    }
}

Write-Output "Notes vides/quasi-vides: $($Empty.Count)"
$Empty | Format-Table -AutoSize
```

## Options

| Option | Description |
|--------|-------------|
| `--delete` | Supprimer les notes vides (avec confirmation) |
| `--min-chars N` | Seuil de contenu minimum (defaut: 50) |
| `--dry-run` | Preview sans action |

## Exemples

```powershell
/obs-empty                    # Lister les notes vides
/obs-empty --min-chars 100    # Seuil plus large
/obs-empty --delete           # Supprimer apres confirmation
```

## Voir Aussi

- `/obs-clean` - Nettoyage general
- `/obs-duplicates` - Notes en double
