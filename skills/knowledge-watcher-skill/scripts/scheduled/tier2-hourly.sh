#!/usr/bin/env bash
set -euo pipefail
# Tier 2 - Hourly cron: scan Downloads, temp files, project dirs
# Runs via: crontab -e -> 0 * * * * /path/to/tier2-hourly.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SOURCES_SCRIPT="${SKILL_DIR}/sources/generic-file.sh"
SOURCES_FILE="${SKILL_DIR}/config/sources.json"
STATE_FILE="${SKILL_DIR}/data/state.json"
LOG_DIR="${SKILL_DIR}/data/logs"

mkdir -p "$LOG_DIR"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [tier2] $*" | tee -a "${LOG_DIR}/tier2.log" >&2; }

log "=== Tier 2 hourly scan starting ==="

# Scan all tier 2 sources
if [[ -f "$SOURCES_FILE" && -x "$SOURCES_SCRIPT" ]]; then
    "$SOURCES_SCRIPT" --scan-sources 2
else
    # Fallback: scan common tier 2 paths directly
    for dir in "$HOME/Downloads" "$HOME/tmp" "/tmp/${USER:-}"; do
        [[ -d "$dir" ]] && "$SOURCES_SCRIPT" --scan "$dir" "*.md,*.txt,*.sh,*.py" "false" 2>/dev/null || true
    done
fi

# Update state
if [[ -f "$STATE_FILE" ]]; then
    tmp="$(mktemp)"
    jq --arg ts "$(date -Iseconds)" '.lastTier2Run = $ts' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
fi

log "=== Tier 2 hourly scan complete ==="
