# Daily Maintenance Script - 4 checks
$vault = "C:\Users\r2d2\Documents\Knowledge"

# ===========================================
# 1. VAULT HEALTH
# ===========================================
Write-Host "=== 1. VAULT HEALTH ==="
$mdFiles = Get-ChildItem $vault -Recurse -Filter "*.md" | Where-Object { $_.FullName -notmatch "\.obsidian" -and $_.FullName -notmatch "_Templates" }
$total = $mdFiles.Count
Write-Host "  Total notes: $total"

$noFrontmatter = 0
$noTitle = 0
$noType = 0
$noStatus = 0
$noTags = 0
foreach ($f in $mdFiles) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    if ($content -notmatch "^---") { $noFrontmatter++; continue }
    if ($content -notmatch "title:") { $noTitle++ }
    if ($content -notmatch "type:") { $noType++ }
    if ($content -notmatch "status:") { $noStatus++ }
    if ($content -notmatch "tags:") { $noTags++ }
}
Write-Host "  Sans frontmatter: $noFrontmatter"
Write-Host "  Sans title: $noTitle | Sans type: $noType | Sans status: $noStatus | Sans tags: $noTags"

$allNames = $mdFiles | ForEach-Object { $_.BaseName }
$brokenLinks = 0
$linkedTo = @{}
foreach ($f in $mdFiles) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    $wikiMatches = [regex]::Matches($content, "\[\[([^\]|#]+)")
    foreach ($m in $wikiMatches) {
        $target = $m.Groups[1].Value.Trim()
        if (-not $linkedTo.ContainsKey($target)) { $linkedTo[$target] = 0 }
        $linkedTo[$target]++
        if ($target -notin $allNames) { $brokenLinks++ }
    }
}
$orphans = @()
foreach ($f in $mdFiles) {
    $bn = $f.BaseName
    if ($f.FullName -match "_Daily|_Index|_Inbox") { continue }
    if (-not $linkedTo.ContainsKey($bn)) { $orphans += $bn }
}
Write-Host "  Liens casses: $brokenLinks"
Write-Host "  Orphelins: $($orphans.Count)"

$fmScore = [math]::Max(0, 100 - ($noFrontmatter * 5) - ($noTitle * 1) - ($noType * 1) - ($noStatus * 0.5) - ($noTags * 0.5))
$linkScore = [math]::Max(0, 100 - ($brokenLinks * 0.5) - ($orphans.Count * 0.3))
$healthScore = [math]::Round(($fmScore + $linkScore) / 2)
Write-Host "  Score: $healthScore/100"

# ===========================================
# 2. WATCHER QUEUE
# ===========================================
Write-Host ""
Write-Host "=== 2. WATCHER QUEUE ==="
$queueFile = "C:\Users\r2d2\.claude\skills\knowledge-watcher-skill\data\queue.json"
if (Test-Path $queueFile) {
    $queue = Get-Content $queueFile -Raw -Encoding UTF8 | ConvertFrom-Json
    $items = $queue.items
    $totalQ = if ($items) { $items.Count } else { 0 }
    $pending = @($items | Where-Object { $_.status -eq "pending" }).Count
    $completed = @($items | Where-Object { $_.status -eq "completed" }).Count
    $errors = @($items | Where-Object { $_.status -eq "error" }).Count
    $skipped = @($items | Where-Object { $_.status -eq "skipped" }).Count
    Write-Host "  Total: $totalQ items"
    Write-Host "  Pending: $pending | Completed: $completed | Errors: $errors | Skipped: $skipped"
    $lastMod = (Get-Item $queueFile).LastWriteTime.ToString("yyyy-MM-dd HH:mm")
    Write-Host "  Derniere MAJ: $lastMod"
} else {
    Write-Host "  Queue file not found"
}

$stateFile = "C:\Users\r2d2\.claude\skills\knowledge-watcher-skill\data\state.json"
if (Test-Path $stateFile) {
    $state = Get-Content $stateFile -Raw -Encoding UTF8 | ConvertFrom-Json
    $watchers = $state.watchers
    if ($watchers) {
        $active = @($watchers | Where-Object { $_.pid }).Count
        Write-Host "  Watchers: $active/$($watchers.Count)"
    } else { Write-Host "  Watchers: aucun" }
} else {
    Write-Host "  State file not found"
}

# ===========================================
# 3. INDEX DES NOTES
# ===========================================
Write-Host ""
Write-Host "=== 3. INDEX DES NOTES ==="
$indexFile = "C:\Users\r2d2\.claude\skills\knowledge-watcher-skill\data\notes-index.json"
$actualNotes = $mdFiles.Count

if (Test-Path $indexFile) {
    $index = Get-Content $indexFile -Raw -Encoding UTF8 | ConvertFrom-Json
    $indexedCount = $index.noteCount
    $termCount = $index.termCount
    $genAt = $index.generatedAt
    $lastMod = (Get-Item $indexFile).LastWriteTime.ToString("yyyy-MM-dd HH:mm")
    $delta = $actualNotes - $indexedCount
    Write-Host "  Indexees: $indexedCount | Reelles: $actualNotes | Delta: $delta"
    Write-Host "  Termes: $termCount"
    Write-Host "  Genere: $genAt"
    if ($delta -gt 5) { Write-Host "  STATUS: SYNC NEEDED" } else { Write-Host "  STATUS: OK" }
} else {
    Write-Host "  Index file not found - REBUILD NEEDED"
}

# ===========================================
# 4. SKILLS INTEGRITY
# ===========================================
Write-Host ""
Write-Host "=== 4. SKILLS INTEGRITY ==="
$skillsDir = "C:\Users\r2d2\.claude\skills"
$skillDirs = Get-ChildItem $skillsDir -Directory | Where-Object { $_.Name -match "-skill$|^sop-|^skill-" }
$okCount = 0
$issues = @()
foreach ($d in $skillDirs) {
    $skillMd = Join-Path $d.FullName "SKILL.md"
    if (Test-Path $skillMd) { $okCount++ }
    else { $issues += "MISSING: $($d.Name)" }
}
Write-Host "  Skills avec SKILL.md: $okCount/$($skillDirs.Count)"

$routerFile = Join-Path $skillsDir "SKILL.md"
if (Test-Path $routerFile) {
    $routerContent = Get-Content $routerFile -Raw -Encoding UTF8
    $missing = @()
    foreach ($d in $skillDirs) {
        if ($routerContent -notmatch $d.Name) { $missing += $d.Name }
    }
    if ($missing.Count -gt 0) { Write-Host "  Non references: $($missing -join ', ')" }
    else { Write-Host "  Meta-router: coherent" }
}

$cmdDir = "C:\Users\r2d2\.claude\commands"
$cmds = (Get-ChildItem $cmdDir -Filter "*.md").Count
Write-Host "  Commandes globales: $cmds"

if ($issues.Count -eq 0) { Write-Host "  STATUS: OK" }
else { foreach ($i in $issues) { Write-Host "  ISSUE: $i" } }
