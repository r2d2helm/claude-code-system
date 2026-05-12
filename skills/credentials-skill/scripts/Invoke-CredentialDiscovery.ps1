#Requires -Version 5.1
<#
.SYNOPSIS
    Scan des VMs via SSH pour decouvrir des secrets non repertories.

.DESCRIPTION
    Se connecte aux VMs via SSH, recherche les fichiers .env,
    inspecte les containers Docker, et compare avec le registre.

.PARAMETER VM
    VM cible (vm100, vm103, vm104, vm105). Defaut: toutes.

.PARAMETER Deep
    Scan approfondi (inclut grep dans les fichiers de config).

.NOTES
    Version: 1.0.0
    Author: Claude Code
#>

[CmdletBinding()]
param(
    [string]$VM,
    [switch]$Deep
)

$ErrorActionPreference = "Stop"
$SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $SkillPath "scripts\CredentialRegistry.psm1") -Force

$VMs = @{
    vm100 = @{ Host = "192.168.1.162"; User = "root"; Name = "r2d2-stage" }
    vm103 = @{ Host = "192.168.1.163"; User = "r2d2helm"; Name = "r2d2-main" }
    vm104 = @{ Host = "192.168.1.164"; User = "r2d2helm"; Name = "r2d2-store" }
    vm105 = @{ Host = "192.168.1.161"; User = "r2d2helm"; Name = "r2d2-lab" }
}

function Invoke-SshCommand {
    param([string]$HostName, [string]$User, [string]$Command)
    try {
        $result = ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=no "${User}@${HostName}" $Command 2>&1
        return @{ Success = $true; Output = $result }
    }
    catch {
        return @{ Success = $false; Output = $_.Exception.Message }
    }
}

function Find-EnvFiles {
    param([string]$HostName, [string]$User)
    $cmd = "find /home -name '.env' -type f 2>/dev/null; find /root -name '.env' -type f 2>/dev/null; find /opt -name '.env' -type f 2>/dev/null"
    $result = Invoke-SshCommand -HostName $HostName -User $User -Command $cmd
    if ($result.Success) {
        return ($result.Output -split "`n" | Where-Object { $_ -ne '' })
    }
    return @()
}

function Parse-EnvFile {
    param([string]$HostName, [string]$User, [string]$FilePath)
    $cmd = "cat '$FilePath' 2>/dev/null"
    $result = Invoke-SshCommand -HostName $HostName -User $User -Command $cmd
    $secrets = @()
    if ($result.Success) {
        foreach ($line in ($result.Output -split "`n")) {
            if ($line -match '^([A-Z_]+PASSWORD|[A-Z_]+SECRET|[A-Z_]+TOKEN|[A-Z_]+KEY|[A-Z_]+API_KEY)\s*=\s*(.+)$') {
                $secrets += @{
                    Variable = $Matches[1]
                    File = $FilePath
                    HasValue = ($Matches[2].Trim() -ne '')
                }
            }
        }
    }
    return $secrets
}

function Get-DockerSecrets {
    param([string]$HostName, [string]$User)
    $cmd = "docker ps --format '{{.Names}}' 2>/dev/null"
    $result = Invoke-SshCommand -HostName $HostName -User $User -Command $cmd
    $secrets = @()
    if ($result.Success) {
        $containers = $result.Output -split "`n" | Where-Object { $_ -ne '' }
        foreach ($container in $containers) {
            $envCmd = "docker inspect --format '{{range .Config.Env}}{{println .}}{{end}}' '$container' 2>/dev/null"
            $envResult = Invoke-SshCommand -HostName $HostName -User $User -Command $envCmd
            if ($envResult.Success) {
                foreach ($line in ($envResult.Output -split "`n")) {
                    if ($line -match '^(.*PASSWORD|.*SECRET|.*TOKEN|.*API_KEY|.*PRIVATE_KEY)=(.+)$') {
                        $secrets += @{
                            Container = $container
                            Variable = $Matches[1]
                            HasValue = ($Matches[2].Trim() -ne '')
                        }
                    }
                }
            }
        }
    }
    return $secrets
}

# Main
$targetVMs = @()
if ($VM) {
    if ($VMs.ContainsKey($VM)) {
        $targetVMs += @{ Key = $VM; Value = $VMs[$VM] }
    } else {
        Write-Error "VM '$VM' not found. Available: $($VMs.Keys -join ', ')"
        return
    }
} else {
    foreach ($key in $VMs.Keys) {
        $targetVMs += @{ Key = $key; Value = $VMs[$key] }
    }
}

# Load existing registry for comparison
$existingEntries = Get-AllCredentialEntries
$existingSlugs = @($existingEntries | ForEach-Object { $_.Slug })

$allDiscoveries = @()

foreach ($vmEntry in $targetVMs) {
    $vmKey = $vmEntry.Key
    $vmInfo = $vmEntry.Value
    Write-Host "`nScanning $vmKey ($($vmInfo.Host))..." -ForegroundColor Cyan

    # Find .env files
    $envFiles = Find-EnvFiles -HostName $vmInfo.Host -User $vmInfo.User
    Write-Host "  Found $($envFiles.Count) .env files" -ForegroundColor Yellow

    foreach ($envFile in $envFiles) {
        $secrets = Parse-EnvFile -HostName $vmInfo.Host -User $vmInfo.User -FilePath $envFile
        foreach ($secret in $secrets) {
            $allDiscoveries += @{
                VM = $vmKey
                Source = ".env"
                SourcePath = $envFile
                Variable = $secret.Variable
                HasValue = $secret.HasValue
            }
        }
    }

    # Docker secrets
    $dockerSecrets = Get-DockerSecrets -HostName $vmInfo.Host -User $vmInfo.User
    Write-Host "  Found $($dockerSecrets.Count) Docker env secrets" -ForegroundColor Yellow

    foreach ($secret in $dockerSecrets) {
        $allDiscoveries += @{
            VM = $vmKey
            Source = "docker"
            SourcePath = $secret.Container
            Variable = $secret.Variable
            HasValue = $secret.HasValue
        }
    }
}

# Output results as JSON
Write-Host "`nTotal discoveries: $($allDiscoveries.Count)" -ForegroundColor Green
$allDiscoveries | ConvertTo-Json -Depth 3
