#Requires -Version 5.1
<#
.SYNOPSIS
    Module core du credentials-skill : CRUD, parse YAML frontmatter, index.

.DESCRIPTION
    Fournit les fonctions Get/Set/Remove-CredentialEntry, Update-CredentialIndex,
    Search-Credentials. Parse le frontmatter YAML des fichiers registre.

.NOTES
    Version: 1.0.0
    Author: Claude Code
    Encoding: UTF-8 BOM (PS 5.1)
#>

$script:SkillPath = Split-Path -Parent $PSScriptRoot
$script:DataPath = Join-Path $script:SkillPath "data"
$script:RegistryPath = Join-Path $script:DataPath "registry"
$script:IndexPath = Join-Path $script:RegistryPath "_index.json"
$script:TemplatePath = Join-Path $script:SkillPath "templates\service-credential.md"
$script:Utf8NoBom = New-Object System.Text.UTF8Encoding $false

#region Utility Functions

function Write-Utf8File {
    param(
        [Parameter(Mandatory)]
        [string]$Path,
        [Parameter(Mandatory)]
        [string]$Content
    )
    $parentDir = Split-Path -Parent $Path
    if ($parentDir -and -not (Test-Path $parentDir)) {
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
    }
    [System.IO.File]::WriteAllText($Path, $Content, $script:Utf8NoBom)
}

function Get-Timestamp {
    return (Get-Date).ToString("yyyy-MM-dd")
}

function Get-TimestampFull {
    return (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")
}

#endregion

#region YAML Frontmatter Parser

function ConvertFrom-YamlFrontmatter {
    <#
    .SYNOPSIS
        Parse le frontmatter YAML d un fichier markdown.
    .PARAMETER Content
        Contenu brut du fichier markdown.
    .OUTPUTS
        PSCustomObject avec .Frontmatter (hashtable) et .Body (string)
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Content
    )

    $result = [PSCustomObject]@{
        Frontmatter = @{}
        Body = ""
    }

    if (-not $Content.StartsWith("---")) {
        $result.Body = $Content
        return $result
    }

    $lines = $Content -split "`n"
    $inFrontmatter = $false
    $frontmatterLines = @()
    $bodyStart = 0

    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i].TrimEnd("`r")
        if ($i -eq 0 -and $line -eq "---") {
            $inFrontmatter = $true
            continue
        }
        if ($inFrontmatter -and $line -eq "---") {
            $bodyStart = $i + 1
            break
        }
        if ($inFrontmatter) {
            $frontmatterLines += $line
        }
    }

    # Parse simple YAML (cles: valeurs)
    $fm = @{}
    foreach ($fmLine in $frontmatterLines) {
        if ($fmLine -match '^\s*(\w[\w_-]*)\s*:\s*(.*)$') {
            $key = $Matches[1]
            $value = $Matches[2].Trim()

            # Nettoyer les guillemets
            if ($value -match '^"(.*)"$') {
                $value = $Matches[1]
            }
            elseif ($value -match "^'(.*)'$") {
                $value = $Matches[1]
            }

            # Detecter les listes inline [item1, item2]
            if ($value -match '^\[(.*)\]$') {
                $items = $Matches[1] -split '\s*,\s*'
                $value = @($items | ForEach-Object { $_.Trim().Trim('"').Trim("'") } | Where-Object { $_ -ne '' })
            }

            # Detecter les nombres
            if ($value -is [string] -and $value -match '^\d+$') {
                $value = [int]$value
            }

            # Detecter null
            if ($value -is [string] -and ($value -eq 'null' -or $value -eq '~' -or $value -eq '')) {
                $value = $null
            }

            $fm[$key] = $value
        }
    }

    $result.Frontmatter = $fm
    if ($bodyStart -lt $lines.Count) {
        $result.Body = ($lines[$bodyStart..($lines.Count - 1)] -join "`n").TrimStart("`n")
    }

    return $result
}

