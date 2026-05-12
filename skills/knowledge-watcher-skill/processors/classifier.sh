#!/usr/bin/env bash
set -euo pipefail
# Classifier - Analyze note content, assign type/tags/folder
# Algorithm:
#   1. Load rules.json classification rules (sorted by priority desc)
#   2. For each rule, test conditions (content patterns, path, extension)
#   3. First matching rule determines: type, folder, prefix, template, base tags
#   4. Auto-tag by scanning content for known patterns (docker, python, etc.)
#   5. Output JSON with classification result

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
RULES_FILE="${SKILL_DIR}/config/rules.json"
VAULT="${KNOWLEDGE_VAULT:-$HOME/Documents/Knowledge}"

log() { echo "[$(date '+%H:%M:%S')] [classifier] $*" >&2; }

check_deps() {
    command -v jq &>/dev/null || { log "ERROR: jq required"; exit 1; }
}

# Auto-detect tags from content based on keyword patterns
detect_auto_tags() {
    local content="$1"
    local tags=()

    # Technology detection patterns
    [[ "$content" =~ (docker|container|Dockerfile) ]] && tags+=("infra/docker")
    [[ "$content" =~ (proxmox|qemu|pve) ]] && tags+=("infra/proxmox")
    [[ "$content" =~ (bash|#!/bin/bash|\.sh) ]] && tags+=("dev/bash")
    [[ "$content" =~ (python|\.py|pip|import) ]] && tags+=("dev/python")
    [[ "$content" =~ (claude|anthropic|LLM|agent) ]] && tags+=("ai/claude")
    [[ "$content" =~ (nginx|apache|systemd|systemctl) ]] && tags+=("infra/linux")
    [[ "$content" =~ (git|commit|branch|merge) ]] && tags+=("dev/git")
    [[ "$content" =~ (error|fix|debug|issue|problem) ]] && tags+=("troubleshooting")
    [[ "$content" =~ (security|auth|firewall|ufw|ssl) ]] && tags+=("security")
    [[ "$content" =~ (kubernetes|k8s|helm|kubectl) ]] && tags+=("infra/kubernetes")

    # If rules.json has autoTags, also check those
    if [[ -f "$RULES_FILE" ]]; then
        while IFS='|' read -r pattern tag; do
            [[ -z "$pattern" ]] && continue
            if echo "$content" | grep -qiP "$pattern" 2>/dev/null; then
                tags+=("$tag")
            fi
        done < <(jq -r '.tagging.autoTags[]? | "\(.pattern)|\(.tag)"' "$RULES_FILE" 2>/dev/null || true)
    fi

    # Deduplicate and output
    printf '%s\n' "${tags[@]+"${tags[@]}"}" | sort -u | jq -R . | jq -s .
}

# Classify content: determine type, folder, prefix, template, tags
classify() {
    local content="$1"
    local source_path="$2"
    local extension="${source_path##*.}"
    extension=".${extension}"

    # Try rules from rules.json (sorted by priority desc)
    if [[ -f "$RULES_FILE" ]]; then
        local rule_match
        rule_match="$(jq -r --arg content "$content" --arg path "$source_path" --arg ext "$extension" '
            .classification.rules | sort_by(.priority) | reverse | .[] |
            select(
                (.conditions.always == true) or
                (.conditions.any // [] | any(
                    (.field == "content" and ($content | test(.contains // "^$"; "i"))) or
                    (.field == "extension" and ($ext == .equals)) or
                    (.field == "path" and ($path | test(.contains // "^$"; "i")))
                ))
            ) | .output | {type, folder, prefix, template, tags}
        ' "$RULES_FILE" 2>/dev/null | head -1)" || true

        if [[ -n "$rule_match" && "$rule_match" != "null" ]]; then
            local auto_tags
            auto_tags="$(detect_auto_tags "$content")"
            echo "$rule_match" | jq --argjson auto "$auto_tags" '.tags = ((.tags // []) + $auto | unique)'
            return
        fi
    fi

    # Heuristic fallback classification
    local type="note" folder="_Inbox" prefix="" template=""
    local tags=()

    # Detect type from content patterns
    if echo "$content" | grep -qiP '(conversation|session|chat|claude)'; then
        type="conversation"; folder="Conversations"; prefix="\$(date +%Y-%m-%d)_Conv_"
        tags+=("conversation")
    elif echo "$content" | grep -qiP '(error|fix|debug|solution|resolve)'; then
        type="troubleshooting"; folder="References"; prefix="\$(date +%Y-%m-%d)_Fix_"
        tags+=("troubleshooting")
    elif echo "$content" | grep -qiP '(concept|definition|pattern|principle)'; then
        type="concept"; folder="Concepts"; prefix="C_"
        tags+=("concept")
    elif [[ "$extension" =~ \.(sh|py|ps1|js|ts)$ ]]; then
        type="code"; folder="References"; prefix="\$(date +%Y-%m-%d)_"
        tags+=("dev/code")
    fi

    local auto_tags
    auto_tags="$(detect_auto_tags "$content")"

    jq -n --arg type "$type" --arg folder "$folder" --arg prefix "$prefix" \
        --arg template "$template" --argjson auto "$auto_tags" \
        --argjson base "$(printf '%s\n' "${tags[@]+"${tags[@]}"}" | jq -R . | jq -s .)" \
        '{type:$type, folder:$folder, prefix:$prefix, template:$template, tags:($base + $auto | unique)}'
}

# Suggest title from content
suggest_title() {
    local content="$1"
    local source_path="$2"

    # Try markdown header
    local header
    header="$(echo "$content" | grep -m1 '^# ' | sed 's/^# //')" || true
    [[ -n "$header" ]] && { echo "$header"; return; }

    # Try first non-empty line (max 100 chars)
    local first
    first="$(echo "$content" | grep -m1 '.' | head -c 100)" || true
    [[ -n "$first" ]] && { echo "$first"; return; }

    # Fallback: filename
    basename "$source_path" | sed 's/\.[^.]*$//'
}

# --- Main ---
check_deps

case "${1:-}" in
    --classify)
        [[ -n "${2:-}" ]] || { log "Usage: $0 --classify <file>"; exit 1; }
        content="$(cat "$2")"
        classify "$content" "$2"
        ;;
    --title)
        [[ -n "${2:-}" ]] || { log "Usage: $0 --title <file>"; exit 1; }
        content="$(cat "$2")"
        suggest_title "$content" "$2"
        ;;
    --tags)
        [[ -n "${2:-}" ]] || { log "Usage: $0 --tags <file>"; exit 1; }
        content="$(cat "$2")"
        detect_auto_tags "$content"
        ;;
    --help) echo "Usage: $0 --classify|--title|--tags <file>" ;;
    *)      echo "Usage: $0 --classify|--title|--tags <file>" ;;
esac
