---
name: meta-router
description: Routeur intelligent pour les 19 skills du systeme MultiPass
prefix: /router
version: 1.7.0
---

# 🎯 Meta-Agent Router

Orchestrateur intelligent qui détecte automatiquement le contexte de la requête et active l'agent approprié.

## Agents Disponibles

| Agent | Domaine | Préfixe | Status |
|-------|---------|---------|--------|
| 🟠 Proxmox | Virtualisation, VMs, Conteneurs LXC, Cluster | `/pve-*` | ✅ Actif |
| 🔵 Windows | Windows 11, Server 2025, PowerShell, AD | `/win-*` | ✅ Actif |
| 🐳 Docker | Conteneurs, Compose, Images, Volumes | `/dk-*` | ✅ Actif |
| 🐧 Linux | Ubuntu, Debian, systemd, services | `/lx-*` | ✅ Actif |
| 🗂️ Obsidian | Maintenance vault, liens, tags, santé | `/obs-*` | ✅ Actif |
| 🧠 Knowledge | Capture, résumé, organisation notes | `/know-*` | ✅ Actif |
| 🔍 Watcher | Surveillance sources, pipeline, queue | `/kwatch-*` | ✅ Actif |
| 📁 FileOrg | Organisation fichiers, doublons, tri | `/file-*` | ✅ Actif |
| 🛡️ Guardian | Maintenance proactive vault, auto-fix | `/guardian-*` | ✅ Actif |
| ⚡ QElectroTech | Plans électriques, schémas, normes NF C 15-100 | `/qet-*` | ✅ Actif |
| 📋 SOP Creator | Runbooks, playbooks, SOPs, documentation opérationnelle | `/sop-*` | ✅ Actif |
| 🔧 Skill Creator | Création et validation de skills Claude Code | `/skill-*` | ✅ Actif |
| 📡 Monitoring | Metriques, alertes, containers, logs, disponibilite | `/mon-*` | ✅ Actif |
| 💾 Backup | Sauvegardes, restauration, retention, disaster recovery | `/bak-*` | ✅ Actif |
| 🔒 Security | Securite, audit, hardening, SSL/TLS, vulnerabilites | `/sec-*` | ✅ Actif |
| 🌐 Network | Reseau, DNS, ports, routing, VPN, connectivite inter-VM | `/net-*` | ✅ Actif |
| 🚀 DevOps | CI/CD, deploiement, pipelines, git workflows | `/devops-*` | ✅ Actif |
| 🤖 AI Infra | LiteLLM, Langfuse, RAG, modeles LLM, embeddings | `/ai-*` | ✅ Actif |
| 🗄️ Supabase | Auth, database PostgreSQL, storage, edge functions, RLS | `/supa-*` | ✅ Actif |
<!-- cloud-skill: prevu, non implemente | ☁️ Cloud | AWS, Azure, GCP, Terraform | `/cloud-*` | ⏳ Prévu | -->

## Détection Automatique du Contexte

### Règles de Routing

