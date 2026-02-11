# Commande: /lx-ssh

Configuration et gestion SSH.

## Syntaxe

```
/lx-ssh [action] [options]
```

## Actions

### Connexion

```bash
# Connexion simple
ssh user@host

# Port specifique
ssh -p 2222 user@host

# Avec cle specifique
ssh -i ~/.ssh/id_ed25519 user@host

# Execution de commande a distance
ssh user@host 'uptime && df -h'
```

### Gestion des cles

```bash
# Generer une cle Ed25519 (recommande)
ssh-keygen -t ed25519 -C "user@host"

# Generer une cle RSA 4096
ssh-keygen -t rsa -b 4096 -C "user@host"

# Copier la cle publique sur le serveur
ssh-copy-id user@host

# Copier avec port specifique
ssh-copy-id -p 2222 user@host

# Verifier les cles autorisees
cat ~/.ssh/authorized_keys
```

### Hardening sshd_config

```bash
# Editer la configuration
sudo nano /etc/ssh/sshd_config

# Recommandations de securite :
# PermitRootLogin no
# PasswordAuthentication no
# PubkeyAuthentication yes
# MaxAuthTries 3
# LoginGraceTime 30
# AllowUsers user1 user2
# Protocol 2
# Port 2222

# Redemarrer le service
sudo systemctl restart sshd
```

### SSH Config (~/.ssh/config)

```bash
# Fichier ~/.ssh/config
Host prod
    HostName 192.168.1.100
    User admin
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_prod

Host staging
    HostName 192.168.1.101
    User deploy
    ForwardAgent yes

# Utilisation : ssh prod / ssh staging
```

### Tunnel et port forwarding

```bash
# Tunnel local (acceder a un service distant localement)
ssh -L 8080:localhost:80 user@host

# Tunnel distant (exposer un service local)
ssh -R 8080:localhost:3000 user@host

# SOCKS proxy
ssh -D 1080 user@host

# Tunnel persistant avec autossh
autossh -M 0 -f -N -L 8080:localhost:80 user@host
```

## Options

| Option | Description |
|--------|-------------|
| `keygen` | Generer une paire de cles |
| `harden` | Appliquer le hardening sshd |
| `config` | Gerer ~/.ssh/config |
| `tunnel` | Creer un tunnel SSH |
| `--port` | Port SSH (defaut: 22) |

## Exemples

```bash
/lx-ssh keygen                       # Generer cle Ed25519
/lx-ssh harden                       # Hardening SSH
/lx-ssh config add prod 10.0.0.1     # Ajouter un host
/lx-ssh tunnel 8080:localhost:80     # Tunnel local
```

## Voir Aussi

- `/lx-firewall` - Ouvrir le port SSH
- `/lx-security` - Audit securite global
- `/lx-users` - Gestion des utilisateurs
