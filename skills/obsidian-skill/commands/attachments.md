# Commande: /obs-attachments

Gerer les pieces jointes du vault (images, PDF, fichiers).

## Syntaxe

```
/obs-attachments [action] [options]
```

## Actions

### Lister les attachments

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

# Trouver les attachments
find "$VAULT" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.webp" -o -name "*.pdf" -o -name "*.svg" \) \
    | grep -v '\.obsidian' > /tmp/attachments.txt

count=$(wc -l < /tmp/attachments.txt)
total_size=$(cat /tmp/attachments.txt | xargs du -cb 2>/dev/null | tail -1 | awk '{printf "%.1f", $1/1048576}')

echo "Total: $count fichiers ($total_size MB)"

# Par type
cat /tmp/attachments.txt | grep -oE '\.[^.]+$' | sort | uniq -c | sort -rn | \
    awk '{print "  "$2": "$1" fichiers"}'
```

### Trouver les attachments orphelins

```bash
# Fichiers non references dans aucune note
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
all_content=$(find "$VAULT" -name "*.md" -type f | xargs cat 2>/dev/null)

while IFS= read -r att; do
    name=$(basename "$att")
    if ! echo "$all_content" | grep -qF "$name"; then
        size=$(du -k "$att" | awk '{printf "%.1f", $1/1024}')
        echo "  - $name (${size} KB)"
    fi
done < /tmp/attachments.txt
```

### Nettoyer les orphelins

```bash
# Dry-run: afficher sans supprimer
while IFS= read -r att; do
    name=$(basename "$att")
    if ! echo "$all_content" | grep -qF "$name"; then
        echo "Supprime (dry-run): $name"
        # Retirer --dry-run pour supprimer : rm "$att"
    fi
done < /tmp/attachments.txt
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister tous les attachments |
| `orphans` | Trouver les non-references |
| `clean` | Supprimer les orphelins |
| `large` | Fichiers > 5 MB |
| `--dry-run` | Preview sans action |

## Exemples

```bash
/obs-attachments list              # Inventaire complet
/obs-attachments orphans           # Non-references
/obs-attachments clean --dry-run   # Preview nettoyage
/obs-attachments large             # Gros fichiers
```

## Voir Aussi

- `/obs-clean` - Nettoyage general
- `/obs-stats` - Statistiques du vault
