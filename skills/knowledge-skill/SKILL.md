---
name: knowledge-skill
description: Capture et organisation des connaissances
prefix: /know-*
---

# 🧠 Super Agent Knowledge Capture

Agent intelligent de capture, résumé et organisation des connaissances extraites des conversations Claude.

## Philosophie

> "La connaissance externalisée est la connaissance exploitable." — Zettelkasten

Cet agent transforme les conversations éphémères en base de connaissances permanente et interconnectée, compatible avec les outils PKM (Obsidian, Notion, etc.).

## Méthode CODE

| Phase | Action | Description |
|-------|--------|-------------|
| **C**ollect | Capturer | Extraire infos clés des conversations |
| **O**rganize | Organiser | Classer par catégorie et tags |
| **D**istill | Distiller | Résumer en notes atomiques |
| **E**xpress | Exprimer | Réutiliser et connecter |

## Compatibilité

| Composant | Support |
|-----------|---------|
| Ubuntu Linux | 24.04+ |
| Bash | 5+ |
| Format | Markdown (.md) |
| Outils PKM | Obsidian, Notion, Logseq, Roam |

## Commandes Slash

### Capture

| Commande | Description |
|----------|-------------|
| `/know-save` | Sauvegarder conversation actuelle |
| `/know-extract` | Extraire éléments spécifiques |
| `/know-quick` | Note rapide (une idée) |

### Gestion

| Commande | Description |
|----------|-------------|
| `/know-search` | Rechercher dans la base |
| `/know-list` | Lister notes récentes |
| `/know-index` | Créer/mettre à jour l'index |
| `/know-link` | Lier notes entre elles |

### Export

| Commande | Description |
|----------|-------------|
| `/know-export` | Exporter vers Obsidian/Notion |
| `/know-report` | Générer rapport périodique |
| `/know-backup` | Sauvegarder la base |

### Wizards

| Commande | Description |
|----------|-------------|
| `/know-wizard setup` | Configuration initiale |
| `/know-wizard review` | Revue quotidienne/hebdo |

## Structure de la Base de Connaissances

### Arborescence

```
Knowledge\
├── _Index\                    # Index et navigation
│   ├── INDEX.md               # Index principal
│   ├── Tags.md                # Liste des tags
│   └── MOC-*.md               # Maps of Content thématiques
├── _Daily\                    # Notes quotidiennes
│   └── {YYYY-MM-DD}.md
├── _Inbox\                    # À traiter
├── Conversations\             # Résumés de conversations
│   └── {YYYY-MM-DD}_Conv_{Sujet}.md
├── Concepts\                  # Notes atomiques (Zettelkasten)
│   └── {ID}_{Concept}.md
├── Projets\                   # Notes par projet
│   └── {Projet}\
├── Références\                # Sources et références
│   └── {Type}\
├── Code\                      # Snippets et scripts
│   └── {Langage}\
└── Templates\                 # Modèles de notes
```

### Types de Notes

| Type | Préfixe | Description |
|------|---------|-------------|
| Conversation | `Conv_` | Résumé d'une conversation Claude |
| Concept | `C_` | Idée atomique (1 idée = 1 note) |
| Projet | `P_` | Note liée à un projet |
| Référence | `R_` | Source externe |
| Code | `Code_` | Script ou snippet |
| Daily | Date | Note quotidienne |
| Index | `MOC_` | Map of Content |

## Format des Notes

### Template Conversation

```markdown
---
id: {YYYYMMDD}-{HHMMSS}
title: {Titre descriptif}
date: {YYYY-MM-DD}
type: conversation
tags: [tag1, tag2, tag3]
source: Claude
status: processed
related: [[Note1]], [[Note2]]
---

# {Titre}

## Résumé
{Résumé en 2-3 phrases}

## Points Clés
- Point 1
- Point 2
- Point 3

## Décisions Prises
- [ ] Décision 1
- [ ] Décision 2

## Code/Commandes
```language
{code extrait}
```

## Concepts Liés
- [[Concept1]]
- [[Concept2]]

## Actions Suivantes
- [ ] Action 1
- [ ] Action 2

## Notes Additionnelles
{Notes libres}

---
*Capturé le {date} depuis conversation Claude*
```

### Template Concept (Zettelkasten)

```markdown
---
id: {ID unique}
title: {Titre = résumé de l'idée}
date: {YYYY-MM-DD}
type: concept
tags: [tag1, tag2]
source: [[Conversation source]]
related: [[Note1]], [[Note2]]
---

# {Titre résumant l'idée}

{Explication de l'idée en quelques paragraphes}

## Pourquoi c'est important
{Contexte et importance}

## Liens
- Découle de: [[Note précédente]]
- Mène à: [[Note suivante]]
- Voir aussi: [[Note liée]]

## Sources
- [[Conversation {date}]]
- {Autres sources}
```

### Template Daily Note

```markdown
---
date: {YYYY-MM-DD}
type: daily
tags: [daily, {YYYY}, {MM}]
---

# 📅 {YYYY-MM-DD}

## Conversations du Jour
- [[Conv_{date}_Sujet1]]
- [[Conv_{date}_Sujet2]]

## Idées Capturées
- [[Concept1]]
- [[Concept2]]

## Code/Scripts Créés
- [[Code_Script1]]

## À Faire
- [ ] Task 1
- [ ] Task 2

## Réflexions
{Notes libres de la journée}
```

