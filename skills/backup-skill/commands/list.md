# Commande: /bak-list

Lister les backups disponibles par type, VM ou date.

## Syntaxe

```
/bak-list [type] [options]
```

## Lister par Type

### VM Proxmox

```bash
# Tous les backups vzdump
ssh root@192.168.1.215 "ls -lth /var/lib/vz/dump/vzdump-*.vma.zst"

# Backups d'une VM specifique
ssh root@192.168.1.215 "ls -lth /var/lib/vz/dump/vzdump-qemu-{vmid}-*"

# Via API Proxmox
ssh root@192.168.1.215 "pvesh get /nodes/proxmox/storage/local/content --content backup"

# Snapshots actifs d'une VM
ssh root@192.168.1.215 "qm listsnapshot {vmid}"
```

### PostgreSQL

```bash
# Tous les dumps
ssh r2d2helm@192.168.1.164 "ls -lth /mnt/nfs/backups/postgresql/"

# Dumps d'une base specifique
ssh r2d2helm@192.168.1.164 "ls -lth /mnt/nfs/backups/postgresql/pg-{dbname}-*"

# Avec taille totale
ssh r2d2helm@192.168.1.164 "du -sh /mnt/nfs/backups/postgresql/ && ls -lth /mnt/nfs/backups/postgresql/ | head -10"
```

### Fichiers rsync

```bash
# Repertoires rsync
ssh r2d2helm@192.168.1.164 "ls -lth /mnt/nfs/backups/rsync/"

# Avec tailles
ssh r2d2helm@192.168.1.164 "du -sh /mnt/nfs/backups/rsync/*"
```

### Docker Volumes

```bash
# Archives de volumes
ssh {user}@{ip} "ls -lth /mnt/nfs/backups/docker-volumes/"
```

### Vault Obsidian

```bash
# Historique git
cd C:\Users\r2d2\Documents\Knowledge
git log --oneline -20

# Tags de backup
git tag -l "backup-*"
```

## Dashboard Global

```bash
echo "==========================================="
echo "  BACKUP DASHBOARD - $(date +%Y-%m-%d)"
echo "==========================================="
echo ""

echo "--- Proxmox VMs ---"
ssh root@192.168.1.215 "ls -lt /var/lib/vz/dump/vzdump-*.vma.zst 2>/dev/null | head -5"
echo ""

echo "--- PostgreSQL ---"
ssh r2d2helm@192.168.1.164 "ls -lt /mnt/nfs/backups/postgresql/ 2>/dev/null | head -5"
echo ""

echo "--- rsync ---"
ssh r2d2helm@192.168.1.164 "ls -lt /mnt/nfs/backups/rsync/ 2>/dev/null | head -5"
echo ""

echo "--- Espace Total ---"
ssh r2d2helm@192.168.1.164 "du -sh /mnt/nfs/backups/* 2>/dev/null"
ssh r2d2helm@192.168.1.164 "df -h /mnt/nfs/backups/"
```
