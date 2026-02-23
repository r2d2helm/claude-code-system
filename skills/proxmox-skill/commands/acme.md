# /pve-acme - Certificats SSL ACME/Let's Encrypt

## Description
Gestion des certificats SSL pour l'interface web Proxmox via le protocole ACME.
Supporte Let's Encrypt et d'autres CA compatibles ACME avec validation HTTP ou DNS.

## Syntaxe
```
/pve-acme <action> [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `status` | `/pve-acme status` | Etat des certificats |
| `register` | `/pve-acme register` | Enregistrer compte ACME |
| `order` | `/pve-acme order [node]` | Commander certificat |
| `renew` | `/pve-acme renew [node]` | Renouveler certificat |
| `revoke` | `/pve-acme revoke [node]` | Revoquer certificat |
| `plugins` | `/pve-acme plugins` | Gerer plugins DNS |

## Exemples

### Configuration initiale

```bash
# Enregistrer un compte ACME Let's Encrypt
pvenode acme account register default admin@example.com \
  --directory https://acme-v02.api.letsencrypt.org/directory

# Enregistrer compte staging (test)
pvenode acme account register staging admin@example.com \
  --directory https://acme-staging-v02.api.letsencrypt.org/directory

# Lister les comptes
pvenode acme account list

# Informations compte
pvenode acme account info default
```

### Certificat avec validation HTTP (standalone)

```bash
# Configurer le domaine sur le node
pvenode config set --acme domains=pve01.example.com

# Commander le certificat (validation HTTP port 80)
pvenode acme cert order

# Verifier le certificat
pvenode acme cert info
openssl x509 -in /etc/pve/nodes/pve01/pveproxy-ssl.pem -noout -dates -subject

# Renouveler manuellement
pvenode acme cert renew
```

### Certificat avec validation DNS

```bash
# Ajouter plugin DNS (Cloudflare)
pvenode acme plugin add dns cloudflare-plugin \
  --api cf \
  --data "CF_Token=your-api-token"

# Ajouter plugin DNS (OVH)
pvenode acme plugin add dns ovh-plugin \
  --api ovh \
  --data "OVH_AK=app-key,OVH_AS=app-secret,OVH_CK=consumer-key"

# Configurer domaine avec plugin DNS
pvenode config set \
  --acme domains=pve01.example.com \
  --acmedomain0 domain=pve01.example.com,plugin=cloudflare-plugin

# Commander certificat DNS
pvenode acme cert order

# Lister plugins configures
pvenode acme plugin list
```

### Renouvellement automatique

```bash
# Le renouvellement est automatique via systemd timer
systemctl status pvecert-renew.timer
systemctl list-timers pvecert-renew*

# Forcer renouvellement sur tous les nodes
for node in pve01 pve02 pve03; do
  ssh root@$node "pvenode acme cert renew" 2>&1
done

# Verifier expiration
openssl x509 -in /etc/pve/nodes/$(hostname)/pveproxy-ssl.pem \
  -noout -enddate
```

### Via API

```bash
# Commander via API
pvesh create /nodes/pve01/certificates/acme/certificate

# Renouveler via API
pvesh set /nodes/pve01/certificates/acme/certificate

# Informations certificat
pvesh get /nodes/pve01/certificates/info --output-format=json-pretty
```

## Notes

- Validation HTTP : le port 80 doit etre accessible depuis Internet
- Validation DNS : preferable en environnement prive (pas de port 80 requis)
- Le timer systemd renouvelle automatiquement 30 jours avant expiration
- Apres renouvellement, pveproxy redemarre automatiquement
- Utiliser le staging Let's Encrypt pour les tests (pas de rate limiting)
- Sauvegarder `/etc/pve/priv/acme/` avec les cles de compte

## Voir Aussi
- `/pve-security` - Hardening et securite
- `/pve-network` - Configuration reseau
- `/pve-node` - Gestion des nodes