## Système de Tags

### Tags Hiérarchiques

```
#domaine/sous-domaine/spécifique

Exemples:
#dev/bash/automation
#infra/proxmox/vm
#infra/windows/security
#projet/multipass/website
#concept/architecture/pattern
```

### Tags Standards

| Catégorie | Tags |
|-----------|------|
| Status | `#todo`, `#inprogress`, `#done`, `#review` |
| Type | `#concept`, `#howto`, `#reference`, `#decision` |
| Priorité | `#p1`, `#p2`, `#p3` |
| Domaine | `#dev`, `#infra`, `#business`, `#personal` |

## Extraction Automatique

### Éléments Extraits

| Élément | Détection | Stockage |
|---------|-----------|----------|
| Code | Blocs ``` | `Code/{Langage}/` |
| Commandes | bash, python | `Code/Commands/` |
| Décisions | "décidé", "choisi" | Section Décisions |
| URLs | http(s):// | Section Références |
| Configs | JSON, YAML | `Code/Configs/` |
| Erreurs/Solutions | "erreur", "résolu" | `Références/Troubleshooting/` |

### Patterns de Détection

```
Concepts:     "important", "à retenir", "clé", "essentiel"
Décisions:    "décidé", "choisi", "opté pour", "on va"
Actions:      "à faire", "todo", "prochaine étape"
Références:   URLs, noms de documentation
Questions:    "?", "comment", "pourquoi"
```

## Templates de Notes

Le fichier `templates/templates.md` contient les templates utilises par `/know-save` pour generer des notes structurees. Templates disponibles :

- **Conversation** : resume de session Claude (frontmatter + points cles + actions)
- **Concept** : note atomique Zettelkasten (idee + liens + sources)
- **Daily** : note quotidienne (focus + conversations + accomplissements)
- **Troubleshooting** : resolution de probleme (symptomes + cause + solution)
- **Code** : snippet avec description, parametres et exemples d'utilisation
- **Projet** : suivi de projet (objectifs + decisions + notes de travail)
- **Reference** : source externe (resume + citations + idees extraites)

Usage : `/know-save --template=conversation`, `/know-save --template=concept`, etc.

## Liens et Connexions

### Syntaxe Obsidian

```markdown
[[Nom de la note]]           # Lien simple
[[Note|Alias]]               # Lien avec alias
[[Note#Section]]             # Lien vers section
![[Note]]                    # Embed (inclusion)
```

### Backlinks Automatiques

Chaque note liste automatiquement les notes qui la référencent.

## Recherche

### Syntaxe de Recherche

```
/know-search "terme"              # Recherche simple
/know-search tag:#proxmox         # Par tag
/know-search type:concept         # Par type
/know-search date:2026-02         # Par date
/know-search "terme" --in=code    # Dans le code
```

## Intégration Outils

### Export Obsidian

```
/know-export obsidian --path="~/Documents/Knowledge"
```

Crée:
- Structure de dossiers compatible
- Fichiers .md avec frontmatter YAML
- Liens [[wikilinks]]
- Tags #hierarchiques

### Export Notion

```
/know-export notion --format=csv
```

### Export JSON

```
/know-export json --path="backup.json"
```

## Workflow Recommandé

### Après Chaque Conversation

```
1. /know-save                    # Sauvegarde automatique
2. Revoir résumé généré
3. Ajouter tags pertinents
4. Créer liens vers notes existantes
```

### Revue Quotidienne

```
1. /know-wizard review daily
2. Consolider notes de l'inbox
3. Créer concepts atomiques
4. Mettre à jour index
```

### Revue Hebdomadaire

```
1. /know-wizard review weekly
2. Identifier patterns et thèmes
3. Créer Maps of Content (MOC)
4. Archiver notes obsolètes
5. Backup de la base
```

## Métriques

### Dashboard

```
/know-stats
```

```
╔══════════════════════════════════════════════════════════════╗
║                   📊 KNOWLEDGE STATS                         ║
╠══════════════════════════════════════════════════════════════╣
║  Total Notes      : 234                                      ║
║  Conversations    : 89                                       ║
║  Concepts         : 67                                       ║
║  Code Snippets    : 45                                       ║
║  Tags utilisés    : 34                                       ║
║  Liens internes   : 456                                      ║
║  Notes orphelines : 12 ⚠️                                    ║
║  Dernière capture : 2026-02-04 08:30                         ║
╚══════════════════════════════════════════════════════════════╝
```

## Best Practices 2025-2026

### Notes Atomiques
- 1 idée = 1 note
- Titre = résumé de l'idée
- Toujours lier à au moins 1 autre note

### Nommage
- Format: `{YYYY-MM-DD}_{Type}_{Sujet}.md`
- Pas d'espaces ni caractères spéciaux
- Titres descriptifs (pas "Note 1")

### Tags
- Hiérarchiques: `#domaine/sous-domaine`
- Cohérents: même tag pour même concept
- Pas trop nombreux (5-10 max par note)

### Revue
- Daily: 5 minutes
- Weekly: 30 minutes
- Monthly: 2 heures

## Références

- [Zettelkasten Method](https://zettelkasten.de/)
- [How to Take Smart Notes - Sönke Ahrens](https://www.soenkeahrens.de/en/takesmartnotes)
- [Building a Second Brain - Tiago Forte](https://www.buildingasecondbrain.com/)
- [Obsidian Documentation](https://help.obsidian.md/)
