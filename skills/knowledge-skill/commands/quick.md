# Commande: /know-quick

Capture rapide d'une note dans la inbox.

## Syntaxe

```
/know-quick "titre" [contenu] [options]
```

## Description

Crée une note atomique minimale dans _Inbox/ avec frontmatter auto-généré (id, date, tags). Optimisé pour la vitesse : capturer une idée en une commande, la trier plus tard. Idéal pour les captures spontanées pendant une session de travail.

## Options

| Option | Description |
|--------|-------------|
| `--tags=t1,t2` | Ajouter des tags manuels |
| `--type=TYPE` | Type de note: `idea`, `todo`, `snippet`, `link` (défaut: `idea`) |
| `--project=NOM` | Associer à un projet |
| `--edit` | Ouvrir la note après création (si $EDITOR défini) |

## Exemples

### Capture rapide simple

```bash
#!/usr/bin/env bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
TITLE="${1:?Usage: know-quick \"titre\" [contenu]}"
CONTENT="${2:-}"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M%S)
ID="${DATE}-${TIME}"

mkdir -p "$KNOWLEDGE_PATH/_Inbox"

SAFE_TITLE=$(echo "$TITLE" | tr ' ' '-' | tr -cd '[:alnum:]-')
FILE_PATH="$KNOWLEDGE_PATH/_Inbox/${DATE}_${SAFE_TITLE}.md"

cat > "$FILE_PATH" << EOF
---
id: $ID
title: $TITLE
date: $DATE
type: idea
status: seedling
tags: [inbox]
---

# $TITLE

$CONTENT

---
*Quick capture le $DATE*
EOF

echo "Note créée: $FILE_PATH"
```

### Capture avec tags et contenu

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
TITLE="Pattern Observer pour hooks"
TAGS="dev/bash,design-pattern"
CONTENT="Les hooks Claude utilisent un pattern Observer : chaque événement déclenche les hooks enregistrés. À explorer pour d'autres usages."

DATE=$(date +%Y-%m-%d)
SAFE_TITLE=$(echo "$TITLE" | tr ' ' '-' | tr -cd '[:alnum:]-')
FILE_PATH="$KNOWLEDGE_PATH/_Inbox/${DATE}_${SAFE_TITLE}.md"

# Convertir tags CSV en YAML list
TAGS_YAML=$(echo "$TAGS" | tr ',' '\n' | sed 's/^/  - /' )

cat > "$FILE_PATH" << EOF
---
id: ${DATE}-$(date +%H%M%S)
title: $TITLE
date: $DATE
type: idea
status: seedling
tags:
  - inbox
$TAGS_YAML
---

# $TITLE

$CONTENT

---
*Quick capture le $DATE*
EOF
```

### Capture de TODO

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
DATE=$(date +%Y-%m-%d)
TITLE="Configurer backup automatique vault"

FILE_PATH="$KNOWLEDGE_PATH/_Inbox/${DATE}_TODO_$(echo "$TITLE" | tr ' ' '-' | tr -cd '[:alnum:]-').md"

cat > "$FILE_PATH" << EOF
---
id: ${DATE}-$(date +%H%M%S)
title: $TITLE
date: $DATE
type: todo
status: seedling
tags: [inbox, todo, p2]
---

# TODO: $TITLE

- [ ] $TITLE

## Contexte


## Deadline


---
*Quick capture le $DATE*
EOF
```

### Capture de snippet de code

```bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
DATE=$(date +%Y-%m-%d)
TITLE="One-liner find fichiers lourds"
CODE='find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null | sort -k5 -h'

FILE_PATH="$KNOWLEDGE_PATH/_Inbox/${DATE}_Snippet_$(echo "$TITLE" | tr ' ' '-' | tr -cd '[:alnum:]-').md"

cat > "$FILE_PATH" << EOF
---
id: ${DATE}-$(date +%H%M%S)
title: $TITLE
date: $DATE
type: code
language: bash
status: seedling
tags: [inbox, code, bash]
---

# $TITLE

\`\`\`bash
$CODE
\`\`\`

---
*Quick capture le $DATE*
EOF
```

## Notes

- Les notes _Inbox/ sont à trier lors de la revue quotidienne (`/know-wizard review daily`).
- Le statut `seedling` indique une note fraiche, non encore développée.
- Utiliser `/know-save` pour les captures complètes de conversation (plus riche).
- Le nom de fichier est assaini automatiquement (pas d'espaces ni caractères spéciaux).
- Les notes quick peuvent être promues vers Concepts/ ou Code/ après traitement.
