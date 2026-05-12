# R2D2 Daily Backup Script
# Runs via Task Scheduler - fail-safe (continues on error)
# Retention: 7 days for daily dumps

$ErrorActionPreference = "Continue"
$date = Get-Date -Format "yyyy-MM-dd"
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$backupRoot = "C:\Users\r2d2\Documents\claude-config-backup"
$dailyDir = "$backupRoot\daily\$date"
$logFile = "C:\Users\r2d2\.claude\hooks\logs\backup.log"

function Log($msg) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | $msg"
    Add-Content -Path $logFile -Value $line -Encoding UTF8
    Write-Host $line
}

# Create directories
New-Item -ItemType Directory -Force -Path $dailyDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path $logFile) | Out-Null

Log "========== BACKUP START $date =========="

# -----------------------------------------------
# 1. GIT REPOS - commit + push to Forgejo (origin) AND GitHub (mirror)
#    Repos: ~/.claude (config), Knowledge (vault), R2D2-Memory (doctrine)
#    Forgejo = forge souveraine sur le Dell (VM 103) ; GitHub = miroir redondant
# -----------------------------------------------
$gitRepos = @(
    @{ Name = "config (~/.claude)"; Path = "C:\Users\r2d2\.claude" },
    @{ Name = "vault (Knowledge)";  Path = "C:\Users\r2d2\Documents\Knowledge" },
    @{ Name = "doctrine (R2D2-Memory)"; Path = "C:\Users\r2d2\Documents\R2D2-Memory" }
)
foreach ($repo in $gitRepos) {
    try {
        if (-not (Test-Path (Join-Path $repo.Path ".git"))) {
            Log "[1/5] $($repo.Name): no .git, skip"
            continue
        }
        Push-Location $repo.Path
        git add -A 2>&1 | Out-Null
        $changes = git status --porcelain
        if ($changes) {
            git commit -m "auto-backup $date" 2>&1 | Out-Null
            Log "[1/5] $($repo.Name): committed"
        } else {
            Log "[1/5] $($repo.Name): no changes"
        }
        $remotes = git remote 2>&1
        foreach ($r in @("origin", "github")) {
            if ($remotes -contains $r) {
                git push $r HEAD 2>&1 | Out-Null
                if ($LASTEXITCODE -eq 0) { Log "[1/5] $($repo.Name): pushed -> $r" }
                else { Log "[1/5] WARN $($repo.Name): push -> $r failed (exit $LASTEXITCODE)" }
            }
        }
        Pop-Location
    } catch {
        Log "[1/5] WARN $($repo.Name) git backup failed: $_"
        try { Pop-Location } catch {}
    }
}

# -----------------------------------------------
# 2. CONFIG CLAUDE - ZIP skills, hooks, commands, agents, memory, PRPs
# -----------------------------------------------
try {
    Log "[2/5] Config Claude - creating ZIP..."
    $claudeDir = "C:\Users\r2d2\.claude"
    $zipPath = "$dailyDir\claude-config-$date.zip"

    # Build list of paths to include
    $includes = @(
        "$claudeDir\CLAUDE.md",
        "$claudeDir\settings.json",
        "$claudeDir\skills",
        "$claudeDir\hooks",
        "$claudeDir\commands",
        "$claudeDir\agents",
        "$claudeDir\PRPs",
        "$claudeDir\mcp-servers",
        "$claudeDir\projects\C--Users-r2d2\memory"
    )

    $existingPaths = $includes | Where-Object { Test-Path $_ }
    Compress-Archive -Path $existingPaths -DestinationPath $zipPath -Force
    $size = [math]::Round((Get-Item $zipPath).Length / 1MB, 1)
    Log "[2/5] Config: $zipPath ($size MB)"
} catch {
    Log "[2/5] WARN Config backup failed: $_"
}

