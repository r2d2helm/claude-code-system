# 🗂️ Super Agent Obsidian Administration

Agent intelligent pour administrer, maintenir et optimiser les vaults Obsidian.

## ✨ Fonctionnalités

- 🏥 **Diagnostic de santé** avec score 0-100
- 🔗 **Gestion des liens** : cassés, orphelins, suggestions
- 🏷️ **Gestion des tags** : normalisation, fusion, hiérarchie
- 🧹 **Nettoyage** : notes vides, attachments orphelins, doublons
- 💾 **Backup** automatisé avec rotation
- 📊 **Statistiques** détaillées du vault

## 📦 Installation

```powershell
# Extraire dans le dossier skills
Expand-Archive -Path "obsidian-skill.zip" -DestinationPath "$env:USERPROFILE\.claude\skills\" -Force

# Vérifier
Get-ChildItem "$env:USERPROFILE\.claude\skills\obsidian-skill"
```

## 🚀 Commandes Principales

### Diagnostic

```powershell
/obs-health              # Diagnostic complet
/obs-health --quick      # Check rapide
/obs-stats               # Statistiques détaillées
```

### Liens

```powershell
/obs-links broken        # Trouver liens cassés
/obs-links fix           # Réparer liens
/obs-links suggest       # Suggérer connexions
/obs-orphans             # Notes orphelines
```

### Tags

```powershell
/obs-tags list           # Lister tous les tags
/obs-tags hierarchy      # Afficher hiérarchie
/obs-tags rename "#old" "#new"    # Renommer
/obs-tags merge "#a,#b" --into="#c"   # Fusionner
```

### Nettoyage

```powershell
/obs-clean               # Analyser
/obs-clean --all         # Nettoyer tout
/obs-clean attachments   # Gérer attachments
/obs-clean duplicates    # Détecter doublons
```

### Backup

```powershell
/obs-backup              # Backup complet
/obs-backup --dest="D:\Backups"   # Destination custom
```

### Wizards

```powershell
/obs-wizard audit        # Audit complet guidé
/obs-wizard cleanup      # Nettoyage guidé
```

## 📊 Score de Santé

Le diagnostic calcule un score sur 100 :

| Critère | Points |
|---------|--------|
| Pas de liens cassés | 20 |
| Notes connectées | 20 |
| Tags cohérents | 15 |
| Frontmatter complet | 15 |
| Pas de doublons | 10 |
| Structure organisée | 10 |
| Attachments liés | 10 |

## 🔧 Configuration

Par défaut, le vault est :
```
C:\Users\{User}\Documents\Knowledge
```

Pour un autre vault :
```powershell
/obs-health --vault="D:\MonVault"
```

## 📋 Intégration Knowledge Agent

| Knowledge Agent | Obsidian Agent |
|-----------------|----------------|
| `/know-save` | `/obs-health` |
| `/know-search` | `/obs-links suggest` |
| `/know-export` | `/obs-backup` |

Workflow recommandé :
1. Capturer avec Knowledge Agent
2. Maintenir avec Obsidian Agent
3. Visualiser dans Obsidian

## 📅 Routine de Maintenance

| Fréquence | Action |
|-----------|--------|
| Quotidien | `/obs-health --quick` |
| Hebdo | `/obs-clean` |
| Mensuel | `/obs-wizard audit` |
| Mensuel | `/obs-backup` |

---

**Version**: 1.0.0  
**Compatibilité**: Windows 11, PowerShell 7.4+, Obsidian 1.4+  
**Dernière mise à jour**: Février 2026
