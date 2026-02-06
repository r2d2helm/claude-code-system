# 🗂️ Super Agent Obsidian Administration

Agent intelligent pour administrer, maintenir et optimiser les vaults Obsidian.

## Philosophie

> "Un vault bien entretenu est un second cerveau performant."

Cet agent automatise la maintenance, détecte les problèmes et optimise l'organisation de vos vaults Obsidian.

## Compatibilité

| Composant | Support |
|-----------|---------|
| Windows | 11/Server 2025 |
| PowerShell | 7.4+ |
| Obsidian | 1.4+ |
| Format | Markdown (.md) |

## Commandes Slash

### 🔍 Analyse & Santé

| Commande | Description |
|----------|-------------|
| `/obs-health` | Diagnostic complet du vault |
| `/obs-stats` | Statistiques détaillées |
| `/obs-graph` | Analyse du graphe de liens [PREVU] |
| `/obs-orphans` | Détecter notes orphelines |

### 🔗 Gestion des Liens

| Commande | Description |
|----------|-------------|
| `/obs-links broken` | Trouver liens cassés |
| `/obs-links unlinked` | Notes sans liens [PREVU] |
| `/obs-links suggest` | Suggérer connexions [PREVU] |
| `/obs-links fix` | Réparer liens cassés [PREVU] |

### 🏷️ Gestion des Tags

| Commande | Description |
|----------|-------------|
| `/obs-tags list` | Lister tous les tags |
| `/obs-tags unused` | Tags non utilisés [PREVU] |
| `/obs-tags rename` | Renommer un tag [PREVU] |
| `/obs-tags merge` | Fusionner des tags [PREVU] |
| `/obs-tags hierarchy` | Afficher hiérarchie [PREVU] |

### 📁 Organisation

| Commande | Description |
|----------|-------------|
| `/obs-structure` | Analyser structure dossiers [PREVU] |
| `/obs-move` | Déplacer notes intelligemment [PREVU] |
| `/obs-rename` | Renommer avec conventions [PREVU] |
| `/obs-frontmatter` | Gérer métadonnées YAML |
| `/obs-templates` | Gérer templates [PREVU] |

### 🧹 Maintenance

| Commande | Description |
|----------|-------------|
| `/obs-clean` | Nettoyage général |
| `/obs-duplicates` | Détecter doublons [PREVU] |
| `/obs-attachments` | Gérer pièces jointes [PREVU] |
| `/obs-empty` | Supprimer notes vides [PREVU] |

### 💾 Backup & Export

| Commande | Description |
|----------|-------------|
| `/obs-backup` | Sauvegarder le vault |
| `/obs-export` | Exporter (PDF, HTML, JSON) [PREVU] |
| `/obs-sync` | Synchroniser vaults [PREVU] |

### ⚙️ Configuration

| Commande | Description |
|----------|-------------|
| `/obs-config` | Gérer configuration Obsidian [PREVU] |
| `/obs-plugins` | Gérer plugins [PREVU] |
| `/obs-hotkeys` | Gérer raccourcis [PREVU] |

### 🧙 Wizards

| Commande | Description |
|----------|-------------|
| `/obs-wizard audit` | Audit complet du vault [PREVU] |
| `/obs-wizard cleanup` | Nettoyage guidé [PREVU] |
| `/obs-wizard reorganize` | Réorganisation assistée [PREVU] |

## Diagnostic de Santé

### Score de Santé (0-100)

```
╔══════════════════════════════════════════════════════════════╗
║                 🏥 SANTÉ DU VAULT                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Score Global: 78/100  ████████████████░░░░                  ║
║                                                              ║
║  📊 DÉTAILS:                                                 ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Liens cassés        : 3    (-5 pts)  ⚠️                 │ ║
║  │ Notes orphelines    : 12   (-8 pts)  ⚠️                 │ ║
║  │ Tags incohérents    : 5    (-4 pts)  ⚠️                 │ ║
║  │ Doublons            : 0    (OK)      ✅                 │ ║
║  │ Frontmatter manquant: 23   (-5 pts)  ⚠️                 │ ║
║  │ Attachments orphelins: 8   (OK)      ℹ️                 │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  💡 RECOMMANDATIONS:                                         ║
║  1. Réparer 3 liens cassés avec /obs-links fix               ║
║  2. Lier 12 notes orphelines avec /obs-links suggest         ║
║  3. Normaliser tags avec /obs-tags rename                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Critères d'Évaluation

| Critère | Points | Description |
|---------|--------|-------------|
| Pas de liens cassés | 20 | Tous les [[liens]] pointent vers des notes existantes |
| Notes connectées | 20 | Pas de notes orphelines (sans liens entrants/sortants) |
| Tags cohérents | 15 | Pas de tags en double ou mal formatés |
| Frontmatter complet | 15 | Toutes les notes ont des métadonnées |
| Pas de doublons | 10 | Pas de fichiers identiques |
| Structure organisée | 10 | Profondeur < 4 niveaux, dossiers cohérents |
| Attachments liés | 10 | Pas de fichiers médias orphelins |

## Détection des Problèmes

### Liens Cassés

```powershell
# Détecte les [[liens]] qui pointent vers des notes inexistantes
/obs-links broken

