# 🎯 Meta-Agent Router

Orchestrateur intelligent qui détecte automatiquement le contexte de la requête et active l'agent approprié.

## Agents Disponibles

| Agent | Domaine | Préfixe | Status |
|-------|---------|---------|--------|
| 🟠 Proxmox | Virtualisation, VMs, Conteneurs LXC, Cluster | `/pve-*` | ✅ Actif |
| 🔵 Windows | Windows 11, Server 2025, PowerShell, AD | `/win-*` | ✅ Actif |
| 🐧 Linux | Ubuntu, Debian, systemd, apt | `/linux-*` | ⏳ Prévu |
| 🐳 Docker | Conteneurs, Compose, Swarm, K8s | `/docker-*` | ⏳ Prévu |
| ☁️ Cloud | AWS, Azure, GCP, Terraform | `/cloud-*` | ⏳ Prévu |

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
│  aws|azure|gcp|terraform|ansible|cloud|s3|ec2|lambda           │
│  │                                                              │
│  └──→ ☁️ CLOUD-SKILL                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

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

#### 🐳 Docker/Kubernetes (docker-skill) [Prévu]

**Keywords primaires**:
- `docker`, `container`, `conteneur docker`, `dockerfile`
- `compose`, `docker-compose`, `stack`
- `kubernetes`, `k8s`, `kubectl`, `pod`, `deployment`
- `helm`, `ingress`, `service mesh`

#### 🐧 Linux (linux-skill) [Prévu]

**Keywords primaires**:
- `ubuntu`, `debian`, `centos`, `rhel`, `linux`
- `apt`, `yum`, `dnf`, `pacman`
- `systemd`, `systemctl`, `journalctl`
- `nginx`, `apache`, `ssh`, `iptables`

#### ☁️ Cloud (cloud-skill) [Prévu]

**Keywords primaires**:
- `aws`, `amazon`, `ec2`, `s3`, `lambda`, `rds`
- `azure`, `microsoft cloud`, `blob`, `aks`
- `gcp`, `google cloud`, `gke`, `bigquery`
- `terraform`, `ansible`, `pulumi`

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
├── SKILL.md                      ← CE FICHIER (Router)
├── proxmox-skill/
│   ├── SKILL.md
│   ├── commands/
│   └── wizards/
├── windows-skill/
│   ├── SKILL.md
│   ├── commands/
│   └── wizards/
├── docker-skill/                 [Prévu]
├── linux-skill/                  [Prévu]
└── cloud-skill/                  [Prévu]
```

## Exemples de Routing

### Exemple 1: Détection Simple
```
User: "Comment voir l'état de mon cluster Proxmox?"
Router: Keywords [cluster, proxmox] → 🟠 proxmox-skill
Action: Charger /pve-cluster, répondre avec status cluster
```

### Exemple 2: Détection Windows
```
User: "Configure le firewall pour autoriser RDP"
Router: Keywords [firewall, rdp] → 🔵 windows-skill
Action: Charger /win-firewall, /win-rdp
```

### Exemple 3: Multi-Contexte
```
User: "Déploie un conteneur LXC Ubuntu puis configure SSH"
Router: 
  - Phase 1: [conteneur, lxc] → 🟠 proxmox-skill (/pve-ct)
  - Phase 2: [ubuntu, ssh] → 🐧 linux-skill (/linux-ssh)
Action: Réponse séquentielle avec les deux contextes
```

### Exemple 4: Ambiguïté
```
User: "Fais un backup"
Router: Ambigu - backup existe dans plusieurs contextes
Action: Demander clarification (Proxmox? Windows? Docker?)
```

### Exemple 5: Commande Explicite
```
User: "/pve-status"
Router: Commande explicite → 🟠 proxmox-skill direct
Action: Exécuter sans analyse
```

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
