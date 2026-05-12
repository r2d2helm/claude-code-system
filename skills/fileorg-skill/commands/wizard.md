# Commande: /file-wizard

Assistant interactif pour organiser un dossier etape par etape.

## Syntaxe

```
/file-wizard <chemin> [options]
```

## Actions

### Etape 1 : Analyse du dossier

```bash
#!/usr/bin/env bash
path="${1}"

total_files=$(find "$path" -maxdepth 1 -type f | wc -l)
total_dirs=$(find "$path" -maxdepth 1 -type d | wc -l)
total_size=$(du -sh "$path" 2>/dev/null | cut -f1)

echo "=== ANALYSE: $path ==="
echo "Fichiers: $total_files"
echo "Dossiers: $total_dirs"
echo "Taille totale: $total_size"
echo ""
echo "Extensions:"
find "$path" -maxdepth 1 -type f | grep -oE '\.[^./]+$' | sort | uniq -c | sort -rn | \
  awk '{printf "  %s: %d fichiers\n", $2, $1}'
```

### Etape 2 : Detection des problemes

```bash
#!/usr/bin/env bash
path="${1}"
issues=()

files=$(find "$path" -maxdepth 1 -type f)

# Fichiers sans extension
no_ext=$(echo "$files" | while read -r f; do
  name=$(basename "$f"); [ "${name%.*}" = "$name" ] && echo "$f"
done | wc -l)
[ "$no_ext" -gt 0 ] && issues+=("  - $no_ext fichiers sans extension")

# Noms avec espaces ou caracteres speciaux
bad_names=$(find "$path" -maxdepth 1 -type f -name "*[ @#\$%&]*" | wc -l)
[ "$bad_names" -gt 0 ] && issues+=("  - $bad_names noms avec caracteres speciaux/espaces")

# Fichiers volumineux (>100MB)
large=$(find "$path" -maxdepth 1 -type f -size +100M | wc -l)
[ "$large" -gt 0 ] && issues+=("  - $large fichiers > 100 MB")

# Doublons potentiels (meme taille + meme extension)
possible_dupes=$(find "$path" -maxdepth 1 -type f -printf '%s.%f\n' | \
  awk -F'.' '{print $1"."$NF}' | sort | uniq -d | wc -l)
[ "$possible_dupes" -gt 0 ] && issues+=("  - $possible_dupes groupes de doublons potentiels")

# Fichiers anciens (>1 an)
old_files=$(find "$path" -maxdepth 1 -type f -mtime +365 | wc -l)
[ "$old_files" -gt 0 ] && issues+=("  - $old_files fichiers non modifies depuis >1 an")

if [ ${#issues[@]} -eq 0 ]; then
  echo "Aucun probleme detecte!"
else
  echo "Problemes detectes:"
  for issue in "${issues[@]}"; do echo "$issue"; done
fi
```

### Etape 3 : Proposition d'organisation

```bash
#!/usr/bin/env bash
path="${1}"

echo "=== PLAN D'ORGANISATION ==="
echo ""
echo "Actions proposees:"
echo "  1. Trier par type (extension) dans des sous-dossiers"
echo "  2. Normaliser les noms (accents, espaces)"
echo "  3. Archiver les fichiers anciens (>1 an)"
echo "  4. Detecter et traiter les doublons"
echo "  5. Nettoyer les fichiers temporaires"
echo ""
echo "Commandes correspondantes:"
echo "  /file-sort $path"
echo "  /file-normalize $path"
echo "  /file-old $path --archive"
echo "  /file-duplicates $path"
echo "  /file-clean $path"
```

### Etape 4 : Execution guidee

```bash
#!/usr/bin/env bash
path="${1}"

# Creer un backup avant modification
timestamp=$(date +%Y%m%d-%H%M%S)
backup_dir="$HOME/Documents/Backups/wizard_${timestamp}"
echo "Backup de securite: $backup_dir"

rsync -a "$path/" "$backup_dir/" --quiet

echo "Backup cree. Pret pour l'organisation."
echo "Executer les commandes une par une avec confirmation."
```

## Options

| Option | Description |
|--------|-------------|
| `--auto` | Executer toutes les etapes automatiquement |
| `--step` | Mode pas-a-pas avec confirmation (defaut) |
| `--backup` | Creer un backup avant modification |
| `--dry-run` | Preview sans modification |

## Exemples

```bash
/file-wizard ~/Downloads                   # Wizard complet
/file-wizard ~/Documents --dry-run         # Preview seulement
/file-wizard ~/Data --auto                 # Mode automatique
```

## Voir Aussi

- `/file-analyze` - Analyse detaillee
- `/file-organize` - Organisation par type
- `/file-audit` - Audit qualite
