# Commande: /obs-frontmatter

Gérer les métadonnées YAML frontmatter des notes.

## Syntaxe

```
/obs-frontmatter [action] [options]
```

## Actions

### /obs-frontmatter check

Vérifier quelles notes manquent de frontmatter :

```powershell
param(
    [string]$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
)

$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" -ErrorAction SilentlyContinue
$Missing = @()
$Invalid = @()
$Valid = 0

foreach ($Note in $Notes) {
    # Exclure templates et .obsidian
    if ($Note.FullName -match '(_Templates|\.obsidian)') { continue }

    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $Content) { continue }

    if ($Content.TrimStart().StartsWith("---")) {
        # Vérifier les champs obligatoires
        $hasTitle = $Content -match 'title:'
        $hasDate = $Content -match 'date:'
        $hasType = $Content -match 'type:'

        if ($hasTitle -and $hasDate -and $hasType) {
            $Valid++
        } else {
            $Invalid += [PSCustomObject]@{
                Path = $Note.FullName.Replace($VaultPath, "")
                MissingTitle = -not $hasTitle
                MissingDate = -not $hasDate
                MissingType = -not $hasType
            }
        }
    } else {
        $Missing += $Note
    }
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════╗"
Write-Host "║     📋 ÉTAT FRONTMATTER                       ║"
Write-Host "╠══════════════════════════════════════════════╣"
Write-Host "║                                              ║"
Write-Host "║  ✅ Complet:     $($Valid.ToString().PadLeft(4))                       ║"
Write-Host "║  ⚠️ Incomplet:   $($Invalid.Count.ToString().PadLeft(4))                       ║"
Write-Host "║  ❌ Manquant:    $($Missing.Count.ToString().PadLeft(4))                       ║"
Write-Host "║                                              ║"
Write-Host "╚══════════════════════════════════════════════╝"
```

### /obs-frontmatter add

Ajouter le frontmatter manquant aux notes qui n'en ont pas :

```powershell
param(
    [string]$VaultPath = "$env:USERPROFILE\Documents\Knowledge",
    [switch]$DryRun
)

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" -ErrorAction SilentlyContinue
$Added = 0

foreach ($Note in $Notes) {
    if ($Note.FullName -match '(_Templates|\.obsidian)') { continue }

    $Content = [System.IO.File]::ReadAllText($Note.FullName, $utf8NoBom)
    if ($Content.TrimStart().StartsWith("---")) { continue }

    # Extraire titre
    $title = if ($Content -match '^#\s+(.+)$') { $matches[1].Trim() -replace '"', "'" }
            else { [System.IO.Path]::GetFileNameWithoutExtension($Note.Name) }

    # Déterminer type
    $type = "reference"
    if ($Note.FullName -match 'Conversations') { $type = "conversation" }
    elseif ($Note.FullName -match 'Concepts') { $type = "concept" }
    elseif ($Note.FullName -match 'Formations') { $type = "formation" }
    elseif ($Note.FullName -match 'Troubleshooting') { $type = "troubleshooting" }
    elseif ($Note.FullName -match 'Projets') { $type = "project" }

    $date = $Note.LastWriteTime.ToString("yyyy-MM-dd")

    $fm = "---`ntitle: `"$title`"`ndate: $date`ntype: $type`ntags:`n  - $type`nrelated: []`n---`n`n"

    if ($DryRun) {
        Write-Host "[DRY RUN] Would add frontmatter to: $($Note.Name)"
    } else {
        [System.IO.File]::WriteAllText($Note.FullName, $fm + $Content, $utf8NoBom)
        Write-Host "Added frontmatter: $($Note.Name)"
    }
    $Added++
}

Write-Host "`nTotal: $Added notes $(if ($DryRun) { '(dry run)' } else { 'updated' })"
```

### /obs-frontmatter validate

Valider la cohérence du frontmatter existant (types valides, dates correctes, tags bien formés).

### /obs-frontmatter update-dates

Mettre à jour le champ `date` avec la date de dernière modification réelle du fichier.

## Options

| Option | Description |
|--------|-------------|
| `check` | Vérifier l'état du frontmatter |
| `add` | Ajouter frontmatter manquant |
| `validate` | Valider le frontmatter existant |
| `update-dates` | Mettre à jour les dates |
| `--dry-run` | Simuler sans modifier |
| `--vault=path` | Vault alternatif |
