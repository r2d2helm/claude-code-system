# Commande: /file-normalize

Normaliser les noms de fichiers (espaces, accents, caracteres speciaux).

## Syntaxe

```
/file-normalize <chemin> [options]
```

## Actions

### Normaliser les noms

```bash
#!/usr/bin/env bash
path="${1}"
dry_run="${2:-}"
modified=0

while IFS= read -r -d '' file; do
  dir=$(dirname "$file")
  name=$(basename "$file")
  ext="${name##*.}"
  base="${name%.*}"

  new_name="$base"
  # Remplacer espaces par tirets
  new_name=$(echo "$new_name" | tr ' ' '-')
  # Remplacer accents courants
  new_name=$(echo "$new_name" | sed \
    -e 's/[àâä]/a/g' -e 's/[éèêë]/e/g' \
    -e 's/[îï]/i/g' -e 's/[ôö]/o/g' \
    -e 's/[ùûü]/u/g' -e 's/ç/c/g' \
    -e 's/[ÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ]/\L&/g')
  # Supprimer caracteres speciaux
  new_name=$(echo "$new_name" | tr -cd '[:alnum:]_.-')
  # Supprimer tirets multiples
  new_name=$(echo "$new_name" | sed 's/-\{2,\}/-/g' | sed 's/^-//' | sed 's/-$//')

  new_file="${dir}/${new_name}.${ext}"
  if [ "$new_file" != "$file" ]; then
    if [ "${dry_run}" = "--dry-run" ]; then
      echo "  $(basename "$file") -> ${new_name}.${ext}"
    else
      mv "$file" "$new_file"
      echo "  $(basename "$file") -> ${new_name}.${ext}"
    fi
    modified=$(( modified + 1 ))
  fi
done < <(find "$path" -maxdepth 1 -type f -print0)

echo "$modified fichiers normalises"
```

### Regles de normalisation

| Avant | Apres | Regle |
|-------|-------|-------|
| `Mon Fichier.pdf` | `Mon-Fichier.pdf` | Espaces -> tirets |
| `Resume ete.doc` | `Resume-ete.doc` | Accents supprimes |
| `file@#$.txt` | `file.txt` | Caracteres speciaux supprimes |
| `a--b--c.md` | `a-b-c.md` | Tirets multiples reduits |

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview sans renommer |
| `--recursive` | Inclure sous-dossiers |
| `--rules` | Afficher les regles actives |

## Exemples

```bash
/file-normalize ~/Downloads            # Normaliser
/file-normalize ~/Documents --dry-run  # Preview
/file-normalize . --recursive          # Recursif
```

## Voir Aussi

- `/file-prefix` - Ajouter prefixe date
- `/file-rename` - Renommer selon convention
