# 🔀 /pve-sdn - Software-Defined Networking

## Description
Gestion SDN Proxmox VE 9+ : Zones, VNets, Subnets, IPAM, et Fabrics.

## Syntaxe
```
/pve-sdn [action] [options]
```

## Architecture SDN

```
┌─────────────────────────────────────────────────────┐
│                     DATACENTER                       │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   ZONE      │  │   ZONE      │  │   ZONE      │  │
│  │   VLAN      │  │   VXLAN     │  │   Simple    │  │
│  │             │  │             │  │             │  │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │  │
│  │ │ VNet 1  │ │  │ │ VNet 3  │ │  │ │ VNet 5  │ │  │
│  │ │ Subnet  │ │  │ │ Subnet  │ │  │ │         │ │  │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │  │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │             │  │
│  │ │ VNet 2  │ │  │ │ VNet 4  │ │  │             │  │
│  │ │ Subnet  │ │  │ │ Subnet  │ │  │             │  │
│  │ └─────────┘ │  │ └─────────┘ │  │             │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Actions Disponibles

### `status` - Vue d'ensemble SDN
```bash
# Status SDN
pvesh get /cluster/sdn

# Zones configurées
pvesh get /cluster/sdn/zones

# VNets configurés
pvesh get /cluster/sdn/vnets

# État application
pvesh get /cluster/sdn/status
```

### `zone create` - Créer une zone

#### Zone Simple (réseau isolé)
```bash
pvesh create /cluster/sdn/zones \
  --zone simple-zone \
  --type simple
```

#### Zone VLAN
```bash
pvesh create /cluster/sdn/zones \
  --zone vlan-zone \
  --type vlan \
  --bridge vmbr0 \
  --nodes "pve1,pve2,pve3"
```

#### Zone VXLAN
```bash
pvesh create /cluster/sdn/zones \
  --zone vxlan-zone \
  --type vxlan \
  --peers "10.0.0.1,10.0.0.2,10.0.0.3" \
  --mtu 1450
```

#### Zone QinQ (VLAN stacking)
```bash
pvesh create /cluster/sdn/zones \
  --zone qinq-zone \
  --type qinq \
  --bridge vmbr0 \
  --tag 100 \
  --vlan-protocol 802.1ad
```

#### Zone EVPN (BGP)
```bash
pvesh create /cluster/sdn/zones \
  --zone evpn-zone \
  --type evpn \
  --controller evpn-ctrl \
  --vrf-vxlan 5000
```

### `vnet create` - Créer un VNet
```bash
# VNet basique
pvesh create /cluster/sdn/vnets \
  --vnet web-net \
  --zone vlan-zone \
  --tag 100 \
  --alias "Web Servers Network"

# VNet VXLAN
pvesh create /cluster/sdn/vnets \
  --vnet db-net \
  --zone vxlan-zone \
  --tag 200 \
  --alias "Database Network"
```

### `subnet create` - Créer un Subnet
```bash
# Subnet avec DHCP
pvesh create /cluster/sdn/vnets/{vnet}/subnets \
  --subnet 10.100.0.0/24 \
  --gateway 10.100.0.1 \
  --snat 1 \
  --dhcp-range "start-address=10.100.0.100,end-address=10.100.0.200"

# Subnet sans DHCP
pvesh create /cluster/sdn/vnets/{vnet}/subnets \
  --subnet 192.168.50.0/24 \
  --gateway 192.168.50.1
```

### `apply` - Appliquer la configuration
```bash
# Appliquer les changements SDN
pvesh put /cluster/sdn

# Vérifier l'état
pvesh get /cluster/sdn/status

# Recharger sur un node spécifique
pvesh put /nodes/{node}/sdn
```

### `ipam` - Gestion IPAM
```bash
# Lister les IPAM
pvesh get /cluster/sdn/ipams

# Créer IPAM interne
pvesh create /cluster/sdn/ipams \
  --ipam pve-ipam \
  --type pve

# Créer IPAM phpIPAM
pvesh create /cluster/sdn/ipams \
  --ipam external-ipam \
  --type phpipam \
  --url "https://ipam.example.com/api" \
  --token "{token}"
```

### `dns` - Configuration DNS SDN
```bash
# Créer zone DNS
pvesh create /cluster/sdn/dns \
  --dns powerdns \
  --type powerdns \
  --url "https://dns.example.com/api" \
  --key "{api_key}"
