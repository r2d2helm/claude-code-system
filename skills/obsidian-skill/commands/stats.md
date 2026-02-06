# Commande: /obs-stats

Statistiques détaillées du vault Obsidian.

## Syntaxe

```
/obs-stats [options]
```

## Comportement

Analyser le vault et afficher les statistiques complètes.

## Script PowerShell

```powershell
param(
    [string]$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
)

$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" -ErrorAction SilentlyContinue
$Attachments = Get-ChildItem -Path $VaultPath -Recurse -Include "*.png","*.jpg","*.jpeg","*.gif","*.pdf","*.webp","*.svg" -ErrorAction SilentlyContinue

$TotalWords = 0
$TotalLinks = 0
$AllTags = @()
$WithFrontmatter = 0

foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $Content) { continue }

    $TotalWords += ($Content -split '\s+').Count
    $TotalLinks += ([regex]::Matches($Content, '\[\[([^\]]+)\]\]')).Count
    $AllTags += [regex]::Matches($Content, '#[\w/-]+') | ForEach-Object { $_.Value }

    if ($Content.TrimStart().StartsWith("---")) { $WithFrontmatter++ }
}

$UniqueTags = $AllTags | Select-Object -Unique
$NoteSize = ($Notes | Measure-Object -Property Length -Sum).Sum
$AttachSize = ($Attachments | Measure-Object -Property Length -Sum).Sum

# Par type (basé sur frontmatter)
$ByType = @{}
foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if ($Content -match 'type:\s*(\w+)') {
        $type = $matches[1]
        if (-not $ByType[$type]) { $ByType[$type] = 0 }
        $ByType[$type]++
    }
}

# Par dossier
$ByFolder = $Notes | Group-Object { Split-Path (Split-Path $_.FullName) -Leaf } |
    Sort-Object Count -Descending | Select-Object -First 10

Write-Host ""
Write-Host "╔══════════════════════════════════════════════╗"
Write-Host "║        📊 STATISTIQUES DU VAULT               ║"
Write-Host "╠══════════════════════════════════════════════╣"
Write-Host "║                                              ║"
Write-Host "║  Notes totales       : $($Notes.Count.ToString().PadLeft(6))          ║"
Write-Host "║  Mots totaux         : $($TotalWords.ToString('N0').PadLeft(10))      ║"
Write-Host "║  Liens internes      : $($TotalLinks.ToString().PadLeft(6))          ║"
Write-Host "║  Tags uniques        : $($UniqueTags.Count.ToString().PadLeft(6))          ║"
Write-Host "║  Avec frontmatter    : $($WithFrontmatter.ToString().PadLeft(6))          ║"
Write-Host "║  Attachments         : $($Attachments.Count.ToString().PadLeft(6))          ║"
Write-Host "║  Taille notes        : $('{0:N1} MB' -f ($NoteSize / 1MB))       ║"
Write-Host "║  Taille attachments  : $('{0:N1} MB' -f ($AttachSize / 1MB))       ║"
Write-Host "║                                              ║"
Write-Host "║  PAR TYPE:                                   ║"
foreach ($t in $ByType.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 8) {
    Write-Host "║    $($t.Key.PadRight(18)) : $($t.Value.ToString().PadLeft(4))           ║"
}
Write-Host "║                                              ║"
Write-Host "║  PAR DOSSIER (top 10):                       ║"
foreach ($f in $ByFolder) {
    Write-Host "║    $($f.Name.PadRight(18)) : $($f.Count.ToString().PadLeft(4))           ║"
}
Write-Host "║                                              ║"
Write-Host "╚══════════════════════════════════════════════╝"
```

## Options

| Option | Description |
|--------|-------------|
| `--json` | Sortie JSON |
| `--vault=path` | Vault alternatif |
