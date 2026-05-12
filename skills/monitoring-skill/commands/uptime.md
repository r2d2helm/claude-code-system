---
name: mon-uptime
description: Disponibilite des services (Uptime Kuma)
---

# /mon-uptime - Disponibilite Services

## Comportement

Uptime Kuma surveille la disponibilite des services. Interroger via son API :

1. **Lister les monitors** :
   ```bash
   ssh root@192.168.1.162 "curl -s http://localhost:3003/api/status-page/default"
   ```

2. **Afficher l'etat** de chaque service avec uptime %

## Services surveilles

| Service | URL | Type |
|---------|-----|------|
| Proxmox WebUI | https://192.168.1.215:8006 | HTTPS |
| Taskyn Core | http://192.168.1.162:8020 | HTTP |
| Taskyn Web | http://192.168.1.162:3020 | HTTP |
| Beszel Hub | http://192.168.1.162:8091 | HTTP |
| Netdata | http://192.168.1.162:19999 | HTTP |
| ntfy | http://192.168.1.162:8084 | HTTP |
| Dozzle | http://192.168.1.162:8082 | HTTP |
| SSH VM 100 | 192.168.1.162:22 | TCP |
| SSH Proxmox | 192.168.1.215:22 | TCP |
| DNS | 192.168.1.162:53 | DNS |

## Uptime Kuma Web UI

- URL : http://192.168.1.162:3003
- Setup initial requis via l'interface web
