---
name: network-skill
description: "Administration reseau : diagnostic, DNS, firewall, ports, routing, VLAN, VPN, proxy, connectivite inter-VM."
prefix: /net-*
---

# Super Agent Network Administration

Agent intelligent pour administrer le reseau homelab : diagnostic, scanning, DNS, firewall, routage, trafic, VPN, cartographie.

## Philosophie

> "Un reseau invisible est un reseau qui fonctionne."

## Compatibilite

| Composant | Support |
|-----------|---------|
| Windows | 11+ (PowerShell, netsh, nmap) |
| Linux | Ubuntu 22.04+, Debian 12+ |
| Proxmox | VE 8+ (bridges, firewall, SDN) |
| Docker | Networks internes (bridge, overlay) |

## Topologie Homelab

```
Internet
  |
[Gateway .1]
  |
LAN 192.168.1.0/24
  |
  +-- PC Windows (.243) ---- SSH ---+
  |                                  |
  +-- Proxmox Host (.215) ---- Bridge vmbr0
                                |
                    +-----------+-----------+-----------+-----------+
                    |           |           |           |           |
               VM 100 (.162)  VM 101 (.101)  VM 103 (.163)  VM 104 (.164)  VM 105 (.161)
               Monitoring    Desktop       Dev principal  Stockage       Lab
               6 containers  (pas Docker)  29 containers  7 containers   3 containers
```

## Inventaire Services Exposes

| Service | VM | IP:Port | Protocole |
|---------|-----|---------|-----------|
| Proxmox Web UI | Host | .215:8006 | HTTPS |
| Beszel Hub | 100 | .162:8091 | HTTP |
| Uptime Kuma | 100 | .162:3003 | HTTP |
| Netdata | 100 | .162:19999 | HTTP |
| Dozzle | 100 | .162:8082 | HTTP |
| ntfy | 100 | .162:8084 | HTTP |
| Beszel Agent | 100 | .162:45876 | TCP |
| Beszel Agent | Host | .215:45876 | TCP |
| Beszel Agent | Win | .243:45876 | TCP |
| Taskyn Core | 103 | .163:8020 | HTTP |
| Taskyn Web | 103 | .163:3020 | HTTP |
| Taskyn Core | 105 | .161:8020 | HTTP |
| Taskyn Web | 105 | .161:3020 | HTTP |

## Commandes Slash

### Diagnostic

| Commande | Description |
|----------|-------------|
| `/net-diag` | Diagnostic reseau complet (ping, traceroute, DNS, latence) |
| `/net-scan` | Scanner le reseau (decouverte hosts, ports ouverts) |
| `/net-ports` | Verifier les ports (ouverts, ecoutant, occupes, tester connectivite) |

### Configuration

| Commande | Description |
|----------|-------------|
| `/net-dns` | Gerer et diagnostiquer DNS (dig, nslookup, /etc/hosts, resolution) |
| `/net-interfaces` | Gerer les interfaces reseau (IP, config, bridges) |
| `/net-firewall` | Regles firewall reseau (ufw, iptables, Windows Firewall) |
| `/net-route` | Tables de routage, passerelles, traceroute |

### Analyse

