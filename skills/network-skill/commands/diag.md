---
name: net-diag
description: Diagnostic reseau complet (ping, traceroute, DNS, latence)
---

# /net-diag - Diagnostic Reseau Complet

## Cible : $ARGUMENTS

Effectue un diagnostic reseau complet vers une cible (IP, hostname, ou "all" pour tout le homelab).

## Comportement

### Si cible = IP ou hostname

1. **Ping** : tester la connectivite (4 paquets)
2. **Traceroute** : identifier le chemin reseau
3. **DNS** : verifier la resolution (si hostname)
4. **Latence** : mesurer le temps de reponse moyen
5. **Port check** : tester les ports standards (22, 80, 443)

### Si cible = "all" ou absent

Diagnostiquer tout le homelab :

| Cible | IP | Ports a tester |
|-------|-----|----------------|
| Gateway | 192.168.1.1 | - |
| Proxmox | 192.168.1.215 | 22, 8006 |
| VM 100 | 192.168.1.162 | 22, 8091, 3003, 19999 |
| VM 101 | 192.168.1.101 | 22 |
| VM 103 | 192.168.1.163 | 22, 8020, 3020 |
| VM 104 | 192.168.1.164 | 22 |
| VM 105 | 192.168.1.161 | 22, 8020, 3020 |

## Commandes par Plateforme

### Windows (PowerShell)

```powershell
# Ping
Test-Connection -ComputerName $target -Count 4

# Traceroute
Test-NetConnection -ComputerName $target -TraceRoute

# Port check
Test-NetConnection -ComputerName $target -Port $port -InformationLevel Quiet

# DNS
Resolve-DnsName $hostname
```

### Linux (Bash)

```bash
# Ping
ping -c 4 $target

# Traceroute
traceroute $target
# ou mtr pour un affichage continu
mtr -r -c 10 $target

# Port check
nc -zv $target $port 2>&1

# DNS
dig $hostname +short
```

## Format de Sortie

```
# Diagnostic Reseau - [cible]

## Connectivite
| Cible | IP | Ping | Latence | Status |
|-------|-----|------|---------|--------|

## Ports
| Cible | Port | Service | Status |
|-------|------|---------|--------|

## DNS
| Hostname | Resolution | IP | TTL |
|----------|------------|-----|-----|

## Problemes detectes
- [WARN/CRIT] Description du probleme
```

## Exemples

```
/net-diag                              # Diagnostic complet homelab
/net-diag 192.168.1.163                # Diagnostic vers VM 103
/net-diag google.com                   # Diagnostic vers un hote externe
/net-diag all                          # Toutes les VMs + services
```
