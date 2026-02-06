# Commande: /lx-disk

Gestion disques, LVM et montages.

## Syntaxe

```
/lx-disk [action]
```

## Actions

```bash
# Utilisation disque
df -h --type=ext4 --type=xfs --type=btrfs --type=tmpfs

# Blocs devices
lsblk -f

# Dossiers les plus gros
du -sh /* 2>/dev/null | sort -rh | head -10
du -sh /var/* 2>/dev/null | sort -rh | head -10

# LVM
sudo pvs    # Physical volumes
sudo vgs    # Volume groups
sudo lvs    # Logical volumes

# Montages
mount | column -t

# fstab
cat /etc/fstab

# SMART status
sudo smartctl -H /dev/sda 2>/dev/null

# I/O stats
iostat -x 1 3 2>/dev/null
```

## Exemples

```bash
/lx-disk                       # Vue d'ensemble
/lx-disk usage /var            # Espace dans /var
/lx-disk lvm                   # Status LVM
```
