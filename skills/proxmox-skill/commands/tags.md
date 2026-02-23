# /pve-tags - Gestion des Tags

## Description
Gestion des tags pour VMs et conteneurs Proxmox VE 9+.
Les tags permettent de categoriser, filtrer et organiser les ressources.

## Syntaxe
```
/pve-tags <action> [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `list` | `/pve-tags list` | Lister tous les tags |
| `add` | `/pve-tags add <vmid> <tag>` | Ajouter tag |
| `remove` | `/pve-tags remove <vmid> <tag>` | Retirer tag |
| `search` | `/pve-tags search <tag>` | Chercher par tag |
| `policy` | `/pve-tags policy` | Configurer politique tags |

## Exemples

### Gestion des tags sur VMs/CTs

```bash
# Ajouter un tag a une VM
qm set 100 --tags "production"

# Ajouter plusieurs tags (separes par ;)
qm set 100 --tags "production;web;critical"

# Ajouter un tag a un conteneur
pct set 1000 --tags "production;database"

# Voir les tags d'une VM
qm config 100 | grep tags

# Supprimer tous les tags
qm set 100 --delete tags
```

### Recherche et filtrage par tags

```bash
# Lister toutes les VMs avec un tag specifique
pvesh get /cluster/resources --type vm --output-format=json | \
  jq '.[] | select(.tags // "" | split(";") | index("production")) | {vmid, name, status, tags}'

# Compter les VMs par tag
pvesh get /cluster/resources --type vm --output-format=json | \
  jq -r '.[].tags // empty' | tr ';' '\n' | sort | uniq -c | sort -rn

# Lister les VMs critiques arretees
pvesh get /cluster/resources --type vm --output-format=json | \
  jq '.[] | select((.tags // "" | contains("critical")) and .status == "stopped") | {vmid, name}'

# VMs sans tags (a categoriser)
pvesh get /cluster/resources --type vm --output-format=json | \
  jq '.[] | select(.tags == null or .tags == "") | {vmid, name, node}'
```

### Politique de tags (datacenter)

```bash
# Configurer les tags autorises (PVE 9+)
pvesh set /cluster/options \
  --tag-style "color-map=production:ff0000;staging:ffaa00;dev:00ff00"

# Forcer l'utilisation de tags predetermines
pvesh set /cluster/options \
  --tag-style "shape=full,ordering=config"

# Voir la politique actuelle
pvesh get /cluster/options --output-format=json | jq '.["tag-style"]'
```

### Tags et automatisation

```bash
# Backup uniquement les VMs tagees "backup-daily"
pvesh get /cluster/resources --type vm --output-format=json | \
  jq -r '.[] | select(.tags // "" | split(";") | index("backup-daily")) | .vmid' | \
  tr '\n' ',' | sed 's/,$//' | \
  xargs -I{} vzdump {} --storage pbs-main --mode snapshot --compress zstd

# Demarrer toutes les VMs de production
pvesh get /cluster/resources --type vm --output-format=json | \
  jq -r '.[] | select((.tags // "" | contains("production")) and .status == "stopped") | .vmid' | \
  while read vmid; do
    qm start "$vmid"
    echo "Demarrage VM $vmid"
  done

# Appliquer une config a toutes les VMs tagees
pvesh get /cluster/resources --type vm --output-format=json | \
  jq -r '.[] | select(.tags // "" | split(";") | index("linux")) | .vmid' | \
  while read vmid; do
    qm set "$vmid" --agent enabled=1
  done
```

### Via API REST

```bash
# Modifier tags via API
pvesh set /nodes/pve01/qemu/100/config --tags "production;web;monitored"

# Recherche via API
curl -s -k -H "Authorization: PVEAPIToken=user@pam!token=TOKEN" \
  "https://pve01:8006/api2/json/cluster/resources?type=vm" | \
  jq '.data[] | select(.tags != null) | {vmid, name, tags}'
```

## Notes

- Les tags sont des chaines separees par `;` (point-virgule)
- PVE 9+ supporte les couleurs et styles de tags dans l'interface web
- Les tags facilitent l'organisation dans les grands environnements
- Combiner tags et pools pour une gestion fine des permissions
- Convention recommandee : `env:production`, `app:web`, `owner:devops`
- Les tags sont stockes dans la configuration VM/CT (fichier .conf)

## Voir Aussi
- `/pve-pool` - Pools de ressources
- `/pve-vm` - Gestion machines virtuelles
- `/pve-ct` - Gestion conteneurs
- `/pve-api` - API REST Proxmox
