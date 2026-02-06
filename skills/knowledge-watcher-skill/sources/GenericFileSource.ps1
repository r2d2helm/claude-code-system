#Requires -Version 5.1
<#
.SYNOPSIS
    GenericFileSource - Parser générique pour fichiers

.DESCRIPTION
    Capture les fichiers de différents types (Markdown, scripts, configs)
    et les prépare pour le pipeline de traitement.
#>

$script:SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $script:SkillPath "scripts\KnowledgeWatcher.psm1") -Force

function Get-GenericFileEntry {
    <#
    .SYNOPSIS
        Capture un fichier et le formate pour la queue

    .PARAMETER Path
        Chemin du fichier

    .PARAMETER SourceId
        Identifiant de la source

    .OUTPUTS
        PSCustomObject avec les données du fichier
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Path,

        [Parameter(Mandatory)]
        [string]$SourceId
    )

    $config = Get-KWConfig

    if (-not (Test-Path $Path)) {
        Write-KWLog -Message "File not found: $Path" -Level "WARN"
        return $null
    }

    $file = Get-Item $Path

    # Vérifier la taille
    if ($file.Length -gt $config.processing.maxFileSize) {
        Write-KWLog -Message "File too large ($($file.Length) bytes): $Path" -Level "WARN"
        return $null
    }

    # Vérifier l'extension
    $extension = $file.Extension.ToLower()
    $supportedExtensions = @(".md", ".txt", ".ps1", ".psm1", ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".sh", ".bash")

    if ($extension -notin $supportedExtensions) {
        Write-KWLog -Message "Unsupported extension: $extension" -Level "DEBUG"
        return $null
    }

    try {
        $content = Get-Content -Path $Path -Raw -Encoding UTF8

        if ([string]::IsNullOrWhiteSpace($content)) {
            Write-KWLog -Message "File is empty: $Path" -Level "DEBUG"
            return $null
        }

        # Extraire le titre
        $title = Get-FileTitle -Content $content -FileName $file.Name -Extension $extension

        return [PSCustomObject]@{
            SourceId = $SourceId
            SourcePath = $Path
            Title = $title
            Content = $content
            Metadata = @{
                fileName = $file.Name
                extension = $extension
                size = $file.Length
                lastModified = $file.LastWriteTime.ToString("o")
                created = $file.CreationTime.ToString("o")
            }
        }
    }
    catch {
        Write-KWLog -Message "Failed to read file $Path : $_" -Level "ERROR"
        return $null
    }
}

function Get-FileTitle {
    <#
    .SYNOPSIS
        Extrait ou génère un titre pour le fichier
    #>
    [CmdletBinding()]
    param(
        [string]$Content,
        [string]$FileName,
        [string]$Extension
    )

    # Pour Markdown, chercher le premier header
    if ($Extension -eq ".md") {
        if ($Content -match '^#\s+(.+)$') {
            return $Matches[1].Trim()
        }
        # Chercher dans le frontmatter
        if ($Content -match 'title:\s*(.+)') {
            $title = $Matches[1].Trim() -replace '^["'']|["'']$', ''
            return $title
        }
    }

    # Pour les scripts, chercher .SYNOPSIS
    if ($Extension -in @(".ps1", ".psm1")) {
        if ($Content -match '\.SYNOPSIS\s*\r?\n\s*(.+)') {
            return $Matches[1].Trim()
        }
    }

    # Pour Python, chercher le docstring
    if ($Extension -eq ".py") {
        $lines = $Content -split "`n"
        if ($lines.Count -gt 0 -and $lines[0] -match '^(["'']){3}(.+)') {
            return $Matches[2].Trim()
        }
    }

    # Fallback: nom du fichier sans extension
    return [System.IO.Path]::GetFileNameWithoutExtension($FileName)
}

