# 🔄 /pve-restore - Restauration VMs & CTs

## Description
Restauration de VMs et conteneurs depuis backups (vzdump, PBS) Proxmox VE 9+.

## Syntaxe
```
/pve-restore [action] [options]
```

## Lister les Backups Disponibles

### Backups locaux (vzdump)
```bash
# Lister sur storage
pvesm list backup --content backup

# Filtrer par VMID
ls -la /var/lib/vz/dump/ | grep "vzdump-qemu-100"

# Détails backup
vzdump-info /var/lib/vz/dump/vzdump-qemu-100-2025_02_03-10_00_00.vma.zst
```

### Backups PBS
```bash
# Via proxmox-backup-client
proxmox-backup-client list --repository user@pbs:datastore

# Via API
pvesh get /nodes/{node}/storage/{pbs-storage}/content --content backup

# Snapshots d'un guest
proxmox-backup-client snapshot list vm/100 --repository user@pbs:datastore
```

## Restauration VM (QEMU)

### Depuis vzdump local
```bash
# Restauration simple
qmrestore /var/lib/vz/dump/vzdump-qemu-100-2025_02_03-10_00_00.vma.zst 100

# Vers nouveau VMID
qmrestore /var/lib/vz/dump/vzdump-qemu-100-*.vma.zst 200 --unique

# Vers storage différent
qmrestore /var/lib/vz/dump/vzdump-qemu-100-*.vma.zst 100 --storage local-lvm

# Avec options
qmrestore /var/lib/vz/dump/vzdump-qemu-100-*.vma.zst 100 \
  --storage local-lvm \
  --unique \
  --force \
  --bwlimit 50000  # KB/s
```

### Depuis PBS
```bash
# Via Web UI: Storage > PBS > Content > Restore

# Via CLI
qmrestore "pbs-storage:backup/vm/100/2025-02-03T10:00:00Z" 100

# Avec options
qmrestore "pbs-storage:backup/vm/100/2025-02-03T10:00:00Z" 200 \
  --storage local-lvm \
  --unique \
  --pool production
```

### Options qmrestore
| Option | Description |
|--------|-------------|
| `--storage` | Storage cible pour disques |
| `--unique` | Générer nouveaux UUIDs/MAC |
| `--force` | Écraser VM existante |
| `--bwlimit` | Limite bande passante (KB/s) |
| `--pool` | Pool de destination |
| `--start` | Démarrer après restore |

## Restauration Conteneur (LXC)

### Depuis vzdump local
```bash
# Restauration simple
pct restore 200 /var/lib/vz/dump/vzdump-lxc-200-2025_02_03-10_00_00.tar.zst

# Vers nouveau CTID
pct restore 300 /var/lib/vz/dump/vzdump-lxc-200-*.tar.zst --unique

# Avec options
pct restore 200 /var/lib/vz/dump/vzdump-lxc-200-*.tar.zst \
  --storage local-lvm \
  --rootfs local-lvm:8 \
  --unique \
  --unprivileged 1
```

### Depuis PBS
```bash
pct restore 200 "pbs-storage:backup/ct/200/2025-02-03T10:00:00Z"

# Avec options
pct restore 300 "pbs-storage:backup/ct/200/2025-02-03T10:00:00Z" \
  --storage local-lvm \
  --unique \
  --hostname "restored-ct"
```

### Options pct restore
| Option | Description |
|--------|-------------|
| `--storage` | Storage cible |
| `--rootfs` | Config rootfs explicite |
| `--unique` | Générer nouveau hostname/MAC |
| `--unprivileged` | Forcer mode unprivileged |
| `--hostname` | Nouveau hostname |
| `--pool` | Pool de destination |
| `--force` | Écraser CT existant |

## File-Level Restore (PBS)

### Monter backup pour exploration
```bash
# Monter snapshot PBS
proxmox-backup-client mount \
  vm/100/2025-02-03T10:00:00Z \
  /mnt/restore \
  --repository user@pbs:datastore

# Explorer
ls /mnt/restore/
cd /mnt/restore/drive-scsi0/

# Copier fichiers spécifiques
cp /mnt/restore/drive-scsi0/etc/nginx/nginx.conf /tmp/

# Démonter
fusermount -u /mnt/restore
```

### Via Web UI PBS
1. Storage > PBS > Content
2. Sélectionner backup
3. File Restore
4. Naviguer et télécharger fichiers

## Live Restore (PBS)

