#Requires -Version 5.1
<#
.SYNOPSIS
    Rétro-Linking - Met à jour les anciennes notes avec des liens vers les nouvelles

.DESCRIPTION
    Scanne toutes les notes du vault et ajoute les liens wiki manquants
    vers les notes existantes. Inclut mode dry-run et rapport détaillé.

.PARAMETER DryRun
    Affiche les changements sans modifier les fichiers

.PARAMETER Path
    Chemin spécifique à traiter (défaut: tout le vault)

.PARAMETER MaxNotesPerRun
    Nombre maximum de notes à traiter (défaut: 100)

.PARAMETER ExcludeFolders
    Dossiers à exclure (défaut: _Templates, .obsidian)

.PARAMETER UseAI
    Utiliser les suggestions IA (plus lent, défaut: false)

.EXAMPLE
    .\Invoke-RetroLinking.ps1 -DryRun
    .\Invoke-RetroLinking.ps1 -MaxNotesPerRun 50
    .\Invoke-RetroLinking.ps1 -Path "C:\Vault\Projets"
#>

[CmdletBinding()]
param(
    [switch]$DryRun,
    [string]$Path,
    [int]$MaxNotesPerRun = 100,
    [string[]]$ExcludeFolders = @("_Templates", ".obsidian", "_Attachments"),
    [switch]$UseAI
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $SkillPath "scripts\KnowledgeWatcher.psm1") -Force
. (Join-Path $SkillPath "processors\AutoLinker.ps1")

function Invoke-RetroLinking {
    $config = Get-KWConfig
    $vaultPath = if ($Path) { $Path } else { $config.paths.obsidianVault }

    if (-not (Test-Path $vaultPath)) {
        Write-Error "Vault path not found: $vaultPath"
        return
    }

    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  RETRO-LINKING" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Vault: $vaultPath" -ForegroundColor Gray
    Write-Host "  Mode: $(if ($DryRun) { 'DRY RUN' } else { 'LIVE' })" -ForegroundColor $(if ($DryRun) { 'Yellow' } else { 'Green' })
    Write-Host "  Max notes: $MaxNotesPerRun" -ForegroundColor Gray
    Write-Host "  Use AI: $UseAI" -ForegroundColor Gray
    Write-Host "========================================`n" -ForegroundColor Cyan

    # Rebuild index first
    Write-Host "Rebuilding notes index..." -ForegroundColor Cyan
    & (Join-Path $SkillPath "scripts\Build-NotesIndex.ps1") | Out-Null
    Write-Host ""

    # Get all markdown files
    $allFiles = Get-ChildItem -Path $vaultPath -Filter "*.md" -Recurse -File

    # Filter excluded folders
    $files = $allFiles | Where-Object {
        $relativePath = $_.FullName.Substring($vaultPath.Length + 1)
        $excluded = $false
        foreach ($folder in $ExcludeFolders) {
            if ($relativePath -match "^$folder[\\/]") {
                $excluded = $true
                break
            }
        }
        -not $excluded
    } | Select-Object -First $MaxNotesPerRun

    Write-Host "Found $($files.Count) notes to process`n" -ForegroundColor Cyan

    # Stats
    $stats = @{
        Processed = 0
        Updated = 0
        Skipped = 0
        Errors = 0
        TotalLinksAdded = 0
    }

    $report = @()

    foreach ($file in $files) {
        $relativePath = $file.FullName.Substring($vaultPath.Length + 1)
        Write-Host "[$($stats.Processed + 1)/$($files.Count)] $relativePath" -ForegroundColor White -NoNewline

        try {
            $content = Read-Utf8File -Path $file.FullName

            if ([string]::IsNullOrWhiteSpace($content)) {
                Write-Host " [SKIP: empty]" -ForegroundColor Gray
                $stats.Skipped++
                $stats.Processed++
                continue
            }

            # Apply auto-linking
            if ($UseAI) {
                $result = Invoke-AutoLinkWithAI -Content $content -NotePath $file.FullName -UseAI
            } else {
                $result = Invoke-AutoLink -Content $content -NotePath $file.FullName
            }

            if ($result.LinkCount -eq 0) {
                Write-Host " [OK: no links to add]" -ForegroundColor Gray
                $stats.Skipped++
            }
            else {
                Write-Host " [+$($result.LinkCount) links]" -ForegroundColor Green

                $report += [PSCustomObject]@{
                    File = $relativePath
                    LinksAdded = $result.LinksAdded -join ", "
                    Count = $result.LinkCount
                }

                if (-not $DryRun) {
                    Write-Utf8File -Path $file.FullName -Content $result.Content
                    Write-KWLog -Message "Retro-linked $($result.LinkCount) terms in: $relativePath" -Level "INFO"
                }

                $stats.Updated++
                $stats.TotalLinksAdded += $result.LinkCount
            }
        }
        catch {
            Write-Host " [ERROR: $_]" -ForegroundColor Red
            $stats.Errors++
            Write-KWLog -Message "Retro-linking failed for $relativePath : $_" -Level "ERROR"
        }

        $stats.Processed++
    }

    # Summary
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  SUMMARY" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Processed: $($stats.Processed)" -ForegroundColor White
    Write-Host "  Updated:   $($stats.Updated)" -ForegroundColor Green
    Write-Host "  Skipped:   $($stats.Skipped)" -ForegroundColor Gray
    Write-Host "  Errors:    $($stats.Errors)" -ForegroundColor $(if ($stats.Errors -gt 0) { 'Red' } else { 'Gray' })
    Write-Host "  Links added: $($stats.TotalLinksAdded)" -ForegroundColor Cyan

    if ($DryRun) {
        Write-Host "`n  [DRY RUN - No files were modified]" -ForegroundColor Yellow
    }

    # Detailed report
    if ($report.Count -gt 0) {
        Write-Host "`n========================================" -ForegroundColor Cyan
        Write-Host "  DETAILED REPORT" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan

        foreach ($item in $report) {
            Write-Host "`n  $($item.File)" -ForegroundColor White
            Write-Host "    + $($item.LinksAdded)" -ForegroundColor Green
        }
    }

    Write-Host "`n========================================`n" -ForegroundColor Cyan

    # Save report to file
    $reportPath = Join-Path $SkillPath "data\retro-linking-report.json"
    $reportData = @{
        timestamp = (Get-Date).ToString("o")
        dryRun = $DryRun.IsPresent
        stats = $stats
        details = $report
    }
    $reportData | ConvertTo-Json -Depth 5 | Out-File -FilePath $reportPath -Encoding UTF8
    Write-Host "Report saved: $reportPath" -ForegroundColor Gray

    return $stats
}

# Execute
Invoke-RetroLinking
