---
name: fileorg-skill
description: Organisation et gestion des fichiers Windows
prefix: /file-*
---

# 📁 Super Agent File Organizer Windows

Agent intelligent de gestion et organisation des fichiers et dossiers Windows avec automatisation, conventions de nommage et best practices 2025-2026.

## Philosophie

> "Un fichier bien nommé est un fichier déjà retrouvé."

Cet agent applique les standards internationaux (ISO 8601) et les meilleures pratiques d'organisation pour transformer le chaos numérique en structure efficace.

## Compatibilité

| Composant | Version |
|-----------|---------|
| Ubuntu Linux | 24.04+ |
| Bash | 5+ |
| Filesystem | ext4, btrfs |

## Commandes Slash

### Organisation

| Commande | Description |
|----------|-------------|
| `/file-organize` | Organiser fichiers par type, date ou projet |
| `/file-structure` | Créer/appliquer une structure de dossiers |
| `/file-sort` | Trier fichiers dans des sous-dossiers |
| `/file-flatten` | Aplatir une arborescence trop profonde |

### Nommage

| Commande | Description |
|----------|-------------|
| `/file-rename` | Renommer fichiers selon convention |
| `/file-prefix` | Ajouter préfixe date ISO aux fichiers |
| `/file-normalize` | Normaliser noms (espaces, caractères spéciaux) |
| `/file-version` | Gérer versions de fichiers (v01, v02...) |

### Analyse

| Commande | Description |
|----------|-------------|
| `/file-analyze` | Analyser structure et statistiques |
| `/file-audit` | Audit qualité nommage et organisation |
| `/file-duplicates` | Détecter fichiers en double |
| `/file-large` | Trouver gros fichiers |
| `/file-old` | Trouver fichiers anciens/obsolètes |

### Nettoyage

| Commande | Description |
|----------|-------------|
| `/file-clean` | Nettoyer fichiers temporaires/inutiles |
| `/file-empty` | Supprimer dossiers vides |
| `/file-archive` | Archiver anciens fichiers |
| `/file-trash` | Gérer la corbeille |

### Synchronisation

| Commande | Description |
|----------|-------------|
| `/file-backup` | Sauvegarder avec structure |
| `/file-sync` | Synchroniser deux dossiers |
| `/file-mirror` | Miroir de dossier |

### Wizards

| Commande | Description |
|----------|-------------|
| `/file-wizard` | Assistant configuration guidée |

## Syntaxe

```
/file-<commande> [action] [chemin] [options]
```

### Exemples

```bash
/file-organize downloads          # Organiser Téléchargements
/file-rename photos --iso-date    # Renommer photos avec date ISO
/file-duplicates ~/               # Trouver doublons
/file-clean temp                  # Nettoyer fichiers temporaires
/file-wizard setup                # Assistant configuration initiale
```

## Conventions de Nommage (Best Practices 2025-2026)

### Format Standard

```
[DATE]_[CATEGORIE]_[DESCRIPTION]_[VERSION].[EXT]
```

**Exemples:**
```
2026-02-03_Facture_Multipass-Design_v01.pdf
2026-02-03_Photo_Vacances-Bretagne_001.jpg
2026-02-03_Rapport_Analyse-Marche_v02-draft.docx
```

### Règles de Base

| Règle | Bonne pratique | Mauvais exemple |
|-------|----------------|-----------------|
| Date | `2026-02-03` (ISO 8601) | `03/02/2026`, `Feb 3` |
| Séparateurs | `_` entre éléments, `-` entre mots | espaces, points |
| Caractères | Alphanumériques uniquement | `é`, `@`, `#`, `&` |
| Longueur | < 30 caractères (hors extension) | noms très longs |
| Versions | `v01`, `v02` avec zéros | `v1`, `final`, `final2` |
| Casse | PascalCase ou kebab-case | mélange incohérent |

### Caractères Interdits

```
~ ! @ # $ % ^ & * ( ) ; : < > ? , { } ' " | / \
```

Remplacer par : `_` (underscore) ou `-` (tiret)

### Versionnage

| Type | Format | Exemple |
|------|--------|---------|
| Version majeure | `v01`, `v02` | Changement significatif |
| Version mineure | `v01.1`, `v01.2` | Corrections mineures |
| Draft | `v01-draft` | En cours de révision |
| Final | `v01-final` | Version approuvée |
| Archive | `v01-archive` | Ancienne version conservée |

## Structure de Dossiers Recommandée

### Structure Personnelle

```
~/
├── Documents/
│   ├── _INBOX/                    # Fichiers à traiter
│   ├── _ARCHIVE/                  # Anciens fichiers par année
│   │   ├── 2024/
│   │   └── 2025/
│   ├── Administratif/
│   │   ├── Banque/
│   │   ├── Impots/
│   │   ├── Assurances/
│   │   └── Factures/
│   ├── Projets/
│   │   ├── {NomProjet1}/
│   │   │   ├── 01-Brief/
│   │   │   ├── 02-Recherche/
│   │   │   ├── 03-Production/
│   │   │   ├── 04-Livrables/
│   │   │   └── 05-Archive/
│   │   └── {NomProjet2}/
│   ├── Travail/
│   │   └── {Entreprise}/
│   └── Personnel/
├── Pictures/
│   ├── {YYYY}/                    # Par année
│   │   └── {YYYY-MM}/             # Par mois
│   ├── Albums/
│   └── Screenshots/
├── Downloads/
│   └── (Auto-organisé)
└── Desktop/
    └── (Minimal - liens seulement)
```