### Restauration avec démarrage immédiat
```bash
# Commence à démarrer pendant que les données sont encore en cours de restauration
qmrestore "pbs-storage:backup/vm/100/2025-02-03T10:00:00Z" 100 --live-restore
```

## Restauration Sélective

### Restaurer uniquement certains disques
```bash
# Voir contenu backup
vzdump-info /path/to/backup.vma.zst

# Extraire un disque spécifique
vma extract /path/to/backup.vma.zst /tmp/extracted/ -v

# Importer manuellement
qm importdisk 100 /tmp/extracted/disk-drive-scsi0.raw local-lvm
```

### Restaurer config uniquement
```bash
# Extraire config
vzdump-info --config /path/to/backup.vma.zst > /tmp/vm-config

# Ou depuis PBS
proxmox-backup-client restore vm/100/2025-02-03T10:00:00Z qemu-server.conf /tmp/ \
  --repository user@pbs:datastore
```

## Vérification et Test

### Test de restauration (dry-run)
```bash
# Pas de dry-run natif, mais on peut:
# 1. Restaurer vers VMID temporaire
qmrestore backup.vma.zst 9999 --unique --storage local-lvm

# 2. Vérifier
qm status 9999
qm config 9999

# 3. Optionnel: démarrer et tester
qm start 9999

# 4. Nettoyer
qm stop 9999
qm destroy 9999
```

### Vérification PBS
```bash
# Vérifier intégrité backup
proxmox-backup-client verify vm/100/2025-02-03T10:00:00Z \
  --repository user@pbs:datastore

# Job de vérification automatique
# Via Web UI: PBS > Datastore > Verify Jobs
```

## Disaster Recovery

### Restauration cluster complet
```bash
# 1. Installer Proxmox frais
# 2. Configurer PBS storage
pvesm add pbs pbs-restore \
  --server pbs.example.com \
  --username restore@pbs \
  --datastore main \
  --fingerprint AA:BB:CC:...

# 3. Lister backups disponibles
pvesh get /nodes/{node}/storage/pbs-restore/content

# 4. Restaurer VMs critiques en priorité
for vmid in 100 101 102; do
    qmrestore "pbs-restore:backup/vm/$vmid/latest" $vmid --storage local-lvm
done

# 5. Restaurer CTs
for ctid in 200 201; do
    pct restore $ctid "pbs-restore:backup/ct/$ctid/latest" --storage local-lvm
done
```

### Script DR automatisé
```bash
#!/bin/bash
# dr-restore.sh - Disaster Recovery Script

PBS_STORAGE="pbs-restore"
TARGET_STORAGE="local-lvm"

# VMs critiques à restaurer
CRITICAL_VMS="100 101 102"
CRITICAL_CTS="200 201"

echo "Starting Disaster Recovery restore..."

# Restaurer VMs
for vmid in $CRITICAL_VMS; do
    echo "Restoring VM $vmid..."
    qmrestore "${PBS_STORAGE}:backup/vm/${vmid}/latest" $vmid \
      --storage $TARGET_STORAGE \
      --force 2>&1 || echo "Failed to restore VM $vmid"
done

# Restaurer CTs
for ctid in $CRITICAL_CTS; do
    echo "Restoring CT $ctid..."
    pct restore $ctid "${PBS_STORAGE}:backup/ct/${ctid}/latest" \
      --storage $TARGET_STORAGE \
      --force 2>&1 || echo "Failed to restore CT $ctid"
done

echo "DR restore completed."
```

## Troubleshooting Restore

### Erreurs courantes
```bash
# "VM already exists"
qmrestore backup.vma.zst 100 --force
# Ou restaurer vers nouveau VMID

# "Storage does not support content type"
pvesm set local-lvm --content images,rootdir

# "Backup file not found"
# Vérifier le chemin exact
ls -la /var/lib/vz/dump/

# "Insufficient disk space"
df -h
pvesm status

# PBS "certificate verification failed"
proxmox-backup-client login --repository user@pbs:datastore
```

### Logs restauration
```bash
# Logs en temps réel
journalctl -f | grep -i restore

# Logs vzdump
cat /var/log/vzdump/*.log
```

## Best Practices

1. **Tester régulièrement**: Restauration mensuelle vers VM test
2. **Documenter**: VMID, storage source, procédures
3. **RTO/RPO**: Définir objectifs temps de récupération
4. **Priorités**: Lister VMs critiques pour DR
5. **Vérification PBS**: Jobs de vérification hebdomadaires
6. **Unique**: Toujours utiliser --unique pour éviter conflits
