# Claude Code System - r2d2

Configuration et skills pour Claude Code : un systeme multi-agents intelligent pour l'administration Windows, Proxmox, la gestion de connaissances Obsidian et l'organisation de fichiers.

## Architecture

```
.claude/
├── CLAUDE.md                    # Configuration racine Claude Code
├── skills/
│   ├── SKILL.md                 # Meta-Agent Router (point d'entree)
│   ├── commands/                # Commandes globales (router, agents, context, infra)
│   ├── proxmox-skill/           # Administration Proxmox VE 9+ (20 cmd, 11 wizards)
│   ├── windows-skill/           # Administration Windows 11/Server 2025 (36 cmd, 10 wizards)
│   ├── knowledge-skill/         # Capture et gestion de connaissances
│   ├── knowledge-watcher-skill/ # Surveillance automatique des sources (4 tiers)
│   ├── obsidian-skill/          # Maintenance vault Obsidian (8 commandes)
│   └── fileorg-skill/           # Organisation fichiers Windows (9 commandes)
└── mcp-servers/                 # Serveurs MCP (repos separees)
    └── knowledge-assistant/     # -> github.com/r2d2helm/knowledge-assistant-mcp
```

## Skills

| Skill | Prefixe | Commandes | Wizards | Description |
|-------|---------|-----------|---------|-------------|
| **proxmox-skill** | `/px-*` | 20 | 11 | VMs, containers, stockage, reseau, HA, Ceph |
| **windows-skill** | `/win-*` | 36 | 10 | Services, registre, reseau, securite, AD |
| **knowledge-skill** | `/know-*` | 3 | - | Sauvegarde, recherche, export de connaissances |
| **knowledge-watcher** | `/kwatch-*` | 6 | 2 | FileSystemWatcher + taches planifiees (4 tiers) |
| **obsidian-skill** | `/obs-*` | 8 | - | Sante, liens, tags, stats, orphelins, backup |
| **fileorg-skill** | `/file-*` | 9 | - | Organiser, renommer, analyser, archiver, nettoyer |

## MCP Servers

| Serveur | Repo | Description |
|---------|------|-------------|
| knowledge-assistant | [knowledge-assistant-mcp](https://github.com/r2d2helm/knowledge-assistant-mcp) | Acces au vault Obsidian (search, read, stats, tags) |

## Prerequis

- Windows 11 / Server 2025
- PowerShell 7.4+
- Claude Code CLI
- Obsidian 1.4+ (pour les skills vault)

## Installation

Voir [claude-code-installer](https://github.com/r2d2helm/claude-code-installer) pour l'installation automatisee.

## Licence

Usage personnel - r2d2
