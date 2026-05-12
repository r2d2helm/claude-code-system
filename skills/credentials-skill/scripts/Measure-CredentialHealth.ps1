#Requires -Version 5.1
<#
.SYNOPSIS
    Score de sante des credentials : age, force, couverture, fraicheur.

.DESCRIPTION
    Calcule un score /100 reparti en 4 axes de 25 points chacun.

.NOTES
    Version: 1.0.0
    Author: Claude Code
#>

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $SkillPath "scripts\CredentialRegistry.psm1") -Force

$today = Get-Date

function Measure-AgeScore {
    param([array]$Entries)
    $maxScore = 25
    if ($Entries.Count -eq 0) { return 0 }

    $totalPenalty = 0
    foreach ($entry in $Entries) {
        $fm = $entry.Frontmatter
        $lastRotated = $fm['last_rotated']
        $interval = $fm['rotation_interval_days']
        if (-not $interval) { $interval = 90 }

        if ($lastRotated) {
            try {
                $rotateDate = [datetime]::ParseExact($lastRotated, "yyyy-MM-dd", $null)
                $ageDays = ($today - $rotateDate).Days
                if ($ageDays -gt $interval) {
                    $overdue = $ageDays - $interval
                    $penalty = [math]::Min(($overdue / $interval), 1.0)
                    $totalPenalty += $penalty
                }
            }
            catch {
                $totalPenalty += 1.0
            }
        }
        else {
            $totalPenalty += 1.0
        }
    }

    $avgPenalty = $totalPenalty / $Entries.Count
    $score = [math]::Round($maxScore * (1 - $avgPenalty), 1)
    return [math]::Max(0, $score)
}

function Measure-StrengthScore {
    param([array]$Entries)
    $maxScore = 25
    if ($Entries.Count -eq 0) { return 0 }

    $totalStrength = 0
    foreach ($entry in $Entries) {
        $fm = $entry.Frontmatter
        $authType = $fm['auth_type']

        # SSH keys and tokens get full marks
        if ($authType -in @('ssh-key', 'token', 'apikey', 'jwt', 'oauth')) {
            $totalStrength += 1.0
            continue
        }

        # For passwords, estimate strength from body
        $body = $entry.Body
        if ($body -match 'Password[:\s]*\*?\*?\s*([^\r\n]+)') {
            $pwd = $Matches[1].Trim()
            $strength = 0.0
            if ($pwd.Length -ge 8) { $strength += 0.25 }
            if ($pwd.Length -ge 16) { $strength += 0.25 }
            if ($pwd -cmatch '[A-Z]' -and $pwd -cmatch '[a-z]') { $strength += 0.25 }
            if ($pwd -match '[^a-zA-Z0-9]') { $strength += 0.25 }
            $totalStrength += $strength
        }
        else {
            $totalStrength += 0.5 # Unknown, assume average
        }
    }

    $avgStrength = $totalStrength / $Entries.Count
    return [math]::Round($maxScore * $avgStrength, 1)
}

function Measure-CoverageScore {
    param([array]$Entries)
    $maxScore = 25
    # Estimated total services in the homelab
    $knownServices = 16
    $coverage = [math]::Min($Entries.Count / $knownServices, 1.0)
    return [math]::Round($maxScore * $coverage, 1)
}

function Measure-FreshnessScore {
    param([array]$Entries)
    $maxScore = 25
    if ($Entries.Count -eq 0) { return 0 }

    $fresh = 0
    foreach ($entry in $Entries) {
        $fm = $entry.Frontmatter
        $lastValidated = $fm['last_validated']
        $status = $fm['validation_status']

        if ($status -eq 'ok' -and $lastValidated) {
            try {
                $valDate = [datetime]::ParseExact($lastValidated, "yyyy-MM-dd", $null)
                $ageDays = ($today - $valDate).Days
                if ($ageDays -le 7) { $fresh++ }
            }
            catch { }
        }
    }

    $freshRatio = $fresh / $Entries.Count
    return [math]::Round($maxScore * $freshRatio, 1)
}

# Main
$entries = Get-AllCredentialEntries

$ageScore = Measure-AgeScore -Entries $entries
$strengthScore = Measure-StrengthScore -Entries $entries
$coverageScore = Measure-CoverageScore -Entries $entries
$freshnessScore = Measure-FreshnessScore -Entries $entries
$totalScore = $ageScore + $strengthScore + $coverageScore + $freshnessScore

# Build recommendations
$recommendations = @()
foreach ($entry in $entries) {
    $fm = $entry.Frontmatter
    $lastRotated = $fm['last_rotated']
    $interval = if ($fm['rotation_interval_days']) { $fm['rotation_interval_days'] } else { 90 }

    if ($lastRotated) {
        try {
            $rotateDate = [datetime]::ParseExact($lastRotated, "yyyy-MM-dd", $null)
            $ageDays = ($today - $rotateDate).Days
            if ($ageDays -gt $interval) {
                $recommendations += @{
                    Priority = "CRITICAL"
                    Slug = $entry.Slug
                    Message = "Rotation overdue by $($ageDays - $interval) days"
                }
            }
        }
        catch { }
    }

    if ($fm['validation_status'] -eq 'untested') {
        $recommendations += @{
            Priority = "HIGH"
            Slug = $entry.Slug
            Message = "Never validated"
        }
    }
    elseif ($fm['validation_status'] -eq 'failed') {
        $recommendations += @{
            Priority = "CRITICAL"
            Slug = $entry.Slug
            Message = "Last validation failed"
        }
    }
}

# Save to audit history
$auditHistoryPath = Join-Path $SkillPath "data\audit-history.json"
$auditEntry = @{
    date = Get-Timestamp
    total_score = $totalScore
    age_score = $ageScore
    strength_score = $strengthScore
    coverage_score = $coverageScore
    freshness_score = $freshnessScore
    entry_count = $entries.Count
    recommendations_count = $recommendations.Count
}

$history = @{ version = "1.0.0"; audits = @() }
if (Test-Path $auditHistoryPath) {
    try {
        $existing = Get-Content $auditHistoryPath -Raw | ConvertFrom-Json
        if ($existing.audits) {
            $history.audits = @($existing.audits)
        }
    }
    catch { }
}
$history.audits += $auditEntry
$historyJson = $history | ConvertTo-Json -Depth 5
Write-Utf8File -Path $auditHistoryPath -Content $historyJson

# Output
$output = @{
    total_score = $totalScore
    age = $ageScore
    strength = $strengthScore
    coverage = $coverageScore
    freshness = $freshnessScore
    entry_count = $entries.Count
    recommendations = $recommendations
}

$output | ConvertTo-Json -Depth 5
Write-Host "`nHealth Score: $totalScore/100" -ForegroundColor $(if ($totalScore -ge 70) { 'Green' } elseif ($totalScore -ge 40) { 'Yellow' } else { 'Red' })
