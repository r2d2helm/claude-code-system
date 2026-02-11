# Commande: /lx-nginx

Gestion du serveur web Nginx.

## Syntaxe

```
/lx-nginx [action] [options]
```

## Actions

### Installation et status

```bash
# Installer (Debian/Ubuntu)
sudo apt update && sudo apt install -y nginx

# Installer (RHEL/Rocky)
sudo dnf install -y nginx

# Status
sudo systemctl status nginx

# Tester la configuration
sudo nginx -t

# Recharger (sans downtime)
sudo systemctl reload nginx

# Redemarrer
sudo systemctl restart nginx
```

### Creer un site (virtual host)

```bash
# Creer la configuration
sudo nano /etc/nginx/sites-available/mysite.conf

# Contenu type :
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/mysite;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    # Logs
    access_log /var/log/nginx/mysite.access.log;
    error_log /var/log/nginx/mysite.error.log;
}

# Activer le site
sudo ln -s /etc/nginx/sites-available/mysite.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### Reverse Proxy

```bash
# Proxy vers une application backend
server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### HTTPS avec certificat

```bash
# Configuration SSL (apres certbot ou certificat manuel)
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Securite SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;
}

# Redirect HTTP -> HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

### Maintenance

```bash
# Lister les sites actifs
ls -la /etc/nginx/sites-enabled/

# Desactiver un site
sudo rm /etc/nginx/sites-enabled/mysite.conf
sudo systemctl reload nginx

# Voir les logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Rotation des logs
sudo logrotate -f /etc/logrotate.d/nginx
```

## Options

| Option | Description |
|--------|-------------|
| `status` | Etat du serveur Nginx |
| `create` | Creer un virtual host |
| `proxy` | Configurer un reverse proxy |
| `ssl` | Activer HTTPS |
| `test` | Tester la configuration |

## Exemples

```bash
/lx-nginx status                         # Etat Nginx
/lx-nginx create mysite example.com      # Creer un site
/lx-nginx proxy app 3000                 # Reverse proxy vers port 3000
/lx-nginx test                           # Valider la config
```

## Voir Aussi

- `/lx-certbot` - Certificats SSL Let's Encrypt
- `/lx-firewall` - Ouvrir ports 80/443
- `/lx-dns` - Configuration DNS
