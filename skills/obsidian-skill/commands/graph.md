# Commande: /obs-graph

Analyse du graphe de liens du vault Obsidian.

## Syntaxe

```
/obs-graph [action] [options]
```

## Actions

### Statistiques du graphe

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
note_count=$(find "$VAULT" -name "*.md" -type f | wc -l)
link_count=0

declare -A backlink_map

while IFS= read -r note; do
    links=$(grep -oP '\[\[\K[^\]|]+' "$note" 2>/dev/null || true)
    count=$(echo "$links" | grep -c . || true)
    link_count=$((link_count + count))
    while IFS= read -r target; do
        [ -n "$target" ] && backlink_map["$target"]=$((${backlink_map["$target"]:-0} + 1))
    done <<< "$links"
done < <(find "$VAULT" -name "*.md" -type f)

density=$(awk "BEGIN {printf \"%.2f\", $link_count / ($note_count > 0 ? $note_count : 1)}")
echo "Notes: $note_count"
echo "Liens totaux: $link_count"
echo "Densite: $density liens/note"
```

### Hubs (notes les plus connectees)

```bash
# Top 10 notes avec le plus de backlinks
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

find "$VAULT" -name "*.md" -type f | xargs grep -hoP '\[\[\K[^\]|]+' 2>/dev/null | \
    sort | uniq -c | sort -rn | head -10 | \
    awk '{print $1" backlinks -> "$2}'
```

### Clusters (groupes de notes liees)

```bash
# Notes isolees (0 liens entrants ET 0 liens sortants)
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

# Recueillir toutes les cibles de liens
all_targets=$(find "$VAULT" -name "*.md" -type f | xargs grep -hoP '\[\[\K[^\]|]+' 2>/dev/null | sort -u)

isolated=0
while IFS= read -r note; do
    name=$(basename "$note" .md)
    has_outgoing=$(grep -cP '\[\[' "$note" 2>/dev/null || echo 0)
    has_incoming=$(echo "$all_targets" | grep -cF "$name" || echo 0)
    if [ "$has_outgoing" -eq 0 ] && [ "$has_incoming" -eq 0 ]; then
        isolated=$((isolated + 1))
    fi
done < <(find "$VAULT" -name "*.md" -type f)

echo "Notes isolees: $isolated"
```

## Options

| Option | Description |
|--------|-------------|
| `stats` | Statistiques globales du graphe |
| `hubs` | Top notes les plus connectees |
| `clusters` | Groupes de notes liees |
| `islands` | Notes completement isolees |

## Exemples

```bash
/obs-graph stats          # Vue d'ensemble du graphe
/obs-graph hubs           # Notes les plus liees
/obs-graph islands        # Notes isolees
```

## Voir Aussi

- `/obs-links` - Gestion des liens
- `/obs-orphans` - Notes orphelines
- `/obs-stats` - Statistiques generales
