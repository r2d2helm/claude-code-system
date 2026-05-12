# Commande: /file-flatten

Aplatir une arborescence trop profonde (>3 niveaux).

## Syntaxe

```
/file-flatten <chemin> [options]
```

## Actions

### Preview (dry-run)

```bash
#!/usr/bin/env bash
path="${1}"
max_depth="${2:-3}"

base_depth=$(echo "$path" | awk -F'/' '{print NF}')
limit=$(( base_depth + max_depth ))

echo "Fichiers a profondeur > $max_depth :"
find "$path" -type f | while read -r file; do
  depth=$(echo "$file" | awk -F'/' '{print NF}')
  if [ "$depth" -gt "$limit" ]; then
    rel="${file#"$path"/}"
    echo "  $rel"
  fi
done | head -50
```

### Executer l'aplatissement

```bash
#!/usr/bin/env bash
path="${1}"
max_depth="${2:-3}"

base_depth=$(echo "$path" | awk -F'/' '{print NF}')
limit=$(( base_depth + max_depth ))

find "$path" -type f | while read -r file; do
  depth=$(echo "$file" | awk -F'/' '{print NF}')
  if [ "$depth" -gt "$limit" ]; then
    rel="${file#"$path"/}"
    # Garder les 2 premiers niveaux + nom du fichier
    parts=$(echo "$rel" | awk -F'/' '{print $1"/"$2}')
    new_dir="${path}/${parts}"
    mkdir -p "$new_dir"
    mv "$file" "${new_dir}/$(basename "$file")"
    echo "Deplace: $rel -> $parts/"
  fi
done

# Supprimer les dossiers vides
find "$path" -type d -empty -delete
```

## Options

| Option | Description |
|--------|-------------|
| `--max-depth N` | Profondeur max (defaut: 3) |
| `--dry-run` | Preview sans deplacer |

## Exemples

```bash
/file-flatten ~/Documents --dry-run         # Preview
/file-flatten ~/Documents --max-depth 2     # Aplatir a 2 niveaux
```

## Voir Aussi

- `/file-structure` - Creer une structure
- `/file-sort` - Trier des fichiers
