#Requires -Version 5.1
<#
.SYNOPSIS
    Knowledge Watcher Module - Surveillance et capture automatique de connaissances

.DESCRIPTION
    Module principal pour le Knowledge Watcher Agent.
    Fournit les fonctions de base pour la gestion de la queue, des watchers,
    et du pipeline de traitement.

.NOTES
    Version: 1.0.0
    Author: Claude Code
#>

$script:SkillPath = Split-Path -Parent $PSScriptRoot
$script:ConfigPath = Join-Path $script:SkillPath "config"
$script:DataPath = Join-Path $script:SkillPath "data"
$script:ProcessorsPath = Join-Path $script:SkillPath "processors"
$script:SourcesPath = Join-Path $script:SkillPath "sources"

$script:MutexName = "KnowledgeWatcherQueue"

# UTF-8 Encoding without BOM for proper French character support
$script:Utf8NoBom = New-Object System.Text.UTF8Encoding $false

# Force UTF-8 encoding for console output (important for French characters)
if ($Host.Name -eq 'ConsoleHost') {
    try {
        [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        [Console]::InputEncoding = [System.Text.Encoding]::UTF8
    }
    catch {
        # Ignore errors if console encoding cannot be set
    }
}

# Set default file encoding to UTF-8 for Out-File and Set-Content
$PSDefaultParameterValues['Out-File:Encoding'] = 'UTF8'
$PSDefaultParameterValues['Set-Content:Encoding'] = 'UTF8'

#region Utility Functions

function Write-Utf8File {
    <#
    .SYNOPSIS
        Écrit du contenu dans un fichier en UTF-8 sans BOM
    .DESCRIPTION
        PowerShell 5.1 écrit UTF-8 avec BOM par défaut, ce qui cause des
        problèmes d'encodage. Cette fonction utilise .NET pour écrire
        UTF-8 sans BOM.
    .PARAMETER Path
        Chemin du fichier
    .PARAMETER Content
        Contenu à écrire
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Path,

        [Parameter(Mandatory, ValueFromPipeline)]
        [AllowEmptyString()]
        [string]$Content
    )

    process {
        $parentDir = Split-Path -Parent $Path
        if ($parentDir -and -not (Test-Path $parentDir)) {
            New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
        }
        [System.IO.File]::WriteAllText($Path, $Content, $script:Utf8NoBom)
    }
}

function Read-Utf8File {
    <#
    .SYNOPSIS
        Lit un fichier en UTF-8
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Path
    )

    if (Test-Path $Path) {
        return [System.IO.File]::ReadAllText($Path, $script:Utf8NoBom)
    }
    return $null
}

#endregion

#region Configuration Functions

function Get-KWConfig {
    <#
    .SYNOPSIS
        Charge la configuration principale
    #>
    [CmdletBinding()]
    param()

    $configFile = Join-Path $script:ConfigPath "config.json"
    if (Test-Path $configFile) {
        return Get-Content $configFile -Raw | ConvertFrom-Json
    }
    throw "Configuration file not found: $configFile"
}

function Get-KWSources {
    <#
    .SYNOPSIS
        Charge la configuration des sources
    #>
    [CmdletBinding()]
    param()

    $sourcesFile = Join-Path $script:ConfigPath "sources.json"
    if (Test-Path $sourcesFile) {
        return (Get-Content $sourcesFile -Raw | ConvertFrom-Json).sources
    }
    throw "Sources file not found: $sourcesFile"
}

function Get-KWRules {
    <#
    .SYNOPSIS
        Charge les règles de classification
    #>
    [CmdletBinding()]
    param()

    $rulesFile = Join-Path $script:ConfigPath "rules.json"
    if (Test-Path $rulesFile) {
        return Get-Content $rulesFile -Raw | ConvertFrom-Json
    }
    throw "Rules file not found: $rulesFile"
}

#endregion

#region State Management

function Get-KWState {
    <#
    .SYNOPSIS
        Charge l'état actuel du watcher
    #>
    [CmdletBinding()]
    param()

    $stateFile = Join-Path $script:DataPath "state.json"
    if (Test-Path $stateFile) {
        return Get-Content $stateFile -Raw | ConvertFrom-Json
    }
    return @{
        hashes = @{}
        lastClaudeHistoryLine = 0
        watchersPid = $null
        watchersStarted = $null
    }
}

