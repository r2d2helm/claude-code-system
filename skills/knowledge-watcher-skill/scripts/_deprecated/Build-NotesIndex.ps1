#Requires -Version 5.1
<#
.SYNOPSIS
    Construit l'index des notes existantes pour l'auto-linking

.DESCRIPTION
    Scanne le vault Obsidian et crée un index JSON avec :
    - Titres des notes
    - Aliases (depuis frontmatter)
    - Tags
    - Chemins des fichiers

.PARAMETER VaultPath
    Chemin du vault Obsidian

.PARAMETER OutputPath
    Chemin du fichier d'index (défaut: data/notes-index.json)

.EXAMPLE
    .\Build-NotesIndex.ps1
    .\Build-NotesIndex.ps1 -VaultPath "C:\MyVault"
#>

[CmdletBinding()]
param(
    [string]$VaultPath,
    [string]$OutputPath
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $SkillPath "scripts\KnowledgeWatcher.psm1") -Force

# Charger la config si pas de paramètres
if (-not $VaultPath) {
    $config = Get-KWConfig
    $VaultPath = $config.paths.obsidianVault
}

if (-not $OutputPath) {
    $OutputPath = Join-Path $SkillPath "data\notes-index.json"
}

function Get-NoteFrontmatter {
    <#
    .SYNOPSIS
        Extrait le frontmatter YAML d'une note
    #>
    param([string]$Content)

    $frontmatter = @{
        title = $null
        aliases = @()
        tags = @()
    }

    if ($Content -match '^---\s*\r?\n([\s\S]*?)\r?\n---') {
        $yaml = $Matches[1]

        # Extraire title
        if ($yaml -match 'title:\s*["\u0027]?([^"\u0027\r\n]+)["\u0027]?') {
            $frontmatter.title = $Matches[1].Trim()
        }

        # Extraire aliases (format liste YAML)
        if ($yaml -match 'aliases:\s*\[([^\]]*)\]') {
            $aliasStr = $Matches[1]
            $frontmatter.aliases = $aliasStr -split ',' | ForEach-Object {
                $_.Trim().Trim('"').Trim("'")
            } | Where-Object { $_ }
        }
        elseif ($yaml -match 'aliases:\s*\r?\n((?:\s*-\s*.+\r?\n?)+)') {
            $aliasLines = $Matches[1]
            $frontmatter.aliases = $aliasLines -split '\r?\n' | ForEach-Object {
                if ($_ -match '^\s*-\s*(.+)$') {
                    $Matches[1].Trim().Trim('"').Trim("'")
                }
            } | Where-Object { $_ }
        }

        # Extraire tags
        if ($yaml -match 'tags:\s*\[([^\]]*)\]') {
            $tagStr = $Matches[1]
            $frontmatter.tags = $tagStr -split ',' | ForEach-Object {
                $_.Trim().Trim('"').Trim("'")
            } | Where-Object { $_ }
        }
        elseif ($yaml -match 'tags:\s*\r?\n((?:\s*-\s*.+\r?\n?)+)') {
            $tagLines = $Matches[1]
            $frontmatter.tags = $tagLines -split '\r?\n' | ForEach-Object {
                if ($_ -match '^\s*-\s*(.+)$') {
                    $Matches[1].Trim().Trim('"').Trim("'")
                }
            } | Where-Object { $_ }
        }
    }

    return $frontmatter
}

function Get-NoteTitle {
    <#
    .SYNOPSIS
        Extrait le titre d'une note (frontmatter ou premier heading)
    #>
    param(
        [string]$Content,
        [string]$FileName
    )

    # D'abord chercher dans le frontmatter
    $fm = Get-NoteFrontmatter -Content $Content
    if ($fm.title) {
        return $fm.title
    }

    # Sinon chercher le premier heading
    if ($Content -match '^#\s+(.+)$') {
        return $Matches[1].Trim()
    }

    # Fallback: nom du fichier sans extension
    return [System.IO.Path]::GetFileNameWithoutExtension($FileName)
}

function Build-Index {
    <#
    .SYNOPSIS
        Construit l'index complet des notes
    #>

    Write-Host "Building notes index from: $VaultPath" -ForegroundColor Cyan

    if (-not (Test-Path $VaultPath)) {
        Write-Error "Vault path not found: $VaultPath"
        return
    }

    $notes = @()
    $terms = @{}  # Table de lookup: terme -> note paths

    # Scanner tous les fichiers .md
    $mdFiles = Get-ChildItem -Path $VaultPath -Filter "*.md" -Recurse -File

    $count = 0
    foreach ($file in $mdFiles) {
        # Ignorer certains dossiers
        $relativePath = $file.FullName.Substring($VaultPath.Length + 1)
        if ($relativePath -match '^_Templates\\|^\.obsidian\\') {
            continue
        }

        try {
            $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
            if ([string]::IsNullOrWhiteSpace($content)) {
                continue
            }

            $fm = Get-NoteFrontmatter -Content $content
            $title = Get-NoteTitle -Content $content -FileName $file.Name
            $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)

            # Construire l'entrée de note
            $noteEntry = @{
                path = $file.FullName
                relativePath = $relativePath
                baseName = $baseName
                title = $title
                aliases = $fm.aliases
                tags = $fm.tags
                lastModified = $file.LastWriteTime.ToString("o")
            }

            $notes += $noteEntry

            # Ajouter les termes de recherche
            $searchTerms = @($title, $baseName) + $fm.aliases | Where-Object { $_ } | Select-Object -Unique

            foreach ($term in $searchTerms) {
                $termLower = $term.ToLower()
                if (-not $terms.ContainsKey($termLower)) {
                    $terms[$termLower] = @{
                        original = $term
                        paths = @()
                    }
                }
                if ($file.FullName -notin $terms[$termLower].paths) {
                    $terms[$termLower].paths += $file.FullName
                }
            }

            $count++
        }
        catch {
            Write-KWLog -Message "Failed to index: $($file.FullName) - $_" -Level "WARN"
        }
    }

    # Construire l'index final
    $index = @{
        version = "1.0"
        vaultPath = $VaultPath
        generatedAt = (Get-Date).ToString("o")
        noteCount = $notes.Count
        termCount = $terms.Count
        notes = $notes
        terms = $terms
    }

    # Sauvegarder l'index
    $jsonContent = $index | ConvertTo-Json -Depth 10
    Write-Utf8File -Path $OutputPath -Content $jsonContent

    Write-Host "Index built successfully!" -ForegroundColor Green
    Write-Host "  Notes: $($notes.Count)" -ForegroundColor Gray
    Write-Host "  Terms: $($terms.Count)" -ForegroundColor Gray
    Write-Host "  Output: $OutputPath" -ForegroundColor Gray

    Write-KWLog -Message "Built notes index: $($notes.Count) notes, $($terms.Count) terms" -Level "INFO"

    return $index
}

# Exécution
Build-Index
