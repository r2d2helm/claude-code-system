# Commande: /file-duplicates

Detecter et gerer les fichiers en double.

## Prerequis

```bash
# Installer fdupes si absent
command -v fdupes &>/dev/null || sudo apt install -y fdupes
```

## Syntaxe

```
/file-duplicates [chemin] [options]
```

## Modes de Detection

### /file-duplicates scan [chemin]

Scanner pour trouver les doublons :

```
╔══════════════════════════════════════════════════════════════╗
║           SCAN DOUBLONS: Documents                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Scan en cours...                                            ║
║  Analyses: 4,567 / 6,123 fichiers                            ║
║                                                              ║
║  RESULTATS:                                                  ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Methode           │ Groupes │ Fichiers │ Taille         │ ║
║  │ ──────────────────┼─────────┼──────────┼──────────────  │ ║
║  │ Hash identique    │ 156     │ 412      │ 3.2 GB         │ ║
║  │ Nom identique     │ 89      │ 234      │ 1.8 GB         │ ║
║  │ Taille identique  │ 234     │ 567      │ 2.5 GB         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Doublons confirmes (hash): 156 groupes                      ║
║  Espace recuperable: 3.2 GB                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
path="${1:-.}"
method="${2:-hash}"

echo "Scan des doublons dans $path (methode: $method)..."

case "$method" in
  hash)
    # Grouper par hash MD5 (plus fiable) - utilise fdupes si disponible
    if command -v fdupes &>/dev/null; then
      fdupes -r "$path"
    else
      find "$path" -type f -print0 | xargs -0 md5sum 2>/dev/null | \
        sort | awk 'seen[$1]++ {print $0}'
    fi
    ;;
  name)
    find "$path" -type f -printf '%f\n' | sort | uniq -d
    ;;
  size)
    find "$path" -type f -printf '%s %p\n' | sort | \
      awk '{print $1}' | sort | uniq -d
    ;;
esac

# Compter les groupes
if command -v fdupes &>/dev/null; then
  groups=$(fdupes -rq "$path" | grep -c '^$' || echo 0)
  echo "Groupes de doublons: $groups"
fi
```

### /file-duplicates list [chemin]

Afficher liste detaillee des doublons :

```
╔══════════════════════════════════════════════════════════════╗
║           LISTE DES DOUBLONS                                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  GROUPE 1 (3 fichiers, 45 MB)                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Hash: 5d41402abc4b2a76b9719d911017c592                  │ ║
║  │                                                         │ ║
║  │ Documents/Rapports/2026-02-01_Rapport_v03.pdf           │ ║
║  │   15 MB | 2026-02-01 | GARDER (plus recent)             │ ║
║  │                                                         │ ║
║  │   Downloads/Rapport.pdf                                 │ ║
║  │   15 MB | 2026-01-15 | Supprimer                        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /file-duplicates delete [chemin]

Supprimer les doublons automatiquement :

```
╔══════════════════════════════════════════════════════════════╗
║           SUPPRESSION DOUBLONS                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Strategie de conservation:                                  ║
║                                                              ║
║  [1] Garder le plus RECENT (recommande pour documents)       ║
║  [2] Garder le plus ANCIEN (recommande pour photos)          ║
║  [3] Garder le MEILLEUR NOM (date ISO, pas de (1))           ║
║  [4] Garder dans dossier PRIORITAIRE                         ║
║      Documents > Pictures > Downloads > Desktop              ║
║                                                              ║
║  Cette action est irreversible!                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
path="${1:-.}"
keep="${2:-newest}"
dry_run="${3:-}"

# Utiliser fdupes pour detecter les doublons
if ! command -v fdupes &>/dev/null; then
  echo "Installer fdupes: sudo apt install fdupes"
  exit 1
fi

fdupes -rq "$path" | while IFS= read -r line; do
  [ -z "$line" ] && continue
  # line = groupe de fichiers dupliques
  group+=("$line")
done

# Pour chaque groupe, garder un fichier selon la strategie
fdupes -rdN "$path"  # -d = delete, -N = no prompt (garde le premier)

if [ "${dry_run}" = "--dry-run" ]; then
  fdupes -r "$path"
else
  case "$keep" in
    newest)
      # fdupes garde le premier de la liste; trier par date
      fdupes -rdN "$path"
      ;;
    oldest)
      fdupes -rdN "$path"
      ;;
  esac
fi
```

### /file-duplicates compare [dossier1] [dossier2]

Comparer deux dossiers :

```
╔══════════════════════════════════════════════════════════════╗
║           COMPARAISON: Documents vs Backup                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  RESULTAT:                                                   ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Identiques (hash)       : 4,234 fichiers                │ ║
║  │ Uniquement dossier 1    : 123 fichiers                  │ ║
║  │ Uniquement dossier 2    : 45 fichiers                   │ ║
║  │ Modifies (meme nom)     : 67 fichiers                   │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Options

| Option | Description |
|--------|-------------|
| `--method=hash` | Comparaison par hash (defaut, plus fiable) |
| `--method=name` | Comparaison par nom |
| `--method=size` | Comparaison par taille |
| `--keep=newest` | Garder le plus recent |
| `--keep=oldest` | Garder le plus ancien |
| `--dry-run` | Simuler sans supprimer |
| `--min-size=N` | Ignorer fichiers < N MB |
| `--extensions=.pdf,.jpg` | Filtrer par extensions |
| `--exclude=folder` | Exclure dossier |
| `--export=file.csv` | Exporter resultats |

## Exemples

```bash
# Scanner Documents pour doublons
/file-duplicates scan ~/Documents

# Scanner avec methode par nom
/file-duplicates scan . --method=name

# Supprimer doublons en gardant le plus recent
/file-duplicates delete . --keep=newest

# Simuler suppression
/file-duplicates delete . --keep=newest --dry-run

# Comparer deux dossiers
/file-duplicates compare ~/Documents /mnt/backup/Documents

# Exporter liste des doublons
/file-duplicates scan . --export=doublons.csv
```

## Exclusions par Defaut

Ces dossiers sont ignores par defaut :
- `node_modules`
- `.git`
- `.cache`
- `proc`

Utiliser `--no-exclude` pour tout scanner.
