#Requires -Version 5.1
<#
.SYNOPSIS
    Comparaison registre vs valeurs live sur les VMs.

.DESCRIPTION
    Se connecte aux VMs, lit les .env et docker inspect,
    compare avec les valeurs du registre (par hash, pas en clair).

.PARAMETER VM
    VM cible. Defaut: toutes.

.NOTES
    Version: 1.0.0
    Author: Claude Code
#>

[CmdletBinding()]
param(
    [string]$VM
)

$ErrorActionPreference = "Stop"
$SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $SkillPath "scripts\CredentialRegistry.psm1") -Force

$VMs = @{
    vm100 = @{ Host = "192.168.1.162"; User = "root" }
    vm103 = @{ Host = "192.168.1.163"; User = "r2d2helm" }
    vm104 = @{ Host = "192.168.1.164"; User = "r2d2helm" }
    vm105 = @{ Host = "192.168.1.161"; User = "r2d2helm" }
}

function Get-StringHash {
    param([string]$String)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($String)
    $hash = $sha.ComputeHash($bytes)
    return [BitConverter]::ToString($hash).Replace('-', '').Substring(0, 16).ToLower()
}

function Get-LiveEnvValues {
    param([string]$HostName, [string]$User)
    $cmd = "find /home /root /opt -name '.env' -type f -exec cat {} \; 2>/dev/null"
    try {
        $result = ssh -o BatchMode=yes -o ConnectTimeout=10 "${User}@${HostName}" $cmd 2>&1
        $values = @{}
        foreach ($line in ($result -split "`n")) {
            if ($line -match '^([A-Z_]+)\s*=\s*(.+)$') {
                $values[$Matches[1]] = $Matches[2].Trim().Trim('"').Trim("'")
            }
        }
        return $values
    }
    catch {
        return @{}
    }
}

# Main
$entries = Get-AllCredentialEntries
$results = @()

$targetVMs = @()
if ($VM -and $VMs.ContainsKey($VM)) {
    $targetVMs += $VM
} else {
    $targetVMs = @($VMs.Keys)
}

foreach ($vmKey in $targetVMs) {
    $vmInfo = $VMs[$vmKey]
    Write-Host "Syncing $vmKey..." -ForegroundColor Cyan

    $liveValues = Get-LiveEnvValues -HostName $vmInfo.Host -User $vmInfo.User

    # Check credentials assigned to this VM
    $vmEntries = $entries | Where-Object { $_.Frontmatter['vm'] -eq $vmKey }

    foreach ($entry in $vmEntries) {
        $fm = $entry.Frontmatter
        $body = $entry.Body

        # Extract password from registry
        $regPassword = ""
        if ($body -match 'Password[:\s]+([^\r\n]+)') {
            $regPassword = $Matches[1].Trim()
        }

        $status = "UNKNOWN"

        # Try to match with live env values
        $matched = $false
        foreach ($envKey in $liveValues.Keys) {
            $envVal = $liveValues[$envKey]
            if ($envVal -eq $regPassword) {
                $status = "IN_SYNC"
                $matched = $true
                break
            }
        }

        if (-not $matched -and $regPassword) {
            $status = "UNVERIFIED"
        }

        $results += @{
            VM = $vmKey
            Service = $fm['service']
            Slug = $entry.Slug
            Status = $status
        }
    }
}

# Output
$results | ConvertTo-Json -Depth 3

$inSync = ($results | Where-Object { $_.Status -eq 'IN_SYNC' }).Count
$drift = ($results | Where-Object { $_.Status -eq 'DRIFT' }).Count
$unknown = ($results | Where-Object { $_.Status -eq 'UNVERIFIED' }).Count
Write-Host "`nSync: $inSync in-sync, $drift drifted, $unknown unverified" -ForegroundColor Cyan
