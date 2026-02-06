#Requires -Version 5.1
<#
.SYNOPSIS
    ClaudeHistorySource - Parser pour l'historique Claude JSONL

.DESCRIPTION
    Parse le fichier history.jsonl de Claude Code et extrait
    les conversations significatives pour la base de connaissances.
#>

$script:SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $script:SkillPath "scripts\KnowledgeWatcher.psm1") -Force

function Get-ClaudeHistoryEntries {
    <#
    .SYNOPSIS
        Lit et parse le fichier history.jsonl de Claude

    .PARAMETER Path
        Chemin vers le fichier history.jsonl

    .PARAMETER FromLine
        Ligne de départ (pour lecture incrémentale)

    .PARAMETER MinMessages
        Nombre minimum de messages pour considérer une conversation

    .OUTPUTS
        Array de conversations parsées
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Path,

        [int]$FromLine = 0,

        [int]$MinMessages = 3
    )

    if (-not (Test-Path $Path)) {
        Write-KWLog -Message "Claude history file not found: $Path" -Level "WARN"
        return @()
    }

    $entries = @()
    $currentLine = 0
    $currentConversation = $null

    try {
        $reader = [System.IO.StreamReader]::new($Path)

        while ($null -ne ($line = $reader.ReadLine())) {
            $currentLine++

            # Skip lignes déjà lues
            if ($currentLine -le $FromLine) {
                continue
            }

            if ([string]::IsNullOrWhiteSpace($line)) {
                continue
            }

            try {
                $entry = $line | ConvertFrom-Json

                # Nouvelle conversation détectée
                if ($entry.type -eq "session_start" -or
                    ($currentConversation -and $entry.sessionId -ne $currentConversation.sessionId)) {

                    # Sauvegarder la conversation précédente si significative
                    if ($currentConversation -and $currentConversation.messages.Count -ge $MinMessages) {
                        $entries += Format-ConversationEntry -Conversation $currentConversation
                    }

                    $currentConversation = @{
                        sessionId = if ($entry.sessionId) { $entry.sessionId } else { [guid]::NewGuid().ToString() }
                        startTime = if ($entry.timestamp) { $entry.timestamp } else { (Get-Date).ToString("o") }
                        messages = @()
                        metadata = @{}
                    }
                }

                # Ajouter le message à la conversation courante
                if ($entry.type -eq "message" -or $entry.role) {
                    if (-not $currentConversation) {
                        $currentConversation = @{
                            sessionId = if ($entry.sessionId) { $entry.sessionId } else { [guid]::NewGuid().ToString() }
                            startTime = if ($entry.timestamp) { $entry.timestamp } else { (Get-Date).ToString("o") }
                            messages = @()
                            metadata = @{}
                        }
                    }

                    $msgContent = if ($entry.content) { $entry.content } elseif ($entry.message) { $entry.message } else { "" }
                    $currentConversation.messages += @{
                        role = if ($entry.role) { $entry.role } else { "unknown" }
                        content = $msgContent
                        timestamp = if ($entry.timestamp) { $entry.timestamp } else { "" }
                    }
                }

                # Capturer les métadonnées de tool use
                if ($entry.type -eq "tool_use" -or $entry.toolName) {
                    if ($currentConversation) {
                        if (-not $currentConversation.metadata.tools) {
                            $currentConversation.metadata.tools = @()
                        }
                        $toolName = if ($entry.toolName) { $entry.toolName } elseif ($entry.name) { $entry.name } else { "unknown" }
                        $currentConversation.metadata.tools += $toolName
                    }
                }
            }
            catch {
                Write-KWLog -Message "Failed to parse line $currentLine : $_" -Level "DEBUG"
            }
        }

        # Dernière conversation
        if ($currentConversation -and $currentConversation.messages.Count -ge $MinMessages) {
            $entries += Format-ConversationEntry -Conversation $currentConversation
        }
    }
    finally {
        if ($reader) {
            $reader.Close()
            $reader.Dispose()
        }
    }

    # Mettre à jour l'état avec la dernière ligne lue
    $state = Get-KWState
    $state.lastClaudeHistoryLine = $currentLine
    Save-KWState -State $state

    Write-KWLog -Message "Parsed $($entries.Count) conversations from Claude history (lines $FromLine to $currentLine)" -Level "INFO"

    return $entries
}

