# R2D2 Departement R&A - Brief Hebdomadaire
# Schedule: Lundi 9h00 via Task Scheduler
# But: Generer le brief strategique de la semaine

$ErrorActionPreference = "SilentlyContinue"
$LogFile = "$env:USERPROFILE\.claude\automation\logs\intel-weekly-$(Get-Date -Format 'yyyy-MM-dd').log"
$LogDir = Split-Path $LogFile
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts | $msg" | Tee-Object -FilePath $LogFile -Append
}

Log "=== Intel Weekly Brief START ==="

try {
    $result = claude --print "/intel-weekly" 2>&1
    Log "Weekly brief completed. Output: $($result.Length) chars"
    $result | Out-File -FilePath "$LogDir\weekly-brief-$(Get-Date -Format 'yyyy-MM-dd').txt" -Encoding utf8
} catch {
    Log "ERROR: Weekly brief failed: $_"
}

Log "=== Intel Weekly Brief END ==="
