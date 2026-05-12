# Wizard: Setup Base de Connaissances

Configuration initiale du système de capture de connaissances.

## Déclenchement

```
/know-wizard setup
```

## Étapes du Wizard (5)

### Étape 1: Emplacement

```
╔══════════════════════════════════════════════════════════════╗
║           🧠 WIZARD KNOWLEDGE SETUP                          ║
║              Étape 1/5 : Emplacement                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Où voulez-vous stocker votre base de connaissances ?        ║
║                                                              ║
║  [1] 📁 Documents/Knowledge (recommandé)                     ║
║      ~/Documents/Knowledge                                   ║
║                                                              ║
║  [2] 📁 Nextcloud/Knowledge (sync cloud)                     ║
║      ~/Nextcloud/Knowledge                                   ║
║                                                              ║
║  [3] 📁 Dropbox/Knowledge                                    ║
║      ~/Dropbox/Knowledge                                     ║
║                                                              ║
║  [4] 📁 Obsidian Vault existant                              ║
║      Sélectionner un vault Obsidian existant                 ║
║                                                              ║
║  [5] 🔧 Personnalisé                                         ║
║      Entrer un chemin personnalisé                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 2: Structure

```
╔══════════════════════════════════════════════════════════════╗
║           🧠 WIZARD KNOWLEDGE SETUP                          ║
║               Étape 2/5 : Structure                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Structure de dossiers à créer :                             ║
║                                                              ║
║  Knowledge/                                                  ║
║  ├── 📁 _Index/           Index et navigation                ║
║  ├── 📁 _Daily/           Notes quotidiennes                 ║
║  ├── 📁 _Inbox/           Notes à traiter                    ║
║  ├── 📁 _Templates/       Modèles de notes                   ║
║  ├── 📁 Conversations/    Résumés conversations Claude       ║
║  ├── 📁 Concepts/         Notes atomiques (Zettelkasten)     ║
║  ├── 📁 Projets/          Notes par projet                   ║
║  ├── 📁 Code/             Snippets et scripts                ║
║  └── 📁 Références/       Sources et documentation           ║
║                                                              ║
║  [x] Créer toutes les structures                             ║
║  [x] Générer templates de base                               ║
║  [x] Créer fichier INDEX.md                                  ║
║  [ ] Importer notes existantes depuis...                     ║
║                                                              ║
║  [1] Continuer  [2] Personnaliser                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script création structure:**
```bash
#!/usr/bin/env bash
BASE_PATH="$1"

declare -A structure=(
    ["_Index"]="INDEX.md Tags.md"
    ["_Daily"]=""
    ["_Inbox"]=""
    ["_Templates"]="Template-Conversation.md Template-Concept.md Template-Code.md"
    ["Conversations"]=""
    ["Concepts"]=""
    ["Projets"]=""
    ["Code/Bash"]=""
    ["Code/Python"]=""
    ["Code/Configs"]=""
    ["Références/Documentation"]=""
    ["Références/Articles"]=""
    ["Références/Troubleshooting"]=""
)

for folder in "${!structure[@]}"; do
    folder_path="$BASE_PATH/$folder"
    mkdir -p "$folder_path"

    for sub_item in ${structure[$folder]}; do
        sub_path="$folder_path/$sub_item"
        if [[ "$sub_item" == *.md ]]; then
            [ ! -f "$sub_path" ] && touch "$sub_path"
        else
            mkdir -p "$sub_path"
        fi
    done
done

echo "✅ Structure créée: $BASE_PATH"
```

### Étape 3: Tags Système

