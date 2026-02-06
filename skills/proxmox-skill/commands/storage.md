# /pve-storage - Gestion Stockage Proxmox

## Description
Gestion du stockage Proxmox : local, NFS, iSCSI, CIFS, GlusterFS, et PBS.
Pour ZFS et Ceph, voir `/pve-zfs` et `/pve-ceph`.

## Syntaxe
```
/pve-storage <action> [storage-id] [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `list` | `/pve-storage list` | Lister tous les storages |
| `status` | `/pve-storage status [id]` | État du stockage |
| `add` | `/pve-storage add <type>` | Ajouter stockage |
| `remove` | `/pve-storage remove <id>` | Supprimer stockage |
| `config` | `/pve-storage config <id>` | Configuration |
| `scan` | `/pve-storage scan <type>` | Scanner (iSCSI, NFS) |
| `content` | `/pve-storage content <id>` | Contenu du stockage |

## Types de Stockage Supportés

| Type | Description | Content |
|------|-------------|---------|
| `dir` | Répertoire local | images, iso, vztmpl, backup |
| `lvm` | LVM Volume Group | images, rootdir |
| `lvmthin` | LVM Thin Pool | images, rootdir |
| `zfspool` | ZFS Pool local | images, rootdir |
| `nfs` | NFS Share | images, iso, vztmpl, backup |
| `cifs` | CIFS/SMB Share | images, iso, vztmpl, backup |
| `glusterfs` | GlusterFS | images, iso, vztmpl, snippets |
| `iscsi` | iSCSI Target | images |
| `iscsidirect` | iSCSI (libiscsi) | images |
| `rbd` | Ceph RBD | images, rootdir |
| `cephfs` | Ceph Filesystem | iso, vztmpl, backup, snippets |
| `pbs` | Proxmox Backup Server | backup |

## Affichage Status

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║  💾 STORAGE STATUS                                                               ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  ┌─────────────┬──────────┬────────────────┬────────────┬──────────────────────┐║
║  │ Storage     │ Type     │ Usage          │ Available  │ Status               │║
║  ├─────────────┼──────────┼────────────────┼────────────┼──────────────────────┤║
║  │ local       │ dir      │ 45% (90/200G)  │ 110 GB     │ 🟢 Active            │║
║  │ local-lvm   │ lvmthin  │ 62% (310/500G) │ 190 GB     │ 🟢 Active            │║
║  │ local-zfs   │ zfspool  │ 38% (1.9/5.0T) │ 3.1 TB     │ 🟢 ONLINE            │║
║  │ nfs-backup  │ nfs      │ 55% (5.5/10T)  │ 4.5 TB     │ 🟢 Mounted           │║
║  │ pbs-main    │ pbs      │ 48% (4.8/10T)  │ 5.2 TB     │ 🟢 Connected         │║
║  │ ceph-pool   │ rbd      │ 32% (16/50T)   │ 34 TB      │ 🟢 HEALTH_OK         │║
║  │ iscsi-san   │ iscsi    │ 71% (7.1/10T)  │ 2.9 TB     │ 🟢 Connected         │║
║  └─────────────┴──────────┴────────────────┴────────────┴──────────────────────┘║
║                                                                                  ║
║  📊 Total: 7 storages | 85.7 TB total | 50.9 TB available                       ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

## Commandes Bash

### Lister et Status

```bash
# Lister tous les storages
pvesm status

# Status JSON détaillé
pvesh get /storage --output-format=json-pretty

# Status d'un storage spécifique
pvesm status --storage local-zfs

# Contenu d'un storage
pvesm list local
pvesm list local --content iso
pvesm list local --content vztmpl
```

### Stockage Local (Directory)

```bash
# Ajouter stockage directory
pvesm add dir backup-dir \
  --path /mnt/backup \
  --content backup,iso,vztmpl \
  --shared 0

# Configuration
pvesm set backup-dir --disable 0 --maxfiles 5

