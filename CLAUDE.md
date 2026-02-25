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

### Skills (19 actifs + meta-router)

| Skill | Chemin | Description | Commandes |
|-------|--------|-------------|-----------|
| **proxmox-skill** | `skills/proxmox-skill/` | Administration Proxmox VE 9+ | `/pve-*`, 22 cmd, 11 wizards |
| **windows-skill** | `skills/windows-skill/` | Administration Windows 11/Server 2025 | `/win-*`, 37 cmd, 10 wizards |
| **docker-skill** | `skills/docker-skill/` | Administration Docker et conteneurs | `/dk-*`, 13 cmd, 3 wizards |
| **linux-skill** | `skills/linux-skill/` | Administration serveurs Linux | `/lx-*`, 17 cmd, 3 wizards |
| **knowledge-skill** | `skills/knowledge-skill/` | Capture et résumé de connaissances | `/know-*`, 10 cmd, 1 wizard |
| **knowledge-watcher-skill** | `skills/knowledge-watcher-skill/` | Surveillance automatique des sources | `/kwatch-*`, 6 cmd, 2 wizards |
| **obsidian-skill** | `skills/obsidian-skill/` | Maintenance vault Obsidian | `/obs-*`, 28 cmd, 3 wizards |
| **fileorg-skill** | `skills/fileorg-skill/` | Organisation fichiers Windows | `/file-*`, 20 cmd, 1 wizard |
| **vault-guardian-skill** | `skills/vault-guardian-skill/` | Maintenance proactive automatisée | `/guardian-*`, 4 cmd |
| **qelectrotech-skill** | `skills/qelectrotech-skill/` | Plans électriques QElectroTech | `/qet-*`, 34 cmd, 9 wizards |
| **sop-creator** | `skills/sop-creator/` | Runbooks, SOPs, documentation opérationnelle | `/sop-*`, 1 cmd, 6 templates |
| **skill-creator** | `skills/skill-creator/` | Création et validation de skills Claude Code | `/skill-*`, 1 cmd |
| **monitoring-skill** | `skills/monitoring-skill/` | Monitoring temps reel homelab (Beszel, Netdata, Uptime Kuma) | `/mon-*`, 10 cmd, 2 wizards |
| **backup-skill** | `skills/backup-skill/` | Backup et restauration | `/bak-*`, 8 cmd, 2 wizards |
| **security-skill** | `skills/security-skill/` | Securite infrastructure | `/sec-*`, 9 cmd, 2 wizards |
| **network-skill** | `skills/network-skill/` | Administration reseau | `/net-*`, 10 cmd, 2 wizards |
| **devops-skill** | `skills/devops-skill/` | DevOps et deploiement | `/devops-*`, 10 cmd, 2 wizards |
| **ai-infra-skill** | `skills/ai-infra-skill/` | Infrastructure AI (LiteLLM, Langfuse, RAG) | `/ai-*`, 9 cmd, 2 wizards |
| **supabase-skill** | `skills/supabase-skill/` | Administration Supabase | `/supa-*`, 8 cmd, 2 wizards |
| **meta-router** | `skills/SKILL.md` + `skills/commands/` | Routage intelligent des 19 skills | `/router`, `/agents`, `/context`, `/infra` |

### MCP Servers

| Serveur | Transport | Description |
|---------|-----------|-------------|
| **knowledge-assistant** | stdio (Python) | Accès au vault Obsidian : search, read, related, stats, tags, backlinks, recent (cache TTL 60s) |
| **taskyn** | streamable-http | Gestion de projet AI-first : companies, projects, nodes, edges, milestones, tags, timers, reporting (40+ outils MCP) |
| **beszel-assistant** | stdio (Python) | Monitoring homelab Beszel : systems, containers, alerts, overview (5 outils MCP) |
| **netdata-vm100** | http | Metriques Netdata detaillees VM 100 : CPU, RAM, IO, network, anomalies (MCP natif v2.9+) |

