# Commande: /file-analyze

Analyser structure de fichiers, statistiques et qualite d'organisation.

## Syntaxe

```
/file-analyze [chemin] [mode]
```

## Modes d'Analyse

### /file-analyze [chemin]

Analyse complete d'un dossier :

```
╔══════════════════════════════════════════════════════════════╗
║           ANALYSE: ~/Documents                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  STRUCTURE                                                   ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Dossiers totaux    : 234                                │ ║
║  │ Fichiers totaux    : 4,567                              │ ║
║  │ Taille totale      : 45.6 GB                            │ ║
║  │ Profondeur max     : 7 niveaux                          │ ║
║  │ Dossiers vides     : 23                                 │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  DISTRIBUTION PAR TYPE                                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Documents  : ████████████████████░░░░░░░░ 45% (2,055)   │ ║
║  │ Images     : ██████████░░░░░░░░░░░░░░░░░░ 25% (1,142)   │ ║
║  │ Videos     : █████░░░░░░░░░░░░░░░░░░░░░░░ 12% (548)     │ ║
║  │ Archives   : ███░░░░░░░░░░░░░░░░░░░░░░░░░ 8% (365)      │ ║
║  │ Autres     : ███░░░░░░░░░░░░░░░░░░░░░░░░░ 10% (457)     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  DISTRIBUTION PAR AGE                                        ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ < 1 mois   : ████████░░░░░░░░░░░░░░░░░░░░ 20% (913)     │ ║
║  │ 1-6 mois   : ██████████████░░░░░░░░░░░░░░ 35% (1,599)   │ ║
║  │ 6-12 mois  : ████████░░░░░░░░░░░░░░░░░░░░ 20% (913)     │ ║
║  │ > 1 an     : ██████████░░░░░░░░░░░░░░░░░░ 25% (1,142)   │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  TOP 10 PLUS GROS FICHIERS                                   ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 1. Backup-VM.img               │ 12.5 GB │ 2025-12     │ ║
║  │ 2. Video-Conference.mp4        │ 3.2 GB  │ 2026-01     │ ║
║  │ 3. Archive-2024.tar.gz         │ 2.8 GB  │ 2025-01     │ ║
║  │ ...                                                     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
path="${1:-.}"

# Statistiques de base
total_files=$(find "$path" -type f | wc -l)
total_dirs=$(find "$path" -type d | wc -l)
total_size=$(du -sh "$path" 2>/dev/null | cut -f1)

# Profondeur maximale
max_depth=$(find "$path" -type f | awk -F'/' '{print NF}' | sort -n | tail -1)
base_depth=$(echo "$path" | awk -F'/' '{print NF}')
depth=$((max_depth - base_depth))

# Dossiers vides
empty_dirs=$(find "$path" -type d -empty | wc -l)

# Distribution par extension (top 10)
find "$path" -type f | grep -oE '\.[^./]+$' | sort | uniq -c | sort -rn | head -10

# Plus gros fichiers
find "$path" -type f -printf '%s %p\n' | sort -rn | head -10 | \
  awk '{printf "%.1f MB  %s\n", $1/1048576, $2}'

echo "Fichiers: $total_files | Dossiers: $total_dirs | Taille: $total_size"
echo "Profondeur max: $depth | Dossiers vides: $empty_dirs"
```

### /file-analyze audit [chemin]

Audit qualite du nommage :

