$vault = "C:\Users\r2d2\Documents\Knowledge"
$indexFile = "C:\Users\r2d2\.claude\skills\knowledge-watcher-skill\data\notes-index.json"
$mdFiles = Get-ChildItem $vault -Recurse -Filter "*.md" | Where-Object { $_.FullName -notmatch "\.obsidian" -and $_.FullName -notmatch "_Templates" }
$terms = @{}
foreach ($f in $mdFiles) {
    $rel = $f.FullName.Substring($vault.Length + 1).Replace("\","/")
    $bn = $f.BaseName
    $normalized = $bn.ToLower() -replace "[_\-\s]+", " "
    $words = $normalized -split "\s+"
    foreach ($w in $words) {
        if ($w.Length -lt 2) { continue }
        if (-not $terms.ContainsKey($w)) { $terms[$w] = @{paths=@();original=@()} }
        if ($rel -notin $terms[$w].paths) { $terms[$w].paths += $rel }
        if ($bn -notin $terms[$w].original) { $terms[$w].original += $bn }
    }
    if (-not $terms.ContainsKey($normalized)) { $terms[$normalized] = @{paths=@();original=@()} }
    if ($rel -notin $terms[$normalized].paths) { $terms[$normalized].paths += $rel }
    if ($bn -notin $terms[$normalized].original) { $terms[$normalized].original += $bn }
    $prefixes = @("C_","Conv_","Fix_")
    foreach ($p in $prefixes) {
        if ($bn.StartsWith($p)) {
            $short = ($bn.Substring($p.Length).ToLower() -replace "[_\-\s]+", " ").Trim()
            if ($short.Length -ge 2 -and -not $terms.ContainsKey($short)) { $terms[$short] = @{paths=@();original=@()} }
            if ($short.Length -ge 2) {
                if ($rel -notin $terms[$short].paths) { $terms[$short].paths += $rel }
                if ($bn -notin $terms[$short].original) { $terms[$short].original += $bn }
            }
        }
    }
}
$index = @{
    version = "2.0"
    generatedAt = (Get-Date).ToString("o")
    vaultPath = $vault
    noteCount = $mdFiles.Count
    termCount = $terms.Count
    terms = $terms
}
$json = $index | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText($indexFile, $json, [System.Text.UTF8Encoding]::new($false))
Write-Host "Index rebuilt: $($mdFiles.Count) notes, $($terms.Count) terms"
