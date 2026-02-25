---
name: net-interfaces
description: Gerer les interfaces reseau (IP, config, bridges)
---

# /net-interfaces - Gestion des Interfaces Reseau

## Cible : $ARGUMENTS

Afficher et configurer les interfaces reseau, adresses IP, bridges.

## Actions

### Liste (par defaut)

Afficher toutes les interfaces avec leur configuration IP.

### Detail (cible = nom d'interface)

Configuration detaillee d'une interface specifique.

### Config (cible = "config")

Afficher les fichiers de configuration reseau.

## Commandes par Plateforme

### Windows (PowerShell)

```powershell
# Lister les adaptateurs
Get-NetAdapter | Format-Table Name, Status, LinkSpeed, MacAddress

# Adresses IP
Get-NetIPAddress -AddressFamily IPv4 | Format-Table InterfaceAlias, IPAddress, PrefixLength

# Configuration complete d'un adaptateur
Get-NetAdapter -Name "Ethernet" | Get-NetIPConfiguration

# Gateway
Get-NetRoute -DestinationPrefix 0.0.0.0/0

# DNS
Get-DnsClientServerAddress -AddressFamily IPv4

# Activer/Desactiver
Enable-NetAdapter -Name "Ethernet"
Disable-NetAdapter -Name "Ethernet"

# Configurer IP statique
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 192.168.1.243 -PrefixLength 24 -DefaultGateway 192.168.1.1
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 8.8.8.8,8.8.4.4

# Revenir en DHCP
Set-NetIPInterface -InterfaceAlias "Ethernet" -Dhcp Enabled
```

### Linux (Bash)

```bash
# Lister les interfaces
ip addr show
ip link show

# Interface specifique
ip addr show eth0

# Configuration Netplan (Ubuntu)
cat /etc/netplan/*.yaml

# Configuration interfaces (Debian)
cat /etc/network/interfaces

# Activer/Desactiver
ip link set eth0 up
ip link set eth0 down

# Configurer IP statique (temporaire)
ip addr add 192.168.1.163/24 dev eth0

# Appliquer Netplan
sudo netplan apply
```

### Proxmox

```bash
# Configuration bridges
cat /etc/network/interfaces

# Exemple bridge vmbr0
# auto vmbr0
# iface vmbr0 inet static
#   address 192.168.1.215/24
#   gateway 192.168.1.1
#   bridge-ports eno1
#   bridge-stp off
#   bridge-fd 0

# Lister les bridges
brctl show

# Appliquer les changements
ifreload -a
```

## Bridges Proxmox Homelab

| Bridge | Interface | IP | VMs Connectees |
|--------|-----------|-----|----------------|
| vmbr0 | eno1 | 192.168.1.215/24 | 100, 101, 103, 104, 105 |

## Format de Sortie

```
# Interfaces Reseau - [machine]

## Adaptateurs
| Interface | Status | IP | Masque | MAC | Vitesse |
|-----------|--------|-----|--------|-----|---------|

## Gateway
| Destination | Gateway | Interface | Metrique |
|-------------|---------|-----------|----------|

## DNS
| Interface | DNS Primaire | DNS Secondaire |
|-----------|-------------|----------------|
```

## Exemples

```
/net-interfaces                        # Lister toutes les interfaces
/net-interfaces eth0                   # Detail d'une interface
/net-interfaces config                 # Fichiers de configuration
/net-interfaces bridges                # Bridges Proxmox
```
