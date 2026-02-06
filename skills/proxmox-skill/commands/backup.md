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

# ═══════════════════════════════════════════════════════════════════════════
# PBS MAINTENANCE (sur serveur PBS)
# ═══════════════════════════════════════════════════════════════════════════

# Vérification intégrité
proxmox-backup-manager verify main

# Garbage collection
proxmox-backup-manager garbage-collection main

# Sync vers autre PBS (offsite)
proxmox-backup-manager sync-job create offsite-sync \
  --store main \
  --remote offsite-pbs \
  --remote-store backup \
  --schedule "05:00"

# ═══════════════════════════════════════════════════════════════════════════
# PBS 4.x NOUVEAUTÉS
# ═══════════════════════════════════════════════════════════════════════════

# S3 backend (tech preview)
proxmox-backup-manager datastore create s3-backup \
  --path s3://bucket-name/prefix \
  --s3-access-key AKIAIOSFODNN7EXAMPLE \
  --s3-secret-key wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
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

### Vérification

```bash
# Vérifier backup PBS (sur PBS)
proxmox-backup-client verify vm/100

# Vérifier tous les backups
proxmox-backup-manager verify main --verify-new

# Job de vérification automatique
proxmox-backup-manager verify-job create weekly-verify \
  --store main \
  --schedule "sat 04:00"
```

## Wizard : Stratégie Backup 3-2-1

```
/pve-wizard backup
```

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  🧙 WIZARD: STRATÉGIE BACKUP 3-2-1                                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  La règle 3-2-1:                                                             ║
║  • 3 copies de vos données                                                   ║
║  • 2 types de supports différents                                            ║
║  • 1 copie hors site                                                         ║
║                                                                              ║
║  Étape 1/5: STOCKAGE PRINCIPAL                                               ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Stockage pour backups quotidiens:                                           ║
║    [1] pbs-main (PBS, 10TB, déduplication)     ← Recommandé                  ║
║    [2] nfs-backup (NFS, 10TB)                                                ║
║    [3] local-backup (Directory, 2TB)                                         ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Étape 2/5: STOCKAGE SECONDAIRE                                              ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Stockage pour copie supplémentaire:                                         ║
║    [1] nfs-backup (NFS, site distant)          ← Recommandé offsite          ║
║    [2] Ajouter nouveau stockage                                              ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Étape 3/5: FRÉQUENCE ET RÉTENTION                                           ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Profil de backup:                                                           ║
║    [1] Standard (daily)                                                      ║
║        Daily: 02:00, Weekly: Sun 03:00                                       ║
║        Retention: 7 daily, 4 weekly, 6 monthly                               ║
║    [2] Critique (hourly databases)                                           ║
║        Hourly: */4, Daily: 02:00                                             ║
║        Retention: 24 hourly, 7 daily, 4 weekly                               ║
║    [3] Personnalisé                                                          ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Étape 4/5: SÉLECTION VMs/CTs                                                ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  VMs à sauvegarder:                                                          ║
║    [x] Toutes les VMs (15 actuellement)                                      ║
║    [ ] Par pool                                                              ║
║    [ ] Sélection manuelle                                                    ║
║  Choix:              > Toutes                                                ║
║                                                                              ║
║  Exclure des VMs? (templates, test): > 200,201,120                           ║
║                                                                              ║
║  Étape 5/5: NOTIFICATIONS ET VÉRIFICATION                                    ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Email notifications:    > admin@example.com                                 ║
║  Notifier sur:                                                               ║
║    [1] Échecs seulement   ← Recommandé                                       ║
║    [2] Toujours                                                              ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Vérification automatique (PBS):                                             ║
║    [Y/n] > Y                                                                 ║
║  Fréquence vérification: > weekly (sat 04:00)                                ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  📋 RÉSUMÉ STRATÉGIE 3-2-1                                                   ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║                                                                              ║
║  COPIE 1: Données live (ZFS snapshots automatiques)                          ║
║  COPIE 2: PBS daily → pbs-main (déduplication)                               ║
║           Rétention: 7 daily, 4 weekly, 6 monthly                            ║
║  COPIE 3: Sync weekly → nfs-backup (offsite)                                 ║
║                                                                              ║
║  Jobs créés:                                                                 ║
║    • daily-backup: 02:00, all VMs → pbs-main                                 ║
║    • weekly-sync: Sun 05:00, pbs-main → nfs-backup                           ║
║    • verify-weekly: Sat 04:00, vérification PBS                              ║
║                                                                              ║
║  Notifications: admin@example.com (échecs)                                   ║
║                                                                              ║
║  Appliquer? [Y/n] > Y                                                        ║
║                                                                              ║
║  ✅ Job daily-backup créé                                                    ║
║  ✅ Job weekly-sync créé                                                     ║
║  ✅ Job verify-weekly créé                                                   ║
║  ✅ Stratégie 3-2-1 configurée!                                              ║
║                                                                              ║
║  💡 Test recommandé: restaurer une VM de test                                ║
║  💡 Documentation: /pve-restore                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Best Practices Backup 2025-2026

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  📋 BEST PRACTICES BACKUP 2025-2026                                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PBS vs vzdump traditionnel                                                  ║
║  • PBS: Déduplication, incrémental, encryption → Recommandé                  ║
║  • vzdump NFS: Simple, compatible, pas de dédup                              ║
║                                                                              ║
║  Modes de backup                                                             ║
║  • snapshot: VMs avec QEMU Agent → Pas de downtime                           ║
║  • suspend: VMs sans agent → Brève pause                                     ║
║  • stop: Maximum cohérence → Downtime                                        ║
║                                                                              ║
║  Rétention recommandée                                                       ║
║  • Production: 7 daily, 4 weekly, 6 monthly, 1 yearly                        ║
║  • Dev/Test: 3 daily, 2 weekly                                               ║
║  • Bases de données: 24 hourly + rétention standard                          ║
║                                                                              ║
║  Vérification                                                                ║
║  • PBS verify: Hebdomadaire minimum                                          ║
║  • Test restauration: Mensuel                                                ║
║  • Documenter procédure de restore!                                          ║
║                                                                              ║
║  Sécurité                                                                    ║
║  • Encryption PBS: Obligatoire pour offsite                                  ║
║  • Clé encryption: Sauvegarder séparément!                                   ║
║  • Accès PBS: Comptes dédiés, permissions minimales                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Voir Aussi
- `/pve-restore` - Restauration détaillée
- `/pve-storage` - Configuration stockage
- `/pve-pbs` - Administration PBS
