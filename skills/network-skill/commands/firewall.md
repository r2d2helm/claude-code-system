---
name: net-firewall
description: Regles firewall reseau (ufw, iptables, Windows Firewall)
---

# /net-firewall - Gestion Firewall

## Cible : $ARGUMENTS

Gerer et diagnostiquer les regles firewall sur Windows, Linux et Proxmox.

## Actions

### Status (par defaut)

Afficher l'etat du firewall et les regles actives.

### Allow/Deny (action + port/service)

Ajouter ou supprimer des regles.

### Audit

Verifier la coherence des regles avec les services actifs.

## Commandes par Plateforme

### Windows Firewall (PowerShell)

```powershell
# Status
Get-NetFirewallProfile | Format-Table Name, Enabled, DefaultInboundAction

# Regles actives (entrant)
Get-NetFirewallRule -Direction Inbound -Enabled True |
    Get-NetFirewallPortFilter |
    Where-Object LocalPort -ne $null |
    Format-Table @{N='Rule';E={$_.InstanceID}}, Protocol, LocalPort

# Autoriser un port
New-NetFirewallRule -DisplayName "Allow SSH" -Direction Inbound -Protocol TCP -LocalPort 22 -Action Allow

# Bloquer un port
New-NetFirewallRule -DisplayName "Block Telnet" -Direction Inbound -Protocol TCP -LocalPort 23 -Action Block

# Supprimer une regle
Remove-NetFirewallRule -DisplayName "Allow SSH"

# Activer/Desactiver un profil
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

### UFW (Linux - Ubuntu/Debian)

```bash
# Status
sudo ufw status verbose

# Status numerote (pour suppression)
sudo ufw status numbered

# Activer
sudo ufw enable

# Politique par defaut
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Autoriser
sudo ufw allow 22/tcp                    # Port
sudo ufw allow from 192.168.1.0/24       # Sous-reseau
sudo ufw allow from 192.168.1.243 to any port 22   # IP + port

# Bloquer
sudo ufw deny 23/tcp

# Supprimer (par numero)
sudo ufw delete 3

# Reload
sudo ufw reload

# Logs
sudo ufw logging on
tail -f /var/log/ufw.log
```

### iptables (Linux)

```bash
# Lister les regles
sudo iptables -L -n -v
sudo iptables -L -n --line-numbers

# Autoriser
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT

# Bloquer
sudo iptables -A INPUT -p tcp --dport 23 -j DROP

# Supprimer (par numero)
sudo iptables -D INPUT 3

# Sauvegarder
sudo iptables-save > /etc/iptables/rules.v4

# Docker et iptables
# ATTENTION : Docker insere ses propres regles et bypass ufw
sudo iptables -L DOCKER-USER -n -v
```

### Proxmox Firewall

```bash
# Status
pve-firewall status

# Configuration datacenter
cat /etc/pve/firewall/cluster.fw

# Configuration VM
cat /etc/pve/firewall/<vmid>.fw

# Activer via API
pvesh set /cluster/firewall/options -enable 1
pvesh set /nodes/<node>/qemu/<vmid>/firewall/options -enable 1
```

## Regles Recommandees Homelab

### VMs Linux (ufw)
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 192.168.1.0/24 to any port 22    # SSH depuis LAN
# + ports specifiques selon le role de la VM
```

### VM 100 (Monitoring)
```bash
sudo ufw allow from 192.168.1.0/24 to any port 8091   # Beszel Hub
sudo ufw allow from 192.168.1.0/24 to any port 3003   # Uptime Kuma
sudo ufw allow from 192.168.1.0/24 to any port 19999  # Netdata
sudo ufw allow from 192.168.1.0/24 to any port 8082   # Dozzle
sudo ufw allow from 192.168.1.0/24 to any port 8084   # ntfy
```

## Piege Docker + UFW

Docker modifie directement iptables et bypass ufw. Pour limiter l'acces a un port Docker :

```bash
# Dans DOCKER-USER chain
sudo iptables -I DOCKER-USER -i eth0 ! -s 192.168.1.0/24 -j DROP

# Ou utiliser docker-compose avec bind IP
ports:
  - "192.168.1.162:8091:8091"   # Ecoute uniquement sur cette IP
```

## Format de Sortie

```
# Firewall - [machine]

## Status
| Profil/Zone | Active | Politique Entrant | Politique Sortant |
|-------------|--------|-------------------|-------------------|

## Regles Actives
| # | Direction | Port | Proto | Source | Action |
|---|-----------|------|-------|--------|--------|

## Problemes
- [WARN] Docker bypass : port XXXX accessible malgre ufw deny
```

## Exemples

```
/net-firewall                          # Status firewall local
/net-firewall allow 8080               # Autoriser le port 8080
/net-firewall deny 23                  # Bloquer telnet
/net-firewall audit                    # Verifier la coherence
/net-firewall docker                   # Regles Docker-specifiques
```
