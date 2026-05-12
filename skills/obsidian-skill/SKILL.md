---
name: obsidian-skill
description: Administration et maintenance du vault Obsidian
prefix: /obs-*
---

# 🗂️ Super Agent Obsidian Administration

Agent intelligent pour administrer, maintenir et optimiser les vaults Obsidian.

## Philosophie

> "Un vault bien entretenu est un second cerveau performant."

Cet agent automatise la maintenance, détecte les problèmes et optimise l'organisation de vos vaults Obsidian.

## Compatibilité

| Composant | Support |
|-----------|---------|
| Ubuntu Linux | 24.04+ |
| Bash | 5+ |
| Obsidian | 1.4+ |
| Format | Markdown (.md) |

## Commandes Slash

### 🔍 Analyse & Santé

| Commande | Description |
|----------|-------------|
| `/obs-health` | Diagnostic complet du vault |
| `/obs-stats` | Statistiques détaillées |
| `/obs-graph` | Analyse du graphe de liens |
| `/obs-orphans` | Détecter notes orphelines |

### 🔗 Gestion des Liens

| Commande | Description |
|----------|-------------|
| `/obs-links broken` | Trouver liens cassés |
| `/obs-links unlinked` | Notes sans liens |
| `/obs-links suggest` | Suggerer connexions |
| `/obs-links fix` | Reparer liens casses |

### 🏷️ Gestion des Tags

| Commande | Description |
|----------|-------------|
| `/obs-tags list` | Lister tous les tags |
| `/obs-tags unused` | Tags non utilises |
| `/obs-tags rename` | Renommer un tag |
| `/obs-tags merge` | Fusionner des tags |
| `/obs-tags hierarchy` | Afficher hierarchie |

### 📁 Organisation

| Commande | Description |
|----------|-------------|
| `/obs-structure` | Analyser structure dossiers |
| `/obs-move` | Deplacer notes intelligemment |
| `/obs-rename` | Renommer avec conventions |
| `/obs-frontmatter` | Gerer metadonnees YAML |
| `/obs-templates` | Gerer templates |

### 🧹 Maintenance

| Commande | Description |
|----------|-------------|
| `/obs-clean` | Nettoyage général |
| `/obs-duplicates` | Detecter doublons |
| `/obs-attachments` | Gerer pieces jointes |
| `/obs-empty` | Supprimer notes vides |

### 💾 Backup & Export

| Commande | Description |
|----------|-------------|
| `/obs-backup` | Sauvegarder le vault |
| `/obs-export` | Exporter (JSON, CSV, HTML) |
| `/obs-sync` | Synchroniser vault (git, backup, compare) |

### ⚙️ Configuration

| Commande | Description |
|----------|-------------|
| `/obs-config` | Gerer configuration Obsidian |
| `/obs-plugins` | Gerer plugins |
| `/obs-hotkeys` | Gerer raccourcis |

### 🧙 Wizards

| Commande | Description |
|----------|-------------|
| `/obs-wizard audit` | Audit complet du vault |
| `/obs-wizard cleanup` | Nettoyage guide |
| `/obs-wizard reorganize` | Reorganisation assistee |

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

```bash
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

```bash
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

```bash
/obs-tags list

# Détecte:
# - Tags similaires: #proxmox vs #Proxmox vs #pve
# - Tags orphelins: utilisés une seule fois
# - Tags mal formés: espaces, caractères spéciaux
```

## Maintenance Automatisée

### Nettoyage Complet

```bash
/obs-clean --all

# Actions:
# 1. Supprimer fichiers temporaires (.tmp, .bak)
# 2. Nettoyer cache Obsidian
# 3. Supprimer notes vides
# 4. Optimiser attachments
# 5. Reconstruire index
```

### Gestion des Attachments

```bash
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

```bash
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

```bash
/obs-backup

╔═══════════════════════════════════════════════════════════╗
║  💾 BACKUP DU VAULT                                       ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Source: ~/Documents/Knowledge                            ║
║  Destination: ~/Backups/Knowledge                         ║
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

```bash
/obs-backup --dest="~/Backups"            # Destination personnalisée
/obs-backup --exclude=".obsidian"         # Exclure config
/obs-backup --incremental                 # Backup incrémental
/obs-backup --git                         # Commit Git
```

## Scripts Bash

### Chemin du Vault

```bash
VAULT_PATH="$HOME/Documents/Knowledge"
```

### Trouver Liens Cassés

```bash
find_broken_links() {
    local vault_path="${1:-$HOME/Documents/Knowledge}"

    # Collecter les noms de toutes les notes (sans extension)
    mapfile -t note_names < <(find "$vault_path" -name "*.md" -exec basename {} .md \;)

    while IFS= read -r -d '' note; do
        while IFS= read -r link; do
            # Vérifier si la cible existe dans la liste des notes
            local found=0
            for name in "${note_names[@]}"; do
                [[ "$name" == "$link" ]] && found=1 && break
            done
            if [[ $found -eq 0 ]]; then
                echo "Source: $note | Lien cassé: $link"
            fi
        done < <(grep -oP '(?<=\[\[)[^\]|]+' "$note")
    done < <(find "$vault_path" -name "*.md" -print0)
}
```

### Trouver Notes Orphelines

```bash
find_orphan_notes() {
    local vault_path="${1:-$HOME/Documents/Knowledge}"

    # Collecter tous les liens dans le vault
    mapfile -t all_links < <(grep -rhoP '(?<=\[\[)[^\]|]+' "$vault_path" --include="*.md")

    # Trouver les notes jamais référencées
    while IFS= read -r -d '' note; do
        local basename
        basename=$(basename "$note" .md)
        local found=0
        for link in "${all_links[@]}"; do
            [[ "$link" == "$basename" ]] && found=1 && break
        done
        [[ $found -eq 0 ]] && echo "Orpheline: $note"
    done < <(find "$vault_path" -name "*.md" -print0)
}
```

### Statistiques du Vault

```bash
get_vault_stats() {
    local vault_path="${1:-$HOME/Documents/Knowledge}"

    local note_count attachment_count word_count link_count tag_count size_mb
    note_count=$(find "$vault_path" -name "*.md" | wc -l)
    attachment_count=$(find "$vault_path" \( -name "*.png" -o -name "*.jpg" -o -name "*.pdf" \) | wc -l)
    word_count=$(find "$vault_path" -name "*.md" -exec cat {} \; | wc -w)
    link_count=$(grep -roh '\[\[' "$vault_path" --include="*.md" | wc -l)
    tag_count=$(grep -rohP '#[\w/-]+' "$vault_path" --include="*.md" | sort -u | wc -l)
    size_mb=$(du -sm "$vault_path" | cut -f1)

    echo "Notes: $note_count | Mots: $word_count | Liens: $link_count"
    echo "Tags uniques: $tag_count | Attachments: $attachment_count | Taille: ${size_mb} MB"
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
