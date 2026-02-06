# Commande: /lx-network

Configuration et diagnostic reseau.

## Syntaxe

```
/lx-network [action]
```

## Actions

```bash
# Adresses IP
ip -br addr

# Routes
ip route show

# DNS
resolvectl status 2>/dev/null || cat /etc/resolv.conf

# Ports en ecoute
ss -tuln

# Connexions etablies
ss -tun

# Test connectivite
ping -c 4 <host>
traceroute <host>

# DNS lookup
dig <domain>
nslookup <domain>

# Interfaces
ip link show

# Config netplan (Ubuntu)
ls /etc/netplan/
```

## Exemples

```bash
/lx-network                    # Vue d'ensemble
/lx-network ports              # Ports en ecoute
/lx-network test 8.8.8.8      # Test connectivite
```
