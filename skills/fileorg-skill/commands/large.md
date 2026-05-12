# Commande: /file-large

Trouver les fichiers les plus volumineux.

## Syntaxe

```
/file-large [chemin] [options]
```

## Comportement

Scanne un dossier et liste les fichiers les plus gros, avec categorisation par type et suggestions d'action.

## Script bash

```bash
#!/usr/bin/env bash
path="${1:-.}"
top="${2:-20}"
min_size_mb="${3:-50}"
min_size_bytes=$(( min_size_mb * 1048576 ))

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║     GROS FICHIERS (> ${min_size_mb} MB)"
echo "╠══════════════════════════════════════════════╣"
echo "║                                              ║"

mapfile -t files < <(
  find "$path" -type f -size +"${min_size_mb}M" -printf '%s %p\n' 2>/dev/null | \
  sort -rn | head -"$top"
)

echo "║  Trouves: ${#files[@]} fichiers"
echo "║                                              ║"

i=1
for entry in "${files[@]}"; do
  size_bytes=$(echo "$entry" | awk '{print $1}')
  file=$(echo "$entry" | awk '{print $2}')
  filename=$(basename "$file")
  ext="${filename##*.}"

  if [ "$size_bytes" -gt 1073741824 ]; then
    size_str=$(awk "BEGIN {printf \"%.1f GB\", $size_bytes/1073741824}")
  else
    size_str=$(awk "BEGIN {printf \"%.0f MB\", $size_bytes/1048576}")
  fi

  mod_date=$(stat -c %y "$file" 2>/dev/null | cut -c1-10)
  age_days=$(( ( $(date +%s) - $(stat -c %Y "$file" 2>/dev/null) ) / 86400 ))

  printf "║  %2d. %8s | .%-5s | %s\n" "$i" "$size_str" "$ext" "$filename"
  printf "║      %s (%d jours) | %s\n" "$mod_date" "$age_days" "$(dirname "${file#"$path"/}")"
  i=$(( i + 1 ))
done

echo "║                                              ║"
echo "║  PAR TYPE:"
find "$path" -type f -size +"${min_size_mb}M" -printf '%s %f\n' 2>/dev/null | \
  awk '{n=split($2,a,"."); ext=a[n]; sizes[ext]+=$1; counts[ext]++}
  END {for(e in sizes) printf "║    .%-6s : %d fichiers (%.1f GB)\n", e, counts[e], sizes[e]/1073741824}' | \
  sort -t'(' -k2 -rn | head -5

echo "║                                              ║"
echo "║  Actions possibles:                          ║"
echo "║  1. /file-archive pour les anciens           ║"
echo "║  2. /file-duplicates pour verifier doublons  ║"
echo "║  3. Supprimer manuellement si obsoletes      ║"
echo "║                                              ║"
echo "╚══════════════════════════════════════════════╝"
```

## Options

| Option | Description |
|--------|-------------|
| `--top=N` | Nombre de fichiers a afficher (defaut: 20) |
| `--min-size=N` | Taille minimum en MB (defaut: 50) |
| `--type=ext` | Filtrer par extension |

## Exemples

```bash
# Top 20 fichiers > 50 MB
/file-large Documents

# Top 10 fichiers > 100 MB
/file-large ~ --top=10 --min-size=100

# Seulement les videos
/file-large Downloads --type=.mp4
```
