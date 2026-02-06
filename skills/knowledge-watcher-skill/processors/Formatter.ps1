#Requires -Version 5.1
<#
.SYNOPSIS
    Formatter - Génération de notes Markdown Obsidian

.DESCRIPTION
    Formate le contenu traité en notes Markdown compatibles Obsidian
    avec frontmatter YAML, wikilinks, et templates appropriés.
#>

$script:SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $script:SkillPath "scripts\KnowledgeWatcher.psm1") -Force

# Charger l'AutoLinker pour les liens automatiques
. (Join-Path $script:SkillPath "processors\AutoLinker.ps1")

function Format-KWNote {
    <#
    .SYNOPSIS
        Formate un élément en note Markdown Obsidian

    .PARAMETER Title
        Titre de la note

    .PARAMETER Content
        Contenu original

    .PARAMETER Classification
        Résultat de la classification

    .PARAMETER Summary
        Résultat du résumé

    .PARAMETER SourcePath
        Chemin source

    .OUTPUTS
        PSCustomObject avec FileName, FilePath, Content
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Title,

        [Parameter(Mandatory)]
        [string]$Content,

        [Parameter(Mandatory)]
        [PSCustomObject]$Classification,

        [Parameter(Mandatory)]
        [PSCustomObject]$Summary,

        [string]$SourcePath
    )

    $config = Get-KWConfig
    $date = Get-Date
    $dateStr = $date.ToString("yyyy-MM-dd")
    $timeStr = $date.ToString("HHmmss")
    $id = "$($date.ToString('yyyyMMdd'))-$timeStr"

    # Générer le nom de fichier
    $prefix = $Classification.Prefix -replace '\{date\}', $dateStr
    $safeName = ConvertTo-SafeFileName -Name $Title
    $fileName = "$prefix$safeName.md"

    # Construire le chemin complet
    $folder = $Classification.Folder
    $fullPath = Join-Path $config.paths.obsidianVault $folder
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
    }
    $filePath = Join-Path $fullPath $fileName

    # Générer les tags combinés
    $allTags = @($Classification.Tags) + @($Summary.SuggestedTags) | Select-Object -Unique

    # Générer le contenu selon le type
    $noteContent = switch ($Classification.Type) {
        "conversation" { Format-ConversationNote -Title $Title -Content $Content -Summary $Summary -Id $id -Date $dateStr -Tags $allTags -SourcePath $SourcePath }
        "code" { Format-CodeNote -Title $Title -Content $Content -Summary $Summary -Id $id -Date $dateStr -Tags $allTags -SourcePath $SourcePath }
        "concept" { Format-ConceptNote -Title $Title -Content $Content -Summary $Summary -Id $id -Date $dateStr -Tags $allTags }
        "troubleshooting" { Format-TroubleshootingNote -Title $Title -Content $Content -Summary $Summary -Id $id -Date $dateStr -Tags $allTags }
        "project" { Format-ProjectNote -Title $Title -Content $Content -Summary $Summary -Id $id -Date $dateStr -Tags $allTags -SourcePath $SourcePath }
        default { Format-DefaultNote -Title $Title -Content $Content -Summary $Summary -Id $id -Date $dateStr -Tags $allTags }
    }

    # Appliquer l'auto-linking vers les notes existantes
    try {
        $autoLinkResult = Invoke-AutoLink -Content $noteContent -NotePath $filePath
        if ($autoLinkResult.LinkCount -gt 0) {
            $noteContent = $autoLinkResult.Content
            Write-KWLog -Message "Auto-linked $($autoLinkResult.LinkCount) terms: $($autoLinkResult.LinksAdded -join ', ')" -Level "INFO"
        }
    }
    catch {
        Write-KWLog -Message "Auto-linking failed: $_" -Level "WARN"
    }

    return [PSCustomObject]@{
        FileName = $fileName
        FilePath = $filePath
        Folder = $folder
        Content = $noteContent
        Type = $Classification.Type
        Tags = $allTags
    }
}

function ConvertTo-SafeFileName {
    <#
    .SYNOPSIS
        Convertit un titre en nom de fichier sûr
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Name
    )

    # Remplacer les espaces et caractères spéciaux
    $safe = $Name -replace '\s+', '-'
    $safe = $safe -replace '[<>:"/\\|?*]', ''
    $safe = $safe -replace '-+', '-'
    $safe = $safe.Trim('-')

    # Limiter la longueur
    if ($safe.Length -gt 100) {
        $safe = $safe.Substring(0, 100)
    }

    return $safe
}

