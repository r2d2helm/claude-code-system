# Commande: /obs-tags hierarchy

Afficher l'arbre hierarchique des tags du vault.

## Syntaxe

```
/obs-tags hierarchy [options]
```

## Actions

### Afficher l'arbre

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
$Tags = @{}

foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if ($Content) {
        [regex]::Matches($Content, '(?<=\s|^)#([\w/-]+)') | ForEach-Object {
            $Tag = $_.Groups[1].Value
            if (-not $Tags.ContainsKey($Tag)) { $Tags[$Tag] = 0 }
            $Tags[$Tag]++
        }
    }
}

# Construire et afficher l'arbre
$Tree = @{}
foreach ($Tag in $Tags.Keys | Sort-Object) {
    $Parts = $Tag -split '/'
    $Current = $Tree
    foreach ($Part in $Parts) {
        if (-not $Current.ContainsKey($Part)) { $Current[$Part] = @{} }
        $Current = $Current[$Part]
    }
}

# Affichage ASCII
# dev/
#   powershell (5)
#   python (3)
#   claude-code (8)
# ai/
#   claude (12)
#   agents (4)
# infra/
#   proxmox (7)
#   windows (15)
```

## Options

| Option | Description |
|--------|-------------|
| `--flat` | Affichage plat (pas d'arbre) |
| `--counts` | Inclure le nombre d'utilisations |
| `--min N` | Filtrer tags avec minimum N occurrences |

## Exemples

```powershell
/obs-tags hierarchy              # Arbre complet
/obs-tags hierarchy --counts     # Avec compteurs
/obs-tags hierarchy --min 3      # Tags utilises 3+ fois
```

## Voir Aussi

- `/obs-tags list` - Lister tous les tags
- `/obs-tags unused` - Tags rares
- `/obs-tags rename` - Renommer un tag
