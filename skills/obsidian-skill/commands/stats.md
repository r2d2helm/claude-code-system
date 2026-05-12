# Commande: /obs-stats

Statistiques détaillées du vault Obsidian.

## Syntaxe

```
/obs-stats [options]
```

## Comportement

Analyser le vault et afficher les statistiques complètes.

## Script bash

```bash
#!/usr/bin/env bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

total_words=0
total_links=0
all_tags=()
with_frontmatter=0

while IFS= read -r note; do
    content=$(< "$note" 2>/dev/null) || continue
    [ -z "$content" ] && continue

    words=$(echo "$content" | wc -w)
    total_words=$((total_words + words))

    links=$(grep -coP '\[\[[^\]]+\]\]' "$note" 2>/dev/null || echo 0)
    total_links=$((total_links + links))

    while IFS= read -r tag; do
        all_tags+=("$tag")
    done < <(grep -oP '#[\w/-]+' "$note" 2>/dev/null || true)

    echo "$content" | head -1 | grep -q '^---' && with_frontmatter=$((with_frontmatter + 1))
done < <(find "$VAULT" -name "*.md" -type f)

note_count=$(find "$VAULT" -name "*.md" -type f | wc -l)
att_count=$(find "$VAULT" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.pdf" -o -name "*.webp" -o -name "*.svg" \) | wc -l)
unique_tags=$(printf '%s\n' "${all_tags[@]}" | sort -u | wc -l)
note_size=$(find "$VAULT" -name "*.md" -type f | xargs du -cb 2>/dev/null | tail -1 | awk '{printf "%.1f", $1/1048576}')
att_size=$(find "$VAULT" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.pdf" -o -name "*.webp" \) | xargs du -cb 2>/dev/null | tail -1 | awk '{printf "%.1f", $1/1048576}')

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║        STATISTIQUES DU VAULT                 ║"
echo "╠══════════════════════════════════════════════╣"
echo "║                                              ║"
printf "║  Notes totales       : %6d          ║\n" "$note_count"
printf "║  Mots totaux         : %10d      ║\n" "$total_words"
printf "║  Liens internes      : %6d          ║\n" "$total_links"
printf "║  Tags uniques        : %6d          ║\n" "$unique_tags"
printf "║  Avec frontmatter    : %6d          ║\n" "$with_frontmatter"
printf "║  Attachments         : %6d          ║\n" "$att_count"
printf "║  Taille notes        : %6s MB       ║\n" "$note_size"
printf "║  Taille attachments  : %6s MB       ║\n" "$att_size"
echo "║                                              ║"

# Par type (base sur frontmatter)
echo "║  PAR TYPE:                                   ║"
find "$VAULT" -name "*.md" -type f | xargs grep -h '^type:' 2>/dev/null | \
    sed 's/type:[[:space:]]*//' | sort | uniq -c | sort -rn | head -8 | \
    while read -r count type; do
        printf "║    %-18s : %4d           ║\n" "$type" "$count"
    done

echo "║                                              ║"

# Par dossier (top 10)
echo "║  PAR DOSSIER (top 10):                       ║"
find "$VAULT" -name "*.md" -type f | xargs -I{} dirname {} | sort | uniq -c | sort -rn | head -10 | \
    while read -r count folder; do
        fname=$(basename "$folder")
        printf "║    %-18s : %4d           ║\n" "$fname" "$count"
    done

echo "║                                              ║"
echo "╚══════════════════════════════════════════════╝"
```

## Exemples

```bash
# Afficher les statistiques completes du vault par defaut
/obs-stats

# Exporter les statistiques en JSON pour traitement automatise
/obs-stats --json

# Statistiques d'un vault alternatif
/obs-stats --vault=~/Documents/SecondVault

# Combiner avec jq pour extraire le nombre total de notes
/obs-stats --json | jq '.total_notes'
```

## Options

| Option | Description |
|--------|-------------|
| `--json` | Sortie JSON |
| `--vault=path` | Vault alternatif |
