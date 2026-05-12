# Commande: /obs-templates

Gerer les templates du vault (_Templates/).

## Syntaxe

```
/obs-templates [action] [options]
```

## Actions

### Lister les templates

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
template_path="${VAULT}/_Templates"

find "$template_path" -name "*.md" -type f | while IFS= read -r tmpl; do
    name=$(basename "$tmpl" .md)
    lines=$(wc -l < "$tmpl")
    printf "%-35s %d lignes\n" "$name" "$lines"
done | column -t
```

### Valider les templates

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
template_path="${VAULT}/_Templates"

# Verifier que chaque template a un frontmatter valide
find "$template_path" -name "*.md" -type f | while IFS= read -r tmpl; do
    name=$(basename "$tmpl" .md)
    if head -1 "$tmpl" | grep -q '^---'; then
        echo "OK: $name"
    else
        echo "MANQUANT: $name"
    fi
done | column -t
```

### Appliquer un template a une note

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
template_path="${VAULT}/_Templates"
note_name="$1"
template_name="${2:-Template-Concept}"

template=$(< "${template_path}/${template_name}.md")
today=$(date '+%Y-%m-%d')

# Remplacer les variables
new_note="${template//\{\{title\}\}/$note_name}"
new_note="${new_note//\{\{date\}\}/$today}"

echo "$new_note" > "${VAULT}/_Inbox/${note_name}.md"
echo "Note creee depuis template: ${note_name}.md"
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister les templates disponibles |
| `validate` | Verifier la validite des templates |
| `apply` | Appliquer un template a une note |
| `create` | Creer un nouveau template |

## Exemples

```bash
/obs-templates list                    # Lister les templates
/obs-templates validate                # Verifier tous les templates
/obs-templates apply Concept MyNote    # Creer note depuis template
```

## Voir Aussi

- `/obs-frontmatter` - Gerer les metadonnees
- `/obs-structure` - Structure du vault
