# Commande: /obs-tags hierarchy

Afficher l'arbre hierarchique des tags du vault.

## Syntaxe

```
/obs-tags hierarchy [options]
```

## Actions

### Afficher l'arbre

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

declare -A tags

while IFS= read -r note; do
    while IFS= read -r tag; do
        [ -n "$tag" ] && tags["$tag"]=$((${tags["$tag"]:-0} + 1))
    done < <(grep -oP '(?<=\s|^)#\K[\w/-]+' "$note" 2>/dev/null || true)
done < <(find "$VAULT" -name "*.md" -type f)

# Afficher l'arbre par groupes de prefixes
echo "=== HIERARCHIE DES TAGS ==="
for tag in $(printf '%s\n' "${!tags[@]}" | sort); do
    count="${tags[$tag]}"
    depth=$(echo "$tag" | tr -cd '/' | wc -c)
    indent=$(printf '%0.s  ' $(seq 1 "$depth"))
    tag_name=$(basename "$tag")
    echo "${indent}${tag_name} ($count)"
done

# Exemple de sortie attendue:
# dev/
#   python (3)
#   bash (5)
# ai/
#   claude (12)
#   agents (4)
# infra/
#   proxmox (7)
#   linux (15)
```

## Options

| Option | Description |
|--------|-------------|
| `--flat` | Affichage plat (pas d'arbre) |
| `--counts` | Inclure le nombre d'utilisations |
| `--min N` | Filtrer tags avec minimum N occurrences |

## Exemples

```bash
/obs-tags hierarchy              # Arbre complet
/obs-tags hierarchy --counts     # Avec compteurs
/obs-tags hierarchy --min 3      # Tags utilises 3+ fois
```

## Voir Aussi

- `/obs-tags list` - Lister tous les tags
- `/obs-tags unused` - Tags rares
- `/obs-tags rename` - Renommer un tag
