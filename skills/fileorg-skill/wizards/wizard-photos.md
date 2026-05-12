# Wizard: Organisation Photos

Organisation complete de bibliotheque photos.

## Declenchement

```
/file-wizard photos
```

## Etapes du Wizard (4)

### Etape 1: Analyse Bibliotheque

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD ORGANISATION PHOTOS                         ║
║                Etape 1/4 : Analyse                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ANALYSE: ~/Pictures                                         ║
║                                                              ║
║  STATISTIQUES:                                               ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Photos totales     : 12,345                             │ ║
║  │ Taille totale      : 89.2 GB                            │ ║
║  │ Periode            : 2018-2026 (8 ans)                  │ ║
║  │ Formats            : JPG (85%), PNG (10%), RAW (5%)     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  DISTRIBUTION PAR ANNEE:                                     ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 2026 : ████░░░░░░░░░░░░░░░░░░░░░░░░░░ 456 (4%)         │ ║
║  │ 2025 : ██████████████░░░░░░░░░░░░░░░░ 2,345 (19%)      │ ║
║  │ 2024 : ████████████████████░░░░░░░░░░ 3,456 (28%)      │ ║
║  │ 2023 : ██████████████░░░░░░░░░░░░░░░░ 2,234 (18%)      │ ║
║  │ <2023: ████████████████████░░░░░░░░░░ 3,854 (31%)      │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  PROBLEMES DETECTES:                                         ║
║  * 4,567 photos avec noms generiques (IMG_, DSC_, Photo)     ║
║  * 234 doublons potentiels (2.1 GB)                          ║
║  * 89 captures d'ecran melangees                             ║
║  * Pas de structure par date                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Etape 2: Structure Cible

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD ORGANISATION PHOTOS                         ║
║               Etape 2/4 : Structure                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  STRUCTURE PROPOSEE:                                         ║
║                                                              ║
║  Pictures/                                                   ║
║  ├── {YYYY}/                    # Par annee                  ║
║  │   └── {YYYY-MM}/             # Par mois                   ║
║  │       └── {YYYY-MM-DD}_001.jpg                            ║
║  ├── Albums/                    # Albums thematiques         ║
║  │   ├── Vacances-2025-Bretagne/                             ║
║  │   └── Anniversaire-Marie/                                 ║
║  ├── Screenshots/               # Captures d'ecran           ║
║  ├── Wallpapers/                # Fonds d'ecran              ║
║  └── _Import/                   # Photos a trier             ║
║                                                              ║
║  Format de nommage:                                          ║
║  [x] Date ISO en prefixe (YYYY-MM-DD)                        ║
║  [x] Numero sequentiel (001, 002...)                         ║
║  [ ] Conserver nom original                                  ║
║  [ ] Ajouter evenement/lieu                                  ║
║                                                              ║
║  [1] Appliquer  [2] Modifier  [3] Previsualiser              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Etape 3: Traitement

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD ORGANISATION PHOTOS                         ║
║              Etape 3/4 : Traitement                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ORGANISATION EN COURS...                                    ║
║                                                              ║
║  [████████████████████████░░░░░░░░░░░░░░░░] 60%              ║
║  7,407 / 12,345 photos traitees                              ║
║                                                              ║
║  Actions en cours:                                           ║
║  Creation structure annee/mois                               ║
║  Deplacement photos 2018-2023                                ║
║  Deplacement photos 2024                                     ║
║  En attente: Deplacement photos 2025-2026                    ║
║  En attente: Renommage avec date                             ║
║  En attente: Separation screenshots                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script organisation photos:**
```bash
#!/usr/bin/env bash
source_path="${1:-$HOME/Pictures}"

# Creer structure annee/mois
for year in $(seq 2018 2026); do
  for month in $(seq -w 1 12); do
    dir="${source_path}/${year}/${year}-${month}"
    mkdir -p "$dir"
  done
done

# Dossiers speciaux
for special in Albums Screenshots Wallpapers _Import; do
  mkdir -p "${source_path}/${special}"
done

# Organiser photos par date
find "$source_path" -type f \( \
  -iname "*.jpg" -o -iname "*.jpeg" -o \
  -iname "*.png" -o -iname "*.gif" -o \
  -iname "*.webp" -o -iname "*.heic" \) | \
while IFS= read -r file; do
  name=$(basename "$file")

  # Separer screenshots
  if echo "$name" | grep -qiE 'screenshot|screen.shot|capture'; then
    dest="${source_path}/Screenshots"
  else
    mod_time=$(stat -c %Y "$file")
    year=$(date -d "@$mod_time" +%Y)
    year_month=$(date -d "@$mod_time" +%Y-%m)
    dest="${source_path}/${year}/${year_month}"
  fi

  # Nouveau nom avec date ISO et numero sequentiel
  mod_time=$(stat -c %Y "$file")
  date_str=$(date -d "@$mod_time" +%Y-%m-%d)
  ext="${name##*.}"
  ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

  counter=1
  while true; do
    new_name=$(printf "%s_%03d.%s" "$date_str" "$counter" "$ext_lower")
    new_path="${dest}/${new_name}"
    [ ! -e "$new_path" ] && break
    counter=$(( counter + 1 ))
  done

  if [ "$(dirname "$file")" != "$dest" ]; then
    mv "$file" "$new_path"
  fi
done

echo "Organisation photos terminee"
```

### Etape 4: Resume

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD ORGANISATION PHOTOS                         ║
║                Etape 4/4 : Termine                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ORGANISATION TERMINEE!                                      ║
║                                                              ║
║  RESUME:                                                     ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Photos organisees    : 12,345                           │ ║
║  │ Photos renommees     : 8,234                            │ ║
║  │ Screenshots separes  : 89                               │ ║
║  │ Dossiers crees       : 96 (8 ans x 12 mois)             │ ║
║  │ Doublons detectes    : 234 (voir rapport)               │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  NOUVELLE STRUCTURE:                                         ║
║  Pictures/                                                   ║
║  ├── 2024/ (3,456 photos)                                    ║
║  ├── 2025/ (2,345 photos)                                    ║
║  ├── 2026/ (456 photos)                                      ║
║  ├── Albums/ (vide - a creer manuellement)                   ║
║  ├── Screenshots/ (89 fichiers)                              ║
║  └── _Import/ (vide)                                         ║
║                                                              ║
║  SUGGESTIONS:                                                ║
║  * Creer des albums dans Albums/ pour evenements             ║
║  * Revoir doublons: /file-duplicates ~/Pictures              ║
║  * Sauvegarder: /file-backup ~/Pictures                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
