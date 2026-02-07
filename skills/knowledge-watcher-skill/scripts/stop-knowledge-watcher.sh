#!/usr/bin/env bash
# stop-knowledge-watcher.sh - Arrête le Knowledge Watcher Agent (Linux)
# Équivalent de Stop-KnowledgeWatcher.ps1

set -euo pipefail

# Répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${SKILL_DIR}/data"
STATE_FILE="${DATA_DIR}/state.json"
PID_FILE="${DATA_DIR}/watcher.pid"
LOG_DIR="${DATA_DIR}/logs"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

log_message() {
    local level="$1"
    local message="$2"
    local timestamp
    timestamp=$(date -Iseconds)
    local log_file="${LOG_DIR}/knowledge-watcher-$(date +%Y-%m-%d).log"

    mkdir -p "$LOG_DIR"
    echo "${timestamp} [${level}] ${message}" >> "$log_file"
}

clear_state() {
    if [[ -f "$STATE_FILE" ]]; then
        local updated
        updated=$(jq '.watchersPid = null | .watchersStarted = null' "$STATE_FILE" 2>/dev/null) || updated='{"watchersPid": null, "watchersStarted": null}'
        echo "$updated" > "$STATE_FILE"
    fi
    rm -f "$PID_FILE"
}

stop_watchers() {
    # Vérifier si le PID file existe
    if [[ ! -f "$PID_FILE" ]]; then
        echo -e "${YELLOW}ℹ️  Knowledge Watcher is not running${NC}"
        return 0
    fi

    local pid
    pid=$(cat "$PID_FILE")

    if [[ -z "$pid" ]]; then
        echo -e "${YELLOW}ℹ️  Knowledge Watcher is not running${NC}"
        clear_state
        return 0
    fi

    # Vérifier si le processus existe
    if ! kill -0 "$pid" 2>/dev/null; then
        echo -e "${YELLOW}ℹ️  Process ${pid} not found (already stopped?)${NC}"
        clear_state
        return 0
    fi

    echo -e "${CYAN}⏹️  Stopping Knowledge Watcher (PID: ${pid})...${NC}"

    # Envoyer SIGTERM pour arrêt gracieux
    kill -TERM "$pid" 2>/dev/null || true
    sleep 2

    # Vérifier si arrêté
    if kill -0 "$pid" 2>/dev/null; then
        echo -e "${YELLOW}   Process still running, sending SIGKILL...${NC}"
        kill -9 "$pid" 2>/dev/null || true
        sleep 1
    fi

    # Tuer aussi tous les processus inotifywait liés
    local inotify_pids
    inotify_pids=$(pgrep -f "inotifywait.*knowledge-watcher" 2>/dev/null || true)
    if [[ -n "$inotify_pids" ]]; then
        echo -e "${GRAY}   Stopping ${inotify_pids} inotifywait process(es)...${NC}"
        echo "$inotify_pids" | xargs -r kill 2>/dev/null || true
    fi

    # Nettoyer l'état
    clear_state

    echo -e "${GREEN}✅ Knowledge Watcher stopped${NC}"
    log_message "INFO" "Knowledge Watcher stopped via stop-knowledge-watcher.sh"
}

# Exécution
stop_watchers
