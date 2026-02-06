# 🔐 /pve-security - Sécurité & Hardening

## Description
Hardening et sécurisation complète de Proxmox VE 9+ selon les best practices 2025-2026.

## Syntaxe
```
/pve-security [action] [options]
```

## Audit Sécurité

### `audit` - Audit complet
```bash
# Script audit sécurité
cat > /usr/local/bin/pve-security-audit << 'EOF'
#!/bin/bash
echo "=== PROXMOX SECURITY AUDIT ==="
echo "Date: $(date)"
echo ""

echo "=== SSH Configuration ==="
grep -E "^(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication)" /etc/ssh/sshd_config

echo ""
echo "=== Fail2ban Status ==="
systemctl is-active fail2ban 2>/dev/null || echo "WARN: fail2ban not running"
fail2ban-client status 2>/dev/null | head -5

echo ""
echo "=== 2FA Status ==="
pveum user list | while read user; do
  realm=$(echo $user | cut -d@ -f2)
  if [[ "$realm" == "pve" ]] || [[ "$realm" == "pam" ]]; then
    tfa=$(pveum user tfa-status $user 2>/dev/null)
    echo "$user: $tfa"
  fi
done

echo ""
echo "=== API Tokens ==="
pveum user token list root@pam 2>/dev/null | wc -l
echo "tokens configured for root@pam"

echo ""
echo "=== Firewall Status ==="
pve-firewall status

echo ""
echo "=== Open Ports ==="
ss -tulpn | grep LISTEN | awk '{print $5}' | sort -u

echo ""
echo "=== Pending Updates ==="
apt list --upgradable 2>/dev/null | grep -c upgradable

echo ""
echo "=== Failed Logins (last 24h) ==="
journalctl --since "24 hours ago" | grep -c "authentication failure"
EOF
chmod +x /usr/local/bin/pve-security-audit
```

## SSH Hardening

### Configuration sécurisée
```bash
# Backup config originale
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Appliquer hardening
cat >> /etc/ssh/sshd_config << 'EOF'

# === Proxmox Hardening 2025 ===
PermitRootLogin prohibit-password
PasswordAuthentication no
PubkeyAuthentication yes
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding no
PrintMotd no
AcceptEnv LANG LC_*
MaxAuthTries 3
MaxSessions 5
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers root@10.0.0.0/24
Protocol 2
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
EOF

# Régénérer clés si nécessaire
ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N "" -q

# Redémarrer SSH
systemctl restart sshd
```

### Ajouter clé SSH
```bash
# Sur le serveur
mkdir -p ~/.ssh && chmod 700 ~/.ssh
cat >> ~/.ssh/authorized_keys << 'EOF'
ssh-ed25519 AAAA... user@workstation
EOF
chmod 600 ~/.ssh/authorized_keys
```

## 2FA/TOTP

### Activer 2FA pour un utilisateur
```bash
# Via Web UI: Datacenter > Permissions > Two Factor

# Via CLI - générer secret TOTP
pveum user tfa add root@pam totp --description "Admin TOTP"
# Scanner le QR code avec app authenticator

# Vérifier status 2FA
pveum user tfa-status root@pam
```

### Forcer 2FA pour realm
```bash
# Éditer realm
pveum realm modify pam --tfa-required 1

# Ou pour PAM
pveum realm modify pve --tfa-required 1
```

## Fail2ban

### Installation et configuration
```bash
# Installer
apt install fail2ban -y

# Configuration Proxmox
cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 3
ignoreip = 127.0.0.1/8 10.0.0.0/24

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

[proxmox]
enabled = true
port = https,http,8006
filter = proxmox
logpath = /var/log/daemon.log
maxretry = 3
bantime = 3600
EOF

# Filtre Proxmox
cat > /etc/fail2ban/filter.d/proxmox.conf << 'EOF'
[Definition]
failregex = pvedaemon\[.*authentication failure; rhost=<HOST> user=.* msg=.*
ignoreregex =
journalmatch = _SYSTEMD_UNIT=pvedaemon.service
EOF

# Activer et démarrer
systemctl enable fail2ban
systemctl restart fail2ban

# Vérifier status
fail2ban-client status
fail2ban-client status proxmox
```

### Gestion bans
```bash
# Voir IPs bannies
fail2ban-client status sshd

# Débannir IP
fail2ban-client set sshd unbanip 192.168.1.100

# Bannir manuellement
fail2ban-client set sshd banip 192.168.1.100
```

