#!/usr/bin/env bash
set -euo pipefail
# Formatter - Ensure YAML frontmatter, normalize headers, generate Obsidian notes
# Algorithm:
#   1. Check if note has valid YAML frontmatter; add if missing
#   2. Normalize headers (ensure single H1, proper hierarchy)
#   3. Fix encoding (ensure UTF-8, strip BOM)
#   4. Format note according to type template (conversation, concept, troubleshooting, etc.)
#   5. Optionally update Daily Note with link to new note

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VAULT="${KNOWLEDGE_VAULT:-$HOME/Documents/Knowledge}"
CONFIG_FILE="${SKILL_DIR}/config/config.json"

log() { echo "[$(date '+%H:%M:%S')] [formatter] $*" >&2; }

# Convert title to safe filename (replace spaces with -, strip special chars)
safe_filename() {
    echo "$1" | sed -E 's/\s+/-/g; s/[<>:"\/\\|?*]//g; s/-+/-/g; s/^-|-$//g' | head -c 100
}

# Generate YAML frontmatter
generate_frontmatter() {
    local title="$1" date="$2" type="$3" status="${4:-seedling}" source="${5:-KnowledgeWatcher}"
    shift 5
    local tags=("$@")

    local tags_yaml=""
    for tag in "${tags[@]+"${tags[@]}"}"; do
        tags_yaml="${tags_yaml}  - \"${tag}\"\n"
    done

    printf -- '---\ntitle: "%s"\ndate: %s\ntype: %s\nstatus: %s\nsource: %s\ntags:\n%brelated: []\ncreated: %s\n---\n' \
        "$title" "$date" "$type" "$status" "$source" "$tags_yaml" "$(date '+%Y-%m-%d %H:%M:%S')"
}

# Check and fix frontmatter on an existing note
ensure_frontmatter() {
    local file="$1"
    [[ -f "$file" ]] || return

    # Check if file starts with ---
    if head -1 "$file" | grep -q '^---$'; then
        log "Frontmatter OK: $(basename "$file")"
        return
    fi

    log "Adding frontmatter to $(basename "$file")"
    local title
    title="$(grep -m1 '^# ' "$file" | sed 's/^# //' || basename "$file" .md)"
    local date
    date="$(date +%Y-%m-%d)"

    local tmp
    tmp="$(mktemp)"
    generate_frontmatter "$title" "$date" "note" "seedling" "formatter" > "$tmp"
    echo "" >> "$tmp"
    cat "$file" >> "$tmp"
    mv "$tmp" "$file"
}

# Strip BOM and ensure UTF-8
fix_encoding() {
    local file="$1"
    # Remove BOM if present (EF BB BF)
    if head -c 3 "$file" | od -An -tx1 | grep -q 'ef bb bf'; then
        local tmp
        tmp="$(mktemp)"
        tail -c +4 "$file" > "$tmp"
        mv "$tmp" "$file"
        log "Stripped BOM from $(basename "$file")"
    fi
}

# Normalize headers: ensure single H1, no skipped levels
normalize_headers() {
    local file="$1"
    local h1_count
    h1_count="$(grep -c '^# ' "$file" 2>/dev/null || echo 0)"

    if [[ "$h1_count" -gt 1 ]]; then
        # Demote extra H1 to H2 (skip first H1)
        local first_seen=false
        local tmp
        tmp="$(mktemp)"
        while IFS= read -r line; do
            if [[ "$line" =~ ^'# ' ]] && ! $first_seen; then
                first_seen=true
                echo "$line"
            elif [[ "$line" =~ ^'# ' ]]; then
                echo "#$line"
            else
                echo "$line"
            fi
        done < "$file" > "$tmp"
        mv "$tmp" "$file"
        log "Normalized headers in $(basename "$file")"
    fi
}

