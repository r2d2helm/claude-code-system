# Wizard: Security Audit

Audit de securite complet guide pour l'infrastructure homelab.

## Questions

1. **Perimetre** : Quelle(s) machine(s) auditer ? (toutes, VM specifique, Windows)
2. **Profondeur** : Audit rapide (5 min) ou complet (30 min) ?
3. **Focus** : Domaine prioritaire ? (SSH, Docker, firewall, credentials, tout)

## Processus d'Audit Complet

### Phase 1 : SSH Hardening (/20 points)

```bash
# Verifier la config SSH
ssh {user}@{ip} "grep -E '^(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|MaxAuthTries|Protocol)' /etc/ssh/sshd_config"

# Scoring :
# PermitRootLogin no         = +5
# PasswordAuthentication no  = +5
# PubkeyAuthentication yes   = +5
# MaxAuthTries <= 3          = +3
# Protocol 2                 = +2
```

### Phase 2 : Firewall (/15 points)

```bash
# Verifier ufw
ssh {user}@{ip} "ufw status verbose"

# Scoring :
# ufw actif                  = +5
# Default deny incoming      = +5
# Regles minimales (<10)     = +5
```

### Phase 3 : Mises a Jour (/15 points)

```bash
# Verifier les updates en attente
ssh {user}@{ip} "apt list --upgradable 2>/dev/null | wc -l"

# Verifier unattended-upgrades
ssh {user}@{ip} "dpkg -l | grep unattended-upgrades"

# Scoring :
# Pas de CVE critiques       = +5
# unattended-upgrades actif  = +5
# < 10 packages en attente   = +5
```

### Phase 4 : fail2ban (/10 points)

```bash
# Verifier fail2ban
ssh {user}@{ip} "fail2ban-client status sshd 2>/dev/null || echo 'NOT INSTALLED'"

# Scoring :
# fail2ban installe          = +5
# Jail SSH active            = +5
```

### Phase 5 : Docker (/15 points)

```bash
# Containers privilegies
ssh {user}@{ip} "docker inspect --format '{{.Name}} privileged={{.HostConfig.Privileged}}' \$(docker ps -q)"

# Containers root
ssh {user}@{ip} "docker inspect --format '{{.Name}} user={{.Config.User}}' \$(docker ps -q)"

# Scoring :
# Pas de --privileged        = +5
# Non-root containers        = +5
# Images recentes (<30j)     = +5
```

### Phase 6 : Credentials (/10 points)

```bash
# Permissions .env
ssh {user}@{ip} "find /opt -name '.env' -perm /o+r -ls 2>/dev/null"

# Scoring :
# .env en 600                = +5
# Pas de secrets en clair    = +5
```

### Phase 7 : Logs (/10 points)

```bash
# auth.log accessible
ssh {user}@{ip} "ls -la /var/log/auth.log 2>/dev/null"

# logrotate actif
ssh {user}@{ip} "ls /etc/logrotate.d/"

# Scoring :
# Logs accessibles           = +5
# Rotation configuree        = +5
```

### Phase 8 : Users (/5 points)

```bash
# Comptes avec shell
ssh {user}@{ip} "grep -v '/nologin\|/false' /etc/passwd | grep -v '^#'"

# Scoring :
# Pas de comptes inutiles    = +5
```

## Rapport

Generer un rapport avec :
- Score total sur /100
- Points faibles identifies
- Actions correctives prioritaires
- Comparaison avec l'audit precedent (si disponible)