function Save-KWState {
    <#
    .SYNOPSIS
        Sauvegarde l'état actuel
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [PSCustomObject]$State
    )

    $stateFile = Join-Path $script:DataPath "state.json"
    $jsonContent = $State | ConvertTo-Json -Depth 10
    Write-Utf8File -Path $stateFile -Content $jsonContent
}

#endregion

#region Queue Management

function Get-KWQueue {
    <#
    .SYNOPSIS
        Charge la queue de traitement
    #>
    [CmdletBinding()]
    param()

    $queueFile = Join-Path $script:DataPath "queue.json"
    if (Test-Path $queueFile) {
        return Get-Content $queueFile -Raw | ConvertFrom-Json
    }
    return @{
        items = @()
        lastProcessed = $null
        stats = @{
            totalCaptured = 0
            totalProcessed = 0
            totalErrors = 0
        }
    }
}

function Save-KWQueue {
    <#
    .SYNOPSIS
        Sauvegarde la queue (thread-safe avec mutex)
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [PSCustomObject]$Queue
    )

    $mutex = [System.Threading.Mutex]::new($false, $script:MutexName)
    try {
        $mutex.WaitOne() | Out-Null
        $queueFile = Join-Path $script:DataPath "queue.json"
        $jsonContent = $Queue | ConvertTo-Json -Depth 10
        Write-Utf8File -Path $queueFile -Content $jsonContent
    }
    finally {
        $mutex.ReleaseMutex()
    }
}

function Add-KWQueueItem {
    <#
    .SYNOPSIS
        Ajoute un élément à la queue avec déduplication
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$SourceId,

        [Parameter(Mandatory)]
        [string]$SourcePath,

        [Parameter(Mandatory)]
        [string]$Content,

        [string]$Title,

        [hashtable]$Metadata = @{}
    )

    $config = Get-KWConfig
    $state = Get-KWState

    # Calculer le hash pour déduplication
    $hash = Get-KWContentHash -Content $Content

    # Vérifier si déjà traité dans la fenêtre de déduplication
    $now = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
    if ($state.hashes.PSObject.Properties[$hash]) {
        $lastSeen = $state.hashes.$hash
        if (($now - $lastSeen) -lt $config.processing.deduplicationWindow) {
            Write-Verbose "Duplicate detected, skipping: $SourcePath"
            return $false
        }
    }

    # Mettre à jour le hash
    if (-not $state.hashes) {
        $state | Add-Member -NotePropertyName "hashes" -NotePropertyValue @{} -Force
    }
    $state.hashes | Add-Member -NotePropertyName $hash -NotePropertyValue $now -Force
    Save-KWState -State $state

    $mutex = [System.Threading.Mutex]::new($false, $script:MutexName)
    try {
        $mutex.WaitOne() | Out-Null

        $queue = Get-KWQueue

        # Vérifier limite de queue - cleanup avant d'ajouter
        if ($queue.items.Count -ge $config.processing.maxQueueSize) {
            Write-KWLog -Message "Queue full, triggering cleanup before adding" -Level "INFO"
            # Release mutex temporarily for cleanup
            $mutex.ReleaseMutex()
            Invoke-KWQueueCleanup
            Invoke-KWHashCleanup
            $mutex.WaitOne() | Out-Null
            # Reload queue after cleanup
            $queue = Get-KWQueue
            # If still full after cleanup, drop oldest
            if ($queue.items.Count -ge $config.processing.maxQueueSize) {
                $queue.items = $queue.items | Select-Object -Skip 1
            }
        }

        # Safety check: if queue file exceeds 10MB, force cleanup
        $queueFile2 = Join-Path $script:DataPath "queue.json"
        if ((Test-Path $queueFile2) -and (Get-Item $queueFile2).Length -gt 10MB) {
            Write-KWLog -Message "Queue file exceeds 10MB safety limit, forcing cleanup" -Level "WARN"
            $mutex.ReleaseMutex()
            Invoke-KWQueueCleanup
            $mutex.WaitOne() | Out-Null
            $queue = Get-KWQueue
        }

        $item = [PSCustomObject]@{
            id = [guid]::NewGuid().ToString()
            sourceId = $SourceId
            sourcePath = $SourcePath
            title = $Title
            hash = $hash
            capturedAt = (Get-Date).ToString("o")
            status = "pending"
            metadata = $Metadata
        }

        $queue.items += $item
        $queue.stats.totalCaptured++

        Save-KWQueue -Queue $queue

        Write-KWLog -Message "Added to queue: $SourcePath" -Level "INFO"
        return $true
    }
    finally {
        $mutex.ReleaseMutex()
    }
}

