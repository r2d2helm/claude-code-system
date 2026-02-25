# Commande: /bak-verify

Verifier l'integrite d'un backup.

## Syntaxe

```
/bak-verify [type] [cible]
```

## Verification par Type

### VM Proxmox (vzdump)

```bash
# Verifier l'integrite d'un fichier vzdump
ssh root@192.168.1.215 "vma verify /var/lib/vz/dump/vzdump-qemu-{vmid}-{date}.vma.zst"

# Lister le contenu d'un backup
ssh root@192.168.1.215 "vma list /var/lib/vz/dump/vzdump-qemu-{vmid}-{date}.vma.zst"

# Verifier le checksum
ssh root@192.168.1.215 "sha256sum /var/lib/vz/dump/vzdump-qemu-{vmid}-{date}.vma.zst"
```

### PostgreSQL (pg_dump)

```bash
# Verifier qu'un dump est lisible
ssh r2d2helm@192.168.1.164 "pg_restore -l {dumpfile}.dump > /dev/null && echo 'OK' || echo 'CORRUPTED'"

# Lister le contenu du dump
ssh r2d2helm@192.168.1.164 "pg_restore -l {dumpfile}.dump"

# Test de restauration dans une base temporaire
ssh r2d2helm@192.168.1.164 "createdb -U postgres test_restore && pg_restore -U postgres -d test_restore {dumpfile}.dump && dropdb -U postgres test_restore"
```

### Fichiers (checksum)

```bash
# Generer un checksum
sha256sum /mnt/nfs/backups/{file} > /mnt/nfs/backups/{file}.sha256

# Verifier un checksum existant
sha256sum -c /mnt/nfs/backups/{file}.sha256

# Comparer source et destination (rsync dry-run)
rsync -avnc /source/ /mnt/nfs/backups/rsync/{backup}/ | head -20
```

### Vault Obsidian (git)

```bash
# Verifier l'integrite du repo git
cd C:\Users\r2d2\Documents\Knowledge
git fsck --full

# Verifier le dernier commit
git log -1 --format="%H %ai %s"

# Comparer avec le remote
git fetch origin && git diff --stat HEAD origin/main
```

## Verification Globale

Script de verification de tous les backups :

```bash
echo "=== Verification Backups ==="
echo ""

# Derniers backups par type
echo "--- PostgreSQL ---"
ls -lt /mnt/nfs/backups/postgresql/ | head -3

echo "--- Proxmox ---"
ls -lt /var/lib/vz/dump/ | head -3

echo "--- rsync ---"
ls -lt /mnt/nfs/backups/rsync/ | head -3

echo "--- Espace disque ---"
df -h /mnt/nfs/backups/
```
