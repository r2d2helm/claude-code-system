#Requires -Version 5.1
<#
.SYNOPSIS
    Summarizer - Génération de résumés via Claude CLI

.DESCRIPTION
    Utilise Claude CLI pour générer des résumés intelligents du contenu,
    extraire les points clés, et identifier les concepts liés.
#>

$script:SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $script:SkillPath "scripts\KnowledgeWatcher.psm1") -Force

function Invoke-KWSummarize {
    <#
    .SYNOPSIS
        Génère un résumé du contenu via Claude CLI

    .PARAMETER Content
        Le contenu à résumer

    .PARAMETER Type
        Type de contenu (conversation, code, concept, etc.)

    .PARAMETER MaxLength
        Longueur maximale du contenu à envoyer (caractères)

    .OUTPUTS
        PSCustomObject avec summary, keyPoints, concepts, actions
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Content,

        [Parameter(Mandatory)]
        [string]$Type,

        [int]$MaxLength = 50000
    )

    $config = Get-KWConfig

    # Tronquer le contenu si nécessaire
    if ($Content.Length -gt $MaxLength) {
        $Content = $Content.Substring(0, $MaxLength) + "`n`n[... contenu tronqué ...]"
        Write-KWLog -Message "Content truncated to $MaxLength characters" -Level "WARN"
    }

    # Construire le prompt selon le type
    $prompt = Get-SummaryPrompt -Type $Type -Content $Content

    try {
        $result = Invoke-ClaudeCli -Prompt $prompt -Timeout $config.processing.claudeTimeout

        if ($result.Success) {
            return Parse-SummaryResponse -Response $result.Output -Type $Type
        }
        else {
            Write-KWLog -Message "Claude CLI failed: $($result.Error)" -Level "ERROR"
            return Get-FallbackSummary -Content $Content -Type $Type
        }
    }
    catch {
        Write-KWLog -Message "Summarization error: $_" -Level "ERROR"
        return Get-FallbackSummary -Content $Content -Type $Type
    }
}

function Get-SummaryPrompt {
    <#
    .SYNOPSIS
        Génère le prompt approprié selon le type de contenu
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Type,

        [Parameter(Mandatory)]
        [string]$Content
    )

    $basePrompt = @"
Tu es un assistant spécialisé dans la capture de connaissances. Analyse le contenu suivant et génère un résumé structuré EN FRANÇAIS.

IMPORTANT: Réponds UNIQUEMENT au format JSON suivant, sans texte avant ou après:
{
  "summary": "Résumé en 2-3 phrases",
  "keyPoints": ["Point 1", "Point 2", "Point 3"],
  "concepts": ["Concept1", "Concept2"],
  "actions": ["Action 1", "Action 2"],
  "suggestedTags": ["tag1", "tag2"]
}
"@

    $typePrompt = switch ($Type) {
        "conversation" {
            @"

TYPE: Conversation Claude
Focus sur: décisions prises, problèmes résolus, code créé, concepts discutés.
"@
        }
        "code" {
            @"

TYPE: Code/Script
Focus sur: but du code, fonctions principales, dépendances, usage.
"@
        }
        "concept" {
            @"

TYPE: Concept/Idée
Focus sur: définition, importance, applications, liens avec d'autres concepts.
"@
        }
        "troubleshooting" {
            @"

TYPE: Troubleshooting
Focus sur: problème rencontré, cause identifiée, solution appliquée, prévention.
"@
        }
        default {
            @"

TYPE: Note générale
Focus sur: sujet principal, informations clés, actions potentielles.
"@
        }
    }

    return @"
$basePrompt
$typePrompt

CONTENU À ANALYSER:
---
$Content
---

Réponds en JSON valide uniquement.
"@
}

