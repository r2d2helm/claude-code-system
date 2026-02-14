#Requires -Version 5.1
<#
.SYNOPSIS
    One-shot script to fix broken wikilinks in the vault.
    Replaces [[X]] with [[C_X]] where a C_X note exists in the index.
    Also removes wikilinks that point to non-existent notes.

.PARAMETER VaultPath
    Path to the Obsidian vault

.PARAMETER DryRun
    Preview changes without modifying files

.EXAMPLE
    .\Fix-BrokenWikilinks.ps1 -DryRun
    .\Fix-BrokenWikilinks.ps1
#>
param(
    [string]$VaultPath = 'C:\Users\r2d2\Documents\Knowledge',
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$utf8 = New-Object System.Text.UTF8Encoding($false)

# Load the notes index
$skillPath = Split-Path -Parent $PSScriptRoot
$indexPath = Join-Path $skillPath "data\notes-index.json"

if (-not (Test-Path $indexPath)) {
    Write-Error "Notes index not found at: $indexPath"
    return
}

$indexContent = [System.IO.File]::ReadAllText($indexPath, $utf8)
$index = $indexContent | ConvertFrom-Json

# Build a set of all known note basenames (originals)
$knownNotes = @{}
foreach ($termProp in $index.terms.PSObject.Properties) {
    $originals = @($termProp.Value.original)
    foreach ($orig in $originals) {
        $knownNotes[$orig] = $true
    }
}

# Build a mapping: bare name -> C_* name (for concepts that exist)
$conceptMap = @{}
foreach ($termProp in $index.terms.PSObject.Properties) {
    $originals = @($termProp.Value.original)
    foreach ($orig in $originals) {
        if ($orig -match '^C_(.+)$') {
            $bareName = $Matches[1]
            # Map the bare name to the C_ version
            if (-not $conceptMap.ContainsKey($bareName)) {
                $conceptMap[$bareName] = $orig
            }
        }
    }
}

Write-Host "=== Fix Broken Wikilinks ===" -ForegroundColor Cyan
Write-Host "Vault: $VaultPath"
Write-Host "Known notes: $($knownNotes.Count)"
Write-Host "Concept mappings (bare -> C_): $($conceptMap.Count)"
Write-Host ""

# Terms to remove wikilinks for (no corresponding note exists)
$removeTerms = @(
    "requirements", "prompt", "solution", "process", "architecture",
    "planning", "examples", "support", "instructions"
)

# Scan all markdown files in the vault
$files = Get-ChildItem $VaultPath -Recurse -Filter '*.md' -File |
    Where-Object { $_.FullName -notmatch '[\\/]_Templates[\\/]|[\\/]\.obsidian[\\/]|[\\/]\.git[\\/]' }

$totalFixed = 0
$totalRemoved = 0
$filesModified = 0
$details = @()

foreach ($file in $files) {
    try {
        $content = [System.IO.File]::ReadAllText($file.FullName, $utf8)
    } catch { continue }

    $originalContent = $content
    $fileChanges = @()

    # Find all wikilinks [[X]] (not [[X|Y]] piped links)
    $linkMatches = [regex]::Matches($content, '\[\[([^\]|]+)\]\]')

    foreach ($linkMatch in $linkMatches) {
        $target = $linkMatch.Groups[1].Value

        # Skip if already C_ prefixed or date-prefixed
        if ($target -match '^C_') { continue }
        if ($target -match '^\d{4}-\d{2}-\d{2}') { continue }
        # Skip if it's already a known note
        if ($knownNotes.ContainsKey($target)) { continue }

        # Check if a C_ version exists
        if ($conceptMap.ContainsKey($target)) {
            $newTarget = $conceptMap[$target]
            $content = $content.Replace("[[${target}]]", "[[${newTarget}]]")
            $fileChanges += "  [[${target}]] -> [[${newTarget}]]"
            $totalFixed++
        }
        # Check if this is a term that should have its wikilink removed
        elseif ($target.ToLower() -in $removeTerms) {
            $content = $content.Replace("[[${target}]]", $target)
            $fileChanges += "  [[${target}]] -> ${target} (removed link)"
            $totalRemoved++
        }
    }

    if ($content -ne $originalContent) {
        $filesModified++
        $relPath = $file.FullName.Substring($VaultPath.Length + 1)
        Write-Host "$relPath :" -ForegroundColor Yellow
        foreach ($change in $fileChanges) {
            Write-Host $change -ForegroundColor Gray
        }

        $details += @{
            File = $relPath
            Changes = $fileChanges
        }

        if (-not $DryRun) {
            [System.IO.File]::WriteAllText($file.FullName, $content, $utf8)
        }
    }
}

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "Files modified: $filesModified"
Write-Host "Links fixed (X -> C_X): $totalFixed"
Write-Host "Links removed (no target): $totalRemoved"
Write-Host "Total changes: $($totalFixed + $totalRemoved)"

if ($DryRun) {
    Write-Host ""
    Write-Host "(DRY RUN - no files were modified)" -ForegroundColor Yellow
    Write-Host "Run without -DryRun to apply changes." -ForegroundColor Yellow
}

return [PSCustomObject]@{
    FilesModified = $filesModified
    LinksFixed = $totalFixed
    LinksRemoved = $totalRemoved
    TotalChanges = $totalFixed + $totalRemoved
    Details = $details
}
