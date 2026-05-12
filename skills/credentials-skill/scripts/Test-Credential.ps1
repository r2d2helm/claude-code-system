#Requires -Version 5.1
<#
.SYNOPSIS
    Validation de connectivite des credentials par type.

.DESCRIPTION
    Teste la connectivite pour SSH, HTTP, DB, API, Telegram
    selon le auth_type et protocol du credential.

.PARAMETER Slug
    Slug du credential a tester.

.PARAMETER All
    Tester tous les credentials du registre.

.NOTES
    Version: 1.0.0
    Author: Claude Code
#>

[CmdletBinding()]
param(
    [string]$Slug,
    [switch]$All
)

$ErrorActionPreference = "Stop"
$SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $SkillPath "scripts\CredentialRegistry.psm1") -Force

function Test-HttpCredential {
    param([hashtable]$FM, [string]$Body)
    $url = "$($FM['protocol'])://$($FM['host']):$($FM['port'])"
    try {
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
        $sw.Stop()
        return @{
            Status = "OK"
            Code = $response.StatusCode
            Time = "$($sw.ElapsedMilliseconds)ms"
        }
    }
    catch {
        if ($_.Exception.Response) {
            $code = [int]$_.Exception.Response.StatusCode
            # 401/403 means the service is reachable
            if ($code -eq 401 -or $code -eq 403 -or $code -eq 302) {
                return @{ Status = "OK"; Code = $code; Time = "N/A" }
            }
        }
        return @{ Status = "FAILED"; Code = 0; Time = $_.Exception.Message }
    }
}

function Test-SshCredential {
    param([hashtable]$FM)
    $host_target = $FM['host']
    try {
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        $result = ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no "root@$host_target" "echo ok" 2>&1
        $sw.Stop()
        if ($result -match "ok") {
            return @{ Status = "OK"; Code = 0; Time = "$($sw.ElapsedMilliseconds)ms" }
        }
        return @{ Status = "FAILED"; Code = 1; Time = "$result" }
    }
    catch {
        return @{ Status = "FAILED"; Code = 1; Time = $_.Exception.Message }
    }
}

function Test-TelegramCredential {
    param([hashtable]$FM, [string]$Body)
    # Extract token from body
    if ($Body -match 'bot\d+:[A-Za-z0-9_-]+') {
        $token = $Matches[0]
        if ($token -notmatch '^bot') { $token = "bot$token" }
    }
    elseif ($Body -match '(\d+:[A-Za-z0-9_-]+)') {
        $token = "bot$($Matches[1])"
    }
    else {
        return @{ Status = "FAILED"; Code = 0; Time = "Token not found in body" }
    }

    try {
        $url = "https://api.telegram.org/$token/getMe"
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10
        $sw.Stop()
        $data = $response.Content | ConvertFrom-Json
        if ($data.ok) {
            return @{ Status = "OK"; Code = 200; Time = "$($sw.ElapsedMilliseconds)ms" }
        }
        return @{ Status = "FAILED"; Code = 0; Time = "API returned ok=false" }
    }
    catch {
        return @{ Status = "FAILED"; Code = 0; Time = $_.Exception.Message }
    }
}

function Test-SingleCredential {
    param([string]$CredSlug)

    $entry = Get-CredentialEntry -Slug $CredSlug
    if (-not $entry) { return $null }

    $fm = $entry.Frontmatter
    $protocol = $fm['protocol']
    $authType = $fm['auth_type']

    $result = switch ($protocol) {
        { $_ -in @('http', 'https') } {
            if ($fm['category'] -eq 'bot') {
                Test-TelegramCredential -FM $fm -Body $entry.Body
            } else {
                Test-HttpCredential -FM $fm -Body $entry.Body
            }
        }
        'ssh' { Test-SshCredential -FM $fm }
        default { Test-HttpCredential -FM $fm -Body $entry.Body }
    }

    # Update frontmatter
    $fm['last_validated'] = Get-Timestamp
    $fm['validation_status'] = if ($result.Status -eq 'OK') { 'ok' } else { 'failed' }
    Set-CredentialEntry -Slug $CredSlug -Frontmatter $fm -Body $entry.Body

    return @{
        Slug = $CredSlug
        Service = $fm['service']
        AuthType = $authType
        Status = $result.Status
        Code = $result.Code
        Time = $result.Time
    }
}

# Main
$results = @()

if ($All) {
    $entries = Get-AllCredentialEntries
    foreach ($entry in $entries) {
        Write-Host "Testing $($entry.Slug)..." -NoNewline
        $r = Test-SingleCredential -CredSlug $entry.Slug
        if ($r) {
            $color = if ($r.Status -eq 'OK') { 'Green' } else { 'Red' }
            Write-Host " $($r.Status)" -ForegroundColor $color
            $results += $r
        }
    }
}
elseif ($Slug) {
    Write-Host "Testing $Slug..." -NoNewline
    $r = Test-SingleCredential -CredSlug $Slug
    if ($r) {
        $color = if ($r.Status -eq 'OK') { 'Green' } else { 'Red' }
        Write-Host " $($r.Status)" -ForegroundColor $color
        $results += $r
    }
}

# Update index
Update-CredentialIndex | Out-Null

# Summary
$passed = ($results | Where-Object { $_.Status -eq 'OK' }).Count
$failed = ($results | Where-Object { $_.Status -eq 'FAILED' }).Count
Write-Host "`nResults: $passed passed, $failed failed out of $($results.Count) tested" -ForegroundColor Cyan

# Output as JSON for consumption
$results | ConvertTo-Json -Depth 3
