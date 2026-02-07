#!/usr/bin/env bash
# invoke-vault-guardian.sh - Maintenance proactive du vault Obsidian (Linux)
# Équivalent de Invoke-VaultGuardian.ps1

set -uo pipefail
# Note: pas de -e car certaines commandes peuvent retourner non-zéro normalement

# Répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${SKILL_DIR}/data"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Mode d'exécution (health, fix, report, quick)
MODE="${1:-health}"

# Vault path (à adapter ou lire depuis config)
# Par défaut: tente de lire depuis la config de knowledge-watcher-skill
VAULT_PATH="${VAULT_PATH:-}"

if [[ -z "$VAULT_PATH" ]]; then
    KW_CONFIG="${SKILL_DIR}/../knowledge-watcher-skill/config/config.json"
    if [[ -f "$KW_CONFIG" ]]; then
        VAULT_PATH=$(jq -r '.paths.obsidianVault // empty' "$KW_CONFIG" 2>/dev/null || echo "")
        VAULT_PATH=$(echo "$VAULT_PATH" | sed 's|\\|/|g' | sed 's|C:|/mnt/c|g; s|D:|/mnt/d|g')
    fi
fi

if [[ -z "$VAULT_PATH" ]]; then
    VAULT_PATH="${HOME}/Knowledge"
fi

# Résultats du health check
declare -A RESULTS
RESULTS[TotalFiles]=0
RESULTS[Score]="10.0"
RESULTS[Timestamp]=$(date -Iseconds)

# Fichiers temporaires pour les listes
EMPTY_FILES=$(mktemp)
NO_FRONTMATTER=$(mktemp)
BROKEN_LINKS=$(mktemp)
ORPHANS=$(mktemp)
STATUS_ISSUES=$(mktemp)
TAG_ISSUES=$(mktemp)
EMPTY_RELATED=$(mktemp)
DUPLICATE_BASENAMES=$(mktemp)

cleanup_temps() {
    rm -f "$EMPTY_FILES" "$NO_FRONTMATTER" "$BROKEN_LINKS" "$ORPHANS" \
          "$STATUS_ISSUES" "$TAG_ISSUES" "$EMPTY_RELATED" "$DUPLICATE_BASENAMES"
}
trap cleanup_temps EXIT

check_dependencies() {
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}Dépendance manquante: jq${NC}"
        echo "Installation: sudo apt install jq"
        exit 1
    fi
}

get_all_notes() {
    find "$VAULT_PATH" -type f -name "*.md" ! -path "*/.obsidian/*" 2>/dev/null
}

has_frontmatter() {
    local file="$1"
    local content
    content=$(head -n 20 "$file" 2>/dev/null || echo "")
    if [[ "$content" =~ ^---[[:space:]] ]]; then
        if echo "$content" | grep -q '^---$' | head -n 2 | tail -n 1; then
            return 0
        fi
        # Vérification plus robuste
        local fm_end
        fm_end=$(echo "$content" | grep -n '^---$' | head -n 2 | tail -n 1 | cut -d: -f1)
        if [[ -n "$fm_end" && "$fm_end" -gt 1 ]]; then
            return 0
        fi
    fi
    return 1
}

get_frontmatter_field() {
    local file="$1"
    local field="$2"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    # Extraire le frontmatter
    if [[ "$content" =~ ^---[[:space:]] ]]; then
        local fm
        fm=$(echo "$content" | sed -n '/^---$/,/^---$/p' | sed '1d;$d')
        echo "$fm" | grep -E "^${field}:" | head -1 | sed "s/^${field}:[[:space:]]*//" | sed 's/^["'\'']//' | sed 's/["'\'']$//' | tr -d '\r'
    fi
}

remove_code_content() {
    # Supprime les blocs de code et le code inline
    local text="$1"
    # Supprimer les blocs de code
    text=$(echo "$text" | sed '/^```/,/^```/d')
    # Supprimer le code inline
    text=$(echo "$text" | sed 's/`[^`]*`//g')
    echo "$text"
}

