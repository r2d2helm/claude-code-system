# Commande: /obs-health

Diagnostic complet de la santé du vault Obsidian.

## Syntaxe

```
/obs-health [options]
```

## Modes

### /obs-health (complet)

Analyse complète du vault :

```
╔══════════════════════════════════════════════════════════════╗
║                    SANTE DU VAULT                            ║
║                    Knowledge                                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Chemin: ~/Documents/Knowledge                               ║
║  Analyse: 2026-02-04 14:30:22                                ║
║                                                              ║
║  SCORE GLOBAL: 78/100                                        ║
║  ████████████████████████████████████░░░░░░░░░░              ║
║                                                              ║
║  STATISTIQUES:                                               ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Notes totales       : 456                               │ ║
║  │ Mots totaux         : 125,430                           │ ║
║  │ Liens internes      : 1,234                             │ ║
║  │ Tags uniques        : 89                                │ ║
║  │ Attachments         : 156 (234 MB)                      │ ║
║  │ Taille vault        : 289 MB                            │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  PROBLEMES DETECTES:                                         ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Liens casses             : 3      (-5 pts)              │ ║
║  │ Notes orphelines         : 12     (-8 pts)              │ ║
║  │ Tags incoherents         : 5      (-4 pts)              │ ║
║  │ Doublons                 : 0      (OK)                  │ ║
║  │ Frontmatter manquant     : 23     (-5 pts)              │ ║
║  │ Attachments orphelins    : 8      (info)                │ ║
║  │ Notes vides              : 0      (OK)                  │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  RECOMMANDATIONS PRIORITAIRES:                               ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 1. [URGENT] Reparer 3 liens casses                      │ ║
║  │    -> /obs-links fix                                    │ ║
║  │                                                         │ ║
║  │ 2. [IMPORTANT] Connecter 12 notes orphelines            │ ║
║  │    -> /obs-links suggest                                │ ║
║  │                                                         │ ║
║  │ 3. [SUGGERE] Normaliser 5 tags similaires               │ ║
║  │    -> /obs-tags merge                                   │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-health --quick

Check rapide :

```
╔══════════════════════════════════════════════════════════════╗
║  QUICK HEALTH CHECK                                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Score: 78/100  ████████████████░░░░                         ║
║                                                              ║
║  3 liens casses                                              ║
║  12 notes orphelines                                         ║
║  Pas de doublons                                             ║
║                                                              ║
║  -> /obs-health pour details complets                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-health --report

Génère un rapport Markdown détaillé :

```bash
/obs-health --report --output="Health-Report-2026-02-04.md"
```

## Script bash

