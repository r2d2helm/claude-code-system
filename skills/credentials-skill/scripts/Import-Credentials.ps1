#Requires -Version 5.1
<#
.SYNOPSIS
    Import de credentials depuis Bitwarden CSV, KeePass, texte, ou docker-compose.

.PARAMETER Source
    Chemin du fichier source.

.PARAMETER Format
    Format du fichier : auto, bitwarden, env, markdown, compose

.NOTES
    Version: 1.0.0
    Author: Claude Code
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$Source,
    [ValidateSet('auto', 'bitwarden', 'env', 'markdown', 'compose')]
    [string]$Format = "auto"
)

$ErrorActionPreference = "Stop"
$SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $SkillPath "scripts\CredentialRegistry.psm1") -Force

if (-not (Test-Path $Source)) {
    Write-Error "Source file not found: $Source"
    return
}

$content = [System.IO.File]::ReadAllText($Source, [System.Text.Encoding]::UTF8)

# Auto-detect format
if ($Format -eq 'auto') {
    $ext = [System.IO.Path]::GetExtension($Source).ToLower()
    $Format = switch ($ext) {
        '.csv' { 'bitwarden' }
        '.env' { 'env' }
        '.md' { 'markdown' }
        '.yml' { 'compose' }
        '.yaml' { 'compose' }
        default { 'markdown' }
    }
    Write-Host "Auto-detected format: $Format" -ForegroundColor Cyan
}

$imported = @()
$skipped = @()
$errors = @()

switch ($Format) {
    'bitwarden' {
        $lines = $content -split "`n"
        # Skip header
        for ($i = 1; $i -lt $lines.Count; $i++) {
            $line = $lines[$i].Trim()
            if ($line -eq '') { continue }
            $cols = $line -split ','
            if ($cols.Count -ge 10) {
                $name = $cols[3]
                $slug = ($name -replace '[^a-zA-Z0-9]', '-').ToLower().Trim('-')
                $existing = Get-CredentialEntry -Slug $slug -ErrorAction SilentlyContinue
                if ($existing) {
                    $skipped += $slug
                    continue
                }
                $fm = @{
                    service = $name
                    slug = $slug
                    category = "web"
                    host = ""
                    port = ""
                    protocol = "https"
                    vm = ""
                    criticality = "medium"
                    auth_type = "password"
                    created = Get-Timestamp
                    last_rotated = Get-Timestamp
                    rotation_interval_days = 90
                    last_validated = $null
                    validation_status = "untested"
                    tags = @()
                }
                $body = "# $name`n`n## Access`n- **URL**: $($cols[7])`n- **Username**: $($cols[8])`n- **Password**: $($cols[9])"
                Set-CredentialEntry -Slug $slug -Frontmatter $fm -Body $body
                $imported += $slug
            }
        }
    }

    'env' {
        foreach ($line in ($content -split "`n")) {
            if ($line -match '^([A-Z_]+(?:PASSWORD|SECRET|TOKEN|KEY|API_KEY))\s*=\s*(.+)$') {
                $varName = $Matches[1]
                $value = $Matches[2].Trim().Trim('"').Trim("'")
                $slug = ($varName -replace '_', '-').ToLower()
                $existing = Get-CredentialEntry -Slug $slug -ErrorAction SilentlyContinue
                if ($existing) {
                    $skipped += $slug
                    continue
                }
                $fm = @{
                    service = $varName
                    slug = $slug
                    category = "infra"
                    host = ""
                    port = ""
                    protocol = ""
                    vm = ""
                    criticality = "medium"
                    auth_type = "password"
                    created = Get-Timestamp
                    last_rotated = Get-Timestamp
                    rotation_interval_days = 90
                    last_validated = $null
                    validation_status = "untested"
                    tags = @("imported", "env")
                }
                $body = "# $varName`n`n## Access`n- **Variable**: $varName`n- **Password**: $value"
                Set-CredentialEntry -Slug $slug -Frontmatter $fm -Body $body
                $imported += $slug
            }
        }
    }

    'markdown' {
        Write-Host "Markdown import delegates to wizard-setup for vm100-credentials.md parsing" -ForegroundColor Yellow
        Write-Host "Use: /cred-wizard setup" -ForegroundColor Yellow
    }

    'compose' {
        if ($content -match 'environment:') {
            $envBlock = $false
            foreach ($line in ($content -split "`n")) {
                if ($line -match '^\s+environment:') { $envBlock = $true; continue }
                if ($envBlock -and $line -match '^\s+-\s+(\w+(?:PASSWORD|SECRET|TOKEN|KEY))=(.+)') {
                    $varName = $Matches[1]
                    $value = $Matches[2].Trim()
                    $slug = ($varName -replace '_', '-').ToLower()
                    $existing = Get-CredentialEntry -Slug $slug -ErrorAction SilentlyContinue
                    if ($existing) { $skipped += $slug; continue }
                    $fm = @{
                        service = $varName
                        slug = $slug
                        category = "infra"
                        host = ""; port = ""; protocol = ""; vm = ""
                        criticality = "medium"
                        auth_type = "password"
                        created = Get-Timestamp
                        last_rotated = Get-Timestamp
                        rotation_interval_days = 90
                        last_validated = $null
                        validation_status = "untested"
                        tags = @("imported", "compose")
                    }
                    $body = "# $varName`n`n## Access`n- **Variable**: $varName`n- **Password**: $value"
                    Set-CredentialEntry -Slug $slug -Frontmatter $fm -Body $body
                    $imported += $slug
                }
                if ($envBlock -and $line -match '^\s+\w+:' -and $line -notmatch '^\s+-') { $envBlock = $false }
            }
        }
    }
}

# Update index
Update-CredentialIndex | Out-Null

# Summary
Write-Host "`nImport Summary:" -ForegroundColor Cyan
Write-Host "  Imported: $($imported.Count)" -ForegroundColor Green
Write-Host "  Skipped: $($skipped.Count)" -ForegroundColor Yellow
Write-Host "  Errors: $($errors.Count)" -ForegroundColor Red
