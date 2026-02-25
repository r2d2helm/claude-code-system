# Commande: /devops-cron

Gerer les crontabs sur les VMs Linux.

## Syntaxe

```
/devops-cron [action] [vm]
```

## Lister

```bash
# Crontab utilisateur
ssh {user}@{ip} "crontab -l 2>/dev/null || echo 'No crontab'"

# Crontab root
ssh root@{ip} "crontab -l 2>/dev/null || echo 'No crontab'"

# Crons systeme
ssh root@{ip} "ls /etc/cron.d/ /etc/cron.daily/ /etc/cron.weekly/ /etc/cron.monthly/ 2>/dev/null"

# Toutes les VMs
for IP in 192.168.1.162 192.168.1.163 192.168.1.164 192.168.1.161; do
  echo "=== $IP ===" && ssh -o ConnectTimeout=3 root@$IP "crontab -l 2>/dev/null || echo 'empty'" && echo
done
```

## Ajouter

```bash
# Ajouter une ligne au crontab
ssh root@{ip} "(crontab -l 2>/dev/null; echo '{minute} {hour} {day} {month} {weekday} {command}') | crontab -"

# Exemples
# Toutes les heures
0 * * * * /opt/scripts/check.sh
# Tous les jours a 3h
0 3 * * * /opt/scripts/backup.sh
# Toutes les 6h
0 */6 * * * /opt/scripts/dump.sh
# Dimanche a 4h
0 4 * * 0 /opt/scripts/weekly.sh
```

## Supprimer

```bash
# Editer le crontab (supprimer la ligne)
ssh root@{ip} "crontab -l | grep -v '{pattern}' | crontab -"

# Supprimer tout le crontab
ssh root@{ip} "crontab -r"
```

## Syntaxe Cron

```
┌───────── minute (0-59)
│ ┌─────── hour (0-23)
│ │ ┌───── day of month (1-31)
│ │ │ ┌─── month (1-12)
│ │ │ │ ┌─ day of week (0-7, 0=Sun)
│ │ │ │ │
* * * * * command
```