| Commande | Description |
|----------|-------------|
| `/net-traffic` | Analyse du trafic (bandwidth, connexions actives, tcpdump) |
| `/net-vpn` | Configuration VPN (WireGuard, OpenVPN) |
| `/net-map` | Cartographie du reseau (inventaire IPs, services, topologie) |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/net-wizard setup` | Configuration reseau initiale d'une VM ou serveur |
| `/net-wizard troubleshoot` | Diagnostic guide pas a pas (connectivite, DNS, ports, firewall) |

## Conventions Reseau

### Adressage IP

| Plage | Usage |
|-------|-------|
| 192.168.1.1 | Gateway/routeur |
| 192.168.1.100-199 | VMs Proxmox (statique recommande) |
| 192.168.1.200-254 | Equipements reseau, serveurs physiques |
| 192.168.1.243 | PC Windows r2d2 (fixe) |
| 192.168.1.215 | Proxmox Host (fixe) |
| DHCP | A eviter pour les serveurs (VM 100 a corriger) |

### Ports Standards Homelab

| Plage | Usage |
|-------|-------|
| 22 | SSH |
| 80, 443 | HTTP/HTTPS |
| 3000-3100 | Web UIs (Taskyn, Uptime Kuma) |
| 8000-8100 | APIs et services (Taskyn API, Beszel, Dozzle, ntfy) |
| 19999 | Netdata |
| 45876 | Beszel Agent |

### Regles de Securite

- Politique par defaut : **deny incoming, allow outgoing**
- SSH : uniquement par cle, port 22 (ou non-standard)
- Services internes : accessibles uniquement depuis 192.168.1.0/24
- Docker : attention aux ports publies qui bypassent ufw
- Proxmox firewall : activer au niveau datacenter + VM

### Bonnes Pratiques

- **IPs statiques** pour tous les serveurs (eviter DHCP)
- **DNS local** pour les noms de VMs (fichier hosts ou DNS interne)
- **MTU coherent** sur tout le reseau (1500 standard)
- **Tester avant/apres** chaque changement reseau
- **Documenter** chaque port expose et sa raison
- **Separer** les reseaux par role quand possible (management, donnees, monitoring)

## Integration avec les autres Skills

| Skill | Relation |
|-------|----------|
| **linux-skill** | `/lx-network` pour la config OS, `/net-*` pour le diagnostic reseau |
| **docker-skill** | `/dk-network` pour les reseaux Docker, `/net-*` pour l'inter-VM |
| **proxmox-skill** | `/pve-*` pour les bridges/VLAN Proxmox, `/net-*` pour la connectivite |
| **monitoring-skill** | `/mon-*` pour les metriques, `/net-*` pour le diagnostic |
| **windows-skill** | `/win-*` pour la config Windows, `/net-*` pour le reseau cross-platform |

## Outils par Plateforme

### Windows
- `Test-NetConnection` (ping + port check)
- `Get-NetAdapter`, `Get-NetIPAddress`
- `netsh` (firewall, interfaces)
- `nmap` (si installe via winget)
- `Resolve-DnsName`

### Linux
- `ping`, `traceroute`, `mtr`
- `ss`, `netstat`, `lsof`
- `ip addr`, `ip route`
- `nmap`, `tcpdump`
- `dig`, `nslookup`, `host`
- `ufw`, `iptables`, `nftables`
- `iperf3` (benchmark bandwidth)

### Proxmox
- `pvesh` (API CLI)
- `/etc/network/interfaces` (bridges)
- `pve-firewall` (firewall integre)

## Troubleshooting Rapide

### Pas de connectivite vers une VM
1. Ping la gateway : `ping 192.168.1.1`
2. Ping le host Proxmox : `ping 192.168.1.215`
3. Ping la VM cible : `ping 192.168.1.XXX`
4. Si le ping echoue a l'etape 3 : verifier que la VM est demarree (`/pve-status`)
5. Verifier le bridge vmbr0 sur Proxmox
6. Verifier le firewall de la VM (`ufw status`)

### Port non accessible
1. Verifier que le service ecoute : `ss -tlnp | grep :PORT`
2. Verifier le firewall local : `ufw status` ou `iptables -L`
3. Verifier Docker : les ports publies bypassent ufw
4. Tester depuis le PC : `Test-NetConnection -ComputerName IP -Port PORT`

### DNS ne resout pas
1. Verifier /etc/resolv.conf ou systemd-resolved
2. Tester avec dig : `dig @8.8.8.8 example.com`
3. Verifier le fichier hosts local
4. Flusher le cache DNS si necessaire

## References

- [Linux Networking - Arch Wiki](https://wiki.archlinux.org/title/Network_configuration)
- [Proxmox Network Configuration](https://pve.proxmox.com/wiki/Network_Configuration)
- [WireGuard Documentation](https://www.wireguard.com/quickstart/)
- [nmap Reference Guide](https://nmap.org/book/man.html)
- [UFW Documentation](https://help.ubuntu.com/community/UFW)
