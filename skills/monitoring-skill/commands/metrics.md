---
name: mon-metrics
description: Metriques detaillees Netdata
---

# /mon-metrics - Metriques Detaillees

## Comportement

1. **Utiliser le MCP Netdata** (natif) pour interroger les metriques
2. Si Netdata MCP non disponible, fallback sur l'API REST :
   ```
   curl http://192.168.1.162:19999/api/v1/data?chart=<chart>&after=-60
   ```

## Metriques disponibles

| Chart | Description |
|-------|-------------|
| `system.cpu` | CPU par core |
| `system.ram` | RAM utilisee/libre/cache |
| `system.io` | IO disque |
| `system.net` | Traffic reseau |
| `system.load` | Load average |
| `docker_containers.*` | Metriques par container |

## Options

- `/mon-metrics cpu` : CPU detaille
- `/mon-metrics ram` : Memoire detaillee
- `/mon-metrics io` : IO disque
- `/mon-metrics net` : Trafic reseau
- `/mon-metrics <host>` : Metriques d'un hote specifique
