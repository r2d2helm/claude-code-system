---
name: mon-health
description: Sante de la stack monitoring
---

# /mon-health - Sante Stack Monitoring

## Comportement

Verifie que tous les composants de la stack monitoring fonctionnent correctement.

## Checks

1. **Containers Docker** (6) :
   ```bash
   ssh root@192.168.1.162 "docker ps --format '{{.Names}} {{.Status}}' | grep -E '(beszel|netdata|uptime|dozzle|ntfy)'"
   ```

2. **APIs accessibles** :
   ```bash
   # Beszel Hub
   curl -s http://192.168.1.162:8091/api/health
   # Netdata
   curl -s http://192.168.1.162:19999/api/v1/info
   # ntfy
   curl -s http://192.168.1.162:8084/v1/health
   # Uptime Kuma
   curl -s http://192.168.1.162:3003/api/status-page/default
   ```

3. **Agents connectes** :
   - Beszel : verifier status != "down" via API
   - Netdata : verifier que les metriques remontent

4. **MCP Servers** :
   - beszel-assistant : tester un appel beszel_systems
   - netdata MCP : tester si les outils sont disponibles

## Format de sortie

```
# Stack Monitoring Health

| Composant | Status | Details |
|-----------|--------|---------|
| Beszel Hub | OK | http://192.168.1.162:8091 |
| Beszel Agent | OK | vm100 connected |
| Netdata | OK | v2.x, 800+ metriques |
| Uptime Kuma | OK | 12 monitors |
| Dozzle | OK | http://192.168.1.162:8082 |
| ntfy | OK | 3 topics |
| MCP Beszel | OK | 5 outils |
| MCP Netdata | OK | outils natifs |

Score: 8/8 composants healthy
```
