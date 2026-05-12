#!/usr/bin/env bash
set -euo pipefail
# AutoLinker - Insert [[wikilinks]] into notes by matching against notes-index.json
# Algorithm:
#   1. Load notes-index.json (terms -> original name + paths)
#   2. For each note, extract body (skip frontmatter)
#   3. Match index terms against body text (longest-first to avoid sub-matches)
#   4. Skip self-references, already-linked terms, and excluded common words
#   5. Replace first occurrence with [[OriginalTerm]]
#   6. Optionally run in batch mode on entire vault

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VAULT="${KNOWLEDGE_VAULT:-$HOME/Documents/Knowledge}"
INDEX_FILE="${SKILL_DIR}/data/notes-index.json"
CONFIG_FILE="${SKILL_DIR}/config/config.json"
MAX_LINKS="${MAX_LINKS:-20}"
MIN_TERM_LEN="${MIN_TERM_LEN:-5}"
DRY_RUN="${DRY_RUN:-false}"

# Excluded common terms (too generic for linking)
EXCLUDED_TERMS="solution|claude|skill|para|note|notes|test|tests|file|files|code|data|type|name|path|index|list|item|items|task|tasks|link|links|tag|tags|date|time|user|config|error|debug|info|warn|true|false|null|string|number|object|array|new|old|get|set|add|remove|update|delete|start|stop|run|execute|process|create|build|input|output|result|value|key|id|status|readme|agents|examples|support|prompts|planning|architecture|initial|setup-instructions|instructions|api|url|cli|gui|sdk|ide"

log() { echo "[$(date '+%H:%M:%S')] [autolinker] $*" >&2; }

check_deps() {
    for cmd in jq; do
        command -v "$cmd" &>/dev/null || { log "ERROR: $cmd required"; exit 1; }
    done
}

ensure_index() {
    if [[ ! -f "$INDEX_FILE" ]]; then
        log "WARN: notes-index.json not found at $INDEX_FILE"
        log "Run build-notes-index.sh first"
        exit 1
    fi
}

# Extract body content (skip YAML frontmatter)
get_body() {
    local file="$1"
    awk 'BEGIN{fm=0} /^---$/{fm++; if(fm==2){getline; found=1}} found{print}' "$file"
    # If no frontmatter found, return entire file
    if ! grep -q '^---$' "$file"; then
        cat "$file"
    fi
}

# Auto-link a single note file
# Outputs JSON: {"file":"...","links_added":N,"terms":["..."]}
autolink_note() {
    local note_path="$1"
    [[ -f "$note_path" ]] || { log "WARN: not found: $note_path"; return; }

    local content
    content="$(cat "$note_path")"
    local body
    body="$(get_body "$note_path")"

    # Get sorted terms from index (longest first, >= MIN_TERM_LEN chars)
    local terms
    terms="$(jq -r --argjson minlen "$MIN_TERM_LEN" \
        '.terms | to_entries | map(select(.key | length >= $minlen)) | sort_by(.key | length) | reverse | .[].key' \
        "$INDEX_FILE" 2>/dev/null)" || return

    local links_added=0
    local added_terms=()
    local modified="$content"

    while IFS= read -r term_lower; do
        [[ $links_added -ge $MAX_LINKS ]] && break
        [[ -z "$term_lower" ]] && continue

        # Skip excluded terms
        if echo "$term_lower" | grep -qwE "$EXCLUDED_TERMS"; then
            continue
        fi

        # Get original term name from index
        local original
        original="$(jq -r --arg t "$term_lower" '.terms[$t].original // empty' "$INDEX_FILE")" || continue
        [[ -z "$original" ]] && continue

        # Skip if paths only contain self
        local valid_paths
        valid_paths="$(jq -r --arg t "$term_lower" --arg self "$note_path" \
            '.terms[$t].paths | map(select(. != $self)) | length' "$INDEX_FILE" 2>/dev/null)" || continue
        [[ "$valid_paths" == "0" ]] && continue

        # Skip if already a wikilink in content
        if echo "$modified" | grep -qF "[[${original}]]"; then
            continue
        fi

        # Skip if this is a sub-term of an already-linked term
        local is_sub=false
        for linked in "${added_terms[@]+"${added_terms[@]}"}"; do
            if echo "$linked" | grep -qi "$term_lower"; then
                is_sub=true; break
            fi
        done
        $is_sub && continue

        # Check if term appears in body (case-insensitive, word boundary)
        if echo "$body" | grep -qiP "(?<!\w)${term_lower}(?!\w)"; then
            # Replace first occurrence in body section only (after frontmatter)
            modified="$(echo "$modified" | sed -E "0,/[^[](${original}|${term_lower})([^]])/I s//\x00[[\1]]\2/" | tr -d '\0' || echo "$modified")"
            # Simpler approach: use perl for first-match case-insensitive replace
            modified="$(echo "$content" | perl -0pe "s/(?<!\[\[)(?<!\w)(${term_lower})(?!\w)(?!\]\])/[[$original]]/i" 2>/dev/null || echo "$modified")"
            links_added=$((links_added + 1))
            added_terms+=("$original")
            content="$modified"
        fi
    done <<< "$terms"

    if [[ $links_added -gt 0 ]]; then
        if [[ "$DRY_RUN" == "false" ]]; then
            echo "$modified" > "$note_path"
        fi
        local terms_json
        terms_json="$(printf '%s\n' "${added_terms[@]}" | jq -R . | jq -s .)"
        echo "{\"file\":\"$note_path\",\"links_added\":$links_added,\"terms\":$terms_json}"
        log "Linked $links_added terms in $(basename "$note_path")"
    fi
}

# Batch auto-link: process vault notes
batch_autolink() {
    local target="${1:-$VAULT}"
    local max_notes="${2:-50}"
    local orphans_only="${3:-false}"
    local total=0
    local processed=0

    find "$target" -name '*.md' -not -path '*/_Templates/*' -not -path '*/.obsidian/*' | \
    while IFS= read -r note && [[ $processed -lt $max_notes ]]; do
        if [[ "$orphans_only" == "true" ]]; then
            # Skip notes that already have outgoing links
            if grep -qP '\[\[.+\]\]' "$note" 2>/dev/null; then
                continue
            fi
        fi
        autolink_note "$note"
        processed=$((processed + 1))
    done

    log "Batch complete: processed up to $max_notes notes"
}

# --- Main ---
check_deps
ensure_index

case "${1:-}" in
    --batch)  batch_autolink "${2:-$VAULT}" "${3:-50}" "${4:-false}" ;;
    --file)   [[ -n "${2:-}" ]] && autolink_note "$2" || log "Usage: $0 --file <path>" ;;
    --help)   echo "Usage: $0 [--batch [vault] [max] [orphans-only]] | [--file <note.md>]"
              echo "  Env: DRY_RUN=true MAX_LINKS=20 MIN_TERM_LEN=5" ;;
    *)        echo "Usage: $0 --batch | --file <note.md> | --help" ;;
esac