function Invoke-ClaudeCli {
    <#
    .SYNOPSIS
        Appelle Claude CLI avec timeout
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Prompt,

        [int]$Timeout = 30000
    )

    $config = Get-KWConfig
    $claudePath = $config.paths.claudeCli

    if (-not (Test-Path $claudePath)) {
        return [PSCustomObject]@{
            Success = $false
            Output = $null
            Error = "Claude CLI not found at: $claudePath"
        }
    }

    try {
        # Sauvegarder le prompt dans un fichier temporaire pour éviter les problèmes d'échappement
        $tempFile = [System.IO.Path]::GetTempFileName()
        Write-Utf8File -Path $tempFile -Content $Prompt

        $processInfo = [System.Diagnostics.ProcessStartInfo]::new()
        $processInfo.FileName = $claudePath
        $processInfo.Arguments = "--print -p `"$(Get-Content $tempFile -Raw | ForEach-Object { $_ -replace '"', '\"' })`""
        $processInfo.RedirectStandardOutput = $true
        $processInfo.RedirectStandardError = $true
        $processInfo.UseShellExecute = $false
        $processInfo.CreateNoWindow = $true
        # UTF-8 encoding for proper French character support
        $processInfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
        $processInfo.StandardErrorEncoding = [System.Text.Encoding]::UTF8

        $process = [System.Diagnostics.Process]::Start($processInfo)

        $outputTask = $process.StandardOutput.ReadToEndAsync()
        $errorTask = $process.StandardError.ReadToEndAsync()

        if ($process.WaitForExit($Timeout)) {
            $output = $outputTask.Result
            $errorOutput = $errorTask.Result

            Remove-Item $tempFile -Force -ErrorAction SilentlyContinue

            if ($process.ExitCode -eq 0) {
                return [PSCustomObject]@{
                    Success = $true
                    Output = $output
                    Error = $null
                }
            }
            else {
                return [PSCustomObject]@{
                    Success = $false
                    Output = $output
                    Error = $errorOutput
                }
            }
        }
        else {
            $process.Kill()
            Remove-Item $tempFile -Force -ErrorAction SilentlyContinue

            return [PSCustomObject]@{
                Success = $false
                Output = $null
                Error = "Claude CLI timeout after $($Timeout)ms"
            }
        }
    }
    catch {
        return [PSCustomObject]@{
            Success = $false
            Output = $null
            Error = $_.Exception.Message
        }
    }
}

function Parse-SummaryResponse {
    <#
    .SYNOPSIS
        Parse la réponse JSON de Claude
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Response,

        [string]$Type
    )

    try {
        # Nettoyer la réponse - extraire le JSON
        $jsonMatch = [regex]::Match($Response, '\{[\s\S]*\}')
        if ($jsonMatch.Success) {
            $json = $jsonMatch.Value | ConvertFrom-Json

            # PowerShell 5.1 compatible null coalescing
            return [PSCustomObject]@{
                Summary = if ($json.summary) { $json.summary } else { "Résumé non disponible" }
                KeyPoints = if ($json.keyPoints) { $json.keyPoints } else { @() }
                Concepts = if ($json.concepts) { $json.concepts } else { @() }
                Actions = if ($json.actions) { $json.actions } else { @() }
                SuggestedTags = if ($json.suggestedTags) { $json.suggestedTags } else { @() }
                Source = "claude"
            }
        }
    }
    catch {
        Write-KWLog -Message "Failed to parse Claude response: $_" -Level "WARN"
    }

    # Fallback si parsing échoue
    return Get-FallbackSummary -Content $Response -Type $Type
}

function Get-FallbackSummary {
    <#
    .SYNOPSIS
        Génère un résumé basique sans Claude CLI
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Content,

        [string]$Type
    )

    # Extraire les premières lignes significatives
    $lines = $Content -split "`n" | Where-Object { $_.Trim() -ne "" } | Select-Object -First 5
    $summary = ($lines -join " ").Substring(0, [Math]::Min(200, ($lines -join " ").Length))

    # Extraire les points clés basiques (lignes commençant par - ou *)
    $keyPoints = $Content -split "`n" |
    Where-Object { $_ -match '^\s*[-*]\s+' } |
    ForEach-Object { ($_ -replace '^\s*[-*]\s+', '').Trim() } |
    Select-Object -First 5

    return [PSCustomObject]@{
        Summary = "$summary..."
        KeyPoints = $keyPoints
        Concepts = @()
        Actions = @()
        SuggestedTags = @()
        Source = "fallback"
    }
}

# Functions exported via dot-sourcing:
# - Invoke-KWSummarize
# - Invoke-ClaudeCli
