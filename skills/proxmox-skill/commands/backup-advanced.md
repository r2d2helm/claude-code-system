> Partie avancée de [[backup]]. Commandes essentielles dans le fichier principal.

# /pve-backup - PBS Maintenance, Wizard 3-2-1 et Best Practices

## Description
Maintenance PBS avancée, wizard stratégie de backup 3-2-1, et best practices 2025-2026.

### PBS Maintenance (sur serveur PBS)

```bash
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
