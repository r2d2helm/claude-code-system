# Commande: /obs-config

Gerer la configuration Obsidian (.obsidian/).

## Syntaxe

```
/obs-config [action] [options]
```

## Actions

### Afficher la configuration

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
config_path="${VAULT}/.obsidian"

# Fichiers de config
find "$config_path" -name "*.json" -type f | while read -r f; do
    name=$(basename "$f")
    size=$(du -k "$f" | awk '{printf "%.1f", $1}')
    modified=$(date -r "$f" '+%Y-%m-%d')
    printf "%-30s %6s KB   %s\n" "$name" "$size" "$modified"
done | column -t
```

### Lire un parametre

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
config_path="${VAULT}/.obsidian"

theme=$(python3 -c "import json,sys; d=json.load(open('${config_path}/app.json')); print(d.get('theme',''))" 2>/dev/null)
spellcheck=$(python3 -c "import json,sys; d=json.load(open('${config_path}/app.json')); print(d.get('spellcheck',''))" 2>/dev/null)
echo "Theme: $theme"
echo "Spell check: $spellcheck"
```

### Backup de la configuration

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
backup_path="${HOME}/Documents/Backups/obsidian-config"
config_path="${VAULT}/.obsidian"

mkdir -p "$backup_path"
cp "${config_path}/"*.json "$backup_path/"
echo "Config sauvegardee dans $backup_path"
```

## Options

| Option | Description |
|--------|-------------|
| `show` | Afficher la configuration |
| `get <key>` | Lire un parametre |
| `backup` | Sauvegarder la config |
| `restore` | Restaurer depuis backup |

## Exemples

```bash
/obs-config show              # Liste des fichiers config
/obs-config backup            # Backup de la config
/obs-config restore           # Restaurer la config
```

## Voir Aussi

- `/obs-plugins` - Gerer les plugins
- `/obs-hotkeys` - Gerer les raccourcis
