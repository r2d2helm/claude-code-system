# /pve-vm - Gestion Machines Virtuelles KVM

## Description
Gestion complète des machines virtuelles KVM/QEMU sur Proxmox VE.
Inclut création, configuration, snapshots, migration et clonage.

## Syntaxe
```
/pve-vm <action> [vmid] [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `list` | `/pve-vm list [node]` | Lister toutes les VMs |
| `info` | `/pve-vm info <vmid>` | Détails VM spécifique |
| `create` | `/pve-vm create [--wizard]` | Créer nouvelle VM |
| `start` | `/pve-vm start <vmid>` | Démarrer VM |
| `stop` | `/pve-vm stop <vmid>` | Arrêter VM (force) |
| `shutdown` | `/pve-vm shutdown <vmid>` | Arrêt gracieux ACPI |
| `reboot` | `/pve-vm reboot <vmid>` | Redémarrer VM |
| `reset` | `/pve-vm reset <vmid>` | Reset hard |
| `suspend` | `/pve-vm suspend <vmid>` | Suspendre (RAM to disk) |
| `resume` | `/pve-vm resume <vmid>` | Reprendre VM suspendue |
| `snapshot` | `/pve-vm snapshot <vmid>` | Créer snapshot |
| `rollback` | `/pve-vm rollback <vmid> <snap>` | Restaurer snapshot |
| `clone` | `/pve-vm clone <vmid>` | Cloner VM |
| `migrate` | `/pve-vm migrate <vmid> <node>` | Migrer vers autre node |
| `template` | `/pve-vm template <vmid>` | Convertir en template |
| `delete` | `/pve-vm delete <vmid>` | Supprimer VM |
| `config` | `/pve-vm config <vmid>` | Modifier configuration |
| `console` | `/pve-vm console <vmid>` | Accès console |
| `monitor` | `/pve-vm monitor <vmid>` | QEMU monitor |

## Options Communes

| Option | Description |
|--------|-------------|
| `--node <n>` | Spécifier le node |
| `--wizard` | Mode assistant interactif |
| `--force` | Forcer l'action |
| `--timeout <s>` | Timeout en secondes |
| `--json` | Sortie JSON |

## Affichage Liste VMs

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║  📋 VIRTUAL MACHINES                                                             ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  ┌──────┬─────────────────────┬────────┬─────────┬────────┬──────────┬────────┐ ║
║  │ VMID │ Name                │ Node   │ Status  │ CPU    │ Memory   │ Disk   │ ║
║  ├──────┼─────────────────────┼────────┼─────────┼────────┼──────────┼────────┤ ║
║  │ 100  │ dc01-windows        │ pve01  │ 🟢 run  │ 4c/12% │ 8G/65%   │ 100G   │ ║
║  │ 101  │ dc02-windows        │ pve02  │ 🟢 run  │ 4c/8%  │ 8G/52%   │ 100G   │ ║
║  │ 102  │ web-nginx-01        │ pve01  │ 🟢 run  │ 2c/15% │ 4G/45%   │ 50G    │ ║
║  │ 103  │ web-nginx-02        │ pve02  │ 🟢 run  │ 2c/18% │ 4G/48%   │ 50G    │ ║
║  │ 104  │ db-postgres-master  │ pve03  │ 🟢 run  │ 8c/35% │ 32G/72%  │ 500G   │ ║
║  │ 105  │ db-postgres-replica │ pve01  │ 🟢 run  │ 8c/22% │ 32G/58%  │ 500G   │ ║
║  │ 120  │ dev-ubuntu          │ pve01  │ 🟡 stop │ 2c/-   │ 8G/-     │ 80G    │ ║
║  │ 200  │ template-ubuntu2404 │ pve01  │ 📦 tpl  │ 2c/-   │ 4G/-     │ 32G    │ ║
║  └──────┴─────────────────────┴────────┴─────────┴────────┴──────────┴────────┘ ║
║                                                                                  ║
║  📊 Total: 8 | Running: 6 | Stopped: 1 | Templates: 1                           ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

## Commandes Bash

### Lister et Informations

```bash
# Lister toutes les VMs
qm list

# Lister avec JSON détaillé
pvesh get /cluster/resources --type vm --output-format=json | jq '.[] | select(.type=="qemu")'

# Configuration complète d'une VM
qm config 100

# Status VM
qm status 100 --verbose

# Pending changes
qm pending 100
```

### Création VM - Best Practices 2025-2026

```bash
# ═══════════════════════════════════════════════════════════════════════════
# CRÉATION VM LINUX OPTIMISÉE
# ═══════════════════════════════════════════════════════════════════════════

qm create 100 \
  --name "web-server-01" \
  --node pve01 \
  --ostype l26 \
  --machine q35 \
  --bios ovmf \
  --efidisk0 local-zfs:1,efitype=4m,pre-enrolled-keys=1 \
  --cpu host \
  --cores 4 \
  --sockets 1 \
  --numa 1 \
  --memory 8192 \
  --balloon 4096 \
  --scsihw virtio-scsi-single \
  --scsi0 local-zfs:50,discard=on,iothread=1,ssd=1 \
  --ide2 local:iso/ubuntu-24.04-live-server-amd64.iso,media=cdrom \
  --net0 virtio,bridge=vmbr0,firewall=1 \
  --agent enabled=1 \
  --onboot 1 \
  --start 0

