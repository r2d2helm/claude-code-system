---
name: mon-notify
description: Tester une notification ntfy
---

# /mon-notify - Test Notification

## Comportement

Envoyer une notification test via ntfy pour verifier le pipeline d'alertes.

## Usage

- `/mon-notify` : envoie un message test sur le topic monitoring-info
- `/mon-notify <message>` : envoie un message personnalise
- `/mon-notify --topic <topic>` : envoie sur un topic specifique

## Implementation

```bash
# Test simple
ssh root@192.168.1.162 "curl -d 'Test notification from Claude Code' http://localhost:8084/monitoring-info"

# Avec priorite
ssh root@192.168.1.162 "curl -H 'Priority: high' -H 'Title: Alert Test' -d 'Message' http://localhost:8084/monitoring-critical"
```

## Topics ntfy

| Topic | Usage |
|-------|-------|
| `monitoring-critical` | Alertes critiques (host down, disk full) |
| `monitoring-warning` | Avertissements (CPU/RAM eleve) |
| `monitoring-info` | Informations, tests |

## ntfy Web UI

- URL : http://192.168.1.162:8084
