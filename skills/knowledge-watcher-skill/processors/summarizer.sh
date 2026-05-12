#!/usr/bin/env bash
set -euo pipefail
# Summarizer - Generate summary/abstract for notes using Claude CLI
# Algorithm:
#   1. Read note content, truncate if > MAX_LENGTH chars
#   2. Build prompt based on content type (conversation, code, concept, troubleshooting)
#   3. Call Claude CLI (claude --print -p "prompt") with timeout
#   4. Parse JSON response: {summary, keyPoints, concepts, actions, suggestedTags}
#   5. Fallback: extract first lines + bullet points if Claude unavailable

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="${SKILL_DIR}/config/config.json"
MAX_LENGTH="${MAX_LENGTH:-50000}"
CLAUDE_TIMEOUT="${CLAUDE_TIMEOUT:-30}"

log() { echo "[$(date '+%H:%M:%S')] [summarizer] $*" >&2; }

# Fallback summary: extract first lines + bullet points
fallback_summary() {
    local content="$1" type="$2"
    local summary first_lines key_points

    # First 5 non-empty lines joined
    first_lines="$(echo "$content" | grep -v '^\s*$' | head -5 | tr '\n' ' ' | head -c 200)"
    summary="${first_lines}..."

    # Extract bullet points as key points
    key_points="$(echo "$content" | grep -E '^\s*[-*]\s+' | sed 's/^\s*[-*]\s*//' | head -5 | jq -R . | jq -s .)"

    jq -n --arg summary "$summary" --argjson kp "$key_points" \
        '{summary:$summary, keyPoints:$kp, concepts:[], actions:[], suggestedTags:[], source:"fallback"}'
}

# Build prompt for Claude based on content type
build_prompt() {
    local type="$1" content="$2"

    local type_focus=""
    case "$type" in
        conversation) type_focus="TYPE: Conversation Claude\nFocus: decisions prises, problemes resolus, code cree, concepts discutes." ;;
        code)         type_focus="TYPE: Code/Script\nFocus: but du code, fonctions principales, dependances, usage." ;;
        concept)      type_focus="TYPE: Concept/Idee\nFocus: definition, importance, applications, liens avec d'autres concepts." ;;
        troubleshooting) type_focus="TYPE: Troubleshooting\nFocus: probleme rencontre, cause identifiee, solution appliquee, prevention." ;;
        *)            type_focus="TYPE: Note generale\nFocus: sujet principal, informations cles, actions potentielles." ;;
    esac

    cat <<PROMPT
Tu es un assistant specialise dans la capture de connaissances. Analyse le contenu suivant et genere un resume structure EN FRANCAIS.

IMPORTANT: Reponds UNIQUEMENT au format JSON suivant, sans texte avant ou apres:
{
  "summary": "Resume en 2-3 phrases",
  "keyPoints": ["Point 1", "Point 2", "Point 3"],
  "concepts": ["Concept1", "Concept2"],
  "actions": ["Action 1", "Action 2"],
  "suggestedTags": ["tag1", "tag2"]
}

$(printf '%b' "$type_focus")

CONTENU A ANALYSER:
---
${content}
---

Reponds en JSON valide uniquement.
PROMPT
}

# Summarize content using Claude CLI
summarize() {
    local content="$1" type="${2:-note}"

    # Truncate if too long
    if [[ ${#content} -gt $MAX_LENGTH ]]; then
        content="${content:0:$MAX_LENGTH}

[... contenu tronque ...]"
        log "WARN: Content truncated to $MAX_LENGTH chars"
    fi

    # Try Claude CLI
    local claude_cmd=""
    if command -v claude &>/dev/null; then
        claude_cmd="claude"
    elif [[ -f "$HOME/.claude/local/claude" ]]; then
        claude_cmd="$HOME/.claude/local/claude"
    fi

    if [[ -z "$claude_cmd" ]]; then
        log "WARN: Claude CLI not found, using fallback"
        fallback_summary "$content" "$type"
        return
    fi

    local prompt
    prompt="$(build_prompt "$type" "$content")"

    local tmp_prompt
    tmp_prompt="$(mktemp)"
    echo "$prompt" > "$tmp_prompt"

    local output
    if output="$(timeout "${CLAUDE_TIMEOUT}s" "$claude_cmd" --print -p "$(cat "$tmp_prompt")" 2>/dev/null)"; then
        rm -f "$tmp_prompt"

        # Extract JSON from response
        local json_str
        json_str="$(echo "$output" | grep -oP '\{[\s\S]*\}' | head -1)" || true

        if [[ -n "$json_str" ]] && echo "$json_str" | jq . &>/dev/null; then
            echo "$json_str" | jq '{
                summary: (.summary // "Resume non disponible"),
                keyPoints: (.keyPoints // []),
                concepts: (.concepts // []),
                actions: (.actions // []),
                suggestedTags: (.suggestedTags // []),
                source: "claude"
            }'
            return
        fi
    fi

    rm -f "$tmp_prompt"
    log "WARN: Claude CLI failed, using fallback"
    fallback_summary "$content" "$type"
}

# --- Main ---
case "${1:-}" in
    --summarize)
        [[ -n "${2:-}" ]] || { log "Usage: $0 --summarize <file> [type]"; exit 1; }
        [[ -f "$2" ]] || { log "ERROR: File not found: $2"; exit 1; }
        content="$(cat "$2")"
        summarize "$content" "${3:-note}"
        ;;
    --fallback)
        [[ -n "${2:-}" ]] || { log "Usage: $0 --fallback <file> [type]"; exit 1; }
        content="$(cat "$2")"
        fallback_summary "$content" "${3:-note}"
        ;;
    --help) echo "Usage: $0 --summarize|--fallback <file> [type]"
            echo "  Types: conversation, code, concept, troubleshooting, note"
            echo "  Env: MAX_LENGTH=50000 CLAUDE_TIMEOUT=30" ;;
    *)      echo "Usage: $0 --summarize|--fallback <file> [type]" ;;
esac
