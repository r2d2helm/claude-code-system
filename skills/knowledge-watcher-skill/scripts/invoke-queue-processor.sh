#!/usr/bin/env bash
# invoke-queue-processor.sh - Traite la queue Knowledge Watcher avec rate limiting
# MF14: Concurrence configurable (defaut 3) pour eviter les tempetes API
# MF15: Dedup cross-tiers via processed-hashes.json

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${SKILL_DIR}/data"
CONFIG_FILE="${SKILL_DIR}/config/config.json"
QUEUE_FILE="${DATA_DIR}/queue.json"
HASHES_FILE="${DATA_DIR}/processed-hashes.json"
LOG_DIR="${DATA_DIR}/logs"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m'

# Arguments
BATCH_SIZE="${1:-10}"
if [[ "${1:-}" == "--batch-size" ]]; then
    BATCH_SIZE="${2:-10}"
fi

# Lire la config
MAX_CONCURRENT=$(jq -r '.processing.maxConcurrentProcessing // 3' "$CONFIG_FILE" 2>/dev/null || echo 3)
CLAUDE_TIMEOUT=$(jq -r '.processing.claudeTimeout // 120000' "$CONFIG_FILE" 2>/dev/null || echo 120000)
CLAUDE_TIMEOUT_SEC=$((CLAUDE_TIMEOUT / 1000))
VAULT_PATH=$(jq -r '.paths.obsidianVault' "$CONFIG_FILE" 2>/dev/null || echo "$HOME/Documents/Knowledge")
CLAUDE_CLI=$(jq -r '.paths.claudeCli // "claude"' "$CONFIG_FILE" 2>/dev/null || echo "claude")

log_message() {
    local level="$1"
    local message="$2"
    local timestamp
    timestamp=$(date -Iseconds)
    local log_file="${LOG_DIR}/queue-processor-$(date +%Y-%m-%d).log"
    mkdir -p "$LOG_DIR"
    echo "${timestamp} [${level}] ${message}" >> "$log_file"
}

# ============================================================
# MF15: Dedup cross-tiers - Processed hashes registry
# ============================================================

init_hashes_registry() {
    if [[ ! -f "$HASHES_FILE" ]]; then
        echo '{}' > "$HASHES_FILE"
    fi
}

is_hash_processed() {
    local hash="$1"
    jq -e --arg h "$hash" 'has($h)' "$HASHES_FILE" 2>/dev/null | grep -q "true"
}

register_hash() {
    local hash="$1"
    local source_path="$2"
    local timestamp
    timestamp=$(date -Iseconds)
    local updated
    updated=$(jq --arg h "$hash" --arg p "$source_path" --arg t "$timestamp" \
        '. + {($h): {"path": $p, "processed_at": $t}}' "$HASHES_FILE")
    echo "$updated" > "$HASHES_FILE"
}

# Cleanup hashes older than 365 days (keep registry compact)
cleanup_old_hashes() {
    local cutoff
    cutoff=$(date -d "-365 days" -Iseconds 2>/dev/null || date -v-365d -Iseconds 2>/dev/null || echo "")
    if [[ -z "$cutoff" ]]; then
        return 0
    fi
    local updated
    updated=$(jq --arg cutoff "$cutoff" \
        'to_entries | map(select(.value.processed_at > $cutoff)) | from_entries' \
        "$HASHES_FILE" 2>/dev/null)
    if [[ -n "$updated" ]]; then
        echo "$updated" > "$HASHES_FILE"
    fi
}

# ============================================================
# MF14: Rate-limited queue processing
# ============================================================

