# Commande: /obs-tags unused

Lister les tags utilises une seule fois ou non utilises dans le vault.

## Syntaxe

```
/obs-tags unused [options]
```

## Actions

### Trouver tags rares

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
declare -A tag_counts

while IFS= read -r note; do
    content=$(< "$note" 2>/dev/null) || continue

    # Tags inline (#tag)
    while IFS= read -r tag; do
        [ -n "$tag" ] && tag_counts["$tag"]=$((${tag_counts["$tag"]:-0} + 1))
    done < <(grep -oP '(?<=\s|^)#\K[\w/-]+' "$note" 2>/dev/null || true)

    # Tags frontmatter (liste YAML)
    if grep -q '^---' "$note"; then
        while IFS= read -r tag; do
            tag=$(echo "$tag" | sed 's/^[[:space:]]*-[[:space:]]*//' | sed 's/[[:space:]]*$//')
            [[ "$tag" =~ ^[a-zA-Z0-9/_-]+$ ]] && \
                tag_counts["$tag"]=$((${tag_counts["$tag"]:-0} + 1))
        done < <(sed -n '/^---$/,/^---$/p' "$note" | grep -E '^[[:space:]]*-[[:space:]]')
    fi
done < <(find "$VAULT" -name "*.md" -type f)

# Tags utilises 1 seule fois
echo "Tags utilises 1 seule fois:"
for tag in $(printf '%s\n' "${!tag_counts[@]}" | sort); do
    [ "${tag_counts[$tag]}" -eq 1 ] && echo "  #$tag"
done
```

## Options

| Option | Description |
|--------|-------------|
| `--max N` | Tags utilises N fois ou moins (defaut: 1) |
| `--delete` | Supprimer les tags rares (avec confirmation) |

## Exemples

```bash
/obs-tags unused              # Tags utilises 1 fois
/obs-tags unused --max 2      # Tags utilises 2 fois ou moins
```

## Voir Aussi

- `/obs-tags list` - Lister tous les tags
- `/obs-tags rename` - Renommer un tag
- `/obs-tags merge` - Fusionner des tags
