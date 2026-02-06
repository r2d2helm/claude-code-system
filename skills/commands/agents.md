# Commande: /agents

Gestion des agents disponibles dans le Meta-Router.

## Syntaxe

```
/agents [action] [options]
```

## Actions

### /agents (sans argument)

Liste tous les agents avec leur statut :

```
╔══════════════════════════════════════════════════════════════╗
║                    🎯 AGENTS DISPONIBLES                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Agent          │ Status │ Commandes │ Wizards │ Version    ║
║  ────────────────┼────────┼───────────┼─────────┼──────────  ║
║  🟠 proxmox     │ ✅ ON  │    20     │   11    │ 1.0.0      ║
║  🔵 windows     │ ✅ ON  │    36     │   10    │ 1.0.0      ║
║  🐧 linux       │ ⏳ ---  │    --     │   --    │ Prévu      ║
║  🐳 docker      │ ⏳ ---  │    --     │   --    │ Prévu      ║
║  ☁️  cloud       │ ⏳ ---  │    --     │   --    │ Prévu      ║
║                                                              ║
║  Total: 2 actifs │ 56 commandes │ 21 wizards                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

💡 Utilisez /agents help <agent> pour plus de détails
```

### /agents status

État détaillé de chaque agent :

```
╔══════════════════════════════════════════════════════════════╗
║                   📊 STATUS DÉTAILLÉ                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🟠 PROXMOX-SKILL                                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Path    : ~/.claude/skills/proxmox-skill/               │ ║
║  │ SKILL.md: ✅ Présent (6.5 KB)                           │ ║
║  │ Commands: 20 fichiers (295 KB)                          │ ║
║  │ Wizards : 11 fichiers (95 KB)                           │ ║
║  │ Préfixe : /pve-*                                        │ ║
║  │ Keywords: proxmox, pve, qemu, lxc, ceph, zfs...         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  🔵 WINDOWS-SKILL                                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Path    : ~/.claude/skills/windows-skill/               │ ║
║  │ SKILL.md: ✅ Présent (6.1 KB)                           │ ║
║  │ Commands: 36 fichiers (550 KB)                          │ ║
║  │ Wizards : 10 fichiers (130 KB)                          │ ║
║  │ Préfixe : /win-*                                        │ ║
║  │ Keywords: windows, powershell, defender, rdp, ad...     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /agents help <agent>

Aide spécifique à un agent :

```
/agents help proxmox
```

```
╔══════════════════════════════════════════════════════════════╗
║              🟠 PROXMOX-SKILL - AIDE                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  DESCRIPTION                                                 ║
║  Agent d'administration Proxmox VE 9.0+ avec commandes       ║
║  slash et wizards interactifs.                               ║
║                                                              ║
║  COMMANDES PRINCIPALES                                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ /pve-status      État global cluster                    │ ║
║  │ /pve-vm          Gestion machines virtuelles            │ ║
║  │ /pve-ct          Gestion conteneurs LXC                 │ ║
║  │ /pve-storage     Stockage (ZFS, Ceph, NFS...)           │ ║
║  │ /pve-backup      Sauvegarde et restauration             │ ║
║  │ /pve-network     Configuration réseau                   │ ║
║  │ /pve-ha          Haute disponibilité                    │ ║
║  │ /pve-wizard      Assistants interactifs                 │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  KEYWORDS DE DÉTECTION                                       ║
║  proxmox, pve, qemu, kvm, lxc, vzdump, ceph, zfs,           ║
║  cluster, corosync, ha, template, storage                    ║
║                                                              ║
║  EXEMPLES                                                    ║
║  • "Créer une VM Ubuntu sur Proxmox"                         ║
║  • "État du cluster PVE"                                     ║
║  • "Configurer Ceph sur mes nœuds"                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /agents commands <agent>

Liste toutes les commandes d'un agent :

```
/agents commands windows
```

```
╔══════════════════════════════════════════════════════════════╗
║           🔵 WINDOWS-SKILL - COMMANDES                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  SYSTÈME (7)                                                 ║
║  /win-diagnostic  /win-perf  /win-maintenance                ║
║  /win-inventory   /win-troubleshoot  /win-update             ║
║  /win-logs                                                   ║
║                                                              ║
║  RÉSEAU (6)                                                  ║
║  /win-network  /win-vpn  /win-wifi  /win-rdp                 ║
║  /win-ssh  /win-firewall                                     ║
║                                                              ║
║  SÉCURITÉ (4)                                                ║
║  /win-security  /win-defender  /win-bitlocker  /win-certs    ║
║                                                              ║
║  STOCKAGE (2)                                                ║
║  /win-disk  /win-backup                                      ║
║                                                              ║
║  DÉVELOPPEMENT (7)                                           ║
║  /win-git  /win-docker  /win-wsl  /win-hyperv                ║
║  /win-powershell  /win-env  /win-pkg                         ║
║                                                              ║
║  INFRASTRUCTURE (4)                                          ║
║  /win-iis  /win-tasks  /win-registry  /win-drivers           ║
║                                                              ║
║  UTILISATEURS (3)                                            ║
║  /win-users  /win-services  /win-apps                        ║
║                                                              ║
║  PÉRIPHÉRIQUES (2)                                           ║
║  /win-printer  /win-bluetooth                                ║
║                                                              ║
║  WIZARDS (1)                                                 ║
║  /win-wizard [setup|security|network|dev|...]                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /agents wizards <agent>

Liste les wizards d'un agent :

```
/agents wizards proxmox
```

```
╔══════════════════════════════════════════════════════════════╗
║           🟠 PROXMOX-SKILL - WIZARDS                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Wizard              │ Étapes │ Description                  ║
║  ────────────────────┼────────┼────────────────────────────  ║
║  /pve-wizard vm      │   6    │ Création VM guidée           ║
║  /pve-wizard ct      │   5    │ Création conteneur LXC       ║
║  /pve-wizard cluster │   7    │ Configuration cluster        ║
║  /pve-wizard ceph    │   8    │ Déploiement Ceph             ║
║  /pve-wizard backup  │   4    │ Stratégie sauvegarde         ║
║  /pve-wizard ha      │   5    │ Haute disponibilité          ║
║  /pve-wizard network │   6    │ Configuration réseau         ║
║  /pve-wizard storage │   5    │ Configuration stockage       ║
║  /pve-wizard migrate │   4    │ Migration VM/CT              ║
║  /pve-wizard security│   6    │ Hardening sécurité           ║
║  /pve-wizard template│   4    │ Création templates           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
