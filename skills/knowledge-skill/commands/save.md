# Commande: /know-save

Sauvegarder et résumer la conversation actuelle.

## Syntaxe

```
/know-save [options]
```

## Modes de Sauvegarde

### /know-save (automatique)

Analyse et sauvegarde automatique de la conversation :

```
╔══════════════════════════════════════════════════════════════╗
║           🧠 CAPTURE DE CONVERSATION                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📊 ANALYSE DE LA CONVERSATION:                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Messages analysés  : 24                                 │ ║
║  │ Durée estimée      : 45 minutes                         │ ║
║  │ Sujets détectés    : 3                                  │ ║
║  │ Code extrait       : 5 blocs                            │ ║
║  │ Décisions prises   : 2                                  │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📝 RÉSUMÉ GÉNÉRÉ:                                           ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Titre: Configuration Super Agent Linux                  │ ║
║  │                                                         │ ║
║  │ Discussion sur la création d'un agent Linux pour        │ ║
║  │ Claude Code avec 36 commandes bash et 10 wizards.       │ ║
║  │ Installation et test du système de routing automatique. │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  🏷️ TAGS SUGGÉRÉS:                                           ║
║  #dev/claude-code #infra/linux #projet/multipass            ║
║  #skill #bash #automation                                    ║
║                                                              ║
║  [1] Sauvegarder  [2] Modifier  [3] Ajouter tags             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script bash:**
```bash
#!/usr/bin/env bash
KNOWLEDGE_PATH="${KNOWLEDGE_PATH:-$HOME/Documents/Knowledge}"
TITLE="${1:-}"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M%S)
ID="${DATE}-${TIME}"

# Créer structure si nécessaire
for FOLDER in Conversations Concepts Code _Index _Daily _Inbox; do
    mkdir -p "$KNOWLEDGE_PATH/$FOLDER"
done

# Générer fichier de conversation
SAFE_TITLE=$(echo "$TITLE" | tr ' ' '-' | tr -cd '[:alnum:]-')
FILE_NAME="${DATE}_Conv_${SAFE_TITLE}.md"
FILE_PATH="$KNOWLEDGE_PATH/Conversations/$FILE_NAME"

TAGS_YAML=""

cat > "$FILE_PATH" << EOF
---
id: $ID
title: $TITLE
date: $DATE
type: conversation
tags: [$TAGS_YAML]
source: Claude
status: captured
related: []
---

# $TITLE

## Résumé
{À compléter - résumé de la conversation}

## Points Clés
-
-
-

## Décisions Prises
- [ ]

## Code/Commandes Extraits
\`\`\`bash
# Code extrait de la conversation
\`\`\`

## Concepts Liés
- [[]]

## Actions Suivantes
- [ ]

## Notes Additionnelles


---
*Capturé le $DATE depuis conversation Claude*
EOF

echo "✅ Conversation sauvegardée: $FILE_PATH"

# Mettre à jour Daily Note
DAILY_PATH="$KNOWLEDGE_PATH/_Daily/$DATE.md"
if [ ! -f "$DAILY_PATH" ]; then
    cat > "$DAILY_PATH" << EOF
---
date: $DATE
type: daily
tags: [daily]
---

# 📅 $DATE

## Conversations du Jour
EOF
fi

# Ajouter lien dans Daily
echo "- [[$FILE_NAME]]" >> "$DAILY_PATH"
```

### /know-save --quick "titre"

Sauvegarde rapide avec titre :

```bash
/know-save --quick "Configuration Proxmox HA"
```

```
✅ Sauvegardé: 2026-02-04_Conv_Configuration-Proxmox-HA.md
   Tags auto: #proxmox #ha #configuration
   Lien ajouté à Daily Note
```

### /know-save --full

Sauvegarde complète avec extraction automatique :

```
╔══════════════════════════════════════════════════════════════╗
║           🧠 CAPTURE COMPLÈTE                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📁 FICHIERS CRÉÉS:                                          ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✓ Conversations/2026-02-04_Conv_Linux-Agent.md          │ ║
║  │ ✓ Code/Bash/2026-02-04_Install-Skills.sh                │ ║
║  │ ✓ Code/Bash/2026-02-04_Organize-Files.sh                │ ║
║  │ ✓ Concepts/C_Meta-Router-Pattern.md                     │ ║
║  │ ✓ Concepts/C_Skill-Structure.md                         │ ║
║  │ ✓ _Daily/2026-02-04.md (mis à jour)                     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📊 EXTRACTION:                                              ║
║  • 5 blocs de code → Code/Bash/                              ║
║  • 2 concepts identifiés → Concepts/                         ║
║  • 3 décisions → Section Décisions                           ║
║  • 12 tags appliqués                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /know-save --template {template}

Utiliser un template spécifique :

```bash
/know-save --template meeting     # Pour réunion
/know-save --template debug       # Pour session debug
/know-save --template learning    # Pour apprentissage
/know-save --template project     # Pour projet
```

## Extraction Automatique

### Éléments Détectés

| Élément | Pattern | Action |
|---------|---------|--------|
| Code Bash | ` ```bash ` | Extrait vers `Code/Bash/` |
| Code Python | ` ```python ` | Extrait vers `Code/Python/` |
| Commandes | `/command` | Liste dans section Commandes |
| URLs | `http(s)://` | Liste dans Références |
| Décisions | "décidé", "choisi" | Section Décisions |
| TODOs | "à faire", "todo" | Section Actions |

### Script d'Extraction

```bash
extract_conversation_elements() {
    local content="$1"

    # Extraire blocs de code
    echo "$content" | grep -oP '```\w+\n[\s\S]*?```'

    # Extraire URLs
    echo "$content" | grep -oE 'https?://[^[:space:])\]>]+'  | sort -u

    # Détecter décisions
    echo "$content" | grep -iE 'décidé|choisi|opté pour|on va utiliser'

    # Détecter actions
    echo "$content" | grep -iE 'à faire|todo|prochaine étape|il faut'
}
```

## Options

| Option | Description |
|--------|-------------|
| `--quick "titre"` | Sauvegarde rapide avec titre |
| `--full` | Extraction complète automatique |
| `--template=name` | Utiliser template spécifique |
| `--tags=t1,t2` | Ajouter tags manuels |
| `--project=name` | Associer à un projet |
| `--no-daily` | Ne pas mettre à jour Daily Note |
| `--dry-run` | Prévisualiser sans créer |

## Exemples

```bash
# Sauvegarde rapide
/know-save --quick "Debug API Proxmox"

# Sauvegarde complète avec tags
/know-save --full --tags="#proxmox,#api,#debug"

# Associer à un projet
/know-save --project="MultiPass" --full

# Prévisualiser
/know-save --dry-run
```
