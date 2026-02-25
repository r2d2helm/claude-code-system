# Commande: /devops-auto

Creer et gerer des taches automatisees.

## Syntaxe

```
/devops-auto [action] [options]
```

## Types d'Automatisation

### Scripts de Maintenance

```bash
# Script de maintenance quotidienne pour une VM
#!/bin/bash
set -euo pipefail
LOG=/var/log/maintenance.log

echo "=== Maintenance $(date) ===" >> $LOG

# Mises a jour
apt update && apt upgrade -y >> $LOG 2>&1

# Nettoyage Docker
docker system prune -f >> $LOG 2>&1

# Espace disque
df -h / >> $LOG

echo "=== Done ===" >> $LOG
```

### Watchers (surveillance continue)

```bash
# Verifier qu'un service tourne, redemarrer si down
#!/bin/bash
SERVICE=$1
if ! docker ps --format '{{.Names}}' | grep -q "$SERVICE"; then
  echo "$(date) - $SERVICE is down, restarting..." >> /var/log/watcher.log
  cd /opt/$SERVICE && docker compose up -d
  # Notifier
  curl -s -d "$SERVICE restarted on $(hostname)" http://192.168.1.162:8084/alerts
fi
```

### Taches Planifiees

```bash
# Lister les crontabs sur une VM
ssh root@{IP} "crontab -l"

# Ajouter une tache
ssh root@{IP} "echo '0 3 * * * /opt/scripts/maintenance.sh' | crontab -"
```

## Windows (Task Scheduler)

```powershell
# Lister les taches custom
Get-ScheduledTask | Where-Object { $_.TaskPath -eq '\' } | Format-Table TaskName, State, LastRunTime

# Creer une tache
$Action = New-ScheduledTaskAction -Execute "powershell" -Argument "-File C:\scripts\backup.ps1"
$Trigger = New-ScheduledTaskTrigger -Daily -At "02:00"
Register-ScheduledTask -TaskName "DailyBackup" -Action $Action -Trigger $Trigger
```
