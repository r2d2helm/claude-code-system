#!/usr/bin/env bash
set -euo pipefail
# Generic File Source - Watch file paths for new content and queue for processing
# Algorithm:
#   1. Load source configs from sources.json (paths, patterns, recursive, excludes)
#   2. Scan directories for files matching patterns, modified since last scan
#   3. Filter by extension whitelist, size limit, ignore patterns
#   4. Extract title (markdown header, script synopsis, or filename)
#   5. Output standardized JSON entries for the processing queue
#   6. Real-time mode: use inotifywait for Tier 1 watching

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SOURCES_FILE="${SKILL_DIR}/config/sources.json"
CONFIG_FILE="${SKILL_DIR}/config/config.json"
STATE_FILE="${SKILL_DIR}/data/state.json"

MAX_FILE_SIZE="${MAX_FILE_SIZE:-1048576}"  # 1MB default
SUPPORTED_EXT="md|txt|sh|bash|py|js|ts|json|yaml|yml|ps1|psm1"

log() { echo "[$(date '+%H:%M:%S')] [generic-file] $*" >&2; }

check_deps() {
    command -v jq &>/dev/null || { log "ERROR: jq required"; exit 1; }
}

# Extract title from file content
extract_title() {
    local file="$1"
    local ext="${file##*.}"

    case "$ext" in
        md)
            # Try markdown header
            grep -m1 '^# ' "$file" 2>/dev/null | sed 's/^# //' && return
            # Try frontmatter title
            grep -m1 '^title:' "$file" 2>/dev/null | sed "s/^title:\s*//; s/^[\"']//; s/[\"']$//" && return
            ;;
        sh|bash)
            # Try comment description after shebang
            sed -n '2,5{/^#[^!]/s/^#\s*//p; q}' "$file" 2>/dev/null | head -1 && return
            ;;
        py)
            # Try docstring
            sed -n '/^"""/,/"""/{ s/^"""//; s/"""$//; /^$/d; p; q }' "$file" 2>/dev/null | head -1 && return
            ;;
    esac

    # Fallback: filename without extension
    basename "$file" | sed 's/\.[^.]*$//'
}

