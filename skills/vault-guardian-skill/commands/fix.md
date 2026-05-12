# /guardian-fix

Auto-correction des problemes courants detectes dans le vault.

## Usage

```
/guardian-fix
/guardian-fix --dry-run
```

## Securite

- Ne supprime JAMAIS de notes avec du contenu
- Log toutes les modifications dans `~/.claude/hooks/logs/guardian-fix.log`
- Mode `--dry-run` pour previsualiser les corrections sans les appliquer
- Backup du frontmatter avant modification

## Script

```bash
#!/usr/bin/env bash
set -euo pipefail

VAULT="${VAULT_PATH:-$HOME/Documents/Knowledge}"
LOG_FILE="$HOME/.claude/hooks/logs/guardian-fix.log"
DRY_RUN=false
TODAY=$(date '+%Y-%m-%d')

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
  esac
done

if [ ! -d "$VAULT" ]; then
  echo "ERREUR: Vault introuvable: $VAULT"
  exit 1
fi

mkdir -p "$(dirname "$LOG_FILE")"

log() {
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
  echo "$msg" >> "$LOG_FILE"
  echo "  $1"
}

echo "=== VAULT GUARDIAN - AUTO-FIX ==="
echo "Vault: $VAULT"
echo "Date:  $TODAY"
echo "Mode:  $([ "$DRY_RUN" = true ] && echo 'DRY-RUN (simulation)' || echo 'LIVE')"
echo ""
log "--- Debut session fix $([ "$DRY_RUN" = true ] && echo '[DRY-RUN]') ---"

# Compteurs avant/apres
fixed_frontmatter=0
fixed_empty=0
fixed_tags=0
fixed_status=0
total_fixes=0

mapfile -t all_notes < <(find "$VAULT" -name '*.md' -not -path '*/.git/*' -not -path '*/.obsidian/*' -not -path '*/.trash/*' -not -path '*/_Templates/*')
total_notes=${#all_notes[@]}

echo "Notes a analyser: $total_notes"
echo ""

# --- 1. Suppression des notes vides ---
echo "--- Nettoyage notes vides ---"
for note in "${all_notes[@]}"; do
  content=$(cat "$note" 2>/dev/null || echo "")
  # Retirer le frontmatter pour evaluer le contenu
  body=$(echo "$content" | sed '/^---$/,/^---$/d')
  body_stripped=$(echo "$body" | tr -d '[:space:]')

  if [ ${#body_stripped} -lt 5 ]; then
    # Verifier qu'il n'y a pas non plus de frontmatter significatif
    fm_lines=$(echo "$content" | sed -n '/^---$/,/^---$/p' | wc -l)
    if [ "$fm_lines" -le 2 ] || [ ${#body_stripped} -eq 0 ]; then
      if [ "$DRY_RUN" = true ]; then
        log "SUPPRESSION (dry-run): $(basename "$note")"
      else
        rm "$note"
        log "SUPPRIME: $(basename "$note")"
      fi
      fixed_empty=$((fixed_empty + 1))
    fi
  fi
done
echo ""

# --- 2. Ajout frontmatter manquant ---
echo "--- Correction frontmatter manquant ---"
for note in "${all_notes[@]}"; do
  [ ! -f "$note" ] && continue  # peut avoir ete supprime
  content=$(cat "$note" 2>/dev/null || echo "")
  basename_note=$(basename "$note" .md)

  # Verifier si frontmatter existe
  has_frontmatter=false
  if echo "$content" | head -1 | grep -q '^---$'; then
    fm_end=$(echo "$content" | tail -n +2 | grep -n '^---$' | head -1 | cut -d: -f1)
    [ -n "$fm_end" ] && has_frontmatter=true
  fi

  if [ "$has_frontmatter" = false ]; then
    # Inferer le type depuis le nom de fichier
    note_type="concept"
    if [[ "$basename_note" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
      note_type="daily"
    elif [[ "$basename_note" =~ _Conv_ ]]; then
      note_type="conversation"
    elif [[ "$basename_note" =~ _Fix_ ]]; then
      note_type="troubleshooting"
    elif [[ "$basename_note" =~ ^C_ ]]; then
      note_type="concept"
    elif [[ "$basename_note" =~ ^SOP_ ]]; then
      note_type="reference"
    fi

    # Inferer tags depuis le chemin
    rel_path=$(realpath --relative-to="$VAULT" "$note" 2>/dev/null || echo "")
    tag_domain=""
    case "$rel_path" in
      Concepts/*) tag_domain="concept" ;;
      Conversations/*) tag_domain="conversation" ;;
      References/*) tag_domain="reference" ;;
      Projets/*) tag_domain="projet" ;;
      Formations/*) tag_domain="formation" ;;
      _Daily/*) tag_domain="daily" ;;
    esac

    # Generer titre propre
    title=$(echo "$basename_note" | sed 's/^C_//;s/^[0-9-]*_Conv_//;s/^[0-9-]*_Fix_//;s/-/ /g;s/_/ /g')

    frontmatter="---
title: \"$title\"
date: $TODAY
type: $note_type
status: seedling
tags:
  - $tag_domain
---
"
    if [ "$DRY_RUN" = true ]; then
      log "FRONTMATTER (dry-run): $basename_note -> type=$note_type"
    else
      # Prepend frontmatter
      tmp_file=$(mktemp)
      echo "$frontmatter" > "$tmp_file"
      cat "$note" >> "$tmp_file"
      mv "$tmp_file" "$note"
      log "FRONTMATTER: $basename_note -> type=$note_type, tag=$tag_domain"
    fi
    fixed_frontmatter=$((fixed_frontmatter + 1))
  fi
done
echo ""

# --- 3. Normalisation tags (majuscules -> minuscules) ---
echo "--- Normalisation tags ---"
for note in "${all_notes[@]}"; do
  [ ! -f "$note" ] && continue
  content=$(cat "$note" 2>/dev/null || echo "")

  # Chercher tags avec majuscules dans le frontmatter
  if echo "$content" | sed -n '/^tags:/,/^[a-z]/p' | grep -qP '^\s*-\s+.*[A-Z]'; then
    if [ "$DRY_RUN" = true ]; then
      log "TAGS (dry-run): $(basename "$note") -> lowercase"
    else
      # Convertir les tags en minuscules dans la section tags du frontmatter
      sed -i '/^tags:/,/^[a-z]/{/^\s*-/{s/\(- \)\(.*\)/\1\L\2/}}' "$note"
      log "TAGS: $(basename "$note") -> lowercase"
    fi
    fixed_tags=$((fixed_tags + 1))
  fi
done
echo ""

# --- 4. Normalisation status (captured -> seedling) ---
echo "--- Normalisation status ---"
for note in "${all_notes[@]}"; do
  [ ! -f "$note" ] && continue

  if grep -q '^status:\s*captured' "$note" 2>/dev/null; then
    if [ "$DRY_RUN" = true ]; then
      log "STATUS (dry-run): $(basename "$note") captured -> seedling"
    else
      sed -i 's/^status:\s*captured/status: seedling/' "$note"
      log "STATUS: $(basename "$note") captured -> seedling"
    fi
    fixed_status=$((fixed_status + 1))
  fi
done
echo ""

# --- Resume ---
total_fixes=$((fixed_empty + fixed_frontmatter + fixed_tags + fixed_status))

echo "=== RESUME DES CORRECTIONS ==="
echo "  Notes vides supprimees:    $fixed_empty"
echo "  Frontmatter ajoute:        $fixed_frontmatter"
echo "  Tags normalises:           $fixed_tags"
echo "  Status corriges:           $fixed_status"
echo "  -------------------------"
echo "  Total corrections:         $total_fixes"
echo ""

if [ "$DRY_RUN" = true ]; then
  echo "Mode DRY-RUN : aucune modification appliquee."
  echo "Relancer sans --dry-run pour appliquer."
else
  echo "Corrections appliquees. Log: $LOG_FILE"
fi

log "--- Fin session fix: $total_fixes corrections ---"
echo ""
echo "=== FIN AUTO-FIX ==="
```

## Corrections effectuees

| Correction | Description | Risque |
|------------|-------------|--------|
| Notes vides | Supprime les notes sans contenu (< 5 chars hors frontmatter) | Faible |
| Frontmatter | Ajoute YAML avec type/tags inferes depuis nom et chemin | Aucun |
| Tags | Convertit en minuscules dans le frontmatter | Aucun |
| Status | Remplace `captured` par `seedling` | Aucun |

## Recommandation

Toujours lancer avec `--dry-run` d'abord pour previsualiser les corrections.