function ConvertTo-YamlFrontmatter {
    <#
    .SYNOPSIS
        Convertit un hashtable en frontmatter YAML + body.
    #>
    param(
        [Parameter(Mandatory)]
        [hashtable]$Frontmatter,
        [string]$Body = ""
    )

    $yamlLines = @("---")
    # Ordre prefere des cles
    $orderedKeys = @(
        'service', 'slug', 'category', 'host', 'port', 'protocol', 'vm',
        'criticality', 'auth_type', 'created', 'last_rotated',
        'rotation_interval_days', 'last_validated', 'validation_status', 'tags'
    )

    $writtenKeys = @{}
    foreach ($key in $orderedKeys) {
        if ($Frontmatter.ContainsKey($key)) {
            $yamlLines += Format-YamlValue -Key $key -Value $Frontmatter[$key]
            $writtenKeys[$key] = $true
        }
    }

    # Ecrire les cles restantes
    foreach ($key in $Frontmatter.Keys) {
        if (-not $writtenKeys.ContainsKey($key)) {
            $yamlLines += Format-YamlValue -Key $key -Value $Frontmatter[$key]
        }
    }

    $yamlLines += "---"
    $content = ($yamlLines -join "`n")
    if ($Body) {
        $content += "`n`n" + $Body
    }
    return $content
}