function Format-ConversationEntry {
    <#
    .SYNOPSIS
        Formate une conversation en entrée standardisée
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [hashtable]$Conversation
    )

    # Construire le contenu texte
    $contentLines = @()
    foreach ($msg in $Conversation.messages) {
        $role = switch ($msg.role) {
            "user" { "User" }
            "assistant" { "Assistant" }
            "human" { "User" }
            default { $msg.role }
        }

        $content = $msg.content
        if ($content -is [array]) {
            $content = ($content | Where-Object { $_.type -eq "text" } | ForEach-Object { $_.text }) -join "`n"
        }

        $contentLines += "$role`:`n$content`n"
    }

    $fullContent = $contentLines -join "`n---`n"

    # Extraire le titre
    $title = Get-ConversationTitle -Messages $Conversation.messages

    # Détecter les sujets
    $subjects = Get-ConversationSubjects -Content $fullContent

    return [PSCustomObject]@{
        SourceId = "claude-history"
        SourcePath = "Claude History - $($Conversation.sessionId)"
        Title = $title
        Content = $fullContent
        Metadata = @{
            sessionId = $Conversation.sessionId
            startTime = $Conversation.startTime
            messageCount = $Conversation.messages.Count
            tools = if ($Conversation.metadata.tools) { $Conversation.metadata.tools } else { @() }
            subjects = $subjects
        }
    }
}

function Get-ConversationTitle {
    <#
    .SYNOPSIS
        Extrait ou génère un titre pour la conversation
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [array]$Messages
    )

    # Prendre le premier message utilisateur
    $firstUserMessage = $Messages | Where-Object { $_.role -in @("user", "human") } | Select-Object -First 1

    if ($firstUserMessage) {
        $content = $firstUserMessage.content
        if ($content -is [array]) {
            $content = ($content | Where-Object { $_.type -eq "text" } | ForEach-Object { $_.text }) -join " "
        }

        # Nettoyer et tronquer
        $title = $content -replace '[\r\n]+', ' ' -replace '\s+', ' '
        $title = $title.Trim()

        if ($title.Length -gt 80) {
            $title = $title.Substring(0, 77) + "..."
        }

        return $title
    }

    return "Conversation $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
}

function Get-ConversationSubjects {
    <#
    .SYNOPSIS
        Détecte les sujets abordés dans la conversation
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Content
    )

    $subjects = @()

    $patterns = @{
        "powershell" = "powershell|\.ps1|cmdlet|param\("
        "python" = "python|\.py|import |def |pip"
        "infrastructure" = "proxmox|docker|kubernetes|vm|container"
        "claude" = "claude|anthropic|llm|ai|agent"
        "git" = "git|commit|branch|merge|pull request"
        "api" = "api|rest|graphql|endpoint|http"
        "database" = "sql|database|query|table"
        "security" = "security|auth|jwt|oauth|credential"
        "configuration" = "config|settings|setup|install"
        "debugging" = "debug|error|fix|issue|problem"
    }

    foreach ($subject in $patterns.Keys) {
        if ($Content -match $patterns[$subject]) {
            $subjects += $subject
        }
    }

    return $subjects
}

function Invoke-ClaudeHistoryCapture {
    <#
    .SYNOPSIS
        Capture les nouvelles conversations depuis Claude history
    #>
    [CmdletBinding()]
    param()

    $config = Get-KWConfig
    $sources = Get-KWSources

    $historySource = $sources | Where-Object { $_.id -eq "claude-history" }
    if (-not $historySource -or -not $historySource.enabled) {
        Write-KWLog -Message "Claude history source not enabled" -Level "INFO"
        return 0
    }

    $state = Get-KWState
    $fromLine = if ($state.lastClaudeHistoryLine) { $state.lastClaudeHistoryLine } else { 0 }

    $historyPath = $historySource.path
    if (-not (Test-Path $historyPath)) {
        Write-KWLog -Message "Claude history file not found: $historyPath" -Level "WARN"
        return 0
    }

    $entries = Get-ClaudeHistoryEntries -Path $historyPath -FromLine $fromLine

    $added = 0
    foreach ($entry in $entries) {
        $result = Add-KWQueueItem `
            -SourceId $entry.SourceId `
            -SourcePath $entry.SourcePath `
            -Content $entry.Content `
            -Title $entry.Title `
            -Metadata $entry.Metadata

        if ($result) {
            $added++
        }
    }

    Write-KWLog -Message "Added $added new Claude conversations to queue" -Level "INFO"
    return $added
}

# Functions exported via dot-sourcing:
# - Get-ClaudeHistoryEntries
# - Invoke-ClaudeHistoryCapture
# - Get-ConversationTitle
# - Get-ConversationSubjects
