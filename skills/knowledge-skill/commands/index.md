# Commande: /know-index

Reconstruire l'index principal de la base de connaissances.

## Syntaxe

```
/know-index [options]
```

## Description

Parcourt l'intégralité du vault pour reconstruire INDEX.md, régénérer les Maps of Content (MOC) thématiques et actualiser la liste des tags. Détecte aussi les notes orphelines (sans liens entrants ni sortants) et les fichiers sans frontmatter.

## Options

| Option | Description |
|--------|-------------|
| `--full` | Reconstruction complète (index + MOCs + tags) |
| `--tags-only` | Mettre à jour uniquement la liste des tags |
| `--moc=THEME` | Régénérer un MOC spécifique (ex: `dev`, `infra`) |
| `--orphans` | Lister uniquement les notes orphelines |
| `--dry-run` | Afficher les changements sans écrire |
| `--stats` | Afficher les statistiques de l'index |

## Exemples

### Reconstruction de l'index principal

```bash
#!/usr/bin/env bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
INDEX_FILE="$KNOWLEDGE_PATH/_Index/INDEX.md"
DATE=$(date +%Y-%m-%d)

mkdir -p "$KNOWLEDGE_PATH/_Index"

# Compter les notes par type
TOTAL=$(find "$KNOWLEDGE_PATH" -name '*.md' -not -path '*/.git/*' -not -path '*/_Templates/*' | wc -l)
CONVS=$(find "$KNOWLEDGE_PATH/Conversations" -name '*.md' 2>/dev/null | wc -l)
CONCEPTS=$(find "$KNOWLEDGE_PATH/Concepts" -name '*.md' 2>/dev/null | wc -l)
CODE=$(find "$KNOWLEDGE_PATH/Code" -name '*.md' 2>/dev/null | wc -l)
DAILY=$(find "$KNOWLEDGE_PATH/_Daily" -name '*.md' 2>/dev/null | wc -l)

# Générer INDEX.md
cat > "$INDEX_FILE" << EOF
---
date: $DATE
type: index
tags: [index, moc]
---

# Index Principal

> Dernière mise à jour: $DATE

## Statistiques
- Total notes: $TOTAL
- Conversations: $CONVS
- Concepts: $CONCEPTS
- Code snippets: $CODE
- Daily notes: $DAILY

## Notes Récentes
EOF

# Ajouter les 20 dernières notes modifiées
find "$KNOWLEDGE_PATH" -name '*.md' -not -path '*/_Index/*' -not -path '*/.git/*' \
    -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -20 | \
    while read -r _ filepath; do
        name=$(basename "$filepath" .md)
        echo "- [[$name]]"
    done >> "$INDEX_FILE"

echo "Index mis à jour: $INDEX_FILE ($TOTAL notes)"
```

### Extraction et mise à jour des tags

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
TAGS_FILE="$KNOWLEDGE_PATH/_Index/Tags.md"

# Extraire tous les tags du frontmatter YAML et du contenu
grep -roh '#[a-zA-Z][a-zA-Z0-9_/-]*' "$KNOWLEDGE_PATH" --include='*.md' \
    --exclude-dir='.git' 2>/dev/null | sort | uniq -c | sort -rn > /tmp/tags_count.txt

# Générer Tags.md
echo "# Tags" > "$TAGS_FILE"
echo "" >> "$TAGS_FILE"
echo "| Tag | Occurrences |" >> "$TAGS_FILE"
echo "|-----|-------------|" >> "$TAGS_FILE"
while read -r count tag; do
    echo "| $tag | $count |" >> "$TAGS_FILE"
done < /tmp/tags_count.txt

echo "Tags mis à jour: $(wc -l < /tmp/tags_count.txt) tags uniques"
```

### Détecter les notes orphelines

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"

# Trouver les notes qui ne sont référencées par aucune autre
find "$KNOWLEDGE_PATH" -name '*.md' -not -path '*/_Index/*' -not -path '*/.git/*' | \
while read -r filepath; do
    name=$(basename "$filepath" .md)
    refs=$(grep -rl "\[\[$name\]\]" "$KNOWLEDGE_PATH" --include='*.md' 2>/dev/null | \
           grep -v "$filepath" | wc -l)
    if [ "$refs" -eq 0 ]; then
        echo "Orpheline: $name"
    fi
done
```

### Régénérer un MOC thématique

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
THEME="${1:-dev}"

# Trouver toutes les notes avec le tag du thème
grep -rl "#${THEME}" "$KNOWLEDGE_PATH" --include='*.md' --exclude-dir='.git' 2>/dev/null | \
while read -r filepath; do
    name=$(basename "$filepath" .md)
    echo "- [[$name]]"
done | sort > "$KNOWLEDGE_PATH/_Index/MOC-${THEME}.md"

echo "MOC $THEME régénéré"
```

## Notes

- L'indexation complète peut prendre quelques secondes sur un vault volumineux (>1000 notes).
- Les notes dans `_Templates/` sont exclues de l'index.
- Exécuter `/know-index --full` après un import massif ou une réorganisation.
- Les notes orphelines ne sont pas forcément problématiques (notes nouvelles, notes de référence).
- Combiner avec `/know-link` pour réduire le nombre d'orphelines.
