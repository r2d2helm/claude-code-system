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
║  [1] 📁 Documents\Knowledge (recommandé)                     ║
║      C:\Users\r2d2\Documents\Knowledge                       ║
║                                                              ║
║  [2] 📁 OneDrive\Knowledge (sync cloud)                      ║
║      C:\Users\r2d2\OneDrive\Knowledge                        ║
║                                                              ║
║  [3] 📁 Dropbox\Knowledge                                    ║
║      C:\Users\r2d2\Dropbox\Knowledge                         ║
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
║  Knowledge\                                                  ║
║  ├── 📁 _Index\           Index et navigation                ║
║  ├── 📁 _Daily\           Notes quotidiennes                 ║
║  ├── 📁 _Inbox\           Notes à traiter                    ║
║  ├── 📁 _Templates\       Modèles de notes                   ║
║  ├── 📁 Conversations\    Résumés conversations Claude       ║
║  ├── 📁 Concepts\         Notes atomiques (Zettelkasten)     ║
║  ├── 📁 Projets\          Notes par projet                   ║
║  ├── 📁 Code\             Snippets et scripts                ║
║  └── 📁 Références\       Sources et documentation           ║
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
```powershell
param([string]$BasePath)

$Structure = @{
    "_Index" = @("INDEX.md", "Tags.md")
    "_Daily" = @()
    "_Inbox" = @()
    "_Templates" = @("Template-Conversation.md", "Template-Concept.md", "Template-Code.md")
    "Conversations" = @()
    "Concepts" = @()
    "Projets" = @()
    "Code" = @("PowerShell", "Python", "Bash", "Configs")
    "Références" = @("Documentation", "Articles", "Troubleshooting")
}

foreach ($Folder in $Structure.Keys) {
    $FolderPath = Join-Path $BasePath $Folder
    New-Item -ItemType Directory -Path $FolderPath -Force | Out-Null
    
    foreach ($SubItem in $Structure[$Folder]) {
        $SubPath = Join-Path $FolderPath $SubItem
        if ($SubItem -match '\.md$') {
            # C'est un fichier
            if (!(Test-Path $SubPath)) {
                "" | Out-File $SubPath -Encoding UTF8
            }
        } else {
            # C'est un sous-dossier
            New-Item -ItemType Directory -Path $SubPath -Force | Out-Null
        }
    }
}

Write-Host "✅ Structure créée: $BasePath"
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
║  #dev/python  #dev/powershell  #dev/javascript               ║
║  #infra/proxmox  #infra/windows  #infra/docker               ║
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
║  ⚡ RACCOURCIS POWERSHELL                                    ║
║  [x] Ajouter alias dans $PROFILE                             ║
║      know-save, know-search, know-list                       ║
║                                                              ║
║  📅 AUTOMATISATION                                           ║
║  [x] Créer tâche planifiée Daily Review                      ║
║      Rappel quotidien 18:00 pour revue notes                 ║
║                                                              ║
║  ☁️ SYNCHRONISATION                                          ║
║  [ ] Configurer sync OneDrive                                ║
║  [ ] Configurer sync Git                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script configuration Obsidian:**
```powershell
param([string]$VaultPath)

$ObsidianPath = Join-Path $VaultPath ".obsidian"
New-Item -ItemType Directory -Path $ObsidianPath -Force | Out-Null

# Configuration principale
$AppJson = @{
    "alwaysUpdateLinks" = $true
    "newFileLocation" = "folder"
    "newFileFolderPath" = "_Inbox"
    "attachmentFolderPath" = "_Attachments"
    "useMarkdownLinks" = $false
    "showLineNumber" = $true
    "foldHeading" = $true
    "foldIndent" = $true
} | ConvertTo-Json -Depth 10
$AppJson | Out-File (Join-Path $ObsidianPath "app.json") -Encoding UTF8

# Plugins activés
$CorePlugins = @{
    "file-explorer" = $true
    "global-search" = $true
    "graph" = $true
    "backlink" = $true
    "outgoing-link" = $true
    "tag-pane" = $true
    "page-preview" = $true
    "daily-notes" = $true
    "templates" = $true
    "command-palette" = $true
    "starred" = $true
    "outline" = $true
} | ConvertTo-Json
$CorePlugins | Out-File (Join-Path $ObsidianPath "core-plugins.json") -Encoding UTF8

# Configuration Daily Notes
$DailyNotes = @{
    "folder" = "_Daily"
    "format" = "YYYY-MM-DD"
    "template" = "_Templates/Template-Daily.md"
} | ConvertTo-Json
$DailyNotes | Out-File (Join-Path $ObsidianPath "daily-notes.json") -Encoding UTF8

Write-Host "✅ Configuration Obsidian créée"
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
║  C:\Users\r2d2\Documents\Knowledge                           ║
║                                                              ║
║  ✅ CRÉÉ:                                                    ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ • 9 dossiers de structure                               │ ║
║  │ • 5 templates de notes                                  │ ║
║  │ • INDEX.md principal                                    │ ║
║  │ • Configuration Obsidian                                │ ║
║  │ • Alias PowerShell (know-*)                             │ ║
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
```powershell
param([string]$BasePath)

# Créer INDEX.md
$IndexContent = @"
---
title: Index Principal
type: index
date: $(Get-Date -Format "yyyy-MM-dd")
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
- [[_Daily/$(Get-Date -Format "yyyy-MM-dd")|Aujourd'hui]]
- Voir dossier [[_Daily|Daily Notes]]

## Statistiques
- Notes totales: {à mettre à jour}
- Dernière mise à jour: $(Get-Date -Format "yyyy-MM-dd HH:mm")

## À Traiter
![[_Inbox]]

---
*Base créée le $(Get-Date -Format "yyyy-MM-dd")*
"@

$IndexContent | Out-File (Join-Path $BasePath "_Index\INDEX.md") -Encoding UTF8

# Créer README
$ReadmeContent = @"
# 🧠 Base de Connaissances

## Structure
- `_Index/` - Index et navigation
- `_Daily/` - Notes quotidiennes
- `_Inbox/` - Notes à traiter
- `_Templates/` - Modèles
- `Conversations/` - Résumés conversations Claude
- `Concepts/` - Notes atomiques (Zettelkasten)
- `Projets/` - Notes par projet
- `Code/` - Snippets et scripts
- `Références/` - Documentation

## Commandes
- `/know-save` - Sauvegarder conversation
- `/know-search "terme"` - Rechercher
- `/know-export obsidian` - Exporter

## Conventions
- Noms: `YYYY-MM-DD_Type_Sujet.md`
- Tags: `#domaine/sous-domaine`
- Liens: `[[NomNote]]`

Créé le $(Get-Date -Format "yyyy-MM-dd")
"@

$ReadmeContent | Out-File (Join-Path $BasePath "README.md") -Encoding UTF8

Write-Host "✅ Base de connaissances initialisée: $BasePath"
```
