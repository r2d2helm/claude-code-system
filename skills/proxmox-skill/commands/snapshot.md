# /pve-snapshot - Gestion des Snapshots

## Description
Gestion des snapshots VM et CT sur Proxmox VE. Inclut creation, restauration,
suppression et arborescence des snapshots pour KVM et LXC.

## Syntaxe
```
/pve-snapshot <action> <vmid|ctid> [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `list` | `/pve-snapshot list <id>` | Lister snapshots d'une VM/CT |
| `create` | `/pve-snapshot create <id> <name>` | Creer snapshot |
| `rollback` | `/pve-snapshot rollback <id> <name>` | Restaurer snapshot |
| `delete` | `/pve-snapshot delete <id> <name>` | Supprimer snapshot |
| `config` | `/pve-snapshot config <id> <name>` | Voir config snapshot |

## Exemples

### Snapshots VM (KVM)

```bash
# Lister snapshots
qm listsnapshot 100

# Creer snapshot avec etat memoire (VM en cours)
qm snapshot 100 pre-upgrade --vmstate 1 --description "Avant mise a jour"

# Creer snapshot sans memoire (plus rapide)
qm snapshot 100 daily-snap --description "Snapshot quotidien $(date +%Y%m%d)"

# Rollback a un snapshot (VM doit etre arretee si pas de vmstate)
qm rollback 100 pre-upgrade

# Supprimer un snapshot
qm delsnapshot 100 pre-upgrade

# Supprimer snapshot avec enfants (force merge)
qm delsnapshot 100 old-snap --force

# Voir la configuration sauvegardee dans un snapshot
qm snapshot 100 pre-upgrade --get-config
```

### Snapshots CT (LXC)

```bash
# Lister snapshots conteneur
pct listsnapshot 1000

# Creer snapshot CT
pct snapshot 1000 pre-upgrade --description "Avant mise a jour"

# Rollback CT
pct rollback 1000 pre-upgrade

# Supprimer snapshot CT
pct delsnapshot 1000 pre-upgrade
```

### Operations en masse

```bash
# Snapshot toutes les VMs en cours d'execution
for vmid in $(qm list | awk '/running/ {print $1}'); do
  qm snapshot "$vmid" pre-maint --description "Maintenance $(date +%Y%m%d)"
done

# Lister tous les snapshots du cluster
pvesh get /cluster/resources --type vm --output-format=json | \
  jq -r '.[] | .vmid' | while read vmid; do
    echo "=== VM/CT $vmid ==="
    qm listsnapshot "$vmid" 2>/dev/null || pct listsnapshot "$vmid" 2>/dev/null
done

# Nettoyer snapshots de plus de 30 jours (script)
pvesh get /nodes/pve01/qemu/100/snapshot --output-format=json | \
  jq -r '.[] | select(.snaptime < (now - 2592000)) | .name'
```

### Via API

```bash
# Creer snapshot via API
pvesh create /nodes/pve01/qemu/100/snapshot \
  --snapname pre-upgrade \
  --vmstate 1 \
  --description "Snapshot API"

# Lister via API
pvesh get /nodes/pve01/qemu/100/snapshot --output-format=json-pretty

# Rollback via API
pvesh create /nodes/pve01/qemu/100/snapshot/pre-upgrade/rollback
```

## Notes

- Les snapshots ZFS sont quasi-instantanes et n'impactent pas les performances
- Les snapshots avec vmstate incluent la RAM (fichier volumineux)
- Eviter l'accumulation de snapshots : chaque snapshot degrade les I/O sur QCOW2
- Sur ZFS/Ceph : pas de degradation I/O liee aux snapshots
- Toujours documenter les snapshots avec `--description`
- Rollback detruit tous les snapshots enfants

## Voir Aussi
- `/pve-vm` - Gestion des machines virtuelles
- `/pve-ct` - Gestion des conteneurs
- `/pve-backup` - Backup complet vzdump/PBS
