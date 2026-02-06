# 📁 Super Agent File Organizer Windows

Agent intelligent de gestion et organisation des fichiers et dossiers Windows avec automatisation PowerShell et best practices 2025-2026.

## ✨ Fonctionnalités

- 🗂️ **Organisation automatique** par type, date ou projet
- 📝 **Renommage intelligent** avec conventions ISO 8601
- 🔍 **Analyse et audit** de la qualité d'organisation
- 🧹 **Nettoyage** fichiers temporaires et doublons
- 🔄 **Détection doublons** par hash MD5
- ⚙️ **Automatisation** via tâches planifiées
- 🧙 **Wizards interactifs** pour configuration guidée

## 📦 Installation

```powershell
# Extraire dans le dossier skills
Expand-Archive -Path "fileorg-skill.zip" -DestinationPath "$env:USERPROFILE\.claude\skills\" -Force

# Vérifier
Get-ChildItem "$env:USERPROFILE\.claude\skills\fileorg-skill"
```

## 📋 Commandes

### Organisation
| Commande | Description |
|----------|-------------|
| `/file-organize` | Organiser fichiers par type/date/projet |
| `/file-structure` | Créer structure de dossiers |
| `/file-sort` | Trier dans sous-dossiers |

### Nommage
| Commande | Description |
|----------|-------------|
| `/file-rename iso-date` | Ajouter préfixe date ISO |
| `/file-rename normalize` | Normaliser noms (espaces, accents) |
| `/file-rename version` | Gérer versions (v01, v02) |
| `/file-rename bulk` | Renommage en masse |

### Analyse
| Commande | Description |
|----------|-------------|
| `/file-analyze` | Statistiques et structure |
| `/file-analyze audit` | Score qualité organisation |
| `/file-duplicates` | Détecter doublons |

### Nettoyage
| Commande | Description |
|----------|-------------|
| `/file-clean temp` | Nettoyer fichiers temporaires |
| `/file-clean downloads` | Nettoyer anciens téléchargements |
| `/file-clean empty` | Supprimer dossiers vides |

### Wizards
| Commande | Description |
|----------|-------------|
| `/file-wizard setup` | Configuration initiale complète |
| `/file-wizard photos` | Organiser bibliothèque photos |

## 📝 Convention de Nommage

### Format Standard
```
{DATE}_{CATEGORIE}_{DESCRIPTION}_{VERSION}.{EXT}
```

### Exemples
```
2026-02-03_Facture_EDF-Janvier_v01.pdf
2026-02-03_Rapport_Analyse-Marche_v02.docx
2026-02-03_Photo_Vacances-Bretagne_001.jpg
```

### Règles
| Élément | Bonne pratique | Éviter |
|---------|----------------|--------|
| Date | `2026-02-03` | `03/02/26` |
| Séparateurs | `_` et `-` | espaces |
| Caractères | alphanumériques | `é@#$%` |
| Versions | `v01`, `v02` | `final`, `v1` |

## 📂 Structure Recommandée

```
Documents\
├── _INBOX\              # Fichiers à trier
├── _ARCHIVE\            # Par année
│   └── {YYYY}\
├── Administratif\
│   ├── Banque\
│   ├── Impots\
│   └── Factures\
├── Projets\
│   └── {NomProjet}\
├── Travail\
└── Personnel\
```

## 💡 Exemples d'Usage

```powershell
# Organiser Downloads par type
/file-organize downloads

# Ajouter dates ISO aux fichiers
/file-rename iso-date "$env:USERPROFILE\Documents"

# Scanner doublons
/file-duplicates scan "$env:USERPROFILE"

# Audit organisation
/file-analyze audit "$env:USERPROFILE\Documents"

# Configuration complète
/file-wizard setup
```

## 🎯 Score d'Organisation

| Score | Niveau | Action |
|-------|--------|--------|
| 90-100 | 🟢 Excellent | Maintenir |
| 70-89 | 🟡 Bon | Améliorations mineures |
| 50-69 | 🟠 Moyen | Réorganisation |
| < 50 | 🔴 Critique | Wizard urgent |

## 📚 Références

- [ISO 8601 Date Format](https://www.iso.org/iso-8601-date-and-time-format.html)
- [File Naming Best Practices - Harvard](https://datamanagement.hms.harvard.edu/plan-design/file-naming-conventions)
- [PARA Method - Tiago Forte](https://fortelabs.com/blog/para/)

---

**Version**: 1.0.0  
**Compatibilité**: Windows 11/Server 2025, PowerShell 7.4+  
**Dernière mise à jour**: Février 2026
