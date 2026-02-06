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
║  │ Titre: Configuration Super Agent Windows                │ ║
║  │                                                         │ ║
║  │ Discussion sur la création d'un agent Windows pour      │ ║
║  │ Claude Code avec 36 commandes PowerShell et 10 wizards. │ ║
║  │ Installation et test du système de routing automatique. │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  🏷️ TAGS SUGGÉRÉS:                                           ║
║  #dev/claude-code #infra/windows #projet/multipass          ║
║  #skill #powershell #automation                              ║
║                                                              ║
║  [1] Sauvegarder  [2] Modifier  [3] Ajouter tags             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
param(
    [string]$KnowledgePath = "$env:USERPROFILE\Documents\Knowledge",
    [string]$Title,
    [string[]]$Tags,
    [switch]$AutoExtract
)

$Date = Get-Date -Format "yyyy-MM-dd"
$Time = Get-Date -Format "HHmmss"
$ID = "$Date-$Time"

# Créer structure si nécessaire
$Folders = @(
    "Conversations",
    "Concepts", 
    "Code",
    "_Index",
    "_Daily",
    "_Inbox"
)
foreach ($Folder in $Folders) {
    $Path = Join-Path $KnowledgePath $Folder
    if (!(Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

# Générer fichier de conversation
$FileName = "{0}_Conv_{1}.md" -f $Date, ($Title -replace '\s+', '-' -replace '[^\w\-]', '')
$FilePath = Join-Path $KnowledgePath "Conversations\$FileName"

$TagsYaml = ($Tags | ForEach-Object { "`"$_`"" }) -join ", "

$Content = @"
---
id: $ID
title: $Title
date: $Date
type: conversation
tags: [$TagsYaml]
source: Claude
status: captured
related: []
---

# $Title

## Résumé
{À compléter - résumé de la conversation}

## Points Clés
- 
- 
- 

## Décisions Prises
- [ ] 

## Code/Commandes Extraits
``````powershell
# Code extrait de la conversation
``````

## Concepts Liés
- [[]]

## Actions Suivantes
- [ ] 

## Notes Additionnelles


---
*Capturé le $Date depuis conversation Claude*
"@

$Content | Out-File -FilePath $FilePath -Encoding UTF8
Write-Host "✅ Conversation sauvegardée: $FilePath"

# Mettre à jour Daily Note
$DailyPath = Join-Path $KnowledgePath "_Daily\$Date.md"
if (!(Test-Path $DailyPath)) {
    $DailyContent = @"
---
date: $Date
type: daily
tags: [daily]
---

# 📅 $Date

## Conversations du Jour
"@
    $DailyContent | Out-File -FilePath $DailyPath -Encoding UTF8
}

# Ajouter lien dans Daily
Add-Content -Path $DailyPath -Value "- [[$FileName]]"
```

### /know-save --quick "titre"

Sauvegarde rapide avec titre :

```powershell
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
║  │ ✓ Conversations\2026-02-04_Conv_Windows-Agent.md        │ ║
║  │ ✓ Code\PowerShell\2026-02-04_Install-Skills.ps1         │ ║
║  │ ✓ Code\PowerShell\2026-02-04_Organize-Files.ps1         │ ║
║  │ ✓ Concepts\C_Meta-Router-Pattern.md                     │ ║
║  │ ✓ Concepts\C_Skill-Structure.md                         │ ║
║  │ ✓ _Daily\2026-02-04.md (mis à jour)                     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📊 EXTRACTION:                                              ║
║  • 5 blocs de code → Code/PowerShell/                        ║
║  • 2 concepts identifiés → Concepts/                         ║
║  • 3 décisions → Section Décisions                           ║
║  • 12 tags appliqués                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /know-save --template {template}

Utiliser un template spécifique :

```powershell
/know-save --template meeting     # Pour réunion
/know-save --template debug       # Pour session debug
/know-save --template learning    # Pour apprentissage
/know-save --template project     # Pour projet
```

## Extraction Automatique

### Éléments Détectés

| Élément | Pattern | Action |
|---------|---------|--------|
| Code PowerShell | ` ```powershell ` | Extrait vers `Code/PowerShell/` |
| Code Python | ` ```python ` | Extrait vers `Code/Python/` |
| Commandes | `/command` | Liste dans section Commandes |
| URLs | `http(s)://` | Liste dans Références |
| Décisions | "décidé", "choisi" | Section Décisions |
| TODOs | "à faire", "todo" | Section Actions |

### Script d'Extraction

```powershell
function Extract-ConversationElements {
    param([string]$Content)
    
    $Elements = @{
        Code = @()
        URLs = @()
        Decisions = @()
        Actions = @()
        Concepts = @()
    }
    
    # Extraire blocs de code
    $CodePattern = '```(\w+)\r?\n([\s\S]*?)```'
    $Matches = [regex]::Matches($Content, $CodePattern)
    foreach ($Match in $Matches) {
        $Elements.Code += @{
            Language = $Match.Groups[1].Value
            Content = $Match.Groups[2].Value
        }
    }
    
    # Extraire URLs
    $URLPattern = 'https?://[^\s\)\]>]+'
    $Elements.URLs = [regex]::Matches($Content, $URLPattern) | 
        ForEach-Object { $_.Value } | 
        Select-Object -Unique
    
    # Détecter décisions
    $DecisionPatterns = @("décidé", "choisi", "opté pour", "on va utiliser")
    foreach ($Pattern in $DecisionPatterns) {
        $Lines = $Content -split "`n" | Where-Object { $_ -match $Pattern }
        $Elements.Decisions += $Lines
    }
    
    # Détecter actions
    $ActionPatterns = @("à faire", "todo", "prochaine étape", "il faut")
    foreach ($Pattern in $ActionPatterns) {
        $Lines = $Content -split "`n" | Where-Object { $_ -match $Pattern }
        $Elements.Actions += $Lines
    }
    
    return $Elements
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

```powershell
# Sauvegarde rapide
/know-save --quick "Debug API Proxmox"

# Sauvegarde complète avec tags
/know-save --full --tags="#proxmox,#api,#debug"

# Associer à un projet
/know-save --project="MultiPass" --full

# Prévisualiser
/know-save --dry-run
```