# Format a new note from classified content
# Args: title, content, type, tags (comma-separated), source_path
format_note() {
    local title="$1" content="$2" type="$3" tags_csv="$4" source_path="${5:-}"
    local date
    date="$(date +%Y-%m-%d)"
    IFS=',' read -ra tags <<< "$tags_csv"

    local fm
    fm="$(generate_frontmatter "$title" "$date" "$type" "seedling" "KnowledgeWatcher" "${tags[@]+"${tags[@]}"}")"

    case "$type" in
        conversation)
            printf '%s\n\n# %s\n\n## Resume\n\n## Points Cles\n\n## Code/Commandes\n\n## Concepts Lies\n\n## Actions Suivantes\n\n---\n*Capture le %s par Knowledge Watcher*\n*Source: %s*\n' \
                "$fm" "$title" "$date" "$source_path"
            ;;
        troubleshooting)
            printf '%s\n\n# %s\n\n## Probleme\n\n## Environnement\n\n## Symptomes\n\n## Cause Identifiee\n\n## Solution\n\n## Prevention\n\n---\n*Capture le %s par Knowledge Watcher*\n' \
                "$fm" "$title" "$date"
            ;;
        concept)
            printf '%s\n\n# %s\n\n## Pourquoi\n\n## Details\n\n## Exemples\n\n## Liens\n\n## Sources\n\n---\n*Capture le %s par Knowledge Watcher*\n' \
                "$fm" "$title" "$date"
            ;;
        *)
            printf '%s\n\n# %s\n\n## Resume\n\n## Points Cles\n\n## Contenu\n%s\n\n---\n*Capture le %s par Knowledge Watcher*\n' \
                "$fm" "$title" "$content" "$date"
            ;;
    esac
}

# Update daily note with link to new note
update_daily() {
    local note_name="$1" type="${2:-note}"
    local date
    date="$(date +%Y-%m-%d)"
    local daily_dir="${VAULT}/_Daily"
    local daily_file="${daily_dir}/${date}.md"

    mkdir -p "$daily_dir"

    # Create daily note if missing
    if [[ ! -f "$daily_file" ]]; then
        generate_frontmatter "$date" "$date" "daily" "seedling" "formatter" "daily" > "$daily_file"
        printf '\n# %s\n\n## Conversations du Jour\n\n## Captures Automatiques\n\n## Notes\n\n' "$date" >> "$daily_file"
    fi

    local link="[[${note_name%.md}]]"
    # Don't add duplicate links
    if ! grep -qF "$link" "$daily_file" 2>/dev/null; then
        local section="## Captures Automatiques"
        [[ "$type" == "conversation" ]] && section="## Conversations du Jour"
        sed -i "/${section}/a - ${link}" "$daily_file"
        log "Updated daily note with $link"
    fi
}

# --- Main ---
case "${1:-}" in
    --ensure-frontmatter)
        [[ -n "${2:-}" ]] || { log "Usage: $0 --ensure-frontmatter <file>"; exit 1; }
        ensure_frontmatter "$2"
        ;;
    --fix-encoding)
        [[ -n "${2:-}" ]] || { log "Usage: $0 --fix-encoding <file>"; exit 1; }
        fix_encoding "$2"
        ;;
    --normalize)
        [[ -n "${2:-}" ]] || { log "Usage: $0 --normalize <file>"; exit 1; }
        normalize_headers "$2"
        ;;
    --format)
        # --format "title" "content" "type" "tag1,tag2" "source"
        [[ -n "${2:-}" && -n "${3:-}" && -n "${4:-}" ]] || { log "Usage: $0 --format <title> <content> <type> [tags] [source]"; exit 1; }
        format_note "$2" "$3" "$4" "${5:-}" "${6:-}"
        ;;
    --update-daily)
        [[ -n "${2:-}" ]] || { log "Usage: $0 --update-daily <note-name> [type]"; exit 1; }
        update_daily "$2" "${3:-note}"
        ;;
    --fix-all)
        # Fix encoding + frontmatter + headers on all vault notes
        log "Fixing all notes in $VAULT..."
        find "$VAULT" -name '*.md' -not -path '*/_Templates/*' -not -path '*/.obsidian/*' | while read -r f; do
            fix_encoding "$f"
            ensure_frontmatter "$f"
            normalize_headers "$f"
        done
        log "Done."
        ;;
    --help) echo "Usage: $0 --ensure-frontmatter|--fix-encoding|--normalize|--format|--update-daily|--fix-all <args>" ;;
    *)      echo "Usage: $0 --ensure-frontmatter|--fix-encoding|--normalize|--format|--update-daily|--fix-all <args>" ;;
esac
