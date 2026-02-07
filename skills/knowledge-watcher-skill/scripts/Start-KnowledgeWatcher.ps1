#Requires -Version 5.1
<#
.SYNOPSIS
    Démarre le Knowledge Watcher Agent

.DESCRIPTION
    Initialise et démarre les FileSystemWatchers pour les sources Tier 1
    et le processeur de queue en arrière-plan.

.PARAMETER Background
    Exécuter en mode background (job)

.EXAMPLE
    .\Start-KnowledgeWatcher.ps1
    .\Start-KnowledgeWatcher.ps1 -Background
#>

[CmdletBinding()]
param(
    [switch]$Background
)

$ErrorActionPreference = "Stop"

$SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $SkillPath "scripts\KnowledgeWatcher.psm1") -Force

# Importer les sources
. (Join-Path $SkillPath "sources\GenericFileSource.ps1")
. (Join-Path $SkillPath "sources\ClaudeHistorySource.ps1")

function Start-Watchers {
    <#
    .SYNOPSIS
        Démarre tous les FileSystemWatchers pour Tier 1
    #>

    $config = Get-KWConfig
    $sources = Get-KWSources
    $state = Get-KWState

    # Vérifier si déjà en cours
    if ($state.watchersPid) {
        try {
            $process = Get-Process -Id $state.watchersPid -ErrorAction SilentlyContinue
            if ($process) {
                Write-Host "⚠️  Knowledge Watcher already running (PID: $($state.watchersPid))" -ForegroundColor Yellow
                return
            }
        }
        catch { }
    }

    Write-Host "🚀 Starting Knowledge Watcher..." -ForegroundColor Cyan

    # Créer les watchers pour les sources Tier 1
    $watchers = @()
    $tier1Sources = $sources | Where-Object { $_.tier -eq 1 -and $_.enabled -and $_.type -eq "directory" }

    foreach ($source in $tier1Sources) {
        if (-not (Test-Path $source.path)) {
            Write-KWLog -Message "Source path not found: $($source.path)" -Level "WARN"
            Write-Host "  ⚠️  Skipping $($source.name) - path not found" -ForegroundColor Yellow
            continue
        }

        try {
            $watcher = [System.IO.FileSystemWatcher]::new()
            $watcher.Path = $source.path
            $watcher.IncludeSubdirectories = if ($null -ne $source.recursive) { $source.recursive } else { $false }
            $watcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite -bor
            [System.IO.NotifyFilters]::FileName -bor
            [System.IO.NotifyFilters]::DirectoryName
            $watcher.EnableRaisingEvents = $false  # Activé après configuration

            # Filter par patterns si spécifié
            if ($source.patterns -and $source.patterns.Count -eq 1) {
                $watcher.Filter = $source.patterns[0]
            }

            # Event handler pour Changed
            $sourceId = $source.id
            $debounceMs = if ($config.watchers.debounceMs) { $config.watchers.debounceMs } else { 1000 }

            $changedAction = {
                $path = $Event.SourceEventArgs.FullPath
                $changeType = $Event.SourceEventArgs.ChangeType

                # Debounce using configured value
                $debounce = if ($Event.MessageData.DebounceMs) { $Event.MessageData.DebounceMs } else { 2000 }
                Start-Sleep -Milliseconds $debounce

                # Skip if file no longer exists (was temporary)
                if (-not (Test-Path $path)) { return }

                # Skip ignored patterns
                $fileName = [System.IO.Path]::GetFileName($path)
                if ($fileName -match '^\~\$|\.tmp$|\.bak$') { return }

                try {
                    . (Join-Path $Event.MessageData.SkillPath "sources\GenericFileSource.ps1")
                    Import-Module (Join-Path $Event.MessageData.SkillPath "scripts\KnowledgeWatcher.psm1") -Force

                    Invoke-GenericFileCapture -Path $path -ChangeType $changeType.ToString()
                }
                catch {
                    Write-KWLog -Message "Watcher error for $path : $_" -Level "ERROR"
                }
            }

            $messageData = @{ SkillPath = $SkillPath; SourceId = $sourceId; DebounceMs = $debounceMs }

            Register-ObjectEvent -InputObject $watcher -EventName Changed -Action $changedAction -MessageData $messageData | Out-Null
            Register-ObjectEvent -InputObject $watcher -EventName Created -Action $changedAction -MessageData $messageData | Out-Null

            # Handler spécial pour Renamed (capture les fichiers créés via temp→rename)
            $renamedAction = {
                $newPath = $Event.SourceEventArgs.FullPath
                $oldPath = $Event.SourceEventArgs.OldFullPath

                $debounce = if ($Event.MessageData.DebounceMs) { $Event.MessageData.DebounceMs } else { 2000 }
                Start-Sleep -Milliseconds $debounce

                if (-not (Test-Path $newPath)) { return }

                $fileName = [System.IO.Path]::GetFileName($newPath)
                if ($fileName -match '^\~\$|\.tmp$|\.bak$') { return }

                try {
                    . (Join-Path $Event.MessageData.SkillPath "sources\GenericFileSource.ps1")
                    Import-Module (Join-Path $Event.MessageData.SkillPath "scripts\KnowledgeWatcher.psm1") -Force

                    Invoke-GenericFileCapture -Path $newPath -ChangeType "Renamed"
                    Write-KWLog -Message "Renamed: $oldPath -> $newPath" -Level "DEBUG"
                }
                catch {
                    Write-KWLog -Message "Watcher rename error for $newPath : $_" -Level "ERROR"
                }
            }

            Register-ObjectEvent -InputObject $watcher -EventName Renamed -Action $renamedAction -MessageData $messageData | Out-Null

            $watcher.EnableRaisingEvents = $true
            $watchers += $watcher

            Write-Host "  ✅ Watching: $($source.name) ($($source.path))" -ForegroundColor Green
            Write-KWLog -Message "Started watcher for: $($source.name)" -Level "INFO"
        }
        catch {
            Write-Host "  ❌ Failed to create watcher for $($source.name): $_" -ForegroundColor Red
            Write-KWLog -Message "Failed to create watcher for $($source.name): $_" -Level "ERROR"
        }
    }

    # Watcher spécial pour Claude history
    $claudeSource = $sources | Where-Object { $_.id -eq "claude-history" -and $_.enabled }
    if ($claudeSource) {
        $historyDir = Split-Path -Parent $claudeSource.path

        if (Test-Path $historyDir) {
            try {
                $historyWatcher = [System.IO.FileSystemWatcher]::new()
                $historyWatcher.Path = $historyDir
                $historyWatcher.Filter = "*.jsonl"
                $historyWatcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite
                $historyWatcher.EnableRaisingEvents = $false

                $historyAction = {
                    Start-Sleep -Milliseconds 2000  # Plus de délai pour Claude history

                    try {
                        . (Join-Path $Event.MessageData.SkillPath "sources\ClaudeHistorySource.ps1")
                        Import-Module (Join-Path $Event.MessageData.SkillPath "scripts\KnowledgeWatcher.psm1") -Force

                        Invoke-ClaudeHistoryCapture
                    }
                    catch {
                        Write-KWLog -Message "Claude history watcher error: $_" -Level "ERROR"
                    }
                }

                Register-ObjectEvent -InputObject $historyWatcher -EventName Changed -Action $historyAction -MessageData @{ SkillPath = $SkillPath } | Out-Null

                $historyWatcher.EnableRaisingEvents = $true
                $watchers += $historyWatcher

                Write-Host "  ✅ Watching: Claude History" -ForegroundColor Green
                Write-KWLog -Message "Started Claude history watcher" -Level "INFO"
            }
            catch {
                Write-Host "  ❌ Failed to create Claude history watcher: $_" -ForegroundColor Red
            }
        }
    }

    if ($watchers.Count -eq 0) {
        Write-Host "❌ No watchers started" -ForegroundColor Red
        return
    }

    # Mettre à jour l'état
    $state.watchersPid = $PID
    $state.watchersStarted = (Get-Date).ToString("o")
    Save-KWState -State $state

    Write-Host "`n✅ Knowledge Watcher started" -ForegroundColor Green
    Write-Host "   PID: $PID" -ForegroundColor Gray
    Write-Host "   Watchers: $($watchers.Count)" -ForegroundColor Gray
    Write-Host "`n   Press Ctrl+C to stop..." -ForegroundColor Gray

    Write-KWLog -Message "Knowledge Watcher started with $($watchers.Count) watchers (PID: $PID)" -Level "INFO"

    # Boucle principale
    $lastCleanup = Get-Date
    $cleanupIntervalHours = 6
    try {
        $cfg = Get-KWConfig
        if ($cfg.processing.cleanupIntervalHours) {
            $cleanupIntervalHours = $cfg.processing.cleanupIntervalHours
        }
    } catch { }

    try {
        while ($true) {
            Start-Sleep -Seconds 60

            # Vérifier la santé des watchers
            $activeWatchers = $watchers | Where-Object { $_.EnableRaisingEvents }
            if ($activeWatchers.Count -eq 0) {
                Write-KWLog -Message "All watchers stopped unexpectedly" -Level "ERROR"
                break
            }

            # Nettoyage périodique queue + hashes
            if (((Get-Date) - $lastCleanup).TotalHours -ge $cleanupIntervalHours) {
                try {
                    Invoke-KWQueueCleanup
                    Invoke-KWHashCleanup
                    $lastCleanup = Get-Date
                    Write-KWLog -Message "Periodic cleanup completed" -Level "INFO"
                } catch {
                    Write-KWLog -Message "Periodic cleanup failed: $_" -Level "WARN"
                }
            }
        }
    }
    finally {
        # Cleanup
        foreach ($watcher in $watchers) {
            $watcher.EnableRaisingEvents = $false
            $watcher.Dispose()
        }

        $state = Get-KWState
        $state.watchersPid = $null
        $state.watchersStarted = $null
        Save-KWState -State $state

        Write-Host "`n⏹️  Knowledge Watcher stopped" -ForegroundColor Yellow
        Write-KWLog -Message "Knowledge Watcher stopped" -Level "INFO"
    }
}

# Exécution
if ($Background) {
    $job = Start-Job -ScriptBlock {
        param($SkillPath)
        Set-Location $SkillPath
        & (Join-Path $SkillPath "scripts\Start-KnowledgeWatcher.ps1")
    } -ArgumentList $SkillPath

    Write-Host "✅ Knowledge Watcher started in background" -ForegroundColor Green
    Write-Host "   Job ID: $($job.Id)" -ForegroundColor Gray
    Write-Host "   Use 'Get-Job $($job.Id)' to check status" -ForegroundColor Gray
}
else {
    Start-Watchers
}
