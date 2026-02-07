#Requires -Version 5.1
<#
.SYNOPSIS
    Vault Guardian - Maintenance proactive du vault Obsidian
.DESCRIPTION
    Script principal du Vault Guardian Agent.
    Effectue des health checks, auto-corrections et rapports.
.PARAMETER Mode
    Mode d'execution: health, fix, report, quick
#>

[CmdletBinding()]
param(
    [ValidateSet("health", "fix", "report", "quick")]
    [string]$Mode = "health"
)

$ErrorActionPreference = "Continue"

$VaultPath = 'C:\Users\r2d2\Documents\Knowledge'
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$Results = @{
    TotalFiles = 0
    EmptyFiles = @()
    NoFrontmatter = @()
    BrokenLinks = @()
    Orphans = @()
    StatusIssues = @()
    TagIssues = @()
    EmptyRelated = @()
    DuplicateBasenames = @()
    Score = 10.0
    Timestamp = (Get-Date).ToString("o")
}

function Get-AllNotes {
    return Get-ChildItem $VaultPath -Recurse -Filter '*.md' -File |
        Where-Object { $_.FullName -notmatch '[\\/]\.obsidian[\\/]' }
}

function Test-HasFrontmatter {
    param([string]$Content)
    return $Content -match '^---\s*\r?\n[\s\S]*?\r?\n---'
}

function Get-FrontmatterField {
    param([string]$Content, [string]$Field)
    if ($Content -match "(?m)^${Field}:\s*(.+)$") {
        return $Matches[1].Trim().Trim('"').Trim("'")
    }
    return $null
}

function Remove-CodeContent {
    param([string]$Text)
    $Text = [regex]::Replace($Text, '(?ms)```[^\n]*\n.*?```', '')
    $Text = [regex]::Replace($Text, '`[^`\r\n]+`', '')
    return $Text
}

