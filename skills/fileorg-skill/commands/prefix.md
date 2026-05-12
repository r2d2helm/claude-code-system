# Commande: /file-prefix

Ajouter un prefixe date ISO 8601 aux fichiers.

## Syntaxe

```
/file-prefix <chemin> [action] [options]
```

## Actions

### Ajouter le prefixe date

```bash
#!/usr/bin/env bash
path="${1}"
dry_run="${2:-}"
count=0

while IFS= read -r -d '' file; do
  name=$(basename "$file")
  # Ignorer si deja prefixe avec date ISO
  if echo "$name" | grep -qE '^\d{4}-\d{2}-\d{2}'; then
    continue
  fi
  dir=$(dirname "$file")
  mod_time=$(stat -c %Y "$file")
  date_prefix=$(date -d "@$mod_time" +%Y-%m-%d)
  new_name="${date_prefix}_${name}"

  if [ "${dry_run}" = "--dry-run" ]; then
    echo "  $name -> $new_name"
  else
    mv "$file" "${dir}/${new_name}"
    echo "  $name -> $new_name"
  fi
  count=$(( count + 1 ))
done < <(find "$path" -maxdepth 1 -type f -print0)

echo "$count fichiers prefixes"
```

### Retirer le prefixe

```bash
#!/usr/bin/env bash
path="${1}"

while IFS= read -r -d '' file; do
  name=$(basename "$file")
  if echo "$name" | grep -qE '^\d{4}-\d{2}-\d{2}_'; then
    dir=$(dirname "$file")
    new_name=$(echo "$name" | sed 's/^\d\{4\}-\d\{2\}-\d\{2\}_//')
    mv "$file" "${dir}/${new_name}"
    echo "  $name -> $new_name"
  fi
done < <(find "$path" -maxdepth 1 -type f -print0)
```

### Mettre a jour le prefixe

```bash
#!/usr/bin/env bash
path="${1}"

# Remplacer le prefixe existant par la date de modification actuelle
while IFS= read -r -d '' file; do
  name=$(basename "$file")
  if echo "$name" | grep -qE '^\d{4}-\d{2}-\d{2}_'; then
    dir=$(dirname "$file")
    mod_time=$(stat -c %Y "$file")
    new_date=$(date -d "@$mod_time" +%Y-%m-%d)
    new_name=$(echo "$name" | sed "s/^\d\{4\}-\d\{2\}-\d\{2\}/${new_date}/")
    if [ "$new_name" != "$name" ]; then
      mv "$file" "${dir}/${new_name}"
      echo "  $name -> $new_name"
    fi
  fi
done < <(find "$path" -maxdepth 1 -type f -print0)
```

## Options

| Option | Description |
|--------|-------------|
| `add` | Ajouter prefixe (defaut) |
| `remove` | Retirer le prefixe |
| `update` | Mettre a jour avec date actuelle |
| `--dry-run` | Preview |

## Exemples

```bash
/file-prefix ~/Documents add       # Ajouter prefixes
/file-prefix ~/Documents remove    # Retirer prefixes
/file-prefix ~/Downloads --dry-run # Preview
```

## Voir Aussi

- `/file-rename` - Renommer selon convention
- `/file-normalize` - Normaliser les noms
