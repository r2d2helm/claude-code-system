---
name: net-route
description: Tables de routage, passerelles, traceroute
---

# /net-route - Routage Reseau

## Cible : $ARGUMENTS

Afficher et gerer les tables de routage, passerelles et tracer le chemin reseau.

## Actions

### Table (par defaut)

Afficher la table de routage complete.

### Trace (cible = IP/hostname)

Tracer le chemin reseau vers une destination.

### Add/Delete (action + route)

Ajouter ou supprimer une route statique.

## Commandes par Plateforme

### Windows (PowerShell)

```powershell
# Table de routage
Get-NetRoute -AddressFamily IPv4 | Format-Table DestinationPrefix, NextHop, RouteMetric, InterfaceAlias

# Gateway par defaut
Get-NetRoute -DestinationPrefix 0.0.0.0/0

# Traceroute
Test-NetConnection -ComputerName $target -TraceRoute
tracert $target

# Ajouter une route statique
New-NetRoute -DestinationPrefix "10.0.0.0/24" -NextHop "192.168.1.1" -InterfaceAlias "Ethernet"

# Supprimer une route
Remove-NetRoute -DestinationPrefix "10.0.0.0/24"

# Route persistante (survive au reboot)
route add 10.0.0.0 mask 255.255.255.0 192.168.1.1 -p
```

### Linux (Bash)

```bash
# Table de routage
ip route show
# ou
route -n

# Gateway par defaut
ip route show default

# Traceroute
traceroute $target
# ou mtr (plus lisible)
mtr -r -c 10 $target

# Ajouter une route
sudo ip route add 10.0.0.0/24 via 192.168.1.1 dev eth0

# Supprimer une route
sudo ip route del 10.0.0.0/24

# Route persistante (Netplan - Ubuntu)
# Dans /etc/netplan/*.yaml :
#   routes:
#     - to: 10.0.0.0/24
#       via: 192.168.1.1

# Verifier par quelle route passe un paquet
ip route get 192.168.1.163
```

### Proxmox

```bash
# Table de routage du host
ip route show

# Verifier le forwarding IP
cat /proc/sys/net/ipv4/ip_forward
# Doit etre 1 pour que les VMs communiquent

# Activer le forwarding (temporaire)
echo 1 > /proc/sys/net/ipv4/ip_forward

# Activer le forwarding (persistant)
# Dans /etc/sysctl.conf :
# net.ipv4.ip_forward = 1
```

## Routes Homelab

```
Destination         Gateway         Interface
0.0.0.0/0           192.168.1.1     eth0/vmbr0    (Internet)
192.168.1.0/24      lien direct     eth0/vmbr0    (LAN)
172.17.0.0/16       -               docker0       (Docker bridge)
```

## Format de Sortie

```
# Routage - [machine]

## Table de Routage
| Destination | Gateway | Interface | Metrique | Type |
|-------------|---------|-----------|----------|------|

## Gateway par defaut
Gateway: X.X.X.X via InterfaceName

## Traceroute vers [cible]
| Hop | IP | Hostname | Latence |
|-----|-----|----------|---------|
```

## Exemples

```
/net-route                             # Table de routage locale
/net-route trace 192.168.1.163         # Tracer vers VM 103
/net-route trace google.com            # Tracer vers Internet
/net-route add 10.0.0.0/24 via 192.168.1.1   # Ajouter une route
```
