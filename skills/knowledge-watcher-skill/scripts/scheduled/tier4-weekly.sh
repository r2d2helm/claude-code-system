#!/usr/bin/env bash
set -euo pipefail
# Tier 4 - Weekly cron: archives, old backups, deep scan
# Runs via: crontab -e -> 0 4 * * 0 /path/to/tier4-weekly.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SOURCES_SCRIPT="${SKILL_DIR}/sources/generic-file.sh"
SOURCES_FILE="${SKILL_DIR}/config/sources.json"
STATE_FILE="${SKILL_DIR}/data/state.json"
LOG_DIR="${SKILL_DIR}/data/logs"

mkdir -p "$LOG_DIR"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [tier4] $*" | tee -a "${LOG_DIR}/tier4.log" >&2; }

log "=== Tier 4 weekly scan starting ==="

# Scan all tier 4 sources
if [[ -f "$SOURCES_FILE" && -x "$SOURCES_SCRIPT" ]]; then
    "$SOURCES_SCRIPT" --scan-sources 4
else
    # Fallback: scan common archive/backup locations
    for dir in "$HOME/Archives" "$HOME/Backups" "$HOME/Documents/Archives"; do
        [[ -d "$dir" ]] && "$SOURCES_SCRIPT" --scan "$dir" "*.md,*.txt" "true" 2>/dev/null || true
    done
fi

# Update state
if [[ -f "$STATE_FILE" ]]; then
    tmp="$(mktemp)"
    jq --arg ts "$(date -Iseconds)" '.lastTier4Run = $ts' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
fi

log "=== Tier 4 weekly scan complete ==="
