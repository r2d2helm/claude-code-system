---
name: mon-alerts
description: Alertes Beszel actives et historique
---

# /mon-alerts - Alertes Monitoring

## Comportement

1. **Appeler `beszel_alerts`** via MCP
2. Separer alertes TRIGGERED des alertes OK
3. Afficher les alertes critiques en premier

## Format de sortie

```
# Alertes Monitoring

## Alertes Actives (X)
- [CRITICAL] CPU > 90% sur vm100 (valeur: 92.3%)
- [WARNING] Disk > 80% sur proxmox (valeur: 81.2%)

## Toutes les regles (Y total)
- [OK] CPU vm100
- [OK] RAM vm100
- [TRIGGERED] Disk proxmox
```