# Résultat:
╔═══════════════════════════════════════════════════════════╗
║  🔗 LIENS CASSÉS: 3 trouvés                               ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  📄 Projets/MultiPass/Architecture.md                     ║
║     └─ [[API-Design]] → Note n'existe pas                 ║
║     └─ [[Database-Schema]] → Note n'existe pas            ║
║                                                           ║
║  📄 Concepts/C_Zettelkasten.md                            ║
║     └─ [[Luhmann-Bio]] → Note n'existe pas                ║
║                                                           ║
║  [1] Créer notes manquantes  [2] Supprimer liens          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Notes Orphelines

```powershell
# Notes sans liens entrants ni sortants
/obs-orphans

# Résultat:
╔═══════════════════════════════════════════════════════════╗
║  🏝️ NOTES ORPHELINES: 12 trouvées                         ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Sans liens entrants (personne ne pointe vers):           ║
║  • _Inbox/Note-Rapide-2026-01-15.md                       ║
║  • Conversations/2026-01-20_Conv_Docker.md                ║
║  • Code/Python/script-test.md                             ║
║                                                           ║
║  Sans liens sortants (ne pointe vers rien):               ║
║  • Concepts/C_Microservices.md                            ║
║  • Références/R_AWS-Documentation.md                      ║
║                                                           ║
║  💡 Suggestions de liens...                               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Tags Problématiques

```powershell
/obs-tags list

# Détecte:
# - Tags similaires: #proxmox vs #Proxmox vs #pve
# - Tags orphelins: utilisés une seule fois
# - Tags mal formés: espaces, caractères spéciaux
```

## Maintenance Automatisée

### Nettoyage Complet

```powershell
/obs-clean --all

# Actions:
# 1. Supprimer fichiers temporaires (.tmp, .bak)
# 2. Nettoyer cache Obsidian
# 3. Supprimer notes vides
# 4. Optimiser attachments
# 5. Reconstruire index
```

### Gestion des Attachments

```powershell
/obs-attachments

╔═══════════════════════════════════════════════════════════╗
║  📎 ANALYSE ATTACHMENTS                                   ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Total: 156 fichiers (234 MB)                             ║
║                                                           ║
║  Par type:                                                ║
║  • Images (png, jpg): 98 fichiers (45 MB)                 ║
║  • PDF: 34 fichiers (156 MB)                              ║
║  • Autres: 24 fichiers (33 MB)                            ║
║                                                           ║
║  ⚠️ PROBLÈMES:                                            ║
║  • 12 attachments non référencés (orphelins)              ║
║  • 3 images dupliquées                                    ║
║  • 5 fichiers > 10 MB                                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

## Organisation du Frontmatter

### Standard YAML

```yaml
---
id: 20260204-143022
title: Titre de la Note
date: 2026-02-04
type: conversation | concept | code | reference | project
tags: [tag1, tag2]
status: draft | active | review | archived
aliases: [alias1, alias2]
related: [[Note1]], [[Note2]]
created: 2026-02-04T14:30:22
modified: 2026-02-04T15:45:00
---
```

### Commandes Frontmatter

```powershell
# Ajouter frontmatter manquant
/obs-frontmatter add --template=default

# Mettre à jour dates
/obs-frontmatter update-dates

# Ajouter un champ à toutes les notes
/obs-frontmatter add-field status=draft

# Valider frontmatter
/obs-frontmatter validate
```

## Backup & Synchronisation

### Backup Automatique

