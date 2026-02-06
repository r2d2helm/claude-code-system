# Système r2d2 - Claude Code Configuration

## Identité

- **Utilisateur :** r2d2 (r2d2helm@gmail.com)
- **Machine :** Windows 11
- **PowerShell :** 7.4+ (PS 5.1 comme fallback)
- **Vault Obsidian :** `C:\Users\r2d2\Documents\Knowledge`

## Architecture Agents

### Meta-Agent Router

Le fichier `~/.claude/skills/SKILL.md` agit comme routeur intelligent. Il analyse chaque requête et active le skill approprié par détection de mots-clés.

### Skills Actifs (9)

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
| **meta-router** | `skills/SKILL.md` + `skills/commands/` | Routage intelligent des requêtes | `/router`, `/agents`, `/context`, `/infra` |

### MCP Servers

| Serveur | Transport | Description |
|---------|-----------|-------------|
| **knowledge-assistant** | stdio (Python) | Accès au vault Obsidian : search, read, related, stats, tags, backlinks, recent |

**Config :** `~/.claude.json` -> `mcpServers.knowledge-assistant`
**Chemin :** `~/.claude/mcp-servers/knowledge-assistant/`
**Env :** `KNOWLEDGE_VAULT_PATH=C:\Users\r2d2\Documents\Knowledge`

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
Quotidien  : /obs-health --quick
Hebdo      : /obs-clean
Mensuel    : /obs-health (audit complet) + /obs-backup
```

## Chemins importants

| Ressource | Chemin |
|-----------|--------|
| Skills | `C:\Users\r2d2\.claude\skills\` |
| MCP Servers | `C:\Users\r2d2\.claude\mcp-servers\` |
| Vault | `C:\Users\r2d2\Documents\Knowledge\` |
| Templates | `C:\Users\r2d2\Documents\Knowledge\_Templates\` |
| Repos formation | `C:\Users\r2d2\Documents\Formations\Repos\` |
| Notes index | `~\.claude\skills\knowledge-watcher-skill\data\notes-index.json` |

## Règles pour Claude Code

1. **Toujours écrire en UTF-8 sans BOM** pour les fichiers .md et .json (l'outil Write fait ça automatiquement)
2. **Utiliser les wikilinks** `[[Nom-Note]]` dans les notes Obsidian pour créer des connexions
3. **Ajouter le frontmatter YAML** à toute nouvelle note créée dans le vault
4. **Respecter le nommage** : `C_` pour concepts, `YYYY-MM-DD_Conv_` pour conversations
5. **Ne pas modifier** les fichiers dans `_Templates/` sauf demande explicite
6. **Consulter le vault** via les outils MCP (knowledge_search, knowledge_read) avant de créer des notes potentiellement dupliquées
7. **PowerShell** : toujours écrire des scripts compatibles PS 5.1 (pas de `??`, pas de `UTF8BOM`)