```
╔══════════════════════════════════════════════════════════════╗
║           🧠 WIZARD KNOWLEDGE SETUP                          ║
║                Étape 3/5 : Tags                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Configuration du système de tags :                          ║
║                                                              ║
║  📂 DOMAINES (premier niveau)                                ║
║  [x] #dev         Développement                              ║
║  [x] #infra       Infrastructure                             ║
║  [x] #projet      Projets                                    ║
║  [x] #business    Business/Commercial                        ║
║  [x] #personal    Personnel                                  ║
║  [ ] Ajouter domaine personnalisé...                         ║
║                                                              ║
║  📂 SOUS-DOMAINES (exemples)                                 ║
║  #dev/python  #dev/bash  #dev/javascript                     ║
║  #infra/proxmox  #infra/linux  #infra/docker                 ║
║  #projet/multipass  #projet/client-x                         ║
║                                                              ║
║  🏷️ TAGS STATUS                                              ║
║  [x] #todo  #inprogress  #done  #review                      ║
║                                                              ║
║  🏷️ TAGS PRIORITÉ                                            ║
║  [x] #p1  #p2  #p3                                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 4: Intégration

```
╔══════════════════════════════════════════════════════════════╗
║           🧠 WIZARD KNOWLEDGE SETUP                          ║
║             Étape 4/5 : Intégration                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Outils d'intégration :                                      ║
║                                                              ║
║  📱 OBSIDIAN                                                 ║
║  [x] Configurer comme vault Obsidian                         ║
║      → Crée .obsidian/ avec plugins recommandés              ║
║                                                              ║
║  ⚡ ALIAS BASH                                               ║
║  [x] Ajouter alias dans ~/.bashrc                            ║
║      know-save, know-search, know-list                       ║
║                                                              ║
║  📅 AUTOMATISATION                                           ║
║  [x] Créer cron job Daily Review                             ║
║      Rappel quotidien 18:00 pour revue notes                 ║
║                                                              ║
║  ☁️ SYNCHRONISATION                                          ║
║  [ ] Configurer sync Nextcloud                               ║
║  [ ] Configurer sync Git                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script configuration Obsidian:**
```bash
#!/usr/bin/env bash
VAULT_PATH="$1"

OBSIDIAN_PATH="$VAULT_PATH/.obsidian"
mkdir -p "$OBSIDIAN_PATH"

# Configuration principale
cat > "$OBSIDIAN_PATH/app.json" << 'EOF'
{
  "alwaysUpdateLinks": true,
  "newFileLocation": "folder",
  "newFileFolderPath": "_Inbox",
  "attachmentFolderPath": "_Attachments",
  "useMarkdownLinks": false,
  "showLineNumber": true,
  "foldHeading": true,
  "foldIndent": true
}
EOF

# Plugins activés
cat > "$OBSIDIAN_PATH/core-plugins.json" << 'EOF'
{
  "file-explorer": true,
  "global-search": true,
  "graph": true,
  "backlink": true,
  "outgoing-link": true,
  "tag-pane": true,
  "page-preview": true,
  "daily-notes": true,
  "templates": true,
  "command-palette": true,
  "starred": true,
  "outline": true
}
EOF

# Configuration Daily Notes
cat > "$OBSIDIAN_PATH/daily-notes.json" << 'EOF'
{
  "folder": "_Daily",
  "format": "YYYY-MM-DD",
  "template": "_Templates/Template-Daily.md"
}
EOF

echo "✅ Configuration Obsidian créée"
```

### Étape 5: Finalisation

```
╔══════════════════════════════════════════════════════════════╗
║           🧠 WIZARD KNOWLEDGE SETUP                          ║
║               Étape 5/5 : Terminé                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🎉 CONFIGURATION TERMINÉE !                                 ║
║                                                              ║
║  📁 BASE DE CONNAISSANCES:                                   ║
║  ~/Documents/Knowledge                                       ║
║                                                              ║
║  ✅ CRÉÉ:                                                    ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ • 9 dossiers de structure                               │ ║
║  │ • 5 templates de notes                                  │ ║
║  │ • INDEX.md principal                                    │ ║
║  │ • Configuration Obsidian                                │ ║
║  │ • Alias bash (know-*)                                   │ ║
║  │ • README documentation                                  │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  🚀 COMMANDES DISPONIBLES:                                   ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ /know-save          Sauvegarder conversation            │ ║
║  │ /know-search        Rechercher dans la base             │ ║
║  │ /know-export        Exporter notes                      │ ║
║  │ /know-wizard review Revue quotidienne                   │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  💡 PROCHAINES ÉTAPES:                                       ║
║  1. Ouvrir le vault dans Obsidian                            ║
║  2. Sauvegarder cette conversation: /know-save               ║
║  3. Configurer revue quotidienne                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script finalisation:**
```bash
#!/usr/bin/env bash
BASE_PATH="$1"
TODAY=$(date +%Y-%m-%d)
NOW=$(date +"%Y-%m-%d %H:%M")

# Créer INDEX.md
cat > "$BASE_PATH/_Index/INDEX.md" << EOF
---
title: Index Principal
type: index
date: $TODAY
---

# 🧠 Base de Connaissances

## Navigation Rapide

### 📁 Par Type
- [[_Index/Conversations|Conversations Claude]]
- [[_Index/Concepts|Concepts (Zettelkasten)]]
- [[_Index/Projets|Projets]]
- [[_Index/Code|Code & Scripts]]
- [[_Index/Références|Références]]

### 🏷️ Par Tag
- [[_Index/Tags|Index des Tags]]

### 📅 Par Date
- [[_Daily/$TODAY|Aujourd'hui]]
- Voir dossier [[_Daily|Daily Notes]]

## Statistiques
- Notes totales: {à mettre à jour}
- Dernière mise à jour: $NOW

## À Traiter
![[_Inbox]]

---
*Base créée le $TODAY*
EOF

# Créer README
cat > "$BASE_PATH/README.md" << EOF
# 🧠 Base de Connaissances

## Structure
- \`_Index/\` - Index et navigation
- \`_Daily/\` - Notes quotidiennes
- \`_Inbox/\` - Notes à traiter
- \`_Templates/\` - Modèles
- \`Conversations/\` - Résumés conversations Claude
- \`Concepts/\` - Notes atomiques (Zettelkasten)
- \`Projets/\` - Notes par projet
- \`Code/\` - Snippets et scripts
- \`Références/\` - Documentation

## Commandes
- \`/know-save\` - Sauvegarder conversation
- \`/know-search "terme"\` - Rechercher
- \`/know-export obsidian\` - Exporter

## Conventions
- Noms: \`YYYY-MM-DD_Type_Sujet.md\`
- Tags: \`#domaine/sous-domaine\`
- Liens: \`[[NomNote]]\`

Créé le $TODAY
EOF

echo "✅ Base de connaissances initialisée: $BASE_PATH"
```
