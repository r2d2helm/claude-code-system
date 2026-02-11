# Commande: /lx-certbot

Certificats SSL Let's Encrypt avec Certbot.

## Syntaxe

```
/lx-certbot [action] [domain] [options]
```

## Actions

### Installation

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install -y certbot python3-certbot-nginx

# RHEL/Rocky
sudo dnf install -y certbot python3-certbot-nginx

# Snap (universel)
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

### Obtenir un certificat

```bash
# Avec plugin Nginx (recommande)
sudo certbot --nginx -d example.com -d www.example.com

# Mode standalone (port 80 libre requis)
sudo certbot certonly --standalone -d example.com

# Mode webroot (serveur deja en place)
sudo certbot certonly --webroot -w /var/www/html -d example.com

# Dry-run (test sans emettre)
sudo certbot certonly --nginx -d example.com --dry-run

# Non-interactif (CI/CD)
sudo certbot --nginx -d example.com --non-interactive --agree-tos -m admin@example.com
```

### Gestion des certificats

```bash
# Lister les certificats
sudo certbot certificates

# Renouveler tous les certificats
sudo certbot renew

# Renouveler avec dry-run
sudo certbot renew --dry-run

# Revoquer un certificat
sudo certbot revoke --cert-path /etc/letsencrypt/live/example.com/fullchain.pem

# Supprimer un certificat
sudo certbot delete --cert-name example.com
```

### Renouvellement automatique

```bash
# Verifier le timer systemd
sudo systemctl list-timers | grep certbot

# Ou via crontab (si pas systemd)
# 0 3 * * * certbot renew --quiet --post-hook "systemctl reload nginx"

# Tester le renouvellement
sudo certbot renew --dry-run
```

### Wildcard (DNS challenge)

```bash
# Certificat wildcard (necessite validation DNS)
sudo certbot certonly --manual --preferred-challenges dns \
  -d "*.example.com" -d example.com

# Avec plugin Cloudflare (automatique)
sudo certbot certonly --dns-cloudflare \
  --dns-cloudflare-credentials ~/.secrets/cloudflare.ini \
  -d "*.example.com"
```

## Options

| Option | Description |
|--------|-------------|
| `install` | Installer Certbot |
| `obtain` | Obtenir un certificat |
| `renew` | Renouveler les certificats |
| `list` | Lister les certificats |
| `revoke` | Revoquer un certificat |
| `--dry-run` | Mode simulation |

## Exemples

```bash
/lx-certbot obtain example.com          # Obtenir certificat
/lx-certbot renew                        # Renouveler tous
/lx-certbot list                         # Lister les certificats
/lx-certbot obtain *.example.com --dns   # Wildcard avec DNS
```

## Voir Aussi

- `/lx-nginx` - Configuration Nginx avec SSL
- `/lx-dns` - Configuration DNS pour validation
