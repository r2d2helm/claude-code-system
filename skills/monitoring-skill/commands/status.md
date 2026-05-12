---
name: mon-status
description: Dashboard complet du monitoring homelab
---

# /mon-status - Dashboard Monitoring Homelab

## Comportement

Affiche un dashboard complet combinant les donnees de Beszel et Netdata :

1. **Utiliser l'outil MCP `beszel_overview`** pour obtenir :
   - Etat de tous les systemes (UP/DOWN)
   - Top containers par CPU/RAM
   - Alertes actives

2. **Completer avec Netdata** si disponible (MCP natif) :
   - Load average
   - Network traffic
   - Anomalies detectees

3. **Formater en tableau** clair avec indicateurs visuels

## Format de sortie

```
# Homelab Monitoring Dashboard

## Systemes : X/Y online
| Hote | Status | CPU | RAM | Disk | Uptime |
|------|--------|-----|-----|------|--------|

## Top Containers (CPU)
| Container | Systeme | CPU | RAM |
|-----------|---------|-----|-----|

## Alertes actives
- [CRITICAL/WARNING] Description

## Services (Uptime Kuma)
Voir /mon-uptime pour les details
```
