# Commande: /obs-links unlinked

Trouver les notes sans aucun lien entrant ou sortant.

## Syntaxe

```
/obs-links unlinked [options]
```

## Actions

### Trouver notes non liees

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" |
    Where-Object { $_.FullName -notmatch '_Templates|\.obsidian' }
$AllLinks = @()

foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if ($Content) {
        $Links = [regex]::Matches($Content, '\[\[([^\]|]+)') |
            ForEach-Object { $_.Groups[1].Value }
        $AllLinks += $Links
    }
}

# Notes sans backlinks (personne ne pointe vers elles)
$NoIncoming = $Notes | Where-Object { $_.BaseName -notin $AllLinks }

# Notes sans liens sortants
$NoOutgoing = $Notes | Where-Object {
    $Content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    $Content -notmatch '\[\['
}

Write-Output "Sans backlinks: $($NoIncoming.Count)"
$NoIncoming | ForEach-Object { "  - $($_.Name)" }
Write-Output "`nSans liens sortants: $($NoOutgoing.Count)"
$NoOutgoing | ForEach-Object { "  - $($_.Name)" }
```

## Options

| Option | Description |
|--------|-------------|
| `--no-incoming` | Notes sans backlinks uniquement |
| `--no-outgoing` | Notes sans liens sortants uniquement |
| `--exclude` | Exclure dossiers (ex: _Daily) |

## Exemples

```powershell
/obs-links unlinked                      # Toutes les notes non liees
/obs-links unlinked --no-incoming        # Sans backlinks
/obs-links unlinked --exclude _Daily     # Exclure les daily notes
```

## Voir Aussi

- `/obs-links suggest` - Suggerer des connexions
- `/obs-orphans` - Notes orphelines
- `/obs-graph` - Analyse du graphe
