#Requires -Version 5.1
#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Enregistre les tâches planifiées pour Knowledge Watcher

.DESCRIPTION
    Crée les tâches Windows Task Scheduler pour les sources Tier 2-4.

.PARAMETER Unregister
    Supprimer les tâches au lieu de les créer

.EXAMPLE
    .\Register-WatcherTasks.ps1
    .\Register-WatcherTasks.ps1 -Unregister
#>

[CmdletBinding()]
param(
    [switch]$Unregister
)

$ErrorActionPreference = "Stop"

$SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $SkillPath "scripts\KnowledgeWatcher.psm1") -Force

$TaskPrefix = "KnowledgeWatcher"

# Compatible PowerShell 5.1 - no ?? operator
$pwshCmd = Get-Command pwsh -ErrorAction SilentlyContinue
if ($pwshCmd) {
    $PwshPath = $pwshCmd.Source
} else {
    $PwshPath = "powershell.exe"
}

function Register-KWScheduledTask {
    param(
        [string]$TaskName,
        [string]$Description,
        [string]$ScriptContent,
        $Trigger
    )

    # Supprimer si existe
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    # Créer le script temporaire
    $scriptPath = Join-Path $SkillPath "scripts\scheduled\$TaskName.ps1"
    $scriptDir = Split-Path -Parent $scriptPath
    if (-not (Test-Path $scriptDir)) {
        New-Item -ItemType Directory -Path $scriptDir -Force | Out-Null
    }
    Write-Utf8File -Path $scriptPath -Content $ScriptContent

    # Action
    $action = New-ScheduledTaskAction -Execute $PwshPath -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" -WorkingDirectory $SkillPath

    # Settings
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    # Principal (current user)
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType S4U -RunLevel Limited

    # Créer la tâche
    $task = New-ScheduledTask -Action $action -Trigger $Trigger -Settings $settings -Principal $principal -Description $Description

    Register-ScheduledTask -TaskName $TaskName -InputObject $task | Out-Null

    Write-Host "  [OK] $TaskName" -ForegroundColor Green
}

function Register-KWTasks {
    Write-Host "Registering Knowledge Watcher scheduled tasks..." -ForegroundColor Cyan
    Write-Host ""

    $config = Get-KWConfig

    # Tâche Tier 2 - Horaire
    $tier2Script = @'
$SkillPath = 'SKILLPATH_PLACEHOLDER'
Import-Module (Join-Path $SkillPath 'scripts\KnowledgeWatcher.psm1') -Force
. (Join-Path $SkillPath 'sources\GenericFileSource.ps1')

$sources = Get-KWSources | Where-Object { $_.tier -eq 2 -and $_.enabled }
foreach ($source in $sources) {
    Invoke-DirectoryScan -SourceConfig $source
}

$state = Get-KWState
$state.lastTier2Run = (Get-Date).ToString('o')
Save-KWState -State $state

& (Join-Path $SkillPath 'scripts\Invoke-QueueProcessor.ps1') -BatchSize 10
'@
    $tier2Script = $tier2Script -replace 'SKILLPATH_PLACEHOLDER', $SkillPath

    $tier2Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)
    Register-KWScheduledTask -TaskName "$TaskPrefix-Tier2-Hourly" -Description "Knowledge Watcher - Tier 2 sources (hourly scan)" -ScriptContent $tier2Script -Trigger $tier2Trigger

    # Tâche Tier 3 - Quotidienne à 6h
    $tier3Script = @'
$SkillPath = 'SKILLPATH_PLACEHOLDER'
Import-Module (Join-Path $SkillPath 'scripts\KnowledgeWatcher.psm1') -Force
. (Join-Path $SkillPath 'sources\GenericFileSource.ps1')
. (Join-Path $SkillPath 'sources\BrowserBookmarksSource.ps1')

