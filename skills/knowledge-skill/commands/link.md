# Commande: /know-link

Trouver et créer des liens entre notes associées.

## Syntaxe

```
/know-link [note] [options]
```

## Description

Analyse le contenu des notes pour suggérer et créer des wikilinks [[Note]] entre notes partageant des thèmes, tags ou termes communs. Renforce la structure du graphe de connaissances en connectant les idées isolées. Met à jour la section "Concepts Liés" ou "Liens" des notes concernées.

## Options

| Option | Description |
|--------|-------------|
| `--note=FILE` | Analyser une note spécifique |
| `--all` | Analyser tout le vault et suggérer des liens |
| `--auto` | Créer les liens automatiquement (sans confirmation) |
| `--threshold=N` | Score minimum de similarité (défaut: 2 mots communs) |
| `--dry-run` | Afficher les suggestions sans modifier les fichiers |
| `--backlinks` | Mettre à jour les backlinks dans les notes cibles |

## Exemples

### Trouver les notes associées par mots-clés

```bash
#!/usr/bin/env bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
NOTE="$1"
NOTE_NAME=$(basename "$NOTE" .md)

# Extraire les mots significatifs de la note (>4 caractères, hors stopwords)
KEYWORDS=$(grep -oE '\b[a-zA-ZÀ-ÿ]{5,}\b' "$NOTE" | \
    tr '[:upper:]' '[:lower:]' | \
    grep -vxF -f <(printf '%s\n' cette cette avoir être faire avec dans pour plus aussi comme) | \
    sort | uniq -c | sort -rn | head -10 | awk '{print $2}')

echo "Mots-clés de [[$NOTE_NAME]]: $KEYWORDS"
echo "---"

# Chercher ces mots dans les autres notes
for kw in $KEYWORDS; do
    grep -rl --include='*.md' -i "$kw" "$KNOWLEDGE_PATH" 2>/dev/null | \
        grep -v "$NOTE" | \
        while read -r match; do
            echo "[[$( basename "$match" .md)]] (mot: $kw)"
        done
done | sort | uniq -c | sort -rn | head -10
```

### Détecter les liens manquants dans tout le vault

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"

# Pour chaque note, vérifier si des noms de notes apparaissent dans le texte sans wikilink
find "$KNOWLEDGE_PATH" -name '*.md' -not -path '*/.git/*' -not -path '*/_Index/*' | \
while read -r filepath; do
    name=$(basename "$filepath" .md)
    # Chercher le nom dans d'autres fichiers sans être un wikilink
    grep -rl "$name" "$KNOWLEDGE_PATH" --include='*.md' 2>/dev/null | \
        grep -v "$filepath" | \
    while read -r other; do
        # Vérifier que ce n'est pas déjà un wikilink
        if ! grep -q "\[\[$name\]\]" "$other" 2>/dev/null; then
            echo "$(basename "$other" .md) mentionne '$name' sans lien -> ajouter [[$name]]"
        fi
    done
done
```

### Ajouter un wikilink dans la section Liens d'une note

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
NOTE="$1"
LINK_TARGET="$2"

# Vérifier que le lien n'existe pas déjà
if grep -q "\[\[$LINK_TARGET\]\]" "$NOTE" 2>/dev/null; then
    echo "Lien [[$LINK_TARGET]] existe déjà dans $(basename "$NOTE")"
    exit 0
fi

# Ajouter dans la section "Concepts Liés" ou "Liens"
if grep -q "## Concepts Liés" "$NOTE"; then
    sed -i "/## Concepts Liés/a - [[$LINK_TARGET]]" "$NOTE"
elif grep -q "## Liens" "$NOTE"; then
    sed -i "/## Liens/a - [[$LINK_TARGET]]" "$NOTE"
else
    # Ajouter une section Liens à la fin
    printf '\n## Liens\n- [[%s]]\n' "$LINK_TARGET" >> "$NOTE"
fi

echo "Lien [[$LINK_TARGET]] ajouté dans $(basename "$NOTE" .md)"
```

### Rapport de backlinks pour une note

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
TARGET=$(basename "$1" .md)

echo "Backlinks vers [[$TARGET]]:"
grep -rl "\[\[$TARGET\]\]" "$KNOWLEDGE_PATH" --include='*.md' 2>/dev/null | \
while read -r filepath; do
    echo "  <- [[$(basename "$filepath" .md)]]"
done
```

## Notes

- Le seuil par défaut de 2 mots communs évite les faux positifs sur des termes génériques.
- Utiliser `--dry-run` d'abord pour valider les suggestions avant modification.
- Les wikilinks utilisent la syntaxe Obsidian `[[Nom de la note]]`.
- Combiner avec `/know-index --orphans` pour identifier les notes à connecter en priorité.
- Les backlinks sont visibles automatiquement dans Obsidian (panneau backlinks).