# -----------------------------------------------
# 3. WAREHOUSE + MEMORY SQLite - copy
# -----------------------------------------------
try {
    Log "[3/5] SQLite databases - copying..."
    $dbFiles = @(
        "C:\Users\r2d2\.claude\hooks\data\memory.db",
        "C:\Users\r2d2\.claude\skills\intelligence-warehouse-skill\data\warehouse.db"
    )
    foreach ($db in $dbFiles) {
        if (Test-Path $db) {
            $name = (Split-Path $db -Leaf) -replace '\.db$', "-$date.db"
            Copy-Item $db "$dailyDir\$name" -Force
            Log "[3/5] Copied: $name"
        }
    }
} catch {
    Log "[3/5] WARN SQLite backup failed: $_"
}

# -----------------------------------------------
# 4. POSTGRESQL - pg_dump via SSH
# -----------------------------------------------
try {
    Log "[4/5] PostgreSQL - pg_dump via SSH..."
    $pgDump = "$dailyDir\pg-r2d2agent-$date.sql"
    ssh r2d2helm@192.168.1.163 "PGPASSWORD=r2d2shared pg_dump -h 192.168.1.164 -U r2d2 r2d2agent --no-owner --no-privileges" | Out-File -FilePath $pgDump -Encoding utf8
    if (Test-Path $pgDump) {
        $size = [math]::Round((Get-Item $pgDump).Length / 1KB, 0)
        Log "[4/5] PostgreSQL: $pgDump ($size KB)"
    } else {
        Log "[4/5] WARN PostgreSQL dump empty or failed"
    }
} catch {
    Log "[4/5] WARN PostgreSQL backup failed: $_"
}

# -----------------------------------------------
# 5. SAAS CODE - tarball hebdo (dimanche only)
# -----------------------------------------------
try {
    if ((Get-Date).DayOfWeek -eq "Sunday") {
        Log "[5/5] SaaS code - weekly tarball..."
        $tarPath = "$dailyDir\r2d2-agent-$date.tar.gz"
        ssh r2d2helm@192.168.1.163 "cd ~ && tar czf /tmp/r2d2-backup.tar.gz --exclude='node_modules' --exclude='.next' --exclude='__pycache__' R2D2-Agent/" 2>&1 | Out-Null
        scp r2d2helm@192.168.1.163:/tmp/r2d2-backup.tar.gz $tarPath 2>&1 | Out-Null
        if (Test-Path $tarPath) {
            $size = [math]::Round((Get-Item $tarPath).Length / 1MB, 1)
            Log "[5/5] SaaS: $tarPath ($size MB)"
        }
    } else {
        Log "[5/5] SaaS: skip (not Sunday)"
    }
} catch {
    Log "[5/5] WARN SaaS backup failed: $_"
}

# -----------------------------------------------
# RETENTION: delete daily dirs older than 7 days
# -----------------------------------------------
try {
    Log "Retention: cleaning backups older than 7 days..."
    $cutoff = (Get-Date).AddDays(-7)
    $dailyRoot = "$backupRoot\daily"
    if (Test-Path $dailyRoot) {
        Get-ChildItem $dailyRoot -Directory | Where-Object {
            try { [datetime]::ParseExact($_.Name, "yyyy-MM-dd", $null) -lt $cutoff } catch { $false }
        } | ForEach-Object {
            Remove-Item $_.FullName -Recurse -Force
            Log "Retention: deleted $($_.Name)"
        }
    }
} catch {
    Log "WARN Retention cleanup failed: $_"
}

# -----------------------------------------------
# SUMMARY
# -----------------------------------------------
if (Test-Path $dailyDir) {
    $totalSize = [math]::Round((Get-ChildItem $dailyDir -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB, 1)
    $fileCount = (Get-ChildItem $dailyDir -File).Count
    Log "========== BACKUP COMPLETE: $fileCount files, $totalSize MB =========="
} else {
    Log "========== BACKUP COMPLETE (no files) =========="
}