function Get-KWContentHash {
    <#
    .SYNOPSIS
        Calcule un hash SHA256 du contenu
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Content
    )

    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Content)
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    $hashBytes = $sha256.ComputeHash($bytes)
    return [BitConverter]::ToString($hashBytes) -replace '-', ''
}

#endregion

#region Queue Maintenance

function Invoke-KWQueueCleanup {
    <#
    .SYNOPSIS
        Archive completed/error items and trim the queue to prevent bloat
    .DESCRIPTION
        Moves completed and error items to a monthly archive file,
        cleans old hashes from state, and keeps queue.json small.
    .PARAMETER MaxAgeDays
        Archive items older than this (default: 7)
    .PARAMETER MaxQueueItems
        Keep at most this many items in active queue (default: 100)
    #>
    [CmdletBinding()]
    param(
        [int]$MaxAgeDays = 7,
        [int]$MaxQueueItems = 100
    )

    $mutex = [System.Threading.Mutex]::new($false, $script:MutexName)
    try {
        $mutex.WaitOne() | Out-Null

        $queueFile = Join-Path $script:DataPath "queue.json"
        if (-not (Test-Path $queueFile)) { return }

        # Check file size first - if over 50MB, something is wrong
        $fileSize = (Get-Item $queueFile).Length
        if ($fileSize -gt 50MB) {
            Write-KWLog -Message "Queue file too large ($([math]::Round($fileSize/1MB,1)) MB), resetting" -Level "WARN"
            $freshQueue = @{
                items = @()
                lastProcessed = $null
                stats = @{ totalCaptured = 0; totalProcessed = 0; totalErrors = 0 }
                maintenance = @{
                    lastCleanup = (Get-Date).ToString("o")
                    archivedItems = 0
                    resetReason = "Queue exceeded 50MB safety limit"
                }
            }
            $jsonContent = $freshQueue | ConvertTo-Json -Depth 10
            Write-Utf8File -Path $queueFile -Content $jsonContent
            return
        }

        $queue = Get-Content $queueFile -Raw | ConvertFrom-Json
        $cutoff = (Get-Date).AddDays(-$MaxAgeDays).ToString("o")

        # Separate items to archive vs keep
        $toArchive = @()
        $toKeep = @()

        foreach ($item in $queue.items) {
            if ($item.status -in @("completed", "error") -or
                ($item.capturedAt -and $item.capturedAt -lt $cutoff)) {
                $toArchive += $item
            } else {
                $toKeep += $item
            }
        }

        # Archive to monthly file
        if ($toArchive.Count -gt 0) {
            $archiveMonth = Get-Date -Format "yyyy-MM"
            $archiveFile = Join-Path $script:DataPath "queue-archive-$archiveMonth.json"

            $existingArchive = @()
            if (Test-Path $archiveFile) {
                try {
                    $existingArchive = @((Get-Content $archiveFile -Raw | ConvertFrom-Json))
                } catch { $existingArchive = @() }
            }
            $allArchived = $existingArchive + $toArchive
            $archiveJson = $allArchived | ConvertTo-Json -Depth 10
            Write-Utf8File -Path $archiveFile -Content $archiveJson

            Write-KWLog -Message "Archived $($toArchive.Count) queue items to $archiveFile" -Level "INFO"
        }

        # Trim if still too many
        if ($toKeep.Count -gt $MaxQueueItems) {
            $toKeep = $toKeep | Select-Object -Last $MaxQueueItems
        }

        # Update queue
        $queue.items = $toKeep
        if (-not $queue.maintenance) {
            $queue | Add-Member -NotePropertyName "maintenance" -NotePropertyValue @{} -Force
        }
        $queue.maintenance = @{
            lastCleanup = (Get-Date).ToString("o")
            archivedItems = $toArchive.Count
        }

        $jsonContent = $queue | ConvertTo-Json -Depth 10
        Write-Utf8File -Path $queueFile -Content $jsonContent

        Write-KWLog -Message "Queue cleanup: kept $($toKeep.Count), archived $($toArchive.Count)" -Level "INFO"
    }
    finally {
        $mutex.ReleaseMutex()
    }
}

