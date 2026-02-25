# Commande: /sec-ssl

Gerer les certificats SSL/TLS : creation, verification, renouvellement, self-signed pour le homelab.

## Cible : $ARGUMENTS

Accepte : une action (`check`, `create`, `renew`, `list`) et optionnellement un domaine ou une IP.

## Syntaxe

```
/sec-ssl [action] [domaine/IP] [options]
```

## Actions

### Verifier un certificat

```bash
# Verifier un certificat distant (service web)
echo | openssl s_client -connect <IP>:<PORT> -servername <DOMAIN> 2>/dev/null | openssl x509 -noout -dates -subject -issuer

# Verifier un fichier certificat local
openssl x509 -in /path/to/cert.pem -noout -text
openssl x509 -in /path/to/cert.pem -noout -dates

# Verifier l'expiration
openssl x509 -in /path/to/cert.pem -noout -enddate

# Verifier la chaine de confiance
openssl verify -CAfile ca.pem cert.pem

# Verifier que cle et certificat correspondent
openssl x509 -noout -modulus -in cert.pem | md5sum
openssl rsa -noout -modulus -in key.pem | md5sum
```

### Verifier les services homelab

```bash
# Proxmox Web UI (auto-signe par defaut)
echo | openssl s_client -connect 192.168.1.215:8006 2>/dev/null | openssl x509 -noout -dates -subject

# Verifier tous les services en une fois
for target in "192.168.1.215:8006" "192.168.1.162:8091" "192.168.1.163:8020"; do
  echo "=== $target ==="
  echo | openssl s_client -connect "$target" 2>/dev/null | openssl x509 -noout -dates 2>/dev/null || echo "Pas de TLS"
done
```

### Creer un certificat self-signed

```bash
# Pour le homelab (valide 365 jours)
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout server.key \
  -out server.crt \
  -subj "/C=FR/O=r2d2-homelab/CN=<hostname>"

# Avec SAN (Subject Alternative Names) pour plusieurs IPs/domaines
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout server.key \
  -out server.crt \
  -subj "/C=FR/O=r2d2-homelab/CN=homelab" \
  -addext "subjectAltName=IP:192.168.1.162,IP:192.168.1.163,DNS:homelab.local"
```

### Creer une CA locale (homelab)

```bash
# 1. Generer la cle de la CA
openssl genrsa -out ca.key 4096

# 2. Creer le certificat CA (valide 10 ans)
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 \
  -out ca.crt \
  -subj "/C=FR/O=r2d2-homelab/CN=r2d2-CA"

# 3. Generer une CSR pour un service
openssl req -new -nodes \
  -newkey rsa:2048 \
  -keyout service.key \
  -out service.csr \
  -subj "/C=FR/O=r2d2-homelab/CN=service.homelab.local"

# 4. Signer avec la CA
openssl x509 -req -in service.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out service.crt -days 365 -sha256
```

### Let's Encrypt (certbot)

```bash
# Obtenir un certificat (si domaine public)
ssh root@<IP> "certbot certonly --standalone -d <domaine>"

# Renouveler
ssh root@<IP> "certbot renew"

# Verifier le timer de renouvellement
ssh root@<IP> "systemctl status certbot.timer"

# Lister les certificats
ssh root@<IP> "certbot certificates"
```

### Deployer un certificat dans Docker (reverse proxy)

```bash
# Avec Nginx reverse proxy
ssh root@<IP> 'cat > /opt/nginx/conf.d/ssl.conf << EOF
server {
    listen 443 ssl;
    server_name service.homelab.local;

    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://service:8080;
    }
}
EOF'
```

## Options

| Option | Description |
|--------|-------------|
| `check` | Verifier un certificat (distant ou local) |
| `create` | Creer un certificat self-signed |
| `ca` | Creer ou gerer une CA locale |
| `renew` | Renouveler un certificat |
| `list` | Lister les certificats installes |
| `--days N` | Duree de validite (defaut: 365) |
| `--san` | Ajouter des Subject Alternative Names |

## Exemples

```bash
/sec-ssl check 192.168.1.215:8006        # Verifier le cert Proxmox
/sec-ssl check all                        # Verifier tous les services
/sec-ssl create vm100 --san               # Cert self-signed avec SANs
/sec-ssl ca init                          # Creer une CA homelab
/sec-ssl renew certbot                    # Renouveler Let's Encrypt
```

## Voir Aussi

- `/lx-certbot` - Gestion detaillee Let's Encrypt
- `/lx-nginx` - Configuration Nginx avec SSL
- `/sec-audit` - Audit incluant les certificats
