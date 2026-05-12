# Commande: /file-mirror

Creer un miroir exact d'un dossier (copie parfaite, supprime les extras).

## Syntaxe

```
/file-mirror <source> <destination> [options]
```

## Actions

### Preview (dry-run)

```bash
#!/usr/bin/env bash
source="${1}"
dest="${2}"

# Simuler le miroir sans modifier
echo "PREVIEW miroir: $source -> $dest"

new=$(rsync -avnc --delete \
  --exclude='.git' \
  --exclude='node_modules' \
  --exclude='__pycache__' \
  "$source/" "$dest/" 2>/dev/null | grep '^>' | wc -l)

deleted=$(rsync -avnc --delete \
  --exclude='.git' \
  --exclude='node_modules' \
  "$source/" "$dest/" 2>/dev/null | grep '^*deleting' | wc -l)

echo "  Fichiers a copier: $new"
echo "  Fichiers a supprimer (extras): $deleted"
echo ""
echo "Utiliser --confirm pour executer"
```

### Miroir exact

```bash
#!/usr/bin/env bash
source="${1}"
dest="${2}"

mkdir -p "$dest"

rsync -av --delete \
  --exclude='.git' \
  --exclude='node_modules' \
  --exclude='__pycache__' \
  --exclude='.venv' \
  --exclude='*.tmp' \
  "$source/" "$dest/"

echo "Miroir termine: $source -> $dest"
```

### Miroir avec exclusions

```bash
#!/usr/bin/env bash
source="${1}"
dest="${2}"

exclude_dirs=('.git' 'node_modules' '__pycache__' '.venv' '.tox')
exclude_files=('*.tmp' '*.log' '*.bak')

rsync_args=(-av --delete)
for d in "${exclude_dirs[@]}"; do rsync_args+=(--exclude="$d/"); done
for f in "${exclude_files[@]}"; do rsync_args+=(--exclude="$f"); done

rsync "${rsync_args[@]}" "$source/" "$dest/"
echo "Miroir (avec exclusions): $source -> $dest"
```

## Options

| Option | Description |
|--------|-------------|
| `--preview` | Simuler sans modifier (dry-run) |
| `--confirm` | Executer le miroir |
| `--exclude` | Patterns supplementaires a exclure |
| `--log` | Ecrire un log dans le dossier destination |

## Exemples

```bash
/file-mirror ~/Projets /mnt/mirror/Projets --preview   # Preview
/file-mirror ~/Projets /mnt/mirror/Projets --confirm    # Executer
/file-mirror ~/Data /mnt/mirror --exclude "*.log"       # Avec exclusions
```

## Voir Aussi

- `/file-sync` - Synchronisation bidirectionnelle
- `/file-backup` - Sauvegarde avec rotation
