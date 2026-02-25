# Commande: /sec-audit

Audit de securite complet multi-machines. Evalue la posture de securite de l'infrastructure homelab.

## Cible : $ARGUMENTS

Accepte : `all` (toutes les machines), un nom de VM (`vm100`, `vm103`, `proxmox`), ou une IP.

## Syntaxe

```
/sec-audit [cible] [--category <cat>] [--report]
```

## Processus

### 1. Audit SSH (toutes VMs)

```bash
# Verifier la configuration sshd
ssh root@<IP> "grep -E '^(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|MaxAuthTries|Port|AllowUsers|Protocol)' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null"

# Verifier les cles autorisees
ssh root@<IP> "for u in /home/*; do echo \"=== \$(basename \$u) ===\"; cat \$u/.ssh/authorized_keys 2>/dev/null || echo 'Aucune cle'; done"

# Verifier les cles root
ssh root@<IP> "cat /root/.ssh/authorized_keys 2>/dev/null"
```

### 2. Audit Ports Ouverts

```bash
# Ports en ecoute
ssh root@<IP> "ss -tuln | grep LISTEN"

# Comparer avec les ports attendus
# VM 100 : 22, 8091, 3003, 19999, 8082, 8084, 45876
# VM 103 : 22, 8020, 3020, (supabase ports), monitoring
# VM 104 : 22, 5432, NFS, monitoring
# VM 105 : 22, 8020, 3020
# Proxmox : 22, 8006
```

### 3. Audit Utilisateurs

```bash
# Utilisateurs avec shell interactif
ssh root@<IP> "grep -v '/nologin\|/false\|/sync' /etc/passwd"

# Utilisateurs avec sudo
ssh root@<IP> "getent group sudo 2>/dev/null; getent group wheel 2>/dev/null"

# NOPASSWD dans sudoers
ssh root@<IP> "grep -r 'NOPASSWD' /etc/sudoers /etc/sudoers.d/ 2>/dev/null"
```

### 4. Audit Fichiers Sensibles

```bash
# Fichiers SUID
ssh root@<IP> "find / -perm -4000 -type f 2>/dev/null | head -20"

# Fichiers world-writable
ssh root@<IP> "find /etc /var /opt -perm -0002 -type f 2>/dev/null | head -20"

# Permissions des fichiers critiques
ssh root@<IP> "ls -la /etc/shadow /etc/passwd /etc/sudoers"

# Fichiers .env exposes
ssh root@<IP> "find /opt /home -name '.env' -exec ls -la {} \; 2>/dev/null"
```

### 5. Audit Firewall

```bash
# Status ufw
ssh root@<IP> "ufw status verbose 2>/dev/null || iptables -L -n 2>/dev/null | head -30"
```

### 6. Audit fail2ban

```bash
# Status fail2ban
ssh root@<IP> "fail2ban-client status 2>/dev/null && fail2ban-client status sshd 2>/dev/null"
```

### 7. Audit Mises a Jour

```bash
# Mises a jour de securite en attente
ssh root@<IP> "apt list --upgradable 2>/dev/null | grep -i security"

# Status unattended-upgrades
ssh root@<IP> "systemctl is-active unattended-upgrades 2>/dev/null; dpkg -l unattended-upgrades 2>/dev/null | tail -1"
```

### 8. Audit Docker (si applicable)

```bash
# Containers privilegies
ssh root@<IP> "docker ps -q | xargs docker inspect --format '{{.Name}}: privileged={{.HostConfig.Privileged}}' 2>/dev/null"

# Containers en root
ssh root@<IP> "docker ps -q | xargs docker inspect --format '{{.Name}}: user={{.Config.User}}' 2>/dev/null"

# Docker socket permissions
ssh root@<IP> "ls -la /var/run/docker.sock"
```

## Score de Securite

Calculer le score /100 selon les criteres du SKILL.md :

```
[SSH]        /20  Root desactive (5), password off (5), cles Ed25519 (5), MaxAuthTries<=3 (5)
[Firewall]   /15  Actif (5), deny default (5), regles minimales (5)
[Updates]    /15  Pas de CVE critiques (10), unattended-upgrades (5)
[fail2ban]   /10  Installe et actif (5), jail SSH (5)
[Docker]     /15  Non-root (5), pas privileged (5), scan recent (5)
[Credentials]/10  Pas de .env 644 (5), pas de secrets en clair (5)
[Logs]       /10  auth.log ok (5), rotation ok (5)
[Users]      /5   Pas de comptes inutiles (3), shells restreints (2)
━━━━━━━━━━━━━━━━
TOTAL        /100
```

## Format de Rapport

```
=== RAPPORT AUDIT SECURITE ===
Date: YYYY-MM-DD
Cible: [machine ou "all"]

--- Score Global: XX/100 ---

[CRITIQUE] Points critiques a corriger immediatement
[WARNING]  Points a ameliorer
[OK]       Points conformes

--- Detail par Machine ---
VM 100 (192.168.1.162): XX/100
  [OK] SSH: root desactive, password off
  [WARNING] fail2ban: non installe
  ...

--- Recommandations ---
1. [Priorite 1] ...
2. [Priorite 2] ...
```

## Options

| Option | Description |
|--------|-------------|
| `all` | Auditer toutes les machines |
| `vm100`, `vm103`, etc. | Auditer une VM specifique |
| `--category ssh\|firewall\|docker\|users\|updates` | Auditer une categorie uniquement |
| `--report` | Generer un rapport complet |

## Exemples

```bash
/sec-audit all                     # Audit complet de toute l'infra
/sec-audit vm100                   # Audit VM 100 uniquement
/sec-audit all --category ssh      # Audit SSH sur toutes les machines
/sec-audit proxmox --report        # Rapport complet Proxmox
```

## Voir Aussi

- `/sec-scan` - Scanner les vulnerabilites
- `/sec-harden` - Appliquer les corrections
- `/sec-wizard audit` - Audit guide interactif
