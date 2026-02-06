# Wizard: Software-Defined Networking (SDN)

## Mode d'emploi
Ce wizard configure le SDN de Proxmox VE 9+ pour créer des réseaux virtuels isolés, des VLANs, ou des overlays VXLAN/EVPN.

---

## Questions Interactives

### 1. Type de Zone

**Q1.1: Quel type de zone réseau?**

| Option | Type | Usage |
|--------|------|-------|
| A | Simple | Réseau L2 basique, pont standard |
| B | VLAN | Segmentation par VLAN ID (802.1Q) |
| C | VXLAN | Overlay L2 sur L3 (multi-site) |
| D | EVPN | BGP + VXLAN (routage distribué avancé) |

```
Choix: ___
```

---

### 2. Configuration de Zone

**Q2.1: Nom de la zone?**
```
Zone: _______________ (ex: production, dmz, dev-zone)
```

**Q2.2: Bridge physique associé?**
```
Bridge: _______________ (ex: vmbr0, vmbr1)
```

**Q2.3: Si VLAN - Range de VLANs autorisés?**
```
VLAN range: _____ - _____ (ex: 100-200)
```

**Q2.4: Si VXLAN/EVPN - Peers?**
```
Peer 1: _______________ (IP node 1)
Peer 2: _______________ (IP node 2)
Peer 3: _______________ (IP node 3)
```

---

### 3. VNet (Réseau Virtuel)

**Q3.1: Nom du VNet?**
```
VNet: _______________ (ex: vnet-web, vnet-db, vnet-mgmt)
```

**Q3.2: VLAN tag? (si zone VLAN)**
```
Tag: _____ (ex: 100)
```

---

### 4. Subnet

**Q4.1: Configurer un subnet?**
```
CIDR: _______________ (ex: 10.10.100.0/24)
Gateway: _______________ (ex: 10.10.100.1)
```

**Q4.2: Activer DHCP?**
```
[ ] Oui - Range: _______________ (ex: 10.10.100.100-10.10.100.200)
[ ] Non - IP statiques uniquement
```

**Q4.3: Serveurs DNS?**
```
DNS 1: _______________ (ex: 10.10.10.1)
DNS 2: _______________ (ex: 8.8.8.8)
```

---

## Génération de Commandes

### Créer une Zone

```bash
# Zone Simple
pvesh create /cluster/sdn/zones --zone ZONE_NAME --type simple --bridge vmbr1

# Zone VLAN
pvesh create /cluster/sdn/zones --zone ZONE_NAME --type vlan --bridge vmbr1

# Zone VXLAN
pvesh create /cluster/sdn/zones --zone ZONE_NAME --type vxlan --peers "IP1,IP2,IP3"

# Zone EVPN
pvesh create /cluster/sdn/zones --zone ZONE_NAME --type evpn --controller CTRL_NAME --peers "IP1,IP2,IP3"
```

### Créer un VNet

```bash
pvesh create /cluster/sdn/vnets --vnet VNET_NAME --zone ZONE_NAME --tag VLAN_TAG --alias "Description"
```

### Créer un Subnet

```bash
pvesh create /cluster/sdn/vnets/VNET_NAME/subnets \
  --subnet CIDR \
  --gateway GATEWAY \
  --type subnet \
  --dhcp-range "start-address=START,end-address=END" \
  --dnszoneprefix ZONE_NAME
```

### Appliquer la Config

```bash
# IMPORTANT: toujours appliquer après modifications
pvesh set /cluster/sdn
```

### Vérifier

```bash
pvesh get /cluster/sdn/zones
pvesh get /cluster/sdn/vnets
cat /etc/network/interfaces.d/sdn
```

---

## Configuration Type: Multi-VLAN

```bash
# Zone VLAN
pvesh create /cluster/sdn/zones --zone prod --type vlan --bridge vmbr1

# VNet Web (VLAN 100)
pvesh create /cluster/sdn/vnets --vnet vnet-web --zone prod --tag 100
pvesh create /cluster/sdn/vnets/vnet-web/subnets --subnet 10.10.100.0/24 --gateway 10.10.100.1 --type subnet

# VNet DB (VLAN 200)
pvesh create /cluster/sdn/vnets --vnet vnet-db --zone prod --tag 200
pvesh create /cluster/sdn/vnets/vnet-db/subnets --subnet 10.10.200.0/24 --gateway 10.10.200.1 --type subnet

# Appliquer
pvesh set /cluster/sdn
```

---

## Best Practices 2026

| Règle | Raison |
|-------|--------|
| Planifier l'adressage IP | Éviter les conflits et simplifier le routage |
| VLAN pour single-site | Simple et performant |
| VXLAN/EVPN pour multi-site | Overlay L2 sur L3, scalable |
| Toujours appliquer après changement | Les changements SDN ne sont pas live avant apply |
| Tester avant production | Valider la connectivité dans un VNet de test |
| Documenter les VLANs | Tableau VLAN/Subnet/Usage |

---

## Commande Associée

Voir `/px-sdn` pour les opérations SDN.