**Config :** `~/.claude.json` -> `mcpServers`

**knowledge-assistant :**
- **Chemin :** `~/.claude/mcp-servers/knowledge-assistant/`
- **Env :** `KNOWLEDGE_VAULT_PATH=C:\Users\r2d2\Documents\Knowledge`, `KNOWLEDGE_INDEX_PATH=~\.claude\skills\knowledge-watcher-skill\data\notes-index.json`

**taskyn :**
- **URL :** `http://192.168.1.163:8020/mcp` (VM 103 r2d2-main, container taskyn-core)
- **Web UI :** `http://192.168.1.163:3020` (container taskyn-web)
- **Auth Web :** `r2d2helm@gmail.com` / `Jarvis@2025`
- **Methodologies :** spec_driven et classic_agile
- **Prerequis :** VM 103 doit etre demarree
- **Aussi sur :** VM 105 r2d2-lab (`192.168.1.161:8020/3020`)

**beszel-assistant :**
- **Chemin :** `~/.claude/mcp-servers/beszel-assistant/`
- **Env :** `BESZEL_HUB_URL=http://192.168.1.162:8091` (VM 100 r2d2-stage), `BESZEL_ADMIN_EMAIL=r2d2helm@gmail.com`, `BESZEL_ADMIN_PASSWORD`
- **Auth endpoint :** `/api/collections/_superusers/auth-with-password` (PocketBase v0.23+)
- **Outils :** beszel_systems, beszel_system_detail, beszel_containers, beszel_alerts, beszel_overview
- **Systemes monitores :** vm100 (localhost), proxmox (192.168.1.215), windows-r2d2 (192.168.1.243)

**netdata-vm100 :**
- **URL :** `http://192.168.1.162:19999/mcp` (VM 100, container netdata)
- **Version :** Netdata v2.9.0+ (MCP natif integre)

### Monitoring Stack (distribue)

Services monitoring repliques sur VM 100, 103 et 104. Instances primaires sur VM 100 :

| Service | VM 100 (primary) | VM 103 | VM 104 |
|---------|-------------------|--------|--------|
| **Beszel Hub** | `:8091` | `:8091`* | `:8091`* |
| **Uptime Kuma** | `:3003` | `:3003` | `:3003` |
| **Netdata** | `:19999` | local | local |
| **Dozzle** | `:8082` | `:8082` | `:8082` |
| **ntfy** | `:8084` | `:8084` | `:8084` |
| **Beszel Agent** | Docker | Docker | Docker |

*Beszel Hub sur VM 103/104 sans port expose (interne)

**URLs primaires (VM 100 `192.168.1.162`) :**
- Beszel Hub: `http://192.168.1.162:8091`
- Uptime Kuma: `http://192.168.1.162:3003`
- Netdata: `http://192.168.1.162:19999`
- Dozzle: `http://192.168.1.162:8082`
- ntfy: `http://192.168.1.162:8084`

**Agents Beszel :** VM 100 (:45876 Docker), Proxmox (:45876 systemd), Windows (:45876 NSSM)
**Alertes Telegram :** Bot token dans credentials, notifie sur tous les monitors Uptime Kuma

### Services par VM

| VM | Containers | Role |
|----|-----------|------|
| 100 r2d2-stage (6) | beszel-hub, beszel-agent, uptime-kuma, netdata, dozzle, ntfy | Monitoring primaire |
| 101 r2d2-monitor (0) | Pas de Docker | Desktop (Linux Mint) |
| 103 r2d2-main (29) | MultiPass stack (Supabase, LiteLLM, Langfuse, Frontend, API, Redis, NetBox) + Taskyn + Monitoring | Dev principal |
| 104 r2d2-store (7) | postgres-shared, monitoring stack + NFS | Stockage & BDD |
| 105 r2d2-lab (3) | rag-indexer, taskyn-web, taskyn-core | Lab & RAG |

### Hooks (9)

Hooks Python executés automatiquement sur les événements Claude Code :

