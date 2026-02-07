#!/usr/bin/env bash
# start-knowledge-watcher.sh - Démarre le Knowledge Watcher Agent (Linux)
# Équivalent de Start-KnowledgeWatcher.ps1
# Utilise inotifywait au lieu de FileSystemWatcher

set -euo pipefail

# Répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${SKILL_DIR}/data"
CONFIG_FILE="${SKILL_DIR}/config/config.json"
SOURCES_FILE="${SKILL_DIR}/config/sources.json"
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

# Mode background
BACKGROUND=false
if [[ "${1:-}" == "-b" || "${1:-}" == "--background" ]]; then
    BACKGROUND=true
fi

# Fonctions utilitaires
log_message() {
    local level="$1"
    local message="$2"
    local timestamp
    timestamp=$(date -Iseconds)
    local log_file="${LOG_DIR}/knowledge-watcher-$(date +%Y-%m-%d).log"

    mkdir -p "$LOG_DIR"
    echo "${timestamp} [${level}] ${message}" >> "$log_file"
}

check_dependencies() {
    local missing=()

    if ! command -v inotifywait &> /dev/null; then
        missing+=("inotify-tools")
    fi

    if ! command -v jq &> /dev/null; then
        missing+=("jq")
    fi

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo -e "${RED}Dépendances manquantes: ${missing[*]}${NC}"
        echo "Installation: sudo apt install ${missing[*]}"
        exit 1
    fi
}

get_config_value() {
    local key="$1"
    jq -r "$key // empty" "$CONFIG_FILE" 2>/dev/null || echo ""
}

get_tier1_sources() {
    # Récupère les sources Tier 1 de type directory et activées
    jq -r '.sources[] | select(.tier == 1 and .enabled == true and .type == "directory") | .path' "$SOURCES_FILE" 2>/dev/null | \
    sed 's|\\|/|g' | \
    sed 's|C:|/mnt/c|g; s|D:|/mnt/d|g' || true
}

get_claude_history_path() {
    # Récupère le chemin de l'historique Claude
    jq -r '.sources[] | select(.id == "claude-history" and .enabled == true) | .path' "$SOURCES_FILE" 2>/dev/null | \
    sed 's|\\|/|g' | \
    sed 's|C:|/mnt/c|g; s|D:|/mnt/d|g' || true
}

get_ignore_patterns() {
    # Récupère les patterns à ignorer
    jq -r '.watchers.ignorePatterns[]?' "$CONFIG_FILE" 2>/dev/null || echo -e "*.tmp\n*.bak\n~$*"
}

save_state() {
    local pid="$1"
    local timestamp
    timestamp=$(date -Iseconds)

    mkdir -p "$DATA_DIR"
    cat > "$STATE_FILE" << EOF
{
  "watchersPid": ${pid},
  "watchersStarted": "${timestamp}",
  "platform": "linux"
}
EOF
}

clear_state() {
    if [[ -f "$STATE_FILE" ]]; then
        jq '.watchersPid = null | .watchersStarted = null' "$STATE_FILE" > "${STATE_FILE}.tmp" && \
        mv "${STATE_FILE}.tmp" "$STATE_FILE"
    fi
    rm -f "$PID_FILE"
}

is_running() {
    if [[ -f "$PID_FILE" ]]; then
        local pid
        pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            return 0
        fi
    fi
    return 1
}

process_file_change() {
    local file="$1"
    local event="$2"
    local queue_file="${DATA_DIR}/queue.json"

    # Ignorer les fichiers temporaires et patterns exclus
    local filename
    filename=$(basename "$file")

    # Vérifier les patterns à ignorer
    if [[ "$filename" =~ ^~\$ ]] || \
       [[ "$filename" =~ \.tmp$ ]] || \
       [[ "$filename" =~ \.bak$ ]] || \
       [[ "$filename" =~ ^\.git ]] || \
       [[ "$file" =~ /node_modules/ ]] || \
       [[ "$file" =~ /\.obsidian/ ]]; then
        return 0
    fi

    # Vérifier que le fichier existe toujours
    if [[ ! -f "$file" ]]; then
        return 0
    fi

    # Calculer le hash du contenu pour déduplication
    local content_hash
    content_hash=$(sha256sum "$file" 2>/dev/null | cut -d' ' -f1 || echo "")

    if [[ -z "$content_hash" ]]; then
        return 0
    fi

    # Ajouter à la queue
    local timestamp
    timestamp=$(date -Iseconds)
    local item
    item=$(jq -n \
        --arg path "$file" \
        --arg event "$event" \
        --arg hash "$content_hash" \
        --arg ts "$timestamp" \
        '{
            id: ($ts + "-" + ($hash | .[0:8])),
            path: $path,
            event: $event,
            hash: $hash,
            timestamp: $ts,
            status: "pending"
        }')

    # Créer la queue si elle n'existe pas
    if [[ ! -f "$queue_file" ]] || [[ ! -s "$queue_file" ]]; then
        echo '{"items": [], "lastUpdated": null}' > "$queue_file"
    fi

    # Vérifier si le hash existe déjà (déduplication)
    local existing
    existing=$(jq -r --arg hash "$content_hash" '.items[] | select(.hash == $hash) | .id' "$queue_file" 2>/dev/null || echo "")

    if [[ -n "$existing" ]]; then
        log_message "DEBUG" "Duplicate detected, skipping: $file"
        return 0
    fi

    # Ajouter l'item à la queue (avec lock)
    (
        flock -x 200
        local updated
        updated=$(jq --argjson item "$item" --arg ts "$timestamp" \
            '.items += [$item] | .lastUpdated = $ts' "$queue_file")
        echo "$updated" > "$queue_file"
    ) 200>"${queue_file}.lock"

    log_message "INFO" "Queued: $file ($event)"
    echo -e "${GREEN}  + ${file}${NC}"
}

