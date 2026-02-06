# Commande: /obs-orphans

Détecter les notes orphelines (sans liens entrants ni sortants).

## Syntaxe

```
/obs-orphans [options]
```

## Comportement

Analyse toutes les notes du vault et identifie celles qui ne sont liées à aucune autre note (ni via `[[wikilinks]]` entrants, ni sortants). Les notes système (`_Templates/`, `_Index/`, `README`) sont exclues.

## Script PowerShell

```powershell
param(
    [string]$VaultPath = "$env:USERPROFILE\Documents\Knowledge",
    [switch]$Suggest
)

$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" -ErrorAction SilentlyContinue
$NoteNames = $Notes | ForEach-Object { $_.BaseName }
$AllBacklinks = @{}
$AllOutlinks = @{}

# Collecter tous les liens
foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $Content) { continue }

    $Links = [regex]::Matches($Content, '\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
    $OutTargets = @()

    foreach ($Link in $Links) {
        $Target = $Link.Groups[1].Value
        $OutTargets += $Target

        if (-not $AllBacklinks[$Target]) { $AllBacklinks[$Target] = @() }
        $AllBacklinks[$Target] += $Note.BaseName
    }

    $AllOutlinks[$Note.BaseName] = $OutTargets
}

# Trouver orphelins
$Orphans = $Notes | Where-Object {
    $Name = $_.BaseName
    $HasBacklinks = $AllBacklinks[$Name] -and $AllBacklinks[$Name].Count -gt 0
    $HasOutlinks = $AllOutlinks[$Name] -and $AllOutlinks[$Name].Count -gt 0
    $IsSystem = $_.FullName -match '(_Templates|_Index|_Attachments|\.obsidian)' -or $Name -match '^(README|INDEX)'

    -not $IsSystem -and -not $HasBacklinks -and -not $HasOutlinks
}

# Notes sans backlinks (mais avec outlinks)
$NoBacklinks = $Notes | Where-Object {
    $Name = $_.BaseName
    $HasBacklinks = $AllBacklinks[$Name] -and $AllBacklinks[$Name].Count -gt 0
    $HasOutlinks = $AllOutlinks[$Name] -and $AllOutlinks[$Name].Count -gt 0
    $IsSystem = $_.FullName -match '(_Templates|_Index|_Attachments|\.obsidian)'

    -not $IsSystem -and -not $HasBacklinks -and $HasOutlinks
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════╗"
Write-Host "║     🏝️ NOTES ORPHELINES                       ║"
Write-Host "╠══════════════════════════════════════════════╣"
Write-Host "║                                              ║"
Write-Host "║  Totalement isolées: $($Orphans.Count.ToString().PadLeft(4))                  ║"
Write-Host "║  Sans backlinks:     $($NoBacklinks.Count.ToString().PadLeft(4))                  ║"
Write-Host "║                                              ║"

if ($Orphans.Count -gt 0) {
    Write-Host "║  ISOLÉES (aucun lien):                       ║"
    foreach ($o in $Orphans | Select-Object -First 15) {
        $rel = $o.FullName.Replace($VaultPath, "").TrimStart("\")
        Write-Host "║    - $($rel.PadRight(38))║"
    }
    if ($Orphans.Count -gt 15) {
        Write-Host "║    ... et $($Orphans.Count - 15) de plus                      ║"
    }
}

Write-Host "║                                              ║"
Write-Host "║  Actions suggérées:                          ║"
Write-Host "║  1. Ajouter des [[liens]] vers ces notes     ║"
Write-Host "║  2. Déplacer vers _Inbox/ pour tri           ║"
Write-Host "║  3. Supprimer si obsolètes                   ║"
Write-Host "║                                              ║"
Write-Host "╚══════════════════════════════════════════════╝"

return @{
    Orphans = $Orphans
    NoBacklinks = $NoBacklinks
}
```

## Options

| Option | Description |
|--------|-------------|
| `--suggest` | Suggérer des liens possibles |
| `--move-inbox` | Déplacer les orphelins vers _Inbox/ |
| `--json` | Sortie JSON |
