# Commande: /obs-export

Exporter des notes ou le vault entier dans differents formats.

## Syntaxe

```
/obs-export [format] [source] [options]
```

## Actions

### Export JSON

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
output="vault-export.json"

echo "[" > "$output"
first=true
find "$VAULT" -name "*.md" -type f | grep -vE '_Templates|\.obsidian|\.git' | while IFS= read -r note; do
    name=$(basename "$note" .md)
    rel_path="${note#$VAULT/}"
    size=$(stat -c %s "$note")
    modified=$(date -r "$note" '+%Y-%m-%d')

    [ "$first" = true ] && first=false || echo "," >> "$output"
    printf '  {"name":"%s","path":"%s","size":%d,"modified":"%s"}' \
        "$name" "$rel_path" "$size" "$modified" >> "$output"
done
echo "]" >> "$output"

count=$(grep -c '"name"' "$output")
echo "Exporte: $count notes -> $output"
```

### Export CSV (metadonnees)

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
output="vault-export.csv"

echo "name,path,size,modified" > "$output"
find "$VAULT" -name "*.md" -type f | grep -vE '_Templates|\.obsidian|\.git' | while IFS= read -r note; do
    name=$(basename "$note" .md)
    rel_path="${note#$VAULT/}"
    size=$(stat -c %s "$note")
    modified=$(date -r "$note" '+%Y-%m-%d')
    echo "\"$name\",\"$rel_path\",$size,$modified"
done >> "$output"
```

### Export HTML

```bash
# Convertir une note Markdown en HTML
# Necessite pandoc : sudo apt install pandoc
note="note.md"
pandoc "$note" -o "${note%.md}.html"
```

## Options

| Option | Description |
|--------|-------------|
| `json` | Export JSON (metadonnees + contenu) |
| `csv` | Export CSV (metadonnees uniquement) |
| `html` | Export HTML |
| `--output` | Chemin du fichier de sortie |
| `--folder` | Exporter un dossier specifique |

## Exemples

```bash
/obs-export json                         # Export complet JSON
/obs-export csv --folder Concepts        # CSV des concepts
/obs-export html C_Docker                # Note en HTML
```

## Voir Aussi

- `/obs-sync` - Synchroniser le vault
- `/obs-backup` - Sauvegarder le vault
