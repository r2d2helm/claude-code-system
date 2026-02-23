# Commande: /know-list

Lister les notes du vault avec filtres.

## Syntaxe

```
/know-list [options]
```

## Description

Affiche les notes de la base de connaissances avec filtrage par type, tag, statut ou date. Permet de naviguer rapidement dans le vault et d'identifier les notes récentes, orphelines ou à traiter. Affiche titre, date, type et tags pour chaque note.

## Options

| Option | Description |
|--------|-------------|
| `--type=TYPE` | Filtrer par type: `conversation`, `concept`, `code`, `daily`, `projet` |
| `--tag=TAG` | Filtrer par tag (ex: `#infra/docker`) |
| `--status=STATUS` | Filtrer par statut: `seedling`, `growing`, `evergreen`, `captured` |
| `--since=DATE` | Notes modifiées depuis DATE (YYYY-MM-DD) |
| `--limit=N` | Nombre de résultats (défaut: 20) |
| `--sort=FIELD` | Trier par: `date` (défaut), `name`, `size` |
| `--inbox` | Lister uniquement les notes dans _Inbox/ |

## Exemples

### Lister les 20 dernières notes modifiées

```bash
#!/usr/bin/env bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
LIMIT="${1:-20}"

echo "=== $LIMIT dernières notes modifiées ==="
find "$KNOWLEDGE_PATH" -name '*.md' \
    -not -path '*/.git/*' \
    -not -path '*/_Templates/*' \
    -printf '%TY-%Tm-%Td %TH:%TM  %p\n' 2>/dev/null | \
    sort -rn | head -n "$LIMIT" | \
    while read -r date time filepath; do
        name=$(basename "$filepath" .md)
        dir=$(basename "$(dirname "$filepath")")
        printf "%-12s %-15s %s\n" "$date" "[$dir]" "$name"
    done
```

### Filtrer par type (frontmatter)

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
TYPE="${1:-conversation}"

echo "=== Notes de type: $TYPE ==="
grep -rl "^type: $TYPE" "$KNOWLEDGE_PATH" --include='*.md' 2>/dev/null | \
    sort | while read -r filepath; do
        name=$(basename "$filepath" .md)
        date=$(grep -m1 '^date:' "$filepath" 2>/dev/null | awk '{print $2}')
        printf "%-12s %s\n" "$date" "$name"
    done
```

### Filtrer par tag

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
TAG="${1:-infra}"

echo "=== Notes avec tag: #$TAG ==="
grep -rl "#$TAG" "$KNOWLEDGE_PATH" --include='*.md' --exclude-dir='.git' 2>/dev/null | \
    while read -r filepath; do
        name=$(basename "$filepath" .md)
        echo "  - [[$name]]"
    done | sort
```

### Lister la inbox (notes à traiter)

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"

echo "=== Inbox (à traiter) ==="
INBOX_COUNT=$(find "$KNOWLEDGE_PATH/_Inbox" -name '*.md' 2>/dev/null | wc -l)
echo "Total: $INBOX_COUNT notes"
echo ""

find "$KNOWLEDGE_PATH/_Inbox" -name '*.md' -printf '%TY-%Tm-%Td  %f\n' 2>/dev/null | \
    sort -rn
```

### Notes modifiées cette semaine

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"

echo "=== Notes modifiées cette semaine ==="
find "$KNOWLEDGE_PATH" -name '*.md' -mtime -7 \
    -not -path '*/.git/*' \
    -not -path '*/_Templates/*' \
    -printf '%-12TY-%Tm-%Td  %p\n' 2>/dev/null | sort -rn | \
    while read -r date filepath; do
        printf "%-12s %s\n" "$date" "$(basename "$filepath" .md)"
    done
```

## Notes

- Le filtrage par frontmatter (`type`, `status`) utilise grep sur le YAML en tete de fichier.
- Pour des recherches de contenu, utiliser `/know-search` à la place.
- Les résultats sont triés par date de modification par défaut.
- Combiner les filtres : `/know-list --type=concept --tag=infra --since=2026-02-01`.
- La colonne `[dir]` indique le dossier parent (Conversations, Concepts, Code, etc.).
