# Commande: /file-structure

Analyser ou creer une structure de dossiers.

## Syntaxe

```
/file-structure [action] [chemin] [options]
```

## Actions

### /file-structure analyze [chemin]

Analyser la structure existante d'un dossier :

```bash
#!/usr/bin/env bash
path="${1:-.}"

total_dirs=$(find "$path" -type d | wc -l)
total_files=$(find "$path" -type f | wc -l)
empty_dirs=$(find "$path" -type d -empty | wc -l)

# Profondeur
base_parts=$(echo "$path" | awk -F'/' '{print NF}')
max_depth=$(find "$path" -type f | awk -F'/' -v base="$base_parts" '{print NF - base}' | sort -n | tail -1)
avg_depth=$(find "$path" -type f | awk -F'/' -v base="$base_parts" '{sum += NF - base; n++} END {printf "%.1f", sum/n}')

# Dossiers avec trop de fichiers (>100)
overloaded=$(find "$path" -mindepth 1 -maxdepth 1 -type d | while read -r dir; do
  count=$(find "$dir" -maxdepth 1 -type f | wc -l)
  [ "$count" -gt 100 ] && echo "$dir ($count fichiers)"
done | wc -l)

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║     ANALYSE STRUCTURE                        ║"
echo "╠══════════════════════════════════════════════╣"
echo "║                                              ║"
printf "║  Dossiers:           %6d              ║\n" "$total_dirs"
printf "║  Fichiers:           %6d              ║\n" "$total_files"
printf "║  Profondeur max:     %6d              ║\n" "$max_depth"
printf "║  Profondeur moyenne: %6s              ║\n" "$avg_depth"
printf "║  Dossiers vides:     %6d              ║\n" "$empty_dirs"
printf "║  Dossiers surcharges:%6d (>100 fich.)  ║\n" "$overloaded"
echo "║                                              ║"

[ "$max_depth" -gt 4 ] && echo "║  Profondeur > 4: considerer /file-flatten    ║"
[ "$empty_dirs" -gt 0 ] && echo "║  Dossiers vides: considerer /file-empty      ║"

echo "║                                              ║"
echo "╚══════════════════════════════════════════════╝"
```

### /file-structure apply [template]

Appliquer une structure predefinie :

| Template | Description |
|----------|-------------|
| `personal` | Structure Documents personnels (PARA) |
| `developer` | Structure projet developpeur |
| `business` | Structure entreprise |
| `creative` | Structure creatif/designer |

```bash
#!/usr/bin/env bash
base_path="${1}"
template="${2:-personal}"

declare -A structures
structures[personal]="_INBOX _ARCHIVE Administratif/Banque Administratif/Impots Administratif/Assurances Administratif/Factures Projets Travail Personnel"
structures[developer]="01-Projects 02-Libraries 03-Scripts 04-Config 05-Archive"
structures[business]="Clients Projets Admin/Contrats Admin/Factures Resources Archive"
structures[creative]="Clients Portfolio/2025 Portfolio/2026 Assets/Fonts Assets/Images Archive"

dirs="${structures[$template]}"

for dir in $dirs; do
  full_path="${base_path}/${dir}"
  if [ ! -d "$full_path" ]; then
    mkdir -p "$full_path"
    echo "Cree: $dir"
  fi
done
```

## Options

| Option | Description |
|--------|-------------|
| `analyze` | Analyser la structure existante |
| `apply [template]` | Appliquer un template |
| `--dry-run` | Simuler sans creer |
