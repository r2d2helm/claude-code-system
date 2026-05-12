#!/usr/bin/env bash
set -euo pipefail
# Browser Bookmarks Source - Extract bookmarks from Firefox/Chrome on Linux
# Algorithm:
#   1. Locate browser profile directories
#   2. Chrome/Chromium: parse Bookmarks JSON with jq (recursive folder traversal)
#   3. Firefox: query places.sqlite with sqlite3 (copy DB first to avoid lock)
#   4. Filter by date (incremental capture since last run)
#   5. Output standardized JSON entries for the processing queue

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
STATE_FILE="${SKILL_DIR}/data/state.json"

# Linux browser profile paths
CHROME_BOOKMARKS="${HOME}/.config/google-chrome/Default/Bookmarks"
CHROMIUM_BOOKMARKS="${HOME}/.config/chromium/Default/Bookmarks"
FIREFOX_PROFILES="${HOME}/.mozilla/firefox"

log() { echo "[$(date '+%H:%M:%S')] [browser-bookmarks] $*" >&2; }

check_deps() {
    command -v jq &>/dev/null || { log "ERROR: jq required"; exit 1; }
}

# Get last capture timestamp from state
get_last_capture() {
    if [[ -f "$STATE_FILE" ]]; then
        jq -r '.lastBookmarksCapture // "1970-01-01T00:00:00"' "$STATE_FILE" 2>/dev/null || echo "1970-01-01T00:00:00"
    else
        echo "1970-01-01T00:00:00"
    fi
}

# Update state with current timestamp
save_state() {
    local now
    now="$(date -Iseconds)"
    if [[ -f "$STATE_FILE" ]]; then
        local tmp
        tmp="$(mktemp)"
        jq --arg ts "$now" '.lastBookmarksCapture = $ts' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
    else
        mkdir -p "$(dirname "$STATE_FILE")"
        echo "{\"lastBookmarksCapture\":\"$now\"}" > "$STATE_FILE"
    fi
}

# Parse Chromium/Chrome Bookmarks JSON
# Recursively extracts: title, url, folder path, date_added
parse_chromium() {
    local bookmarks_file="$1"
    local browser_name="$2"

    [[ -f "$bookmarks_file" ]] || { log "Not found: $bookmarks_file"; return; }

    # jq recursive descent through bookmark tree
    jq -r --arg browser "$browser_name" '
        def walk_bookmarks(folder_path):
            if .type == "url" then
                {
                    title: .name,
                    url: .url,
                    folder: folder_path,
                    date_added: (.date_added // "0"),
                    browser: $browser
                }
            elif .type == "folder" and .children then
                .children[] | walk_bookmarks(
                    if folder_path == "" then .name
                    else folder_path + "/" + .name end
                )
            else empty
            end;
        .roots | to_entries[] | .value | walk_bookmarks("")
    ' "$bookmarks_file" 2>/dev/null | jq -s '.'
}

# Parse Firefox bookmarks from places.sqlite
parse_firefox() {
    command -v sqlite3 &>/dev/null || { log "sqlite3 not found, skipping Firefox"; return; }

    [[ -d "$FIREFOX_PROFILES" ]] || { log "Firefox profiles dir not found"; return; }

    # Find default profile
    local profile_dir=""
    for d in "$FIREFOX_PROFILES"/*.default-release "$FIREFOX_PROFILES"/*.default; do
        [[ -d "$d" ]] && { profile_dir="$d"; break; }
    done
    [[ -n "$profile_dir" ]] || { log "No Firefox default profile found"; return; }

    local places_db="${profile_dir}/places.sqlite"
    [[ -f "$places_db" ]] || { log "places.sqlite not found"; return; }

    # Copy DB to avoid locking issues with running Firefox
    local tmp_db
    tmp_db="$(mktemp)"
    cp "$places_db" "$tmp_db" 2>/dev/null || { log "Cannot copy places.sqlite"; rm -f "$tmp_db"; return; }

    # Query bookmarks with folder hierarchy
    sqlite3 -json "$tmp_db" "
        SELECT
            b.title,
            p.url,
            COALESCE(parent_b.title, '') as folder,
            b.dateAdded / 1000000 as date_added_unix
        FROM moz_bookmarks b
        JOIN moz_places p ON b.fk = p.id
        LEFT JOIN moz_bookmarks parent_b ON b.parent = parent_b.id
        WHERE b.type = 1
        AND p.url NOT LIKE 'place:%'
        ORDER BY b.dateAdded DESC
        LIMIT 500;
    " 2>/dev/null | jq '[.[] | . + {browser: "firefox"}]' 2>/dev/null || echo "[]"

    rm -f "$tmp_db"
}

# Format bookmark as queue entry JSON
format_entry() {
    local bookmark_json="$1"
    jq '{
        sourceId: "browser-bookmarks",
        sourcePath: (.browser + " - " + .url),
        title: .title,
        content: ("# " + .title + "\n\n## URL\n" + .url + "\n\n## Details\n- **Navigateur**: " + .browser + "\n- **Dossier**: " + (.folder // "Root") + "\n\n## Notes\n"),
        metadata: {url: .url, browser: .browser, folder: (.folder // "Root")}
    }' <<< "$bookmark_json"
}

# --- Main ---
check_deps

case "${1:-}" in
    --capture)
        log "Starting bookmark capture..."
        all_bookmarks="[]"

        # Chrome
        if [[ -f "$CHROME_BOOKMARKS" ]]; then
            chrome_bm="$(parse_chromium "$CHROME_BOOKMARKS" "chrome")"
            all_bookmarks="$(jq -s '.[0] + .[1]' <(echo "$all_bookmarks") <(echo "${chrome_bm:-[]}"))"
            log "Chrome: $(echo "${chrome_bm:-[]}" | jq length) bookmarks"
        fi

        # Chromium
        if [[ -f "$CHROMIUM_BOOKMARKS" ]]; then
            chromium_bm="$(parse_chromium "$CHROMIUM_BOOKMARKS" "chromium")"
            all_bookmarks="$(jq -s '.[0] + .[1]' <(echo "$all_bookmarks") <(echo "${chromium_bm:-[]}"))"
            log "Chromium: $(echo "${chromium_bm:-[]}" | jq length) bookmarks"
        fi

        # Firefox
        firefox_bm="$(parse_firefox)" || firefox_bm="[]"
        all_bookmarks="$(jq -s '.[0] + .[1]' <(echo "$all_bookmarks") <(echo "${firefox_bm:-[]}"))"
        log "Firefox: $(echo "${firefox_bm:-[]}" | jq length) bookmarks"

        echo "$all_bookmarks"
        save_state
        log "Total: $(echo "$all_bookmarks" | jq length) bookmarks captured"
        ;;
    --stats)
        echo "Browser bookmark sources:"
        [[ -f "$CHROME_BOOKMARKS" ]] && echo "  Chrome: available ($CHROME_BOOKMARKS)" || echo "  Chrome: not found"
        [[ -f "$CHROMIUM_BOOKMARKS" ]] && echo "  Chromium: available ($CHROMIUM_BOOKMARKS)" || echo "  Chromium: not found"
        [[ -d "$FIREFOX_PROFILES" ]] && echo "  Firefox: available ($FIREFOX_PROFILES)" || echo "  Firefox: not found"
        echo "  Last capture: $(get_last_capture)"
        ;;
    --help) echo "Usage: $0 --capture | --stats" ;;
    *)      echo "Usage: $0 --capture | --stats" ;;
esac
