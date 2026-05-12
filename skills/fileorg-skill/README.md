# Super Agent File Organizer Linux

Agent intelligent de gestion et organisation des fichiers et dossiers Linux avec automatisation bash et best practices 2025-2026.

## Fonctionnalites

- Organisation automatique par type, date ou projet
- Renommage intelligent avec conventions ISO 8601
- Analyse et audit de la qualite d'organisation
- Nettoyage fichiers temporaires et doublons
- Detection doublons par hash MD5
- Automatisation via cron et systemd
- Wizards interactifs pour configuration guidee

## Installation

```bash
# Extraire dans le dossier skills
unzip fileorg-skill.zip -d ~/.claude/skills/

# Verifier
ls ~/.claude/skills/fileorg-skill
```

## Commandes

### Organisation
| Commande | Description |
|----------|-------------|
| `/file-organize` | Organiser fichiers par type/date/projet |
| `/file-structure` | Creer structure de dossiers |
| `/file-sort` | Trier dans sous-dossiers |

### Nommage
| Commande | Description |
|----------|-------------|
| `/file-rename iso-date` | Ajouter prefixe date ISO |
| `/file-rename normalize` | Normaliser noms (espaces, accents) |
| `/file-rename version` | Gerer versions (v01, v02) |
| `/file-rename bulk` | Renommage en masse |

### Analyse
| Commande | Description |
|----------|-------------|
| `/file-analyze` | Statistiques et structure |
| `/file-analyze audit` | Score qualite organisation |
| `/file-duplicates` | Detecter doublons |

### Nettoyage
| Commande | Description |
|----------|-------------|
| `/file-clean temp` | Nettoyer fichiers temporaires |
| `/file-clean downloads` | Nettoyer anciens telechargements |
| `/file-clean empty` | Supprimer dossiers vides |

### Wizards
| Commande | Description |
|----------|-------------|
| `/file-wizard setup` | Configuration initiale complete |
| `/file-wizard photos` | Organiser bibliotheque photos |

## Convention de Nommage

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

### Regles
| Element | Bonne pratique | Eviter |
|---------|----------------|--------|
| Date | `2026-02-03` | `03/02/26` |
| Separateurs | `_` et `-` | espaces |
| Caracteres | alphanumeriques | `e@#$%` |
| Versions | `v01`, `v02` | `final`, `v1` |

## Structure Recommandee

```
Documents/
├── _INBOX/              # Fichiers a trier
├── _ARCHIVE/            # Par annee
│   └── {YYYY}/
├── Administratif/
│   ├── Banque/
│   ├── Impots/
│   └── Factures/
├── Projets/
│   └── {NomProjet}/
├── Travail/
└── Personnel/
```

## Exemples d'Usage

```bash
# Organiser Downloads par type
/file-organize downloads

# Ajouter dates ISO aux fichiers
/file-rename iso-date ~/Documents

# Scanner doublons
/file-duplicates scan ~/

# Audit organisation
/file-analyze audit ~/Documents

# Configuration complete
/file-wizard setup
```

## Score d'Organisation

| Score | Niveau | Action |
|-------|--------|--------|
| 90-100 | Excellent | Maintenir |
| 70-89 | Bon | Ameliorations mineures |
| 50-69 | Moyen | Reorganisation |
| < 50 | Critique | Wizard urgent |

## References

- [ISO 8601 Date Format](https://www.iso.org/iso-8601-date-and-time-format.html)
- [File Naming Best Practices - Harvard](https://datamanagement.hms.harvard.edu/plan-design/file-naming-conventions)
- [PARA Method - Tiago Forte](https://fortelabs.com/blog/para/)

---

**Version**: 1.0.0
**Compatibilite**: Ubuntu 22.04+, bash 5+
**Derniere mise a jour**: Fevrier 2026
