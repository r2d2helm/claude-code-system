# Commande: /sec-logs

Analyser les logs de securite : tentatives de connexion, bans fail2ban, erreurs d'authentification, activite suspecte.

## Cible : $ARGUMENTS

Accepte : `all`, un nom de VM, ou un type de log (`auth`, `fail2ban`, `docker`, `syslog`).

## Syntaxe

```
/sec-logs [cible] [--type <type>] [--period <duree>] [--tail <N>]
```

## Processus

### 1. Logs d'Authentification

```bash
# Tentatives de connexion echouees
ssh root@<IP> "grep 'Failed password\|authentication failure' /var/log/auth.log | tail -20"

# Connexions reussies
ssh root@<IP> "grep 'Accepted' /var/log/auth.log | tail -20"

# Resume des echecs par IP
ssh root@<IP> "grep 'Failed password' /var/log/auth.log | awk '{print \$(NF-3)}' | sort | uniq -c | sort -rn | head -10"

# Tentatives root
ssh root@<IP> "grep 'Failed password for root' /var/log/auth.log | wc -l"

# Connexions SSH depuis des IPs non-LAN
ssh root@<IP> "grep 'Accepted' /var/log/auth.log | grep -v '192.168.1\.\|127.0.0.1' | tail -20"

# Via journalctl (alternative)
ssh root@<IP> "journalctl -u sshd --since '24 hours ago' --no-pager | grep -i 'failed\|error\|invalid'"
```

### 2. Logs fail2ban

```bash
# Status des jails
ssh root@<IP> "fail2ban-client status 2>/dev/null"

# Detail jail SSH
ssh root@<IP> "fail2ban-client status sshd 2>/dev/null"

# IPs actuellement bannies
ssh root@<IP> "fail2ban-client status sshd 2>/dev/null | grep 'Banned IP'"

# Historique des bans
ssh root@<IP> "grep 'Ban\|Unban' /var/log/fail2ban.log 2>/dev/null | tail -30"

# Top IPs bannies
ssh root@<IP> "grep 'Ban' /var/log/fail2ban.log 2>/dev/null | awk '{print \$NF}' | sort | uniq -c | sort -rn | head -10"
```

### 3. Logs Sudo

```bash
# Commandes sudo executees
ssh root@<IP> "grep 'sudo:' /var/log/auth.log | tail -20"

# Echecs sudo (tentative d'elevation non autorisee)
ssh root@<IP> "grep 'sudo:.*authentication failure\|NOT in sudoers' /var/log/auth.log | tail -10"
```

### 4. Logs Systeme Suspects

```bash
# Erreurs kernel/securite
ssh root@<IP> "dmesg | grep -i 'error\|denied\|segfault\|oom' | tail -20"

# Changements de compte
ssh root@<IP> "grep 'useradd\|userdel\|usermod\|groupadd\|passwd' /var/log/auth.log | tail -10"

# Services demarres/arretes recemment
ssh root@<IP> "journalctl --since '24 hours ago' --no-pager | grep -i 'started\|stopped\|failed' | tail -20"

# Connexions reseau suspectes
ssh root@<IP> "ss -tunap | grep ESTAB | grep -v '192.168.1\.\|127.0.0.1\|::1'"
```

### 5. Logs Docker (securite)

```bash
# Evenements Docker recents
ssh root@<IP> "docker events --since '24h' --until '0s' --filter 'type=container' 2>/dev/null | tail -30"

# Containers qui ont crash
ssh root@<IP> "docker ps -a --filter 'status=exited' --format '{{.Names}}: {{.Status}}' | head -10"

# Logs d'un container specifique
ssh root@<IP> "docker logs --since '24h' --tail 50 <container>"
```

### 6. Logs Proxmox

```bash
# Acces a l'interface web
ssh root@192.168.1.215 "grep 'login' /var/log/pveproxy/access.log | tail -20"

# Taches recentes
ssh root@192.168.1.215 "pvesh get /cluster/tasks --limit 10 --output-format json 2>/dev/null"

# Auth log Proxmox
ssh root@192.168.1.215 "grep 'authentication failure\|Accepted' /var/log/auth.log | tail -20"
```

### 7. Logs Windows (si applicable)

```powershell
# Echecs de connexion (Event ID 4625)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} -MaxEvents 20 |
  Select-Object TimeCreated, Message

# Connexions reussies (Event ID 4624)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624} -MaxEvents 10 |
  Select-Object TimeCreated, Message

# Modifications de comptes (Event ID 4720, 4722, 4725, 4726)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=@(4720,4722,4725,4726)} -MaxEvents 10 |
  Select-Object TimeCreated, Id, Message
```

## Format de Rapport

```
=== ANALYSE LOGS SECURITE ===
Periode: derniere 24h

[CRITICAL]
  - 0 connexions depuis des IPs non-LAN (OK)
  - 0 echecs sudo (OK)

[WARNING]
  - 15 tentatives SSH echouees (IPs: ...)
  - 3 IPs bannies par fail2ban

[INFO]
  - 42 connexions SSH reussies
  - 0 modifications de comptes
  - 2 containers redemarres

Top IPs echouees:
  12x - 192.168.1.xxx
  3x  - 10.0.0.xxx
```

## Options

| Option | Description |
|--------|-------------|
| `--type auth\|fail2ban\|sudo\|docker\|syslog\|all` | Type de logs |
| `--period 1h\|24h\|7d\|30d` | Periode d'analyse (defaut: 24h) |
| `--tail N` | Nombre de lignes (defaut: 20) |
| `--summary` | Resume uniquement (compteurs) |

## Exemples

```bash
/sec-logs all                              # Logs securite toutes machines
/sec-logs vm100 --type auth               # Auth.log VM 100
/sec-logs all --type fail2ban              # fail2ban toutes machines
/sec-logs vm103 --type docker --period 7d  # Logs Docker VM 103 (7 jours)
/sec-logs all --summary                    # Resume rapide
```

## Voir Aussi

- `/lx-logs` - Logs systeme detailles (journalctl)
- `/mon-logs` - Logs Docker via Dozzle
- `/sec-audit` - Audit incluant l'analyse des logs
