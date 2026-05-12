# Commande: /file-sort

Trier fichiers dans des sous-dossiers par type, date ou taille.

## Syntaxe

```
/file-sort <chemin> [mode] [options]
```

## Actions

### Trier par extension

```bash
#!/usr/bin/env bash
path="${1}"

find "$path" -maxdepth 1 -type f | while IFS= read -r file; do
  name=$(basename "$file")
  ext="${name##*.}"
  folder=$(echo "$ext" | tr '[:lower:]' '[:upper:]')
  dest="${path}/${folder}"
  mkdir -p "$dest"
  mv "$file" "$dest/"
  echo "  .${ext}: $name -> ${folder}/"
done | sort | uniq -c
```

### Trier par date

```bash
#!/usr/bin/env bash
path="${1}"

find "$path" -maxdepth 1 -type f | while IFS= read -r file; do
  mod_time=$(stat -c %Y "$file")
  date_folder=$(date -d "@$mod_time" +%Y-%m)
  dest="${path}/${date_folder}"
  mkdir -p "$dest"
  mv "$file" "$dest/"
done
```

### Trier par taille

```bash
#!/usr/bin/env bash
path="${1}"

find "$path" -maxdepth 1 -type f -printf '%s %p\n' | while read -r size file; do
  if [ "$size" -lt 1048576 ]; then
    folder="Petit_lt1MB"
  elif [ "$size" -lt 104857600 ]; then
    folder="Moyen_1-100MB"
  else
    folder="Gros_gt100MB"
  fi
  dest="${path}/${folder}"
  mkdir -p "$dest"
  mv "$file" "$dest/"
done
```

## Options

| Option | Description |
|--------|-------------|
| `by-type` | Par extension (defaut) |
| `by-date` | Par mois (YYYY-MM) |
| `by-size` | Par taille (petit/moyen/gros) |
| `--dry-run` | Preview sans deplacer |

## Exemples

```bash
/file-sort ~/Downloads by-type         # Par extension
/file-sort ~/Downloads by-date         # Par mois
/file-sort ~/Desktop by-size --dry-run # Preview
```

## Voir Aussi

- `/file-organize` - Organisation avancee
- `/file-flatten` - Aplatir arborescence
