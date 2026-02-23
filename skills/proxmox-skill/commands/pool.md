# /pve-pool - Gestion des Pools de Ressources

## Description
Gestion des pools de ressources Proxmox VE. Les pools regroupent VMs, CTs
et stockage pour simplifier l'administration et les permissions.

## Syntaxe
```
/pve-pool <action> [pool-name] [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `list` | `/pve-pool list` | Lister les pools |
| `create` | `/pve-pool create <name>` | Creer un pool |
| `delete` | `/pve-pool delete <name>` | Supprimer un pool |
| `members` | `/pve-pool members <name>` | Lister les membres |
| `add` | `/pve-pool add <name> <vmid>` | Ajouter une VM/CT |
| `remove` | `/pve-pool remove <name> <vmid>` | Retirer une VM/CT |

## Exemples

### Gestion des pools

```bash
# Lister tous les pools
pvesh get /pools --output-format=json-pretty

# Creer un pool
pvesh create /pools --poolid production --comment "VMs de production"

# Creer pool avec stockage associe
pvesh create /pools --poolid dev-team --comment "Environnement developpement"

# Supprimer un pool (doit etre vide)
pvesh delete /pools/dev-team

# Voir les membres d'un pool
pvesh get /pools/production --output-format=json-pretty
```

### Affecter des ressources

```bash
# Ajouter une VM au pool
pvesh set /pools/production --vms 100

# Ajouter plusieurs VMs
pvesh set /pools/production --vms 100,101,102,103

# Ajouter un stockage au pool
pvesh set /pools/production --storage local-zfs

# Retirer une VM du pool
pvesh set /pools/production --vms 100 --delete 1

# Deplacer VM vers un autre pool
qm set 100 --pool production
```

### Permissions par pool

```bash
# Donner acces complet a un groupe sur un pool
pveum acl modify /pool/production --roles PVEVMAdmin --groups devops

# Acces lecture seule
pveum acl modify /pool/production --roles PVEAuditor --users viewer@pam

# Lister les permissions du pool
pveum acl list --output-format=json | jq '.[] | select(.path | startswith("/pool/"))'
```

### Backup par pool

```bash
# Backup toutes les VMs d'un pool
pvesh create /cluster/backup \
  --id pool-production-daily \
  --schedule "02:00" \
  --storage pbs-main \
  --pool production \
  --mode snapshot \
  --compress zstd

# Lister VMs d'un pool
pvesh get /pools/production --output-format=json | jq '.members[] | {vmid, name, type}'
```

## Notes

- Les pools simplifient la gestion des permissions (une ACL par pool au lieu d'une par VM)
- Un pool peut contenir des VMs, CTs et du stockage
- Les jobs de backup supportent le filtre par pool
- Les pools n'impactent pas le placement des VMs sur les nodes
- Utiliser les pools avec les roles RBAC pour une delegation securisee

## Voir Aussi
- `/pve-users` - Gestion utilisateurs et permissions RBAC
- `/pve-backup` - Backup par pool
- `/pve-vm` - Gestion des machines virtuelles