```bash
#!/usr/bin/env bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
score=100
issues=()

start_time=$(date +%s)
echo ""
echo "Analyse du vault: $VAULT"
echo ""

# === STATISTIQUES DE BASE ===
mapfile -t notes < <(find "$VAULT" -name "*.md" -type f 2>/dev/null)
mapfile -t attachments < <(find "$VAULT" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.pdf" -o -name "*.webp" \) 2>/dev/null)

total_notes=${#notes[@]}
total_attachments=${#attachments[@]}
total_words=0
total_links=0
all_tags=()
declare -A all_backlinks
declare -A all_outlinks

# === ANALYSE DES NOTES ===
mapfile -t note_names < <(printf '%s\n' "${notes[@]}" | xargs -I{} basename {} .md)

for note in "${notes[@]}"; do
    content=$(< "$note" 2>/dev/null) || continue
    [ -z "$content" ] && continue

    # Compter mots
    words=$(echo "$content" | wc -w)
    total_words=$((total_words + words))

    # Extraire liens
    while IFS= read -r target; do
        [ -z "$target" ] && continue
        total_links=$((total_links + 1))
        echo "$target" | grep -qE '^https?://' && continue

        # Verifier lien casse
        found=false
        for n in "${note_names[@]}"; do
            [ "$n" = "$target" ] && found=true && break
        done
        [ "$found" = false ] && issues+=("LIEN_CASSE:$(basename "$note"):$target")
        all_backlinks["$target"]+=" $(basename "$note" .md)"
    done < <(grep -oP '\[\[\K[^\]|#]+' "$note" 2>/dev/null || true)

    # Extraire tags
    while IFS= read -r tag; do
        all_tags+=("$tag")
    done < <(grep -oP '#[\w/-]+' "$note" 2>/dev/null || true)
done

# Compter liens casses
broken_count=$(printf '%s\n' "${issues[@]}" | grep -c '^LIEN_CASSE:' || true)
if [ "$broken_count" -gt 0 ]; then
    penalty=$((broken_count * 5 > 20 ? 20 : broken_count * 5))
    score=$((score - penalty))
    echo "  Liens casses: $broken_count (-$penalty pts)"
fi

# Notes orphelines
orphan_count=0
for note in "${notes[@]}"; do
    name=$(basename "$note" .md)
    echo "$note" | grep -qE '_Templates|_Index|_Attachments|\.obsidian' && continue
    echo "$name" | grep -qE '^(README|INDEX)' && continue
    has_backlinks=false
    [ -n "${all_backlinks[$name]:-}" ] && has_backlinks=true
    has_outlinks=$(grep -cP '\[\[' "$note" 2>/dev/null || echo 0)
    [ "$has_backlinks" = false ] && [ "$has_outlinks" -eq 0 ] && orphan_count=$((orphan_count + 1))
done
if [ "$orphan_count" -gt 0 ]; then
    penalty=$((orphan_count > 15 ? 15 : orphan_count))
    score=$((score - penalty))
    echo "  Notes orphelines: $orphan_count (-$penalty pts)"
fi

# Tags similaires
unique_tags=$(printf '%s\n' "${all_tags[@]}" | sort -u)
similar_tag_count=$(printf '%s\n' "${all_tags[@]}" | \
    tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g' | \
    sort | uniq -d | wc -l)
if [ "$similar_tag_count" -gt 0 ]; then
    penalty=$((similar_tag_count > 10 ? 10 : similar_tag_count))
    score=$((score - penalty))
    echo "  Tags incoherents: $similar_tag_count (-$penalty pts)"
fi

# Frontmatter manquant
no_fm=$(for note in "${notes[@]}"; do
    head -1 "$note" 2>/dev/null | grep -qv '^---' && echo "$note"
done | wc -l)
threshold=$(( total_notes / 10 ))
if [ "$no_fm" -gt "$threshold" ]; then
    penalty=$(( no_fm / 5 > 10 ? 10 : no_fm / 5 ))
    score=$((score - penalty))
    echo "  Frontmatter manquant: $no_fm (-$penalty pts)"
fi

# Notes vides
empty_count=$(for note in "${notes[@]}"; do
    content=$(< "$note" 2>/dev/null)
    body=$(echo "$content" | sed '/^---$/,/^---$/d')
    [ ${#body} -lt 10 ] && echo "$note"
done | wc -l)
if [ "$empty_count" -gt 0 ]; then
    penalty=$((empty_count * 2 > 10 ? 10 : empty_count * 2))
    score=$((score - penalty))
    echo "  Notes vides: $empty_count (-$penalty pts)"
fi

[ "$score" -lt 0 ] && score=0

# Affichage score
echo ""
echo "  SCORE GLOBAL: $score/100"
bar_len=$((score * 40 / 100))
bar=$(printf '%0.s█' $(seq 1 $bar_len))
empty_bar=$(printf '%0.s░' $(seq 1 $((40 - bar_len))))
echo "  ${bar}${empty_bar}"

end_time=$(date +%s)
elapsed=$((end_time - start_time))
echo ""
echo "  Analyse terminee en ${elapsed}s"
```

## Options

| Option | Description |
|--------|-------------|
| `--quick` | Analyse rapide (stats de base) |
| `--report` | Générer rapport Markdown |
| `--output=file` | Fichier de sortie pour rapport |
| `--json` | Sortie JSON |
| `--fix` | Proposer corrections automatiques |

## Exemples

```bash
# Analyse complète
/obs-health

# Check rapide
/obs-health --quick

# Générer rapport
/obs-health --report --output="vault-health.md"

# Analyse d'un vault spécifique
/obs-health --vault="$HOME/MonVault"
```
