# 🌐 /pve-network - Gestion Réseau Proxmox

## Description
Configuration réseau bridges, VLANs, et interfaces Proxmox VE 9+.

## Syntaxe
```
/pve-network [action] [options]
```

## Actions Disponibles

### `list` - Lister les interfaces
```bash
# Toutes les interfaces
pvesh get /nodes/{node}/network --output-format json-pretty

# Interfaces actives
ip -br addr show

# Bridges
brctl show

# VLANs
cat /proc/net/vlan/config
```

### `show` - Détails interface
```bash
# Configuration interface
pvesh get /nodes/{node}/network/{iface}

# Stats interface
ip -s link show {iface}

# Connexions actives
ss -tulpn | grep {iface}
```

### `create-bridge` - Créer un bridge
```bash
# Bridge simple (vmbr1)
pvesh create /nodes/{node}/network \
  --iface vmbr1 \
  --type bridge \
  --bridge_ports eth1 \
  --cidr 10.0.1.1/24 \
  --autostart 1

# Bridge VLAN aware (recommandé PVE 9+)
pvesh create /nodes/{node}/network \
  --iface vmbr0 \
  --type bridge \
  --bridge_ports eth0 \
  --bridge_vlan_aware 1 \
  --cidr 192.168.1.10/24 \
  --gateway 192.168.1.1 \
  --autostart 1
```

### `create-bond` - Créer un bond
```bash
# Bond LACP (802.3ad)
pvesh create /nodes/{node}/network \
  --iface bond0 \
  --type bond \
  --slaves "eth0 eth1" \
  --bond_mode 802.3ad \
  --bond_xmit_hash_policy layer3+4 \
  --bond_miimon 100

# Bridge sur bond
pvesh create /nodes/{node}/network \
  --iface vmbr0 \
  --type bridge \
  --bridge_ports bond0 \
  --bridge_vlan_aware 1
```

### `create-vlan` - Créer interface VLAN
```bash
# VLAN tagged interface
pvesh create /nodes/{node}/network \
  --iface eth0.100 \
  --type vlan \
  --vlan-raw-device eth0

# Bridge pour ce VLAN
pvesh create /nodes/{node}/network \
  --iface vmbr100 \
  --type bridge \
  --bridge_ports eth0.100 \
  --cidr 10.100.0.1/24
```

### `apply` - Appliquer la configuration
```bash
# Appliquer les changements (sans reboot)
ifreload -a

# Vérifier la syntaxe d'abord
ifquery -a --syntax-check

# Via API
pvesh put /nodes/{node}/network
```

### `edit` - Modifier une interface
```bash
# Modifier l'IP
pvesh set /nodes/{node}/network/{iface} \
  --cidr 192.168.1.20/24

# Changer le gateway
pvesh set /nodes/{node}/network/{iface} \
  --gateway 192.168.1.1

# Activer VLAN aware
pvesh set /nodes/{node}/network/vmbr0 \
  --bridge_vlan_aware 1
```

### `delete` - Supprimer une interface
```bash
# Supprimer interface
pvesh delete /nodes/{node}/network/{iface}

# Puis appliquer
ifreload -a
```

### `mtu` - Configurer MTU
```bash
# MTU Jumbo Frames (stockage)
pvesh set /nodes/{node}/network/{iface} --mtu 9000

# Vérifier MTU actuel
ip link show {iface} | grep mtu
```

## Configuration Manuelle

### Fichier /etc/network/interfaces
```bash
# Configuration typique Proxmox 9
auto lo
iface lo inet loopback

# Interface physique
auto eth0
iface eth0 inet manual

# Bridge principal avec VLAN aware
auto vmbr0
iface vmbr0 inet static
    address 192.168.1.10/24
    gateway 192.168.1.1
    bridge-ports eth0
    bridge-stp off
    bridge-fd 0
    bridge-vlan-aware yes
    bridge-vids 2-4094

# Bridge stockage (10GbE)
auto vmbr1
iface vmbr1 inet static
    address 10.10.10.10/24
    bridge-ports eth1
    bridge-stp off
    bridge-fd 0
    mtu 9000
```

### Bond LACP Exemple
```bash
auto bond0
iface bond0 inet manual
    bond-slaves eth2 eth3
    bond-miimon 100
    bond-mode 802.3ad
    bond-xmit-hash-policy layer3+4

auto vmbr2
iface vmbr2 inet static
    address 10.20.20.10/24
    bridge-ports bond0
    bridge-stp off
    bridge-fd 0
```

## Topologies Recommandées

### Single Node Lab
```
┌─────────────────────────────────┐
│ eth0 ─── vmbr0 (Management+VMs) │
│          192.168.1.0/24         │
└─────────────────────────────────┘
```

### Production 3-Node
```
┌──────────────────────────────────────────┐
│ eth0 ─── vmbr0 (Management) VLAN 10      │
│ eth1 ─── vmbr1 (VMs) VLAN-aware          │
│ eth2+eth3 ─ bond0 ─ vmbr2 (Storage) 10G  │
│ eth4 ─── vmbr3 (Corosync) VLAN 99        │
└──────────────────────────────────────────┘
```

## Diagnostics

### Troubleshooting
```bash
# État des interfaces
ip addr show

# Routes
ip route show

# Tester connectivité
ping -c 3 {gateway}

# Voir erreurs
dmesg | grep -i eth

# Bridge info
bridge link show

# VLAN info
bridge vlan show
```

### Performance
```bash
# Bande passante
iperf3 -s  # Serveur
iperf3 -c {server} -t 30  # Client

# Stats détaillées
ethtool -S eth0

# Offload features
ethtool -k eth0
```

## Options Commandes

| Option | Description |
|--------|-------------|
| `--node {node}` | Spécifier le node |
| `--iface {iface}` | Interface cible |
| `--cidr {ip/mask}` | Adresse CIDR |
| `--gateway {ip}` | Passerelle |
| `--mtu {size}` | Taille MTU |
| `--bridge_vlan_aware` | Activer VLAN aware |

## Fichiers Importants
- `/etc/network/interfaces` - Configuration réseau
- `/etc/network/interfaces.d/` - Configs additionnelles
- `/var/log/syslog` - Logs réseau

## Best Practices 2025-2026

1. **VLAN-aware bridges**: Toujours pour production
2. **Séparation réseaux**: Management, VMs, Storage, Corosync
3. **MTU 9000**: Stockage et migration
4. **Bond LACP**: Redondance liens critiques
5. **IPv6**: Désactiver si non utilisé
