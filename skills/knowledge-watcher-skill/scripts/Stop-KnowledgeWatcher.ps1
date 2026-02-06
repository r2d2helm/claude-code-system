#Requires -Version 5.1
<#
.SYNOPSIS
    Arrête le Knowledge Watcher Agent

.DESCRIPTION
    Arrête proprement les watchers en cours d'exécution.

.EXAMPLE
    .\Stop-KnowledgeWatcher.ps1
#>

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $SkillPath "scripts\KnowledgeWatcher.psm1") -Force

function Stop-Watchers {
    $state = Get-KWState

    if (-not $state.watchersPid) {
        Write-Host "ℹ️  Knowledge Watcher is not running" -ForegroundColor Yellow
        return
    }

    $pid = $state.watchersPid

    try {
        $process = Get-Process -Id $pid -ErrorAction SilentlyContinue

        if ($process) {
            Write-Host "⏹️  Stopping Knowledge Watcher (PID: $pid)..." -ForegroundColor Cyan

            # Envoyer signal d'arrêt gracieux
            $process.CloseMainWindow() | Out-Null
            Start-Sleep -Seconds 2

            # Forcer si nécessaire
            if (-not $process.HasExited) {
                $process.Kill()
                Start-Sleep -Milliseconds 500
            }

            Write-Host "✅ Knowledge Watcher stopped" -ForegroundColor Green
            Write-KWLog -Message "Knowledge Watcher stopped via Stop-KnowledgeWatcher" -Level "INFO"
        }
        else {
            Write-Host "ℹ️  Process $pid not found (already stopped?)" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "⚠️  Error stopping process: $_" -ForegroundColor Yellow
    }

    # Nettoyer l'état
    $state.watchersPid = $null
    $state.watchersStarted = $null
    Save-KWState -State $state

    # Arrêter aussi les jobs PowerShell liés
    $jobs = Get-Job | Where-Object { $_.Command -like "*KnowledgeWatcher*" }
    if ($jobs) {
        Write-Host "   Stopping $($jobs.Count) background job(s)..." -ForegroundColor Gray
        $jobs | Stop-Job -PassThru | Remove-Job
    }

    # Nettoyer les événements enregistrés
    $events = Get-EventSubscriber | Where-Object { $_.SourceIdentifier -like "*FileSystemWatcher*" }
    if ($events) {
        Write-Host "   Unregistering $($events.Count) event(s)..." -ForegroundColor Gray
        $events | Unregister-Event
    }
}

Stop-Watchers
