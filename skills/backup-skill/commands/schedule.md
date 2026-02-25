# Commande: /bak-schedule

Gerer les planifications de backup (cron Linux, Task Scheduler Windows).

## Syntaxe

```
/bak-schedule [action] [options]
```

## Planifications Recommandees

| Type | Frequence | Heure | Machine |
|------|-----------|-------|---------|
| VM snapshots | Quotidien | 02:00 | Proxmox Host |
| pg_dump | Toutes les 6h | 00/06/12/18h | VM 104 |
| Vault git push | A chaque commit | - | PC Windows |
| rsync fichiers | Quotidien | 03:00 | VMs sources |
| Docker volumes | Hebdomadaire | Dimanche 04:00 | VMs Docker |
| Prune retention | Hebdomadaire | Dimanche 05:00 | VM 104 |

## Linux (cron)

```bash
# Editer le crontab
ssh {user}@{ip} "crontab -e"

# Backup PostgreSQL toutes les 6h
0 */6 * * * pg_dump -Fc -U postgres -h localhost {dbname} > /mnt/nfs/backups/postgresql/pg-{dbname}-$(date +\%Y-\%m-\%d_\%H\%M\%S).dump 2>> /var/log/backup-pg.log

# Backup rsync quotidien a 3h
0 3 * * * rsync -az --delete /data/ /mnt/nfs/backups/rsync/data-$(date +\%Y-\%m-\%d)/ >> /var/log/backup-rsync.log 2>&1

# Prune hebdomadaire dimanche 5h
0 5 * * 0 find /mnt/nfs/backups/postgresql/ -name "*.dump" -mtime +7 -delete >> /var/log/backup-prune.log 2>&1

# Lister les crontabs actifs
ssh {user}@{ip} "crontab -l"
```

## Proxmox (vzdump)

```bash
# Voir les jobs vzdump planifies
ssh root@192.168.1.215 "cat /etc/pve/vzdump.cron 2>/dev/null; pvesh get /cluster/backup"

# Creer un job de backup via API
ssh root@192.168.1.215 "pvesh create /cluster/backup --vmid {vmid} --storage local --schedule '0 2 * * *' --mode snapshot --compress zstd"
```

## Windows (Task Scheduler)

```powershell
# Creer une tache planifiee pour le vault
$Action = New-ScheduledTaskAction -Execute "git" -Argument "push" -WorkingDirectory "C:\Users\r2d2\Documents\Knowledge"
$Trigger = New-ScheduledTaskTrigger -Daily -At "22:00"
Register-ScheduledTask -TaskName "BackupVaultGit" -Action $Action -Trigger $Trigger -Description "Push vault Obsidian"

# Lister les taches de backup
Get-ScheduledTask | Where-Object { $_.TaskName -like "*Backup*" -or $_.TaskName -like "*Knowledge*" }

# Voir le statut
Get-ScheduledTaskInfo -TaskName "BackupVaultGit"
```

## Verification

```bash
# Verifier que les crons tournent (Linux)
ssh {user}@{ip} "grep -i backup /var/log/syslog | tail -10"

# Verifier les derniers backups
ls -lt /mnt/nfs/backups/{type}/ | head -5
```