function Invoke-DirectoryScan {
    <#
    .SYNOPSIS
        Scanne un répertoire pour les fichiers nouveaux ou modifiés

    .PARAMETER SourceConfig
        Configuration de la source

    .PARAMETER LastScan
        Timestamp du dernier scan (pour scan incrémental)

    .OUTPUTS
        Nombre de fichiers ajoutés à la queue
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [PSCustomObject]$SourceConfig,

        [DateTime]$LastScan = [DateTime]::MinValue
    )

    $config = Get-KWConfig

    if (-not (Test-Path $SourceConfig.path)) {
        Write-KWLog -Message "Source path not found: $($SourceConfig.path)" -Level "WARN"
        return 0
    }

    $patterns = if ($SourceConfig.patterns) { $SourceConfig.patterns } else { @("*.*") }
    $recursive = if ($null -ne $SourceConfig.recursive) { $SourceConfig.recursive } else { $false }
    $excludePaths = if ($SourceConfig.excludePaths) { $SourceConfig.excludePaths } else { @() }

    $files = @()

    foreach ($pattern in $patterns) {
        $searchPath = Join-Path $SourceConfig.path $pattern

        if ($recursive) {
            $found = Get-ChildItem -Path $SourceConfig.path -Filter $pattern -Recurse -File -ErrorAction SilentlyContinue
        }
        else {
            $found = Get-ChildItem -Path $SourceConfig.path -Filter $pattern -File -ErrorAction SilentlyContinue
        }

        if ($found) {
            $files += $found
        }
    }

    # Filtrer les exclusions
    if ($excludePaths.Count -gt 0) {
        $files = $files | Where-Object {
            $filePath = $_.FullName
            $excluded = $false
            foreach ($exclude in $excludePaths) {
                if ($filePath -like "*\$exclude\*" -or $filePath -like "*/$exclude/*") {
                    $excluded = $true
                    break
                }
            }
            -not $excluded
        }
    }

    # Filtrer par date de modification
    if ($LastScan -ne [DateTime]::MinValue) {
        $files = $files | Where-Object { $_.LastWriteTime -gt $LastScan }
    }

    # Filtrer par ignore patterns
    $ignorePatterns = $(if ($config.watchers.ignorePatterns) { $config.watchers.ignorePatterns } else { @() })
    foreach ($ignore in $ignorePatterns) {
        $files = $files | Where-Object { $_.Name -notlike $ignore }
    }

    $added = 0

    foreach ($file in $files) {
        $entry = Get-GenericFileEntry -Path $file.FullName -SourceId $SourceConfig.id

        if ($entry) {
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
    }

    Write-KWLog -Message "Scanned $($SourceConfig.name): found $($files.Count) files, added $added to queue" -Level "INFO"

    return $added
}

function Invoke-GenericFileCapture {
    <#
    .SYNOPSIS
        Capture un fichier spécifique (appelé par FileSystemWatcher)

    .PARAMETER Path
        Chemin du fichier

    .PARAMETER ChangeType
        Type de changement (Created, Changed, Renamed)

    .OUTPUTS
        $true si ajouté à la queue, $false sinon
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Path,

        [ValidateSet("Created", "Changed", "Renamed")]
        [string]$ChangeType = "Changed"
    )

    $config = Get-KWConfig
    $sources = Get-KWSources

    # Trouver la source correspondante
    $matchingSource = $null
    foreach ($source in $sources) {
        if ($source.type -eq "directory" -and $source.enabled) {
            if ($Path.StartsWith($source.path)) {
                $matchingSource = $source
                break
            }
        }
    }

    if (-not $matchingSource) {
        Write-KWLog -Message "No matching source for: $Path" -Level "DEBUG"
        return $false
    }

    # Vérifier les patterns
    $fileName = [System.IO.Path]::GetFileName($Path)
    $patterns = $(if ($matchingSource.patterns) { $matchingSource.patterns } else { @("*.*") })

    $matches = $false
    foreach ($pattern in $patterns) {
        if ($fileName -like $pattern) {
            $matches = $true
            break
        }
    }

    if (-not $matches) {
        Write-KWLog -Message "File doesn't match patterns: $Path" -Level "DEBUG"
        return $false
    }

    # Vérifier ignore patterns
    $ignorePatterns = $(if ($config.watchers.ignorePatterns) { $config.watchers.ignorePatterns } else { @() })
    foreach ($ignore in $ignorePatterns) {
        if ($fileName -like $ignore) {
            Write-KWLog -Message "File matches ignore pattern: $Path" -Level "DEBUG"
            return $false
        }
    }

    # Capturer le fichier
    $entry = Get-GenericFileEntry -Path $Path -SourceId $matchingSource.id

    if ($entry) {
        $result = Add-KWQueueItem `
            -SourceId $entry.SourceId `
            -SourcePath $entry.SourcePath `
            -Content $entry.Content `
            -Title $entry.Title `
            -Metadata ($entry.Metadata + @{ changeType = $ChangeType })

        Write-KWLog -Message "Captured file ($ChangeType): $Path" -Level "INFO"
        return $result
    }

    return $false
}

# Functions exported via dot-sourcing:
# - Get-GenericFileEntry
# - Get-FileTitle
# - Invoke-DirectoryScan
# - Invoke-GenericFileCapture
