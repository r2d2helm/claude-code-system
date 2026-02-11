# Système r2d2 - Claude Code Configuration

## Identité

- **Utilisateur :** r2d2 (r2d2helm@gmail.com)
- **Machine :** Windows 11
- **PowerShell :** 7.4+ (PS 5.1 comme fallback)
- **Vault Obsidian :** `C:\Users\r2d2\Documents\Knowledge`

## Architecture Agents

### Meta-Agent Router

Le fichier `~/.claude/skills/SKILL.md` agit comme routeur intelligent. Il analyse chaque requête et active le skill approprié par détection de mots-clés.

### Custom Commands (6)

Commandes globales invocables depuis n'importe quel contexte avec `/<nom>` :

| Commande | Description | Usage |
|----------|-------------|-------|
| `/generate-prp` | Génère un PRP (Product Requirements Prompt) complet | `/generate-prp INITIAL.md` |
| `/execute-prp` | Exécute l'implémentation depuis un PRP | `/execute-prp PRPs/feature.md` |
| `/primer` | Analyse rapide d'un projet ou dossier | `/primer C:\chemin\vers\projet` |
| `/validate` | Validation 3 niveaux (structure, fonctionnel, intégration) | `/validate` ou `/validate mon-skill` |
| `/new-skill` | Création guidée d'un nouveau skill | `/new-skill nom-du-skill` |
| `/daily-maintenance` | Routine de maintenance quotidienne complète | `/daily-maintenance` |

**Chemin :** `~/.claude/commands/`

### Subagents (4)

Agents spécialisés invocables via le Task tool pour orchestration multi-agents :

| Agent | Rôle | Quand l'invoquer |
|-------|------|-----------------|
| **skill-builder** | Construit un skill complet (SKILL.md, commands/, wizards/) | Création d'un nouveau skill |
| **router-updater** | Met à jour SKILL.md (meta-router) + CLAUDE.md | Après skill-builder (downstream) |
| **knowledge-indexer** | Crée notes vault, met à jour MOCs et wikilinks | Après skill-builder (downstream) |
| **validation-gates** | Validation 3 niveaux + rapport + corrections autorisées | Après toute modification |

**Chemin :** `~/.claude/agents/`
**Protocole :** Contract-First (skill-builder publie un contrat, les agents downstream le consomment)

### PRP Framework

Système de planification structurée inspiré du Context Engineering :

