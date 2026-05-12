# Commande: /file-sync

Synchroniser deux dossiers (bidirectionnel).

## Syntaxe

```
/file-sync <source> <destination> [options]
```

## Actions

### Preview des differences

```bash
#!/usr/bin/env bash
source="${1}"
dest="${2}"

# Utiliser rsync en mode dry-run pour comparer
echo "PREVIEW sync: $source -> $dest"

rsync -avnc --delete \
  --exclude='.git' \
  --exclude='node_modules' \
  "$source/" "$dest/" 2>/dev/null | grep -E '^(>|<|\*)'

only_in_source=$(rsync -avnc "$source/" "$dest/" 2>/dev/null | grep '^>' | wc -l)
only_in_dest=$(rsync -avnc "$dest/" "$source/" 2>/dev/null | grep '^>' | wc -l)

echo "Uniquement dans source: $only_in_source"
echo "Uniquement dans destination: $only_in_dest"
```

### Synchroniser (source -> destination)

```bash
#!/usr/bin/env bash
source="${1}"
dest="${2}"

rsync -av \
  --exclude='.git' \
  --exclude='node_modules' \
  "$source/" "$dest/"

echo "Synchronise: $source -> $dest"
```

### Synchroniser bidirectionnel

```bash
#!/usr/bin/env bash
source="${1}"
dest="${2}"

# Source -> Dest (fichiers nouveaux/modifies)
rsync -av --update \
  --exclude='.git' \
  "$source/" "$dest/"

# Dest -> Source (fichiers uniquement dans dest)
rsync -av --update \
  --exclude='.git' \
  "$dest/" "$source/"

echo "Synchronisation bidirectionnelle terminee"
```

## Options

| Option | Description |
|--------|-------------|
| `--preview` | Afficher sans synchroniser |
| `--one-way` | Source -> Dest uniquement |
| `--two-way` | Bidirectionnel (defaut) |
| `--exclude` | Patterns a exclure |

## Exemples

```bash
/file-sync ~/Projets /mnt/backup --preview    # Preview
/file-sync ~/Projets /mnt/backup --one-way    # Unidirectionnel
/file-sync ~/Data /mnt/mirror                 # Bidirectionnel
```

## Voir Aussi

- `/file-mirror` - Miroir exact
- `/file-backup` - Sauvegarde
