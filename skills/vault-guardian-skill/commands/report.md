# /guardian-report

Genere un rapport hebdomadaire de sante du vault avec metriques et recommandations.

## Usage

```
/guardian-report
```

## Contenu du rapport

1. Score de sante global
2. Activite de la semaine (notes ajoutees/modifiees)
3. Metriques detaillees (densite graphe, taux orphelins, couverture frontmatter)
4. Problemes detectes
5. Recommandations priorisees

## Script

```bash
#!/usr/bin/env bash
set -euo pipefail

VAULT="${VAULT_PATH:-$HOME/Documents/Knowledge}"
REPORT_DIR="$HOME/reports"
TODAY=$(date '+%Y-%m-%d')
WEEK_AGO=$(date -d '7 days ago' '+%Y-%m-%d')
REPORT_FILE="$REPORT_DIR/${TODAY}_vault-health-report.md"

if [ ! -d "$VAULT" ]; then
  echo "ERREUR: Vault introuvable: $VAULT"
  exit 1
fi

mkdir -p "$REPORT_DIR"

# --- Collecte des notes ---
mapfile -t all_notes < <(find "$VAULT" -name '*.md' -not -path '*/.git/*' -not -path '*/.obsidian/*' -not -path '*/.trash/*')
total_notes=${#all_notes[@]}

# Notes modifiees cette semaine
mapfile -t modified_notes < <(find "$VAULT" -name '*.md' -not -path '*/.git/*' -not -path '*/.obsidian/*' -not -path '*/.trash/*' -mtime -7)
modified_count=${#modified_notes[@]}

# Notes creees cette semaine (approximation via ctime)
mapfile -t created_notes < <(find "$VAULT" -name '*.md' -not -path '*/.git/*' -not -path '*/.obsidian/*' -not -path '*/.trash/*' -ctime -7 -newer "$VAULT")
created_count=${#created_notes[@]}

# --- Analyse ---
notes_with_fm=0
notes_without_fm=0
empty_notes=0
orphan_notes=0
total_links=0
total_words=0

declare -A incoming_links
declare -A outgoing_count
declare -A note_names

for note in "${all_notes[@]}"; do
  bn=$(basename "$note" .md)
  note_names["$bn"]=1
done

for note in "${all_notes[@]}"; do
  content=$(cat "$note" 2>/dev/null || echo "")
  bn=$(basename "$note" .md)

  # Frontmatter
  if echo "$content" | head -1 | grep -q '^---$'; then
    fm_end=$(echo "$content" | tail -n +2 | grep -n '^---$' | head -1 | cut -d: -f1)
    [ -n "$fm_end" ] && notes_with_fm=$((notes_with_fm + 1)) || notes_without_fm=$((notes_without_fm + 1))
  else
    notes_without_fm=$((notes_without_fm + 1))
  fi

  # Contenu vide
  body=$(echo "$content" | sed '/^---$/,/^---$/d')
  body_stripped=$(echo "$body" | tr -d '[:space:]')
  [ ${#body_stripped} -lt 10 ] && empty_notes=$((empty_notes + 1))

  # Liens
  link_count=$(echo "$content" | grep -coP '\[\[' 2>/dev/null || echo 0)
  total_links=$((total_links + link_count))
  outgoing_count["$bn"]=$link_count

  # Liens entrants
  while IFS= read -r link; do
    [ -z "$link" ] && continue
    target=$(echo "$link" | sed 's/\[\[//;s/\]\]//;s/|.*//' | xargs)
    [ -n "${note_names[$target]+x}" ] && incoming_links["$target"]=$(( ${incoming_links[$target]:-0} + 1 ))
  done <<< "$(echo "$content" | grep -oP '\[\[[^\]]+\]\]' 2>/dev/null || true)"

  # Mots
  wc_w=$(echo "$body" | wc -w 2>/dev/null || echo 0)
  total_words=$((total_words + wc_w))
done

# Orphelins
for note in "${all_notes[@]}"; do
  bn=$(basename "$note" .md)
  in_c=${incoming_links[$bn]:-0}
  out_c=${outgoing_count[$bn]:-0}
  [ "$in_c" -eq 0 ] && [ "$out_c" -eq 0 ] && orphan_notes=$((orphan_notes + 1))
done

# --- Metriques calculees ---
fm_coverage=0
orphan_rate=0
graph_density=0
links_per_note=0

if [ "$total_notes" -gt 0 ]; then
  fm_coverage=$((notes_with_fm * 100 / total_notes))
  orphan_rate=$((orphan_notes * 100 / total_notes))
  links_per_note=$((total_links / total_notes))
  # Densite = liens / (notes * (notes-1)) * 100, simplifie
  if [ "$total_notes" -gt 1 ]; then
    max_links=$((total_notes * (total_notes - 1)))
    graph_density=$((total_links * 10000 / max_links))
  fi
fi

# --- Score de sante ---
score=100
fm_pct=$((notes_without_fm * 100 / (total_notes > 0 ? total_notes : 1)))
score=$((score - fm_pct * 30 / 100))
empty_pct=$((empty_notes * 100 / (total_notes > 0 ? total_notes : 1)))
score=$((score - empty_pct * 15 / 100))
score=$((score - orphan_rate * 20 / 100))
[ "$links_per_note" -ge 3 ] && score=$((score + 10))
[ "$score" -gt 100 ] && score=100
[ "$score" -lt 0 ] && score=0

# --- Generation rapport markdown ---
cat > "$REPORT_FILE" << REPORT
---
title: "Rapport Vault - $TODAY"
date: $TODAY
type: reference
status: evergreen
tags:
  - vault/maintenance
  - rapport
---

# Rapport de Sante du Vault - $TODAY

> **Score global : $score / 100**

## Activite de la semaine ($WEEK_AGO -> $TODAY)

- **Notes modifiees :** $modified_count
- **Notes creees (approx) :** $created_count

### Notes modifiees recemment

$(for note in "${modified_notes[@]:0:20}"; do
  echo "- \`$(basename "$note")\` ($(date -r "$note" '+%Y-%m-%d %H:%M'))"
done)
$([ "$modified_count" -gt 20 ] && echo "- ... et $((modified_count - 20)) autres")

## Metriques

| Metrique | Valeur |
|----------|--------|
| Notes totales | $total_notes |
| Mots totaux | $total_words |
| Liens totaux | $total_links |
| Liens/note (moy) | $links_per_note |
| Couverture frontmatter | ${fm_coverage}% |
| Taux orphelins | ${orphan_rate}% |
| Densite graphe | ${graph_density}bp (pour 10000) |

## Problemes detectes

| Probleme | Nombre | Severite |
|----------|--------|----------|
| Frontmatter manquant | $notes_without_fm | $([ "$notes_without_fm" -gt 10 ] && echo "Haute" || echo "Basse") |
| Notes vides | $empty_notes | $([ "$empty_notes" -gt 5 ] && echo "Moyenne" || echo "Basse") |
| Notes orphelines | $orphan_notes | $([ "$orphan_rate" -gt 30 ] && echo "Haute" || echo "Moyenne") |

## Recommandations

$(if [ "$notes_without_fm" -gt 0 ]; then echo "1. Lancer \`/guardian-fix\` pour ajouter le frontmatter manquant ($notes_without_fm notes)"; fi)
$(if [ "$empty_notes" -gt 0 ]; then echo "2. Supprimer ou completer les $empty_notes notes vides"; fi)
$(if [ "$orphan_rate" -gt 20 ]; then echo "3. Connecter les notes orphelines ($orphan_notes notes sans liens)"; fi)
$(if [ "$links_per_note" -lt 2 ]; then echo "4. Augmenter la connectivite (actuellement $links_per_note liens/note, viser 3+)"; fi)
$(if [ "$fm_coverage" -lt 90 ]; then echo "5. Atteindre 90%+ de couverture frontmatter (actuellement ${fm_coverage}%)"; fi)

## Actions suggerees

- \`/guardian-fix\` pour les corrections automatiques
- \`/guardian-health\` pour un diagnostic interactif
- Revue manuelle des orphelins pour identifier les notes a connecter ou supprimer
REPORT

echo "=== RAPPORT GENERE ==="
echo "Fichier: $REPORT_FILE"
echo ""
echo "Score:   $score / 100"
echo "Notes:   $total_notes (modifiees cette semaine: $modified_count)"
echo "Issues:  FM=$notes_without_fm  Vides=$empty_notes  Orphelins=$orphan_notes"
echo ""

# Copier dans le vault si le dossier existe
VAULT_REPORTS="$VAULT/References/SOPs"
if [ -d "$VAULT_REPORTS" ] || [ -d "$VAULT/References" ]; then
  mkdir -p "$VAULT_REPORTS"
  cp "$REPORT_FILE" "$VAULT_REPORTS/"
  echo "Copie dans le vault: $VAULT_REPORTS/$(basename "$REPORT_FILE")"
fi
```

## Rapport genere

Le rapport est sauvegarde dans `~/reports/` au format `YYYY-MM-DD_vault-health-report.md` avec frontmatter YAML pour indexation dans le vault. Une copie est placee dans `Knowledge/References/SOPs/` si le dossier existe.
