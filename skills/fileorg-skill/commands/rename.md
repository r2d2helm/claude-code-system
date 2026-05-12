# Commande: /file-rename

Renommer fichiers selon les conventions de nommage standardisees.

## Syntaxe

```
/file-rename [chemin] [mode] [options]
```

## Modes de Renommage

### /file-rename iso-date [chemin]

Ajouter prefixe date ISO 8601 aux fichiers :

```
╔══════════════════════════════════════════════════════════════╗
║           RENOMMAGE DATE ISO                                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  PREVISUALISATION:                                           ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ AVANT                    ->  APRES                      │ ║
║  │ ──────────────────────────────────────────────────────  │ ║
║  │ Facture EDF.pdf          ->  2026-01-15_Facture-EDF.pdf │ ║
║  │ Photo vacances.jpg       ->  2025-08-22_Photo-vacances.jpg│ ║
║  │ Rapport final v2.docx    ->  2026-02-01_Rapport-final_v02.docx│ ║
║  │ scan001.pdf              ->  2026-02-03_scan001.pdf     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Fichiers a renommer: 47                                     ║
║                                                              ║
║  [1] Appliquer  [2] Modifier  [3] Annuler                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
path="${1:-.}"
dry_run="${2:-}"

find "$path" -maxdepth 1 -type f | while IFS= read -r file; do
  name=$(basename "$file")
  dir=$(dirname "$file")
  ext="${name##*.}"
  base="${name%.*}"

  mod_time=$(stat -c %Y "$file")
  date_prefix=$(date -d "@$mod_time" +%Y-%m-%d)

  # Nettoyer le nom existant
  clean_name=$(echo "$base" | tr ' ' '-' | tr -cd '[:alnum:]_.-')

  # Eviter double prefixe date
  if ! echo "$clean_name" | grep -qE '^\d{4}-\d{2}-\d{2}'; then
    new_name="${date_prefix}_${clean_name}.${ext}"
  else
    new_name="${clean_name}.${ext}"
  fi

  if [ "${dry_run}" = "--dry-run" ]; then
    echo "$name -> $new_name"
  else
    mv "$file" "${dir}/${new_name}"
  fi
done
```

### /file-rename normalize [chemin]

Normaliser les noms de fichiers :

```
╔══════════════════════════════════════════════════════════════╗
║           NORMALISATION DES NOMS                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  CORRECTIONS:                                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Probleme                 ->  Correction                 │ ║
║  │ ──────────────────────────────────────────────────────  │ ║
║  │ Mon Document (1).pdf     ->  Mon-Document_01.pdf        │ ║
║  │ cafe & croissant.jpg     ->  cafe-croissant.jpg         │ ║
║  │ RAPPORT FINAL!!!.docx    ->  Rapport-Final.docx         │ ║
║  │ fichier   mal  nomme.txt ->  fichier-mal-nomme.txt      │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Corrections: espaces (23), accents (12), speciaux (8)       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
normalize_filename() {
  local name="$1"

  # Remplacer accents
  name=$(echo "$name" | sed \
    -e 's/[éèêë]/e/g' -e 's/[àâä]/a/g' \
    -e 's/[ùûü]/u/g' -e 's/[îï]/i/g' \
    -e 's/[ôö]/o/g' -e 's/ç/c/g' \
    -e 's/[ÉÈÊË]/E/g' -e 's/[ÀÂÄ]/A/g' \
    -e 's/[ÙÛÜ]/U/g' -e 's/[ÔÖ]/O/g' \
    -e 's/Ç/C/g')

  # Remplacer espaces multiples par un tiret
  name=$(echo "$name" | tr -s ' ' '-')

  # Supprimer caracteres speciaux
  name=$(echo "$name" | tr -cd '[:alnum:]_.-')

  # Supprimer tirets multiples
  name=$(echo "$name" | sed 's/-\{2,\}/-/g' | sed 's/^-//' | sed 's/-$//')

  echo "$name"
}

path="${1:-.}"

find "$path" -maxdepth 1 -type f | while IFS= read -r file; do
  dir=$(dirname "$file")
  name=$(basename "$file")
  ext="${name##*.}"
  base="${name%.*}"

  new_base=$(normalize_filename "$base")
  new_name="${new_base}.${ext}"

  if [ "$name" != "$new_name" ]; then
    mv "$file" "${dir}/${new_name}"
    echo "  $name -> $new_name"
  fi
done
```

### /file-rename version [chemin]

Gerer le versionnage des fichiers :

