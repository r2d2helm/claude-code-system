# Commande: /bak-restore

Restaurer depuis un backup existant.

## Syntaxe

```
/bak-restore [type] [cible] [options]
```

## Types de Restauration

### VM Proxmox (vzdump)

```bash
# Lister les backups disponibles
ssh root@192.168.1.215 "ls -la /var/lib/vz/dump/"

# Restaurer une VM
ssh root@192.168.1.215 "qmrestore /var/lib/vz/dump/vzdump-qemu-{vmid}-{date}.vma.zst {new_vmid}"

# Restaurer avec options
ssh root@192.168.1.215 "qmrestore /path/to/backup.vma.zst {vmid} --storage local-lvm --force"
```

### PostgreSQL

```bash
# Restaurer un dump format custom
ssh r2d2helm@192.168.1.164 "pg_restore -h localhost -U postgres -d {dbname} --clean --if-exists {dumpfile}.dump"

# Restaurer dans une nouvelle base
ssh r2d2helm@192.168.1.164 "createdb -U postgres {newdb} && pg_restore -h localhost -U postgres -d {newdb} {dumpfile}.dump"

# Restaurer un dump SQL
ssh r2d2helm@192.168.1.164 "gunzip -c {dumpfile}.sql.gz | psql -U postgres -d {dbname}"

# Restaurer une table specifique
ssh r2d2helm@192.168.1.164 "pg_restore -h localhost -U postgres -d {dbname} -t {tablename} {dumpfile}.dump"
```

### Fichiers (rsync)

```bash
# Restaurer depuis NFS
rsync -avz --progress r2d2helm@192.168.1.164:/mnt/nfs/backups/rsync/{source}-{date}/ /destination/

# Restaurer avec dry-run d'abord
rsync -avz --dry-run r2d2helm@192.168.1.164:/mnt/nfs/backups/rsync/{source}/ /destination/
```

### Vault Obsidian (git)

```bash
# Voir l'historique
cd C:\Users\r2d2\Documents\Knowledge
git log --oneline -20

# Restaurer un fichier specifique
git checkout {commit_hash} -- "chemin/vers/fichier.md"

# Restaurer tout le vault a une date
git checkout {commit_hash}
```

## Precautions

- **Toujours faire un backup avant de restaurer** (snapshot pre-restore)
- **Tester sur une copie** avant restauration en production
- **Verifier l'integrite** du backup avant restauration (`/bak-verify`)
- **Documenter** la raison et la date de la restauration
