---
name: net-ports
description: Verifier les ports (ouverts, ecoutant, occupes, tester connectivite)
---

# /net-ports - Gestion des Ports

## Cible : $ARGUMENTS

Verifier, tester et diagnostiquer les ports reseau.

## Actions

### Ecoute locale (par defaut ou "listen")

Lister tous les ports en ecoute sur la machine locale.

### Test distant (cible = IP:PORT)

Tester si un port est accessible sur une machine distante.

### Recherche (cible = numero de port)

Trouver quel processus utilise un port specifique.

### Homelab (cible = "homelab")

Verifier tous les ports services du homelab.

## Commandes par Plateforme

### Windows (PowerShell)

```powershell
# Ports en ecoute
Get-NetTCPConnection -State Listen | Sort-Object LocalPort |
    Select-Object LocalPort, OwningProcess,
    @{N='Process';E={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).ProcessName}}

# Toutes les connexions actives
Get-NetTCPConnection | Where-Object State -eq Established

# Tester un port distant
Test-NetConnection -ComputerName 192.168.1.163 -Port 8020

# Trouver qui utilise un port
Get-NetTCPConnection -LocalPort 8080 |
    Select-Object LocalPort, RemoteAddress, State, OwningProcess,
    @{N='Process';E={(Get-Process -Id $_.OwningProcess).ProcessName}}

# Ports UDP en ecoute
Get-NetUDPEndpoint | Sort-Object LocalPort
```

### Linux (Bash)

```bash
# Ports en ecoute (TCP)
ss -tlnp

# Ports en ecoute (TCP + UDP)
ss -tulnp

# Connexions actives
ss -tnp state established

# Tester un port distant
nc -zv 192.168.1.163 8020

# Tester une plage de ports
nc -zv 192.168.1.163 8000-8100

# Trouver qui utilise un port
lsof -i :8080
# ou
fuser 8080/tcp

# Netstat (legacy)
netstat -tlnp
```

## Verification Homelab Complte

Quand la cible est "homelab", tester systematiquement :

```
Gateway      .1    : -
Proxmox      .215  : 22, 8006
VM 100       .162  : 22, 8091, 3003, 19999, 8082, 8084, 45876
VM 101       .101  : 22
VM 103       .163  : 22, 8020, 3020
VM 104       .164  : 22
VM 105       .161  : 22, 8020, 3020
Windows      .243  : 45876
```

## Format de Sortie

```
# Ports - [contexte]

## Ports en ecoute (local)
| Port | Proto | PID | Processus | Adresse |
|------|-------|-----|-----------|---------|

## Test connectivite (distant)
| Cible | Port | Service Attendu | Status | Latence |
|-------|------|-----------------|--------|---------|

## Conflits detectes
- [WARN] Port XXXX utilise par ProcessA, attendu pour ServiceB
```

## Exemples

```
/net-ports                             # Ports locaux en ecoute
/net-ports 192.168.1.163:8020          # Tester un port distant
/net-ports 8080                        # Qui utilise le port 8080 ?
/net-ports homelab                     # Verifier tous les services
/net-ports listen                      # Ports locaux en ecoute
```
