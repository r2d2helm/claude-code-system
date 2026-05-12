# Commande: /obs-rename

Renommer une note selon les conventions du vault et mettre a jour les backlinks.

## Syntaxe

```
/obs-rename <note> <new-name> [options]
```

## Actions

### Renommer avec mise a jour des backlinks

```bash
#!/usr/bin/env bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
old_name="$1"
new_name="$2"

# Trouver la note
note_file=$(find "$VAULT" -name "${old_name}.md" -type f | head -1)
if [ -z "$note_file" ]; then
    echo "Erreur: Note '$old_name' non trouvee"
    exit 1
fi

note_dir=$(dirname "$note_file")
new_path="${note_dir}/${new_name}.md"

# Renommer le fichier
mv "$note_file" "$new_path"

# Mettre a jour tous les backlinks dans le vault
updated=0
while IFS= read -r note; do
    if grep -qF "[[$old_name" "$note"; then
        sed -i "s/\[\[$old_name\]\]/[[$new_name]]/g" "$note"
        sed -i "s/\[\[$old_name|/[[$new_name|/g" "$note"
        updated=$((updated + 1))
    fi
done < <(find "$VAULT" -name "*.md" -type f)

echo "Renomme: $old_name -> $new_name ($updated backlinks mis a jour)"
```

### Conventions de nommage

| Type | Format | Exemple |
|------|--------|---------|
| Concept | `C_Name` | `C_Docker-Compose` |
| Conversation | `YYYY-MM-DD_Conv_Description` | `2026-02-11_Conv_Audit-Skills` |
| Daily | `YYYY-MM-DD` | `2026-02-11` |
| Troubleshooting | `YYYY-MM-DD_Fix_Description` | `2026-02-11_Fix_Path-Guard` |

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Afficher sans renommer |
| `--convention` | Appliquer convention automatiquement |

## Exemples

```bash
/obs-rename Docker C_Docker                    # Ajouter prefixe concept
/obs-rename old-note 2026-02-11_Conv_Session   # Convention conversation
/obs-rename MyNote C_MyNote --dry-run          # Preview
```

## Voir Aussi

- `/obs-move` - Deplacer une note
- `/obs-frontmatter` - Gerer les metadonnees
