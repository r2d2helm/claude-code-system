# /pve-replication - Replication de Stockage

## Description
Gestion de la replication de stockage entre nodes Proxmox VE.
Utilise les snapshots ZFS pour repliquer les disques VM/CT de maniere incrementale.

## Syntaxe
```
/pve-replication <action> [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `status` | `/pve-replication status` | Etat des replications |
| `list` | `/pve-replication list` | Lister les jobs |
| `create` | `/pve-replication create <vmid> <target>` | Creer job replication |
| `delete` | `/pve-replication delete <jobid>` | Supprimer job |
| `schedule` | `/pve-replication schedule <jobid>` | Modifier frequence |
| `log` | `/pve-replication log <jobid>` | Voir logs replication |

## Exemples

### Etat et diagnostic

```bash
# Voir l'etat de toutes les replications
pvesr status

# Lister les jobs de replication
pvesr list

# Logs d'un job specifique
pvesr read <jobid>

# Etat detaille via API
pvesh get /cluster/replication --output-format=json-pretty

# Voir le prochain run prevu
pvesr status --output-format=json | jq '.[] | {id, vmid, target, next_sync}'
```

### Creer des jobs de replication

```bash
# Replication VM vers autre node (toutes les 15 min)
pvesr create-local-job 100-0 pve02 --schedule "*/15"

# Replication toutes les heures
pvesr create-local-job 101-0 pve02 --schedule "*/60"

# Replication avec commentaire
pvesr create-local-job 104-0 pve03 --schedule "*/15" \
  --comment "Replication base de donnees"

# Replication toutes les 5 minutes (bases critiques)
pvesr create-local-job 104-0 pve02 --schedule "*/5"

# Replication avec limite de taux
pvesr create-local-job 100-0 pve02 --schedule "*/15" --rate 50
```

### Gestion des jobs

```bash
# Modifier la frequence d'un job
pvesr update 100-0 --schedule "*/30"

# Desactiver temporairement un job
pvesr update 100-0 --disable 1

# Reactiver un job
pvesr update 100-0 --disable 0

# Modifier la limite de bande passante (MB/s)
pvesr update 100-0 --rate 100

# Supprimer un job de replication
pvesr delete 100-0

# Forcer supression (ignore les erreurs)
pvesr delete 100-0 --force --keep
```

### Via API

```bash
# Creer job via API
pvesh create /cluster/replication \
  --id 100-0 \
  --type local \
  --target pve02 \
  --schedule "*/15"

# Etat via API
pvesh get /cluster/replication --output-format=json-pretty

# Logs via API
pvesh get /nodes/pve01/replication/100-0/log --output-format=json-pretty
```

## Notes

- Necessite ZFS sur les deux nodes (source et cible)
- La premiere replication est un transfert complet (peut etre long)
- Les replications suivantes sont incrementales (snapshots ZFS)
- Intervalle minimum recommande : 1 minute (*/1)
- La replication accelere le basculement HA (disques deja presents)
- Ne remplace pas les backups : protege contre la panne node, pas contre la corruption

## Voir Aussi
- `/pve-ha` - Haute disponibilite
- `/pve-zfs` - Administration ZFS
- `/pve-storage` - Configuration stockage
- `/pve-backup` - Backup vzdump/PBS
