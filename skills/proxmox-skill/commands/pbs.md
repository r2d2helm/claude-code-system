# /pve-pbs - Administration Proxmox Backup Server

## Description
Administration du Proxmox Backup Server (PBS). Gestion des datastores,
utilisateurs, verification d'integrite, garbage collection et synchronisation.

## Syntaxe
```
/pve-pbs <action> [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `status` | `/pve-pbs status` | Etat general PBS |
| `datastore` | `/pve-pbs datastore <action>` | Gestion datastores |
| `verify` | `/pve-pbs verify [datastore]` | Verification integrite |
| `gc` | `/pve-pbs gc [datastore]` | Garbage collection |
| `sync` | `/pve-pbs sync <action>` | Synchronisation offsite |
| `prune` | `/pve-pbs prune [datastore]` | Nettoyage retentions |
| `users` | `/pve-pbs users` | Gestion utilisateurs PBS |

## Exemples

### Etat et diagnostic

```bash
# Etat general du PBS
proxmox-backup-manager datastore list

# Utilisation d'un datastore
proxmox-backup-manager datastore show main

# Lister les backups d'un datastore
proxmox-backup-client list --repository user@pbs!token@192.168.1.60:main

# Espace utilise par VM
proxmox-backup-client catalog dump vm/100 \
  --repository user@pbs!token@192.168.1.60:main
```

### Gestion des datastores

```bash
# Creer un datastore
proxmox-backup-manager datastore create main /mnt/datastore/main

# Creer avec options
proxmox-backup-manager datastore create offsite /mnt/datastore/offsite \
  --gc-schedule "daily 04:00" \
  --prune-schedule "daily 05:00" \
  --keep-daily 7 --keep-weekly 4 --keep-monthly 6

# Modifier retention
proxmox-backup-manager datastore update main \
  --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --keep-yearly 1

# Supprimer un datastore
proxmox-backup-manager datastore remove old-store
```

### Verification d'integrite

```bash
# Verifier tout un datastore
proxmox-backup-manager verify main

# Verifier uniquement les nouveaux backups
proxmox-backup-manager verify main --verify-new

# Creer job de verification automatique
proxmox-backup-manager verify-job create weekly-check \
  --store main \
  --schedule "sat 04:00"

# Lister les jobs de verification
proxmox-backup-manager verify-job list

# Voir les resultats de verification
proxmox-backup-manager task list --typefilter verify
```

### Garbage Collection

```bash
# Lancer GC manuellement
proxmox-backup-manager garbage-collection start main

# Etat du dernier GC
proxmox-backup-manager garbage-collection status main

# Planifier GC automatique
proxmox-backup-manager datastore update main \
  --gc-schedule "daily 03:00"
```

### Synchronisation offsite

```bash
# Ajouter un serveur distant
proxmox-backup-manager remote add offsite-pbs \
  --host pbs-offsite.example.com \
  --userid backup@pbs!sync-token \
  --fingerprint "AA:BB:CC:..."

# Creer job de sync
proxmox-backup-manager sync-job create offsite-sync \
  --store main \
  --remote offsite-pbs \
  --remote-store backup \
  --schedule "daily 05:00" \
  --remove-vanished true

# Lancer sync manuellement
proxmox-backup-manager sync-job run offsite-sync

# Lister jobs de sync
proxmox-backup-manager sync-job list
```

### Utilisateurs et encryption

```bash
# Creer utilisateur PBS
proxmox-backup-manager user create backup@pbs --password "secure-password"

# Creer token API
proxmox-backup-manager user generate-token backup@pbs automation

# Configurer ACL datastore
proxmox-backup-manager acl update /datastore/main DatastoreBackup --userid backup@pbs

# Generer cle de chiffrement
proxmox-backup-client key create /etc/pve/priv/pbs-encryption.key

# Sauvegarder la cle (CRITIQUE - stocker paperkey dans coffre-fort)
proxmox-backup-client key show /etc/pve/priv/pbs-encryption.key
```

## Notes

- PBS 4.x supporte le backend S3 (tech preview)
- La deduplication reduit l'espace disque de 3:1 en moyenne
- Toujours verifier les backups hebdomadairement au minimum
- Les cles de chiffrement doivent etre sauvegardees separement (paperkey)
- GC doit tourner regulierement pour liberer l'espace des chunks orphelins
- Sync offsite respecte la regle 3-2-1 pour la copie hors site

## Voir Aussi
- `/pve-backup` - Backup vzdump depuis Proxmox
- `/pve-restore` - Restauration VMs/CTs
- `/pve-storage` - Configuration stockage PBS sur PVE
