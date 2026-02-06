# /pve-zfs - Administration ZFS

## Description
Administration complète ZFS sur Proxmox VE : pools, datasets, snapshots,
réplication, et RAIDZ expansion (ZFS 2.3+ / PVE 9+).

## Syntaxe
```
/pve-zfs <action> [pool/dataset] [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `status` | `/pve-zfs status [pool]` | État des pools ZFS |
| `create` | `/pve-zfs create <pool>` | Créer pool |
| `destroy` | `/pve-zfs destroy <pool>` | Supprimer pool |
| `expand` | `/pve-zfs expand <pool>` | RAIDZ expansion (PVE 9+) |
| `scrub` | `/pve-zfs scrub <pool>` | Lancer scrub |
| `snapshot` | `/pve-zfs snapshot` | Gérer snapshots |
| `replicate` | `/pve-zfs replicate` | Réplication ZFS |
| `send` | `/pve-zfs send` | Envoyer snapshot |
| `receive` | `/pve-zfs receive` | Recevoir snapshot |
| `properties` | `/pve-zfs properties <ds>` | Propriétés dataset |

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

### Création de Pools - Best Practices 2025-2026

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

### Snapshots ZFS

```bash
# Créer snapshot
zfs snapshot tank/vms@daily-$(date +%Y%m%d)

# Snapshot récursif
zfs snapshot -r tank@backup-pre-upgrade

# Lister snapshots
zfs list -t snapshot

# Lister snapshots d'un dataset
zfs list -t snapshot -r tank/vms

# Espace utilisé par snapshots
zfs list -o name,used,refer -t snapshot

# Rollback (attention: perte données après snapshot)
zfs rollback tank/vms@daily-20250201

# Rollback forcé (détruit snapshots intermédiaires)
zfs rollback -r tank/vms@daily-20250101

# Supprimer snapshot
zfs destroy tank/vms@old-snapshot

# Supprimer snapshots en batch
zfs destroy tank/vms@daily-202401%  # Pattern matching
```

### Réplication ZFS

```bash
# ═══════════════════════════════════════════════════════════════════════════
# RÉPLICATION ZFS (entre nodes)
# ═══════════════════════════════════════════════════════════════════════════

# Envoi initial complet
zfs snapshot tank/vms@initial
zfs send tank/vms@initial | ssh pve02 zfs receive backup/vms

# Envoi incrémental
zfs snapshot tank/vms@snap2
zfs send -i tank/vms@initial tank/vms@snap2 | ssh pve02 zfs receive backup/vms

# Envoi compressé (plus rapide sur réseau lent)
zfs send tank/vms@snap | gzip | ssh pve02 "gunzip | zfs receive backup/vms"

# Envoi avec pv pour progression
zfs send -v tank/vms@snap | pv | ssh pve02 zfs receive backup/vms

# Réplication récursive
zfs send -R tank@snap | ssh pve02 zfs receive -F backup

# ═══════════════════════════════════════════════════════════════════════════
# RÉPLICATION PROXMOX INTÉGRÉE (pour VMs)
# ═══════════════════════════════════════════════════════════════════════════

# Créer job de réplication
pvesr create-local-job 100-0 pve02 --schedule '*/15' --rate 50

# Lister jobs
pvesr list

# Status réplication
pvesr status

# Exécuter réplication manuellement
pvesr run 100-0

# Supprimer job
pvesr delete 100-0
```

### Maintenance

```bash
# Scrub (vérification intégrité) - Hebdomadaire recommandé
zpool scrub tank

# Progression scrub
zpool status tank | grep -A5 scan

# Annuler scrub
zpool scrub -s tank

# Trim (SSD) - Automatique si supporté
zpool trim tank

# Clear erreurs (après remplacement disque)
zpool clear tank

# Importer pool (après déplacement)
zpool import
zpool import tank

# Exporter pool (avant déplacement)
zpool export tank
```

### Remplacement de Disque

```bash
# Identifier disque défaillant
zpool status tank  # Chercher DEGRADED ou FAULTED

# Remplacer disque online (hot spare ou nouveau)
zpool replace tank /dev/disk/by-id/old-disk /dev/disk/by-id/new-disk

# Progression resilver
zpool status tank

