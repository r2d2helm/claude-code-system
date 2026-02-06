# Commande: /lx-firewall

Gestion du firewall (auto-detection ufw/firewalld).

## Syntaxe

```
/lx-firewall [action] [rule]
```

## Actions UFW (Ubuntu/Debian)

```bash
# Status
sudo ufw status verbose

# Activer/Desactiver
sudo ufw enable
sudo ufw disable

# Autoriser
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow from 192.168.1.0/24

# Refuser
sudo ufw deny 3306/tcp

# Supprimer une regle
sudo ufw delete allow 80/tcp
sudo ufw status numbered
sudo ufw delete <number>

# Presets courants
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
```

## Actions firewalld (RHEL/Rocky)

```bash
sudo firewall-cmd --state
sudo firewall-cmd --list-all
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
```

## Exemples

```bash
/lx-firewall status            # Voir les regles
/lx-firewall allow 80,443      # Ouvrir web
/lx-firewall deny 3306         # Bloquer MySQL externe
```
