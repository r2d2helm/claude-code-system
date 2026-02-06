# Commande: /lx-security

Audit de securite du systeme.

## Syntaxe

```
/lx-security [check]
```

## Checks

```bash
# === SSH Hardening ===
grep -E "^(PermitRootLogin|PasswordAuthentication|Port|AllowUsers)" /etc/ssh/sshd_config

# === Mises a jour de securite ===
# Debian/Ubuntu
sudo apt list --upgradable 2>/dev/null | grep -i security
# RHEL
sudo dnf updateinfo list security 2>/dev/null

# === Fichiers SUID ===
find / -perm -4000 -type f 2>/dev/null | head -20

# === Fichiers world-writable ===
find / -perm -0002 -type f ! -path "/proc/*" ! -path "/sys/*" 2>/dev/null | head -20

# === Ports en ecoute ===
ss -tuln

# === fail2ban ===
sudo fail2ban-client status 2>/dev/null
sudo fail2ban-client status sshd 2>/dev/null

# === Dernieres connexions echouees ===
lastb -n 10 2>/dev/null

# === Utilisateurs avec shell ===
grep -v '/nologin\|/false' /etc/passwd

# === Sudo sans mot de passe ===
sudo grep -r "NOPASSWD" /etc/sudoers /etc/sudoers.d/ 2>/dev/null
```

## Score de securite

| Check | Points | Description |
|-------|--------|-------------|
| SSH root desactive | 20 | PermitRootLogin no |
| SSH password desactive | 20 | PasswordAuthentication no |
| Mises a jour | 20 | Pas de maj securite en attente |
| fail2ban actif | 15 | Protection brute force |
| Firewall actif | 15 | ufw/firewalld active |
| Pas de NOPASSWD | 10 | sudo avec mot de passe |

## Exemples

```bash
/lx-security               # Audit complet
/lx-security ssh            # Check SSH seulement
/lx-security updates        # Mises a jour securite
```
