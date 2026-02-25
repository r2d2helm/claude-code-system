# Commande: /sec-users

Audit des comptes utilisateurs et permissions sur l'ensemble de l'infrastructure.

## Cible : $ARGUMENTS

Accepte : `all`, un nom de VM, `proxmox`, ou `windows`.

## Syntaxe

```
/sec-users [cible] [--check <type>]
```

## Processus

### 1. Lister les Utilisateurs Actifs

```bash
# Utilisateurs avec shell interactif (login possible)
ssh root@<IP> "awk -F: '\$7 !~ /nologin|false|sync/ {print \$1, \$3, \$6, \$7}' /etc/passwd"

# Derniere connexion
ssh root@<IP> "lastlog | grep -v 'Never logged in'"

# Utilisateurs connectes maintenant
ssh root@<IP> "who"

# Historique des connexions recentes
ssh root@<IP> "last -n 20"
```

### 2. Audit des Privileges

```bash
# Membres du groupe sudo/wheel
ssh root@<IP> "getent group sudo 2>/dev/null; getent group wheel 2>/dev/null"

# Membres du groupe docker (acces au daemon = quasi-root)
ssh root@<IP> "getent group docker 2>/dev/null"

# Regles sudoers
ssh root@<IP> "cat /etc/sudoers 2>/dev/null; ls -la /etc/sudoers.d/"

# NOPASSWD (risque)
ssh root@<IP> "grep -r 'NOPASSWD' /etc/sudoers /etc/sudoers.d/ 2>/dev/null"
```

### 3. Audit des Cles SSH

```bash
# Cles autorisees par utilisateur
ssh root@<IP> 'for home in /root /home/*; do
  user=$(basename "$home")
  akf="$home/.ssh/authorized_keys"
  if [ -f "$akf" ]; then
    count=$(wc -l < "$akf")
    echo "$user: $count cle(s)"
    cat "$akf" | awk "{print \"  - \" \$NF}"
  else
    echo "$user: aucune cle"
  fi
done'

# Permissions des repertoires .ssh
ssh root@<IP> 'find /home -name ".ssh" -exec ls -ld {} \; 2>/dev/null'
```

### 4. Comptes Service et Systeme

```bash
# Comptes systeme avec UID < 1000
ssh root@<IP> "awk -F: '\$3 < 1000 && \$3 != 0 {print \$1, \$3, \$7}' /etc/passwd"

# Comptes avec UID 0 (root equivalents) - DEVRAIT ETRE UNIQUE
ssh root@<IP> "awk -F: '\$3 == 0 {print \$1}' /etc/passwd"

# Comptes sans mot de passe
ssh root@<IP> "awk -F: '(\$2 == \"\" || \$2 == \"!\") {print \$1}' /etc/shadow 2>/dev/null"

# Comptes expires
ssh root@<IP> "awk -F: '\$8 != \"\" && \$8 < '$(date +%s)/86400' {print \$1, \"expire\"}' /etc/shadow 2>/dev/null"
```

### 5. Audit des Permissions Fichiers Utilisateur

```bash
# Home directories permissions
ssh root@<IP> "ls -la /home/"

# Fichiers .bashrc, .profile modifies recemment (backdoor potentielle)
ssh root@<IP> "find /home -name '.bashrc' -o -name '.profile' -o -name '.bash_profile' | xargs ls -la 2>/dev/null"

# Cron utilisateur
ssh root@<IP> 'for u in $(cut -f1 -d: /etc/passwd); do
  crontab_u=$(crontab -l -u "$u" 2>/dev/null)
  if [ -n "$crontab_u" ]; then
    echo "=== $u ==="
    echo "$crontab_u"
  fi
done'
```

### 6. Audit Windows (si applicable)

```powershell
# Comptes locaux
Get-LocalUser | Select-Object Name, Enabled, LastLogon, PasswordLastSet

# Membres du groupe Administrateurs
Get-LocalGroupMember -Group "Administrators"

# Comptes sans expiration de mot de passe
Get-LocalUser | Where-Object { $_.PasswordNeverExpires -eq $true } | Select-Object Name

# Sessions actives
query user
```

## Matrice des Comptes Attendus

| Machine | Utilisateur | UID | Groupes | Shell | Cle SSH |
|---------|-------------|-----|---------|-------|---------|
| VM 100 | root | 0 | root | /bin/bash | Oui |
| VM 103 | root | 0 | root | /bin/bash | Oui |
| VM 104 | r2d2helm | 1000 | sudo,docker | /bin/bash | Oui |
| VM 105 | r2d2helm | 1000 | sudo,docker | /bin/bash | Oui |
| Proxmox | root | 0 | root | /bin/bash | Oui |

Tout compte non present dans cette matrice est suspect.

## Format de Rapport

```
=== AUDIT UTILISATEURS ===

[CRITICAL] Comptes avec UID 0 supplementaires
[CRITICAL] Comptes sans mot de passe
[WARNING]  NOPASSWD dans sudoers
[WARNING]  Comptes avec shell non utilises
[INFO]     N utilisateurs actifs, M cles SSH

Par machine:
- VM 100: 2 comptes actifs (root, ubuntu) - OK
- VM 103: 1 compte actif (root) - OK
```

## Options

| Option | Description |
|--------|-------------|
| `--check privileges` | Audit sudo/groupes uniquement |
| `--check ssh-keys` | Audit cles SSH uniquement |
| `--check inactive` | Trouver les comptes inactifs |
| `--check service` | Audit des comptes service |

## Exemples

```bash
/sec-users all                        # Audit complet toutes machines
/sec-users vm100 --check ssh-keys     # Cles SSH VM 100
/sec-users all --check privileges     # Sudo/groupes partout
/sec-users windows                    # Audit Windows local
```

## Voir Aussi

- `/lx-users` - Gestion detaillee utilisateurs Linux
- `/win-users` - Gestion utilisateurs Windows
- `/sec-audit` - Audit incluant les utilisateurs
- `/sec-passwords` - Audit credentials