## API Tokens

### Créer token automation
```bash
# Token pour Terraform
pveum user add terraform@pve
pveum aclmod / -user terraform@pve -role PVEAdmin
pveum user token add terraform@pve terraform-token --privsep 0
# Sauvegarder le token affiché !

# Token lecture seule (monitoring)
pveum user add monitoring@pve
pveum aclmod / -user monitoring@pve -role PVEAuditor
pveum user token add monitoring@pve prometheus-token --privsep 0
```

### Utiliser token
```bash
# Format: user@realm!tokenid=secret
TOKEN="terraform@pve!terraform-token=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# Test API
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  https://localhost:8006/api2/json/version
```

## Firewall Strict

### Policy DROP par défaut
```bash
# Datacenter firewall
pvesh set /cluster/firewall/options \
  --enable 1 \
  --policy_in DROP \
  --policy_out ACCEPT

# Règles essentielles
pvesh create /cluster/firewall/rules \
  --action ACCEPT --type in --proto tcp --dport 22 \
  --source 10.0.0.0/24 --comment "SSH from management"

pvesh create /cluster/firewall/rules \
  --action ACCEPT --type in --proto tcp --dport 8006 \
  --source 10.0.0.0/24 --comment "Web UI from management"

pvesh create /cluster/firewall/rules \
  --action ACCEPT --type in --proto icmp \
  --comment "ICMP ping"
```

## Updates Sécurité

### Unattended upgrades
```bash
# Installer
apt install unattended-upgrades apt-listchanges -y

# Configurer
cat > /etc/apt/apt.conf.d/50unattended-upgrades << 'EOF'
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    "${distro_id}:${distro_codename}-updates";
    "Proxmox:${distro_codename}";
};
Unattended-Upgrade::Package-Blacklist {
    "pve-kernel";
};
Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::Mail "admin@example.com";
Unattended-Upgrade::MailReport "on-change";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
EOF

# Activer
cat > /etc/apt/apt.conf.d/20auto-upgrades << 'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
EOF

# Test
unattended-upgrade --dry-run
```

## Audit Logging

### Configurer auditd
```bash
# Installer
apt install auditd audispd-plugins -y

# Règles Proxmox
cat > /etc/audit/rules.d/proxmox.rules << 'EOF'
# Surveiller fichiers config Proxmox
-w /etc/pve/ -p wa -k proxmox_config
-w /etc/pve/user.cfg -p wa -k proxmox_users
-w /etc/pve/authkey.pub -p wa -k proxmox_auth

# Surveiller commandes admin
-a always,exit -F arch=b64 -S execve -F euid=0 -k admin_commands

# Surveiller accès SSH
-w /var/log/auth.log -p wa -k auth_log
EOF

# Charger règles
augenrules --load
systemctl restart auditd

# Voir logs
ausearch -k proxmox_config
```

## Certificats SSL

### Let's Encrypt ACME
```bash
# Configurer ACME account
pvenode acme account register default admin@example.com

# Configurer challenge DNS (recommandé)
pvenode config set --acme domains=pve.example.com

# Ou challenge HTTP
pvenode acme cert order

# Renouvellement auto via timer systemd
systemctl enable pve-acme-timer
```

### Certificat personnalisé
```bash
# Importer certificat
cp mycert.pem /etc/pve/local/pveproxy-ssl.pem
cp mykey.pem /etc/pve/local/pveproxy-ssl.key
chmod 640 /etc/pve/local/pveproxy-ssl.key

# Redémarrer proxy
systemctl restart pveproxy
```

## Checklist Sécurité

### Production Hardening
```
[x] SSH: Clés uniquement, pas de password
[x] SSH: PermitRootLogin prohibit-password ou no
[x] 2FA/TOTP: Activé pour tous les admins
[x] Fail2ban: SSH + Proxmox jails actifs
[x] API Tokens: Pour toute automation
[x] Firewall: Policy DROP, règles explicites
[x] Updates: Unattended-upgrades activé
[x] SSL: Certificat valide (Let's Encrypt)
[x] Audit: auditd configuré
[x] Backup: Clés et secrets sauvegardés
```

## Commandes Rapides

```bash
# Status sécurité rapide
pve-security-audit

# Voir connexions SSH
who -a

# Voir tentatives échouées
lastb | head -20

# Voir dernières connexions réussies
last | head -20

# Checker vulnérabilités
apt update && apt list --upgradable

# Vérifier firewall
pve-firewall status && iptables -L -n
```
