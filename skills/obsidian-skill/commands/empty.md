# Commande: /obs-empty

Trouver et supprimer les notes vides ou quasi-vides.

## Syntaxe

```
/obs-empty [options]
```

## Actions

### Trouver les notes vides

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
MIN_CHARS=50

find "$VAULT" -name "*.md" -type f | grep -vE '_Templates|\.obsidian' | while IFS= read -r note; do
    name=$(basename "$note")
    content=$(< "$note")

    if [ -z "$content" ]; then
        echo "VIDE          0 chars   $name"
        continue
    fi

    # Retirer le frontmatter pour mesurer le contenu reel
    body=$(echo "$content" | sed '/^---$/,/^---$/d' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

    body_len=${#body}
    if [ "$body_len" -eq 0 ]; then
        echo "FRONTMATTER   ${#content} chars   $name"
    elif [ "$body_len" -lt "$MIN_CHARS" ]; then
        echo "QUASI-VIDE    $body_len chars   $name"
    fi
done | column -t
```

## Options

| Option | Description |
|--------|-------------|
| `--delete` | Supprimer les notes vides (avec confirmation) |
| `--min-chars N` | Seuil de contenu minimum (defaut: 50) |
| `--dry-run` | Preview sans action |

## Exemples

```bash
/obs-empty                    # Lister les notes vides
/obs-empty --min-chars 100    # Seuil plus large
/obs-empty --delete           # Supprimer apres confirmation
```

## Voir Aussi

- `/obs-clean` - Nettoyage general
- `/obs-duplicates` - Notes en double
