---
name: proxmox-skill
description: Administration Proxmox VE 9+
prefix: /pve-*
---

# 🖥️ Proxmox VE 9+ Super Agent Skill

## Description
Agent IA d'administration complète pour Proxmox Virtual Environment 9.x.
Conçu pour Claude Code avec commandes slash modulaires et wizards interactifs.

## Version & Compatibilité
- **Version Agent**: 2.0.0
- **Proxmox VE**: 9.0, 9.1+ (Debian 13 "Trixie")
- **Kernel**: 6.14+ / 6.17+
- **QEMU**: 10.0+ / 10.1+
- **LXC**: 6.0.4+
- **Ceph**: Squid 19.2.x
- **ZFS**: 2.3.3+
- **PBS**: 4.x

## Prérequis
- Accès SSH au(x) node(s) Proxmox
- Utilisateur avec privilèges appropriés (root ou PVEAdmin)
- API Token configuré pour automation

## Structure des Commandes

### Commandes Slash Disponibles

| Catégorie | Commande | Description |
|-----------|----------|-------------|
| **Cluster** | `/pve-status` | Vue d'ensemble cluster et nodes |
| | `/pve-cluster` | Gestion cluster Corosync |
| **Compute** | `/pve-vm` | Gestion machines virtuelles KVM |
| | `/pve-ct` | Gestion conteneurs LXC |
| | `/pve-template` | Gestion templates et Cloud-Init |
| **Storage** | `/pve-storage` | Gestion stockage (local, NFS, iSCSI) |
| | `/pve-zfs` | Administration ZFS |
| | `/pve-ceph` | Administration Ceph |
| **Backup** | `/pve-backup` | Backup vzdump et PBS |
| | `/pve-restore` | Restauration VMs/CTs |
| **Network** | `/pve-network` | Configuration réseau bridges |
| | `/pve-sdn` | Software-Defined Networking |
| | `/pve-firewall` | Firewall Proxmox |
| **HA** | `/pve-ha` | Haute Disponibilité |
| | `/pve-snapshot` | Gestion snapshots VM/CT |
| | `/pve-migrate` | Migration live/offline |
| | `/pve-pool` | Pools de ressources |
| | `/pve-replication` | Réplication ZFS inter-nodes |
| | `/pve-tags` | Tags PVE 9+ |
| **GPU** | `/pve-gpu` | Passthrough GPU/PCI (IOMMU, VFIO) |
| **Certificats** | `/pve-acme` | Let's Encrypt SSL via ACME |
| **Security** | `/pve-security` | Hardening et sécurité |
| | `/pve-users` | Utilisateurs et permissions |
| **Monitoring** | `/pve-monitor` | Monitoring et métriques |
| **Automation** | `/pve-api` | API REST et automation |
| | `/pve-terraform` | Infrastructure as Code |
| **Troubleshoot** | `/pve-diag` | Diagnostic et dépannage |
| **Wizards** | `/pve-wizard` | Assistants de configuration |

## Utilisation

### Syntaxe Générale
```
/pve-<commande> [action] [options]
```

### Exemples
```bash
# Vue d'ensemble
/pve-status

# Lister les VMs
/pve-vm list

# Créer une VM avec wizard
/pve-vm create --wizard

# Snapshot une VM
/pve-vm snapshot 100 --name "pre-upgrade"

# Configurer SDN
/pve-sdn zone create vlan --wizard

# Diagnostic complet
/pve-diag full
```

## Wizards Interactifs

Les wizards guident l'utilisateur étape par étape pour les tâches complexes :

| Wizard | Commande | Description |
|--------|----------|-------------|
| Initial Setup | `/pve-wizard setup` | Configuration initiale node |
| VM Creation | `/pve-wizard vm` | Création VM optimisée |
| CT Creation | `/pve-wizard ct` | Création conteneur |
| Template | `/pve-wizard template` | Création template Cloud-Init |
| Cluster | `/pve-wizard cluster` | Setup cluster multi-nodes |
| Ceph | `/pve-wizard ceph` | Déploiement Ceph |
| HA | `/pve-wizard ha` | Configuration haute dispo |
| Backup | `/pve-wizard backup` | Stratégie backup 3-2-1 |
| Security | `/pve-wizard security` | Hardening production |
| SDN | `/pve-wizard sdn` | Configuration SDN/VLAN |
| Migration | `/pve-wizard migrate` | Migration depuis autre hyperviseur |