function Invoke-KWHashCleanup {
    <#
    .SYNOPSIS
        Remove expired hashes from state.json to prevent unbounded growth
    .PARAMETER MaxAgeMs
        Remove hashes older than this (default: deduplicationWindow from config, or 24h)
    #>
    [CmdletBinding()]
    param(
        [long]$MaxAgeMs = 0
    )

    $state = Get-KWState
    if (-not $state.hashes) { return }

    if ($MaxAgeMs -eq 0) {
        try {
            $config = Get-KWConfig
            $MaxAgeMs = $config.processing.deduplicationWindow
        } catch {
            $MaxAgeMs = 86400000  # 24h default
        }
    }

    $now = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
    $cleanHashes = @{}
    $removed = 0

    foreach ($prop in $state.hashes.PSObject.Properties) {
        $lastSeen = [long]$prop.Value
        if (($now - $lastSeen) -lt $MaxAgeMs) {
            $cleanHashes[$prop.Name] = $prop.Value
        } else {
            $removed++
        }
    }

    if ($removed -gt 0) {
        $state.hashes = [PSCustomObject]$cleanHashes
        Save-KWState -State $state
        Write-KWLog -Message "Hash cleanup: removed $removed expired hashes, kept $($cleanHashes.Count)" -Level "INFO"
    }
}

#endregion

#region Logging

function Write-KWLog {
    <#
    .SYNOPSIS
        Écrit dans le fichier de log
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Message,

        [ValidateSet("INFO", "WARN", "ERROR", "DEBUG")]
        [string]$Level = "INFO"
    )

    $config = Get-KWConfig
    $logDir = $config.paths.logDir

    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }

    $logFile = Join-Path $logDir "kwatch_$(Get-Date -Format 'yyyy-MM-dd').log"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logLine = "[$timestamp] [$Level] $Message"

    Add-Content -Path $logFile -Value $logLine -Encoding UTF8

    if ($Level -eq "ERROR") {
        Write-Error $Message
    }
    elseif ($Level -eq "WARN") {
        Write-Warning $Message
    }
    else {
        Write-Verbose $Message
    }
}

#endregion

#region Status Functions

function Get-KWStatus {
    <#
    .SYNOPSIS
        Retourne le statut complet du Knowledge Watcher
    #>
    [CmdletBinding()]
    param()

    $config = Get-KWConfig
    $state = Get-KWState
    $queue = Get-KWQueue
    $sources = Get-KWSources

    $watchersRunning = $false
    if ($state.watchersPid) {
        try {
            $process = Get-Process -Id $state.watchersPid -ErrorAction SilentlyContinue
            $watchersRunning = $null -ne $process
        }
        catch {
            $watchersRunning = $false
        }
    }

    return [PSCustomObject]@{
        IsRunning = $watchersRunning
        WatchersPid = $state.watchersPid
        StartedAt = $state.watchersStarted
        QueueCount = $queue.items.Count
        QueuePending = ($queue.items | Where-Object { $_.status -eq "pending" }).Count
        Stats = $queue.stats
        EnabledSources = ($sources | Where-Object { $_.enabled }).Count
        TotalSources = $sources.Count
        LastTier2 = $state.lastTier2Run
        LastTier3 = $state.lastTier3Run
        LastTier4 = $state.lastTier4Run
        VaultPath = $config.paths.obsidianVault
    }
}

