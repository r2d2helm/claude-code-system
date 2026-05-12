# /pve-zfs - Administration ZFS

## Description
Administration complete ZFS sur Proxmox VE : pools, datasets, snapshots,
replication, et RAIDZ expansion (ZFS 2.3+ / PVE 9+).

## Syntaxe
```
/pve-zfs <action> [pool/dataset] [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `status` | `/pve-zfs status [pool]` | Etat des pools ZFS |
| `create` | `/pve-zfs create <pool>` | Creer pool |
| `destroy` | `/pve-zfs destroy <pool>` | Supprimer pool |
| `expand` | `/pve-zfs expand <pool>` | RAIDZ expansion (PVE 9+) |
| `scrub` | `/pve-zfs scrub <pool>` | Lancer scrub |
| `snapshot` | `/pve-zfs snapshot` | Gerer snapshots |
| `replicate` | `/pve-zfs replicate` | Replication ZFS |
| `send` | `/pve-zfs send` | Envoyer snapshot |
| `receive` | `/pve-zfs receive` | Recevoir snapshot |
| `properties` | `/pve-zfs properties <ds>` | Proprietes dataset |

## Affichage Status

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║  🗄️ ZFS POOLS STATUS                                                            ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  ┌─ POOL: rpool ─────────────────────────────────────────────────────────────┐  ║
║  │ Status: 🟢 ONLINE    Health: HEALTHY    Scrub: 2d ago (no errors)        │  ║
║  │ Size: 447 GB         Used: 245 GB (55%)        Free: 202 GB              │  ║
║  │                                                                           │  ║
║  │ Configuration:                                                            │  ║
║  │   rpool                                   ONLINE                          │  ║
║  │     mirror-0                              ONLINE                          │  ║
║  │       /dev/disk/by-id/nvme-Samsung_1      ONLINE                          │  ║
║  │       /dev/disk/by-id/nvme-Samsung_2      ONLINE                          │  ║
║  │                                                                           │  ║
║  │ Properties: compression=lz4, atime=off, recordsize=128K                   │  ║
║  └───────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                  ║
║  ┌─ POOL: tank ──────────────────────────────────────────────────────────────┐  ║
║  │ Status: 🟢 ONLINE    Health: HEALTHY    Scrub: 5d ago (no errors)        │  ║
║  │ Size: 10.9 TB        Used: 4.2 TB (38%)        Free: 6.7 TB              │  ║
║  │                                                                           │  ║
║  │ Configuration:                                                            │  ║
║  │   tank                                    ONLINE                          │  ║
║  │     raidz2-0                              ONLINE                          │  ║
║  │       /dev/disk/by-id/scsi-ST4000_1       ONLINE                          │  ║
║  │       /dev/disk/by-id/scsi-ST4000_2       ONLINE                          │  ║
║  │       /dev/disk/by-id/scsi-ST4000_3       ONLINE                          │  ║
║  │       /dev/disk/by-id/scsi-ST4000_4       ONLINE                          │  ║
║  │       /dev/disk/by-id/scsi-ST4000_5       ONLINE                          │  ║
║  │       /dev/disk/by-id/scsi-ST4000_6       ONLINE                          │  ║
║  │     special                               ONLINE                          │  ║
║  │       mirror-1                            ONLINE                          │  ║
║  │         /dev/disk/by-id/nvme-Intel_1      ONLINE                          │  ║
║  │         /dev/disk/by-id/nvme-Intel_2      ONLINE                          │  ║
║  │                                                                           │  ║
║  │ Properties: compression=lz4, atime=off, special_small_blocks=32K         │  ║
║  └───────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

## Commandes Bash

### Status et Information

```bash
# Status tous pools
zpool status

# Status pool spécifique
zpool status tank

# Liste pools avec usage
zpool list

# Liste datasets
zfs list

# Liste datasets avec snapshots
zfs list -t all

# I/O stats
zpool iostat -v tank 5

# Historique commandes
zpool history tank
```

### Creation de Pools - Best Practices 2025-2026

```bash
# ═══════════════════════════════════════════════════════════════════════════
# CRÉATION POOL - BEST PRACTICES
# ═══════════════════════════════════════════════════════════════════════════