```
╔══════════════════════════════════════════════════════════════╗
║           GESTION DES VERSIONS                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ANALYSE DES VERSIONS:                                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Fichier                  │ Versions │ Action            │ ║
║  │ ─────────────────────────┼──────────┼─────────────────  │ ║
║  │ Rapport-Analyse          │ 5        │ Garder v05        │ ║
║  │ Proposition-Client       │ 3        │ Renommer          │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
path="${1:-.}"

# Detecter les fichiers avec patterns de version courants
find "$path" -type f | while IFS= read -r file; do
  name=$(basename "$file")
  base="${name%.*}"
  # Detecter: v1, v2, (1), (2), final, new, old
  if echo "$base" | grep -qiE '[-_]?v[0-9]+$|\([0-9]+\)$|[-_]?(final[0-9]*|new|nouveau|old)$'; then
    # Extraire la base sans le suffixe de version
    clean=$(echo "$base" | sed -E 's/[-_]?v[0-9]+$//; s/\([0-9]+\)$//; s/[-_]?(final[0-9]*|new|nouveau|old)$//')
    echo "$clean | $name"
  fi
done | sort | \
  awk -F' | ' '{
    if ($1 != prev) { if (count > 1) print group; count=0; group=""; prev=$1 }
    count++; group=group"\n  "$2
  } END { if (count > 1) print group }'
```

### /file-rename bulk [chemin] [pattern]

Renommage en masse avec pattern :

```
╔══════════════════════════════════════════════════════════════╗
║           RENOMMAGE EN MASSE                                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Pattern: {date}_{type}_{numero:3}                           ║
║  Exemple: 2026-02-03_Photo_001.jpg                           ║
║                                                              ║
║  Tokens disponibles:                                         ║
║  {date}     - Date ISO (2026-02-03)                          ║
║  {year}     - Annee (2026)                                   ║
║  {month}    - Mois (02)                                      ║
║  {day}      - Jour (03)                                      ║
║  {numero:N} - Numero sequentiel (N = nb chiffres)            ║
║  {original} - Nom original                                   ║
║  {ext}      - Extension                                      ║
║  {type}     - Type personnalise                              ║
║                                                              ║
║  Previsualisation:                                           ║
║  IMG_001.jpg -> 2026-02-03_Photo_001.jpg                     ║
║  IMG_002.jpg -> 2026-02-03_Photo_002.jpg                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
path="${1}"
pattern="${2:-{date}_{original}}"
type_str="${3:-File}"
dry_run="${4:-}"

counter=1
find "$path" -maxdepth 1 -type f | sort | while IFS= read -r file; do
  name=$(basename "$file")
  dir=$(dirname "$file")
  ext="${name##*.}"
  base="${name%.*}"

  mod_time=$(stat -c %Y "$file")
  date=$(date -d "@$mod_time" +%Y-%m-%d)
  year=$(date -d "@$mod_time" +%Y)
  month=$(date -d "@$mod_time" +%m)
  day=$(date -d "@$mod_time" +%d)

  new_name="$pattern"
  new_name="${new_name//\{date\}/$date}"
  new_name="${new_name//\{year\}/$year}"
  new_name="${new_name//\{month\}/$month}"
  new_name="${new_name//\{day\}/$day}"
  new_name="${new_name//\{original\}/$base}"
  new_name="${new_name//\{type\}/$type_str}"
  new_name="${new_name//\{ext\}/$ext}"
  new_name="${new_name//\{numero\}/$(printf '%d' $counter)}"
  new_name="${new_name//\{numero:3\}/$(printf '%03d' $counter)}"

  new_full="${new_name}.${ext}"

  if [ "${dry_run}" = "--dry-run" ]; then
    echo "$name -> $new_full"
  else
    mv "$file" "${dir}/${new_full}"
  fi
  counter=$(( counter + 1 ))
done
```

## Options Globales

| Option | Description |
|--------|-------------|
| `--dry-run` | Previsualiser sans renommer |
| `--recursive` | Inclure sous-dossiers |
| `--lowercase` | Forcer minuscules |
| `--uppercase` | Forcer majuscules |
| `--backup` | Creer copie avant renommage |
| `--log` | Enregistrer les changements |

## Exemples

```bash
# Ajouter date ISO a tous les fichiers
/file-rename iso-date ~/Documents

# Normaliser noms (espaces, accents)
/file-rename normalize ~/Downloads

# Previsualiser sans executer
/file-rename iso-date . --dry-run

# Renommer photos en masse
/file-rename bulk ~/Pictures "{date}_Photo_{numero:3}"

# Standardiser versions
/file-rename version ~/Documents/Rapports
```
