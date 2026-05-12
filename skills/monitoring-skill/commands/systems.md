---
name: mon-systems
description: Liste tous les hotes monitores avec metriques
---

# /mon-systems - Liste des Systemes

## Comportement

1. **Appeler `beszel_systems`** via MCP pour lister tous les hotes
2. Pour chaque systeme, afficher : nom, status, CPU%, RAM%, Disk%, uptime
3. Signaler les systemes DOWN en priorite

## Format de sortie

```
# Systemes Monitores

| Hote | Status | CPU | RAM | Disk | Uptime |
|------|--------|-----|-----|------|--------|
| vm100 | [UP] | 12.3% | 20.1% | 45.2% | 5d 3h |
| proxmox | [UP] | 5.1% | 62.3% | 38.1% | 30d 2h |
```

## Variantes

- `/mon-systems detail <nom>` : appeler `beszel_system_detail` pour un hote specifique