| Hook | Événement | Matcher | Description |
|------|-----------|---------|-------------|
| `load_context.py` | SessionStart | * | Charge contexte système + injection mémoires startup |
| `security_validator.py` | PreToolUse | Bash | Valide commandes shell (blocked/confirm/alert) |
| `path_guard.py` | PreToolUse | Read,Write,Edit | Protège chemins sensibles (secrets, système) |
| `memory_extractor_v2.py` | Stop | * | Memory v2: extraction heuristique + SQLite |
| `subagent_capture.py` | SubagentStop | * | Log résultats des subagents |
| `prompt_analyzer.py` | UserPromptSubmit | * | Analyse requêtes + injection mémoires contextuelles |
| `error_capture.py` | PostToolUse | Bash | Capture commandes en echec dans errors.jsonl |
| `notify_write.py` | PostToolUse | Write | Notification ecriture fichier markdown |
| `notify_complete.py` | Notification | * | Notification OS de fin de tache |

**Chemin :** `~/.claude/hooks/`
**Config :** `~/.claude/settings.json` -> `hooks`
**Principe :** Fail-open (exit 0 en cas d'erreur, jamais bloquer Claude Code)

### Memory v2 (auto-apprenant)

Systeme de memoire SQLite qui remplace le stockage JSONL write-only :

| Composant | Fichier | Role |
|-----------|---------|------|
| **DB Layer** | `hooks/lib/memory_db.py` | SQLite WAL (sessions, memories, facts, retrieval_log) |
| **Retriever** | `hooks/lib/memory_retriever.py` | Recuperation contextuelle (startup + per-prompt) |
| **Extractor v2** | `hooks/memory_extractor_v2.py` | 5 heuristiques: tool_sequences, problem_solution, topics, decisions, facts |
| **Consolidator** | `hooks/memory_consolidator.py` | Periodique: decay, merge, prune, promote |
| **Config** | `hooks/config/memory_v2.yaml` | Seuils, stopwords, parametres |
| **Migration** | `hooks/migrate_memory_v1_to_v2.py` | JSONL -> SQLite (one-shot) |

**Cycle de vie :** Creation (Stop) -> Retrieval (SessionStart/UserPromptSubmit) -> Feedback (Stop suivant) -> Consolidation (periodique)
**DB :** `~/.claude/hooks/data/memory.db`
**Backward compat :** JSONL toujours ecrit en backup

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
| Hooks | `C:\Users\r2d2\.claude\hooks\` |
| Hooks logs | `C:\Users\r2d2\.claude\hooks\logs\` |
| Memory data | `C:\Users\r2d2\.claude\hooks\data\memory\` |
| Memory DB | `C:\Users\r2d2\.claude\hooks\data\memory.db` |
| Proxmox Host | `192.168.1.215` (SSH root, Web UI :8006) |
| VM 100 r2d2-stage | `192.168.1.162` (SSH root, DHCP, 6 containers monitoring) |
| VM 101 r2d2-monitor | `192.168.1.101` (SSH mint, desktop Linux Mint, pas de Docker) |
| VM 103 r2d2-main | `192.168.1.163` (SSH root, 29 containers, MultiPass stack + Taskyn + monitoring) |
| VM 104 r2d2-store | `192.168.1.164` (SSH r2d2helm, 7 containers, PostgreSQL + NFS + monitoring) |
| VM 105 r2d2-lab | `192.168.1.161` (SSH r2d2helm, 3 containers, RAG + Taskyn) |
| VM credentials | `C:\Users\r2d2\Documents\claude-config-backup\vm100-credentials.md` |

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

### Hooks
18. **Fail-open** : tous les hooks exit 0 en cas d'erreur, jamais bloquer Claude Code
19. **Path guard** : les chemins sensibles (.credentials, .env, secrets) sont bloqués en lecture ; les fichiers système (CLAUDE.md, hooks, agents) demandent confirmation en écriture
