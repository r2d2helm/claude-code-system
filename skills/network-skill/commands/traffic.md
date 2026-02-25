---
name: net-traffic
description: Analyse du trafic (bandwidth, connexions actives, tcpdump)
---

# /net-traffic - Analyse du Trafic Reseau

## Cible : $ARGUMENTS

Analyser le trafic reseau : bande passante, connexions actives, capture de paquets.

## Actions

### Connexions (par defaut)

Afficher les connexions actives, groupees par etat et destination.

### Bandwidth (cible = "bw" ou "bandwidth")

Mesurer la bande passante disponible (iperf3) ou le trafic courant.

### Capture (cible = "capture" + filtre)

Capturer du trafic avec tcpdump.

### Top (cible = "top")

Afficher les connexions les plus actives en temps reel.

## Commandes par Plateforme

### Windows (PowerShell)

```powershell
# Connexions actives
Get-NetTCPConnection -State Established |
    Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort,
    @{N='Process';E={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).ProcessName}} |
    Sort-Object RemoteAddress

# Statistiques par protocole
Get-NetTCPConnection | Group-Object State | Select-Object Count, Name

# Stats interfaces (bytes in/out)
Get-NetAdapterStatistics | Format-Table Name, ReceivedBytes, SentBytes, ReceivedUnicastPackets, SentUnicastPackets

# Bande passante en temps reel (approximation)
$before = Get-NetAdapterStatistics -Name "Ethernet"
Start-Sleep 5
$after = Get-NetAdapterStatistics -Name "Ethernet"
$rxRate = ($after.ReceivedBytes - $before.ReceivedBytes) / 5 / 1MB
$txRate = ($after.SentBytes - $before.SentBytes) / 5 / 1MB
Write-Host "RX: $([math]::Round($rxRate,2)) MB/s | TX: $([math]::Round($txRate,2)) MB/s"
```

### Linux (Bash)

```bash
# Connexions actives
ss -tnp state established

# Connexions par etat
ss -s

# Top connexions
ss -tnp | sort -k4 | head -20

# Trafic en temps reel par interface
iftop -i eth0
# ou
nload eth0

# Bande passante (iperf3)
# Serveur : iperf3 -s
# Client :  iperf3 -c 192.168.1.163

# Statistiques interface
ip -s link show eth0
cat /proc/net/dev

# Capture tcpdump
sudo tcpdump -i eth0 -c 100
sudo tcpdump -i eth0 port 22
sudo tcpdump -i eth0 host 192.168.1.243
sudo tcpdump -i eth0 -w /tmp/capture.pcap   # Sauvegarder

# Connexions par IP (top talkers)
ss -tnp state established | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head

# Docker trafic (bridge)
sudo tcpdump -i docker0 -c 50
```

## Benchmark Bandwidth Inter-VM

Pour mesurer la bande passante entre deux VMs :

```bash
# Sur VM cible (serveur)
iperf3 -s -p 5201

# Sur VM source (client)
iperf3 -c 192.168.1.163 -p 5201 -t 10

# Bidirectionnel
iperf3 -c 192.168.1.163 -p 5201 --bidir
```

Installer iperf3 si absent : `sudo apt install iperf3`

## Format de Sortie

```
# Trafic Reseau - [machine]

## Statistiques Interface
| Interface | RX (bytes) | TX (bytes) | RX (pkt) | TX (pkt) | Errors |
|-----------|-----------|-----------|---------|---------|--------|

## Connexions Actives : N
| Local | Remote | Port | Process | State |
|-------|--------|------|---------|-------|

## Repartition par Etat
| Etat | Nombre |
|------|--------|

## Top Destinations
| IP | Connexions | Bytes |
|----|-----------|-------|
```

## Exemples

```
/net-traffic                           # Connexions actives
/net-traffic bw                        # Mesure bande passante
/net-traffic capture port 8091         # Capturer trafic Beszel
/net-traffic top                       # Top connexions
/net-traffic iperf 192.168.1.163       # Benchmark vers VM 103
```
