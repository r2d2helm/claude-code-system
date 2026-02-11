# Commande: /lx-backup

Backup rsync et tar pour serveurs Linux.

## Syntaxe

```
/lx-backup [action] [source] [destination] [options]
```

## Actions

### Backup avec rsync

```bash
# Backup local simple
rsync -avh --progress /source/ /backup/

# Backup vers serveur distant
rsync -avhz -e ssh /source/ user@remote:/backup/

# Backup incremental avec delete
rsync -avh --delete /source/ /backup/

# Exclure des fichiers
rsync -avh --exclude='*.log' --exclude='.cache' /source/ /backup/

# Dry-run (simulation)
rsync -avhn /source/ /backup/

# Avec bande passante limitee (5 MB/s)
rsync -avhz --bwlimit=5000 /source/ user@remote:/backup/
```

### Backup avec tar

```bash
# Creer une archive compressee
tar -czf backup-$(date +%Y%m%d).tar.gz /source/

# Avec exclusions
tar -czf backup.tar.gz --exclude='*.log' --exclude='.git' /source/

# Extraire
tar -xzf backup.tar.gz -C /destination/

# Lister le contenu
tar -tzf backup.tar.gz

# Backup incremental avec snapshot
tar -czf backup-full.tar.gz -g snapshot.snar /source/
tar -czf backup-incr.tar.gz -g snapshot.snar /source/
```

### Script de rotation

```bash
# Rotation des backups (garder N jours)
find /backup/ -name "backup-*.tar.gz" -mtime +30 -delete

# Verifier l'espace disponible avant backup
AVAIL=$(df -BG /backup | tail -1 | awk '{print $4}' | tr -d 'G')
if [ "$AVAIL" -lt 10 ]; then
  echo "WARN: Moins de 10G disponible pour le backup"
fi
```

### Crontab backup

```bash
# Backup quotidien a 2h du matin
0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1

# Backup hebdomadaire dimanche 3h
0 3 * * 0 rsync -avh --delete /data/ /backup/weekly/
```

## Options

| Option | Description |
|--------|-------------|
| `rsync` | Backup rsync (par defaut) |
| `tar` | Backup archive tar.gz |
| `--dry-run` | Simulation sans execution |
| `--exclude` | Patterns a exclure |
| `--rotate N` | Garder les N derniers backups |

## Exemples

```bash
/lx-backup rsync /var/www /backup/www       # Backup rsync
/lx-backup tar /etc backup-etc.tar.gz       # Archive /etc
/lx-backup rsync /data user@nas:/backup     # Backup distant
```

## Voir Aussi

- `/lx-cron` - Planifier des backups automatiques
- `/lx-disk` - Verifier l'espace disque
