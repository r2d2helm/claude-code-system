#Requires -Version 5.1
<#
.SYNOPSIS
    Auto-Linker - Ajoute automatiquement des liens wiki vers les notes existantes

.DESCRIPTION
    Analyse le contenu d'une note et ajoute des liens [[...]] vers les notes
    existantes dans le vault. Utilise matching exact et fuzzy.

.NOTES
    Stratégies de matching:
    1. Exact: correspondance exacte du titre/alias (insensible à la casse)
    2. Fuzzy: tolère pluriel, accents, tirets/espaces
#>

$script:SkillPath = Split-Path -Parent $PSScriptRoot
Import-Module (Join-Path $script:SkillPath "scripts\KnowledgeWatcher.psm1") -Force

# Cache de l'index
$script:NotesIndex = $null
$script:IndexLoadedAt = $null

# Termes à exclure - chargés depuis config.json si disponible, sinon fallback hardcodé
$script:ExcludedTerms = $null

function Get-ExcludedTerms {
    if ($null -ne $script:ExcludedTerms) { return $script:ExcludedTerms }

    try {
        $config = Get-KWConfig
        if ($config.autoLinker -and $config.autoLinker.excludedTerms) {
            $script:ExcludedTerms = @($config.autoLinker.excludedTerms)
            return $script:ExcludedTerms
        }
    } catch { }

    # Fallback hardcodé
    $script:ExcludedTerms = @(
        "solution", "claude", "skill", "para", "note", "notes", "test", "tests",
        "file", "files", "code", "data", "type", "name", "path", "index", "list",
        "item", "items", "task", "tasks", "link", "links", "tag", "tags",
        "date", "time", "user", "config", "error", "debug", "info", "warn",
        "true", "false", "null", "string", "number", "object", "array",
        "new", "old", "get", "set", "add", "remove", "update", "delete",
        "start", "stop", "run", "execute", "process", "create", "build",
        "input", "output", "result", "value", "key", "id", "status",
        "readme", "agents", "examples", "support", "prompts", "planning",
        "architecture", "initial", "setup-instructions", "instructions",
        "exercise", "fonctionnement", "prompt-templates",
        "api", "url", "cli", "gui", "sdk", "ide"
    )
    return $script:ExcludedTerms
}

