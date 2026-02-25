---
name: net-map
description: Cartographie du reseau (inventaire IPs, services, topologie)
---

# /net-map - Cartographie Reseau

## Cible : $ARGUMENTS

Generer une cartographie complete du reseau : inventaire des hotes, services, topologie.

## Actions

### Carte (par defaut)

Afficher la carte complete du homelab avec tous les hotes et services.

### Discover

Scanner le reseau et construire une carte automatiquement.

### Services

Lister tous les services exposes par hote.

### Export

Exporter la carte au format Markdown (pour le vault Obsidian).

## Carte Homelab de Reference

### Hotes

| Hote | IP | OS | Role | SSH User | Containers |
|------|-----|-----|------|----------|------------|
| Gateway | 192.168.1.1 | Router | Passerelle Internet | - | - |
| Proxmox | 192.168.1.215 | Proxmox VE | Hyperviseur | root | - |
| VM 100 r2d2-stage | 192.168.1.162 | Ubuntu 24.04 | Monitoring primaire | root | 6 |
| VM 101 r2d2-monitor | 192.168.1.101 | Linux Mint | Desktop | mint | 0 |
| VM 103 r2d2-main | 192.168.1.163 | Ubuntu 24.04 | Dev principal | root | 29 |
| VM 104 r2d2-store | 192.168.1.164 | Ubuntu 24.04 | Stockage & BDD | r2d2helm | 7 |
| VM 105 r2d2-lab | 192.168.1.161 | Ubuntu 24.04 | Lab & RAG | r2d2helm | 3 |
| PC Windows | 192.168.1.243 | Windows 11 | Poste de travail | - | - |

### Services par Hote

```
Proxmox (.215)
  :8006/tcp  - Proxmox Web UI (HTTPS)
  :22/tcp    - SSH
  :45876/tcp - Beszel Agent

VM 100 (.162) - Monitoring
  :22/tcp    - SSH
  :8091/tcp  - Beszel Hub
  :3003/tcp  - Uptime Kuma
  :19999/tcp - Netdata
  :8082/tcp  - Dozzle
  :8084/tcp  - ntfy
  :45876/tcp - Beszel Agent

VM 101 (.101) - Desktop
  :22/tcp    - SSH

VM 103 (.163) - Dev
  :22/tcp    - SSH
  :8020/tcp  - Taskyn Core
  :3020/tcp  - Taskyn Web
  (+ services internes : Supabase, LiteLLM, Langfuse, Redis, NetBox)

VM 104 (.164) - Store
  :22/tcp    - SSH
  (+ PostgreSQL, NFS internes)

VM 105 (.161) - Lab
  :22/tcp    - SSH
  :8020/tcp  - Taskyn Core
  :3020/tcp  - Taskyn Web
  (+ rag-indexer interne)

PC Windows (.243)
  :45876/tcp - Beszel Agent
```

## Commandes de Decouverte

```bash
# Scan reseau complet avec services
nmap -sV -p 22,80,443,3003,3020,8006,8020,8082,8084,8091,19999,45876 192.168.1.0/24

# Decouverte ARP (rapide, LAN uniquement)
arp -a                          # Windows/Linux
ip neigh show                   # Linux

# Decouverte mDNS/Avahi
avahi-browse -at                # Linux
```

## Topologie Visuelle

```
                    [Internet]
                        |
                   [Gateway .1]
                        |
              +---------+---------+
              |    LAN 192.168.1.0/24    |
              +---------+---------+
                        |
    +-------------------+-------------------+
    |                                       |
[PC Windows .243]                  [Proxmox .215]
  Beszel Agent                       Web UI :8006
                                     Beszel Agent
                                        |
                                   [Bridge vmbr0]
                                        |
          +--------+--------+--------+--------+
          |        |        |        |        |
       [VM100]  [VM101]  [VM103]  [VM104]  [VM105]
       .162     .101     .163     .164     .161
       Monitor  Desktop  Dev      Store    Lab
       6 cont.  0 cont.  29 cont. 7 cont.  3 cont.
```

## Docker Networks (par VM)

Chaque VM avec Docker a ses propres reseaux internes :

```bash
# Lister les reseaux Docker
ssh root@192.168.1.163 "docker network ls"

# Inspecter un reseau
ssh root@192.168.1.163 "docker network inspect bridge"
```

Les reseaux Docker (172.x.x.x) sont isoles par VM et ne sont pas routables entre VMs.

## Format de Sortie

```
# Carte Reseau Homelab

## Hotes Actifs : X
[Tableau des hotes]

## Services Exposes : Y
[Tableau des services]

## Topologie
[Schema ASCII]

## Hotes Inconnus
[Tout hote detecte non reference]
```

## Exemples

```
/net-map                               # Carte complete du homelab
/net-map discover                      # Scanner et construire la carte
/net-map services                      # Services exposes uniquement
/net-map export                        # Exporter vers le vault Obsidian
/net-map 192.168.1.163                 # Detail d'un hote specifique
```
