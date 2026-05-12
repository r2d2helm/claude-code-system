# R2D2 Departement R&A - Press Review Quotidienne
# Schedule: Lundi-Vendredi 8h00 via Task Scheduler
# But: Scanner les 4 categories, scorer Seldon, generer note vault

$ErrorActionPreference = "SilentlyContinue"
$LogFile = "$env:USERPROFILE\.claude\automation\logs\press-review-$(Get-Date -Format 'yyyy-MM-dd').log"
$LogDir = Split-Path $LogFile
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts | $msg" | Tee-Object -FilePath $LogFile -Append
}

Log "=== Press Review Daily START ==="

# Run Claude with the press-review command
try {
    $result = claude --print "/press-review" 2>&1
    Log "Press review completed. Output length: $($result.Length) chars"
    $result | Out-File -FilePath "$LogDir\press-review-output-$(Get-Date -Format 'yyyy-MM-dd').txt" -Encoding utf8
} catch {
    Log "ERROR: Press review failed: $_"
}

Log "=== Press Review Daily END ==="
