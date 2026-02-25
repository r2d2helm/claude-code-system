---
name: net-vpn
description: Configuration VPN (WireGuard, OpenVPN)
---

# /net-vpn - Configuration VPN

## Cible : $ARGUMENTS

Configurer et gerer les connexions VPN (WireGuard principalement, OpenVPN en fallback).

## Actions

### Status (par defaut)

Afficher l'etat des interfaces VPN actives.

### Setup WireGuard

Configuration guidee d'un tunnel WireGuard.

### Connect/Disconnect

Activer ou desactiver un tunnel VPN.

## WireGuard

### Installation

```bash
# Linux (Ubuntu/Debian)
sudo apt install wireguard wireguard-tools

# Windows
winget install WireGuard.WireGuard
```

### Generer les cles

```bash
# Cle privee + publique
wg genkey | tee privatekey | wg pubkey > publickey

# Cle pre-partagee (optionnel, securite renforcee)
wg genpsk > presharedkey
```

### Configuration Serveur

```ini
# /etc/wireguard/wg0.conf (sur le serveur VPN)
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <server_private_key>

# Activer le forwarding
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# Client 1
PublicKey = <client1_public_key>
AllowedIPs = 10.0.0.2/32
```

### Configuration Client

```ini
# /etc/wireguard/wg0.conf (sur le client)
[Interface]
Address = 10.0.0.2/24
PrivateKey = <client_private_key>
DNS = 8.8.8.8

[Peer]
PublicKey = <server_public_key>
Endpoint = <server_ip>:51820
AllowedIPs = 0.0.0.0/0          # Tout le trafic via VPN
# ou
AllowedIPs = 192.168.1.0/24     # Split tunnel (LAN uniquement)
PersistentKeepalive = 25
```

### Operations

```bash
# Demarrer
sudo wg-quick up wg0

# Arreter
sudo wg-quick down wg0

# Status
sudo wg show

# Activer au demarrage
sudo systemctl enable wg-quick@wg0

# Ajouter un peer dynamiquement
sudo wg set wg0 peer <pubkey> allowed-ips 10.0.0.3/32
```

## OpenVPN (Fallback)

```bash
# Installation
sudo apt install openvpn

# Connexion avec fichier .ovpn
sudo openvpn --config client.ovpn

# En arriere-plan
sudo openvpn --config client.ovpn --daemon

# Status
sudo systemctl status openvpn
```

## Cas d'Usage Homelab

### Acces distant au homelab

WireGuard sur le Proxmox host (.215) pour acceder aux VMs depuis l'exterieur :

```
Internet --> [Router NAT 51820] --> Proxmox (.215) wg0 (10.0.0.1)
                                        |
                                   Bridge vmbr0
                                        |
                                   VMs (192.168.1.x)
```

### Inter-site

Tunnel entre deux reseaux prives via WireGuard.

## Format de Sortie

```
# VPN - [status]

## Interfaces VPN
| Interface | Type | Status | IP VPN | Endpoint | Transfert |
|-----------|------|--------|--------|----------|-----------|

## Peers
| Peer | IP Autorisees | Dernier Handshake | RX | TX |
|------|---------------|-------------------|-----|-----|
```

## Exemples

```
/net-vpn                               # Status des VPN actifs
/net-vpn setup wireguard               # Configuration guidee WireGuard
/net-vpn connect wg0                   # Activer le tunnel wg0
/net-vpn disconnect wg0                # Desactiver le tunnel wg0
/net-vpn peers                         # Lister les peers WireGuard
```
