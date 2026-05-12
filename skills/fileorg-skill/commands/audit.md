# Commande: /file-audit

Audit qualite du nommage et de l'organisation d'un dossier.

## Syntaxe

```
/file-audit <chemin> [options]
```

## Actions

### Audit rapide (score)

```bash
#!/usr/bin/env bash
path="${1:-.}"
score=100
issues=()

files=$(find "$path" -maxdepth 1 -type f)
total=$(echo "$files" | grep -c . || echo 0)

# Nommage ISO (25 pts)
no_date=$(echo "$files" | xargs -I{} basename {} | grep -cv '^\d{4}-\d{2}-\d{2}' || echo 0)
[ "$total" -gt 0 ] && ratio=$(( no_date * 100 / total )) || ratio=0
if [ "$ratio" -gt 50 ]; then
  score=$(( score - 25 ))
  issues+=("Plus de 50% sans date ISO")
fi

# Caracteres speciaux (10 pts)
bad_chars=$(find "$path" -maxdepth 1 -type f -name "*[' @#\$%&]*" | wc -l)
if [ "$bad_chars" -gt 0 ]; then
  score=$(( score - 10 ))
  issues+=("$bad_chars fichiers avec caracteres speciaux")
fi

# Doublons potentiels (15 pts)
dupe_count=$(find "$path" -maxdepth 1 -type f -print0 | xargs -0 md5sum 2>/dev/null | \
  awk '{print $1}' | sort | uniq -d | wc -l)
if [ "$dupe_count" -gt 0 ]; then
  score=$(( score - 15 ))
  issues+=("$dupe_count groupes de doublons")
fi

# Profondeur (20 pts)
max_depth=$(find "$path" -type d | awk -F'/' '{print NF}' | sort -n | tail -1)
base_depth=$(echo "$path" | awk -F'/' '{print NF}')
depth=$(( max_depth - base_depth ))
if [ "$depth" -gt 4 ]; then
  score=$(( score - 20 ))
  issues+=("Profondeur > 4 niveaux ($depth)")
fi

# Dossiers vides (10 pts)
empty_dirs=$(find "$path" -type d -empty | wc -l)
if [ "$empty_dirs" -gt 0 ]; then
  score=$(( score - 10 ))
  issues+=("$empty_dirs dossiers vides")
fi

echo "SCORE: $score/100"
echo "Issues:"
for issue in "${issues[@]}"; do echo "  - $issue"; done
```

## Options

| Option | Description |
|--------|-------------|
| `--quick` | Score uniquement |
| `--full` | Rapport detaille |
| `--fix` | Proposer des corrections |

## Exemples

```bash
/file-audit ~/Downloads              # Audit rapide
/file-audit ~/Documents --full       # Rapport complet
/file-audit ~/Desktop --fix          # Audit + corrections
```

## Voir Aussi

- `/file-normalize` - Normaliser les noms
- `/file-clean` - Nettoyer
- `/file-organize` - Organiser
