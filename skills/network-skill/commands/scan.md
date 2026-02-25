---
name: net-scan
description: Scanner le reseau (decouverte hosts, ports ouverts)
---

# /net-scan - Scanner Reseau

## Cible : $ARGUMENTS

Scanne le reseau pour decouvrir les hotes actifs et les ports ouverts.

## Comportement

### Mode decouverte (par defaut ou "discover")

Scanner tout le sous-reseau 192.168.1.0/24 pour lister les hotes actifs.

### Mode ports (cible = IP)

Scanner les ports d'un hote specifique.

### Mode services (cible = IP + "services")

Scanner les ports avec detection de version des services.

## Commandes par Plateforme

### Windows (PowerShell)

```powershell
# Scan de decouverte rapide (sans nmap)
$subnet = "192.168.1"
1..254 | ForEach-Object {
    $ip = "$subnet.$_"
    $ping = Test-Connection -ComputerName $ip -Count 1 -Quiet -TimeoutSeconds 1
    if ($ping) { [PSCustomObject]@{IP=$ip; Status="UP"} }
}

# Avec nmap (si installe)
nmap -sn 192.168.1.0/24

# Scan de ports
nmap -sT -p 1-1024 $target

# Scan de services
nmap -sV -p 22,80,443,3003,8006,8020,8082,8084,8091,19999,45876 $target
```

### Linux (Bash)

```bash
# Scan de decouverte
nmap -sn 192.168.1.0/24

# Scan de ports rapide
nmap -sT --top-ports 100 $target

# Scan de ports complet
nmap -sT -p- $target

# Scan de services avec versions
nmap -sV -sC -p 22,80,443,3003,8006,8020,8082,8084,8091,19999,45876 $target

# Scan agressif (OS detection + scripts)
nmap -A $target
```

## Ports Homelab a Scanner

Lors d'un scan cible sur le homelab, toujours inclure ces ports :

```
22,80,443,3003,3020,8006,8020,8082,8084,8091,19999,45876
```

## Format de Sortie

```
# Scan Reseau - [scope]

## Hotes Actifs : X/254
| IP | Hostname | MAC | Vendor |
|----|----------|-----|--------|

## Ports Ouverts (si cible)
| Port | Proto | Service | Version |
|------|-------|---------|---------|

## Hotes Inconnus
| IP | MAC | Note |
|----|-----|------|
```

## Exemples

```
/net-scan                              # Decouverte 192.168.1.0/24
/net-scan 192.168.1.163                # Ports ouverts sur VM 103
/net-scan 192.168.1.215 services       # Scan services Proxmox
/net-scan discover                     # Decouverte explicite
```

## Notes

- **nmap** doit etre installe (`winget install nmap` ou `apt install nmap`)
- Le scan de decouverte PowerShell sans nmap est plus lent mais ne necessite rien
- Les scans de ports sur des machines tierces sont a eviter sans autorisation
- Certains scans necessitent des privileges root/admin
