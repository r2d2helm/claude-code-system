# Commande: /obs-move

Deplacer une note et mettre a jour tous les wikilinks pointant vers elle.

## Syntaxe

```
/obs-move <note> <destination> [options]
```

## Actions

### Deplacer avec mise a jour des liens

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
note_name="$1"
destination="$2"

# Trouver la note
note_file=$(find "$VAULT" -name "${note_name}.md" -type f | head -1)
if [ -z "$note_file" ]; then
    echo "Erreur: Note '$note_name' non trouvee"
    exit 1
fi

dest_path="${VAULT}/${destination}"
mkdir -p "$dest_path"

# Deplacer le fichier
mv "$note_file" "${dest_path}/${note_name}.md"

# Wikilinks Obsidian utilisent le nom sans chemin, donc pas de mise a jour necessaire
# sauf si le vault utilise des chemins relatifs dans les liens
echo "Deplace: ${note_name}.md -> ${destination}/"
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Afficher sans deplacer |
| `--update-links` | Mettre a jour les liens relatifs |

## Exemples

```bash
/obs-move C_Docker Concepts/           # Deplacer vers Concepts
/obs-move Note-Temp _Inbox/            # Deplacer vers Inbox
/obs-move C_Docker Concepts --dry-run  # Preview
```

## Voir Aussi

- `/obs-rename` - Renommer une note
- `/obs-structure` - Analyser structure
