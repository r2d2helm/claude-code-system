# Commande: /obs-tags unused

Lister les tags utilises une seule fois ou non utilises dans le vault.

## Syntaxe

```
/obs-tags unused [options]
```

## Actions

### Trouver tags rares

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
$TagCounts = @{}

foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if ($Content) {
        # Tags inline (#tag)
        [regex]::Matches($Content, '(?<=\s|^)#([\w/-]+)') | ForEach-Object {
            $Tag = $_.Groups[1].Value
            if (-not $TagCounts.ContainsKey($Tag)) { $TagCounts[$Tag] = 0 }
            $TagCounts[$Tag]++
        }
        # Tags frontmatter
        if ($Content -match '(?s)^---\s*\n(.+?)\n---') {
            [regex]::Matches($Matches[1], '^\s*-\s+(.+)$', 'Multiline') | ForEach-Object {
                $Tag = $_.Groups[1].Value.Trim()
                if ($Tag -match '^[\w/-]+$') {
                    if (-not $TagCounts.ContainsKey($Tag)) { $TagCounts[$Tag] = 0 }
                    $TagCounts[$Tag]++
                }
            }
        }
    }
}

# Tags utilises 1 seule fois
$Rare = $TagCounts.GetEnumerator() | Where-Object { $_.Value -eq 1 } | Sort-Object Key
Write-Output "Tags utilises 1 seule fois ($($Rare.Count)):"
$Rare | ForEach-Object { "  #$($_.Key)" }
```

## Options

| Option | Description |
|--------|-------------|
| `--max N` | Tags utilises N fois ou moins (defaut: 1) |
| `--delete` | Supprimer les tags rares (avec confirmation) |

## Exemples

```powershell
/obs-tags unused              # Tags utilises 1 fois
/obs-tags unused --max 2      # Tags utilises 2 fois ou moins
```

## Voir Aussi

- `/obs-tags list` - Lister tous les tags
- `/obs-tags rename` - Renommer un tag
- `/obs-tags merge` - Fusionner des tags
