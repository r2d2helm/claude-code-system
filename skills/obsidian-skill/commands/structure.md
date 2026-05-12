# Commande: /obs-structure

Analyser la structure des dossiers du vault Obsidian.

## Syntaxe

```
/obs-structure [options]
```

## Actions

### Analyse de la structure

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

# Stats par dossier
find "$VAULT" -type d | grep -vE '\.obsidian|\.git' | while IFS= read -r folder; do
    rel="${folder#$VAULT/}"
    [ "$rel" = "$folder" ] && rel="."
    file_count=$(find "$folder" -maxdepth 1 -name "*.md" -type f | wc -l)
    depth=$(echo "$rel" | tr -cd '/' | wc -c)
    printf "%d\t%s\t%d\n" "$file_count" "$rel" "$depth"
done | sort -rn | awk '{printf "%-40s %4d notes  profondeur: %d\n", $2, $1, $3}' | column -t

# Profondeur maximale
max_depth=$(find "$VAULT" -type d | grep -vE '\.obsidian|\.git' | while IFS= read -r d; do
    rel="${d#$VAULT/}"
    echo "$rel" | tr -cd '/' | wc -c
done | sort -rn | head -1)

echo ""
echo "Profondeur max: $max_depth niveaux"
echo "Total dossiers: $(find "$VAULT" -type d | grep -vE '\.obsidian|\.git' | wc -l)"

# Alertes
deep_count=$(find "$VAULT" -type d | grep -vE '\.obsidian|\.git' | while IFS= read -r d; do
    rel="${d#$VAULT/}"
    depth=$(echo "$rel" | tr -cd '/' | wc -c)
    [ "$depth" -gt 3 ] && echo "$d"
done | wc -l)

[ "$deep_count" -gt 0 ] && echo "ALERTE: $deep_count dossiers avec profondeur > 3"
```

## Options

| Option | Description |
|--------|-------------|
| `--tree` | Affichage en arbre ASCII |
| `--depth N` | Limiter a N niveaux |
| `--empty` | Montrer les dossiers vides |

## Exemples

```bash
/obs-structure                # Analyse complete
/obs-structure --tree         # Vue en arbre
/obs-structure --empty        # Dossiers vides
```

## Voir Aussi

- `/obs-health` - Diagnostic complet
- `/obs-stats` - Statistiques generales