```
┌─────────────────────────────────────────────────────────────────┐
│                    REQUÊTE UTILISATEUR                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ANALYSE KEYWORDS                              │
│                                                                 │
│  proxmox|pve|qemu|lxc|ceph|zfs|cluster|ha|corosync             │
│  │                                                              │
│  └──→ 🟠 PROXMOX-SKILL                                         │
│                                                                 │
│  windows|powershell|defender|bitlocker|rdp|iis|hyper-v|gpo|ad  │
│  │                                                              │
│  └──→ 🔵 WINDOWS-SKILL                                         │
│                                                                 │
│  docker|container|compose|swarm|kubernetes|k8s|pod|helm        │
│  │                                                              │
│  └──→ 🐳 DOCKER-SKILL                                          │
│                                                                 │
│  ubuntu|debian|apt|systemd|nginx|apache|ssh|linux|bash         │
│  │                                                              │
│  └──→ 🐧 LINUX-SKILL                                           │
│                                                                 │
│  [cloud-skill: prevu, non implemente]                           │
│  <!-- aws|azure|gcp|terraform|ansible|cloud|s3|ec2|lambda -->   │
│  <!-- └──→ ☁️ CLOUD-SKILL -->                                   │
│                                                                 │
│  obsidian|vault|liens|orphelines|frontmatter|tags|backup-vault  │
│  │                                                              │
│  └──→ 🗂️ OBSIDIAN-SKILL                                        │
│                                                                 │
│  know-save|know-search|capture|résumé|zettelkasten|note|pkm    │
│  │                                                              │
│  └──→ 🧠 KNOWLEDGE-SKILL                                       │
│                                                                 │
│  kwatch|watcher|surveillance|queue|pipeline|sources|tier        │
│  │                                                              │
│  └──→ 🔍 KNOWLEDGE-WATCHER-SKILL                               │
│                                                                 │
│  file-organize|fichiers|doublons|renommer|dupliqu|downloads     │
│  │                                                              │
│  └──→ 📁 FILEORG-SKILL                                         │
│                                                                 │
│  vault-guardian|santé|health|maintenance|auto-fix|rapport-vault  │
│  │                                                              │
│  └──→ 🛡️ VAULT-GUARDIAN-SKILL                                  │
│                                                                 │
│  qelectrotech|qet|electrique|schema|folio|unifilaire|disjoncteur│
│  │                                                              │
│  └──→ ⚡ QELECTROTECH-SKILL                                    │
│                                                                 │
│  sop|runbook|playbook|documentation|procedure|checklist         │
│  │                                                              │
│  └──→ 📋 SOP-CREATOR                                           │
│                                                                 │
│  skill-create|new-skill|create skill|build skill|init skill     │
│  │                                                              │
│  └──→ 🔧 SKILL-CREATOR                                         │
│                                                                 │
│  monitoring|beszel|netdata|uptime|kuma|dozzle|ntfy|metriques    │
│  |alertes|containers status|logs docker                         │
│  │                                                              │
│  └──→ 📡 MONITORING-SKILL                                      │
│                                                                 │
│  backup|restore|snapshot|recovery|disaster|rsync|retention       │
│  |dump|pg_dump|sauvegarde|archivage                              │
│  │                                                              │
│  └──→ 💾 BACKUP-SKILL                                           │
│                                                                 │
│  security|securite|ssl|tls|certificate|audit|hardening          │
│  |vulnerability|cve|fail2ban|chiffrement                        │
│  │                                                              │
│  └──→ 🔒 SECURITY-SKILL                                         │
│                                                                 │
│  network|reseau|dns|vlan|subnet|ping|traceroute|nmap|netstat    │
│  |routing|arp|interface|bridge|gateway                          │
│  │                                                              │
│  └──→ 🌐 NETWORK-SKILL                                          │
│                                                                 │
│  devops|deploy|deploiement|pipeline|cicd|release|rollback       │
│  |automatisation|cron|crontab                                    │
│  │                                                              │
│  └──→ 🚀 DEVOPS-SKILL                                           │
│                                                                 │
│  litellm|langfuse|rag|llm|embedding|vector|pgvector|ollama     │
│  |inference|prompt management|ai infra                           │
│  │                                                              │
│  └──→ 🤖 AI-INFRA-SKILL                                         │
│                                                                 │
│  supabase|postgrest|gotrue|realtime|rls|row level security      │
│  |edge function|supabase auth|supabase storage                   │
│  │                                                              │
│  └──→ 🗄️ SUPABASE-SKILL                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Règles de Désambiguïsation

Certains keywords secondaires sont partagés entre skills. Appliquer ces règles de priorité :

| Keyword ambigu | Contexte | Skill cible |
|---------------|----------|-------------|
| `backup` | + proxmox/pve/vzdump | proxmox-skill |
| `backup` | + windows/système/bitlocker | windows-skill |
| `backup` | + vault/obsidian | obsidian-skill |
| `backup` | (seul, sans contexte) | **Demander clarification** |
| `service` | + windows/powershell/sc | windows-skill |
| `service` | + linux/systemd/systemctl | linux-skill |
| `service` | + docker/compose | docker-skill |
| `service` | (seul, sans contexte) | **Demander clarification** |
| `firewall` | + proxmox/pve | proxmox-skill |
| `firewall` | + windows/defender/netsh | windows-skill |
| `firewall` | + linux/iptables/ufw/nftables | linux-skill |
| `firewall` | (seul, sans contexte) | **Demander clarification** |
| `maintenance` | + vault/obsidian/notes | vault-guardian-skill |
| `maintenance` | + windows/système/disque | windows-skill |
| `tags` | + vault/obsidian/notes | obsidian-skill |
| `tags` | + capture/know/pkm | knowledge-skill |
| `notes` | + vault/liens/orphelines | obsidian-skill |
| `notes` | + capture/résumé/save | knowledge-skill |
| `containers` | + monitoring/metriques/stats | monitoring-skill |
| `containers` | + docker/compose/build | docker-skill |
| `alertes` | + monitoring/beszel/serveurs | monitoring-skill |
| `logs` | + monitoring/containers/dozzle | monitoring-skill |
| `logs` | + linux/systemd/journalctl | linux-skill |

**Règle générale** : si un keyword ambigu est utilisé SEUL sans contexte clair, demander à l'utilisateur de préciser le domaine avant de router.

### Patterns de Détection Détaillés

#### 🟠 Proxmox VE (proxmox-skill)

**Keywords primaires** (haute confiance):
- `proxmox`, `pve`, `qemu`, `lxc`, `vzdump`, `pveam`
- `cluster proxmox`, `corosync`, `pmxcfs`
- `ceph`, `zfs pool`, `storage proxmox`

**Keywords secondaires** (contexte requis):
- `vm`, `conteneur`, `template` → si contexte virtualisation/homelab
- `backup`, `snapshot` → si mention proxmox/pve
- `ha`, `haute disponibilité` → si contexte cluster

**Commandes activées**: `/pve-status`, `/pve-vm`, `/pve-ct`, `/pve-storage`, `/pve-backup`, `/pve-cluster`, `/pve-ha`, `/pve-network`, `/pve-firewall`, `/pve-wizard`

#### 🔵 Windows (windows-skill)

**Keywords primaires** (haute confiance):
- `windows`, `powershell`, `cmd`, `batch`
- `defender`, `bitlocker`, `gpo`, `group policy`
- `active directory`, `ad ds`, `domain controller`
- `iis`, `rdp`, `remote desktop`, `winrm`
- `hyper-v`, `wsl`, `windows server`

**Keywords secondaires** (contexte requis):
- `service`, `registry`, `task scheduler` → si contexte Windows
- `firewall`, `certificat` → si mention Windows/PowerShell
- `utilisateur`, `groupe` → si contexte Windows/AD

**Commandes activées**: `/win-diagnostic`, `/win-network`, `/win-security`, `/win-defender`, `/win-backup`, `/win-users`, `/win-services`, `/win-wizard`

#### 🐳 Docker (docker-skill)

**Keywords primaires** (haute confiance):
- `docker`, `container`, `conteneur docker`, `dockerfile`
- `compose`, `docker-compose`, `stack`
- `docker volume`, `docker network`, `docker build`
- `registry`, `docker image`, `docker prune`

**Keywords secondaires** (contexte requis):
- `image`, `volume`, `network` → si contexte Docker
- `build`, `deploy` → si mention conteneur/compose
- `logs`, `exec` → si contexte conteneur

**Commandes activées** (13): `/dk-ps`, `/dk-images`, `/dk-compose`, `/dk-volume`, `/dk-network`, `/dk-build`, `/dk-logs`, `/dk-exec`, `/dk-prune`, `/dk-stats`, `/dk-registry`, `/dk-swarm`, `/dk-security`

#### 🐧 Linux (linux-skill)

**Keywords primaires** (haute confiance):
- `ubuntu`, `debian`, `centos`, `rhel`, `rocky`, `linux`
- `apt`, `yum`, `dnf`, `pacman`
- `systemd`, `systemctl`, `journalctl`
- `nginx`, `apache`, `ssh`, `iptables`, `ufw`

**Keywords secondaires** (contexte requis):
- `service`, `package` → si contexte Linux
- `firewall`, `cron` → si contexte serveur Linux
- `utilisateur`, `groupe` → si contexte Linux/SSH
- `curl`, `wget`, `git` → si contexte serveur/CLI

**Commandes activées** (17): `/lx-status`, `/lx-services`, `/lx-packages`, `/lx-users`, `/lx-firewall`, `/lx-network`, `/lx-disk`, `/lx-logs`, `/lx-cron`, `/lx-process`, `/lx-security`, `/lx-performance`, `/lx-backup`, `/lx-ssh`, `/lx-dns`, `/lx-nginx`, `/lx-certbot`

#### 🗂️ Obsidian (obsidian-skill)

**Keywords primaires** (haute confiance):
- `obsidian`, `vault`, `obs-health`, `obs-clean`, `obs-links`, `obs-tags`
- `liens cassés`, `broken links`, `orphelines`, `frontmatter`
- `backup vault`, `wikilinks`, `dataview`

**Keywords secondaires** (contexte requis):
- `tags`, `liens`, `notes` -> si contexte vault/obsidian
- `nettoyage`, `maintenance` -> si mention vault
- `graphe`, `backlinks` -> si contexte notes

**Commandes activées** (31): `/obs-health`, `/obs-stats`, `/obs-orphans`, `/obs-links`, `/obs-tags`, `/obs-clean`, `/obs-frontmatter`, `/obs-backup`, `/obs-graph`, `/obs-links-unlinked`, `/obs-links-suggest`, `/obs-links-fix`, `/obs-tags-unused`, `/obs-tags-rename`, `/obs-tags-merge`, `/obs-tags-hierarchy`, `/obs-structure`, `/obs-move`, `/obs-rename`, `/obs-templates`, `/obs-duplicates`, `/obs-attachments`, `/obs-empty`, `/obs-export`, `/obs-sync`, `/obs-config`, `/obs-plugins`, `/obs-hotkeys`, `/obs-wizard-audit`, `/obs-wizard-cleanup`, `/obs-wizard-reorganize`

#### 🧠 Knowledge Capture (knowledge-skill)

**Keywords primaires** (haute confiance):
- `know-save`, `know-search`, `know-export`, `capture`
- `zettelkasten`, `second brain`, `pkm`, `résumé conversation`
- `sauvegarder conversation`, `extraire connaissances`

**Keywords secondaires** (contexte requis):
- `note`, `concept` -> si contexte capture/sauvegarde
- `résumé`, `synthèse` -> si mention conversation
- `index`, `moc` -> si contexte knowledge base
- `tagging`, `metadata` -> si contexte notes/organisation

**Commandes activées**: `/know-save`, `/know-search`, `/know-export`, `/know-quick`, `/know-list`, `/know-index`

#### 🔍 Knowledge Watcher (knowledge-watcher-skill)

**Keywords primaires** (haute confiance):
- `kwatch`, `watcher`, `knowledge watcher`, `surveillance`
- `queue`, `pipeline`, `sources`, `tier`
- `kwatch-start`, `kwatch-stop`, `kwatch-status`, `kwatch-process`

**Keywords secondaires** (contexte requis):
- `moniteur`, `automatique` -> si contexte capture
- `claude history`, `batch` -> si contexte watcher
- `scheduler`, `tâche planifiée` -> si contexte surveillance

**Commandes activées**: `/kwatch-start`, `/kwatch-stop`, `/kwatch-status`, `/kwatch-process`, `/kwatch-config`, `/kwatch-logs`

#### 📁 File Organization (fileorg-skill)

**Keywords primaires** (haute confiance):
- `file-organize`, `file-rename`, `file-analyze`, `file-duplicates`
- `organiser fichiers`, `doublons`, `renommer fichiers`
- `downloads`, `nettoyage dossier`, `trier fichiers`

**Keywords secondaires** (contexte requis):
- `fichiers`, `dossier` -> si contexte organisation
- `dupliqu`, `identique` -> si contexte fichiers
- `taille`, `ancien` -> si contexte nettoyage

**Commandes activées** (21): `/file-organize`, `/file-rename`, `/file-analyze`, `/file-duplicates`, `/file-clean`, `/file-structure`, `/file-archive`, `/file-empty`, `/file-large`, `/file-sort`, `/file-flatten`, `/file-prefix`, `/file-normalize`, `/file-version`, `/file-audit`, `/file-old`, `/file-trash`, `/file-backup`, `/file-sync`, `/file-mirror`, `/file-wizard`

#### 🛡️ Vault Guardian (vault-guardian-skill)

**Keywords primaires** (haute confiance):
- `vault-guardian`, `guardian`, `santé vault`, `health check`
- `maintenance automatique`, `auto-fix`, `rapport santé`
- `audit vault`, `surveillance vault`

**Keywords secondaires** (contexte requis):
- `maintenance`, `santé` -> si contexte vault/obsidian
- `rapport`, `score` -> si contexte vault health
- `automatique`, `planifié` -> si contexte maintenance

**Commandes activées**: `/guardian-health`, `/guardian-fix`, `/guardian-report`, `/guardian-schedule`

#### ⚡ QElectroTech (qelectrotech-skill)

**Keywords primaires** (haute confiance):
- `qelectrotech`, `qet`, `.qet`, `.elmt`, `unifilaire`
- `plan electrique`, `schema electrique`, `folio`
- `tableau electrique`, `TGBT`, `disjoncteur`, `differentiel`
- `NF C 15-100`, `nfc15100`, `norme electrique`
- `cartouche`, `titleblock`, `bornier`, `terminal strip`
- `crossref`, `reference croisee`, `master/slave`
- `auto-numerotation`, `autonumber`

**Keywords secondaires** (contexte requis):
- `prise`, `interrupteur`, `lampe`, `eclairage` → si contexte plan/schema
- `circuit`, `cable`, `section` → si contexte electrique
- `devis`, `nomenclature`, `BOM` → si contexte projet electrique
- `conducteur`, `borne`, `bornier` → si contexte schema
- `DXF`, `SVG`, `element` → si contexte QET/CAO
- `IEC 81346`, `plant`, `localisation` → si contexte schema industriel

**Commandes activées** (35): `/qet-create`, `/qet-open`, `/qet-merge`, `/qet-info`, `/qet-export`, `/qet-backup`, `/qet-bom`, `/qet-element-search`, `/qet-element-create`, `/qet-element-import`, `/qet-element-list`, `/qet-element-catalog`, `/qet-element-transform`, `/qet-folio-add`, `/qet-folio-list`, `/qet-folio-reorder`, `/qet-folio-rename`, `/qet-folio-extract`, `/qet-circuit`, `/qet-panel`, `/qet-nfc15100`, `/qet-sizing`, `/qet-conductors`, `/qet-devis`, `/qet-materials`, `/qet-titleblock`, `/qet-autonumber`, `/qet-crossref`, `/qet-terminal-strip`, `/qet-validate`, `/qet-variables`, `/qet-diff`, `/qet-stats`, `/qet-dxf-import`, `/qet-wizard`

#### 📋 SOP Creator (sop-creator)

**Keywords primaires** (haute confiance):
- `sop`, `runbook`, `playbook`, `procedure`, `documentation operationnelle`
- `sop-create`, `creer runbook`, `documenter processus`
- `checklist`, `decision tree`, `how-to guide`

**Keywords secondaires** (contexte requis):
- `documenter`, `processus` -> si contexte operations/maintenance
- `guide`, `template` -> si contexte documentation
- `incident`, `on-call` -> si contexte runbook

**Commandes activees**: `/sop-create`

#### 🔧 Skill Creator (skill-creator)

**Keywords primaires** (haute confiance):
- `skill-create`, `new-skill`, `create skill`, `build skill`
- `init skill`, `initialiser skill`, `creer skill`
- `skill-creator`, `skill builder`

**Keywords secondaires** (contexte requis):
- `skill` -> si contexte creation/developpement
- `SKILL.md`, `commands/` -> si contexte structure skill
- `validate skill` -> si contexte verification

**Commandes activees**: `/skill-create`

#### 📡 Monitoring (monitoring-skill)

**Keywords primaires** (haute confiance):
- `monitoring`, `beszel`, `netdata`, `uptime kuma`, `dozzle`, `ntfy`
- `mon-status`, `mon-systems`, `mon-containers`, `mon-alerts`
- `metriques serveur`, `dashboard monitoring`, `alertes monitoring`
- `homelab monitoring`, `sante infra`, `health check infra`

**Keywords secondaires** (contexte requis):
- `containers`, `stats` -> si contexte monitoring/metriques (pas docker-skill)
- `alertes`, `notifications` -> si contexte monitoring/serveurs
- `logs` -> si contexte monitoring/containers (pas linux-skill)
- `uptime`, `disponibilite` -> si contexte services/monitoring

**Commandes activees** (10): `/mon-status`, `/mon-systems`, `/mon-containers`, `/mon-alerts`, `/mon-metrics`, `/mon-logs`, `/mon-uptime`, `/mon-notify`, `/mon-config`, `/mon-health`


| 💾 Backup | Sauvegardes, restauration, retention, disaster recovery | `/bak-*` | ✅ Actif |
| 🔒 Security | Securite, audit, hardening, SSL/TLS, vulnerabilites | `/sec-*` | ✅ Actif |
| 🌐 Network | Reseau, DNS, ports, routing, VPN, connectivite inter-VM | `/net-*` | ✅ Actif |
| 🚀 DevOps | CI/CD, deploiement, pipelines, git workflows | `/devops-*` | ✅ Actif |
| 🤖 AI Infra | LiteLLM, Langfuse, RAG, modeles LLM, embeddings | `/ai-*` | ✅ Actif |
| 🗄️ Supabase | Auth, database PostgreSQL, storage, edge functions, RLS | `/supa-*` | ✅ Actif |
<!-- cloud-skill: prevu, non implemente
#### ☁️ Cloud (cloud-skill) [Prévu]

**Keywords primaires**:
- `aws`, `amazon`, `ec2`, `s3`, `lambda`, `rds`
- `azure`, `microsoft cloud`, `blob`, `aks`
- `gcp`, `google cloud`, `gke`, `bigquery`
- `terraform`, `ansible`, `pulumi`
-->

## Commandes Meta-Agent

### Commande Universelle

```
/infra [contexte] <action> [options]
```

**Exemples:**
```
/infra status                    → Détecte auto et affiche status
/infra proxmox status            → Force contexte Proxmox
/infra windows diagnostic        → Force contexte Windows
/infra wizard                    → Liste wizards disponibles
```

### Commandes de Gestion

| Commande | Description |
|----------|-------------|
| `/agents` | Liste tous les agents disponibles et leur status |
| `/agents status` | État détaillé de chaque agent |
| `/agents help <agent>` | Aide spécifique à un agent |
| `/context` | Affiche le contexte actuellement détecté |
| `/context set <agent>` | Force un contexte spécifique |
| `/context auto` | Réactive la détection automatique |

## Logique de Décision

### Priorité de Détection

```
1. Commande explicite (/pve-*, /win-*) → Agent direct
2. Préfixe contexte (@proxmox, @windows) → Agent forcé
3. Keywords primaires détectés → Agent correspondant
4. Keywords secondaires + contexte → Agent probable
5. Historique conversation → Agent précédent
6. Aucune correspondance → Demander clarification
```

### Gestion des Ambiguïtés

Quand plusieurs agents correspondent:

```
┌─────────────────────────────────────────────────────────────────┐
│ 🤔 CONTEXTE AMBIGU DÉTECTÉ                                      │
│                                                                 │
│ Votre requête pourrait concerner plusieurs domaines:            │
│                                                                 │
│ [1] 🟠 Proxmox - "backup vm" détecté                           │
│ [2] 🔵 Windows - "backup" détecté                              │
│                                                                 │
│ Précisez le contexte ou utilisez:                               │
│ • /pve-backup pour Proxmox                                      │
│ • /win-backup pour Windows                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Requêtes Multi-Contexte