# Vérifier montage
ls -la /mnt/backup
```

### NFS

```bash
# Scanner exports NFS
pvesm nfsscan 192.168.1.100

# Ajouter NFS
pvesm add nfs nfs-data \
  --server 192.168.1.100 \
  --export /export/proxmox \
  --path /mnt/pve/nfs-data \
  --content images,iso,vztmpl,backup \
  --options vers=4.2,soft,timeo=150

# NFS avec Kerberos
pvesm add nfs nfs-secure \
  --server 192.168.1.100 \
  --export /export/secure \
  --content images,backup \
  --options sec=krb5p
```

### CIFS/SMB

```bash
# Scanner shares CIFS
pvesm cifsscan 192.168.1.100 --username admin

# Ajouter CIFS
pvesm add cifs smb-backup \
  --server 192.168.1.100 \
  --share backup \
  --path /mnt/pve/smb-backup \
  --username backup-user \
  --password "SecurePassword" \
  --content backup,iso \
  --domain MYDOMAIN

# CIFS avec version spécifique
pvesm add cifs smb-legacy \
  --server 192.168.1.200 \
  --share data \
  --content images \
  --smbversion 2.1
```

### iSCSI

```bash
# Scanner targets iSCSI
pvesm iscsiscan --portal 192.168.1.50

# Ajouter iSCSI
pvesm add iscsi iscsi-san \
  --portal 192.168.1.50 \
  --target iqn.2024-01.com.storage:lun1 \
  --content images

# iSCSI avec CHAP
pvesm add iscsi iscsi-secure \
  --portal 192.168.1.50 \
  --target iqn.2024-01.com.storage:lun2 \
  --content images \
  --username initiator-user \
  --password "chap-secret"

# LVM sur iSCSI (courant en entreprise)
# 1. Ajouter target iSCSI
pvesm add iscsi iscsi-base --portal 192.168.1.50 --target iqn...

# 2. Créer VG sur LUN iSCSI
pvcreate /dev/sdb
vgcreate vg-iscsi /dev/sdb

# 3. Ajouter LVM thin sur iSCSI
lvcreate -L 900G -T vg-iscsi/thin-pool
pvesm add lvmthin iscsi-thin \
  --vgname vg-iscsi \
  --thinpool thin-pool \
  --content images,rootdir
```

### Proxmox Backup Server (PBS)

```bash
# Ajouter datastore PBS
pvesm add pbs pbs-main \
  --server 192.168.1.60 \
  --datastore main \
  --username backup@pbs \
  --password "PBSPassword" \
  --fingerprint "AA:BB:CC:DD:..." \
  --content backup

# PBS avec encryption key
pvesm add pbs pbs-encrypted \
  --server 192.168.1.60 \
  --datastore encrypted \
  --username backup@pbs \
  --password "PBSPassword" \
  --fingerprint "AA:BB:CC:DD:..." \
  --encryption-key /etc/pve/priv/pbs-encryption.key \
  --content backup

# Générer clé encryption
proxmox-backup-client key create /etc/pve/priv/pbs-encryption.key

# Vérifier connexion PBS
pvesm status --storage pbs-main
```

### LVM et LVM-Thin

```bash
# Lister VGs disponibles
vgs

# Ajouter LVM classique
pvesm add lvm local-lvm \
  --vgname pve \
  --content images,rootdir

# Créer LVM thin pool
lvcreate -L 400G -T pve/data

# Ajouter LVM thin
pvesm add lvmthin local-thin \
  --vgname pve \
  --thinpool data \
  --content images,rootdir

# Étendre thin pool
lvextend -L +100G pve/data
lvextend -l +100%FREE pve/data_tmeta  # Si metadata plein
```

### GlusterFS

```bash
# Ajouter GlusterFS
pvesm add glusterfs gluster-vol \
  --server 192.168.1.70 \
  --server2 192.168.1.71 \
  --volume gv0 \
  --content images,iso,vztmpl \
  --transport tcp
