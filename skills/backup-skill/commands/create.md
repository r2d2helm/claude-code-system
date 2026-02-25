---
name: bak-create
description: Creer un backup selon le type choisi
---

# /bak-create - Creer un Backup

## Syntaxe

```
/bak-create <type> [cible] [options]
```

## Types de backup

| Type | Cible | Methode |
|------|-------|---------|
| `vm-snapshot` | VMID (100, 103, 104, 105) | vzdump snapshot via Proxmox |
| `pg-dump` | nom de base ou "all" | pg_dump --format=custom |
| `files-rsync` | chemin source | rsync incremental vers NFS |
| `vault-git` | - | git commit + push du vault Obsidian |
| `docker-vol` | container:volume | docker cp + tar |
| `config` | - | copie config Claude Code |

## Processus par type

### vm-snapshot

```bash
# Snapshot rapide (sans memoire)
ssh root@192.168.1.215 "qm snapshot {vmid} bak-$(date +%Y%m%d-%H%M) --description 'Backup manuel $(date +%Y-%m-%d)'"

# Snapshot avec etat memoire (VM en cours)
ssh root@192.168.1.215 "qm snapshot {vmid} bak-$(date +%Y%m%d-%H%M) --vmstate 1 --description 'Backup complet $(date +%Y-%m-%d)'"

# vzdump complet vers stockage
ssh root@192.168.1.215 "vzdump {vmid} --mode snapshot --compress zstd --notes 'Backup manuel'"

# vzdump vers NFS
ssh root@192.168.1.215 "vzdump {vmid} --mode snapshot --compress zstd --storage nfs-backup"
```

### pg-dump

```bash
# Dump une base (format custom, compresse)
ssh r2d2helm@192.168.1.164 "docker exec postgres-shared pg_dump -U postgres -Fc {dbname} > /mnt/nfs/backups/postgresql/pg-{dbname}-$(date +%Y-%m-%d_%H%M%S).dump"

# Dump toutes les bases
ssh r2d2helm@192.168.1.164 "docker exec postgres-shared pg_dumpall -U postgres | gzip > /mnt/nfs/backups/postgresql/pg-all-$(date +%Y-%m-%d_%H%M%S).sql.gz"

# Dump avec exclusion de tables temporaires
ssh r2d2helm@192.168.1.164 "docker exec postgres-shared pg_dump -U postgres -Fc --exclude-table-data='*_temp*' {dbname} > /mnt/nfs/backups/postgresql/pg-{dbname}-$(date +%Y-%m-%d_%H%M%S).dump"
```

### files-rsync

```bash
# Rsync incremental avec hardlinks
ssh r2d2helm@192.168.1.164 "rsync -avz --delete --link-dest=/mnt/nfs/backups/rsync/{source}-latest {user}@{source_ip}:{source_path}/ /mnt/nfs/backups/rsync/{source}-$(date +%Y-%m-%d)/"

# Mettre a jour le lien "latest"
ssh r2d2helm@192.168.1.164 "ln -sfn /mnt/nfs/backups/rsync/{source}-$(date +%Y-%m-%d) /mnt/nfs/backups/rsync/{source}-latest"
```

### vault-git

```bash
# Depuis Windows (PowerShell)
cd C:\Users\r2d2\Documents\Knowledge
git add -A
git commit -m "backup: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin main

# Verification
git log --oneline -3
git status
```

### docker-vol

```bash
# Exporter un volume Docker
ssh {user}@{vm_ip} "docker run --rm -v {volume}:/data -v /mnt/nfs/backups/docker-volumes:/backup alpine tar czf /backup/docker-vol-{container}-{volume}-$(date +%Y-%m-%d).tar.gz -C /data ."

# Alternative avec docker cp
ssh {user}@{vm_ip} "docker cp {container}:{path} /tmp/backup-tmp && tar czf /mnt/nfs/backups/docker-volumes/docker-vol-{container}-$(date +%Y-%m-%d).tar.gz -C /tmp/backup-tmp . && rm -rf /tmp/backup-tmp"
```

### config

```bash
# Backup config Claude Code (depuis Windows)
robocopy "C:\Users\r2d2\.claude" "C:\Users\r2d2\Documents\claude-config-backup" /MIR /XD "hooks\logs" "hooks\data" ".git" /XF "*.log" "*.jsonl"

# Rsync vers VM 104 (optionnel)
rsync -avz "C:\Users\r2d2\Documents\claude-config-backup/" r2d2helm@192.168.1.164:/mnt/nfs/backups/config/claude-code/
```

## Exemples

```
/bak-create vm-snapshot 103           # Snapshot VM 103
/bak-create vm-snapshot all           # Snapshot toutes les VMs
/bak-create pg-dump taskyn            # Dump base taskyn
/bak-create pg-dump all               # Dump toutes les bases
/bak-create files-rsync /etc          # Rsync du /etc
/bak-create vault-git                 # Commit + push vault
/bak-create docker-vol postgres-shared pgdata  # Backup volume PostgreSQL
/bak-create config                    # Backup config Claude Code
```

## Notes

- Toujours verifier l'espace disque avant un backup volumineux (`/bak-status disk`)
- Les snapshots Proxmox sont quasi-instantanes sur ZFS
- Preferer `--format=custom` pour pg_dump (compression + restauration selective)
- rsync avec `--link-dest` economise l'espace pour les backups incrementaux
