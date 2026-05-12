# Commande: /know-export

Exporter la base de connaissances vers différents formats et outils.

## Syntaxe

```
/know-export [format] [options]
```

## Formats Supportés

### /know-export obsidian

Export optimisé pour Obsidian :

```
╔══════════════════════════════════════════════════════════════╗
║           📤 EXPORT OBSIDIAN                                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📁 CONFIGURATION:                                           ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Source      : ~/Documents/Knowledge                     │ ║
║  │ Destination : ~/Obsidian/SecondBrain                    │ ║
║  │ Notes       : 234                                       │ ║
║  │ Attachments : 45                                        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ⚙️ OPTIONS:                                                 ║
║  [x] Convertir liens en [[wikilinks]]                        ║
║  [x] Préserver frontmatter YAML                              ║
║  [x] Créer dossier .obsidian avec config                     ║
║  [x] Générer graph.json pour visualisation                   ║
║  [ ] Inclure fichiers attachés                               ║
║                                                              ║
║  [1] Exporter  [2] Configurer  [3] Prévisualiser             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
SOURCE_PATH="${1:-$HOME/Documents/Knowledge}"
DEST_PATH="${2:-$HOME/Obsidian/SecondBrain}"
CREATE_CONFIG="${3:-false}"

# Créer structure Obsidian
OBSIDIAN_CONFIG="$DEST_PATH/.obsidian"
if [ "$CREATE_CONFIG" = "true" ] && [ ! -d "$OBSIDIAN_CONFIG" ]; then
    mkdir -p "$OBSIDIAN_CONFIG"

    # app.json - Configuration de base
    cat > "$OBSIDIAN_CONFIG/app.json" << 'EOF'
{
  "alwaysUpdateLinks": true,
  "newFileLocation": "folder",
  "newFileFolderPath": "_Inbox",
  "attachmentFolderPath": "_Attachments"
}
EOF

    # core-plugins.json
    cat > "$OBSIDIAN_CONFIG/core-plugins.json" << 'EOF'
{
  "file-explorer": true,
  "global-search": true,
  "graph": true,
  "backlink": true,
  "tag-pane": true,
  "daily-notes": true,
  "templates": true
}
EOF
fi

# Copier et convertir fichiers
find "$SOURCE_PATH" -name "*.md" -type f | while read -r src_file; do
    relative="${src_file#$SOURCE_PATH/}"
    dest_file="$DEST_PATH/$relative"
    dest_dir="$(dirname "$dest_file")"

    mkdir -p "$dest_dir"

    # Lire et convertir contenu
    # Convertir liens Markdown en Wikilinks: [Texte](fichier.md) → [[fichier|Texte]]
    sed 's/\[([^]]*)\](\([^)]*\)\.md)/[[\2|\1]]/g' "$src_file" > "$dest_file"
done

echo "✅ Export Obsidian terminé: $DEST_PATH"
echo "   Notes exportées: $(find "$DEST_PATH" -name '*.md' | wc -l)"
```

### /know-export notion

Export pour import Notion (CSV) :

```
╔══════════════════════════════════════════════════════════════╗
║           📤 EXPORT NOTION                                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Format: CSV compatible Notion Import                        ║
║                                                              ║
║  Colonnes exportées:                                         ║
║  • Title                                                     ║
║  • Date                                                      ║
║  • Type                                                      ║
║  • Tags (multi-select)                                       ║
║  • Content                                                   ║
║  • Related (relations)                                       ║
║                                                              ║
║  Fichier: knowledge-export-2026-02-04.csv                    ║
║  Notes: 234                                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script:**
```bash
#!/usr/bin/env bash
SOURCE_PATH="${1:-$HOME/Documents/Knowledge}"
OUTPUT_FILE="${2:-notion-export.csv}"

echo "Title,Date,Type,Tags,Content" > "$OUTPUT_FILE"

find "$SOURCE_PATH" -name "*.md" -type f | while read -r f; do
    title=$(grep -m1 'title:' "$f" | sed 's/title: *//' | tr -d '"')
    date=$(grep -m1 'date:' "$f" | sed 's/date: *//')
    type=$(grep -m1 'type:' "$f" | sed 's/type: *//')
    tags=$(grep -m1 'tags:' "$f" | sed 's/tags: *\[//;s/\]//' | tr -d '"')
    # Extraire contenu sans frontmatter, limité à 1000 chars
    body=$(awk '/^---/{p++} p==2{print}' "$f" | head -c 1000 | tr '\n' ' ' | tr ',' ';')

    echo "\"$title\",\"$date\",\"$type\",\"$tags\",\"$body\"" >> "$OUTPUT_FILE"
done

count=$(wc -l < "$OUTPUT_FILE")
echo "✅ Export Notion: $OUTPUT_FILE ($((count - 1)) notes)"
```

### /know-export json

Export JSON complet :

```bash
/know-export json --output=knowledge-backup.json
```

```json
{
  "exported": "2026-02-04T08:30:00",
  "stats": {
    "total_notes": 234,
    "conversations": 89,
    "concepts": 67,
    "code": 45
  },
  "notes": [
    {
      "id": "20260204-083000",
      "title": "Configuration Super Agent Linux",
      "date": "2026-02-04",
      "type": "conversation",
      "tags": ["linux", "claude-code", "skill"],
      "content": "...",
      "links": ["Concept1", "Concept2"],
      "path": "Conversations/2026-02-04_Conv_Linux-Agent.md"
    }
  ]
}
```

### /know-export html

Générer site statique navigable :

```
╔══════════════════════════════════════════════════════════════╗
║           📤 EXPORT HTML                                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🌐 SITE GÉNÉRÉ:                                             ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ knowledge-site/                                         │ ║
║  │ ├── index.html          # Page d'accueil                │ ║
║  │ ├── search.html         # Recherche                     │ ║
║  │ ├── tags.html           # Index des tags                │ ║
║  │ ├── graph.html          # Visualisation graphe          │ ║
║  │ ├── notes/              # Notes converties              │ ║
║  │ ├── css/                # Styles                        │ ║
║  │ └── js/                 # Scripts (search, graph)       │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Ouvrir: file:///home/r2d2/knowledge-site/index.html         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /know-export backup

Backup complet avec versioning :

```bash
/know-export backup --dest="$HOME/Backups/Knowledge"
```

```
╔══════════════════════════════════════════════════════════════╗
║           💾 BACKUP KNOWLEDGE BASE                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📁 Backup créé:                                             ║
║  ~/Backups/Knowledge/2026-02-04_Knowledge-Backup.tar.gz      ║
║                                                              ║
║  📊 Contenu:                                                 ║
║  • 234 notes Markdown                                        ║
║  • 45 fichiers code                                          ║
║  • 12 attachments                                            ║
║  • Taille: 45 MB                                             ║
║                                                              ║
║  🔄 Rotation: 5 derniers backups conservés                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Options

| Option | Description |
|--------|-------------|
| `--dest=path` | Chemin de destination |
| `--include-attachments` | Inclure pièces jointes |
| `--format=md/html/pdf` | Format de sortie |
| `--filter=tag` | Filtrer par tag |
| `--since=date` | Depuis date |
| `--compress` | Compresser en tar.gz |

## Exemples

```bash
# Export Obsidian
/know-export obsidian --dest="$HOME/Obsidian/Vault"

# Export Notion
/know-export notion --output="notion-import.csv"

# Backup complet
/know-export backup --dest="$HOME/Backups" --compress

# Export HTML navigable
/know-export html --dest="$HOME/knowledge-site"

# Export partiel (tag spécifique)
/know-export obsidian --filter="#proxmox"
```
