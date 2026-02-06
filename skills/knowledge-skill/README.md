# 🧠 Super Agent Knowledge Capture

Agent intelligent de capture, résumé et organisation des connaissances extraites des conversations Claude.

## ✨ Fonctionnalités

- 💾 **Sauvegarde automatique** des conversations avec résumé
- 🔍 **Extraction intelligente** de code, décisions, actions
- 🏷️ **Tags hiérarchiques** pour organisation
- 🔗 **Liens bidirectionnels** entre notes (Zettelkasten)
- 📤 **Export** vers Obsidian, Notion, JSON
- 📊 **Index et statistiques** de la base

## 📦 Installation

```powershell
# Extraire dans le dossier skills
Expand-Archive -Path "knowledge-skill.zip" -DestinationPath "$env:USERPROFILE\.claude\skills\" -Force

# Vérifier
Get-ChildItem "$env:USERPROFILE\.claude\skills\knowledge-skill"
```

## 🚀 Démarrage Rapide

```powershell
# 1. Configuration initiale
/know-wizard setup

# 2. Sauvegarder une conversation
/know-save --quick "Titre de la conversation"

# 3. Rechercher
/know-search "terme"
```

## 📋 Commandes

| Commande | Description |
|----------|-------------|
| `/know-save` | Sauvegarder conversation |
| `/know-save --full` | Extraction complète |
| `/know-search "terme"` | Rechercher |
| `/know-search tag:#tag` | Rechercher par tag |
| `/know-export obsidian` | Export Obsidian |
| `/know-export json` | Export JSON |
| `/know-wizard setup` | Configuration initiale |
| `/know-wizard review` | Revue quotidienne |

## 📁 Structure

```
Knowledge\
├── _Index\           # Navigation
├── _Daily\           # Notes quotidiennes
├── _Inbox\           # À traiter
├── _Templates\       # Modèles
├── Conversations\    # Résumés Claude
├── Concepts\         # Notes atomiques
├── Projets\          # Par projet
├── Code\             # Snippets
└── Références\       # Documentation
```

## 🏷️ Système de Tags

### Format
```
#domaine/sous-domaine/spécifique
```

### Exemples
```
#dev/powershell/automation
#infra/proxmox/cluster
#projet/multipass
```

## 📝 Format des Notes

### Frontmatter YAML
```yaml
---
id: 20260204-083000
title: Configuration Super Agent
date: 2026-02-04
type: conversation
tags: [dev, claude-code]
status: processed
related: [[Note1], [Note2]]
---
```

### Liens Wikilinks
```markdown
[[Nom de la Note]]
[[Note|Alias]]
[[Note#Section]]
```

## 🔗 Intégration Obsidian

Export automatique compatible :
- Structure de dossiers
- Frontmatter YAML
- Wikilinks `[[]]`
- Tags hiérarchiques
- Graph view

```powershell
/know-export obsidian --dest="C:\Obsidian\Vault"
```

## 📊 Méthode Zettelkasten

1. **Notes atomiques** : 1 idée = 1 note
2. **Titre = résumé** de l'idée
3. **Liens** vers autres notes
4. **Tags** pour navigation
5. **Revue régulière** pour connexions

## 💡 Best Practices

### Capture
- Sauvegarder après chaque conversation importante
- Extraire le code et les décisions
- Ajouter 3-5 tags pertinents

### Organisation
- Traiter l'Inbox quotidiennement
- Créer des notes de concept atomiques
- Mettre à jour l'index hebdomadairement

### Revue
- Daily: 5 minutes
- Weekly: 30 minutes
- Monthly: 2 heures

## 📚 Références

- [Zettelkasten Method](https://zettelkasten.de/)
- [Building a Second Brain](https://www.buildingasecondbrain.com/)
- [How to Take Smart Notes](https://www.soenkeahrens.de/en/takesmartnotes)

---

**Version**: 1.0.0  
**Compatibilité**: Windows 11, PowerShell 7.4+, Obsidian  
**Dernière mise à jour**: Février 2026
