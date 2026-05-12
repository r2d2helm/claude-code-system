# /pve-backup - Backup et Proxmox Backup Server

## Description
Gestion complète des sauvegardes Proxmox : vzdump, PBS, jobs programmés,
et stratégie 3-2-1.

## Syntaxe
```
/pve-backup <action> [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `status` | `/pve-backup status` | État des backups |
| `now` | `/pve-backup now <vmid>` | Backup immédiat |
| `jobs` | `/pve-backup jobs` | Jobs programmés |
| `schedule` | `/pve-backup schedule` | Créer job programmé |
| `list` | `/pve-backup list [storage]` | Lister backups |
| `restore` | `/pve-backup restore` | Restaurer backup |
| `verify` | `/pve-backup verify` | Vérifier intégrité |
| `prune` | `/pve-backup prune` | Nettoyer anciens backups |
| `pbs` | `/pve-backup pbs <action>` | Gestion PBS |

## Affichage Status Backups

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║  💾 BACKUP STATUS                                                                ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  ┌─ SCHEDULED JOBS ──────────────────────────────────────────────────────────┐  ║
║  │ ID      │ Schedule      │ Storage   │ VMs/CTs    │ Last Run    │ Status   │  ║
║  │─────────┼───────────────┼───────────┼────────────┼─────────────┼──────────│  ║
║  │ daily   │ 02:00 daily   │ pbs-main  │ all (15)   │ 6h ago      │ ✅ OK    │  ║
║  │ weekly  │ 03:00 sun     │ nfs-backup│ production │ 3d ago      │ ✅ OK    │  ║
║  │ db-hourly│ */4 *        │ pbs-main  │ 104,105    │ 2h ago      │ ✅ OK    │  ║
║  └───────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                  ║
║  ┌─ STORAGE USAGE ───────────────────────────────────────────────────────────┐  ║
║  │ Storage   │ Type │ Used       │ Available │ Backups │ Dedup Ratio        │  ║
║  │───────────┼──────┼────────────┼───────────┼─────────┼────────────────────│  ║
║  │ pbs-main  │ PBS  │ 4.8 TB     │ 5.2 TB    │ 342     │ 3.2:1              │  ║
║  │ nfs-backup│ NFS  │ 5.5 TB     │ 4.5 TB    │ 89      │ N/A                │  ║
║  └───────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                  ║
║  ┌─ RECENT BACKUPS ──────────────────────────────────────────────────────────┐  ║
║  │ Time              │ VMID │ Name           │ Size    │ Duration │ Status  │  ║
║  │───────────────────┼──────┼────────────────┼─────────┼──────────┼─────────│  ║
║  │ 2025-02-03 02:15  │ 104  │ db-postgres    │ 45.2 GB │ 12m 34s  │ ✅ OK   │  ║
║  │ 2025-02-03 02:12  │ 100  │ dc01-windows   │ 32.1 GB │ 8m 45s   │ ✅ OK   │  ║
║  │ 2025-02-03 02:05  │ 102  │ web-nginx-01   │ 8.4 GB  │ 2m 12s   │ ✅ OK   │  ║
║  │ 2025-02-02 02:00  │ 105  │ db-replica     │ 44.8 GB │ 11m 58s  │ ✅ OK   │  ║
║  └───────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                  ║
║  ┌─ 3-2-1 RULE STATUS ───────────────────────────────────────────────────────┐  ║
║  │ ✅ 3 copies: Local ZFS snapshot + PBS + NFS offsite                       │  ║
║  │ ✅ 2 media types: SSD (PBS) + HDD (NFS)                                   │  ║
║  │ ✅ 1 offsite: nfs-backup sur site distant                                  │  ║
║  │ ⚠️  Dernière vérification PBS: il y a 8 jours (recommandé: 7 jours)       │  ║
║  └───────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

## Commandes Bash

### Backup Immédiat (vzdump)

```bash
# ═══════════════════════════════════════════════════════════════════════════
# BACKUP MANUEL
# ═══════════════════════════════════════════════════════════════════════════

# Backup VM simple
vzdump 100 --storage pbs-main --mode snapshot

# Backup avec compression
vzdump 100 --storage pbs-main --mode snapshot --compress zstd

# Backup plusieurs VMs
vzdump 100,101,102 --storage pbs-main --mode snapshot

# Backup toutes les VMs d'un node
vzdump --all --storage pbs-main --mode snapshot --node pve01

# Backup avec options complètes
vzdump 100 \
  --storage pbs-main \
  --mode snapshot \
  --compress zstd \
  --notes "Pre-upgrade backup" \
  --mailto admin@example.com \
  --mailnotification always \
  --protected 1