function Format-FrontMatter {
    <#
    .SYNOPSIS
        Génère le frontmatter YAML
    #>
    [CmdletBinding()]
    param(
        [string]$Id,
        [string]$Title,
        [string]$Date,
        [string]$Type,
        [string[]]$Tags,
        [string]$Source = "KnowledgeWatcher",
        [string]$Status = "captured",
        [string[]]$Related = @()
    )

    $tagsYaml = ($Tags | ForEach-Object { "`"$_`"" }) -join ", "
    $relatedYaml = ($Related | ForEach-Object { "`"[[$_]]`"" }) -join ", "

    return @"
---
id: $Id
title: "$Title"
date: $Date
type: $Type
tags: [$tagsYaml]
source: $Source
status: $Status
related: [$relatedYaml]
created: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
---
"@
}

function Format-ConversationNote {
    param($Title, $Content, $Summary, $Id, $Date, $Tags, $SourcePath)

    $frontMatter = Format-FrontMatter -Id $Id -Title $Title -Date $Date -Type "conversation" -Tags $Tags -Source "Claude"

    $keyPointsList = if ($Summary.KeyPoints.Count -gt 0) {
        ($Summary.KeyPoints | ForEach-Object { "- $_" }) -join "`n"
    }
    else { "- (Aucun point clé extrait)" }

    $actionsList = if ($Summary.Actions.Count -gt 0) {
        ($Summary.Actions | ForEach-Object { "- [ ] $_" }) -join "`n"
    }
    else { "- [ ] " }

    $conceptsList = if ($Summary.Concepts.Count -gt 0) {
        ($Summary.Concepts | ForEach-Object { "- [[$_]]" }) -join "`n"
    }
    else { "- [[]]" }

    # Extraire le code du contenu
    $codeBlocks = Extract-CodeBlocks -Content $Content

    return @"
$frontMatter

# $Title

## Résumé
$($Summary.Summary)

## Points Clés
$keyPointsList

## Décisions Prises
- [ ]

## Code/Commandes
$codeBlocks

## Concepts Liés
$conceptsList

## Actions Suivantes
$actionsList

## Notes
<!-- Notes additionnelles -->


---
*Capturé le $Date par Knowledge Watcher*
*Source: $SourcePath*
"@
}

function Format-CodeNote {
    param($Title, $Content, $Summary, $Id, $Date, $Tags, $SourcePath)

    $frontMatter = Format-FrontMatter -Id $Id -Title $Title -Date $Date -Type "code" -Tags $Tags

    # Détecter le langage
    $ext = [System.IO.Path]::GetExtension($SourcePath)
    $lang = switch ($ext) {
        ".ps1" { "powershell" }
        ".psm1" { "powershell" }
        ".py" { "python" }
        ".js" { "javascript" }
        ".ts" { "typescript" }
        ".go" { "go" }
        ".rs" { "rust" }
        ".sh" { "bash" }
        default { "" }
    }

    return @"
$frontMatter

# $Title

## Description
$($Summary.Summary)

## Code
``````$lang
$Content
``````

## Utilisation
``````
<!-- Exemple d'utilisation -->
``````

## Points Clés
$(($Summary.KeyPoints | ForEach-Object { "- $_" }) -join "`n")

## Notes
<!-- Notes sur l'implémentation -->


## Voir aussi
$(($Summary.Concepts | ForEach-Object { "- [[$_]]" }) -join "`n")

---
*Capturé le $Date par Knowledge Watcher*
*Source: $SourcePath*
"@
}

function Format-ConceptNote {
    param($Title, $Content, $Summary, $Id, $Date, $Tags)

    $frontMatter = Format-FrontMatter -Id $Id -Title $Title -Date $Date -Type "concept" -Tags $Tags

    return @"
$frontMatter

# $Title

$($Summary.Summary)

## Pourquoi c'est important
<!-- Contexte et pertinence -->


## Détails
$(($Summary.KeyPoints | ForEach-Object { "- $_" }) -join "`n")

## Exemples
<!-- Exemples concrets -->


## Liens
- Découle de: [[]]
- Mène à: [[]]
$(($Summary.Concepts | ForEach-Object { "- Voir aussi: [[$_]]" }) -join "`n")

## Sources
- [[]]

---
*Capturé le $Date par Knowledge Watcher*
"@
}

function Format-TroubleshootingNote {
    param($Title, $Content, $Summary, $Id, $Date, $Tags)

    $frontMatter = Format-FrontMatter -Id $Id -Title $Title -Date $Date -Type "troubleshooting" -Tags $Tags -Status "resolved"

    return @"
$frontMatter

# 🔧 $Title

## Problème
$($Summary.Summary)

## Environnement
- **OS**:
- **Version**:
- **Contexte**:

## Symptômes
$(($Summary.KeyPoints | ForEach-Object { "- $_" }) -join "`n")

## Message d'Erreur
``````
<!-- Message exact -->
``````

## Cause Identifiée
<!-- Pourquoi ça arrive -->


## Solution
$(($Summary.Actions | ForEach-Object { $i = [array]::IndexOf($Summary.Actions, $_) + 1; "$i. $_" }) -join "`n")

## Code de Résolution
$(Extract-CodeBlocks -Content $Content)

## Prévention
<!-- Comment éviter à l'avenir -->


## Références
$(($Summary.Concepts | ForEach-Object { "- [[$_]]" }) -join "`n")

---
*Capturé le $Date par Knowledge Watcher*
"@
}

function Format-ProjectNote {
    param($Title, $Content, $Summary, $Id, $Date, $Tags, $SourcePath)

    $frontMatter = Format-FrontMatter -Id $Id -Title $Title -Date $Date -Type "project" -Tags $Tags

    # Extraire le nom du projet
    $projectName = ""
    if ($SourcePath -match '[/\\]Projets[/\\]([^/\\]+)') {
        $projectName = $Matches[1]
    }

    return @"
$frontMatter

# $Title

**Projet:** $projectName

## Résumé
$($Summary.Summary)

## Points Clés
$(($Summary.KeyPoints | ForEach-Object { "- $_" }) -join "`n")

## Actions
$(($Summary.Actions | ForEach-Object { "- [ ] $_" }) -join "`n")

## Contenu Original
$Content

## Notes
<!-- Notes additionnelles -->


## Liens
$(($Summary.Concepts | ForEach-Object { "- [[$_]]" }) -join "`n")

---
*Capturé le $Date par Knowledge Watcher*
*Source: $SourcePath*
"@
}

function Format-DefaultNote {
    param($Title, $Content, $Summary, $Id, $Date, $Tags)

    $frontMatter = Format-FrontMatter -Id $Id -Title $Title -Date $Date -Type "note" -Tags $Tags

    return @"
$frontMatter

# $Title

## Résumé
$($Summary.Summary)

## Points Clés
$(($Summary.KeyPoints | ForEach-Object { "- $_" }) -join "`n")

## Contenu
$Content

## Notes
<!-- Notes additionnelles -->


---
*Capturé le $Date par Knowledge Watcher*
"@
}

function Extract-CodeBlocks {
    <#
    .SYNOPSIS
        Extrait les blocs de code du contenu
    #>
    [CmdletBinding()]
    param(
        [string]$Content
    )

    $pattern = '```(\w*)\r?\n([\s\S]*?)```'
    $matches = [regex]::Matches($Content, $pattern)

    if ($matches.Count -eq 0) {
        return "``````powershell`n# Code à ajouter`n``````"
    }

    $blocks = @()
    foreach ($match in $matches) {
        $lang = $match.Groups[1].Value
        if ([string]::IsNullOrWhiteSpace($lang)) { $lang = "" }
        $code = $match.Groups[2].Value
        $blocks += "``````$lang`n$code``````"
    }

    return $blocks -join "`n`n"
}

function Update-DailyNote {
    <#
    .SYNOPSIS
        Met à jour la Daily Note avec un lien vers la nouvelle note
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$NoteFileName,

        [Parameter(Mandatory)]
        [string]$Type
    )

    $config = Get-KWConfig
    if (-not $config.output.updateDailyNote) {
        return
    }

    $date = Get-Date -Format "yyyy-MM-dd"
    $dailyPath = Join-Path $config.paths.obsidianVault "_Daily\$date.md"

    # Créer la Daily Note si elle n'existe pas
    if (-not (Test-Path $dailyPath)) {
        $dailyFolder = Join-Path $config.paths.obsidianVault "_Daily"
        if (-not (Test-Path $dailyFolder)) {
            New-Item -ItemType Directory -Path $dailyFolder -Force | Out-Null
        }

        $dailyContent = @"
---
date: $date
type: daily
tags: [daily]
---

# 📅 $date

## Conversations du Jour

## Captures Automatiques

## Notes

"@
        Write-Utf8File -Path $dailyPath -Content $dailyContent
    }

    # Ajouter le lien
    $noteLink = "[[$($NoteFileName -replace '\.md$', '')]]"
    $section = switch ($Type) {
        "conversation" { "## Conversations du Jour" }
        default { "## Captures Automatiques" }
    }

    $content = Read-Utf8File -Path $dailyPath
    if (-not $content) {
        $content = Get-Content $dailyPath -Raw
    }

    # Vérifier si le lien existe déjà
    if ($content -notmatch [regex]::Escape($noteLink)) {
        # Trouver la section et ajouter le lien
        if ($content -match $section) {
            $content = $content -replace "($section)", "`$1`n- $noteLink"
        }
        else {
            # Ajouter la section si elle n'existe pas
            $content += "`n$section`n- $noteLink"
        }

        Write-Utf8File -Path $dailyPath -Content $content
        Write-KWLog -Message "Updated Daily Note with: $noteLink" -Level "INFO"
    }
}

# Functions exported via dot-sourcing:
# - Format-KWNote
# - Update-DailyNote
# - ConvertTo-SafeFileName
# - Extract-CodeBlocks