function Get-NotesIndex {
    <#
    .SYNOPSIS
        Charge l'index des notes (avec cache de 5 minutes)
    #>
    [CmdletBinding()]
    param([switch]$ForceReload)

    $indexPath = Join-Path $script:SkillPath "data\notes-index.json"

    if (-not (Test-Path $indexPath)) {
        Write-KWLog -Message "Notes index not found, building..." -Level "WARN"
        & (Join-Path $script:SkillPath "scripts\Build-NotesIndex.ps1")
    }

    # Vérifier le cache (configurable, défaut 5 minutes)
    $cacheTtl = 5
    try {
        $cfg = Get-KWConfig
        if ($cfg.autoLinker -and $cfg.autoLinker.cacheTtlMinutes) {
            $cacheTtl = $cfg.autoLinker.cacheTtlMinutes
        }
    } catch { }
    $cacheValid = $script:NotesIndex -and $script:IndexLoadedAt -and `
        ((Get-Date) - $script:IndexLoadedAt).TotalMinutes -lt $cacheTtl

    if ($cacheValid -and -not $ForceReload) {
        return $script:NotesIndex
    }

    # Charger l'index
    $content = Read-Utf8File -Path $indexPath
    $script:NotesIndex = $content | ConvertFrom-Json
    $script:IndexLoadedAt = Get-Date

    return $script:NotesIndex
}

function Remove-Diacritics {
    <#
    .SYNOPSIS
        Supprime les accents d'une chaîne
    #>
    param([string]$Text)

    $normalized = $Text.Normalize([System.Text.NormalizationForm]::FormD)
    $sb = New-Object System.Text.StringBuilder

    foreach ($char in $normalized.ToCharArray()) {
        $category = [System.Globalization.CharUnicodeInfo]::GetUnicodeCategory($char)
        if ($category -ne [System.Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$sb.Append($char)
        }
    }

    return $sb.ToString()
}

function Get-FuzzyVariants {
    <#
    .SYNOPSIS
        Génère les variantes fuzzy d'un terme pour le matching
    #>
    param([string]$Term)

    $variants = @($Term)
    $lower = $Term.ToLower()
    $variants += $lower

    # Sans accents
    $noAccents = Remove-Diacritics $lower
    if ($noAccents -ne $lower) {
        $variants += $noAccents
        # Aussi sans accents avec variantes tirets/espaces
        $variants += $noAccents -replace '-', ' '
        $variants += $noAccents -replace ' ', '-'
    }

    # Avec/sans tirets et espaces
    $variants += $lower -replace '-', ' '
    $variants += $lower -replace ' ', '-'
    $variants += $lower -replace '[-_]', ''
    $variants += $lower -replace '\s+', ''  # Sans espaces

    # Pluriel simple (français/anglais)
    if ($lower.EndsWith('s')) {
        $singular = $lower.Substring(0, $lower.Length - 1)
        $variants += $singular
        $variants += Remove-Diacritics $singular
    } else {
        $variants += "${lower}s"
        $variants += "$(Remove-Diacritics $lower)s"
    }

    # Pluriel français -x → -ux
    if ($lower.EndsWith('x')) {
        $variants += $lower.Substring(0, $lower.Length - 1)
    }

    return $variants | Where-Object { $_ } | Select-Object -Unique
}

function Build-FuzzyPattern {
    <#
    .SYNOPSIS
        Construit un pattern regex pour matcher toutes les variantes fuzzy
    #>
    param([string]$Term)

    $variants = Get-FuzzyVariants -Term $Term

    # Échapper chaque variante et les joindre avec |
    $escapedVariants = $variants | ForEach-Object { [regex]::Escape($_) }
    $alternation = $escapedVariants -join '|'

    # Pattern pour mot entier (insensible à la casse)
    return "(?<!\w)($alternation)(?!\w)"
}

function Find-TermMatches {
    <#
    .SYNOPSIS
        Trouve les correspondances d'un terme dans le contenu
    #>
    param(
        [string]$Content,
        [string]$Term,
        [string]$NotePath  # Pour éviter l'auto-référence
    )

    $index = Get-NotesIndex
    $matches = @()

    # Chercher le terme exact dans l'index
    $termLower = $Term.ToLower()

    if ($index.terms.PSObject.Properties.Name -contains $termLower) {
        $termEntry = $index.terms.$termLower

        # Vérifier que ce n'est pas la même note
        $validPaths = $termEntry.paths | Where-Object { $_ -ne $NotePath }

        if ($validPaths.Count -gt 0) {
            $matches += @{
                term = $termEntry.original
                type = "exact"
                paths = $validPaths
            }
        }
    }

    return $matches
}

function Invoke-AutoLink {
    <#
    .SYNOPSIS
        Ajoute automatiquement des liens wiki au contenu

    .PARAMETER Content
        Contenu de la note

    .PARAMETER NotePath
        Chemin de la note (pour éviter l'auto-référence)

    .PARAMETER MaxLinks
        Nombre maximum de liens à ajouter (défaut: 20)

    .PARAMETER MinTermLength
        Longueur minimale d'un terme (défaut: 5)

    .OUTPUTS
        PSCustomObject avec Content (modifié) et LinksAdded (liste)
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Content,

        [string]$NotePath = "",

        [int]$MaxLinks = 20,

        [int]$MinTermLength = 5
    )

    $index = Get-NotesIndex
    $linksAdded = @()
    $modifiedContent = $Content

    # Extraire le contenu sans frontmatter
    $contentStart = 0
    if ($Content -match '^---\s*\r?\n[\s\S]*?\r?\n---\s*\r?\n') {
        $contentStart = $Matches[0].Length
    }

    $frontmatter = $Content.Substring(0, $contentStart)
    $bodyContent = $Content.Substring($contentStart)

    # Parcourir les termes de l'index (triés par longueur décroissante pour éviter les sous-matches)
    $sortedTerms = $index.terms.PSObject.Properties |
        Sort-Object { $_.Name.Length } -Descending |
        Where-Object { $_.Name.Length -ge $MinTermLength }

    # Tracker les termes déjà liés (pour éviter les sous-termes)
    $linkedTerms = @()

    foreach ($termProp in $sortedTerms) {
        if ($linksAdded.Count -ge $MaxLinks) {
            break
        }

        $termLower = $termProp.Name
        $termData = $termProp.Value
        $originalTerm = $termData.original

        # Vérifier la liste d'exclusions
        $excluded = Get-ExcludedTerms
        if ($termLower -in $excluded) {
            continue
        }

        # Vérifier que ce n'est pas la note elle-même
        $validPaths = @($termData.paths | Where-Object { $_ -ne $NotePath })
        if ($validPaths.Count -eq 0) {
            continue
        }

        # Vérifier si ce terme est un sous-terme d'un terme déjà lié
        $isSubTerm = $false
        foreach ($linked in $linkedTerms) {
            if ($linked.ToLower().Contains($termLower)) {
                $isSubTerm = $true
                break
            }
        }
        if ($isSubTerm) {
            continue
        }

        # Construire le pattern fuzzy (inclut variantes sans accents, pluriel, tirets)
        $fuzzyPattern = Build-FuzzyPattern -Term $originalTerm
        $escapedTerm = [regex]::Escape($originalTerm)

        # Vérifier que ce n'est pas déjà un lien
        if ($bodyContent -match "\[\[$escapedTerm\]\]") {
            continue
        }

        # Chercher une variante fuzzy dans le body
        $matchFound = [regex]::Match($bodyContent, $fuzzyPattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)

        if ($matchFound.Success) {
            # Vérifier que la position n'est pas dans un lien existant [[...]]
            $pos = $matchFound.Index
            $beforeMatch = $bodyContent.Substring(0, $pos)
            $openBrackets = ([regex]::Matches($beforeMatch, '\[\[')).Count
            $closeBrackets = ([regex]::Matches($beforeMatch, '\]\]')).Count

            # Si on n'est pas dans un lien ouvert
            if ($openBrackets -eq $closeBrackets) {
                # Remplacer par le terme original (pas la variante trouvée)
                $replacement = "[[$originalTerm]]"
                $matchedText = $matchFound.Value
                $newBody = $bodyContent.Substring(0, $pos) + $replacement + $bodyContent.Substring($pos + $matchFound.Length)

                if ($newBody -ne $bodyContent) {
                    $bodyContent = $newBody
                    $linksAdded += $originalTerm
                    $linkedTerms += $originalTerm

                    # Log avec la variante trouvée si différente
                    if ($matchedText.ToLower() -ne $originalTerm.ToLower()) {
                        Write-KWLog -Message "Auto-linked (fuzzy): '$matchedText' -> [[$originalTerm]]" -Level "DEBUG"
                    } else {
                        Write-KWLog -Message "Auto-linked: $originalTerm" -Level "DEBUG"
                    }
                }
            }
        }
    }

    # Recombiner frontmatter et body
    $modifiedContent = $frontmatter + $bodyContent

    return [PSCustomObject]@{
        Content = $modifiedContent
        LinksAdded = $linksAdded
        LinkCount = $linksAdded.Count
    }
}

function Update-NoteWithAutoLinks {
    <#
    .SYNOPSIS
        Met à jour une note existante avec des auto-liens

    .PARAMETER NotePath
        Chemin de la note à mettre à jour

    .PARAMETER DryRun
        Si activé, affiche les changements sans modifier le fichier
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$NotePath,

        [switch]$DryRun
    )

    if (-not (Test-Path $NotePath)) {
        Write-Error "Note not found: $NotePath"
        return
    }

    $content = Read-Utf8File -Path $NotePath
    $result = Invoke-AutoLink -Content $content -NotePath $NotePath

    if ($result.LinkCount -eq 0) {
        Write-Host "  No links to add" -ForegroundColor Gray
        return $result
    }

    Write-Host "  Links to add: $($result.LinksAdded -join ', ')" -ForegroundColor Cyan

    if (-not $DryRun) {
        Write-Utf8File -Path $NotePath -Content $result.Content
        Write-Host "  Note updated!" -ForegroundColor Green
        Write-KWLog -Message "Auto-linked $($result.LinkCount) terms in: $NotePath" -Level "INFO"
    }
    else {
        Write-Host "  (Dry run - no changes made)" -ForegroundColor Yellow
    }

    return $result
}

function Invoke-AILinkSuggestions {
    <#
    .SYNOPSIS
        Utilise Claude pour suggérer des liens sémantiques intelligents

    .PARAMETER Content
        Contenu de la note à analyser

    .PARAMETER MaxSuggestions
        Nombre maximum de suggestions (défaut: 5)

    .OUTPUTS
        Array de suggestions avec terme et raison
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Content,

        [int]$MaxSuggestions = 5
    )

    $config = Get-KWConfig
    $index = Get-NotesIndex

    # Extraire les titres des notes existantes (max 100 pour le prompt)
    $existingNotes = $index.notes |
        Select-Object -First 100 |
        ForEach-Object { $_.title } |
        Where-Object { $_ -and $_.Length -gt 3 }

    $notesList = $existingNotes -join "`n- "

    # Construire le prompt pour Claude
    $prompt = @"
Analyse ce contenu et identifie les concepts qui devraient etre lies a des notes existantes.

CONTENU:
$Content

NOTES EXISTANTES DANS LE VAULT:
- $notesList

INSTRUCTIONS:
1. Identifie les concepts importants dans le contenu
2. Pour chaque concept, trouve la note existante la plus pertinente
3. Retourne UNIQUEMENT un JSON valide avec ce format:

{
  "suggestions": [
    {"term": "mot ou phrase dans le contenu", "linkTo": "titre exact de la note existante", "reason": "courte explication"}
  ]
}

REGLES:
- Maximum $MaxSuggestions suggestions
- Le "term" doit etre un mot ou phrase EXACT du contenu
- Le "linkTo" doit etre un titre EXACT d'une note existante
- Ne suggere PAS de liens deja presents [[...]]
- Privilegie les liens semantiques (sens similaire, meme domaine)
"@

    try {
        $claudePath = $config.paths.claudeCli
        if (-not (Test-Path $claudePath)) {
            $claudePath = "claude"
        }

        # Appeler Claude CLI
        $processInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processInfo.FileName = $claudePath
        $processInfo.Arguments = "-p `"$($prompt -replace '"', '\"')`" --output-format json --max-tokens 500"
        $processInfo.RedirectStandardOutput = $true
        $processInfo.RedirectStandardError = $true
        $processInfo.UseShellExecute = $false
        $processInfo.CreateNoWindow = $true
        $processInfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
        $processInfo.StandardErrorEncoding = [System.Text.Encoding]::UTF8

        $process = [System.Diagnostics.Process]::Start($processInfo)
        $output = $process.StandardOutput.ReadToEnd()
        $process.WaitForExit(30000)

        if ($process.ExitCode -ne 0) {
            Write-KWLog -Message "Claude CLI failed for AI suggestions" -Level "WARN"
            return @()
        }

        # Parser la réponse JSON
        # Chercher le JSON dans la sortie
        if ($output -match '\{[\s\S]*"suggestions"[\s\S]*\}') {
            $jsonStr = $Matches[0]
            $result = $jsonStr | ConvertFrom-Json

            if ($result.suggestions) {
                Write-KWLog -Message "AI suggested $($result.suggestions.Count) links" -Level "INFO"
                return $result.suggestions
            }
        }

        return @()
    }
    catch {
        Write-KWLog -Message "AI link suggestions failed: $_" -Level "WARN"
        return @()
    }
}

function Invoke-AutoLinkWithAI {
    <#
    .SYNOPSIS
        Auto-linking enrichi avec suggestions IA

    .PARAMETER Content
        Contenu de la note

    .PARAMETER NotePath
        Chemin de la note

    .PARAMETER UseAI
        Activer les suggestions IA (défaut: true)

    .PARAMETER MaxLinks
        Nombre maximum de liens (défaut: 20)

    .OUTPUTS
        PSCustomObject avec Content modifié et liens ajoutés
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Content,

        [string]$NotePath = "",

        [switch]$UseAI = $true,

        [int]$MaxLinks = 20
    )

    # D'abord appliquer l'auto-linking standard (exact + fuzzy)
    $result = Invoke-AutoLink -Content $Content -NotePath $NotePath -MaxLinks $MaxLinks
    $modifiedContent = $result.Content
    $linksAdded = [System.Collections.ArrayList]@($result.LinksAdded)

    # Si IA activée et qu'on n'a pas atteint le max
    if ($UseAI -and $linksAdded.Count -lt $MaxLinks) {
        Write-KWLog -Message "Requesting AI link suggestions..." -Level "DEBUG"

        $aiSuggestions = Invoke-AILinkSuggestions -Content $modifiedContent -MaxSuggestions ($MaxLinks - $linksAdded.Count)

        foreach ($suggestion in $aiSuggestions) {
            if ($linksAdded.Count -ge $MaxLinks) { break }

            $term = $suggestion.term
            $linkTo = $suggestion.linkTo

            # Vérifier que le terme existe dans le contenu et n'est pas déjà lié
            $escapedTerm = [regex]::Escape($term)
            if ($modifiedContent -match "(?<!\[\[)$escapedTerm(?!\]\])" -and
                $modifiedContent -notmatch "\[\[$escapedTerm\]\]") {

                # Remplacer la première occurrence
                $modifiedContent = $modifiedContent -replace "(?<!\[\[)($escapedTerm)(?!\]\])", "[[$linkTo|`$1]]", 1

                [void]$linksAdded.Add("$term -> $linkTo (AI)")
                Write-KWLog -Message "AI-linked: '$term' -> [[$linkTo]] - $($suggestion.reason)" -Level "DEBUG"
            }
        }
    }

    return [PSCustomObject]@{
        Content = $modifiedContent
        LinksAdded = $linksAdded
        LinkCount = $linksAdded.Count
    }
}

