# Commande: /obs-tags merge

Fusionner deux tags en un seul dans tout le vault.

## Syntaxe

```
/obs-tags merge <tag1> <tag2> <target> [options]
```

## Actions

### Fusionner

```bash
#!/usr/bin/env bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
tag1="$1"
tag2="$2"
target="$3"

modified=0

while IFS= read -r note; do
    content=$(< "$note")
    [ -z "$content" ] && continue
    new_content="$content"

    # Remplacer les deux tags par le target (inline #tag)
    new_content=$(echo "$new_content" | sed -E "s/(^|[[:space:]])#${tag1}([[:space:]]|$)/\1#${target}\2/g")
    new_content=$(echo "$new_content" | sed -E "s/(^|[[:space:]])#${tag2}([[:space:]]|$)/\1#${target}\2/g")

    # Remplacer dans frontmatter (liste YAML "  - tag")
    new_content=$(echo "$new_content" | sed -E "s/^([[:space:]]*-[[:space:]]+)${tag1}[[:space:]]*$/\1${target}/")
    new_content=$(echo "$new_content" | sed -E "s/^([[:space:]]*-[[:space:]]+)${tag2}[[:space:]]*$/\1${target}/")

    if [ "$new_content" != "$content" ]; then
        printf '%s' "$new_content" > "$note"
        modified=$((modified + 1))
    fi
done < <(find "$VAULT" -name "*.md" -type f)

echo "$modified notes modifiees: #$tag1 + #$tag2 -> #$target"
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Afficher sans modifier |

## Exemples

```bash
/obs-tags merge proxmox pve infra/proxmox    # Fusionner variantes
/obs-tags merge ai/gpt ai/openai ai/llm      # Unifier sous un tag
```

## Voir Aussi

- `/obs-tags rename` - Renommer un tag
- `/obs-tags unused` - Tags rares
