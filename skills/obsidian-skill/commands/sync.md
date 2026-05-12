# Commande: /obs-sync

Synchroniser le vault avec un backup ou un depot Git.

## Syntaxe

```
/obs-sync [mode] [options]
```

## Actions

### Sync Git

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"

# Status
git -C "$VAULT" status --short

# Commit et push
git -C "$VAULT" add -A
git -C "$VAULT" commit -m "vault: sync $(date '+%Y-%m-%d %H:%M')"
git -C "$VAULT" push
```

### Sync backup (ZIP)

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
backup_dir="${HOME}/Documents/Backups/Knowledge"
timestamp=$(date '+%Y%m%d-%H%M%S')
zip_path="${backup_dir}/Knowledge_${timestamp}.zip"

mkdir -p "$backup_dir"

zip -r "$zip_path" "$VAULT" > /dev/null
echo "Backup: $zip_path"

# Rotation : garder les 5 derniers
ls -t "${backup_dir}/Knowledge_"*.zip 2>/dev/null | tail -n +6 | xargs rm -f
```

### Comparer deux vaults

```bash
source="${VAULT}"
target="$HOME/Backup/Knowledge"

# Fichiers differents
echo "=== Fichiers dans source mais pas dans target ==="
diff <(find "$source" -name "*.md" -type f | xargs -I{} basename {} | sort) \
     <(find "$target" -name "*.md" -type f | xargs -I{} basename {} | sort) | grep '^<'

echo "=== Fichiers dans target mais pas dans source ==="
diff <(find "$source" -name "*.md" -type f | xargs -I{} basename {} | sort) \
     <(find "$target" -name "*.md" -type f | xargs -I{} basename {} | sort) | grep '^>'
```

## Options

| Option | Description |
|--------|-------------|
| `git` | Commit et push Git |
| `backup` | Creer un backup ZIP |
| `compare` | Comparer avec un backup |
| `--message` | Message de commit personnalise |

## Exemples

```bash
/obs-sync git                              # Commit + push
/obs-sync backup                           # Backup ZIP
/obs-sync compare $HOME/Backup/Knowledge   # Comparer
```

## Voir Aussi

- `/obs-backup` - Backup complet
- `/obs-export` - Export en differents formats
