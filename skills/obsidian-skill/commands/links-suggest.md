# Commande: /obs-links suggest

Suggerer des connexions entre notes basees sur les tags et mots-cles communs.

## Syntaxe

```
/obs-links suggest [note] [options]
```

## Actions

### Suggerer des liens pour une note

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
target_note="$1"  # Nom de la note cible

# Trouver la note cible
target_file=$(find "$VAULT" -name "${target_note}.md" -type f | head -1)
[ -z "$target_file" ] && echo "Note '$target_note' non trouvee" && exit 1

# Extraire tags de la cible
target_tags=$(grep -oP '(?<=\s|^)#[\w/-]+' "$target_file" 2>/dev/null | sort -u)

# Chercher notes avec tags communs
find "$VAULT" -name "*.md" -type f | grep -v "$(basename "$target_file")" | while IFS= read -r note; do
    note_tags=$(grep -oP '(?<=\s|^)#[\w/-]+' "$note" 2>/dev/null | sort -u)
    common=$(comm -12 <(echo "$target_tags") <(echo "$note_tags") | wc -l)
    if [ "$common" -gt 0 ]; then
        shared=$(comm -12 <(echo "$target_tags") <(echo "$note_tags") | tr '\n' ',' | sed 's/,$//')
        printf "%d\t%s\t%s\n" "$common" "$(basename "$note" .md)" "$shared"
    fi
done | sort -rn | head -10 | \
    awk '{printf "%-40s  Tags communs: %d  (%s)\n", $2, $1, $3}'
```

### Suggerer pour tout le vault

```bash
# Trouver les paires de notes les plus similaires (par tags)
# sans lien existant entre elles
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
echo "Analyse des connexions manquantes dans le vault..."
# Implementation: comparer chaque paire de notes
```

## Options

| Option | Description |
|--------|-------------|
| `--by-tags` | Similarite par tags (defaut) |
| `--by-title` | Similarite par mots du titre |
| `--limit N` | Limiter a N suggestions |

## Exemples

```bash
/obs-links suggest C_Docker          # Suggestions pour la note C_Docker
/obs-links suggest --by-tags         # Suggestions pour tout le vault
```

## Voir Aussi

- `/obs-links unlinked` - Notes non liees
- `/obs-links fix` - Reparer liens casses
- `/obs-graph` - Analyse du graphe
