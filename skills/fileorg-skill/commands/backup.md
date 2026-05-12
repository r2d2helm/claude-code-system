# Commande: /file-backup

Sauvegarder un dossier avec structure (tar/gz, copie, incremental).

## Syntaxe

```
/file-backup <source> [destination] [options]
```

## Actions

### Backup tar.gz

```bash
#!/usr/bin/env bash
source="${1}"
timestamp=$(date +%Y%m%d-%H%M%S)
name=$(basename "$source")
backup_dir=~/Documents/Backups
zip_path="${backup_dir}/${name}_${timestamp}.tar.gz"

mkdir -p "$backup_dir"

tar czf "$zip_path" -C "$(dirname "$source")" "$(basename "$source")"
size=$(du -sh "$zip_path" | cut -f1)
echo "Backup: $zip_path ($size)"
```

### Backup copie (rsync)

```bash
#!/usr/bin/env bash
source="${1}"
destination="${2}"

rsync -av --delete \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='node_modules' \
  --exclude='*.tmp' \
  "$source/" "$destination/"

echo "Copie miroir: $source -> $destination"
```

### Rotation des backups

```bash
#!/usr/bin/env bash
backup_dir=~/Documents/Backups
name="${1}"
keep_count="${2:-5}"

ls -t "${backup_dir}/${name}_"*.tar.gz 2>/dev/null | \
  tail -n +$(( keep_count + 1 )) | \
  xargs -r rm -f

echo "Rotation: garde $keep_count backups"
```

## Options

| Option | Description |
|--------|-------------|
| `--tar` | Archive tar.gz (defaut) |
| `--copy` | Copie miroir (rsync) |
| `--keep N` | Garder N backups (defaut: 5) |

## Exemples

```bash
/file-backup ~/Documents                       # Backup tar.gz
/file-backup ~/Projets /mnt/backup --copy      # Copie miroir
/file-backup ~/Data --keep 10                  # Garder 10 versions
```

## Voir Aussi

- `/file-sync` - Synchroniser deux dossiers
- `/file-mirror` - Miroir exact
