---
name: net-dns
description: Gerer et diagnostiquer DNS (dig, nslookup, /etc/hosts, resolution)
---

# /net-dns - Gestion et Diagnostic DNS

## Cible : $ARGUMENTS

Diagnostiquer et configurer la resolution DNS.

## Actions

### Diagnostic (par defaut)

1. Afficher la configuration DNS actuelle
2. Tester la resolution de noms courants
3. Verifier la resolution des VMs du homelab
4. Mesurer le temps de resolution

### Lookup (cible = hostname)

Resolution DNS d'un nom specifique avec details (A, AAAA, MX, NS, CNAME).

### Hosts (action = "hosts")

Gerer le fichier hosts local pour le DNS du homelab.

## Commandes par Plateforme

### Windows (PowerShell)

```powershell
# Configuration DNS actuelle
Get-DnsClientServerAddress -AddressFamily IPv4

# Resolution
Resolve-DnsName example.com
Resolve-DnsName example.com -Type MX
Resolve-DnsName example.com -Server 8.8.8.8

# Cache DNS
Get-DnsClientCache
Clear-DnsClientCache

# Fichier hosts
Get-Content C:\Windows\System32\drivers\etc\hosts

# Ajouter une entree hosts (admin requis)
Add-Content -Path "C:\Windows\System32\drivers\etc\hosts" -Value "192.168.1.163`tr2d2-main"
```

### Linux (Bash)

```bash
# Configuration DNS
cat /etc/resolv.conf
resolvectl status   # systemd-resolved

# Resolution
dig example.com
dig example.com MX
dig @8.8.8.8 example.com +short

# Reverse DNS
dig -x 192.168.1.163

# Trace DNS (chemin de resolution complet)
dig +trace example.com

# Fichier hosts
cat /etc/hosts

# Ajouter une entree hosts
echo "192.168.1.163 r2d2-main" | sudo tee -a /etc/hosts
```

## Mapping DNS Homelab Recommande

Entrees a ajouter dans /etc/hosts ou le fichier hosts Windows :

```
# Homelab r2d2
192.168.1.215   proxmox pve
192.168.1.162   r2d2-stage vm100
192.168.1.101   r2d2-monitor vm101
192.168.1.163   r2d2-main vm103
192.168.1.164   r2d2-store vm104
192.168.1.161   r2d2-lab vm105
```

## Format de Sortie

```
# DNS Diagnostic

## Serveurs DNS configures
| Interface | DNS Primaire | DNS Secondaire |
|-----------|-------------|----------------|

## Resolution Homelab
| Nom | IP Attendue | Resolue | Status |
|-----|-------------|---------|--------|

## Resolution Externe
| Domaine | IP | TTL | Temps |
|---------|-----|-----|-------|

## Fichier Hosts
[Contenu actuel avec les entrees homelab surlignees]
```

## Exemples

```
/net-dns                               # Diagnostic DNS complet
/net-dns google.com                    # Lookup d'un domaine
/net-dns hosts                         # Afficher/gerer le fichier hosts
/net-dns hosts setup                   # Deployer les entrees homelab
/net-dns flush                         # Vider le cache DNS
```
