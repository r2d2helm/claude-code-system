#Requires -Version 5.1
<#
.SYNOPSIS
    BrowserBookmarksSource - Parser pour les bookmarks des navigateurs

.DESCRIPTION
    Capture les bookmarks de Chrome, Edge et Firefox
    pour créer des notes de référence dans Obsidian.
#>

$script:SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $script:SkillPath "scripts\KnowledgeWatcher.psm1") -Force

# Chemins des bookmarks par navigateur
$script:BrowserPaths = @{
    chrome  = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Bookmarks"
    edge    = "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Bookmarks"
    firefox = "$env:APPDATA\Mozilla\Firefox\Profiles"
}

function Get-BrowserBookmarks {
    <#
    .SYNOPSIS
        Récupère les bookmarks d'un navigateur spécifique

    .PARAMETER Browser
        Nom du navigateur (chrome, edge, firefox)

    .PARAMETER LastCapture
        Timestamp de la dernière capture (pour capture incrémentale)

    .OUTPUTS
        Array de bookmarks formatés
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateSet("chrome", "edge", "firefox")]
        [string]$Browser,

        [DateTime]$LastCapture = [DateTime]::MinValue
    )

    switch ($Browser) {
        "chrome" { return Get-ChromiumBookmarks -Path $script:BrowserPaths.chrome -LastCapture $LastCapture }
        "edge" { return Get-ChromiumBookmarks -Path $script:BrowserPaths.edge -LastCapture $LastCapture }
        "firefox" { return Get-FirefoxBookmarks -ProfilesPath $script:BrowserPaths.firefox -LastCapture $LastCapture }
    }

    return @()
}

function Get-ChromiumBookmarks {
    <#
    .SYNOPSIS
        Parse les bookmarks de Chrome/Edge (format JSON)
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Path,

        [DateTime]$LastCapture = [DateTime]::MinValue
    )

    if (-not (Test-Path $Path)) {
        Write-KWLog -Message "Chromium bookmarks file not found: $Path" -Level "DEBUG"
        return @()
    }

    try {
        $content = Get-Content -Path $Path -Raw -Encoding UTF8 | ConvertFrom-Json
        $bookmarks = @()

        # Parser récursivement les folders
        function Parse-BookmarkNode {
            param($Node, $FolderPath)

            if ($Node.type -eq "url") {
                # Convertir le timestamp Chrome (microseconds depuis 1601-01-01)
                $addedTime = [DateTime]::MinValue
                if ($Node.date_added) {
                    try {
                        $ticks = [long]$Node.date_added * 10
                        $addedTime = [DateTime]::FromFileTimeUtc($ticks - 116444736000000000)
                    }
                    catch { }
                }

                if ($addedTime -gt $LastCapture) {
                    return [PSCustomObject]@{
                        Title       = $Node.name
                        Url         = $Node.url
                        Folder      = $FolderPath
                        AddedDate   = $addedTime
                        Type        = "bookmark"
                    }
                }
            }
            elseif ($Node.type -eq "folder" -and $Node.children) {
                $newPath = if ($FolderPath) { "$FolderPath/$($Node.name)" } else { $Node.name }
                $results = @()
                foreach ($child in $Node.children) {
                    $results += Parse-BookmarkNode -Node $child -FolderPath $newPath
                }
                return $results
            }

            return $null
        }

        # Parcourir les racines
        if ($content.roots) {
            foreach ($root in @($content.roots.bookmark_bar, $content.roots.other, $content.roots.synced)) {
                if ($root -and $root.children) {
                    foreach ($child in $root.children) {
                        $result = Parse-BookmarkNode -Node $child -FolderPath $root.name
                        if ($result) {
                            $bookmarks += $result
                        }
                    }
                }
            }
        }

        return $bookmarks
    }
    catch {
        Write-KWLog -Message "Failed to parse Chromium bookmarks: $_" -Level "ERROR"
        return @()
    }
}

