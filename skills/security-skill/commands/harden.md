# Commande: /sec-harden

Appliquer le hardening sur une machine cible. Securise SSH, kernel (sysctl), services inutiles, et parametres systeme.

## Cible : $ARGUMENTS

Accepte : un nom de VM (`vm100`, `vm103`, `proxmox`), une IP, ou `all` (avec confirmation).

## Syntaxe

```
/sec-harden [cible] [--category <cat>] [--dry-run]
```

## Processus

### 1. Hardening SSH

```bash
# Backup de la config existante
ssh root@<IP> "cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%Y%m%d)"

# Creer un fichier de hardening
ssh root@<IP> 'cat > /etc/ssh/sshd_config.d/99-hardening.conf << EOF
# Hardening SSH - r2d2 homelab
PermitRootLogin prohibit-password
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowTcpForwarding no
MaxSessions 3
EOF'

# Valider la config avant restart
ssh root@<IP> "sshd -t && systemctl restart sshd"
```

**IMPORTANT** : Toujours verifier qu'une cle SSH est en place AVANT de desactiver le password auth.

### 2. Hardening Kernel (sysctl)

```bash
ssh root@<IP> 'cat > /etc/sysctl.d/99-hardening.conf << EOF
# Desactiver IP forwarding (sauf si routeur)
net.ipv4.ip_forward = 0

# Protection contre le spoofing
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignorer les redirections ICMP
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0

# Ignorer les requetes ICMP broadcast
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Protection SYN flood
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048

# Desactiver source routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0

# Logs des paquets suspects
net.ipv4.conf.all.log_martians = 1

# IPv6 (desactiver si non utilise)
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
EOF'

# Appliquer
ssh root@<IP> "sysctl -p /etc/sysctl.d/99-hardening.conf"
```

**Exception** : Sur les hotes Docker, `net.ipv4.ip_forward = 1` est REQUIS.

### 3. Desactiver les Services Inutiles

```bash
# Lister les services actifs
ssh root@<IP> "systemctl list-units --type=service --state=running"

# Services typiquement inutiles sur un serveur
ssh root@<IP> "systemctl disable --now avahi-daemon 2>/dev/null"
ssh root@<IP> "systemctl disable --now cups 2>/dev/null"
ssh root@<IP> "systemctl disable --now bluetooth 2>/dev/null"
ssh root@<IP> "systemctl disable --now ModemManager 2>/dev/null"
```

### 4. Installer fail2ban

```bash
ssh root@<IP> "apt install -y fail2ban"

ssh root@<IP> 'cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
ignoreip = 127.0.0.1/8 192.168.1.0/24

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
EOF'

ssh root@<IP> "systemctl enable --now fail2ban"
```

### 5. Mises a Jour Automatiques

```bash
ssh root@<IP> "apt install -y unattended-upgrades"
ssh root@<IP> "dpkg-reconfigure -plow unattended-upgrades"

# Verifier la configuration
ssh root@<IP> "cat /etc/apt/apt.conf.d/20auto-upgrades"
```

### 6. Permissions Fichiers Critiques

```bash
ssh root@<IP> "chmod 640 /etc/shadow"
ssh root@<IP> "chmod 644 /etc/passwd"
ssh root@<IP> "chmod 440 /etc/sudoers"
ssh root@<IP> "find /opt /home -name '.env' -exec chmod 600 {} \;"
```

### 7. Configurer la Rotation des Logs

```bash
# Verifier logrotate
ssh root@<IP> "cat /etc/logrotate.d/rsyslog"

# Verifier que auth.log est couvert
ssh root@<IP> "ls -la /var/log/auth.log"
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Afficher les actions sans les executer |
| `--category ssh\|sysctl\|services\|fail2ban\|updates\|perms` | Appliquer une categorie uniquement |
| `--force` | Ne pas demander de confirmation |
| `--skip-ssh` | Passer le hardening SSH (utile si deja fait) |

## Precautions

1. **Toujours tester la connexion SSH** dans un second terminal avant de fermer la session
2. **Backup avant modification** : chaque etape cree un backup date
3. **Ne pas desactiver ip_forward** sur les hotes Docker
4. **ignoreip** dans fail2ban inclut le reseau local 192.168.1.0/24
5. **Ne pas appliquer sur Proxmox** les sysctl qui interfereraient avec la virtualisation

## Exemples

```bash
/sec-harden vm100                              # Hardening complet VM 100
/sec-harden vm103 --category ssh               # SSH seulement sur VM 103
/sec-harden all --dry-run                      # Preview sur toutes les machines
/sec-harden proxmox --skip-ssh --category sysctl  # Sysctl Proxmox (SSH deja fait)
```

## Voir Aussi

- `/sec-audit` - Auditer avant de hardener
- `/sec-firewall` - Configurer le firewall
- `/sec-wizard harden` - Hardening guide etape par etape