process_single_item() {
    local item_json="$1"
    local item_id item_path item_hash item_status

    item_id=$(echo "$item_json" | jq -r '.id')
    item_path=$(echo "$item_json" | jq -r '.path')
    item_hash=$(echo "$item_json" | jq -r '.hash')
    item_status=$(echo "$item_json" | jq -r '.status')

    # Skip non-pending items
    if [[ "$item_status" != "pending" ]]; then
        return 0
    fi

    # MF15: Check cross-tier dedup
    if is_hash_processed "$item_hash"; then
        log_message "INFO" "Cross-tier duplicate skipped: $item_path (hash=$item_hash)"
        echo -e "  ${YELLOW}SKIP${NC} $item_path (cross-tier duplicate)"
        # Mark as skipped in queue
        update_item_status "$item_id" "skipped_duplicate"
        return 0
    fi

    # Check file exists
    if [[ ! -f "$item_path" ]]; then
        log_message "WARN" "File not found: $item_path"
        update_item_status "$item_id" "error_not_found"
        return 0
    fi

    echo -e "  ${CYAN}PROC${NC} $item_path"

    # Mark as processing
    update_item_status "$item_id" "processing"

    # Process via Claude CLI (with timeout)
    local result=0
    if command -v "$CLAUDE_CLI" &>/dev/null; then
        timeout "${CLAUDE_TIMEOUT_SEC}s" "$CLAUDE_CLI" -p \
            "Resume ce fichier en note Obsidian avec frontmatter YAML. Fichier: $item_path" \
            --output-format text 2>/dev/null || result=$?
    else
        log_message "WARN" "Claude CLI not found, using fallback"
        result=1
    fi

    if [[ $result -eq 0 ]]; then
        update_item_status "$item_id" "processed"
        register_hash "$item_hash" "$item_path"
        echo -e "  ${GREEN}DONE${NC} $item_path"
        log_message "INFO" "Processed: $item_path"
    else
        update_item_status "$item_id" "error"
        echo -e "  ${RED}FAIL${NC} $item_path"
        log_message "ERROR" "Failed to process: $item_path (exit=$result)"
    fi
}

update_item_status() {
    local item_id="$1"
    local new_status="$2"
    (
        flock -x 200
        local updated
        updated=$(jq --arg id "$item_id" --arg status "$new_status" \
            '(.items[] | select(.id == $id)).status = $status' \
            "$QUEUE_FILE" 2>/dev/null)
        if [[ -n "$updated" ]]; then
            echo "$updated" > "$QUEUE_FILE"
        fi
    ) 200>"${QUEUE_FILE}.lock"
}

# ============================================================
# Main
# ============================================================

main() {
    init_hashes_registry

    # Check queue exists
    if [[ ! -f "$QUEUE_FILE" ]] || [[ ! -s "$QUEUE_FILE" ]]; then
        echo -e "${YELLOW}Queue is empty${NC}"
        exit 0
    fi

    # Get pending items
    local pending_count
    pending_count=$(jq '[.items[] | select(.status == "pending")] | length' "$QUEUE_FILE" 2>/dev/null || echo 0)

    if [[ "$pending_count" -eq 0 ]]; then
        echo -e "${YELLOW}No pending items in queue${NC}"
        exit 0
    fi

    local to_process=$((pending_count < BATCH_SIZE ? pending_count : BATCH_SIZE))

    echo -e "${CYAN}Processing ${to_process} item(s) (max concurrent: ${MAX_CONCURRENT})...${NC}"
    echo ""
    log_message "INFO" "Starting queue processing: $to_process items, max_concurrent=$MAX_CONCURRENT"

    # Extract pending items
    local items
    items=$(jq -c "[.items[] | select(.status == \"pending\")] | .[0:${to_process}] | .[]" "$QUEUE_FILE" 2>/dev/null)

    local processed=0
    local errors=0
    local skipped=0
    local running=0

    # Rate-limited processing with semaphore
    while IFS= read -r item; do
        # Wait if at max concurrency
        while [[ $running -ge $MAX_CONCURRENT ]]; do
            wait -n 2>/dev/null || true
            running=$((running - 1))
        done

        # Process item in background
        (
            process_single_item "$item"
        ) &
        running=$((running + 1))

    done <<< "$items"

    # Wait for remaining background jobs
    wait

    # Count results
    processed=$(jq '[.items[] | select(.status == "processed")] | length' "$QUEUE_FILE" 2>/dev/null || echo 0)
    errors=$(jq '[.items[] | select(.status | startswith("error"))] | length' "$QUEUE_FILE" 2>/dev/null || echo 0)
    skipped=$(jq '[.items[] | select(.status == "skipped_duplicate")] | length' "$QUEUE_FILE" 2>/dev/null || echo 0)

    echo ""
    echo "=================================================="
    echo -e "  ${GREEN}Processed${NC} : ${processed}"
    echo -e "  ${RED}Errors${NC}    : ${errors}"
    echo -e "  ${YELLOW}Skipped${NC}   : ${skipped} (cross-tier dedup)"
    echo "=================================================="

    log_message "INFO" "Queue processing complete: processed=$processed errors=$errors skipped=$skipped"

    # Periodic hash cleanup
    cleanup_old_hashes
}

main "$@"
