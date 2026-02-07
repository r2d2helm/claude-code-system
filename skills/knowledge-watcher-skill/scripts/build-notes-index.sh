#!/usr/bin/env bash
# build-notes-index.sh - Construit l'index des notes pour auto-linking (Linux)
# Équivalent de Build-NotesIndex.ps1

set -euo pipefail

# Répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${SKILL_DIR}/data"
CONFIG_FILE="${SKILL_DIR}/config/config.json"
LOG_DIR="${DATA_DIR}/logs"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Paramètres
VAULT_PATH="${1:-}"
OUTPUT_PATH="${2:-${DATA_DIR}/notes-index.json}"

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
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}Dépendance manquante: jq${NC}"
        echo "Installation: sudo apt install jq"
        exit 1
    fi
}

get_vault_path() {
    # Récupère le vault path depuis la config si non fourni en paramètre
    if [[ -z "$VAULT_PATH" ]]; then
        if [[ -f "$CONFIG_FILE" ]]; then
            VAULT_PATH=$(jq -r '.paths.obsidianVault // empty' "$CONFIG_FILE" 2>/dev/null || echo "")
            # Convertir les chemins Windows en Linux si nécessaire
            VAULT_PATH=$(echo "$VAULT_PATH" | sed 's|\\|/|g' | sed 's|C:|/mnt/c|g; s|D:|/mnt/d|g')
        fi
    fi

    # Fallback: utiliser le home de l'utilisateur
    if [[ -z "$VAULT_PATH" ]]; then
        VAULT_PATH="${HOME}/Knowledge"
    fi

    echo "$VAULT_PATH"
}

extract_frontmatter() {
    # Extrait le contenu du frontmatter YAML d'un fichier
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    # Vérifier si le fichier commence par ---
    if [[ "$content" =~ ^---[[:space:]] ]]; then
        # Extraire jusqu'au deuxième ---
        echo "$content" | sed -n '/^---$/,/^---$/p' | sed '1d;$d'
    else
        echo ""
    fi
}

extract_field() {
    # Extrait un champ du frontmatter YAML
    local yaml="$1"
    local field="$2"

    # Extraction simple pour les champs inline
    local value
    value=$(echo "$yaml" | grep -E "^${field}:" | head -1 | sed "s/^${field}:[[:space:]]*//" | sed 's/^["'\'']//' | sed 's/["'\'']$//' | tr -d '\r')

    echo "$value"
}

extract_list_field() {
    # Extrait un champ liste du frontmatter YAML
    local yaml="$1"
    local field="$2"

    # Format inline: field: [item1, item2]
    local inline
    inline=$(echo "$yaml" | grep -E "^${field}:[[:space:]]*\[" | sed "s/^${field}:[[:space:]]*\[//" | sed 's/\]$//' | tr -d '\r')

    if [[ -n "$inline" ]]; then
        echo "$inline" | tr ',' '\n' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//' | sed 's/^["'\'']//' | sed 's/["'\'']$//' | grep -v '^$'
        return
    fi

    # Format liste YAML multilignes
    local in_list=false
    echo "$yaml" | while IFS= read -r line; do
        if [[ "$line" =~ ^${field}: ]]; then
            in_list=true
            continue
        fi
        if [[ "$in_list" == true ]]; then
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]] ]]; then
                echo "$line" | sed 's/^[[:space:]]*-[[:space:]]*//' | sed 's/^["'\'']//' | sed 's/["'\'']$//' | tr -d '\r'
            elif [[ ! "$line" =~ ^[[:space:]] ]]; then
                break
            fi
        fi
    done
}

get_note_title() {
    # Extrait le titre d'une note (frontmatter ou premier heading)
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    # D'abord chercher dans le frontmatter
    local fm
    fm=$(extract_frontmatter "$file")
    local title
    title=$(extract_field "$fm" "title")

    if [[ -n "$title" ]]; then
        echo "$title"
        return
    fi

    # Sinon chercher le premier heading
    title=$(echo "$content" | grep -m1 '^# ' | sed 's/^# //' | tr -d '\r')

    if [[ -n "$title" ]]; then
        echo "$title"
        return
    fi

    # Fallback: nom du fichier sans extension
    basename "$file" .md
}

