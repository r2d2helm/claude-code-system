# Commande: /file-version

Gerer les versions de fichiers (v01, v02...).

## Syntaxe

```
/file-version <chemin> [action] [options]
```

## Actions

### Lister les versions

```bash
#!/usr/bin/env bash
path="${1}"

find "$path" -type f | grep -E '_v[0-9]+\.' | while IFS= read -r file; do
  name=$(basename "$file")
  base=$(echo "${name%.*}" | sed 's/_v[0-9]*$//')
  mod_date=$(stat -c %y "$file" | cut -c1-10)
  echo "$base | $name ($mod_date)"
done | sort | awk -F' | ' '
{
  if ($1 != prev) {
    if (count > 0) print ""
    print $1":"
    prev=$1; count=0
  }
  print "  "$2
  count++
}'
```

### Incrementer la version

```bash
#!/usr/bin/env bash
file="${1}"
dir=$(dirname "$file")
name=$(basename "$file")
ext="${name##*.}"
base="${name%.*}"

if echo "$base" | grep -qE '_v[0-9]+$'; then
  current=$(echo "$base" | grep -oE 'v[0-9]+$' | grep -oE '[0-9]+')
  next=$(printf '%02d' $(( current + 1 )))
  new_base=$(echo "$base" | sed "s/v${current}\$/v${next}/")
  cp "$file" "${dir}/${new_base}.${ext}"
  echo "Nouvelle version: ${new_base}.${ext}"
else
  # Premier versionnage
  mv "$file" "${dir}/${base}_v01.${ext}"
  cp "${dir}/${base}_v01.${ext}" "${dir}/${base}_v02.${ext}"
  echo "Versionne: v01 (original) + v02 (copie)"
fi
```

### Nettoyer les anciennes versions

```bash
#!/usr/bin/env bash
path="${1}"
keep="${2:-2}"

find "$path" -type f | grep -E '_v[0-9]+\.' | \
  sed 's/_v[0-9]*\././' | sort -u | while IFS= read -r base_file; do
    # Trouver toutes les versions de ce fichier
    pattern="${base_file%.*}_v"
    ext="${base_file##*.}"
    versions=$(ls "${pattern}"*".$ext" 2>/dev/null | sort -t'v' -k2 -n)
    count=$(echo "$versions" | grep -c . || echo 0)

    if [ "$count" -gt "$keep" ]; then
      to_delete=$(echo "$versions" | head -n $(( count - keep )))
      echo "$to_delete" | while read -r old_file; do
        echo "Supprimer: $(basename "$old_file")"
        # rm "$old_file"  # Decommentez pour supprimer
      done
    fi
  done
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister les fichiers versionnes |
| `bump` | Incrementer la version |
| `clean` | Supprimer anciennes versions |
| `--keep N` | Garder N versions (defaut: 2) |

## Exemples

```bash
/file-version ~/Documents list      # Lister les versions
/file-version rapport.docx bump     # v01 -> v02
/file-version ~/Documents clean     # Nettoyer
```

## Voir Aussi

- `/file-rename` - Renommer fichiers
- `/file-archive` - Archiver anciens fichiers