```

## Configuration Avancée

```bash
# Modifier storage existant
pvesm set local-zfs --content images,rootdir,iso

# Désactiver storage temporairement
pvesm set nfs-data --disable 1

# Réactiver
pvesm set nfs-data --disable 0

# Définir limites
pvesm set local --maxfiles 3  # Max backups par VM

# Supprimer storage
pvesm remove old-storage

# Shared storage (cluster)
pvesm set ceph-pool --shared 1
```

## Wizard : Ajout Stockage

```
/pve-storage add --wizard
```

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  🧙 WIZARD: AJOUT STOCKAGE                                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Étape 1/4: TYPE DE STOCKAGE                                                 ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Type:                                                                       ║
║    [1] Directory (local)                                                     ║
║    [2] NFS Share                                                             ║
║    [3] CIFS/SMB Share                                                        ║
║    [4] iSCSI Target                                                          ║
║    [5] LVM Volume Group                                                      ║
║    [6] LVM-Thin Pool                                                         ║
║    [7] ZFS Pool             → Voir /pve-zfs                                  ║
║    [8] Ceph RBD             → Voir /pve-ceph                                 ║
║    [9] Proxmox Backup Server                                                 ║
║  Choix:              > 2                                                     ║
║                                                                              ║
║  Étape 2/4: CONFIGURATION NFS                                                ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Storage ID:         > nfs-backup                                            ║
║  Server:             > 192.168.1.100                                         ║
║                                                                              ║
║  Scanning NFS exports...                                                     ║
║  Exports disponibles:                                                        ║
║    [1] /export/backup                                                        ║
║    [2] /export/iso                                                           ║
║    [3] /export/data                                                          ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Étape 3/4: CONTENU                                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Types de contenu (multi-select):                                            ║
║    [x] Disk images (VM disks)                                                ║
║    [x] ISO images                                                            ║
║    [x] Container templates                                                   ║
║    [x] VZDump backups                                                        ║
║    [ ] Snippets                                                              ║
║                                                                              ║
║  Étape 4/4: OPTIONS                                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  NFS Version:                                                                ║
║    [1] Auto-detect         ← Recommandé                                      ║
║    [2] NFSv4.2                                                               ║
║    [3] NFSv4.1                                                               ║
║    [4] NFSv3                                                                 ║
║  Choix:              > 2                                                     ║
║                                                                              ║
║  Max backups per VM [3]: > 5                                                 ║
║  Shared (cluster):   [Y/n] > Y                                               ║
║  Enable now:         [Y/n] > Y                                               ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  📋 RÉSUMÉ                                                                   ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  ID: nfs-backup                                                              ║
║  Type: NFS                                                                   ║
║  Server: 192.168.1.100                                                       ║
║  Export: /export/backup                                                      ║
║  Content: images, iso, vztmpl, backup                                        ║
║  Options: vers=4.2, shared=1, maxfiles=5                                     ║
║                                                                              ║
║  Confirmer? [Y/n] > Y                                                        ║
║                                                                              ║
║  ✅ Storage nfs-backup ajouté avec succès!                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Content Types

| Type | Description | Stockages compatibles |
|------|-------------|----------------------|
| `images` | Disques VM/CT | Tous sauf PBS |
| `rootdir` | Rootfs CT | dir, lvm, lvmthin, zfs, rbd |
| `iso` | Images ISO | dir, nfs, cifs, cephfs |
| `vztmpl` | Templates CT | dir, nfs, cifs, cephfs |
| `backup` | Backups vzdump | dir, nfs, cifs, cephfs, pbs |
| `snippets` | Fichiers config | dir, nfs, cifs, cephfs, glusterfs |

## Voir Aussi
- `/pve-zfs` - Administration ZFS
- `/pve-ceph` - Administration Ceph
- `/pve-backup` - Backup et PBS