## Best Practices 2025-2026

### VMs (KVM/QEMU)
- Machine type: **q35** (PCIe natif)
- BIOS: **OVMF/UEFI** avec Secure Boot
- CPU: **host** pour performance maximale
- Disque: **VirtIO SCSI Single** + iothread + discard
- Réseau: **VirtIO** avec firewall activé
- Agent: **QEMU Guest Agent** obligatoire

### Conteneurs (LXC)
- Mode: **unprivileged** toujours
- Features: **nesting=1** si Docker requis
- cgroup: **v2** uniquement (PVE 9+)
- OCI: Support images Docker Hub (PVE 9.1+)

### Stockage
- **ZFS**: compression lz4, RAID-Z2, special vdev metadata
- **Ceph**: minimum 3 nodes, 10GbE dédié, 3x réplication
- **RAIDZ Expansion**: disponible ZFS 2.3+ (PVE 9+)

### Réseau
- Management: VLAN isolé dédié
- Stockage: 10GbE minimum, MTU 9000
- SDN Fabrics: OpenFabric/OSPF pour auto-config

### Haute Disponibilité
- Minimum: 3 nodes pour quorum
- Fencing: watchdog ou IPMI obligatoire
- QDevice: pour clusters 2 nodes
- Affinity Rules: PVE 9+ pour placement intelligent

### Backup (PBS)
- Règle 3-2-1: 3 copies, 2 supports, 1 offsite
- Déduplication: zstd compression
- Vérification: hebdomadaire automatique
- Test: restauration mensuelle

### Sécurité
- SSH: clés uniquement, pas de root login
- 2FA/TOTP: obligatoire pour admins
- API Tokens: pour toute automation
- Firewall: policy DROP par défaut
- Fail2ban: SSH + Web UI

## Structure des Fichiers

```
proxmox-skill/
├── SKILL.md                 # Ce fichier
├── commands/
│   ├── status.md           # /pve-status
│   ├── cluster.md          # /pve-cluster
│   ├── vm.md               # /pve-vm
│   ├── ct.md               # /pve-ct
│   ├── template.md         # /pve-template
│   ├── storage.md          # /pve-storage
│   ├── zfs.md              # /pve-zfs
│   ├── ceph.md             # /pve-ceph
│   ├── backup.md           # /pve-backup
│   ├── restore.md          # /pve-restore
│   ├── network.md          # /pve-network
│   ├── sdn.md              # /pve-sdn
│   ├── firewall.md         # /pve-firewall
│   ├── ha.md               # /pve-ha
│   ├── security.md         # /pve-security
│   ├── users.md            # /pve-users
│   ├── monitor.md          # /pve-monitor
│   ├── api.md              # /pve-api
│   ├── terraform.md        # /pve-terraform
│   └── diag.md             # /pve-diag
└── wizards/
    ├── setup.md            # Configuration initiale
    ├── vm-create.md        # Création VM
    ├── ct-create.md        # Création CT
    ├── template.md         # Template Cloud-Init
    ├── cluster.md          # Setup cluster
    ├── ceph.md             # Déploiement Ceph
    ├── ha.md               # Configuration HA
    ├── backup.md           # Stratégie backup
    ├── security.md         # Hardening
    ├── sdn.md              # Configuration SDN
    └── migrate.md          # Migration
```

## Références
- Documentation officielle: https://pve.proxmox.com/pve-docs/
- Wiki: https://pve.proxmox.com/wiki/
- Forum: https://forum.proxmox.com/
- API Reference: https://pve.proxmox.com/pve-docs/api-viewer/

## Changelog
- **2.0.0** (2026-02): Restructuration complète, commandes slash séparées, wizards interactifs
- **1.0.0** (2026-02): Version initiale monolithique