# Scan a directory for new/modified files
# Args: source_id path patterns(comma-sep) recursive(true/false) last_scan_epoch
scan_directory() {
    local source_id="$1" dir_path="$2" patterns="$3" recursive="${4:-false}" last_scan="${5:-0}"

    [[ -d "$dir_path" ]] || { log "WARN: Directory not found: $dir_path"; return; }

    local find_args=("$dir_path")
    [[ "$recursive" != "true" ]] && find_args+=("-maxdepth" "1")
    find_args+=("-type" "f")

    # Build -name conditions from patterns
    local name_args=()
    IFS=',' read -ra pats <<< "$patterns"
    for pat in "${pats[@]}"; do
        pat="$(echo "$pat" | xargs)"  # trim
        [[ -n "$pat" ]] && name_args+=("-name" "$pat" "-o")
    done
    # Remove trailing -o
    [[ ${#name_args[@]} -gt 0 ]] && unset 'name_args[-1]'

    if [[ ${#name_args[@]} -gt 0 ]]; then
        find_args+=("(" "${name_args[@]}" ")")
    fi

    # Filter by modification time if incremental
    if [[ "$last_scan" -gt 0 ]]; then
        find_args+=("-newer" <(date -d "@$last_scan" '+%Y%m%d%H%M.%S' 2>/dev/null || true))
        # Alternative: use -newermt
        local ts
        ts="$(date -d "@$last_scan" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo '1970-01-01')"
        find_args=("$dir_path")
        [[ "$recursive" != "true" ]] && find_args+=("-maxdepth" "1")
        find_args+=("-type" "f" "-newermt" "$ts")
        if [[ ${#name_args[@]} -gt 0 ]]; then
            find_args+=("(" "${name_args[@]}" ")")
        fi
    fi

    local entries="[]"
    while IFS= read -r file; do
        [[ -z "$file" ]] && continue

        # Check extension whitelist
        local ext="${file##*.}"
        echo "$ext" | grep -qiE "^($SUPPORTED_EXT)$" || continue

        # Check file size
        local size
        size="$(stat -c%s "$file" 2>/dev/null || echo 0)"
        [[ "$size" -gt "$MAX_FILE_SIZE" ]] && { log "Skip (too large): $file"; continue; }
        [[ "$size" -eq 0 ]] && continue

        # Skip ignore patterns
        local fname
        fname="$(basename "$file")"
        [[ "$fname" =~ ^\.  ]] && continue
        [[ "$fname" =~ ~$ ]] && continue

        local title
        title="$(extract_title "$file")"
        local modified
        modified="$(stat -c%Y "$file" 2>/dev/null || echo 0)"

        local entry
        entry="$(jq -n \
            --arg sid "$source_id" \
            --arg sp "$file" \
            --arg title "$title" \
            --arg fname "$fname" \
            --arg ext ".$ext" \
            --argjson size "$size" \
            --arg mod "$(date -d "@$modified" -Iseconds 2>/dev/null || date -Iseconds)" \
            '{sourceId:$sid, sourcePath:$sp, title:$title, metadata:{fileName:$fname, extension:$ext, size:$size, lastModified:$mod}}'
        )"
        entries="$(echo "$entries" | jq --argjson e "$entry" '. + [$e]')"

    done < <(find "${find_args[@]}" 2>/dev/null || true)

    echo "$entries"
}

# Watch directory in real-time using inotifywait (Tier 1)
watch_realtime() {
    local dir_path="$1"
    command -v inotifywait &>/dev/null || { log "ERROR: inotifywait required (apt install inotify-tools)"; exit 1; }
    [[ -d "$dir_path" ]] || { log "ERROR: Directory not found: $dir_path"; exit 1; }

    log "Watching $dir_path for changes..."
    inotifywait -m -r -e create,modify,moved_to --format '%w%f' "$dir_path" 2>/dev/null | \
    while IFS= read -r file; do
        local ext="${file##*.}"
        echo "$ext" | grep -qiE "^($SUPPORTED_EXT)$" || continue
        log "Detected: $file"
        local title
        title="$(extract_title "$file")"
        jq -n --arg sp "$file" --arg title "$title" '{sourceId:"file-watcher", sourcePath:$sp, title:$title, event:"changed"}'
    done
}

# --- Main ---
check_deps

case "${1:-}" in
    --scan)
        # Scan a specific directory
        [[ -n "${2:-}" ]] || { log "Usage: $0 --scan <dir> [patterns] [recursive]"; exit 1; }
        scan_directory "generic" "$2" "${3:-*.md,*.txt,*.sh}" "${4:-false}" "0"
        ;;
    --scan-sources)
        # Scan all configured sources of a given tier
        tier="${2:-}"
        [[ -n "$tier" ]] || { log "Usage: $0 --scan-sources <tier>"; exit 1; }
        [[ -f "$SOURCES_FILE" ]] || { log "ERROR: sources.json not found"; exit 1; }

        jq -c --argjson t "$tier" '.[] | select(.tier == $t and .enabled == true and .type == "directory")' "$SOURCES_FILE" 2>/dev/null | \
        while IFS= read -r src; do
            local sid="$(echo "$src" | jq -r '.id')"
            local spath="$(echo "$src" | jq -r '.path')"
            local patterns="$(echo "$src" | jq -r '(.patterns // ["*.*"]) | join(",")')"
            local recursive="$(echo "$src" | jq -r '.recursive // false')"
            log "Scanning source: $sid ($spath)"
            scan_directory "$sid" "$spath" "$patterns" "$recursive" "0"
        done
        ;;
    --watch)
        watch_realtime "${2:-$HOME/Documents/Knowledge}"
        ;;
    --help) echo "Usage: $0 --scan <dir> | --scan-sources <tier> | --watch [dir]"
            echo "  Env: MAX_FILE_SIZE=1048576" ;;
    *)      echo "Usage: $0 --scan <dir> | --scan-sources <tier> | --watch [dir]" ;;
esac