function Format-YamlValue {
    param([string]$Key, $Value)
    if ($null -eq $Value) {
        return "${Key}: null"
    }
    if ($Value -is [array]) {
        $items = ($Value | ForEach-Object { '"' + $_ + '"' }) -join ', '
        return "${Key}: [$items]"
    }
    if ($Value -is [int]) {
        return "${Key}: $Value"
    }
    return "${Key}: `"$Value`""
}

#endregion

#region CRUD Operations

function Get-CredentialEntry {
    <#
    .SYNOPSIS
        Lit une entree du registre par slug.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Slug
    )

    $filePath = Join-Path $script:RegistryPath "$Slug.md"
    if (-not (Test-Path $filePath)) {
        Write-Error "Credential '$Slug' not found in registry"
        return $null
    }

    $content = [System.IO.File]::ReadAllText($filePath, [System.Text.Encoding]::UTF8)
    $parsed = ConvertFrom-YamlFrontmatter -Content $content
    $parsed | Add-Member -NotePropertyName "Slug" -NotePropertyValue $Slug -Force
    $parsed | Add-Member -NotePropertyName "FilePath" -NotePropertyValue $filePath -Force
    return $parsed
}

function Get-AllCredentialEntries {
    <#
    .SYNOPSIS
        Lit toutes les entrees du registre.
    #>
    $entries = @()
    $files = Get-ChildItem -Path $script:RegistryPath -Filter "*.md" -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        $slug = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
        $entry = Get-CredentialEntry -Slug $slug
        if ($entry) {
            $entries += $entry
        }
    }
    return $entries
}

function Set-CredentialEntry {
    <#
    .SYNOPSIS
        Cree ou met a jour une entree du registre.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Slug,
        [Parameter(Mandatory)]
        [hashtable]$Frontmatter,
        [string]$Body = ""
    )

    $filePath = Join-Path $script:RegistryPath "$Slug.md"
    $content = ConvertTo-YamlFrontmatter -Frontmatter $Frontmatter -Body $Body
    Write-Utf8File -Path $filePath -Content $content
    Write-Host "  Credential '$Slug' saved to $filePath" -ForegroundColor Green
    return $filePath
}

function Remove-CredentialEntry {
    <#
    .SYNOPSIS
        Archive et supprime une entree du registre.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Slug
    )

    $filePath = Join-Path $script:RegistryPath "$Slug.md"
    if (-not (Test-Path $filePath)) {
        Write-Error "Credential '$Slug' not found"
        return $false
    }

    # Archiver avant suppression
    $archivePath = Join-Path $script:RegistryPath "_archive"
    if (-not (Test-Path $archivePath)) {
        New-Item -ItemType Directory -Path $archivePath -Force | Out-Null
    }
    $timestamp = (Get-Date).ToString("yyyyMMdd-HHmmss")
    $archiveFile = Join-Path $archivePath "${Slug}_${timestamp}.md"
    Copy-Item -Path $filePath -Destination $archiveFile -Force
    Remove-Item -Path $filePath -Force

    Write-Host "  Credential '$Slug' archived to $archiveFile" -ForegroundColor Yellow
    return $true
}

#endregion

#region Search & Filter

function Search-Credentials {
    <#
    .SYNOPSIS
        Recherche dans le registre avec filtres.
    #>
    param(
        [string]$Category,
        [string]$VM,
        [string]$Status,
        [string]$Criticality,
        [string]$Query
    )

    $entries = Get-AllCredentialEntries
    $results = @()

    foreach ($entry in $entries) {
        $fm = $entry.Frontmatter
        $match = $true

        if ($Category -and $fm['category'] -ne $Category) { $match = $false }
        if ($VM -and $fm['vm'] -ne $VM) { $match = $false }
        if ($Status -and $fm['validation_status'] -ne $Status) { $match = $false }
        if ($Criticality -and $fm['criticality'] -ne $Criticality) { $match = $false }
        if ($Query) {
            $searchText = ($fm['service'], $fm['slug'], $fm['category'], $fm['vm'], ($fm['tags'] -join ' ')) -join ' '
            if ($searchText -notmatch [regex]::Escape($Query)) { $match = $false }
        }

        if ($match) {
            $results += $entry
        }
    }

    return $results
}

#endregion

#region Index Management

function Update-CredentialIndex {
    <#
    .SYNOPSIS
        Reconstruit l index _index.json a partir des fichiers registre.
    #>
    $entries = Get-AllCredentialEntries
    $indexEntries = @()

    foreach ($entry in $entries) {
        $fm = $entry.Frontmatter
        $indexEntries += @{
            slug = $entry.Slug
            service = $fm['service']
            category = $fm['category']
            host = $fm['host']
            vm = $fm['vm']
            criticality = $fm['criticality']
            auth_type = $fm['auth_type']
            validation_status = $fm['validation_status']
            last_validated = $fm['last_validated']
            last_rotated = $fm['last_rotated']
            rotation_interval_days = $fm['rotation_interval_days']
        }
    }

    $index = @{
        version = "1.0.0"
        generated = Get-TimestampFull
        count = $indexEntries.Count
        entries = $indexEntries
    }

    $json = $index | ConvertTo-Json -Depth 5
    Write-Utf8File -Path $script:IndexPath -Content $json
    Write-Host "  Index updated: $($indexEntries.Count) entries" -ForegroundColor Cyan
    return $index
}

#endregion

#region Rotation Log

function Add-RotationLog {
    <#
    .SYNOPSIS
        Ajoute une entree au log de rotation (append-only JSONL).
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Slug,
        [string]$Action = "rotated",
        [string]$OldHash = "",
        [string]$NewHash = "",
        [string]$Notes = ""
    )

    $logPath = Join-Path $script:DataPath "logs\rotation-log.jsonl"
    $parentDir = Split-Path -Parent $logPath
    if (-not (Test-Path $parentDir)) {
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
    }

    $entry = @{
        timestamp = Get-TimestampFull
        slug = $Slug
        action = $Action
        old_hash = $OldHash
        new_hash = $NewHash
        notes = $Notes
    } | ConvertTo-Json -Compress

    [System.IO.File]::AppendAllText($logPath, $entry + "`n", $script:Utf8NoBom)
}

#endregion

# Export des fonctions
Export-ModuleMember -Function @(
    'ConvertFrom-YamlFrontmatter',
    'ConvertTo-YamlFrontmatter',
    'Get-CredentialEntry',
    'Get-AllCredentialEntries',
    'Set-CredentialEntry',
    'Remove-CredentialEntry',
    'Search-Credentials',
    'Update-CredentialIndex',
    'Add-RotationLog',
    'Write-Utf8File',
    'Get-Timestamp',
    'Get-TimestampFull'
)
