# Commande: /obs-links unlinked

Trouver les notes sans aucun lien entrant ou sortant.

## Syntaxe

```
/obs-links unlinked [options]
```

## Actions

### Trouver notes non liees

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

# Collecter tous les liens sortants de toutes les notes
all_links=$(find "$VAULT" -name "*.md" -type f | grep -vE '_Templates|\.obsidian' | \
    xargs grep -hoP '\[\[\K[^\]|]+' 2>/dev/null | sort -u)

# Notes sans backlinks (personne ne pointe vers elles)
echo "=== Sans backlinks ==="
find "$VAULT" -name "*.md" -type f | grep -vE '_Templates|\.obsidian' | while IFS= read -r note; do
    name=$(basename "$note" .md)
    if ! echo "$all_links" | grep -qxF "$name"; then
        echo "  - $(basename "$note")"
    fi
done

# Notes sans liens sortants
echo ""
echo "=== Sans liens sortants ==="
find "$VAULT" -name "*.md" -type f | grep -vE '_Templates|\.obsidian' | while IFS= read -r note; do
    if ! grep -qP '\[\[' "$note" 2>/dev/null; then
        echo "  - $(basename "$note")"
    fi
done
```

## Options

| Option | Description |
|--------|-------------|
| `--no-incoming` | Notes sans backlinks uniquement |
| `--no-outgoing` | Notes sans liens sortants uniquement |
| `--exclude` | Exclure dossiers (ex: _Daily) |

## Exemples

```bash
/obs-links unlinked                      # Toutes les notes non liees
/obs-links unlinked --no-incoming        # Sans backlinks
/obs-links unlinked --exclude _Daily     # Exclure les daily notes
```

## Voir Aussi

- `/obs-links suggest` - Suggerer des connexions
- `/obs-orphans` - Notes orphelines
- `/obs-graph` - Analyse du graphe
