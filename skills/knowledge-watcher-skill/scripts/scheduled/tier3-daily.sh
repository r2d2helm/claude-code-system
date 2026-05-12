#!/usr/bin/env bash
set -euo pipefail
# Tier 3 - Daily cron: bookmarks, VS Code settings, browser history
# Runs via: crontab -e -> 0 3 * * * /path/to/tier3-daily.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SOURCES_SCRIPT="${SKILL_DIR}/sources/generic-file.sh"
BOOKMARKS_SCRIPT="${SKILL_DIR}/sources/browser-bookmarks.sh"
SOURCES_FILE="${SKILL_DIR}/config/sources.json"
STATE_FILE="${SKILL_DIR}/data/state.json"
LOG_DIR="${SKILL_DIR}/data/logs"

mkdir -p "$LOG_DIR"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [tier3] $*" | tee -a "${LOG_DIR}/tier3.log" >&2; }

log "=== Tier 3 daily scan starting ==="

# Scan tier 3 directory sources
if [[ -f "$SOURCES_FILE" && -x "$SOURCES_SCRIPT" ]]; then
    "$SOURCES_SCRIPT" --scan-sources 3
fi

# Capture browser bookmarks
if [[ -x "$BOOKMARKS_SCRIPT" ]]; then
    log "Capturing browser bookmarks..."
    "$BOOKMARKS_SCRIPT" --capture > "${LOG_DIR}/bookmarks-latest.json" 2>/dev/null || log "WARN: Bookmark capture failed"
fi

# Scan VS Code snippets/settings if present
VSCODE_DIR="${HOME}/.config/Code/User"
if [[ -d "$VSCODE_DIR" && -x "$SOURCES_SCRIPT" ]]; then
    log "Scanning VS Code user dir..."
    "$SOURCES_SCRIPT" --scan "$VSCODE_DIR" "*.json" "false" 2>/dev/null || true
fi

# Update state
if [[ -f "$STATE_FILE" ]]; then
    tmp="$(mktemp)"
    jq --arg ts "$(date -Iseconds)" '.lastTier3Run = $ts' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
fi

log "=== Tier 3 daily scan complete ==="
