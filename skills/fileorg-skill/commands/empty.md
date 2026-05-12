# Commande: /file-empty

Trouver et supprimer les dossiers vides.

## Syntaxe

```
/file-empty [chemin] [action]
```

## Actions

### /file-empty [chemin]

Lister les dossiers vides :

```bash
#!/usr/bin/env bash
path="${1:-.}"
delete="${2:-}"
dry_run="${3:-}"

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║     DOSSIERS VIDES                            ║"
echo "╠══════════════════════════════════════════════╣"
echo "║                                              ║"

# Trouver les dossiers vides (recursivement, du plus profond)
# find -empty detecte les dossiers sans contenu
mapfile -t empty_folders < <(find "$path" -type d -empty 2>/dev/null | sort -r)

echo "║  Trouves: ${#empty_folders[@]} dossiers vides"
echo "║                                              ║"

count=0
for folder in "${empty_folders[@]}"; do
  [ $count -ge 20 ] && break
  rel="${folder#"$path"/}"
  if [ "${delete}" = "delete" ] && [ "${dry_run}" != "--dry-run" ]; then
    rmdir "$folder" 2>/dev/null && echo "║  Supprime: $rel"
  elif [ "${dry_run}" = "--dry-run" ]; then
    echo "║  [DRY RUN] $rel"
  else
    echo "║  $rel"
  fi
  count=$(( count + 1 ))
done

remaining=$(( ${#empty_folders[@]} - count ))
[ "$remaining" -gt 0 ] && echo "║  ... et $remaining de plus"

echo "║                                              ║"
if [ "${delete}" != "delete" ]; then
  echo "║  -> Utiliser /file-empty delete pour supprimer"
fi
echo "╚══════════════════════════════════════════════╝"
```

## Options

| Option | Description |
|--------|-------------|
| `delete` | Supprimer les dossiers vides |
| `--dry-run` | Simuler la suppression |
| `--include-hidden` | Inclure dossiers caches |

## Exemples

```bash
# Lister les dossiers vides
/file-empty Documents

# Supprimer les dossiers vides (dry run)
/file-empty Documents delete --dry-run

# Supprimer pour de vrai
/file-empty Documents delete
```
