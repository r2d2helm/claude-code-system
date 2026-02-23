# Commande: /know-backup

Sauvegarder la base de connaissances sous forme d'archive compressée.

## Syntaxe

```
/know-backup [options]
```

## Description

Crée une archive tar.gz horodatée de l'intégralité du vault ~/Documents/Knowledge. Vérifie l'intégrité de l'archive après création et conserve un historique des sauvegardes. Recommandé après chaque revue hebdomadaire.

## Options

| Option | Description |
|--------|-------------|
| `--dest=PATH` | Répertoire de destination (défaut: ~/Backups/Knowledge/) |
| `--name=NOM` | Nom personnalisé de l'archive |
| `--keep=N` | Nombre de backups à conserver (défaut: 5, rotation) |
| `--dry-run` | Afficher ce qui serait sauvegardé sans créer l'archive |
| `--exclude=PATTERN` | Exclure des fichiers (ex: `.obsidian`, `.git`) |
| `--verify` | Vérifier l'intégrité après création |

## Exemples

### Backup standard

```bash
#!/usr/bin/env bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
BACKUP_DIR="${1:-$HOME/Backups/Knowledge}"
DATE=$(date +%Y-%m-%d_%H%M%S)
ARCHIVE_NAME="knowledge-backup_${DATE}.tar.gz"

mkdir -p "$BACKUP_DIR"

# Créer l'archive
tar -czf "$BACKUP_DIR/$ARCHIVE_NAME" \
    --exclude='.obsidian/workspace.json' \
    --exclude='.git' \
    -C "$(dirname "$KNOWLEDGE_PATH")" \
    "$(basename "$KNOWLEDGE_PATH")"

echo "Archive créée: $BACKUP_DIR/$ARCHIVE_NAME"
echo "Taille: $(du -sh "$BACKUP_DIR/$ARCHIVE_NAME" | cut -f1)"
```

### Vérification d'intégrité

```bash
# Vérifier que l'archive est lisible
tar -tzf "$BACKUP_DIR/$ARCHIVE_NAME" > /dev/null 2>&1 && \
    echo "Intégrité OK" || echo "ERREUR: archive corrompue"

# Compter les fichiers dans l'archive
echo "Fichiers archivés: $(tar -tzf "$BACKUP_DIR/$ARCHIVE_NAME" | wc -l)"
```

### Rotation des anciens backups

```bash
KEEP=5
# Supprimer les backups les plus anciens au-delà de $KEEP
ls -1t "$BACKUP_DIR"/knowledge-backup_*.tar.gz 2>/dev/null | \
    tail -n +$((KEEP + 1)) | xargs -r rm -v
```

### Dry-run

```bash
# Afficher la taille estimée et le nombre de fichiers
echo "Fichiers à sauvegarder:"
find "$KNOWLEDGE_PATH" -type f -not -path '*/.git/*' | wc -l
echo "Taille totale:"
du -sh "$KNOWLEDGE_PATH" --exclude='.git'
```

## Notes

- La destination par défaut `~/Backups/Knowledge/` est créée automatiquement si absente.
- Exclure `.obsidian/workspace.json` évite les conflits de session Obsidian.
- La rotation par défaut conserve les 5 dernières archives.
- Pour un backup vers un disque externe, utiliser `--dest=/media/user/externe/backups`.
- Compléter avec `/know-export json` pour un export structuré portable.
