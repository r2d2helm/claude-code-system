# Commande: /file-old

Trouver les fichiers anciens ou obsoletes.

## Syntaxe

```
/file-old <chemin> [options]
```

## Actions

### Lister les fichiers anciens

```bash
#!/usr/bin/env bash
path="${1}"
days="${2:-365}"

echo "Fichiers non modifies depuis $days jours:"

total=0
total_size=0

while IFS= read -r -d '' file; do
  age=$(( ( $(date +%s) - $(stat -c %Y "$file") ) / 86400 ))
  size=$(stat -c %s "$file")
  size_kb=$(( size / 1024 ))
  echo "  [$age j] $(basename "$file") (${size_kb} KB)"
  total=$(( total + 1 ))
  total_size=$(( total_size + size ))
done < <(find "$path" -type f -mtime +"$days" -print0 2>/dev/null | head -z -20)

total_mb=$(( total_size / 1048576 ))
echo "Total: $total fichiers | Taille: ${total_mb} MB"
```

### Archiver les anciens fichiers

```bash
#!/usr/bin/env bash
path="${1}"
days="${2:-365}"
year=$(date +%Y)
archive_path="${path}/_ARCHIVE/${year}"

mkdir -p "$archive_path"

find "$path" -maxdepth 1 -type f -mtime +"$days" -print0 | \
  xargs -0 -I{} mv {} "$archive_path/"

count=$(find "$archive_path" -type f | wc -l)
echo "Archives: $count fichiers -> $archive_path"
```

## Options

| Option | Description |
|--------|-------------|
| `--days N` | Age minimum en jours (defaut: 365) |
| `--archive` | Deplacer vers _ARCHIVE/ |
| `--delete` | Supprimer (avec confirmation) |
| `--dry-run` | Preview sans action |

## Exemples

```bash
/file-old ~/Documents                  # >1 an
/file-old ~/Downloads --days 90        # >3 mois
/file-old ~/Documents --archive        # Archiver
```

## Voir Aussi

- `/file-archive` - Archiver fichiers
- `/file-clean` - Nettoyer