# ═══════════════════════════════════════════════════════════════════════════
# MODES DE BACKUP
# ═══════════════════════════════════════════════════════════════════════════

# snapshot: Pas d'interruption (recommandé pour VMs)
vzdump 100 --mode snapshot

# suspend: Pause brève pour cohérence mémoire
vzdump 100 --mode suspend

# stop: Arrêt complet (plus sûr mais downtime)
vzdump 100 --mode stop

# ══ RECOMMANDATIONS ══
# VMs avec QEMU Guest Agent: snapshot
# VMs sans agent: suspend ou stop
# Bases de données: stop ou scripts pre/post
```

### Jobs de Backup Programmés

```bash
# ═══════════════════════════════════════════════════════════════════════════
# JOBS PROGRAMMÉS
# ═══════════════════════════════════════════════════════════════════════════

# Lister jobs
pvesh get /cluster/backup --output-format=json-pretty

# Créer job daily pour toutes VMs
pvesh create /cluster/backup \
  --id daily-backup \
  --schedule "02:00" \
  --storage pbs-main \
  --mode snapshot \
  --compress zstd \
  --all 1 \
  --enabled 1 \
  --mailnotification failure \
  --mailto admin@example.com

# Job pour VMs spécifiques
pvesh create /cluster/backup \
  --id db-backup \
  --schedule "*/6:00" \
  --storage pbs-main \
  --vmid "104,105" \
  --mode snapshot \
  --compress zstd \
  --enabled 1

# Job hebdomadaire
pvesh create /cluster/backup \
  --id weekly-full \
  --schedule "sun 03:00" \
  --storage nfs-backup \
  --mode stop \
  --all 1 \
  --compress zstd

# Job avec pool
pvesh create /cluster/backup \
  --id production-daily \
  --schedule "01:00" \
  --storage pbs-main \
  --pool production \
  --mode snapshot

# Modifier job
pvesh set /cluster/backup/daily-backup --schedule "03:00"

# Désactiver job
pvesh set /cluster/backup/daily-backup --enabled 0

# Supprimer job
pvesh delete /cluster/backup/old-job

# Exécuter job manuellement
vzdump --jobid daily-backup

# ═══════════════════════════════════════════════════════════════════════════
# RÉTENTION
# ═══════════════════════════════════════════════════════════════════════════

# Job avec rétention définie
pvesh create /cluster/backup \
  --id daily-retention \
  --schedule "02:00" \
  --storage pbs-main \
  --all 1 \
  --prune-backups "keep-daily=7,keep-weekly=4,keep-monthly=6"

# ══ RÉTENTION RECOMMANDÉE 3-2-1 ══
# keep-daily=7       # 7 derniers jours
# keep-weekly=4      # 4 dernières semaines
# keep-monthly=6     # 6 derniers mois
# keep-yearly=1      # 1 an (optionnel)
```

### Proxmox Backup Server (PBS)

```bash
# ═══════════════════════════════════════════════════════════════════════════
# PBS CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

# Ajouter datastore PBS
pvesm add pbs pbs-main \
  --server 192.168.1.60 \
  --datastore main \
  --username backup@pbs \
  --password "password" \
  --fingerprint "AA:BB:CC:..." \
  --content backup

# Avec encryption
proxmox-backup-client key create /etc/pve/priv/pbs-key.enc
pvesm add pbs pbs-encrypted \
  --server 192.168.1.60 \
  --datastore encrypted \
  --username backup@pbs \
  --encryption-key /etc/pve/priv/pbs-key.enc
```

### Lister et Restaurer

```bash
# Lister backups
pvesh get /nodes/pve01/storage/pbs-main/content --content backup

# Lister backups d'une VM
pvesh get /nodes/pve01/storage/pbs-main/content --vmid 100

# Restaurer VM
qmrestore pbs-main:backup/vm/100/2025-02-03T02:15:00Z 100

# Restaurer vers nouveau VMID
qmrestore pbs-main:backup/vm/100/2025-02-03T02:15:00Z 150

# Restaurer CT
pct restore 1000 pbs-main:backup/ct/1000/2025-02-03T02:00:00Z

# Restaurer avec options
qmrestore pbs-main:backup/vm/100/... 100 \
  --storage local-zfs \
  --unique \
  --force
```

## Voir Aussi
- `/pve-restore` - Restauration détaillée
- `/pve-storage` - Configuration stockage
- `/pve-pbs` - Administration PBS

> Voir aussi : [[backup-advanced]]
