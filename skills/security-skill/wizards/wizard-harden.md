# Wizard: Security Hardening

Hardening guide pas a pas pour securiser une machine du homelab.

## Questions

1. **Machine** : Quelle machine hardener ? (VM, Proxmox host, Windows)
2. **Niveau** : Basique (essentiels) ou avance (complet) ?
3. **Contraintes** : Services qui doivent rester accessibles ?

## Processus de Hardening

### Etape 1 : SSH (priorite haute)

```bash
# Sauvegarder la config actuelle
ssh {user}@{ip} "cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak"

# Appliquer le hardening SSH
ssh {user}@{ip} "cat > /etc/ssh/sshd_config.d/hardening.conf << 'EOF'
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowTcpForwarding no
EOF"

# Redemarrer SSH
ssh {user}@{ip} "systemctl restart sshd"

# IMPORTANT : garder la session ouverte et tester dans un nouveau terminal
```

### Etape 2 : Firewall (priorite haute)

```bash
# Installer et configurer ufw
ssh {user}@{ip} "apt install -y ufw"
ssh {user}@{ip} "ufw default deny incoming"
ssh {user}@{ip} "ufw default allow outgoing"
ssh {user}@{ip} "ufw allow from 192.168.1.0/24 to any port 22"

# Ajouter les ports necessaires (adapter par VM)
# VM 100 : monitoring
ssh {user}@{ip} "ufw allow from 192.168.1.0/24 to any port 8091,3003,19999,8082,8084 proto tcp"

# Activer
ssh {user}@{ip} "ufw --force enable"
ssh {user}@{ip} "ufw status numbered"
```

### Etape 3 : fail2ban (priorite moyenne)

```bash
ssh {user}@{ip} "apt install -y fail2ban"

# Configurer le jail SSH
ssh {user}@{ip} "cat > /etc/fail2ban/jail.local << 'EOF'
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
ignoreip = 192.168.1.0/24
EOF"

ssh {user}@{ip} "systemctl enable --now fail2ban"
```

### Etape 4 : Mises a jour automatiques (priorite moyenne)

```bash
ssh {user}@{ip} "apt install -y unattended-upgrades"
ssh {user}@{ip} "dpkg-reconfigure -plow unattended-upgrades"
```

### Etape 5 : Kernel hardening (priorite basse)

```bash
ssh {user}@{ip} "cat > /etc/sysctl.d/99-hardening.conf << 'EOF'
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
kernel.randomize_va_space = 2
EOF"

ssh {user}@{ip} "sysctl --system"
```

### Etape 6 : Verification

Lancer `/sec-audit` pour verifier le score apres hardening.

## Precautions

- **Toujours tester SSH** avant de fermer la session active
- **Sauvegarder** les configs avant modification
- **Ne pas bloquer** les ports des services necessaires avec ufw
- **Documenter** chaque changement dans le vault