# ═══════════════════════════════════════════════════════════════════════════
# CRÉATION VM WINDOWS SERVER 2025
# ═══════════════════════════════════════════════════════════════════════════

qm create 300 \
  --name "ws2025-server" \
  --ostype win11 \
  --machine q35 \
  --bios ovmf \
  --efidisk0 local-zfs:1,efitype=4m,pre-enrolled-keys=1 \
  --tpmstate0 local-zfs:1,version=v2.0 \
  --cpu host \
  --cores 4 \
  --sockets 1 \
  --memory 8192 \
  --balloon 0 \
  --scsihw virtio-scsi-single \
  --scsi0 local-zfs:100,discard=on,iothread=1,cache=writeback,ssd=1 \
  --ide0 local:iso/windows_server_2025.iso,media=cdrom \
  --ide1 local:iso/virtio-win.iso,media=cdrom \
  --net0 virtio,bridge=vmbr0,firewall=1 \
  --agent enabled=1,fstrim_cloned_disks=1 \
  --tablet 1

# ══ NOTES WINDOWS ══
# - ostype: win11 pour Windows 2025 (même génération)
# - TPM 2.0: requis pour Windows 2025
# - balloon: désactivé (instabilité Windows)
# - cache: writeback pour performance
# - VirtIO drivers: installer depuis CD virtio-win.iso
# - QEMU Guest Agent: virtio-win-gt-x64.msi

# ═══════════════════════════════════════════════════════════════════════════
# BEST PRACTICES VM 2025-2026
# ═══════════════════════════════════════════════════════════════════════════
#
# Machine: q35 (moderne, PCIe natif, hot-plug)
# BIOS: OVMF/UEFI avec Secure Boot pre-enrolled
# CPU: host pour performance maximale (ou x86-64-v3 pour compatibilité)
# NUMA: activer si CPU multi-socket
# Disque: VirtIO SCSI Single + iothread=1 + discard=on + ssd=1
# Réseau: VirtIO avec firewall=1
# Agent: QEMU Guest Agent toujours activé
# Ballooning: Linux OK, Windows désactivé
```

### Opérations VM

```bash
# Démarrer VM
qm start 100

# Arrêt gracieux (ACPI shutdown)
qm shutdown 100

# Arrêt forcé après timeout
qm stop 100 --timeout 60

# Redémarrer
qm reboot 100

# Reset hard (comme bouton power)
qm reset 100

# Suspendre (RAM to disk)
qm suspend 100 --todisk

# Reprendre
qm resume 100

# Débloquer VM verrouillée
qm unlock 100
```

### Snapshots

```bash
# Créer snapshot avec RAM (VM running)
qm snapshot 100 pre-upgrade --vmstate 1 --description "Before system upgrade"

# Créer snapshot sans RAM (plus rapide)
qm snapshot 100 backup-daily --description "Daily backup $(date +%Y%m%d)"

# Lister snapshots
qm listsnapshot 100

# Rollback à un snapshot
qm rollback 100 pre-upgrade

# Supprimer snapshot
qm delsnapshot 100 pre-upgrade

# Supprimer snapshot et ses enfants
qm delsnapshot 100 old-snap --force
```

### Migration

```bash
# Migration live (VM en cours)
qm migrate 100 pve02 --online

# Migration avec stockage local
qm migrate 100 pve02 --online --with-local-disks --targetstorage local-zfs

# Migration offline
qm migrate 100 pve02

# Migration avec bande passante limitée
qm migrate 100 pve02 --online --migration_network 10.0.1.0/24
```

### Clonage

```bash
# Clone complet (indépendant)
qm clone 100 101 --name "web-server-02" --full

# Clone lié (dépend du parent, économise espace)
qm clone 100 101 --name "web-server-02"

# Clone vers autre stockage
qm clone 100 101 --name "web-server-02" --full --storage ceph-pool

# Clone template Cloud-Init
qm clone 9000 100 --name "new-server" --full
qm set 100 --ipconfig0 ip=10.0.0.50/24,gw=10.0.0.1
qm set 100 --ciuser admin --sshkeys ~/.ssh/authorized_keys
```

### Configuration

```bash
# Ajouter CPU/RAM (hot-plug si supporté)
qm set 100 --cores 8 --memory 16384

# Ajouter disque
qm set 100 --scsi1 local-zfs:100,discard=on,iothread=1

# Redimensionner disque (augmenter uniquement)
qm resize 100 scsi0 +50G

# Ajouter interface réseau
qm set 100 --net1 virtio,bridge=vmbr1,tag=100

# Activer nested virtualization
qm set 100 --cpu host,flags=+vmx

# PCI Passthrough GPU
qm set 100 --hostpci0 0000:01:00,pcie=1,x-vga=1

# USB passthrough
qm set 100 --usb0 host=1234:5678
```

### Suppression

```bash
# Supprimer VM (doit être arrêtée)
qm destroy 100

# Supprimer VM + purger disques orphelins
qm destroy 100 --purge --destroy-unreferenced-disks
```

## Voir Aussi
- `/pve-template` - Gestion templates Cloud-Init
- `/pve-snapshot` - Gestion avancée des snapshots
- `/pve-migrate` - Migration avancée
- `/pve-wizard vm` - Assistant création VM complet

> Voir aussi : [[vm-advanced]]
