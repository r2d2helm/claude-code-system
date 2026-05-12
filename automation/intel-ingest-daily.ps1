# R2D2 Departement R&A - Ingestion Warehouse post-review
# Schedule: Lundi-Vendredi 8h30 via Task Scheduler
# But: Ingerer la press-review du jour dans le warehouse

$ErrorActionPreference = "SilentlyContinue"
$LogFile = "$env:USERPROFILE\.claude\automation\logs\intel-ingest-$(Get-Date -Format 'yyyy-MM-dd').log"
$LogDir = Split-Path $LogFile
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd"
    "$ts | $msg" | Tee-Object -FilePath $LogFile -Append
}

Log "=== Intel Ingest Daily START ==="

# Check if today's press review exists
$today = Get-Date -Format "yyyy-MM-dd"
$reviewPath = "$env:USERPROFILE\Documents\Knowledge\References\${today}_Press-Review.md"

if (Test-Path $reviewPath) {
    Log "Found press review: $reviewPath"
    try {
        $result = claude --print "/intel-ingest --from-press-review $today" 2>&1
        Log "Ingestion completed. Output: $($result.Length) chars"
    } catch {
        Log "ERROR: Ingestion failed: $_"
    }
} else {
    Log "SKIP: No press review found for $today"
}

Log "=== Intel Ingest Daily END ==="