start_watchers() {
    check_dependencies

    # Vérifier si déjà en cours
    if is_running; then
        local pid
        pid=$(cat "$PID_FILE")
        echo -e "${YELLOW}⚠️  Knowledge Watcher already running (PID: ${pid})${NC}"
        return 1
    fi

    echo -e "${CYAN}🚀 Starting Knowledge Watcher...${NC}"

    # Récupérer les sources Tier 1
    local sources=()
    while IFS= read -r source; do
        if [[ -n "$source" && -d "$source" ]]; then
            sources+=("$source")
        fi
    done < <(get_tier1_sources)

    # Ajouter le répertoire Claude history
    local claude_history
    claude_history=$(get_claude_history_path)
    if [[ -n "$claude_history" ]]; then
        local claude_dir
        claude_dir=$(dirname "$claude_history")
        if [[ -d "$claude_dir" ]]; then
            sources+=("$claude_dir")
        fi
    fi

    if [[ ${#sources[@]} -eq 0 ]]; then
        echo -e "${RED}❌ No valid sources found${NC}"
        log_message "ERROR" "No valid Tier 1 sources found"
        return 1
    fi

    # Afficher les sources surveillées
    for source in "${sources[@]}"; do
        echo -e "  ${GREEN}✅ Watching: ${source}${NC}"
        log_message "INFO" "Started watcher for: $source"
    done

    # Récupérer le debounce configuré (en secondes)
    local debounce_ms
    debounce_ms=$(get_config_value '.watchers.debounceMs')
    local debounce_sec
    debounce_sec=$(echo "scale=1; ${debounce_ms:-2000} / 1000" | bc)

    # Sauvegarder le PID du processus principal
    mkdir -p "$DATA_DIR"
    echo $$ > "$PID_FILE"
    save_state $$

    echo ""
    echo -e "${GREEN}✅ Knowledge Watcher started${NC}"
    echo -e "${GRAY}   PID: $$${NC}"
    echo -e "${GRAY}   Watchers: ${#sources[@]}${NC}"
    echo ""
    echo -e "${GRAY}   Press Ctrl+C to stop...${NC}"

    log_message "INFO" "Knowledge Watcher started with ${#sources[@]} watchers (PID: $$)"

    # Variables pour le nettoyage périodique
    local last_cleanup
    last_cleanup=$(date +%s)
    local cleanup_interval
    cleanup_interval=$(get_config_value '.processing.cleanupIntervalHours')
    cleanup_interval=${cleanup_interval:-6}
    local cleanup_interval_sec=$((cleanup_interval * 3600))

    # Gestionnaire de signal pour arrêt propre
    trap 'cleanup_and_exit' SIGINT SIGTERM

    # Lancer inotifywait pour toutes les sources
    # Utilise --monitor pour surveillance continue
    # Événements: modify (changement), create (création), moved_to (renommage)
    inotifywait -m -r \
        --format '%w%f|%e' \
        -e modify -e create -e moved_to \
        "${sources[@]}" 2>/dev/null | \
    while IFS='|' read -r filepath events; do
        # Debounce simple (attendre avant de traiter)
        sleep "$debounce_sec"

        # Traiter le fichier
        if [[ -f "$filepath" ]]; then
            process_file_change "$filepath" "$events"
        fi

        # Vérifier si nettoyage périodique nécessaire
        local now
        now=$(date +%s)
        if (( now - last_cleanup >= cleanup_interval_sec )); then
            log_message "INFO" "Periodic cleanup triggered"
            # Le nettoyage pourrait être fait ici
            last_cleanup=$now
        fi
    done
}

cleanup_and_exit() {
    echo ""
    echo -e "${YELLOW}⏹️  Stopping Knowledge Watcher...${NC}"

    # Tuer tous les processus inotifywait enfants
    pkill -P $$ inotifywait 2>/dev/null || true

    # Nettoyer l'état
    clear_state

    log_message "INFO" "Knowledge Watcher stopped"
    echo -e "${YELLOW}⏹️  Knowledge Watcher stopped${NC}"
    exit 0
}

# Exécution
if [[ "$BACKGROUND" == true ]]; then
    # Mode background avec nohup
    nohup "$0" > "${LOG_DIR}/watcher-stdout.log" 2>&1 &
    bg_pid=$!
    echo $bg_pid > "$PID_FILE"
    save_state $bg_pid

    echo -e "${GREEN}✅ Knowledge Watcher started in background${NC}"
    echo -e "${GRAY}   PID: ${bg_pid}${NC}"
    echo -e "${GRAY}   Log: ${LOG_DIR}/watcher-stdout.log${NC}"
else
    start_watchers
fi
