# Commande: /obs-plugins

Gerer les plugins community Obsidian.

## Syntaxe

```
/obs-plugins [action] [options]
```

## Actions

### Lister les plugins installes

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
plugins_path="${VAULT}/.obsidian/plugins"

echo "Plugins installes:"
find "$plugins_path" -maxdepth 1 -type d | tail -n +2 | while IFS= read -r plugin_dir; do
    manifest="${plugin_dir}/manifest.json"
    if [ -f "$manifest" ]; then
        name=$(python3 -c "import json; d=json.load(open('$manifest')); print(d.get('name',''))" 2>/dev/null)
        version=$(python3 -c "import json; d=json.load(open('$manifest')); print(d.get('version',''))" 2>/dev/null)
        id=$(python3 -c "import json; d=json.load(open('$manifest')); print(d.get('id',''))" 2>/dev/null)
        author=$(python3 -c "import json; d=json.load(open('$manifest')); print(d.get('author',''))" 2>/dev/null)
        printf "%-35s %-10s %-30s %s\n" "$name" "$version" "$id" "$author"
    fi
done | sort | column -t
```

### Verifier les plugins actifs

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
community_file="${VAULT}/.obsidian/community-plugins.json"

count=$(python3 -c "import json; d=json.load(open('$community_file')); print(len(d))" 2>/dev/null)
echo "Plugins actifs: $count"
python3 -c "
import json
with open('$community_file') as f:
    for p in json.load(f):
        print(f'  - {p}')
" 2>/dev/null
```

### Informations sur un plugin

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
plugins_path="${VAULT}/.obsidian/plugins"
plugin_id="$1"

manifest="${plugins_path}/${plugin_id}/manifest.json"
data_file="${plugins_path}/${plugin_id}/data.json"

python3 -c "
import json, os
d = json.load(open('$manifest'))
print(f'Plugin: {d[\"name\"]} v{d[\"version\"]}')
print(f'Auteur: {d[\"author\"]}')
print(f'Description: {d.get(\"description\", \"\")}')
print(f'Config: {\"Oui\" if os.path.exists(\"$data_file\") else \"Non\"}')
"
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister les plugins |
| `active` | Plugins actifs uniquement |
| `info <id>` | Details d'un plugin |
| `disable <id>` | Desactiver un plugin |
| `enable <id>` | Activer un plugin |

## Exemples

```bash
/obs-plugins list                 # Tous les plugins
/obs-plugins active               # Plugins actifs
/obs-plugins info dataview        # Info sur Dataview
```

## Voir Aussi

- `/obs-config` - Configuration Obsidian
- `/obs-hotkeys` - Raccourcis clavier