# Si disque complètement mort
zpool offline tank /dev/disk/by-id/dead-disk
# Installer nouveau disque physiquement
zpool replace tank /dev/disk/by-id/dead-disk /dev/disk/by-id/new-disk

# Retirer disque d'un mirror (réduction)
zpool detach tank /dev/disk/by-id/disk-to-remove
```

### Ajout Stockage Proxmox

```bash
# Ajouter pool ZFS comme storage Proxmox
pvesm add zfspool local-zfs \
  --pool tank/vms \
  --content images,rootdir \
  --sparse 1

# Avec thin provisioning
pvesm add zfspool tank-vms \
  --pool tank/proxmox \
  --content images,rootdir \
  --sparse 1 \
  --blocksize 8k
```

## Wizard : Création Pool ZFS

```
/pve-zfs create --wizard
```

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  🧙 WIZARD: CRÉATION POOL ZFS                                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Étape 1/4: SÉLECTION DISQUES                                                ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Disques disponibles:                                                        ║
║    [1] /dev/sdb - ST4000NM 4TB (SMART: OK)                                   ║
║    [2] /dev/sdc - ST4000NM 4TB (SMART: OK)                                   ║
║    [3] /dev/sdd - ST4000NM 4TB (SMART: OK)                                   ║
║    [4] /dev/sde - ST4000NM 4TB (SMART: OK)                                   ║
║    [5] /dev/sdf - ST4000NM 4TB (SMART: OK)                                   ║
║    [6] /dev/sdg - ST4000NM 4TB (SMART: OK)                                   ║
║    [7] /dev/nvme0n1 - Samsung 980 1TB (SMART: OK)                            ║
║    [8] /dev/nvme1n1 - Samsung 980 1TB (SMART: OK)                            ║
║                                                                              ║
║  Sélection (ex: 1,2,3,4,5,6): > 1,2,3,4,5,6                                  ║
║                                                                              ║
║  Étape 2/4: NIVEAU RAID                                                      ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Avec 6 disques, options disponibles:                                        ║
║    [1] RAIDZ2 (4+2)    ← Recommandé production                               ║
║        Capacité: ~16TB | Tolérance: 2 disques                                ║
║    [2] RAIDZ1 (5+1)                                                          ║
║        Capacité: ~20TB | Tolérance: 1 disque                                 ║
║    [3] Mirror (3x2)                                                          ║
║        Capacité: ~12TB | Tolérance: 1 par groupe                             ║
║    [4] RAIDZ3 (3+3)    ← Ultra-redondant                                     ║
║        Capacité: ~12TB | Tolérance: 3 disques                                ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Étape 3/4: SPECIAL VDEV (optionnel)                                         ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Ajouter Special VDEV pour accélérer metadata?                               ║
║    [1] Non                                                                   ║
║    [2] Oui - utiliser NVMe 7,8 en mirror                                     ║
║  Choix:              > 2                                                     ║
║                                                                              ║
║  Étape 4/4: OPTIONS                                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Nom du pool:        > tank                                                  ║
║  Compression:                                                                ║
║    [1] lz4            ← Recommandé (rapide)                                  ║
║    [2] zstd           ← Meilleur ratio                                       ║
║    [3] off                                                                   ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  atime:              [y/N] > N                                               ║
║  Ajouter à Proxmox:  [Y/n] > Y                                               ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  📋 RÉSUMÉ                                                                   ║
║  Pool: tank    Type: RAIDZ2    Disques: 6x 4TB + 2x 1TB NVMe special        ║
║  Capacité utile: ~16 TB    Options: compression=lz4, atime=off              ║
║                                                                              ║
║  Commande:                                                                   ║
║  zpool create -o ashift=12 -O compression=lz4 -O atime=off \                 ║
║    -O special_small_blocks=32K tank raidz2 \                                 ║
║    /dev/disk/by-id/scsi-{1,2,3,4,5,6} \                                      ║
║    special mirror /dev/disk/by-id/nvme-{1,2}                                 ║
║                                                                              ║
║  Confirmer? [Y/n] > Y                                                        ║
║                                                                              ║
║  ✅ Pool tank créé avec succès!                                              ║
║  ✅ Storage local-zfs ajouté à Proxmox                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Voir Aussi
- `/pve-storage` - Gestion stockage général
- `/pve-ceph` - Administration Ceph
- `/pve-backup` - Backup et réplication
