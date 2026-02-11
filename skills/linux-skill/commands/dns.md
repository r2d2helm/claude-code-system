# Commande: /lx-dns

Configuration DNS (resolv.conf, systemd-resolved, Bind9, dnsmasq).

## Syntaxe

```
/lx-dns [action] [options]
```

## Actions

### Diagnostic DNS

```bash
# Resolution DNS
dig example.com
dig example.com +short

# Type specifique
dig MX example.com
dig TXT example.com
dig AAAA example.com

# Serveur DNS specifique
dig @8.8.8.8 example.com

# Trace complete
dig +trace example.com

# nslookup (alternatif)
nslookup example.com

# Resolution inverse
dig -x 93.184.216.34

# Verifier la configuration actuelle
resolvectl status
cat /etc/resolv.conf
```

### Configuration resolv.conf

```bash
# Configuration directe
cat > /etc/resolv.conf << 'EOF'
nameserver 1.1.1.1
nameserver 8.8.8.8
search example.com
options timeout:2 attempts:3
EOF
```

### systemd-resolved

```bash
# Status
resolvectl status

# Configurer un DNS global
sudo nano /etc/systemd/resolved.conf
# [Resolve]
# DNS=1.1.1.1 8.8.8.8
# FallbackDNS=9.9.9.9
# DNSOverTLS=opportunistic

# Redemarrer
sudo systemctl restart systemd-resolved

# Vider le cache DNS
resolvectl flush-caches
resolvectl statistics
```

### Fichier hosts

```bash
# Ajouter une entree locale
echo "192.168.1.100 myserver.local" | sudo tee -a /etc/hosts

# Lister les entrees
cat /etc/hosts

# Verifier la priorite (hosts vs DNS)
grep hosts /etc/nsswitch.conf
```

## Options

| Option | Description |
|--------|-------------|
| `status` | Etat de la resolution DNS |
| `lookup` | Resoudre un nom |
| `flush` | Vider le cache DNS |
| `config` | Configurer le DNS |
| `--server` | Serveur DNS specifique |

## Exemples

```bash
/lx-dns status                       # Etat DNS actuel
/lx-dns lookup example.com           # Resoudre un nom
/lx-dns flush                        # Vider le cache
/lx-dns config 1.1.1.1 8.8.8.8      # Configurer les serveurs DNS
```

## Voir Aussi

- `/lx-network` - Configuration reseau
- `/lx-firewall` - Regles firewall (port 53)
