# Commande: /obs-backup

Sauvegarder le vault Obsidian.

## Syntaxe

```
/obs-backup [options]
```

## Comportement

Crée une archive ZIP du vault avec rotation automatique des sauvegardes.

## Script bash

```bash
#!/usr/bin/env bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
BACKUP_DIR="${HOME}/Documents/Backups/Knowledge"
KEEP_DAYS=7
EXCLUDE_OBSIDIAN=false

timestamp=$(date '+%Y-%m-%d_%H%M%S')
archive_name="Knowledge_${timestamp}.zip"

# Creer le dossier backup si necessaire
mkdir -p "$BACKUP_DIR"

archive_path="${BACKUP_DIR}/${archive_name}"

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║     BACKUP DU VAULT                          ║"
echo "╠══════════════════════════════════════════════╣"
echo "║                                              ║"
echo "║  Source:  $VAULT"
echo "║  Dest:    $archive_path"
echo "║                                              ║"

# Compter les fichiers
if [ "$EXCLUDE_OBSIDIAN" = true ]; then
    file_count=$(find "$VAULT" -type f | grep -v '\.obsidian' | wc -l)
else
    file_count=$(find "$VAULT" -type f | wc -l)
fi

total_size=$(du -sm "$VAULT" | awk '{print $1}')

echo "║  Fichiers: $file_count"
echo "║  Taille:   ${total_size} MB"
echo "║                                              ║"
echo "║  Compression en cours...                     ║"

# Creer l'archive
if [ "$EXCLUDE_OBSIDIAN" = true ]; then
    find "$VAULT" -type f | grep -v '\.obsidian' | \
        zip -@ "$archive_path" > /dev/null
else
    zip -r "$archive_path" "$VAULT" > /dev/null
fi

archive_size=$(du -sm "$archive_path" | awk '{print $1}')
echo "║  Archive creee: ${archive_size} MB"
echo "║                                              ║"

# Rotation: supprimer les anciennes sauvegardes
old_count=$(ls -t "${BACKUP_DIR}/Knowledge_"*.zip 2>/dev/null | tail -n +$((KEEP_DAYS + 1)) | wc -l)
if [ "$old_count" -gt 0 ]; then
    ls -t "${BACKUP_DIR}/Knowledge_"*.zip | tail -n +$((KEEP_DAYS + 1)) | xargs rm -f
    echo "║  Rotation: $old_count anciens backups supprimes"
else
    echo "║  Rotation: rien a supprimer"
fi

# Lister les backups existants
echo "║                                              ║"
backup_count=$(ls "${BACKUP_DIR}/Knowledge_"*.zip 2>/dev/null | wc -l)
echo "║  Backups disponibles: $backup_count"
ls -t "${BACKUP_DIR}/Knowledge_"*.zip 2>/dev/null | head -5 | while read -r b; do
    bname=$(basename "$b")
    bsize=$(du -sm "$b" | awk '{print $1}')
    echo "║    - $bname ($bsize MB)"
done

echo "║                                              ║"
echo "╚══════════════════════════════════════════════╝"
```

## Options

| Option | Description |
|--------|-------------|
| `--dest=path` | Destination personnalisée |
| `--keep=N` | Nombre de backups à garder (défaut: 7) |
| `--exclude-obsidian` | Exclure le dossier .obsidian |
| `--incremental` | Backup incrémental (fichiers modifiés uniquement) |

## Exemples

```bash
# Backup standard
/obs-backup

# Backup vers un autre emplacement
/obs-backup --dest="$HOME/Backups/Knowledge"

# Garder 14 jours
/obs-backup --keep=14

# Sans config Obsidian
/obs-backup --exclude-obsidian
```