function Format-KWStatus {
    <#
    .SYNOPSIS
        Formate le statut pour affichage
    #>
    [CmdletBinding()]
    param()

    $status = Get-KWStatus

    $runningIcon = if ($status.IsRunning) { "✅ RUNNING" } else { "⏹️ STOPPED" }

    $startedAt = if ($status.StartedAt) { $status.StartedAt } else { "N/A" }
    $watchersPid = if ($status.WatchersPid) { $status.WatchersPid } else { "N/A" }
    $lastTier2 = if ($status.LastTier2) { $status.LastTier2 } else { "Never" }
    $lastTier3 = if ($status.LastTier3) { $status.LastTier3 } else { "Never" }
    $lastTier4 = if ($status.LastTier4) { $status.LastTier4 } else { "Never" }

    $output = @"
╔══════════════════════════════════════════════════════════════╗
║            🔍 KNOWLEDGE WATCHER STATUS                       ║
╠══════════════════════════════════════════════════════════════╣
║  Status        : $runningIcon
║  Started At    : $startedAt
║  PID           : $watchersPid
╠══════════════════════════════════════════════════════════════╣
║  QUEUE                                                       ║
║  ├─ Total Items    : $($status.QueueCount)
║  ├─ Pending        : $($status.QueuePending)
║  └─ Max Size       : 100
╠══════════════════════════════════════════════════════════════╣
║  STATISTICS                                                  ║
║  ├─ Total Captured : $($status.Stats.totalCaptured)
║  ├─ Processed      : $($status.Stats.totalProcessed)
║  └─ Errors         : $($status.Stats.totalErrors)
╠══════════════════════════════════════════════════════════════╣
║  SOURCES                                                     ║
║  ├─ Enabled        : $($status.EnabledSources) / $($status.TotalSources)
║  └─ Vault Path     : $($status.VaultPath)
╠══════════════════════════════════════════════════════════════╣
║  LAST BATCH RUNS                                             ║
║  ├─ Tier 2 (hourly): $lastTier2
║  ├─ Tier 3 (daily) : $lastTier3
║  └─ Tier 4 (weekly): $lastTier4
╚══════════════════════════════════════════════════════════════╝
"@

    return $output
}

#endregion

#region Utility Functions

function Test-KWSetup {
    <#
    .SYNOPSIS
        Vérifie que le setup est correct
    #>
    [CmdletBinding()]
    param()

    $issues = @()
    $config = Get-KWConfig

    # Vérifier Claude CLI
    if (-not (Test-Path $config.paths.claudeCli)) {
        $issues += "Claude CLI not found at: $($config.paths.claudeCli)"
    }

    # Vérifier Obsidian vault
    if (-not (Test-Path $config.paths.obsidianVault)) {
        $issues += "Obsidian vault not found at: $($config.paths.obsidianVault)"
    }

    # Vérifier répertoire de logs
    $logDir = $config.paths.logDir
    if (-not (Test-Path $logDir)) {
        try {
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        }
        catch {
            $issues += "Cannot create log directory: $logDir"
        }
    }

    return [PSCustomObject]@{
        IsValid = $issues.Count -eq 0
        Issues = $issues
    }
}

function Get-KWQueueItems {
    <#
    .SYNOPSIS
        Retourne les éléments de la queue avec filtrage optionnel
    #>
    [CmdletBinding()]
    param(
        [ValidateSet("pending", "processing", "completed", "error", "all")]
        [string]$Status = "all",

        [int]$Limit = 10
    )

    $queue = Get-KWQueue
    $items = $queue.items

    if ($Status -ne "all") {
        $items = $items | Where-Object { $_.status -eq $Status }
    }

    return $items | Select-Object -First $Limit
}

#endregion

# Export des fonctions
Export-ModuleMember -Function @(
    # Utility Functions
    'Write-Utf8File',
    'Read-Utf8File',
    # Configuration Functions
    'Get-KWConfig',
    'Get-KWSources',
    'Get-KWRules',
    # State Management
    'Get-KWState',
    'Save-KWState',
    # Queue Management
    'Get-KWQueue',
    'Save-KWQueue',
    'Add-KWQueueItem',
    'Get-KWContentHash',
    # Queue Maintenance
    'Invoke-KWQueueCleanup',
    'Invoke-KWHashCleanup',
    # Logging
    'Write-KWLog',
    # Status Functions
    'Get-KWStatus',
    'Format-KWStatus',
    'Test-KWSetup',
    'Get-KWQueueItems'
)
