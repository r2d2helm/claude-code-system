# Commande: /obs-duplicates

Detecter les notes avec contenu similaire ou identique.

## Syntaxe

```
/obs-duplicates [options]
```

## Actions

### Detecter les doublons exacts (hash)

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

declare -A hashes
while IFS= read -r note; do
    # Exclure templates et .obsidian
    if echo "$note" | grep -qE '_Templates|\.obsidian'; then continue; fi
    hash=$(md5sum "$note" | awk '{print $1}')
    if [ -n "${hashes[$hash]}" ]; then
        echo "DOUBLON EXACT:"
        echo "  - ${hashes[$hash]}"
        echo "  - $note"
    else
        hashes[$hash]="$note"
    fi
done < <(find "$VAULT" -name "*.md" -type f)
```

### Detecter les titres similaires

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

# Extraire les noms de base, normaliser et comparer
find "$VAULT" -name "*.md" -type f | xargs -I{} basename {} .md | sort > /tmp/note_names.txt

# Trouver les noms identiques apres normalisation (minuscules, sans tirets/underscores)
while IFS= read -r name1; do
    norm1=$(echo "$name1" | tr '[:upper:]' '[:lower:]' | tr '_-' ' ')
    while IFS= read -r name2; do
        [ "$name1" = "$name2" ] && continue
        norm2=$(echo "$name2" | tr '[:upper:]' '[:lower:]' | tr '_-' ' ')
        if [ "$norm1" = "$norm2" ] || \
           echo "$norm1" | grep -qF "$norm2" || \
           echo "$norm2" | grep -qF "$norm1"; then
            echo "TITRE SIMILAIRE: $name1 <-> $name2"
        fi
    done < /tmp/note_names.txt
done < /tmp/note_names.txt | sort -u
```

## Options

| Option | Description |
|--------|-------------|
| `--exact` | Doublons exacts uniquement (hash) |
| `--title` | Titres similaires |
| `--tags` | Notes avec memes tags |
| `--merge` | Proposer de fusionner |

## Exemples

```bash
/obs-duplicates                # Detection complete
/obs-duplicates --exact        # Hash uniquement
/obs-duplicates --title        # Titres similaires
```

## Voir Aussi

- `/obs-clean` - Nettoyage general
- `/obs-empty` - Notes vides