```powershell
/obs-backup

╔═══════════════════════════════════════════════════════════╗
║  💾 BACKUP DU VAULT                                       ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Source: C:\Users\r2d2\Documents\Knowledge                ║
║  Destination: D:\Backups\Knowledge                        ║
║                                                           ║
║  📊 CONTENU:                                              ║
║  • 456 notes Markdown                                     ║
║  • 156 attachments                                        ║
║  • Configuration Obsidian                                 ║
║                                                           ║
║  📦 ARCHIVE CRÉÉE:                                        ║
║  Knowledge_2026-02-04_143022.zip (45 MB)                  ║
║                                                           ║
║  🔄 Rotation: 5 derniers backups conservés                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Options de Backup

```powershell
/obs-backup --dest="D:\Backups"           # Destination personnalisée
/obs-backup --exclude=".obsidian"         # Exclure config
/obs-backup --incremental                 # Backup incrémental
/obs-backup --git                         # Commit Git
```

## Scripts PowerShell

### Chemin du Vault

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
```

### Trouver Liens Cassés

```powershell
function Find-BrokenLinks {
    param([string]$VaultPath)
    
    $Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
    $NoteNames = $Notes | ForEach-Object { $_.BaseName }
    $BrokenLinks = @()
    
    foreach ($Note in $Notes) {
        $Content = Get-Content $Note.FullName -Raw
        $Links = [regex]::Matches($Content, '\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
        
        foreach ($Link in $Links) {
            $Target = $Link.Groups[1].Value
            if ($Target -notin $NoteNames) {
                $BrokenLinks += [PSCustomObject]@{
                    Source = $Note.FullName
                    Target = $Target
                }
            }
        }
    }
    
    return $BrokenLinks
}
```

### Trouver Notes Orphelines

```powershell
function Find-OrphanNotes {
    param([string]$VaultPath)
    
    $Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
    $AllLinks = @()
    
    # Collecter tous les liens
    foreach ($Note in $Notes) {
        $Content = Get-Content $Note.FullName -Raw
        $Links = [regex]::Matches($Content, '\[\[([^\]|]+)') |
            ForEach-Object { $_.Groups[1].Value }
        $AllLinks += $Links
    }
    
    # Trouver notes jamais référencées
    $Orphans = $Notes | Where-Object {
        $_.BaseName -notin $AllLinks
    }
    
    return $Orphans
}
```

### Statistiques du Vault

```powershell
function Get-VaultStats {
    param([string]$VaultPath)
    
    $Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
    $Attachments = Get-ChildItem -Path $VaultPath -Recurse -Include "*.png","*.jpg","*.pdf"
    
    $TotalWords = 0
    $TotalLinks = 0
    $TotalTags = @()
    
    foreach ($Note in $Notes) {
        $Content = Get-Content $Note.FullName -Raw
        $TotalWords += ($Content -split '\s+').Count
        $TotalLinks += ([regex]::Matches($Content, '\[\[')).Count
        $TotalTags += [regex]::Matches($Content, '#[\w/-]+') | 
            ForEach-Object { $_.Value }
    }
    
    return [PSCustomObject]@{
        Notes = $Notes.Count
        Words = $TotalWords
        Links = $TotalLinks
        UniqueTags = ($TotalTags | Select-Object -Unique).Count
        Attachments = $Attachments.Count
        Size = "{0:N2} MB" -f (($Notes + $Attachments | 
            Measure-Object -Property Length -Sum).Sum / 1MB)
    }
}
```

## Intégration Knowledge Agent

### Workflow Combiné

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Knowledge Agent          Obsidian Agent                   │
│   ───────────────          ──────────────                   │
│   /know-save               /obs-health                      │
│   /know-search             /obs-links fix                   │
│   /know-export             /obs-clean                       │
│        │                        │                           │
│        └──────────┬─────────────┘                           │
│                   │                                         │
│                   ▼                                         │
│          ┌───────────────┐                                  │
│          │  Vault Sain   │                                  │
│          │  & Organisé   │                                  │
│          └───────────────┘                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Routine de Maintenance

| Fréquence | Commande | Action |
|-----------|----------|--------|
| Quotidien | `/obs-health --quick` | Check rapide |
| Hebdo | `/obs-wizard cleanup` | Nettoyage guidé |
| Mensuel | `/obs-wizard audit` | Audit complet |
| Mensuel | `/obs-backup` | Backup complet |

## Références

- [Obsidian Documentation](https://help.obsidian.md/)
- [Obsidian API](https://docs.obsidian.md/)
- [Dataview Plugin](https://blacksmithgu.github.io/obsidian-dataview/)