```
╔══════════════════════════════════════════════════════════════╗
║           AUDIT QUALITE: Documents                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  SCORE D'ORGANISATION: 62/100                                ║
║     ████████████████████████████░░░░░░░░░░░░░░░░░░           ║
║                                                              ║
║  POINTS POSITIFS                                             ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Pas de fichiers a la racine excessive                   │ ║
║  │ Extensions coherentes                                   │ ║
║  │ Taille moyenne des dossiers acceptable                  │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  PROBLEMES DETECTES                                          ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 156 fichiers sans date ISO (35%)           -15 pts     │ ║
║  │ 89 fichiers avec espaces (20%)             -10 pts     │ ║
║  │ 34 fichiers avec accents (8%)              -5 pts      │ ║
║  │ 23 dossiers vides                          -3 pts      │ ║
║  │ Profondeur > 4 niveaux (7 max)             -5 pts      │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  RECOMMANDATIONS                                             ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 1. /file-rename iso-date . --recursive                  │ ║
║  │ 2. /file-rename normalize .                             │ ║
║  │ 3. /file-empty delete                                   │ ║
║  │ 4. /file-flatten . --max-depth=4                        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
path="${1:-.}"
score=100
issues=()

files=$(find "$path" -type f)
total=$(echo "$files" | wc -l)

# Verifier date ISO (YYYY-MM-DD)
no_date=$(echo "$files" | xargs -I{} basename {} | grep -cv '^\d{4}-\d{2}-\d{2}' || true)
if [ "$no_date" -gt 0 ] && [ "$total" -gt 0 ]; then
  percent=$(( no_date * 100 / total ))
  penalty=$(( percent < 100 ? percent / 4 : 25 ))
  [ "$penalty" -gt 25 ] && penalty=25
  score=$(( score - penalty ))
  issues+=("$no_date fichiers sans date ISO (${percent}%) -${penalty} pts")
fi

# Verifier espaces
with_spaces=$(find "$path" -type f -name "* *" | wc -l)
if [ "$with_spaces" -gt 0 ] && [ "$total" -gt 0 ]; then
  percent=$(( with_spaces * 100 / total ))
  penalty=$(( percent < 45 ? percent / 3 : 15 ))
  score=$(( score - penalty ))
  issues+=("$with_spaces fichiers avec espaces (${percent}%) -${penalty} pts")
fi

# Verifier profondeur
max_depth=$(find "$path" -type f | awk -F'/' '{print NF}' | sort -n | tail -1)
base_depth=$(echo "$path" | awk -F'/' '{print NF}')
depth=$(( max_depth - base_depth ))
if [ "$depth" -gt 4 ]; then
  score=$(( score - 5 ))
  issues+=("Profondeur excessive: $depth niveaux (max recommande: 4) -5 pts")
fi

echo "SCORE D'ORGANISATION: $score/100"
if [ ${#issues[@]} -gt 0 ]; then
  echo "PROBLEMES DETECTES:"
  for issue in "${issues[@]}"; do echo "  $issue"; done
fi
```

### /file-analyze tree [chemin]

Afficher arborescence visuelle :

```
╔══════════════════════════════════════════════════════════════╗
║           ARBORESCENCE: Documents                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Documents/                                     [45.6 GB]   ║
║  ├── _INBOX/                                   [2.3 GB]     ║
║  │   └── 34 fichiers a trier                               ║
║  ├── Administratif/                            [1.2 GB]     ║
║  │   ├── Banque/                    [450 MB]               ║
║  │   ├── Impots/                    [320 MB]               ║
║  │   └── Factures/                  [430 MB]               ║
║  ├── Projets/                                  [28.5 GB]    ║
║  │   ├── MultiPass/                 [12.3 GB]              ║
║  │   ├── ClientA/                   [8.2 GB]               ║
║  │   └── ClientB/                   [8.0 GB]               ║
║  ├── Travail/                                  [8.6 GB]     ║
║  └── Personnel/                                [5.0 GB]     ║
║                                                              ║
║  Legende: [Taille] <100 fichiers 100-500 >500               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
# Utiliser tree si disponible, sinon find
path="${1:-.}"
max_depth="${2:-3}"

if command -v tree &>/dev/null; then
  tree "$path" -d -L "$max_depth" --du -h
else
  find "$path" -maxdepth "$max_depth" -type d | while read -r dir; do
    depth=$(echo "$dir" | awk -F'/' '{print NF}')
    base=$(echo "$path" | awk -F'/' '{print NF}')
    indent=$(printf '%*s' $(( (depth - base) * 2 )) '')
    size=$(du -sh "$dir" 2>/dev/null | cut -f1)
    echo "${indent}$(basename "$dir")/ [$size]"
  done
fi
```

## Rapports

### /file-analyze report [chemin]

Generer rapport complet en Markdown :

```bash
# Generer rapport Markdown
/file-analyze report ~/Documents --format=md

# Generer rapport JSON
/file-analyze report ~/Documents --format=json
```

## Options

| Option | Description |
|--------|-------------|
| `--format=md` | Rapport Markdown |
| `--format=json` | Export JSON |
| `--depth=N` | Profondeur d'analyse |
| `--include-hidden` | Inclure fichiers caches |
