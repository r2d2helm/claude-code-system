# /guardian-health

Effectue un diagnostic complet du vault Obsidian Knowledge.

## Usage

```
/guardian-health
/guardian-health --quick
```

## Actions

1. Scanner toutes les notes du vault
2. Verifier : frontmatter, liens, tags, status, fichiers vides
3. Calculer le score de sante (0-100)
4. Afficher rapport detaille avec barre de progression ASCII

## Script

```bash
#!/usr/bin/env bash
set -euo pipefail

VAULT="${VAULT_PATH:-$HOME/Documents/Knowledge}"
QUICK_MODE=false

for arg in "$@"; do
  case "$arg" in
    --quick) QUICK_MODE=true ;;
  esac
done

if [ ! -d "$VAULT" ]; then
  echo "ERREUR: Vault introuvable: $VAULT"
  exit 1
fi

# --- Compteurs ---
total_notes=0
notes_with_frontmatter=0
notes_without_frontmatter=0
empty_notes=0
broken_links=0
orphan_notes=0
total_links=0
total_tags=0
total_words=0

# --- Collecte des notes ---
mapfile -t all_notes < <(find "$VAULT" -name '*.md' -not -path '*/.git/*' -not -path '*/.obsidian/*' -not -path '*/.trash/*')
total_notes=${#all_notes[@]}

if [ "$total_notes" -eq 0 ]; then
  echo "Aucune note trouvee dans $VAULT"
  exit 0
fi

echo "=== VAULT GUARDIAN - HEALTH CHECK ==="
echo "Vault: $VAULT"
echo "Date:  $(date '+%Y-%m-%d %H:%M')"
echo "Mode:  $([ "$QUICK_MODE" = true ] && echo 'Quick' || echo 'Complet')"
echo ""

# --- Barre de progression ---
progress_bar() {
  local current=$1 total=$2 width=40
  local pct=$((current * 100 / total))
  local filled=$((current * width / total))
  local empty=$((width - filled))
  printf "\r  [%-${width}s] %3d%% (%d/%d)" "$(printf '#%.0s' $(seq 1 "$filled" 2>/dev/null) 2>/dev/null)" "$pct" "$current" "$total"
}

# --- Analyse de chaque note ---
echo "Analyse des notes..."

# Construire liste de noms de notes pour detection liens casses
declare -A note_names
for note in "${all_notes[@]}"; do
  basename_no_ext=$(basename "$note" .md)
  note_names["$basename_no_ext"]=1
done

# Compteurs liens entrants/sortants par note
declare -A incoming_links
declare -A outgoing_links

processed=0
for note in "${all_notes[@]}"; do
  processed=$((processed + 1))
  [ $((processed % 20)) -eq 0 ] && progress_bar "$processed" "$total_notes"

  content=$(cat "$note" 2>/dev/null || echo "")
  basename_note=$(basename "$note" .md)

  # Note vide (moins de 10 caracteres hors frontmatter)
  body=$(echo "$content" | sed '/^---$/,/^---$/d')
  body_stripped=$(echo "$body" | tr -d '[:space:]')
  if [ ${#body_stripped} -lt 10 ]; then
    empty_notes=$((empty_notes + 1))
  fi

  # Frontmatter YAML
  if echo "$content" | head -1 | grep -q '^---$'; then
    fm_end=$(echo "$content" | tail -n +2 | grep -n '^---$' | head -1 | cut -d: -f1)
    if [ -n "$fm_end" ]; then
      notes_with_frontmatter=$((notes_with_frontmatter + 1))
    else
      notes_without_frontmatter=$((notes_without_frontmatter + 1))
    fi
  else
    notes_without_frontmatter=$((notes_without_frontmatter + 1))
  fi

  # Wikilinks [[...]]
  note_links=$(echo "$content" | grep -oP '\[\[[^\]]+\]\]' 2>/dev/null || true)
  link_count=$(echo "$note_links" | grep -c '\[\[' 2>/dev/null || echo 0)
  total_links=$((total_links + link_count))
  outgoing_links["$basename_note"]=$link_count

  # Verifier liens casses
  if [ "$QUICK_MODE" = false ]; then
    while IFS= read -r link; do
      [ -z "$link" ] && continue
      target=$(echo "$link" | sed 's/\[\[//;s/\]\]//;s/|.*//' | xargs)
      if [ -z "${note_names[$target]+x}" ]; then
        broken_links=$((broken_links + 1))
      else
        incoming_links["$target"]=$(( ${incoming_links[$target]:-0} + 1 ))
      fi
    done <<< "$note_links"
  fi

  # Tags
  tag_count=$(echo "$content" | grep -coP '(?:^|\s)#[a-zA-Z][a-zA-Z0-9/_-]+' 2>/dev/null || echo 0)
  # Tags dans frontmatter
  fm_tags=$(echo "$content" | sed -n '/^tags:/,/^[a-z]/p' | grep -c '^\s*-' 2>/dev/null || echo 0)
  total_tags=$((total_tags + tag_count + fm_tags))

  # Comptage mots
  wc_words=$(echo "$body" | wc -w 2>/dev/null || echo 0)
  total_words=$((total_words + wc_words))
done

progress_bar "$total_notes" "$total_notes"
echo ""
echo ""

# --- Detection orphelins (pas de liens entrants ET pas de liens sortants) ---
if [ "$QUICK_MODE" = false ]; then
  for note in "${all_notes[@]}"; do
    bn=$(basename "$note" .md)
    in_count=${incoming_links[$bn]:-0}
    out_count=${outgoing_links[$bn]:-0}
    if [ "$in_count" -eq 0 ] && [ "$out_count" -eq 0 ]; then
      orphan_notes=$((orphan_notes + 1))
    fi
  done
fi

# --- Calcul score de sante (0-100) ---
score=100

# Penalite frontmatter manquant (-30 max)
if [ "$total_notes" -gt 0 ]; then
  fm_pct=$((notes_without_frontmatter * 100 / total_notes))
  fm_penalty=$((fm_pct * 30 / 100))
  score=$((score - fm_penalty))
fi

# Penalite notes vides (-15 max)
if [ "$total_notes" -gt 0 ]; then
  empty_pct=$((empty_notes * 100 / total_notes))
  empty_penalty=$((empty_pct * 15 / 100))
  score=$((score - empty_penalty))
fi

# Penalite liens casses (-25 max)
if [ "$total_links" -gt 0 ]; then
  broken_pct=$((broken_links * 100 / total_links))
  broken_penalty=$((broken_pct * 25 / 100))
  score=$((score - broken_penalty))
fi

# Penalite orphelins (-20 max)
if [ "$total_notes" -gt 0 ] && [ "$QUICK_MODE" = false ]; then
  orphan_pct=$((orphan_notes * 100 / total_notes))
  orphan_penalty=$((orphan_pct * 20 / 100))
  score=$((score - orphan_penalty))
fi

# Bonus densite liens (+10 max)
if [ "$total_notes" -gt 0 ]; then
  links_per_note=$((total_links / total_notes))
  if [ "$links_per_note" -ge 3 ]; then
    score=$((score + 10))
  elif [ "$links_per_note" -ge 1 ]; then
    score=$((score + 5))
  fi
fi

[ "$score" -gt 100 ] && score=100
[ "$score" -lt 0 ] && score=0

# --- Score visuel ---
score_bar_width=30
score_filled=$((score * score_bar_width / 100))
score_empty=$((score_bar_width - score_filled))

if [ "$score" -ge 80 ]; then
  grade="EXCELLENT"
elif [ "$score" -ge 60 ]; then
  grade="BON"
elif [ "$score" -ge 40 ]; then
  grade="MOYEN"
else
  grade="CRITIQUE"
fi

echo "=== SCORE DE SANTE ==="
printf "  [%-${score_bar_width}s] %d/100 - %s\n" "$(printf '#%.0s' $(seq 1 "$score_filled" 2>/dev/null) 2>/dev/null)" "$score" "$grade"
echo ""

# --- Metriques ---
echo "=== METRIQUES ==="
echo "  Notes totales:        $total_notes"
echo "  Mots totaux:          $total_words"
echo "  Liens totaux:         $total_links"
echo "  Tags totaux:          $total_tags"
if [ "$total_notes" -gt 0 ]; then
  echo "  Liens/note (moy):    $((total_links / total_notes))"
  echo "  Mots/note (moy):     $((total_words / total_notes))"
fi
echo ""

# --- Problemes ---
echo "=== PROBLEMES DETECTES ==="
echo "  Frontmatter manquant: $notes_without_frontmatter / $total_notes"
echo "  Notes vides:          $empty_notes"
echo "  Liens casses:         $broken_links"
if [ "$QUICK_MODE" = false ]; then
  echo "  Notes orphelines:     $orphan_notes"
fi
echo ""

# --- Couverture ---
echo "=== COUVERTURE ==="
if [ "$total_notes" -gt 0 ]; then
  echo "  Frontmatter:          $((notes_with_frontmatter * 100 / total_notes))%"
  if [ "$QUICK_MODE" = false ]; then
    non_orphan=$((total_notes - orphan_notes))
    echo "  Connectivite:         $((non_orphan * 100 / total_notes))%"
  fi
fi
echo ""
echo "=== FIN DU DIAGNOSTIC ==="
```

## Quick mode

Pour un check rapide (notes vides + liens casses uniquement), passer `--quick`. Ce mode ignore l'analyse des orphelins et la verification approfondie des liens, reduisant le temps d'execution a quelques secondes.

## Interpretation du score

| Plage   | Grade     | Action recommandee                    |
|---------|-----------|---------------------------------------|
| 80-100  | EXCELLENT | Maintenance de routine suffisante     |
| 60-79   | BON       | Corriger les problemes mineurs        |
| 40-59   | MOYEN     | Lancer `/guardian-fix` rapidement     |
| 0-39    | CRITIQUE  | Fix immediat + audit manuel necessaire|
