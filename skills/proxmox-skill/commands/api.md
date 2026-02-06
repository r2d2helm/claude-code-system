# 🔌 /pve-api - API REST & Automation

## Description
Utilisation de l'API REST Proxmox VE 9+ pour automation et intégration.

## Syntaxe
```
/pve-api [action] [options]
```

## Authentification API

### Méthode 1: API Token (Recommandé)
```bash
# Créer utilisateur et token
pveum user add automation@pve
pveum aclmod / -user automation@pve -role PVEAdmin
pveum user token add automation@pve api-token --privsep 0

# Utilisation
TOKEN="automation@pve!api-token=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  https://pve.example.com:8006/api2/json/version
```

### Méthode 2: Ticket/Cookie
```bash
# Obtenir ticket
RESPONSE=$(curl -k -d "username=root@pam&password=secret" \
  https://pve.example.com:8006/api2/json/access/ticket)

TICKET=$(echo $RESPONSE | jq -r '.data.ticket')
CSRF=$(echo $RESPONSE | jq -r '.data.CSRFPreventionToken')

# Utilisation
curl -k -b "PVEAuthCookie=$TICKET" -H "CSRFPreventionToken: $CSRF" \
  https://pve.example.com:8006/api2/json/nodes
```

## Endpoints Principaux

### Cluster
```bash
# Status cluster
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/cluster/status"

# Resources cluster
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/cluster/resources"

# Configuration cluster
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/cluster/config"
```

### Nodes
```bash
# Lister nodes
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes"

# Info node spécifique
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes/{node}/status"

# Réseau node
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes/{node}/network"
```

### VMs (QEMU)
```bash
# Lister VMs
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes/{node}/qemu"

# Status VM
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes/{node}/qemu/{vmid}/status/current"

# Config VM
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes/{node}/qemu/{vmid}/config"

# Créer VM
curl -k -X POST -H "Authorization: PVEAPIToken=$TOKEN" \
  -d "vmid=100&name=test-vm&memory=2048&cores=2&sockets=1" \
  -d "scsi0=local-lvm:32&ostype=l26&net0=virtio,bridge=vmbr0" \
  "https://pve:8006/api2/json/nodes/{node}/qemu"

# Démarrer VM
curl -k -X POST -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes/{node}/qemu/{vmid}/status/start"

# Arrêter VM
curl -k -X POST -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes/{node}/qemu/{vmid}/status/stop"

# Snapshot VM
curl -k -X POST -H "Authorization: PVEAPIToken=$TOKEN" \
  -d "snapname=snap1&description=API snapshot" \
  "https://pve:8006/api2/json/nodes/{node}/qemu/{vmid}/snapshot"
```

### Conteneurs (LXC)
```bash
# Lister conteneurs
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes/{node}/lxc"

# Créer conteneur
curl -k -X POST -H "Authorization: PVEAPIToken=$TOKEN" \
  -d "vmid=200&hostname=test-ct&ostemplate=local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst" \
  -d "storage=local-lvm&rootfs=local-lvm:8&memory=512&swap=512" \
  -d "net0=name=eth0,bridge=vmbr0,ip=dhcp&unprivileged=1" \
  "https://pve:8006/api2/json/nodes/{node}/lxc"
```

### Storage
```bash
# Lister storages
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/storage"

# Contenu storage
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes/{node}/storage/{storage}/content"

# Upload ISO
curl -k -X POST -H "Authorization: PVEAPIToken=$TOKEN" \
  -F "content=iso" \
  -F "filename=@/path/to/image.iso" \
  "https://pve:8006/api2/json/nodes/{node}/storage/{storage}/upload"
```

### Backup
```bash
# Lancer backup
curl -k -X POST -H "Authorization: PVEAPIToken=$TOKEN" \
  -d "vmid=100&storage=pbs-storage&mode=snapshot&compress=zstd" \
  "https://pve:8006/api2/json/nodes/{node}/vzdump"

# Lister backups
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes/{node}/storage/{storage}/content?content=backup"
```

## Scripts Automation