$sources = Get-KWSources | Where-Object { $_.tier -eq 3 -and $_.enabled }
foreach ($source in $sources) {
    if ($source.type -eq 'directory') {
        Invoke-DirectoryScan -SourceConfig $source
    }
    elseif ($source.type -eq 'browser-bookmarks') {
        Invoke-BookmarksCapture
    }
}

$state = Get-KWState
$state.lastTier3Run = (Get-Date).ToString('o')
Save-KWState -State $state

& (Join-Path $SkillPath 'scripts\Invoke-QueueProcessor.ps1') -BatchSize 20
'@
    $tier3Script = $tier3Script -replace 'SKILLPATH_PLACEHOLDER', $SkillPath

    $tier3Trigger = New-ScheduledTaskTrigger -Daily -At "6:00 AM"
    Register-KWScheduledTask -TaskName "$TaskPrefix-Tier3-Daily" -Description "Knowledge Watcher - Tier 3 sources (daily at 6 AM)" -ScriptContent $tier3Script -Trigger $tier3Trigger

    # Tâche Tier 4 - Hebdomadaire dimanche 3h
    $tier4Script = @'
$SkillPath = 'SKILLPATH_PLACEHOLDER'
Import-Module (Join-Path $SkillPath 'scripts\KnowledgeWatcher.psm1') -Force
. (Join-Path $SkillPath 'sources\GenericFileSource.ps1')

$sources = Get-KWSources | Where-Object { $_.tier -eq 4 -and $_.enabled }
foreach ($source in $sources) {
    Invoke-DirectoryScan -SourceConfig $source
}

$state = Get-KWState
$state.lastTier4Run = (Get-Date).ToString('o')
Save-KWState -State $state

& (Join-Path $SkillPath 'scripts\Invoke-QueueProcessor.ps1') -BatchSize 50
'@
    $tier4Script = $tier4Script -replace 'SKILLPATH_PLACEHOLDER', $SkillPath

    $tier4Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "3:00 AM"
    Register-KWScheduledTask -TaskName "$TaskPrefix-Tier4-Weekly" -Description "Knowledge Watcher - Tier 4 sources (weekly on Sunday at 3 AM)" -ScriptContent $tier4Script -Trigger $tier4Trigger

    Write-Host ""
    Write-Host "[OK] Scheduled tasks registered" -ForegroundColor Green
    Write-Host ""
    Write-Host "   Tasks created:" -ForegroundColor White
    Write-Host "   - $TaskPrefix-Tier2-Hourly  : Every hour" -ForegroundColor Gray
    Write-Host "   - $TaskPrefix-Tier3-Daily   : Daily at 6:00 AM" -ForegroundColor Gray
    Write-Host "   - $TaskPrefix-Tier4-Weekly  : Sunday at 3:00 AM" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   Use Task Scheduler or 'Get-ScheduledTask -TaskName $TaskPrefix*' to manage" -ForegroundColor Gray
}

function Unregister-KWTasks {
    Write-Host "Unregistering Knowledge Watcher scheduled tasks..." -ForegroundColor Cyan
    Write-Host ""

    $tasks = Get-ScheduledTask -TaskName "$TaskPrefix*" -ErrorAction SilentlyContinue

    if (-not $tasks -or $tasks.Count -eq 0) {
        Write-Host "[INFO] No tasks found" -ForegroundColor Yellow
        return
    }

    foreach ($task in $tasks) {
        Unregister-ScheduledTask -TaskName $task.TaskName -Confirm:$false
        Write-Host "  [OK] Removed: $($task.TaskName)" -ForegroundColor Green
    }

    # Nettoyer les scripts
    $scheduledDir = Join-Path $SkillPath "scripts\scheduled"
    if (Test-Path $scheduledDir) {
        Remove-Item -Path $scheduledDir -Recurse -Force
    }

    Write-Host ""
    Write-Host "[OK] All scheduled tasks removed" -ForegroundColor Green
}

# Exécution
if ($Unregister) {
    Unregister-KWTasks
}
else {
    Register-KWTasks
}
