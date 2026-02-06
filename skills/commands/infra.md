# Commande: /infra

Commande universelle pour interagir avec tous les agents via une interface unifiée.

## Syntaxe

```
/infra [agent] <action> [options]
```

## Détection Automatique

Sans spécifier l'agent, `/infra` détecte automatiquement le contexte :

```
/infra status           → Détecte l'agent et affiche le status
/infra diagnostic       → Diagnostic selon contexte
/infra wizard           → Lance le wizard approprié
```

## Avec Agent Explicite

```
/infra proxmox status        → Force Proxmox
/infra windows diagnostic    → Force Windows
/infra docker ps             → Force Docker
```

## Actions Universelles

Ces actions fonctionnent sur tous les agents :

### /infra status

```
/infra status
```

**Auto-détection → Proxmox:**
```
╔══════════════════════════════════════════════════════════════╗
║  🟠 PROXMOX │ /infra status                                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  CLUSTER: homelab (3 nœuds)                                  ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ pve1   │ ✅ Online │ CPU: 23% │ RAM: 45% │ 12 VMs      │ ║
║  │ pve2   │ ✅ Online │ CPU: 18% │ RAM: 52% │ 8 VMs       │ ║
║  │ pve3   │ ✅ Online │ CPU: 31% │ RAM: 38% │ 10 VMs      │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Storage: 2.4 TB / 4 TB (60%)                                ║
║  VMs: 30 running │ CTs: 15 running                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Auto-détection → Windows:**
```
╔══════════════════════════════════════════════════════════════╗
║  🔵 WINDOWS │ /infra status                                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  SYSTEM: WORKSTATION-01                                      ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ OS      : Windows 11 Pro 23H2                           │ ║
║  │ Uptime  : 5 days, 3 hours                               │ ║
║  │ CPU     : 12% (Intel i7-12700K)                         │ ║
║  │ RAM     : 18.5 / 32 GB (58%)                            │ ║
║  │ Disk C: : 180 / 256 GB (70%)                            │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Services: 142 running │ Updates: 2 pending                  ║
║  Security: Defender ✅ │ Firewall ✅                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /infra diagnostic

```
/infra diagnostic [quick|full]
```

Lance un diagnostic adapté au contexte détecté.

### /infra wizard

```
/infra wizard [type]
```

Liste ou lance les wizards disponibles pour le contexte.

**Sans argument:**
```
╔══════════════════════════════════════════════════════════════╗
║  🎯 WIZARDS DISPONIBLES                                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Contexte actuel: 🟠 PROXMOX                                 ║
║                                                              ║
║  [1] vm        - Création VM guidée (6 étapes)               ║
║  [2] ct        - Création conteneur LXC (5 étapes)           ║
║  [3] cluster   - Configuration cluster (7 étapes)            ║
║  [4] backup    - Stratégie sauvegarde (4 étapes)             ║
║  [5] network   - Configuration réseau (6 étapes)             ║
║                                                              ║
║  Autres agents:                                              ║
║  • /infra windows wizard - 10 wizards disponibles            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /infra backup

```
/infra backup [create|list|restore]
```

Gestion des sauvegardes selon le contexte.

### /infra security

```
/infra security [audit|harden]
```

Audit et hardening sécurité selon le contexte.

### /infra network

```
/infra network [status|config]
```

Gestion réseau selon le contexte.

## Tableau de Correspondance

| /infra | Proxmox | Windows | Docker | Linux |
|--------|---------|---------|--------|-------|
| status | /pve-status | /win-diagnostic | docker ps | systemctl status |
| diagnostic | /pve-diag | /win-diagnostic full | docker system df | journalctl |
| wizard | /pve-wizard | /win-wizard | - | - |
| backup | /pve-backup | /win-backup | docker save | tar/rsync |
| security | /pve-security | /win-security | docker scan | lynis |
| network | /pve-network | /win-network | docker network | ip/nmcli |
| update | /pve-update | /win-update | docker pull | apt update |
| logs | /pve-logs | /win-logs | docker logs | journalctl |

## Exemples Complets

### Status Multi-Agent

```
/infra all status
```

```
╔══════════════════════════════════════════════════════════════╗
║                   📊 STATUS GLOBAL                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🟠 PROXMOX CLUSTER                                          ║
║  ├── Nœuds: 3/3 online                                       ║
║  ├── VMs: 30 running, 5 stopped                              ║
║  ├── Storage: 60% utilisé                                    ║
║  └── Status: ✅ Healthy                                      ║
║                                                              ║
║  🔵 WINDOWS SERVERS (via WinRM)                              ║
║  ├── DC01: ✅ Online (AD DS, DNS)                            ║
║  ├── WEB01: ✅ Online (IIS)                                  ║
║  └── Status: ✅ Healthy                                      ║
║                                                              ║
║  🐳 DOCKER HOSTS                                             ║
║  ├── docker01: 45 containers                                 ║
║  └── Status: ✅ Healthy                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Comparaison Cross-Platform

```
/infra compare backup proxmox windows
```

```
╔══════════════════════════════════════════════════════════════╗
║              📊 COMPARAISON: BACKUP                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Feature          │ 🟠 Proxmox    │ 🔵 Windows              ║
║  ─────────────────┼───────────────┼────────────────────────  ║
║  Outil natif      │ vzdump        │ wbadmin                  ║
║  Incrémental      │ ✅ Oui        │ ✅ Oui                   ║
║  Compression      │ zstd, gzip    │ Non                      ║
║  Chiffrement      │ ✅ AES        │ ✅ BitLocker             ║
║  Déduplication    │ Via PBS       │ Via DPM                  ║
║  Cloud target     │ S3, NFS       │ Azure Backup             ║
║  Snapshot         │ ✅ Live       │ ✅ VSS                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