| Fichier | Rôle |
|---------|------|
| `PRPs/templates/prp_base.md` | Template PRP adapté au système r2d2 |
| `PRPs/templates/INITIAL.md` | Template de feature request |
| `PRPs/*.md` | PRPs générés (blueprints d'implémentation) |

**Chemin :** `~/.claude/PRPs/`
**Workflow :** `INITIAL.md` → `/generate-prp` → PRP complet → `/execute-prp` → Code validé

### Skills Actifs (13)

| Skill | Chemin | Description | Commandes |
|-------|--------|-------------|-----------|
| **proxmox-skill** | `skills/proxmox-skill/` | Administration Proxmox VE 9+ | `/px-*`, 20 cmd, 11 wizards |
| **windows-skill** | `skills/windows-skill/` | Administration Windows 11/Server 2025 | `/win-*`, 36 cmd, 10 wizards |
| **docker-skill** | `skills/docker-skill/` | Administration Docker et conteneurs | `/dk-*`, 10 cmd, 3 wizards |
| **linux-skill** | `skills/linux-skill/` | Administration serveurs Linux | `/lx-*`, 12 cmd, 3 wizards |
| **knowledge-skill** | `skills/knowledge-skill/` | Capture et résumé de connaissances | `/know-save`, `/know-search`, `/know-export` |
| **knowledge-watcher-skill** | `skills/knowledge-watcher-skill/` | Surveillance automatique des sources | `/kwatch-*` (start, stop, status, process, config, logs) |
| **obsidian-skill** | `skills/obsidian-skill/` | Maintenance vault Obsidian | `/obs-health`, `/obs-links`, `/obs-tags`, `/obs-clean` |
| **fileorg-skill** | `skills/fileorg-skill/` | Organisation fichiers Windows | `/file-organize`, `/file-rename`, `/file-analyze`, `/file-duplicates`, `/file-clean` |
| **vault-guardian-skill** | `skills/vault-guardian-skill/` | Maintenance proactive automatisée | `/guardian-health`, `/guardian-fix`, `/guardian-report` |
| **qelectrotech-skill** | `skills/qelectrotech-skill/` | Plans électriques QElectroTech | `/qet-*`, 35 cmd, 9 wizards |
| **sop-creator** | `skills/sop-creator/` | Runbooks, SOPs, documentation opérationnelle | `/sop-create`, 6 templates |
| **skill-creator** | `skills/skill-creator/` | Création et validation de skills Claude Code | `/skill-create`, scripts init/validate |
| **meta-router** | `skills/SKILL.md` + `skills/commands/` | Routage intelligent (12 skills) | `/router`, `/agents`, `/context`, `/infra` |

### MCP Servers

| Serveur | Transport | Description |
|---------|-----------|-------------|
| **knowledge-assistant** | stdio (Python) | Accès au vault Obsidian : search, read, related, stats, tags, backlinks, recent (cache TTL 60s) |

**Config :** `~/.claude.json` -> `mcpServers.knowledge-assistant`
**Chemin :** `~/.claude/mcp-servers/knowledge-assistant/`
**Env :** `KNOWLEDGE_VAULT_PATH=C:\Users\r2d2\Documents\Knowledge`, `KNOWLEDGE_INDEX_PATH=~\.claude\skills\knowledge-watcher-skill\data\notes-index.json`

## Structure du Vault Obsidian

```
Knowledge/
├── _Index/          # MOCs et navigation
├── _Daily/          # Notes quotidiennes (YYYY-MM-DD.md)
├── _Inbox/          # Notes à traiter
├── _Templates/      # 4 templates : Conversation, Concept, Daily, Troubleshooting
├── Concepts/        # Notes Zettelkasten atomiques (C_Name.md)
├── Conversations/   # Résumés de sessions Claude (YYYY-MM-DD_Conv_Description.md)
├── Projets/         # Notes de projets (MultiPass, etc.)
├── Formations/      # Cours et formations
└── Références/      # Documentation et troubleshooting
```

## Conventions

### Nommage des notes

| Type | Format | Exemple |
|------|--------|---------|
| Conversation | `YYYY-MM-DD_Conv_Description.md` | `2026-02-05_Conv_Setup-Knowledge.md` |
| Concept | `C_Name.md` | `C_MCP-Pattern.md` |
| Daily | `YYYY-MM-DD.md` | `2026-02-06.md` |
| Troubleshooting | `YYYY-MM-DD_Fix_Description.md` | `2026-02-05_Fix_FileSystemWatcher.md` |

### Frontmatter YAML obligatoire

```yaml
---
title: "Titre de la note"
date: YYYY-MM-DD
type: conversation | concept | daily | troubleshooting | reference | formation
status: seedling | growing | evergreen
tags:
  - tag/hierarchique
related:
  - "[[Note-Liée]]"
---
```

### Tags hiérarchiques

- `dev/powershell`, `dev/python`, `dev/claude-code`
- `ai/claude`, `ai/claude-code`, `ai/agents`
- `infra/proxmox`, `infra/windows`
- `automation`, `troubleshooting`, `formation`

### Encodage

- **Fichiers Markdown/JSON :** UTF-8 sans BOM
- **Scripts PowerShell (.ps1/.psm1) :** UTF-8 avec BOM (requis par PS 5.1)
- **Utiliser :** `[System.IO.File]::WriteAllText()` avec encodage explicite, jamais `Set-Content` par défaut

## Workflows

### Capture de connaissances

```
Conversation Claude → /know-save → Note formatée dans vault
                                    ↓
                              Auto-linking (wikilinks)
                                    ↓
                              Indexée par MCP knowledge-assistant
```

### Surveillance automatique (Knowledge Watcher)

```
Tier 1 (Temps réel) : FileSystemWatcher sur Claude history + Projets
Tier 2 (Horaire)    : Downloads via Task Scheduler
Tier 3 (Quotidien)  : Bookmarks, VS Code
Tier 4 (Hebdomadaire): Archives
```

### Maintenance vault

```
Quotidien  : /daily-maintenance (ou /guardian-health --quick) + git commit vault
Hebdo      : /guardian-fix + /obs-clean
Mensuel    : /guardian-report (audit complet) + /obs-backup
```

### Context Engineering (PRP Framework)

Workflow pour les tâches complexes (nouveau skill, feature multi-fichiers, refonte) :

```
1. Rédiger INITIAL.md (décrire la feature, contexte, docs)
       ↓
2. /generate-prp INITIAL.md
       ↓  Recherche codebase + docs + vault MCP
       ↓  ULTRATHINK → planification exhaustive
       ↓
3. PRP complet généré dans PRPs/{feature}.md
       ↓  Blueprint avec tout le contexte
       ↓
4. /execute-prp PRPs/{feature}.md
       ↓  Implémentation tâche par tâche
       ↓  Validation 3 niveaux à chaque étape
       ↓
5. Code fonctionnel et validé ✅
```

### Orchestration multi-agents (Contract-First)

Workflow pour les tâches nécessitant plusieurs agents coordonnés :

```
skill-builder (upstream)
    │  Construit le skill + publie son contrat
    │  (nom, prefix, keywords, description)
    │
    ├──→ router-updater (downstream)
    │       Reçoit le contrat → MAJ SKILL.md + CLAUDE.md
    │
    ├──→ knowledge-indexer (downstream)
    │       Reçoit le contrat → crée note vault + MAJ MOCs
    │
    └──→ validation-gates (vérification finale)
            Valide structure + fonctionnel + intégration
```

Principes :
- **Upstream d'abord** : toujours spawner les agents producteurs avant les consommateurs
- **Contrat explicite** : chaque agent upstream publie un contrat structuré
- **Lead vérifie** : le contrat est vérifié avant transmission aux agents downstream
- **Jamais peer-to-peer** : les agents ne communiquent pas entre eux directement

## Chemins importants

| Ressource | Chemin |
|-----------|--------|
| Skills | `C:\Users\r2d2\.claude\skills\` |
| Custom Commands | `C:\Users\r2d2\.claude\commands\` |
| Subagents | `C:\Users\r2d2\.claude\agents\` |
| PRPs | `C:\Users\r2d2\.claude\PRPs\` |
| MCP Servers | `C:\Users\r2d2\.claude\mcp-servers\` |
| Vault | `C:\Users\r2d2\Documents\Knowledge\` |
| Templates | `C:\Users\r2d2\Documents\Knowledge\_Templates\` |
| Repos formation | `C:\Users\r2d2\Documents\Formations\Repos\` |
| Notes index | `~\.claude\skills\knowledge-watcher-skill\data\notes-index.json` |
| Config backup | `C:\Users\r2d2\Documents\claude-config-backup\` |
| Vault git | `C:\Users\r2d2\Documents\Knowledge\.git` (init 2026-02-11) |

## Règles pour Claude Code

### Encodage & fichiers
1. **Toujours écrire en UTF-8 sans BOM** pour les fichiers .md et .json (l'outil Write fait ça automatiquement)
2. **PowerShell** : toujours écrire des scripts compatibles PS 5.1 (pas de `??`, pas de `UTF8BOM`)
3. **Ne jamais dépasser 500 lignes** par fichier SKILL.md ; découper dans `references/`

### Vault Obsidian
4. **Utiliser les wikilinks** `[[Nom-Note]]` dans les notes Obsidian pour créer des connexions
5. **Ajouter le frontmatter YAML** à toute nouvelle note créée dans le vault
6. **Respecter le nommage** : `C_` pour concepts, `YYYY-MM-DD_Conv_` pour conversations
7. **Ne pas modifier** les fichiers dans `_Templates/` sauf demande explicite
8. **Consulter le vault** via les outils MCP (knowledge_search, knowledge_read) avant de créer des notes potentiellement dupliquées

### Context Engineering & PRP
9. **Utiliser le PRP Framework** pour les tâches complexes (multi-fichiers, nouveau skill, refonte) : `/generate-prp` puis `/execute-prp`
10. **ULTRATHINK** avant toute implémentation de PRP : planifier l'approche complète avant d'écrire du code
11. **Valider à 3 niveaux** après chaque modification significative : structure, fonctionnel, intégration

### Orchestration multi-agents
12. **Contract-First** : lors de la création d'un skill, le skill-builder publie son contrat AVANT que router-updater et knowledge-indexer ne travaillent
13. **Jamais peer-to-peer** : les agents downstream reçoivent le contrat via le Lead (agent principal), pas directement entre eux
14. **Validation systématique** : invoquer validation-gates après toute orchestration multi-agents

### Cohérence du système
15. **Mettre à jour CLAUDE.md** quand un nouveau skill, command ou agent est ajouté
16. **Mettre à jour le meta-router** (skills/SKILL.md) quand un skill est ajouté/modifié/supprimé
17. **Sauvegarder les modifications** dans le backup (`Documents/claude-config-backup/`) pour les changements importants
