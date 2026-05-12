# Commande: /obs-tags rename

Renommer un tag dans tout le vault (frontmatter et inline).

## Syntaxe

```
/obs-tags rename <old-tag> <new-tag> [options]
```

## Actions

### Renommer un tag

```bash
#!/usr/bin/env bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
old_tag="$1"
new_tag="$2"

modified=0

while IFS= read -r note; do
    content=$(< "$note" 2>/dev/null) || continue
    [ -z "$content" ] && continue
    new_content="$content"

    # Remplacer inline tags (#old -> #new)
    new_content=$(echo "$new_content" | sed -E "s/(^|[[:space:]])#${old_tag}([[:space:]]|$)/\1#${new_tag}\2/g")

    # Remplacer dans frontmatter tags array (  - old_tag)
    new_content=$(echo "$new_content" | sed -E "s/^([[:space:]]*-[[:space:]]+)${old_tag}[[:space:]]*$/\1${new_tag}/")

    if [ "$new_content" != "$content" ]; then
        printf '%s' "$new_content" > "$note"
        echo "Modifie: $(basename "$note")"
        modified=$((modified + 1))
    fi
done < <(find "$VAULT" -name "*.md" -type f)

echo ""
echo "$modified notes modifiees: #$old_tag -> #$new_tag"
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Afficher sans modifier |
| `--inline-only` | Tags inline uniquement |
| `--frontmatter-only` | Frontmatter uniquement |

## Exemples

```bash
/obs-tags rename dev/bash dev/shell         # Renommer un tag
/obs-tags rename Proxmox infra/proxmox      # Hierarchiser un tag
/obs-tags rename dev/python dev/py --dry-run # Preview
```

## Voir Aussi

- `/obs-tags merge` - Fusionner des tags
- `/obs-tags list` - Lister tous les tags