function Get-FirefoxBookmarks {
    <#
    .SYNOPSIS
        Parse les bookmarks de Firefox (SQLite)
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$ProfilesPath,

        [DateTime]$LastCapture = [DateTime]::MinValue
    )

    if (-not (Test-Path $ProfilesPath)) {
        Write-KWLog -Message "Firefox profiles path not found: $ProfilesPath" -Level "DEBUG"
        return @()
    }

    # Trouver le profil par défaut
    $profiles = Get-ChildItem -Path $ProfilesPath -Directory | Where-Object { $_.Name -like "*.default*" }
    if ($profiles.Count -eq 0) {
        Write-KWLog -Message "No Firefox default profile found" -Level "DEBUG"
        return @()
    }

    $placesDb = Join-Path $profiles[0].FullName "places.sqlite"
    if (-not (Test-Path $placesDb)) {
        Write-KWLog -Message "Firefox places.sqlite not found" -Level "DEBUG"
        return @()
    }

    # Note: SQLite access requires additional module or native calls
    # For simplicity, we'll skip Firefox for now and log a message
    Write-KWLog -Message "Firefox bookmark parsing requires SQLite support - skipping" -Level "INFO"

    return @()
}

function Format-BookmarkEntry {
    <#
    .SYNOPSIS
        Formate un bookmark en entrée pour la queue
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [PSCustomObject]$Bookmark,

        [string]$Browser
    )

    # Créer un contenu enrichi pour le bookmark
    $content = @"
# $($Bookmark.Title)

## URL
$($Bookmark.Url)

## Détails
- **Navigateur**: $Browser
- **Dossier**: $($Bookmark.Folder ?? "Root")
- **Ajouté le**: $($Bookmark.AddedDate.ToString("yyyy-MM-dd"))

## Description
<!-- Ajouter une description du contenu de la page -->


## Notes
<!-- Notes personnelles sur cette ressource -->

"@

    return [PSCustomObject]@{
        SourceId   = "browser-bookmarks"
        SourcePath = "$Browser - $($Bookmark.Url)"
        Title      = $Bookmark.Title
        Content    = $content
        Metadata   = @{
            url        = $Bookmark.Url
            browser    = $Browser
            folder     = $Bookmark.Folder
            addedDate  = $Bookmark.AddedDate.ToString("o")
        }
    }
}

function Invoke-BookmarksCapture {
    <#
    .SYNOPSIS
        Capture les nouveaux bookmarks de tous les navigateurs configurés
    #>
    [CmdletBinding()]
    param()

    $sources = Get-KWSources
    $bookmarksSource = $sources | Where-Object { $_.id -eq "browser-bookmarks" }

    if (-not $bookmarksSource -or -not $bookmarksSource.enabled) {
        Write-KWLog -Message "Browser bookmarks source not enabled" -Level "INFO"
        return 0
    }

    $state = Get-KWState
    $lastCapture = if ($state.lastBookmarksCapture) {
        [DateTime]::Parse($state.lastBookmarksCapture)
    }
    else {
        [DateTime]::MinValue
    }

    $browsers = $bookmarksSource.browsers ?? @("chrome", "edge")
    $added = 0

    foreach ($browser in $browsers) {
        $bookmarks = Get-BrowserBookmarks -Browser $browser -LastCapture $lastCapture

        foreach ($bookmark in $bookmarks) {
            $entry = Format-BookmarkEntry -Bookmark $bookmark -Browser $browser

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

    # Mettre à jour l'état
    $state.lastBookmarksCapture = (Get-Date).ToString("o")
    Save-KWState -State $state

    Write-KWLog -Message "Captured $added new bookmarks" -Level "INFO"

    return $added
}

function Get-BookmarkStats {
    <#
    .SYNOPSIS
        Retourne les statistiques des bookmarks disponibles
    #>
    [CmdletBinding()]
    param()

    $stats = @{}

    foreach ($browser in @("chrome", "edge", "firefox")) {
        $path = $script:BrowserPaths[$browser]

        if ($browser -eq "firefox") {
            $profiles = if (Test-Path $path) {
                Get-ChildItem -Path $path -Directory | Where-Object { $_.Name -like "*.default*" }
            }
            $stats[$browser] = @{
                available = $profiles.Count -gt 0
                path      = $path
            }
        }
        else {
            $stats[$browser] = @{
                available = Test-Path $path
                path      = $path
            }
        }
    }

    return $stats
}

# Functions exported via dot-sourcing:
# - Get-BrowserBookmarks
# - Invoke-BookmarksCapture
# - Get-BookmarkStats
