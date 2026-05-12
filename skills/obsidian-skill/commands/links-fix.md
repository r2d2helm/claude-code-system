# Commande: /obs-links fix

Reparer les liens casses du vault (cibles renommees, supprimees, typos).

## Syntaxe

```
/obs-links fix [options]
```

## Actions

### Detecter et reparer

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

# Construire la liste des noms de notes existants
mapfile -t note_names < <(find "$VAULT" -name "*.md" -type f | xargs -I{} basename {} .md)

find "$VAULT" -name "*.md" -type f | while IFS= read -r note; do
    content=$(< "$note")
    [ -z "$content" ] && continue

    # Extraire les wikilinks
    while IFS= read -r target; do
        [ -z "$target" ] && continue
        # Verifier si la note existe
        found=false
        for n in "${note_names[@]}"; do
            [ "$n" = "$target" ] && found=true && break
        done

        if [ "$found" = false ]; then
            # Chercher correspondance approximative
            suggestion=$(printf '%s\n' "${note_names[@]}" | grep -iF "$target" | head -1 || true)
            [ -z "$suggestion" ] && suggestion="(aucune)"
            printf "Source: %s\nLien casse: %s\nSuggestion: %s\n---\n" \
                "$(basename "$note")" "$target" "$suggestion"
        fi
    done < <(grep -oP '\[\[\K[^\]|#]+' "$note" 2>/dev/null || true)
done
```

### Appliquer les corrections

```bash
# Mode interactif : proposer chaque fix
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

# Remplacer un lien casse dans un fichier
old_link="AncienNom"
new_link="NouveauNom"
file="$VAULT/path/to/note.md"

sed -i "s/\[\[$old_link\]\]/[[$new_link]]/g" "$file"
sed -i "s/\[\[$old_link|/[[$new_link|/g" "$file"
echo "Lien remplace: [[$old_link]] -> [[$new_link]]"
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Afficher sans corriger |
| `--auto` | Corriger automatiquement les correspondances exactes |
| `--remove` | Supprimer les liens sans correspondance |
| `--create` | Creer les notes manquantes |

## Exemples

```bash
/obs-links fix                # Detecter et proposer corrections
/obs-links fix --dry-run      # Preview des corrections
/obs-links fix --auto         # Appliquer les correspondances evidentes
/obs-links fix --create       # Creer les notes manquantes
```

## Voir Aussi

- `/obs-links broken` - Lister les liens casses
- `/obs-links suggest` - Suggerer connexions
- `/obs-health` - Diagnostic complet
