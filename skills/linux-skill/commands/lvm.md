# Commande: /lx-lvm

Gestion des volumes logiques LVM (Logical Volume Manager).

## Syntaxe

```
/lx-lvm [action] [options]
```

## Actions

### Afficher l'etat LVM

```bash
# Vue d'ensemble rapide
pvs    # Physical Volumes
vgs    # Volume Groups
lvs    # Logical Volumes

# Details complets
pvdisplay
vgdisplay
lvdisplay

# Espace disponible dans un VG
vgs --noheadings -o vg_name,vg_free
```

### Physical Volumes (PV)

```bash
# Creer un PV sur un disque
sudo pvcreate /dev/sdb

# Creer PV sur une partition
sudo pvcreate /dev/sdb1

# Informations PV
sudo pvdisplay /dev/sdb

# Supprimer un PV (doit etre vide)
sudo pvremove /dev/sdb
```

### Volume Groups (VG)

```bash
# Creer un VG
sudo vgcreate vg-data /dev/sdb /dev/sdc

# Etendre un VG avec un nouveau disque
sudo pvcreate /dev/sdd
sudo vgextend vg-data /dev/sdd

# Retirer un disque d'un VG (migrer les donnees d'abord)
sudo pvmove /dev/sdb
sudo vgreduce vg-data /dev/sdb

# Renommer un VG
sudo vgrename vg-data vg-storage
```

### Logical Volumes (LV)

```bash
# Creer un LV de 100G
sudo lvcreate -L 100G -n lv-www vg-data

# Creer un LV utilisant tout l'espace libre
sudo lvcreate -l 100%FREE -n lv-www vg-data

# Creer un LV utilisant 50% de l'espace libre
sudo lvcreate -l 50%FREE -n lv-data vg-data

# Formater le LV
sudo mkfs.ext4 /dev/vg-data/lv-www

# Monter le LV
sudo mkdir -p /var/www
sudo mount /dev/vg-data/lv-www /var/www

# Ajouter au fstab pour montage automatique
echo '/dev/vg-data/lv-www /var/www ext4 defaults 0 2' | sudo tee -a /etc/fstab
```

### Redimensionnement

```bash
# Etendre un LV de 50G
sudo lvextend -L +50G /dev/vg-data/lv-www

# Etendre et redimensionner le filesystem en une commande
sudo lvextend -L +50G --resizefs /dev/vg-data/lv-www

# Utiliser tout l'espace restant du VG
sudo lvextend -l +100%FREE --resizefs /dev/vg-data/lv-www

# Reduire un LV (ATTENTION: risque de perte de donnees)
# Demonter d'abord, verifier le filesystem
sudo umount /var/www
sudo e2fsck -f /dev/vg-data/lv-www
sudo lvreduce -L 50G --resizefs /dev/vg-data/lv-www
sudo mount /dev/vg-data/lv-www /var/www
```

### Snapshots LVM

```bash
# Creer un snapshot (reserve 10G pour les changements)
sudo lvcreate -L 10G -s -n lv-www-snap /dev/vg-data/lv-www

# Monter le snapshot en lecture seule
sudo mount -o ro /dev/vg-data/lv-www-snap /mnt/snapshot

# Restaurer depuis un snapshot
sudo umount /var/www
sudo lvconvert --merge /dev/vg-data/lv-www-snap

# Supprimer un snapshot
sudo lvremove /dev/vg-data/lv-www-snap
```

## Options

| Option | Description |
|--------|-------------|
| `status` | Vue d'ensemble PV/VG/LV |
| `extend` | Etendre un volume |
| `create` | Creer PV/VG/LV |
| `snapshot` | Gestion snapshots LVM |
| `--resize` | Redimensionner filesystem automatiquement |

## Exemples

```bash
/lx-lvm status                        # Vue d'ensemble LVM
/lx-lvm extend lv-www +50G            # Etendre de 50G
/lx-lvm create vg-data lv-app 200G    # Creer LV 200G
/lx-lvm snapshot lv-www               # Snapshot avant modification
```

## Voir Aussi

- `/lx-disk` - Gestion disques et partitions
- `/lx-backup` - Backup avant modification LVM