build_index() {
    check_dependencies

    local vault_path
    vault_path=$(get_vault_path)

    echo -e "${CYAN}Building notes index from: ${vault_path}${NC}"

    if [[ ! -d "$vault_path" ]]; then
        echo -e "${RED}Vault path not found: ${vault_path}${NC}"
        log_message "ERROR" "Vault path not found: $vault_path"
        exit 1
    fi

    # Créer le répertoire de données si nécessaire
    mkdir -p "$(dirname "$OUTPUT_PATH")"

    # Initialiser les compteurs
    local note_count=0
    local term_count=0

    # Tableaux temporaires (fichiers)
    local notes_file
    notes_file=$(mktemp)
    local terms_file
    terms_file=$(mktemp)

    # Initialiser les fichiers JSON
    echo "[]" > "$notes_file"
    echo "{}" > "$terms_file"

    # Scanner tous les fichiers .md
    while IFS= read -r -d '' file; do
        # Obtenir le chemin relatif
        local relative_path="${file#${vault_path}/}"

        # Ignorer les dossiers système
        if [[ "$relative_path" =~ ^_Templates/ ]] || \
           [[ "$relative_path" =~ ^\.obsidian/ ]]; then
            continue
        fi

        # Lire le contenu
        local content
        content=$(cat "$file" 2>/dev/null || echo "")

        # Ignorer les fichiers vides
        if [[ -z "$content" ]] || [[ "$content" =~ ^[[:space:]]*$ ]]; then
            continue
        fi

        # Extraire les métadonnées
        local fm
        fm=$(extract_frontmatter "$file")
        local title
        title=$(get_note_title "$file")
        local basename_note
        basename_note=$(basename "$file" .md)
        local last_modified
        last_modified=$(stat -c '%Y' "$file" 2>/dev/null || stat -f '%m' "$file" 2>/dev/null || echo "0")
        last_modified=$(date -d "@$last_modified" -Iseconds 2>/dev/null || date -r "$last_modified" -Iseconds 2>/dev/null || echo "")

        # Extraire aliases et tags
        local aliases_json="[]"
        local tags_json="[]"

        if [[ -n "$fm" ]]; then
            # Extraire les aliases
            local aliases_list
            aliases_list=$(extract_list_field "$fm" "aliases")
            if [[ -n "$aliases_list" ]]; then
                aliases_json=$(echo "$aliases_list" | jq -R -s 'split("\n") | map(select(length > 0))')
            fi

            # Extraire les tags
            local tags_list
            tags_list=$(extract_list_field "$fm" "tags")
            if [[ -n "$tags_list" ]]; then
                tags_json=$(echo "$tags_list" | jq -R -s 'split("\n") | map(select(length > 0))')
            fi
        fi

        # Créer l'entrée de note
        local note_entry
        note_entry=$(jq -n \
            --arg path "$file" \
            --arg relativePath "$relative_path" \
            --arg baseName "$basename_note" \
            --arg title "$title" \
            --argjson aliases "$aliases_json" \
            --argjson tags "$tags_json" \
            --arg lastModified "$last_modified" \
            '{
                path: $path,
                relativePath: $relativePath,
                baseName: $baseName,
                title: $title,
                aliases: $aliases,
                tags: $tags,
                lastModified: $lastModified
            }')

        # Ajouter à la liste des notes
        local current_notes
        current_notes=$(cat "$notes_file")
        echo "$current_notes" | jq --argjson entry "$note_entry" '. += [$entry]' > "$notes_file"

        # Ajouter les termes de recherche
        local current_terms
        current_terms=$(cat "$terms_file")

        # Titre
        if [[ -n "$title" ]]; then
            local title_lower
            title_lower=$(echo "$title" | tr '[:upper:]' '[:lower:]')
            current_terms=$(echo "$current_terms" | jq \
                --arg term "$title_lower" \
                --arg original "$title" \
                --arg path "$file" \
                'if .[$term] then .[$term].paths += [$path] | .[$term].paths |= unique else .[$term] = {original: $original, paths: [$path]} end')
        fi

        # Basename
        local basename_lower
        basename_lower=$(echo "$basename_note" | tr '[:upper:]' '[:lower:]')
        current_terms=$(echo "$current_terms" | jq \
            --arg term "$basename_lower" \
            --arg original "$basename_note" \
            --arg path "$file" \
            'if .[$term] then .[$term].paths += [$path] | .[$term].paths |= unique else .[$term] = {original: $original, paths: [$path]} end')

        # Aliases
        while IFS= read -r alias; do
            if [[ -n "$alias" ]]; then
                local alias_lower
                alias_lower=$(echo "$alias" | tr '[:upper:]' '[:lower:]')
                current_terms=$(echo "$current_terms" | jq \
                    --arg term "$alias_lower" \
                    --arg original "$alias" \
                    --arg path "$file" \
                    'if .[$term] then .[$term].paths += [$path] | .[$term].paths |= unique else .[$term] = {original: $original, paths: [$path]} end')
            fi
        done < <(echo "$aliases_json" | jq -r '.[]?')

        echo "$current_terms" > "$terms_file"

        ((note_count++)) || true

        # Afficher progression tous les 100 fichiers
        if (( note_count % 100 == 0 )); then
            echo -e "${GRAY}  Scanning... ${note_count} notes${NC}"
        fi

    done < <(find "$vault_path" -type f -name "*.md" -print0 2>/dev/null)

    # Compter les termes
    term_count=$(jq 'keys | length' "$terms_file")

    # Construire l'index final
    local timestamp
    timestamp=$(date -Iseconds)

    local final_notes
    final_notes=$(cat "$notes_file")
    local final_terms
    final_terms=$(cat "$terms_file")

    jq -n \
        --arg version "1.0" \
        --arg vaultPath "$vault_path" \
        --arg generatedAt "$timestamp" \
        --argjson noteCount "$note_count" \
        --argjson termCount "$term_count" \
        --argjson notes "$final_notes" \
        --argjson terms "$final_terms" \
        '{
            version: $version,
            vaultPath: $vaultPath,
            generatedAt: $generatedAt,
            noteCount: $noteCount,
            termCount: $termCount,
            notes: $notes,
            terms: $terms
        }' > "$OUTPUT_PATH"

    # Nettoyer les fichiers temporaires
    rm -f "$notes_file" "$terms_file"

    echo -e "${GREEN}Index built successfully!${NC}"
    echo -e "${GRAY}  Notes: ${note_count}${NC}"
    echo -e "${GRAY}  Terms: ${term_count}${NC}"
    echo -e "${GRAY}  Output: ${OUTPUT_PATH}${NC}"

    log_message "INFO" "Built notes index: ${note_count} notes, ${term_count} terms"
}

# Exécution
build_index
