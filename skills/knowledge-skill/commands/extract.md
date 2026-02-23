# Commande: /know-extract

Extraire des éléments clés d'une conversation ou d'un fichier.

## Syntaxe

```
/know-extract [source] [options]
```

## Description

Analyse un fichier ou le contenu d'une conversation pour en extraire automatiquement les éléments pertinents : blocs de code, URLs, décisions, commandes, concepts clés et TODOs. Génère des notes atomiques classées par type dans les dossiers appropriés du vault.

## Options

| Option | Description |
|--------|-------------|
| `--type=TYPE` | Filtrer par type: `code`, `urls`, `decisions`, `commands`, `concepts`, `todos` |
| `--source=FILE` | Fichier source à analyser |
| `--output=DIR` | Répertoire de sortie (défaut: dossiers du vault) |
| `--format=FMT` | Format de sortie: `md` (défaut), `json`, `csv` |
| `--dry-run` | Afficher les éléments détectés sans créer de fichiers |

## Exemples

### Extraire les URLs d'un fichier

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
SOURCE="$1"

# Extraire toutes les URLs uniques
grep -oE 'https?://[^[:space:])\]>"'"'"']+' "$SOURCE" | sort -u
```

### Extraire les blocs de code

```bash
# Extraire les blocs de code avec leur langage
awk '/^```[a-z]/{lang=substr($0,4); capture=1; next} /^```$/{capture=0; print "---"} capture{print}' "$SOURCE"
```

### Extraire décisions et TODOs

```bash
# Décisions prises dans le texte
grep -inE 'décidé|choisi|opté pour|on va utiliser|retenu' "$SOURCE"

# TODOs et actions à suivre
grep -inE 'à faire|todo|prochaine étape|il faut|reste à' "$SOURCE"
```

### Extraction complète vers le vault

```bash
#!/usr/bin/env bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
SOURCE="$1"
DATE=$(date +%Y-%m-%d)

# Extraire URLs -> Références
URLS=$(grep -oE 'https?://[^[:space:])\]>"'"'"']+' "$SOURCE" 2>/dev/null | sort -u)
if [ -n "$URLS" ]; then
    echo "$URLS" >> "$KNOWLEDGE_PATH/Références/URLs_${DATE}.md"
    echo "URLs extraites: $(echo "$URLS" | wc -l)"
fi

# Extraire blocs bash -> Code/Bash/
awk '/^```bash/{f=1;n++;next}/^```$/{f=0;next}f' "$SOURCE" | \
while IFS= read -r line; do
    echo "$line"
done > "$KNOWLEDGE_PATH/Code/Bash/${DATE}_extract.sh" 2>/dev/null

# Extraire concepts (lignes marquées)
grep -iE '^\*\*|^## |important|essentiel|à retenir' "$SOURCE" 2>/dev/null | \
    head -20 > "$KNOWLEDGE_PATH/_Inbox/${DATE}_concepts.md"

echo "Extraction terminée pour: $SOURCE"
```

### Extraction en JSON

```bash
# Générer un résumé structuré en JSON
jq -n \
  --arg date "$(date +%Y-%m-%d)" \
  --arg urls "$(grep -coE 'https?://' "$SOURCE" 2>/dev/null || echo 0)" \
  --arg code "$(grep -c '^```' "$SOURCE" 2>/dev/null || echo 0)" \
  --arg todos "$(grep -ciE 'todo|à faire' "$SOURCE" 2>/dev/null || echo 0)" \
  '{date: $date, urls: ($urls|tonumber), code_blocks: (($code|tonumber)/2|floor), todos: ($todos|tonumber)}'
```

## Notes

- Les patterns de détection sont définis dans la section Extraction Automatique de SKILL.md.
- L'extraction ne modifie jamais le fichier source.
- Les fichiers créés dans `_Inbox/` sont à trier manuellement lors de la revue quotidienne.
- Combiner avec `/know-save --full` pour une extraction automatique complète de conversation.
- Utiliser `--dry-run` d'abord pour prévisualiser les éléments détectés.