invoke_health_check() {
    echo -e "${CYAN}=== VAULT GUARDIAN - HEALTH CHECK ===${NC}"
    echo ""

    if [[ ! -d "$VAULT_PATH" ]]; then
        echo -e "${RED}Vault path not found: ${VAULT_PATH}${NC}"
        exit 1
    fi

    # Collecter toutes les notes
    local all_notes
    all_notes=$(get_all_notes)
    local total_files
    total_files=$(echo "$all_notes" | grep -c '.' || echo "0")
    RESULTS[TotalFiles]=$total_files

    echo "Total notes: ${total_files}"

    # Construire un index des noms de notes
    local note_names_file
    note_names_file=$(mktemp)
    while IFS= read -r file; do
        [[ -z "$file" ]] && continue
        basename "$file" .md >> "$note_names_file"
    done <<< "$all_notes"

    # Construire un index des notes liées (pour détection orphelins)
    local linked_names_file
    linked_names_file=$(mktemp)

    local processed=0
    while IFS= read -r file; do
        [[ -z "$file" ]] && continue
        ((processed++)) || true

        if (( processed % 100 == 0 )); then
            echo -e "${GRAY}  Scanning... ${processed} / ${total_files}${NC}"
        fi

        # Lire le contenu
        local content
        content=$(cat "$file" 2>/dev/null || echo "")

        # Vérifier si vide
        if [[ -z "$content" ]] || [[ "$content" =~ ^[[:space:]]*$ ]]; then
            echo "$file" >> "$EMPTY_FILES"
            continue
        fi

        # Vérifier frontmatter
        if ! has_frontmatter "$file"; then
            echo "$file" >> "$NO_FRONTMATTER"
        fi

        # Extraire le frontmatter pour analyses
        local fm_block=""
        if [[ "$content" =~ ^---[[:space:]] ]]; then
            fm_block=$(echo "$content" | sed -n '/^---$/,/^---$/p' | sed '1d;$d')
        fi

        # Vérifier le status (captured est déprécié)
        local status
        status=$(echo "$fm_block" | grep -E "^status:" | head -1 | sed 's/^status:[[:space:]]*//' | tr -d '\r"'\''')
        if [[ "$status" == "captured" ]]; then
            echo "$file" >> "$STATUS_ISSUES"
        fi

        # Vérifier les tags (pas de majuscule en début, pas d'espaces)
        while IFS= read -r tag; do
            [[ -z "$tag" ]] && continue
            tag=$(echo "$tag" | sed 's/^[[:space:]]*-[[:space:]]*//' | tr -d '\r"'\''')
            if [[ "$tag" =~ ^[A-Z] ]] || [[ "$tag" =~ [[:space:]] ]]; then
                echo "${file}|${tag}" >> "$TAG_ISSUES"
            fi
        done < <(echo "$fm_block" | sed -n '/^tags:/,/^[a-z]/p' | grep '^\s*-' || true)

        # Vérifier related vide
        if echo "$fm_block" | grep -q "^related:"; then
            local has_valid_related=false
            if echo "$fm_block" | grep -qE "^related:\s*\[\s*\]\s*$"; then
                has_valid_related=false
            elif echo "$fm_block" | grep -qE "^related:\s*$"; then
                has_valid_related=false
            elif echo "$fm_block" | grep -qE "^related:\s+\S"; then
                has_valid_related=true
            elif echo "$fm_block" | sed -n '/^related:/,/^[a-z]/p' | grep -q '^\s*-'; then
                has_valid_related=true
            fi
            if [[ "$has_valid_related" == false ]]; then
                echo "$file" >> "$EMPTY_RELATED"
            fi
        else
            echo "$file" >> "$EMPTY_RELATED"
        fi

        # Détecter les liens cassés
        local clean_content
        clean_content=$(remove_code_content "$content")
        while IFS= read -r link; do
            [[ -z "$link" ]] && continue
            # Extraire le nom de la note (avant | et #)
            local target
            target=$(echo "$link" | sed 's/|.*//' | sed 's/#.*//')
            [[ -z "$target" ]] && continue

            # Vérifier si la note cible existe
            if ! grep -qFx "$target" "$note_names_file"; then
                echo "${file}|${target}" >> "$BROKEN_LINKS"
            fi

            # Ajouter aux notes liées (pour orphelins)
            echo "$target" >> "$linked_names_file"
        done < <(echo "$clean_content" | grep -oP '\[\[([^\]|]+)' | sed 's/\[\[//' || true)

    done <<< "$all_notes"

    # Détecter les orphelins (notes sans liens entrants)
    while IFS= read -r file; do
        [[ -z "$file" ]] && continue
        local bn
        bn=$(basename "$file" .md)
        local rel="${file#${VAULT_PATH}/}"

        # Ignorer certains dossiers
        if [[ "$rel" =~ ^_Index/ ]] || [[ "$rel" =~ ^_Templates/ ]] || [[ "$rel" =~ ^_Daily/ ]]; then
            continue
        fi

        if ! grep -qFx "$bn" "$linked_names_file"; then
            echo "$file" >> "$ORPHANS"
        fi
    done <<< "$all_notes"

    # Détecter les doublons de basename
    sort "$note_names_file" | uniq -d | while IFS= read -r dup_name; do
        [[ -z "$dup_name" ]] && continue
        local paths
        paths=$(grep -l "^$" "$VAULT_PATH"/**/"${dup_name}.md" 2>/dev/null || find "$VAULT_PATH" -name "${dup_name}.md" 2>/dev/null | tr '\n' '|')
        echo "${dup_name}|${paths}" >> "$DUPLICATE_BASENAMES"
    done

    # Calculer le score
    local score="10.0"
    local empty_count broken_count orphan_count nofm_count status_count tag_count related_count dup_count

    empty_count=$(wc -l < "$EMPTY_FILES" | tr -d ' ')
    broken_count=$(wc -l < "$BROKEN_LINKS" | tr -d ' ')
    orphan_count=$(wc -l < "$ORPHANS" | tr -d ' ')
    nofm_count=$(wc -l < "$NO_FRONTMATTER" | tr -d ' ')
    status_count=$(wc -l < "$STATUS_ISSUES" | tr -d ' ')
    tag_count=$(wc -l < "$TAG_ISSUES" | tr -d ' ')
    related_count=$(wc -l < "$EMPTY_RELATED" | tr -d ' ')
    dup_count=$(wc -l < "$DUPLICATE_BASENAMES" | tr -d ' ')

    # Pénalités
    if (( empty_count > 0 )); then
        local penalty
        penalty=$(echo "scale=1; if ($empty_count * 0.2 > 1.0) 1.0 else $empty_count * 0.2" | bc)
        score=$(echo "scale=1; $score - $penalty" | bc)
    fi
    if (( nofm_count > 0 )); then
        local penalty
        penalty=$(echo "scale=1; if ($nofm_count * 0.02 > 1.5) 1.5 else $nofm_count * 0.02" | bc)
        score=$(echo "scale=1; $score - $penalty" | bc)
    fi
    if (( broken_count > 0 )); then
        local penalty
        penalty=$(echo "scale=1; if ($broken_count * 0.1 > 2.0) 2.0 else $broken_count * 0.1" | bc)
        score=$(echo "scale=1; $score - $penalty" | bc)
    fi
    if (( orphan_count > 0 && total_files > 0 )); then
        local orphan_rate
        orphan_rate=$(echo "scale=2; $orphan_count / $total_files" | bc)
        if (( $(echo "$orphan_rate > 0.5" | bc -l) )); then
            score=$(echo "scale=1; $score - 2.0" | bc)
        elif (( $(echo "$orphan_rate > 0.3" | bc -l) )); then
            score=$(echo "scale=1; $score - 1.0" | bc)
        elif (( $(echo "$orphan_rate > 0.1" | bc -l) )); then
            score=$(echo "scale=1; $score - 0.5" | bc)
        fi
    fi
    if (( status_count > 0 )); then
        local penalty
        penalty=$(echo "scale=1; if ($status_count * 0.01 > 0.5) 0.5 else $status_count * 0.01" | bc)
        score=$(echo "scale=1; $score - $penalty" | bc)
    fi
    if (( tag_count > 0 )); then
        local penalty
        penalty=$(echo "scale=1; if ($tag_count * 0.05 > 0.5) 0.5 else $tag_count * 0.05" | bc)
        score=$(echo "scale=1; $score - $penalty" | bc)
    fi
    if (( related_count > 0 )); then
        local penalty
        penalty=$(echo "scale=1; if ($related_count * 0.005 > 1.0) 1.0 else $related_count * 0.005" | bc)
        score=$(echo "scale=1; $score - $penalty" | bc)
    fi
    if (( dup_count > 0 )); then
        local penalty
        penalty=$(echo "scale=1; if ($dup_count * 0.02 > 0.5) 0.5 else $dup_count * 0.02" | bc)
        score=$(echo "scale=1; $score - $penalty" | bc)
    fi

    # S'assurer que le score est >= 0
    if (( $(echo "$score < 0" | bc -l) )); then
        score="0.0"
    fi

    RESULTS[Score]=$score

    # Affichage des résultats
    echo ""
    echo -e "${CYAN}============================================${NC}"

    local score_color
    if (( $(echo "$score >= 8" | bc -l) )); then
        score_color="${GREEN}"
    elif (( $(echo "$score >= 6" | bc -l) )); then
        score_color="${YELLOW}"
    else
        score_color="${RED}"
    fi

    echo -e "  ${score_color}SCORE DE SANTE: ${score} / 10${NC}"
    echo -e "${CYAN}============================================${NC}"
    echo -e "  Total notes       : ${total_files}"

    local color
    color=$([ "$empty_count" -eq 0 ] && echo "$GREEN" || echo "$RED")
    echo -e "  Notes vides       : ${color}${empty_count}${NC}"

    color=$([ "$nofm_count" -eq 0 ] && echo "$GREEN" || echo "$YELLOW")
    echo -e "  Sans frontmatter  : ${color}${nofm_count}${NC}"

    color=$([ "$broken_count" -eq 0 ] && echo "$GREEN" || echo "$RED")
    echo -e "  Liens casses      : ${color}${broken_count}${NC}"

    color=$([ "$orphan_count" -eq 0 ] && echo "$GREEN" || echo "$YELLOW")
    echo -e "  Orphelines        : ${color}${orphan_count}${NC}"

    color=$([ "$status_count" -eq 0 ] && echo "$GREEN" || echo "$YELLOW")
    echo -e "  Status non-standard: ${color}${status_count}${NC}"

    color=$([ "$tag_count" -eq 0 ] && echo "$GREEN" || echo "$YELLOW")
    echo -e "  Tags incorrects   : ${color}${tag_count}${NC}"

    color=$([ "$related_count" -eq 0 ] && echo "$GREEN" || echo "$YELLOW")
    echo -e "  Related vides     : ${color}${related_count}${NC}"

    color=$([ "$dup_count" -eq 0 ] && echo "$GREEN" || echo "$YELLOW")
    echo -e "  Doublons basename : ${color}${dup_count}${NC}"

    echo -e "${CYAN}============================================${NC}"

    # Afficher quelques liens cassés si peu nombreux
    if (( broken_count > 0 && broken_count <= 10 )); then
        echo ""
        echo -e "${YELLOW}Liens casses:${NC}"
        while IFS='|' read -r src target; do
            local rel="${src#${VAULT_PATH}/}"
            echo -e "${GRAY}  ${rel} -> [[${target}]]${NC}"
        done < "$BROKEN_LINKS"
    fi

    # Nettoyer les fichiers temporaires
    rm -f "$note_names_file" "$linked_names_file"

    # Retourner les compteurs pour usage par d'autres fonctions
    echo "$empty_count|$nofm_count|$broken_count|$orphan_count|$status_count|$tag_count|$related_count|$dup_count|$score|$total_files"
}

invoke_autofix() {
    echo -e "${CYAN}=== VAULT GUARDIAN - AUTO-FIX ===${NC}"

    # Exécuter d'abord le health check
    local health_output
    health_output=$(invoke_health_check | tail -1)

    local fixed=0

    # Supprimer les fichiers vides
    local empty_count
    empty_count=$(wc -l < "$EMPTY_FILES" | tr -d ' ')
    if (( empty_count > 0 )); then
        echo ""
        echo -e "${YELLOW}Fixing: ${empty_count} empty files...${NC}"
        while IFS= read -r file; do
            [[ -z "$file" ]] && continue
            rm -f "$file"
            ((fixed++)) || true
        done < "$EMPTY_FILES"
        echo -e "${GREEN}  Deleted ${empty_count} empty files${NC}"
    fi

    # Corriger les status non-standard
    local status_count
    status_count=$(wc -l < "$STATUS_ISSUES" | tr -d ' ')
    if (( status_count > 0 )); then
        echo ""
        echo -e "${YELLOW}Fixing: ${status_count} non-standard status...${NC}"
        local status_fixed=0
        while IFS= read -r file; do
            [[ -z "$file" ]] && continue
            if sed -i 's/^status:[[:space:]]*captured[[:space:]]*$/status: seedling/' "$file" 2>/dev/null; then
                ((status_fixed++)) || true
            fi
        done < "$STATUS_ISSUES"
        echo -e "${GREEN}  Fixed ${status_fixed} status fields${NC}"
        ((fixed += status_fixed)) || true
    fi

    echo ""
    echo -e "${GREEN}Total fixes applied: ${fixed}${NC}"
}

invoke_quick_check() {
    echo -e "${CYAN}=== VAULT GUARDIAN - QUICK CHECK ===${NC}"

    if [[ ! -d "$VAULT_PATH" ]]; then
        echo -e "${RED}Vault path not found: ${VAULT_PATH}${NC}"
        exit 1
    fi

    local all_notes
    all_notes=$(get_all_notes)
    local total
    total=$(echo "$all_notes" | grep -c '.' || echo "0")
    local empty=0
    local broken=0

    # Index des noms de notes
    local note_names_file
    note_names_file=$(mktemp)
    while IFS= read -r file; do
        [[ -z "$file" ]] && continue
        basename "$file" .md >> "$note_names_file"
    done <<< "$all_notes"

    while IFS= read -r file; do
        [[ -z "$file" ]] && continue
        local content
        content=$(cat "$file" 2>/dev/null || echo "")

        if [[ -z "$content" ]] || [[ "$content" =~ ^[[:space:]]*$ ]]; then
            ((empty++)) || true
            continue
        fi

        # Compter les liens cassés
        local clean_content
        clean_content=$(remove_code_content "$content")
        while IFS= read -r target; do
            [[ -z "$target" ]] && continue
            if ! grep -qFx "$target" "$note_names_file"; then
                ((broken++)) || true
            fi
        done < <(echo "$clean_content" | grep -oP '\[\[([^\]|#]+)' | sed 's/\[\[//' || true)
    done <<< "$all_notes"

    rm -f "$note_names_file"

    local status
    if (( empty == 0 && broken == 0 )); then
        status="OK"
    else
        status="ISSUES"
    fi

    echo "  Notes: ${total} | Empty: ${empty} | Broken links: ${broken} | Status: ${status}"
}

invoke_report() {
    # Exécuter le health check et générer un rapport JSON
    local health_output
    health_output=$(invoke_health_check | tail -1)

    IFS='|' read -r empty_count nofm_count broken_count orphan_count status_count tag_count related_count dup_count score total_files <<< "$health_output"

    echo ""
    echo -e "${CYAN}=== RECOMMENDATIONS ===${NC}"

    if (( broken_count > 0 )); then
        echo "  - Corriger ${broken_count} liens casses"
    fi
    if (( nofm_count > 0 )); then
        echo "  - Ajouter frontmatter a ${nofm_count} fichiers"
    fi
    if (( orphan_count > 0 )); then
        echo "  - Connecter ${orphan_count} notes orphelines"
    fi
    if (( related_count > 0 )); then
        echo "  - Ajouter des related a ${related_count} notes"
    fi
    if (( dup_count > 0 )); then
        echo "  - Resoudre ${dup_count} doublons de basename"
    fi
    if (( $(echo "$score >= 9" | bc -l) )); then
        echo -e "  ${GREEN}Le vault est en excellent etat!${NC}"
    fi

    # Générer le rapport JSON
    mkdir -p "$DATA_DIR"
    local report_date
    report_date=$(date +%Y-%m-%d)
    local report_path="${DATA_DIR}/health-${report_date}.json"

    jq -n \
        --arg timestamp "${RESULTS[Timestamp]}" \
        --argjson score "$score" \
        --argjson totalFiles "$total_files" \
        --argjson emptyFiles "$empty_count" \
        --argjson noFrontmatter "$nofm_count" \
        --argjson brokenLinks "$broken_count" \
        --argjson orphans "$orphan_count" \
        --argjson statusIssues "$status_count" \
        --argjson tagIssues "$tag_count" \
        --argjson emptyRelated "$related_count" \
        --argjson duplicateBasenames "$dup_count" \
        '{
            Timestamp: $timestamp,
            Score: $score,
            TotalFiles: $totalFiles,
            EmptyFiles: $emptyFiles,
            NoFrontmatter: $noFrontmatter,
            BrokenLinks: $brokenLinks,
            Orphans: $orphans,
            StatusIssues: $statusIssues,
            TagIssues: $tagIssues,
            EmptyRelated: $emptyRelated,
            DuplicateBasenames: $duplicateBasenames
        }' > "$report_path"

    echo ""
    echo -e "${GREEN}  Rapport JSON sauvegarde: ${report_path}${NC}"
}

# Validation des arguments
case "$MODE" in
    health|fix|report|quick)
        ;;
    *)
        echo "Usage: $0 [health|fix|report|quick]"
        echo ""
        echo "Modes:"
        echo "  health  - Rapport de sante complet (defaut)"
        echo "  fix     - Auto-correction des problemes"
        echo "  report  - Health check + recommandations + JSON"
        echo "  quick   - Check rapide (~30s)"
        exit 1
        ;;
esac

check_dependencies

# Exécution selon le mode
case "$MODE" in
    health)
        # Exécuter health check, exclure la dernière ligne (données internes)
        output=$(invoke_health_check 2>&1)
        echo "$output" | head -n -1 || true
        ;;
    fix)
        invoke_autofix
        ;;
    report)
        invoke_report
        ;;
    quick)
        invoke_quick_check
        ;;
esac
