> Partie avancee de [[zfs]]. Commandes essentielles dans le fichier principal.

# /pve-zfs - Administration ZFS (Avancee)

## Description
Snapshots, replication, maintenance, remplacement de disque, integration Proxmox et wizard ZFS.

## Snapshots ZFS

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

## Replication ZFS

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

## Maintenance

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

## Remplacement de Disque

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

## Ajout Stockage Proxmox

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

## Wizard : Creation Pool ZFS

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
- `/pve-storage` - Gestion stockage general
- `/pve-ceph` - Administration Ceph
- `/pve-backup` - Backup et replication
