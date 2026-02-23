# /pve-migrate - Migration VMs et Conteneurs

## Description
Migration de machines virtuelles et conteneurs entre nodes Proxmox.
Supporte la migration live (sans downtime), offline et avec stockage local.

## Syntaxe
```
/pve-migrate <action> <vmid|ctid> <target-node> [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `vm` | `/pve-migrate vm <vmid> <node>` | Migrer une VM |
| `ct` | `/pve-migrate ct <ctid> <node>` | Migrer un conteneur |
| `bulk` | `/pve-migrate bulk <node>` | Migration groupee |
| `precondition` | `/pve-migrate precondition <vmid>` | Verifier faisabilite |

## Exemples

### Migration VM Live

```bash
# Migration live (VM en cours, stockage partage)
qm migrate 100 pve02 --online

# Migration live avec stockage local
qm migrate 100 pve02 --online --with-local-disks --targetstorage local-zfs

# Migration avec reseau dedie
qm migrate 100 pve02 --online --migration_network 10.0.1.0/24

# Migration avec bande passante limitee (MB/s)
qm migrate 100 pve02 --online --migration_type secure --bwlimit 500
```

### Migration VM Offline

```bash
# Migration offline (VM arretee)
qm migrate 100 pve02

# Migration vers stockage different
qm migrate 100 pve02 --targetstorage ceph-pool

# Forcer la migration (ignorer verrous locaux)
qm migrate 100 pve02 --force
```

### Migration Conteneur LXC

```bash
# Migration CT online (si sur stockage partage)
pct migrate 1000 pve02 --online

# Migration CT offline
pct migrate 1000 pve02

# Migration CT avec changement de stockage
pct migrate 1000 pve02 --target-storage local-zfs

# Restart CT apres migration
pct migrate 1000 pve02 --restart
```

### Migration en masse

```bash
# Migrer toutes les VMs d'un node (maintenance)
for vmid in $(qm list | awk 'NR>1 {print $1}'); do
  echo "Migration VM $vmid vers pve02..."
  qm migrate "$vmid" pve02 --online --with-local-disks 2>&1
done

# Verifier les preconditions avant migration
pvesh get /nodes/pve01/qemu/100/migrate --target pve02 --output-format=json-pretty
```

### Via API

```bash
# Migration via API REST
pvesh create /nodes/pve01/qemu/100/migrate \
  --target pve02 \
  --online 1 \
  --with-local-disks 1

# Verifier preconditions via API
pvesh get /nodes/pve01/qemu/100/migrate \
  --target pve02 \
  --output-format=json-pretty
```

## Notes

- Migration live requiert CPU compatible entre nodes (meme famille)
- Stockage partage (Ceph, NFS, iSCSI) : migration quasi-instantanee
- Stockage local : necessite `--with-local-disks` et transfert des donnees
- Reseau dedie migration : fortement recommande en production (10GbE)
- Les snapshots locaux ne sont pas migres avec la VM
- HA gere automatiquement la migration en cas de panne node

## Voir Aussi
- `/pve-ha` - Haute disponibilite et migration automatique
- `/pve-vm` - Gestion des machines virtuelles
- `/pve-ct` - Gestion des conteneurs
- `/pve-cluster` - Gestion cluster multi-nodes