### Structure Projet (PARA Method)

```
Projet\
├── 01-Projects\          # Projets actifs
├── 02-Areas\             # Responsabilités continues
├── 03-Resources\         # Références et ressources
└── 04-Archive\           # Projets terminés
```

### Limites Recommandées

| Élément | Limite | Raison |
|---------|--------|--------|
| Profondeur | 3-4 niveaux max | Navigation facile |
| Fichiers par dossier | < 100 | Performance |
| Longueur chemin | < 4096 caractères | Limite PATH_MAX Linux |
| Dossiers racine | 5-10 catégories | Clarté |

## Catégories de Fichiers

### Par Extension

| Catégorie | Extensions | Dossier suggéré |
|-----------|------------|-----------------|
| Documents | .doc, .docx, .pdf, .txt, .odt | Documents/ |
| Tableurs | .xls, .xlsx, .csv | Documents/Tableurs/ |
| Présentations | .ppt, .pptx | Documents/Presentations/ |
| Images | .jpg, .png, .gif, .webp, .svg | Pictures/ |
| Vidéos | .mp4, .mkv, .avi, .mov | Videos/ |
| Audio | .mp3, .wav, .flac, .m4a | Music/ |
| Archives | .zip, .rar, .7z, .tar | Downloads/Archives/ |
| Code | .py, .js, .ps1, .sh, .bat | Dev/Code/ |
| Données | .json, .xml, .sql, .db | Dev/Data/ |
| Exécutables | .exe, .msi, .appx | Downloads/Installers/ |

### Par Usage

| Usage | Rétention | Action |
|-------|-----------|--------|
| Temporaire | 7 jours | Auto-suppression |
| En cours | Actif | Dossier principal |
| Référence | Permanent | Resources/ |
| Archive | 1-7 ans | Archive/{Année}/ |
| Légal | 10+ ans | Archive/Legal/ |

## Automatisation

### Tâches Planifiées Recommandées

| Tâche | Fréquence | Description |
|-------|-----------|-------------|
| Organiser Downloads | Quotidien | Trier par type/date |
| Nettoyer Temp | Hebdomadaire | Supprimer fichiers temp > 7j |
| Détecter doublons | Mensuel | Scanner et rapporter |
| Archiver anciens | Mensuel | Déplacer fichiers > 1 an |
| Vider corbeille | Mensuel | Si > 1 GB |
| Rapport structure | Trimestriel | Audit organisation |

### Script Auto-Organisation

```bash
# Exemple: Organiser Downloads automatiquement
declare -A RULES=(
    ["Documents"]="pdf doc docx txt odt"
    ["Images"]="jpg jpeg png gif webp"
    ["Videos"]="mp4 mkv avi mov"
    ["Archives"]="zip rar 7z tar gz"
    ["Installers"]="deb AppImage sh"
)

organize_downloads() {
    local src="${1:-$HOME/Downloads}"
    for category in "${!RULES[@]}"; do
        mkdir -p "$src/$category"
        for ext in ${RULES[$category]}; do
            find "$src" -maxdepth 1 -name "*.$ext" -exec mv {} "$src/$category/" \;
        done
    done
}
```

## Wizards Disponibles

| Wizard | Étapes | Description |
|--------|--------|-------------|
| Setup Initial | 6 | Configuration complète système de fichiers |
| Migration | 5 | Migrer structure existante vers nouvelle |
| Nettoyage Grand | 4 | Nettoyage profond du système |
| Photos | 4 | Organiser bibliothèque photos |
| Projet | 3 | Créer structure projet standard |
| Audit | 4 | Audit complet avec recommandations |

## Métriques de Qualité

### Score d'Organisation (0-100)

| Critère | Points | Description |
|---------|--------|-------------|
| Nommage ISO | 25 | Fichiers avec date ISO |
| Structure | 20 | Profondeur < 4 niveaux |
| Doublons | 15 | Pas de fichiers en double |
| Fichiers orphelins | 15 | Pas de fichiers à la racine |
| Dossiers vides | 10 | Pas de dossiers vides |
| Noms normalisés | 10 | Pas de caractères spéciaux |
| Taille équilibrée | 5 | Dossiers < 100 fichiers |

### Interprétation

| Score | Niveau | Action |
|-------|--------|--------|
| 90-100 | 🟢 Excellent | Maintenir |
| 70-89 | 🟡 Bon | Améliorations mineures |
| 50-69 | 🟠 Moyen | Réorganisation recommandée |
| < 50 | 🔴 Critique | Wizard de nettoyage urgent |

## Templates de Structure

### Personnel
```
/file-structure apply personal
```

### Développeur
```
/file-structure apply developer
```

### Business
```
/file-structure apply business
```

### Creative
```
/file-structure apply creative
```

## Références

- [ISO 8601 - Date Format](https://www.iso.org/iso-8601-date-and-time-format.html)
- [PARA Method - Tiago Forte](https://fortelabs.com/blog/para/)
- [File Naming Best Practices - Harvard](https://datamanagement.hms.harvard.edu/plan-design/file-naming-conventions)
- [Digital Asset Management Guide](https://www.suitefiles.com/guide/the-guide-to-folder-structures-best-practices-for-professional-service-firms-and-more/)
