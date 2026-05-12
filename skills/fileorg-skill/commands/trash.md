# Commande: /file-trash

Gerer la corbeille Linux (trash-cli).

## Syntaxe

```
/file-trash [action] [options]
```

## Actions

### Taille de la corbeille

```bash
#!/usr/bin/env bash
trash_dir="$HOME/.local/share/Trash"

count=$(find "${trash_dir}/files" -type f 2>/dev/null | wc -l)
size=$(du -sh "${trash_dir}/files" 2>/dev/null | cut -f1)

echo "Corbeille: $count elements"
echo "Taille: $size"
```

### Lister le contenu

```bash
#!/usr/bin/env bash
# Utiliser trash-cli si disponible
if command -v trash-list &>/dev/null; then
  trash-list | column -t
else
  ls -lh ~/.local/share/Trash/files/ | column -t
fi
```

### Vider la corbeille

```bash
#!/usr/bin/env bash
# Avec trash-cli
if command -v trash-empty &>/dev/null; then
  trash-empty
else
  rm -rf ~/.local/share/Trash/files/*
  rm -rf ~/.local/share/Trash/info/*
fi
echo "Corbeille videe"
```

### Envoyer en corbeille (au lieu de rm)

```bash
# Installer trash-cli : sudo apt install trash-cli
# Puis utiliser trash-put au lieu de rm
trash-put fichier.txt
trash-put ~/Downloads/ancien-fichier.zip
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister le contenu |
| `size` | Taille de la corbeille |
| `empty` | Vider la corbeille |
| `restore` | Restaurer un element (trash-restore) |

## Exemples

```bash
/file-trash size           # Taille
/file-trash list           # Contenu
/file-trash empty          # Vider
trash-empty 30             # Vider elements > 30 jours
```

## Installation trash-cli

```bash
sudo apt install trash-cli
```

## Voir Aussi

- `/file-clean` - Nettoyer fichiers temporaires
- `/file-old` - Fichiers anciens
