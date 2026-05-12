#!/usr/bin/env bash
set -euo pipefail
# Claude History Source - Parse Claude conversation JSONL for knowledge extraction
# Algorithm:
#   1. Read history JSONL file line-by-line (incremental from last position)
#   2. Group messages by sessionId into conversations
#   3. Filter: keep conversations with >= MIN_MESSAGES messages
#   4. Extract title from first user message
#   5. Detect subjects via keyword patterns (docker, python, git, etc.)
#   6. Output standardized JSON entries for the processing queue

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
STATE_FILE="${SKILL_DIR}/data/state.json"
SOURCES_FILE="${SKILL_DIR}/config/sources.json"
MIN_MESSAGES="${MIN_MESSAGES:-3}"

# Default Claude history path (Claude Code on Linux)
CLAUDE_HISTORY="${CLAUDE_HISTORY:-$HOME/.claude/history.jsonl}"

log() { echo "[$(date '+%H:%M:%S')] [claude-history] $*" >&2; }

check_deps() {
    command -v jq &>/dev/null || { log "ERROR: jq required"; exit 1; }
}

# Get last read line from state
get_last_line() {
    if [[ -f "$STATE_FILE" ]]; then
        jq -r '.lastClaudeHistoryLine // 0' "$STATE_FILE" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# Save last read line to state
save_last_line() {
    local line_num="$1"
    if [[ -f "$STATE_FILE" ]]; then
        local tmp
        tmp="$(mktemp)"
        jq --argjson n "$line_num" '.lastClaudeHistoryLine = $n' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
    else
        mkdir -p "$(dirname "$STATE_FILE")"
        echo "{\"lastClaudeHistoryLine\":$line_num}" > "$STATE_FILE"
    fi
}

# Detect conversation subjects from content
detect_subjects() {
    local content="$1"
    local subjects=()

    [[ "$content" =~ (bash|\.sh|shell) ]] && subjects+=("bash")
    [[ "$content" =~ (python|\.py|pip) ]] && subjects+=("python")
    [[ "$content" =~ (docker|container|Dockerfile) ]] && subjects+=("infrastructure")
    [[ "$content" =~ (proxmox|vm|qemu) ]] && subjects+=("infrastructure")
    [[ "$content" =~ (claude|anthropic|llm|agent) ]] && subjects+=("claude")
    [[ "$content" =~ (git|commit|branch|merge) ]] && subjects+=("git")
    [[ "$content" =~ (api|rest|graphql|endpoint) ]] && subjects+=("api")
    [[ "$content" =~ (sql|database|query|table) ]] && subjects+=("database")
    [[ "$content" =~ (security|auth|jwt|credential) ]] && subjects+=("security")
    [[ "$content" =~ (config|setup|install) ]] && subjects+=("configuration")
    [[ "$content" =~ (error|fix|debug|issue|problem) ]] && subjects+=("debugging")

    printf '%s\n' "${subjects[@]+"${subjects[@]}"}" | sort -u | jq -R . | jq -s .
}

# Extract title from first user message (max 80 chars)
extract_title() {
    local first_msg="$1"
    local title
    title="$(echo "$first_msg" | tr '\n' ' ' | sed 's/\s\+/ /g' | head -c 80)"
    [[ ${#title} -ge 77 ]] && title="${title:0:77}..."
    echo "$title"
}

# Parse JSONL and group into conversations
# Outputs array of conversation entries as JSON
parse_history() {
    local history_file="$1"
    local from_line="$2"

    [[ -f "$history_file" ]] || { log "WARN: History file not found: $history_file"; echo "[]"; return; }

    local total_lines
    total_lines="$(wc -l < "$history_file")"
    log "History file: $total_lines lines, reading from line $from_line"

    # Use jq to process JSONL: group by sessionId, filter by min messages
    tail -n +"$((from_line + 1))" "$history_file" 2>/dev/null | \
    jq -s --argjson min "$MIN_MESSAGES" '
        # Group entries by sessionId
        group_by(.sessionId // "unknown") |
        map(
            # Filter groups with enough messages
            select(
                [.[] | select(.role != null or .type == "message")] | length >= $min
            ) |
            {
                sessionId: (.[0].sessionId // "unknown"),
                startTime: (.[0].timestamp // now | tostring),
                messageCount: ([.[] | select(.role != null)] | length),
                # First user message as title source
                firstUserMessage: ([.[] | select(.role == "user" or .role == "human")] | .[0].content // .[0].message // "Untitled" |
                    if type == "array" then [.[] | select(.type == "text") | .text] | join(" ") else . end |
                    gsub("\n"; " ") | .[0:80]),
                # Collect tools used
                tools: [.[] | select(.type == "tool_use" or .toolName != null) | (.toolName // .name // "unknown")] | unique,
                # Build content from messages
                content: [.[] | select(.role != null) |
                    ((if .role == "user" or .role == "human" then "User" else "Assistant" end) + ":\n" +
                    (if .content | type == "array" then [.content[] | select(.type == "text") | .text] | join("\n")
                     elif .content then .content
                     elif .message then .message
                     else "" end))
                ] | join("\n---\n")
            }
        ) |
        map({
            sourceId: "claude-history",
            sourcePath: ("Claude History - " + .sessionId),
            title: .firstUserMessage,
            content: .content,
            metadata: {
                sessionId: .sessionId,
                startTime: .startTime,
                messageCount: .messageCount,
                tools: .tools
            }
        })
    ' 2>/dev/null || echo "[]"

    save_last_line "$total_lines"
}

# --- Main ---
check_deps

case "${1:-}" in
    --capture)
        # Resolve history path from sources.json if available
        if [[ -f "$SOURCES_FILE" ]]; then
            configured_path="$(jq -r '.[] | select(.id == "claude-history") | .path // empty' "$SOURCES_FILE" 2>/dev/null)" || true
            [[ -n "$configured_path" ]] && CLAUDE_HISTORY="$configured_path"
        fi

        from_line="$(get_last_line)"
        log "Capturing from line $from_line of $CLAUDE_HISTORY"
        entries="$(parse_history "$CLAUDE_HISTORY" "$from_line")"
        count="$(echo "$entries" | jq length)"
        log "Captured $count conversations"
        echo "$entries"
        ;;
    --stats)
        echo "Claude history source:"
        [[ -f "$CLAUDE_HISTORY" ]] && echo "  File: $CLAUDE_HISTORY ($(wc -l < "$CLAUDE_HISTORY") lines)" || echo "  File: not found"
        echo "  Last read line: $(get_last_line)"
        echo "  Min messages: $MIN_MESSAGES"
        ;;
    --help) echo "Usage: $0 --capture | --stats"
            echo "  Env: CLAUDE_HISTORY=path MIN_MESSAGES=3" ;;
    *)      echo "Usage: $0 --capture | --stats" ;;
esac
