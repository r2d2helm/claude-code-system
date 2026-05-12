# Commande: /file-archive

Archiver les fichiers anciens dans une structure par annee.

## Syntaxe

```
/file-archive [chemin] [options]
```

## Comportement

Deplace les fichiers plus anciens qu'un seuil donne vers un dossier `_ARCHIVE/YYYY/` organise par annee de derniere modification.

## Script bash

```bash
#!/usr/bin/env bash
path="${1:-.}"
older_than_months="${2:-12}"
archive_dir="${3:-_ARCHIVE}"
dry_run="${4:-}"

cutoff_days=$(( older_than_months * 30 ))
archive_path="${path}/${archive_dir}"
moved=0
total_size=0

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║     ARCHIVAGE DE FICHIERS                    ║"
echo "╠══════════════════════════════════════════════╣"
echo "║                                              ║"
echo "║  Source:   $path"
echo "║  Seuil:    > $older_than_months mois"
echo "║                                              ║"

while IFS= read -r -d '' file; do
  year=$(date -r "$file" +%Y 2>/dev/null || stat -c %y "$file" | cut -c1-4)
  year_dir="${archive_path}/${year}"

  if [ "${dry_run}" = "--dry-run" ]; then
    echo "[DRY RUN] $(basename "$file") -> ${archive_dir}/${year}/"
  else
    mkdir -p "$year_dir"
    dest="${year_dir}/$(basename "$file")"
    if [ -e "$dest" ]; then
      dest="${year_dir}/$(basename "${file%.*}")_$(date +%H%M%S).${file##*.}"
    fi
    mv "$file" "$dest"
  fi
  moved=$(( moved + 1 ))
done < <(find "$path" -type f -mtime +"$cutoff_days" -not -path "*/${archive_dir}/*" -print0)

echo "║  Traite: $moved fichiers"
echo "║                                              ║"
echo "╚══════════════════════════════════════════════╝"
```

## Options

| Option | Description |
|--------|-------------|
| `--older-than=N` | Mois d'anciennete (defaut: 12) |
| `--dest=path` | Dossier d'archive personnalise |
| `--dry-run` | Simuler sans deplacer |

## Exemples

```bash
# Archiver les fichiers > 1 an
/file-archive Documents

# Archiver les fichiers > 6 mois (dry run)
/file-archive Downloads --older-than=6 --dry-run

# Archive personnalisee
/file-archive Documents --dest="/mnt/data/Archives"
```
