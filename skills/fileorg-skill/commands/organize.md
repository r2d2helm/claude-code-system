# Commande: /file-organize

Organiser automatiquement les fichiers par type, date ou categorie personnalisee.

## Syntaxe

```
/file-organize [chemin] [mode] [options]
```

## Modes d'Organisation

### /file-organize downloads

Organiser le dossier Telechargements :

```
╔══════════════════════════════════════════════════════════════╗
║           ORGANISATION DOWNLOADS                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ANALYSE:                                                    ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Fichiers trouves    : 247                               │ ║
║  │ Taille totale       : 12.4 GB                           │ ║
║  │ Types detectes      : 15                                │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  PLAN D'ORGANISATION:                                        ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Documents  (42)  -> Downloads/Documents/                │ ║
║  │ Images     (89)  -> Downloads/Images/                   │ ║
║  │ Videos     (12)  -> Downloads/Videos/                   │ ║
║  │ Archives   (34)  -> Downloads/Archives/                 │ ║
║  │ Autres     (42)  -> Downloads/Autres/                   │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Executer  [2] Previsualiser  [3] Personnaliser          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
downloads=~/Downloads

declare -A rules
rules[Documents]="pdf doc docx txt odt rtf xls xlsx ppt pptx"
rules[Images]="jpg jpeg png gif webp svg bmp ico tiff"
rules[Videos]="mp4 mkv avi mov wmv flv webm"
rules[Audio]="mp3 wav flac m4a aac ogg"
rules[Archives]="zip rar 7z tar gz bz2 xz"
rules[Paquets]="deb rpm AppImage run"
rules[Code]="py js ts sh bash json xml yaml yml"

for category in "${!rules[@]}"; do
  dest="${downloads}/${category}"
  mkdir -p "$dest"
  for ext in ${rules[$category]}; do
    find "$downloads" -maxdepth 1 -type f -iname "*.${ext}" -exec mv {} "$dest/" \; 2>/dev/null
  done
done

# Deplacer le reste dans "Autres"
mkdir -p "${downloads}/Autres"
find "$downloads" -maxdepth 1 -type f -exec mv {} "${downloads}/Autres/" \; 2>/dev/null
```

### /file-organize by-date [chemin]

Organiser par date (YYYY/YYYY-MM) :

```
╔══════════════════════════════════════════════════════════════╗
║           ORGANISATION PAR DATE                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Structure creee:                                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Pictures/                                               │ ║
║  │ ├── 2024/                                               │ ║
║  │ │   ├── 2024-01/ (23 fichiers)                          │ ║
║  │ │   ├── 2024-02/ (45 fichiers)                          │ ║
║  │ │   └── ...                                             │ ║
║  │ └── 2026/                                               │ ║
║  │     └── 2026-02/ (12 fichiers)                          │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Total: 456 fichiers organises dans 24 dossiers              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
source_path="${1:-$HOME/Pictures}"

find "$source_path" -type f | while IFS= read -r file; do
  mod_time=$(stat -c %Y "$file")
  year=$(date -d "@$mod_time" +%Y)
  year_month=$(date -d "@$mod_time" +%Y-%m)

  dest_folder="${source_path}/${year}/${year_month}"
  mkdir -p "$dest_folder"

  if [ "$(dirname "$file")" != "$dest_folder" ]; then
    mv "$file" "$dest_folder/"
  fi
done

echo "Fichiers organises par date"
```

### /file-organize by-project [chemin]

Creer structure projet standard :

```
╔══════════════════════════════════════════════════════════════╗
║           STRUCTURE PROJET                                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Nom du projet: MultiPass-Website                            ║
║                                                              ║
║  Structure creee:                                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ MultiPass-Website/                                      │ ║
║  │ ├── 00-Admin/          # Contrats, briefs, planning     │ ║
║  │ ├── 01-Recherche/      # Etudes, benchmarks             │ ║
║  │ ├── 02-Design/         # Maquettes, assets              │ ║
║  │ ├── 03-Development/    # Code source                    │ ║
║  │ ├── 04-Content/        # Textes, medias                 │ ║
║  │ ├── 05-Livrables/      # Exports finaux                 │ ║
║  │ ├── 06-Archive/        # Anciennes versions             │ ║
║  │ └── README.md          # Documentation projet           │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
project_name="${1}"
base_path="${2:-$HOME/Documents/Projets}"

project_path="${base_path}/${project_name}"
folders=(
  "00-Admin"
  "01-Recherche"
  "02-Design"
  "03-Development"
  "04-Content"
  "05-Livrables"
  "06-Archive"
)

for folder in "${folders[@]}"; do
  mkdir -p "${project_path}/${folder}"
done

# Creer README
cat > "${project_path}/README.md" <<EOF
# ${project_name}

## Structure
- **00-Admin**: Contrats, briefs, planning
- **01-Recherche**: Etudes, benchmarks, references
- **02-Design**: Maquettes, wireframes, assets
- **03-Development**: Code source, configs
- **04-Content**: Textes, medias, contenus
- **05-Livrables**: Exports finaux
- **06-Archive**: Anciennes versions

## Conventions de nommage
- Date ISO: YYYY-MM-DD
- Versions: v01, v02...
- Pas d'espaces ni caracteres speciaux

Cree le: $(date +%Y-%m-%d)
EOF

echo "Structure projet '${project_name}' creee"
```

## Options

| Option | Description | Exemple |
|--------|-------------|---------|
| `--dry-run` | Simuler sans deplacer | `/file-organize downloads --dry-run` |
| `--recursive` | Inclure sous-dossiers | `/file-organize . --recursive` |
| `--by-type` | Organiser par extension | `/file-organize . --by-type` |
| `--by-date` | Organiser par date | `/file-organize . --by-date` |
| `--verbose` | Afficher details | `/file-organize . --verbose` |

## Exemples

```bash
# Organiser Telechargements par type
/file-organize downloads

# Organiser Photos par date
/file-organize ~/Pictures --by-date

# Simuler organisation sans executer
/file-organize downloads --dry-run

# Creer structure projet
/file-organize by-project "MonProjet"

# Organisation automatique
/file-organize auto ~/Documents
```