### Script Bash complet
```bash
#!/bin/bash
# pve-api.sh - Automation Proxmox

PVE_HOST="https://pve.example.com:8006"
PVE_TOKEN="automation@pve!api-token=xxxxx"

# Fonction API générique
pve_api() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    if [ -z "$data" ]; then
        curl -s -k -X "$method" \
            -H "Authorization: PVEAPIToken=$PVE_TOKEN" \
            "${PVE_HOST}/api2/json${endpoint}"
    else
        curl -s -k -X "$method" \
            -H "Authorization: PVEAPIToken=$PVE_TOKEN" \
            -d "$data" \
            "${PVE_HOST}/api2/json${endpoint}"
    fi
}

# Exemples utilisation
# Lister VMs
pve_api GET "/nodes/pve1/qemu" | jq '.data[] | {vmid, name, status}'

# Démarrer VM
pve_api POST "/nodes/pve1/qemu/100/status/start"

# Créer snapshot
pve_api POST "/nodes/pve1/qemu/100/snapshot" "snapname=auto-$(date +%Y%m%d)"
```

### Script Python
```python
#!/usr/bin/env python3
"""Proxmox API Client"""

import requests
import urllib3
urllib3.disable_warnings()

class ProxmoxAPI:
    def __init__(self, host, token):
        self.base_url = f"https://{host}:8006/api2/json"
        self.headers = {"Authorization": f"PVEAPIToken={token}"}
    
    def get(self, endpoint):
        r = requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            verify=False
        )
        return r.json()['data']
    
    def post(self, endpoint, data=None):
        r = requests.post(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            data=data,
            verify=False
        )
        return r.json()['data']

# Utilisation
pve = ProxmoxAPI("pve.example.com", "automation@pve!api-token=xxxxx")

# Lister VMs
vms = pve.get("/nodes/pve1/qemu")
for vm in vms:
    print(f"VM {vm['vmid']}: {vm['name']} - {vm['status']}")

# Démarrer VM
pve.post("/nodes/pve1/qemu/100/status/start")
```

## pvesh CLI

### Usage local (sur le node)
```bash
# Lister resources
pvesh get /cluster/resources

# Status VM
pvesh get /nodes/pve1/qemu/100/status/current

# Créer VM
pvesh create /nodes/pve1/qemu \
  --vmid 105 \
  --name test-api \
  --memory 2048 \
  --cores 2 \
  --scsi0 local-lvm:32 \
  --net0 virtio,bridge=vmbr0

# Modifier VM
pvesh set /nodes/pve1/qemu/100/config --memory 4096

# Supprimer VM
pvesh delete /nodes/pve1/qemu/100

# Format JSON
pvesh get /nodes/pve1/qemu --output-format json-pretty
```

## Tasks & Jobs

### Suivre une tâche
```bash
# Lancer backup (retourne UPID)
UPID=$(curl -s -k -X POST -H "Authorization: PVEAPIToken=$TOKEN" \
  -d "vmid=100&storage=local&mode=snapshot" \
  "https://pve:8006/api2/json/nodes/pve1/vzdump" | jq -r '.data')

# Suivre progression
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes/pve1/tasks/$UPID/status"

# Logs tâche
curl -k -H "Authorization: PVEAPIToken=$TOKEN" \
  "https://pve:8006/api2/json/nodes/pve1/tasks/$UPID/log"
```

## Webhooks & Events

### Polling status
```bash
#!/bin/bash
# Monitor VM status changes
VMID=100
LAST_STATUS=""

while true; do
    STATUS=$(pvesh get /nodes/pve1/qemu/$VMID/status/current --output-format json | jq -r '.status')
    
    if [ "$STATUS" != "$LAST_STATUS" ]; then
        echo "$(date): VM $VMID status changed: $LAST_STATUS -> $STATUS"
        # Trigger webhook/notification ici
        LAST_STATUS=$STATUS
    fi
    
    sleep 5
done
```

## Référence API

### Documentation interactive
```
https://pve.example.com:8006/pve-docs/api-viewer/
```

### Endpoints principaux
| Endpoint | Description |
|----------|-------------|
| `/version` | Version Proxmox |
| `/cluster/status` | Status cluster |
| `/cluster/resources` | Resources cluster |
| `/nodes` | Liste nodes |
| `/nodes/{node}/qemu` | VMs sur node |
| `/nodes/{node}/lxc` | CTs sur node |
| `/nodes/{node}/storage` | Storages node |
| `/access/users` | Utilisateurs |
| `/access/acl` | ACLs |

## Best Practices

1. **Toujours API Token** plutôt que password
2. **HTTPS** obligatoire (auto-signé OK pour lab)
3. **Privilèges minimum** pour les tokens
4. **Rate limiting** dans vos scripts
5. **Gérer les erreurs** et timeouts
6. **Logger les actions** API
