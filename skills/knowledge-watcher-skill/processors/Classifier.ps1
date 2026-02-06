#Requires -Version 5.1
<#
.SYNOPSIS
    Classifier - Classification automatique du contenu

.DESCRIPTION
    Analyse le contenu et détermine son type, dossier de destination,
    template à utiliser et tags à appliquer selon les règles définies.
#>

$script:SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $script:SkillPath "scripts\KnowledgeWatcher.psm1") -Force

function Invoke-KWClassify {
    <#
    .SYNOPSIS
        Classifie un contenu selon les règles définies

    .PARAMETER Content
        Le contenu à classifier

    .PARAMETER SourcePath
        Chemin source du fichier

    .PARAMETER SourceId
        Identifiant de la source

    .OUTPUTS
        PSCustomObject avec type, folder, prefix, template, tags
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Content,

        [Parameter(Mandatory)]
        [string]$SourcePath,

        [string]$SourceId
    )

    $rules = Get-KWRules
    $extension = [System.IO.Path]::GetExtension($SourcePath)

    # Trier les règles par priorité décroissante
    $sortedRules = $rules.classification.rules | Sort-Object -Property priority -Descending

    foreach ($rule in $sortedRules) {
        if (Test-RuleMatch -Rule $rule -Content $Content -SourcePath $SourcePath -Extension $extension) {
            Write-Verbose "Matched rule: $($rule.name)"

            $output = $rule.output.PSObject.Copy()

            # Résoudre les variables dans le dossier
            $folder = Resolve-FolderPath -FolderTemplate $output.folder -SourcePath $SourcePath

            # Générer les tags automatiques
            $autoTags = Get-AutoTags -Content $Content -Rules $rules.tagging

            return [PSCustomObject]@{
                RuleId = $rule.id
                RuleName = $rule.name
                Type = $output.type
                Folder = $folder
                Prefix = $output.prefix
                Template = $output.template
                Tags = @($output.tags) + $autoTags | Select-Object -Unique
            }
        }
    }

    # Fallback - ne devrait jamais arriver car il y a une règle "default"
    return [PSCustomObject]@{
        RuleId = "default"
        RuleName = "Default"
        Type = "note"
        Folder = "_Inbox"
        Prefix = "{date}_"
        Template = $null
        Tags = @("inbox")
    }
}

function Test-RuleMatch {
    <#
    .SYNOPSIS
        Teste si une règle correspond au contenu
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [PSCustomObject]$Rule,

        [string]$Content,
        [string]$SourcePath,
        [string]$Extension
    )

    $conditions = $Rule.conditions

    # Règle "always" (pour default)
    if ($conditions.always -eq $true) {
        return $true
    }

    # Conditions "any" (OR)
    if ($conditions.any) {
        foreach ($condition in $conditions.any) {
            if (Test-SingleCondition -Condition $condition -Content $Content -SourcePath $SourcePath -Extension $Extension) {
                return $true
            }
        }
        return $false
    }

    # Conditions "all" (AND)
    if ($conditions.all) {
        foreach ($condition in $conditions.all) {
            if (-not (Test-SingleCondition -Condition $condition -Content $Content -SourcePath $SourcePath -Extension $Extension)) {
                return $false
            }
        }
        return $true
    }

    return $false
}

function Test-SingleCondition {
    <#
    .SYNOPSIS
        Teste une condition unique
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [PSCustomObject]$Condition,

        [string]$Content,
        [string]$SourcePath,
        [string]$Extension
    )

    $field = $Condition.field
    $value = switch ($field) {
        "content" { $Content }
        "path" { $SourcePath }
        "source" { $SourcePath }
        "extension" { $Extension }
        default { "" }
    }

    # Opérateur "contains"
    if ($Condition.contains) {
        return $value -like "*$($Condition.contains)*"
    }

    # Opérateur "containsAny"
    if ($Condition.containsAny) {
        foreach ($pattern in $Condition.containsAny) {
            if ($value -like "*$pattern*") {
                return $true
            }
        }
        return $false
    }

    # Opérateur "equals"
    if ($Condition.equals) {
        return $value -eq $Condition.equals
    }

    # Opérateur "matches" (regex)
    if ($Condition.matches) {
        return $value -match $Condition.matches
    }

    return $false
}

function Resolve-FolderPath {
    <#
    .SYNOPSIS
        Résout les variables dans le chemin du dossier
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$FolderTemplate,

        [string]$SourcePath
    )

    $result = $FolderTemplate

    # {projectName} - extraire le nom du projet du chemin
    if ($result -match '\{projectName\}') {
        $projectName = ""
        if ($SourcePath -match '[/\\]Projets[/\\]([^/\\]+)') {
            $projectName = $Matches[1]
        }
        $result = $result -replace '\{projectName\}', $projectName
    }

    # {lang} - extraire le langage de l'extension
    if ($result -match '\{lang\}') {
        $ext = [System.IO.Path]::GetExtension($SourcePath).TrimStart('.')
        $lang = switch ($ext) {
            "ps1" { "PowerShell" }
            "psm1" { "PowerShell" }
            "py" { "Python" }
            "js" { "JavaScript" }
            "ts" { "TypeScript" }
            "go" { "Go" }
            "rs" { "Rust" }
            "sh" { "Shell" }
            "bash" { "Shell" }
            default { $ext.ToUpper() }
        }
        $result = $result -replace '\{lang\}', $lang
    }

    return $result
}

function Get-AutoTags {
    <#
    .SYNOPSIS
        Génère les tags automatiques basés sur le contenu
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Content,

        [PSCustomObject]$Rules
    )

    $tags = @()

    if ($Rules.autoTags) {
        foreach ($autoTag in $Rules.autoTags) {
            if ($Content -match $autoTag.pattern) {
                $tags += $autoTag.tag
            }
        }
    }

    return $tags
}

function Get-SuggestedTitle {
    <#
    .SYNOPSIS
        Suggère un titre basé sur le contenu
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Content,

        [string]$SourcePath
    )

    # Essayer d'extraire un titre du contenu
    # 1. Chercher un header markdown
    if ($Content -match '^#\s+(.+)$') {
        return $Matches[1].Trim()
    }

    # 2. Chercher une première ligne significative
    $lines = $Content -split "`n" | Where-Object { $_.Trim() -ne "" }
    if ($lines.Count -gt 0) {
        $firstLine = $lines[0].Trim()
        if ($firstLine.Length -le 100) {
            return $firstLine
        }
        return $firstLine.Substring(0, 97) + "..."
    }

    # 3. Utiliser le nom du fichier
    return [System.IO.Path]::GetFileNameWithoutExtension($SourcePath)
}

# Functions exported via dot-sourcing:
# - Invoke-KWClassify
# - Get-SuggestedTitle
# - Get-AutoTags