function Invoke-BatchAutoLink {
    <#
    .SYNOPSIS
        Batch auto-linking for multiple notes (especially orphans)
    .PARAMETER VaultPath
        Path to the vault
    .PARAMETER TargetFolder
        Limit to a specific folder (e.g. "Concepts", "Conversations")
    .PARAMETER OrphansOnly
        Only process notes with no outgoing links
    .PARAMETER DryRun
        Preview changes without modifying files
    .PARAMETER MaxNotes
        Maximum notes to process (default: 50)
    #>
    [CmdletBinding()]
    param(
        [string]$VaultPath = 'C:\Users\r2d2\Documents\Knowledge',
        [string]$TargetFolder = "",
        [switch]$OrphansOnly,
        [switch]$DryRun,
        [int]$MaxNotes = 50
    )

    $utf8 = New-Object System.Text.UTF8Encoding($false)
    $index = Get-NotesIndex -ForceReload
    $results = @()
    $totalLinksAdded = 0

    $searchPath = $VaultPath
    if ($TargetFolder) { $searchPath = Join-Path $VaultPath $TargetFolder }

    $files = Get-ChildItem $searchPath -Recurse -Filter '*.md' -File |
        Where-Object { $_.FullName -notmatch '[\\/]_Templates[\\/]|[\\/]\.obsidian[\\/]' }

    $processed = 0
    foreach ($file in $files) {
        if ($processed -ge $MaxNotes) { break }

        try {
            $content = [System.IO.File]::ReadAllText($file.FullName, $utf8)
        } catch { continue }

        if ([string]::IsNullOrWhiteSpace($content)) { continue }

        # If OrphansOnly, skip notes that already have outgoing links
        if ($OrphansOnly) {
            $existingLinks = [regex]::Matches($content, '\[\[([^\]]+)\]\]')
            if ($existingLinks.Count -gt 0) { continue }
        }

        $result = Invoke-AutoLink -Content $content -NotePath $file.FullName
        if ($result.LinkCount -gt 0) {
            $processed++
            $totalLinksAdded += $result.LinkCount

            $relPath = $file.FullName.Substring($VaultPath.Length + 1)
            Write-Host "  $relPath : +$($result.LinkCount) liens ($($result.LinksAdded -join ', '))" -ForegroundColor Cyan

            $results += @{
                File = $relPath
                LinksAdded = $result.LinksAdded
                Count = $result.LinkCount
            }

            if (-not $DryRun) {
                [System.IO.File]::WriteAllText($file.FullName, $result.Content, $utf8)
            }
        }
    }

    Write-Host ""
    Write-Host "Batch auto-link complete:" -ForegroundColor Green
    Write-Host "  Notes processed: $processed"
    Write-Host "  Total links added: $totalLinksAdded"
    if ($DryRun) { Write-Host "  (DRY RUN - no files modified)" -ForegroundColor Yellow }

    return [PSCustomObject]@{
        NotesProcessed = $processed
        TotalLinksAdded = $totalLinksAdded
        Details = $results
    }
}