function Invoke-HealthCheck {
    Write-Host "=== VAULT GUARDIAN - HEALTH CHECK ===" -ForegroundColor Cyan
    Write-Host ""

    $allNotes = Get-AllNotes
    $Results.TotalFiles = $allNotes.Count
    Write-Host "Total notes: $($allNotes.Count)"

    $noteNames = @{}
    foreach ($n in $allNotes) {
        $noteNames[$n.BaseName] = $n.FullName
    }

    $processed = 0
    foreach ($file in $allNotes) {
        $processed++
        if ($processed % 100 -eq 0) { Write-Host "  Scanning... $processed / $($allNotes.Count)" -ForegroundColor Gray }

        try {
            $content = [System.IO.File]::ReadAllText($file.FullName, $Utf8NoBom)
        } catch { continue }

        if ([string]::IsNullOrWhiteSpace($content)) {
            $Results.EmptyFiles += $file.FullName
            continue
        }

        if (-not (Test-HasFrontmatter $content)) {
            $Results.NoFrontmatter += $file.FullName
        }

        # Extract frontmatter block only for status/tags
        $fmBlock = ''
        if ($content -match '(?s)^---\r?\n(.*?)\r?\n---') { $fmBlock = $Matches[1] }

        $status = Get-FrontmatterField $fmBlock 'status'
        if ($status -eq 'captured') {
            $Results.StatusIssues += $file.FullName
        }

        if ($fmBlock -match '(?m)^tags:\s*\r?\n((?:\s*-\s*.+\r?\n?)*)') {
            $tagBlock = $Matches[1]
            foreach ($line in ($tagBlock -split '\r?\n')) {
                if ($line -match '^\s*-\s*(.+)$') {
                    $tag = $Matches[1].Trim().Trim('"').Trim("'")
                    if ($tag -cmatch '^[A-Z]' -or $tag -match '\s') {
                        $Results.TagIssues += @{ File = $file.FullName; Tag = $tag }
                    }
                }
            }
        }

        # Empty related field detection
        $hasValidRelated = $false
        if ($fmBlock -match '(?m)^related:') {
            if ($fmBlock -match '(?m)^related:\s*\[\s*\]\s*$') {
                $hasValidRelated = $false
            }
            elseif ($fmBlock -match '(?m)^related:\s*\r?\n((?:\s*-\s*.+\r?\n?)*)') {
                $relatedBlock = $Matches[1]
                if (-not [string]::IsNullOrWhiteSpace($relatedBlock)) {
                    $hasValidRelated = $true
                }
            }
            elseif ($fmBlock -match '(?m)^related:\s+\S') {
                $hasValidRelated = $true
            }
        }
        if (-not $hasValidRelated) {
            $Results.EmptyRelated += $file.FullName
        }

        $cleanContent = Remove-CodeContent $content
        $links = [regex]::Matches($cleanContent, '\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
        foreach ($link in $links) {
            $target = $link.Groups[1].Value
            if ($target -match '#') { $target = $target.Split('#')[0] }
            if ([string]::IsNullOrWhiteSpace($target)) { continue }
            if (-not $noteNames.ContainsKey($target)) {
                $Results.BrokenLinks += @{ Source = $file.FullName; Target = $target }
            }
        }
    }

    # Orphan detection
    $allLinkedNames = @{}
    foreach ($file in $allNotes) {
        try {
            $content = [System.IO.File]::ReadAllText($file.FullName, $Utf8NoBom)
            $cleanContent = Remove-CodeContent $content
            $links = [regex]::Matches($cleanContent, '\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
            foreach ($link in $links) {
                $target = $link.Groups[1].Value.Split('#')[0]
                if ($target) { $allLinkedNames[$target] = $true }
            }
        } catch { continue }
    }

    foreach ($file in $allNotes) {
        $bn = $file.BaseName
        $rel = $file.FullName.Substring($VaultPath.Length + 1)
        if ($rel -match '^_Index[\\/]|^_Templates[\\/]|^_Daily[\\/]') { continue }
        if (-not $allLinkedNames.ContainsKey($bn)) {
            $Results.Orphans += $file.FullName
        }
    }

    # Duplicate basename detection
    $basenameMap = @{}
    foreach ($file in $allNotes) {
        $bn = $file.BaseName
        if (-not $basenameMap.ContainsKey($bn)) {
            $basenameMap[$bn] = @()
        }
        $basenameMap[$bn] += $file.FullName
    }
    foreach ($bn in $basenameMap.Keys) {
        $paths = $basenameMap[$bn]
        if ($paths.Count -gt 1) {
            $Results.DuplicateBasenames += @{ BaseName = $bn; Paths = $paths }
        }
    }

    # Score
    $Results.Score = 10.0
    if ($Results.EmptyFiles.Count -gt 0) { $Results.Score -= [math]::Min(1.0, $Results.EmptyFiles.Count * 0.2) }
    if ($Results.NoFrontmatter.Count -gt 0) { $Results.Score -= [math]::Min(1.5, $Results.NoFrontmatter.Count * 0.02) }
    if ($Results.BrokenLinks.Count -gt 0) { $Results.Score -= [math]::Min(2.0, $Results.BrokenLinks.Count * 0.1) }
    if ($Results.Orphans.Count -gt 0) {
        $orphanRate = $Results.Orphans.Count / [math]::Max(1, $Results.TotalFiles)
        if ($orphanRate -gt 0.5) { $Results.Score -= 2.0 }
        elseif ($orphanRate -gt 0.3) { $Results.Score -= 1.0 }
        elseif ($orphanRate -gt 0.1) { $Results.Score -= 0.5 }
    }
    if ($Results.StatusIssues.Count -gt 0) { $Results.Score -= [math]::Min(0.5, $Results.StatusIssues.Count * 0.01) }
    if ($Results.TagIssues.Count -gt 0) { $Results.Score -= [math]::Min(0.5, $Results.TagIssues.Count * 0.05) }
    if ($Results.EmptyRelated.Count -gt 0) { $Results.Score -= [math]::Min(1.0, $Results.EmptyRelated.Count * 0.005) }
    if ($Results.DuplicateBasenames.Count -gt 0) { $Results.Score -= [math]::Min(0.5, $Results.DuplicateBasenames.Count * 0.02) }
    $Results.Score = [math]::Round([math]::Max(0, $Results.Score), 1)

    Write-Host ""
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "  SCORE DE SANTE: $($Results.Score) / 10" -ForegroundColor $(if ($Results.Score -ge 8) { 'Green' } elseif ($Results.Score -ge 6) { 'Yellow' } else { 'Red' })
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "  Total notes       : $($Results.TotalFiles)"
    Write-Host "  Notes vides       : $($Results.EmptyFiles.Count)" -ForegroundColor $(if ($Results.EmptyFiles.Count -eq 0) { 'Green' } else { 'Red' })
    Write-Host "  Sans frontmatter  : $($Results.NoFrontmatter.Count)" -ForegroundColor $(if ($Results.NoFrontmatter.Count -eq 0) { 'Green' } else { 'Yellow' })
    Write-Host "  Liens casses      : $($Results.BrokenLinks.Count)" -ForegroundColor $(if ($Results.BrokenLinks.Count -eq 0) { 'Green' } else { 'Red' })
    Write-Host "  Orphelines        : $($Results.Orphans.Count)" -ForegroundColor $(if ($Results.Orphans.Count -eq 0) { 'Green' } else { 'Yellow' })
    Write-Host "  Status non-standard: $($Results.StatusIssues.Count)" -ForegroundColor $(if ($Results.StatusIssues.Count -eq 0) { 'Green' } else { 'Yellow' })
    Write-Host "  Tags incorrects   : $($Results.TagIssues.Count)" -ForegroundColor $(if ($Results.TagIssues.Count -eq 0) { 'Green' } else { 'Yellow' })
    Write-Host "  Related vides     : $($Results.EmptyRelated.Count)" -ForegroundColor $(if ($Results.EmptyRelated.Count -eq 0) { 'Green' } else { 'Yellow' })
    Write-Host "  Doublons basename : $($Results.DuplicateBasenames.Count)" -ForegroundColor $(if ($Results.DuplicateBasenames.Count -eq 0) { 'Green' } else { 'Yellow' })
    Write-Host "============================================" -ForegroundColor Cyan

    if ($Results.BrokenLinks.Count -gt 0 -and $Results.BrokenLinks.Count -le 10) {
        Write-Host ""
        Write-Host "Liens casses:" -ForegroundColor Yellow
        foreach ($bl in $Results.BrokenLinks) {
            $src = $bl.Source.Substring($VaultPath.Length + 1)
            Write-Host "  $src -> [[$($bl.Target)]]" -ForegroundColor Gray
        }
    }

    return $Results
}

function Invoke-AutoFix {
    Write-Host "=== VAULT GUARDIAN - AUTO-FIX ===" -ForegroundColor Cyan
    $health = Invoke-HealthCheck
    $fixed = 0

    if ($health.EmptyFiles.Count -gt 0) {
        Write-Host ""
        Write-Host "Fixing: $($health.EmptyFiles.Count) empty files..." -ForegroundColor Yellow
        foreach ($f in $health.EmptyFiles) {
            Remove-Item $f -Force -ErrorAction SilentlyContinue
            $fixed++
        }
        Write-Host "  Deleted $($health.EmptyFiles.Count) empty files" -ForegroundColor Green
    }

    if ($health.StatusIssues.Count -gt 0) {
        Write-Host ""
        Write-Host "Fixing: $($health.StatusIssues.Count) non-standard status..." -ForegroundColor Yellow
        $statusFixed = 0
        foreach ($f in $health.StatusIssues) {
            try {
                $content = [System.IO.File]::ReadAllText($f, $Utf8NoBom)
                $newContent = $content -replace '(?m)^(status:\s*)captured(\s*)$', '${1}seedling${2}'
                if ($newContent -ne $content) {
                    [System.IO.File]::WriteAllText($f, $newContent, $Utf8NoBom)
                    $statusFixed++
                }
            } catch { continue }
        }
        Write-Host "  Fixed $statusFixed status fields" -ForegroundColor Green
        $fixed += $statusFixed
    }

    Write-Host ""
    Write-Host "Total fixes applied: $fixed" -ForegroundColor Green
    return $fixed
}

function Invoke-QuickCheck {
    Write-Host "=== VAULT GUARDIAN - QUICK CHECK ===" -ForegroundColor Cyan
    $allNotes = Get-AllNotes
    $empty = 0
    $broken = 0

    $noteNames = @{}
    foreach ($n in $allNotes) { $noteNames[$n.BaseName] = $true }

    foreach ($file in $allNotes) {
        try {
            $content = [System.IO.File]::ReadAllText($file.FullName, $Utf8NoBom)
        } catch { continue }

        if ([string]::IsNullOrWhiteSpace($content)) { $empty++; continue }

        $cleanContent = Remove-CodeContent $content
        $links = [regex]::Matches($cleanContent, '\[\[([^\]|#]+)')
        foreach ($link in $links) {
            $target = $link.Groups[1].Value
            if (-not $noteNames.ContainsKey($target)) { $broken++ }
        }
    }

    $status = if ($empty -eq 0 -and $broken -eq 0) { "OK" } else { "ISSUES" }
    Write-Host "  Notes: $($allNotes.Count) | Empty: $empty | Broken links: $broken | Status: $status"
    return @{ Notes = $allNotes.Count; Empty = $empty; BrokenLinks = $broken }
}

switch ($Mode) {
    "health" { Invoke-HealthCheck }
    "fix"    { Invoke-AutoFix }
    "report" {
        $health = Invoke-HealthCheck
        Write-Host ""
        Write-Host "=== RECOMMENDATIONS ===" -ForegroundColor Cyan
        if ($health.BrokenLinks.Count -gt 0) { Write-Host "  - Corriger $($health.BrokenLinks.Count) liens casses" }
        if ($health.NoFrontmatter.Count -gt 0) { Write-Host "  - Ajouter frontmatter a $($health.NoFrontmatter.Count) fichiers" }
        if ($health.Orphans.Count -gt 0) { Write-Host "  - Connecter $($health.Orphans.Count) notes orphelines" }
        if ($health.EmptyRelated.Count -gt 0) { Write-Host "  - Ajouter des related a $($health.EmptyRelated.Count) notes" }
        if ($health.DuplicateBasenames.Count -gt 0) { Write-Host "  - Resoudre $($health.DuplicateBasenames.Count) doublons de basename" }
        if ($health.Score -ge 9) { Write-Host "  Le vault est en excellent etat!" -ForegroundColor Green }

        # Generate health report JSON
        $dataDir = 'C:\Users\r2d2\.claude\skills\vault-guardian-skill\data'
        if (-not (Test-Path $dataDir)) {
            New-Item -Path $dataDir -ItemType Directory -Force | Out-Null
        }
        $reportDate = (Get-Date).ToString("yyyy-MM-dd")
        $reportPath = Join-Path $dataDir "health-$reportDate.json"

        $reportObj = @{
            Timestamp = $health.Timestamp
            Score = $health.Score
            TotalFiles = $health.TotalFiles
            EmptyFiles = $health.EmptyFiles.Count
            NoFrontmatter = $health.NoFrontmatter.Count
            BrokenLinks = $health.BrokenLinks.Count
            Orphans = $health.Orphans.Count
            StatusIssues = $health.StatusIssues.Count
            TagIssues = $health.TagIssues.Count
            EmptyRelated = $health.EmptyRelated.Count
            DuplicateBasenames = $health.DuplicateBasenames.Count
        }

        $jsonContent = $reportObj | ConvertTo-Json -Depth 4
        [System.IO.File]::WriteAllText($reportPath, $jsonContent, $Utf8NoBom)
        Write-Host ""
        Write-Host "  Rapport JSON sauvegarde: $reportPath" -ForegroundColor Green
    }
    "quick"  { Invoke-QuickCheck }
}
