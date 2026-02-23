#Requires -Version 5.1
<#
.SYNOPSIS
    Traite la queue de Knowledge Watcher

.DESCRIPTION
    Prend les éléments de la queue et les transforme en notes Obsidian
    via le pipeline Classifier → Summarizer → Formatter.

.PARAMETER BatchSize
    Nombre maximum d'éléments à traiter

.PARAMETER Force
    Traiter même si des erreurs se produisent

.EXAMPLE
    .\Invoke-QueueProcessor.ps1
    .\Invoke-QueueProcessor.ps1 -BatchSize 5
#>

[CmdletBinding()]
param(
    [int]$BatchSize = 10,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $SkillPath "scripts\KnowledgeWatcher.psm1") -Force

# Importer les processors
. (Join-Path $SkillPath "processors\Classifier.ps1")
. (Join-Path $SkillPath "processors\Summarizer.ps1")
. (Join-Path $SkillPath "processors\Formatter.ps1")

function Invoke-QueueProcessing {
    param(
        [int]$BatchSize = 10
    )

    $config = Get-KWConfig
    $queue = Get-KWQueue

    $pendingItems = $queue.items | Where-Object { $_.status -eq "pending" } | Select-Object -First $BatchSize

    if ($pendingItems.Count -eq 0) {
        Write-Host "[INFO] Queue is empty" -ForegroundColor Yellow
        return @{
            Processed = 0
            Errors = 0
            Skipped = 0
        }
    }

    Write-Host "Processing $($pendingItems.Count) item(s)..." -ForegroundColor Cyan
    Write-Host ""

    $processed = 0
    $errors = 0
    $skipped = 0

    foreach ($item in $pendingItems) {
        # PowerShell 5.1 compatible null coalescing
        $displayTitle = if ($item.title) { $item.title } else { $item.sourcePath }
        Write-Host "  [FILE] $displayTitle" -ForegroundColor White

        try {
            # Marquer comme en cours
            $item.status = "processing"
            Save-KWQueue -Queue $queue

            # Récupérer le contenu si pas déjà présent
            $content = $null
            if (Test-Path $item.sourcePath -ErrorAction SilentlyContinue) {
                $content = Get-Content -Path $item.sourcePath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
            }

            if (-not $content) {
                # Pour Claude history ou autres sources, le contenu devrait être dans les métadonnées
                # ou on doit le récupérer autrement
                $content = "Content from: $($item.sourcePath)`n`nCaptured at: $($item.capturedAt)"
            }

            # 1. Classification
            Write-Host "     -> Classifying..." -ForegroundColor Gray
            $classification = Invoke-KWClassify -Content $content -SourcePath $item.sourcePath -SourceId $item.sourceId

            Write-Host "       Type: $($classification.Type), Folder: $($classification.Folder)" -ForegroundColor DarkGray

            # 2. Résumé (avec Claude CLI)
            Write-Host "     -> Summarizing..." -ForegroundColor Gray
            $summary = Invoke-KWSummarize -Content $content -Type $classification.Type

            Write-Host "       Source: $($summary.Source)" -ForegroundColor DarkGray

            # 3. Formatage
            Write-Host "     -> Formatting..." -ForegroundColor Gray
            # PowerShell 5.1 compatible null coalescing
            $noteTitle = if ($item.title) { $item.title } else { Get-SuggestedTitle -Content $content -SourcePath $item.sourcePath }
            $note = Format-KWNote `
                -Title $noteTitle `
                -Content $content `
                -Classification $classification `
                -Summary $summary `
                -SourcePath $item.sourcePath

            # 4. Écriture du fichier
            Write-Host "     -> Writing note..." -ForegroundColor Gray

            # Vérifier si le fichier existe déjà
            if (Test-Path $note.FilePath) {
                Write-Host "     [SKIP] File already exists" -ForegroundColor Yellow
                $item.status = "skipped"
                $skipped++
            }
            else {
                Write-Utf8File -Path $note.FilePath -Content $note.Content
                Write-Host "     [OK] Created: $($note.FileName)" -ForegroundColor Green

                # Mettre à jour la Daily Note
                Update-DailyNote -NoteFileName $note.FileName -Type $note.Type

                $item.status = "completed"
                # Add properties dynamically if they don't exist
                if (-not ($item.PSObject.Properties.Name -contains "processedAt")) {
                    $item | Add-Member -NotePropertyName "processedAt" -NotePropertyValue $null
                }
                if (-not ($item.PSObject.Properties.Name -contains "outputPath")) {
                    $item | Add-Member -NotePropertyName "outputPath" -NotePropertyValue $null
                }
                $item.processedAt = (Get-Date).ToString("o")
                $item.outputPath = $note.FilePath
                $processed++
            }

            Write-KWLog -Message "Processed: $($item.sourcePath) -> $($note.FilePath)" -Level "INFO"
        }
        catch {
            Write-Host "     [ERROR] $_" -ForegroundColor Red
            $item.status = "error"
            # Add error property dynamically if it doesn't exist
            if (-not ($item.PSObject.Properties.Name -contains "error")) {
                $item | Add-Member -NotePropertyName "error" -NotePropertyValue $null
            }
            $item.error = $_.ToString()
            $errors++

            Write-KWLog -Message "Error processing $($item.sourcePath): $_" -Level "ERROR"

            if (-not $Force) {
                # Continuer avec les autres items
            }
        }

        Write-Host ""
    }

    # Mettre à jour les stats
    $queue.stats.totalProcessed += $processed
    $queue.stats.totalErrors += $errors
    $queue.lastProcessed = (Get-Date).ToString("o")

    # Nettoyer les items complétés (garder 24h pour debug)
    $cutoff = (Get-Date).AddHours(-24)
    $queue.items = $queue.items | Where-Object {
        # PowerShell 5.1 compatible null coalescing
        $processedAt = if ($_.processedAt) { $_.processedAt } else { "2000-01-01" }
        $_.status -ne "completed" -or ([DateTime]::Parse($processedAt) -gt $cutoff)
    }

    Save-KWQueue -Queue $queue

    # Résumé
    Write-Host "===========================================" -ForegroundColor Cyan
    Write-Host "  [OK] Processed : $processed" -ForegroundColor Green
    $errColor = if ($errors -gt 0) { "Red" } else { "Gray" }
    Write-Host "  [ERR] Errors   : $errors" -ForegroundColor $errColor
    $skipColor = if ($skipped -gt 0) { "Yellow" } else { "Gray" }
    Write-Host "  [SKIP] Skipped : $skipped" -ForegroundColor $skipColor
    Write-Host "===========================================" -ForegroundColor Cyan

    return @{
        Processed = $processed
        Errors = $errors
        Skipped = $skipped
    }
}

# Exécution
$result = Invoke-QueueProcessing -BatchSize $BatchSize