```

## Fabrics (PVE 9+)

### Créer un Fabric OpenFabric
```bash
# Fabric pour réseau Ceph
pvesh create /cluster/sdn/fabrics \
  --fabric ceph-fabric \
  --type openfabric \
  --bridge vmbr1 \
  --net "10.10.0.0/16"
```

### Créer un Fabric OSPF
```bash
pvesh create /cluster/sdn/fabrics \
  --fabric ospf-fabric \
  --type ospf \
  --bridge vmbr2 \
  --router-id 10.0.0.1 \
  --area 0
```

## Controllers (pour EVPN)

### BGP Controller
```bash
pvesh create /cluster/sdn/controllers \
  --controller bgp-ctrl \
  --type evpn \
  --asn 65000 \
  --peers "10.0.0.254"
```

## Exemples Complets

### Lab Multi-tenant
```bash
# 1. Zone VLAN
pvesh create /cluster/sdn/zones \
  --zone tenants \
  --type vlan \
  --bridge vmbr0

# 2. VNet Tenant A (VLAN 100)
pvesh create /cluster/sdn/vnets \
  --vnet tenant-a \
  --zone tenants \
  --tag 100

pvesh create /cluster/sdn/vnets/tenant-a/subnets \
  --subnet 10.100.0.0/24 \
  --gateway 10.100.0.1 \
  --dhcp-range "start-address=10.100.0.50,end-address=10.100.0.250"

# 3. VNet Tenant B (VLAN 200)
pvesh create /cluster/sdn/vnets \
  --vnet tenant-b \
  --zone tenants \
  --tag 200

pvesh create /cluster/sdn/vnets/tenant-b/subnets \
  --subnet 10.200.0.0/24 \
  --gateway 10.200.0.1 \
  --snat 1

# 4. Appliquer
pvesh put /cluster/sdn
```

### Overlay VXLAN Cluster
```bash
# 1. Zone VXLAN (nécessite IP routable entre nodes)
pvesh create /cluster/sdn/zones \
  --zone overlay \
  --type vxlan \
  --peers "192.168.1.11,192.168.1.12,192.168.1.13" \
  --mtu 1450

# 2. VNet applicatif
pvesh create /cluster/sdn/vnets \
  --vnet app-overlay \
  --zone overlay \
  --tag 10000

pvesh create /cluster/sdn/vnets/app-overlay/subnets \
  --subnet 172.16.0.0/16 \
  --gateway 172.16.0.1

pvesh put /cluster/sdn
```

## Utilisation dans VMs/CTs

### Assigner VNet à une VM
```bash
# Via qm
qm set 100 --net0 virtio,bridge=web-net

# Via API
pvesh set /nodes/{node}/qemu/100/config \
  --net0 "virtio,bridge=web-net"
```

### Assigner VNet à un CT
```bash
pct set 200 --net0 name=eth0,bridge=web-net,ip=dhcp
```

## Diagnostics SDN

### Vérifier état
```bash
# Bridges créés
bridge link show

# VXLAN interfaces
ip -d link show type vxlan

# FDB (forwarding database)
bridge fdb show

# Routes VRF (EVPN)
ip route show vrf {vrf_name}
```

### Logs SDN
```bash
# Logs application SDN
journalctl -u pve-cluster -f | grep sdn

# Logs FRR (EVPN)
vtysh -c "show running-config"
```

## Fichiers Configuration

| Fichier | Description |
|---------|-------------|
| `/etc/pve/sdn/zones.cfg` | Configuration zones |
| `/etc/pve/sdn/vnets.cfg` | Configuration VNets |
| `/etc/pve/sdn/subnets.cfg` | Configuration subnets |
| `/etc/pve/sdn/controllers.cfg` | Controllers BGP |
| `/etc/pve/sdn/.running-config` | Config active |

## Best Practices 2025-2026

1. **Zones VLAN**: Pour environnements simples avec switch compatible
2. **Zones VXLAN**: Pour overlay sans dépendance switch
3. **MTU VXLAN**: Toujours MTU-50 (1450 si base 1500)
4. **Fabrics**: Utiliser OpenFabric pour Ceph en PVE 9+
5. **IPAM**: Activer pour gestion automatique IP
6. **SNAT**: Activer pour accès Internet depuis VNets isolés