Pour les requêtes impliquant plusieurs systèmes:

```
Requête: "Créer une VM Windows sur Proxmox avec RDP activé"

Détection:
├── Proxmox (création VM) → proxmox-skill
└── Windows (config RDP) → windows-skill

Réponse séquentielle:
1. [Proxmox] Création VM avec template Windows
2. [Windows] Configuration RDP post-installation
```

## Format de Réponse

### En-tête Contextuel

Chaque réponse indique l'agent actif:

```
┌─────────────────────────────────────────────────────────────────┐
│ 🟠 PROXMOX-AGENT │ Contexte: Gestion VM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ [Contenu de la réponse...]                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Suggestions Contextuelles

À la fin des réponses, suggérer des commandes pertinentes:

```
───────────────────────────────────────────────────────────────────
💡 Commandes associées:
   /pve-vm list          Lister toutes les VMs
   /pve-vm start 100     Démarrer VM 100
   /pve-wizard vm        Assistant création VM
───────────────────────────────────────────────────────────────────
```

## Structure des Skills

```
~/.claude/skills/
├── SKILL.md              ← CE FICHIER (Router)
├── proxmox-skill/        ← Infra: Proxmox VE (22 cmd, 11 wizards)
├── windows-skill/        ← Infra: Windows (37 cmd, 10 wizards)
├── docker-skill/         ← Infra: Docker (13 cmd, 3 wizards)
├── linux-skill/          ← Infra: Linux (17 cmd, 3 wizards)
├── obsidian-skill/       ← Data: Vault maintenance (28 cmd, 3 wizards)
├── knowledge-skill/      ← Data: Capture connaissances (3 cmd, 1 wizard)
├── knowledge-watcher-skill/ ← Data: Pipeline automatisé (6 cmd, 2 wizards)
├── fileorg-skill/        ← Utils: Organisation fichiers (20 cmd, 1 wizard)
├── vault-guardian-skill/ ← Data: Maintenance proactive (4 cmd)
├── qelectrotech-skill/   ← CAO: Plans électriques (35 cmd, 9 wizards)
├── sop-creator/          ← Docs: SOPs et runbooks (1 cmd, 6 templates)
├── skill-creator/        ← Meta: Création de skills (1 cmd)
├── monitoring-skill/     ← Infra: Monitoring homelab (10 cmd, 2 wizards)
<!-- └── cloud-skill/       [Prévu - cloud-skill: prevu, non implemente] -->
```

## Exemples de Routing

> Voir `references/routing-examples.md` pour 5 scénarios détaillés (simple, Windows, multi-contexte, ambiguïté, commande explicite).

## Maintenance

### Ajouter un Nouvel Agent

1. Créer le dossier `~/.claude/skills/<agent>-skill/`
2. Ajouter SKILL.md avec commandes
3. Mettre à jour ce fichier (patterns de détection)
4. Tester le routing

### Debugging

```
/router debug                    → Affiche la logique de décision
/router test "ma requête"        → Teste le routing sans exécuter
/router logs                     → Historique des décisions
```
