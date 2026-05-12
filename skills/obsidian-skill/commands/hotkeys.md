# Commande: /obs-hotkeys

Gerer les raccourcis clavier Obsidian.

## Syntaxe

```
/obs-hotkeys [action] [options]
```

## Actions

### Lister les raccourcis personnalises

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
hotkeys_file="${VAULT}/.obsidian/hotkeys.json"

if [ -f "$hotkeys_file" ]; then
    python3 -c "
import json
data = json.load(open('${hotkeys_file}'))
for cmd, bindings in data.items():
    shortcuts = []
    for b in bindings:
        parts = b.get('modifiers', []) + [b.get('key', '')]
        shortcuts.append('+'.join(parts))
    print(f'{cmd:50s}  {\" / \".join(shortcuts)}')
" | column -t
else
    echo "Aucun raccourci personnalise"
fi
```

### Raccourcis par defaut utiles

| Raccourci | Action |
|-----------|--------|
| Ctrl+N | Nouvelle note |
| Ctrl+O | Ouvrir note (quick switcher) |
| Ctrl+P | Palette de commandes |
| Ctrl+E | Basculer edition/lecture |
| Ctrl+K | Inserer lien |
| Ctrl+Shift+F | Recherche globale |
| Ctrl+G | Ouvrir le graphe |

### Detecter les conflits

```bash
VAULT="${KNOWLEDGE_VAULT_PATH:-$HOME/Documents/Knowledge}"
hotkeys_file="${VAULT}/.obsidian/hotkeys.json"

python3 -c "
import json
data = json.load(open('${hotkeys_file}'))
seen = {}
for cmd, bindings in data.items():
    for b in bindings:
        key = b.get('key', '')
        if key in seen:
            print(f'CONFLIT: {key} -> {seen[key]} vs {cmd}')
        seen[key] = cmd
"
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister les raccourcis personnalises |
| `defaults` | Raccourcis par defaut |
| `conflicts` | Detecter les conflits |
| `search <key>` | Chercher un raccourci |

## Exemples

```bash
/obs-hotkeys list              # Raccourcis personnalises
/obs-hotkeys defaults          # Raccourcis par defaut
/obs-hotkeys conflicts         # Conflits de raccourcis
/obs-hotkeys search Ctrl+G     # Chercher un raccourci
```

## Voir Aussi

- `/obs-config` - Configuration Obsidian
- `/obs-plugins` - Gerer les plugins