# Mirror (2 disques) - Petit setup, haute performance
zpool create -o ashift=12 \
  -O compression=lz4 \
  -O atime=off \
  -O xattr=sa \
  -O acltype=posixacl \
  tank mirror \
  /dev/disk/by-id/scsi-disk1 \
  /dev/disk/by-id/scsi-disk2

# RAIDZ1 (3+ disques) - Dev/Test seulement
zpool create -o ashift=12 \
  -O compression=lz4 \
  -O atime=off \
  tank raidz1 \
  /dev/disk/by-id/scsi-disk{1,2,3,4}

# RAIDZ2 (6+ disques) - Production recommandé
zpool create -o ashift=12 \
  -O compression=lz4 \
  -O atime=off \
  -O xattr=sa \
  -O acltype=posixacl \
  tank raidz2 \
  /dev/disk/by-id/scsi-disk{1,2,3,4,5,6}

# RAIDZ3 (8+ disques) - Haute redondance
zpool create -o ashift=12 \
  -O compression=lz4 \
  -O atime=off \
  tank raidz3 \
  /dev/disk/by-id/scsi-disk{1,2,3,4,5,6,7,8}

# Pool avec Special VDEV (metadata sur SSD)
zpool create -o ashift=12 \
  -O compression=lz4 \
  -O atime=off \
  -O special_small_blocks=32K \
  tank raidz2 \
  /dev/disk/by-id/scsi-hdd{1,2,3,4,5,6} \
  special mirror \
  /dev/disk/by-id/nvme-ssd1 \
  /dev/disk/by-id/nvme-ssd2

# ══ BEST PRACTICES ZFS 2025 ══
# - ashift=12: Toujours pour disques modernes (4K sectors)
# - compression=lz4: Quasi gratuit, toujours activer
# - atime=off: Performance I/O
# - RAIDZ2: Minimum pour production
# - Special vdev: Accélère metadata (miroir obligatoire)
# - Utiliser by-id: Évite problèmes après reboot
```

### RAIDZ Expansion (ZFS 2.3+ / PVE 9+)

```bash
# ═══════════════════════════════════════════════════════════════════════════
# RAIDZ EXPANSION - NOUVEAUTÉ ZFS 2.3 (PVE 9+)
# ═══════════════════════════════════════════════════════════════════════════

# Vérifier version ZFS
zfs version  # Doit être 2.3.0+

# État actuel
zpool status tank
# tank  ONLINE
#   raidz2-0  ONLINE
#     disk1   ONLINE
#     disk2   ONLINE
#     disk3   ONLINE
#     disk4   ONLINE

# Ajouter disque au RAIDZ existant (expansion!)
zpool attach tank raidz2-0 /dev/disk/by-id/scsi-disk5

# Vérifier progression
zpool status tank
# Expansion en cours... 45% complete

# IMPORTANT: L'expansion peut prendre des heures/jours
# Le pool reste accessible pendant l'opération

# ══ NOTES RAIDZ EXPANSION ══
# - Disponible ZFS 2.3.0+ (PVE 9+)
# - Un seul disque à la fois
# - Pool reste online pendant expansion
# - Performance réduite pendant opération
# - Planifier pendant période calme
```

### Gestion des Datasets

```bash
# Créer dataset
zfs create tank/vms
zfs create tank/containers
zfs create tank/backups

# Créer avec quota
zfs create -o quota=500G tank/vms

# Créer avec réservation
zfs create -o reservation=100G tank/critical

# Propriétés dataset
zfs get all tank/vms

# Modifier propriétés
zfs set compression=zstd tank/backups
zfs set recordsize=1M tank/backups  # Pour gros fichiers séquentiels
zfs set sync=disabled tank/scratch  # Si perte acceptable

# Renommer dataset
zfs rename tank/old tank/new

# Supprimer dataset
zfs destroy tank/test

# Supprimer avec descendants
zfs destroy -r tank/old
```

## Voir Aussi
- `/pve-storage` - Gestion stockage general
- `/pve-ceph` - Administration Ceph
- `/pve-backup` - Backup et replication

> Voir aussi : [[zfs-advanced]]