function Get-LinkSuggestionReport {
    <#
    .SYNOPSIS
        Generate a report of potential links that could be added across the vault
    .PARAMETER VaultPath
        Path to the vault
    .PARAMETER MaxSuggestions
        Maximum suggestions to return (default: 30)
    #>
    [CmdletBinding()]
    param(
        [string]$VaultPath = 'C:\Users\r2d2\Documents\Knowledge',
        [int]$MaxSuggestions = 30
    )

    $utf8 = New-Object System.Text.UTF8Encoding($false)
    $index = Get-NotesIndex -ForceReload
    $suggestions = @()

    $files = Get-ChildItem $VaultPath -Recurse -Filter '*.md' -File |
        Where-Object { $_.FullName -notmatch '[\\/]_Templates[\\/]|[\\/]\.obsidian[\\/]|[\\/]Formations[\\/]' }

    foreach ($file in $files) {
        if ($suggestions.Count -ge $MaxSuggestions) { break }

        try {
            $content = [System.IO.File]::ReadAllText($file.FullName, $utf8)
        } catch { continue }

        if ([string]::IsNullOrWhiteSpace($content)) { continue }

        $result = Invoke-AutoLink -Content $content -NotePath $file.FullName
        if ($result.LinkCount -gt 0) {
            $relPath = $file.FullName.Substring($VaultPath.Length + 1)
            foreach ($link in $result.LinksAdded) {
                $suggestions += @{
                    Source = $relPath
                    SuggestedLink = $link
                }
            }
        }
    }

    Write-Host "=== LINK SUGGESTION REPORT ===" -ForegroundColor Cyan
    Write-Host "Total suggestions: $($suggestions.Count)"
    Write-Host ""

    $grouped = $suggestions | Group-Object { $_.Source }
    foreach ($group in $grouped) {
        Write-Host "  $($group.Name):" -ForegroundColor Yellow
        foreach ($s in $group.Group) {
            Write-Host "    -> [[$($s.SuggestedLink)]]" -ForegroundColor Gray
        }
    }

    return $suggestions
}

# Functions exported via dot-sourcing:
# - Get-NotesIndex
# - Invoke-AutoLink
# - Invoke-AutoLinkWithAI
# - Invoke-AILinkSuggestions
# - Update-NoteWithAutoLinks
# - Remove-Diacritics
# - Get-FuzzyVariants
# - Build-FuzzyPattern
# - Invoke-BatchAutoLink
# - Get-LinkSuggestionReport
# - Get-ExcludedTerms
