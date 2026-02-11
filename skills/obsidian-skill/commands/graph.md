# Commande: /obs-graph

Analyse du graphe de liens du vault Obsidian.

## Syntaxe

```
/obs-graph [action] [options]
```

## Actions

### Statistiques du graphe

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
$LinkCount = 0
$BacklinkMap = @{}

foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if ($Content) {
        $Links = [regex]::Matches($Content, '\[\[([^\]|]+)')
        $LinkCount += $Links.Count
        foreach ($Link in $Links) {
            $Target = $Link.Groups[1].Value
            if (-not $BacklinkMap.ContainsKey($Target)) { $BacklinkMap[$Target] = 0 }
            $BacklinkMap[$Target]++
        }
    }
}

Write-Output "Notes: $($Notes.Count)"
Write-Output "Liens totaux: $LinkCount"
Write-Output "Densite: $([math]::Round($LinkCount / [math]::Max($Notes.Count, 1), 2)) liens/note"
```

### Hubs (notes les plus connectees)

```powershell
# Top 10 notes avec le plus de backlinks
$BacklinkMap.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 10 |
    ForEach-Object { "$($_.Value) backlinks -> $($_.Key)" }
```

### Clusters (groupes de notes liees)

```powershell
# Notes isolees (0 liens entrants ET 0 liens sortants)
$AllTargets = $BacklinkMap.Keys
$Isolated = $Notes | Where-Object {
    $Content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    $HasOutgoing = $Content -match '\[\['
    $HasIncoming = $_.BaseName -in $AllTargets
    -not $HasOutgoing -and -not $HasIncoming
}
Write-Output "Notes isolees: $($Isolated.Count)"
```

## Options

| Option | Description |
|--------|-------------|
| `stats` | Statistiques globales du graphe |
| `hubs` | Top notes les plus connectees |
| `clusters` | Groupes de notes liees |
| `islands` | Notes completement isolees |

## Exemples

```powershell
/obs-graph stats          # Vue d'ensemble du graphe
/obs-graph hubs           # Notes les plus liees
/obs-graph islands        # Notes isolees
```

## Voir Aussi

- `/obs-links` - Gestion des liens
- `/obs-orphans` - Notes orphelines
- `/obs-stats` - Statistiques generales
