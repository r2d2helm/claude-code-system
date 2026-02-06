# /pve-status - Vue d'ensemble Proxmox

## Description
Affiche une vue d'ensemble complète du cluster Proxmox, incluant l'état des nodes,
les ressources, le stockage, et les services critiques.

## Syntaxe
```
/pve-status [scope] [options]
```

## Scopes Disponibles

| Scope | Description |
|-------|-------------|
| `(défaut)` | Vue d'ensemble complète |
| `nodes` | État détaillé des nodes |
| `resources` | Ressources VMs/CTs |
| `storage` | État du stockage |
| `ceph` | Santé Ceph (si configuré) |
| `ha` | État haute disponibilité |
| `tasks` | Tâches en cours/récentes |

## Options

| Option | Description |
|--------|-------------|
| `--node <name>` | Filtrer par node spécifique |
| `--json` | Sortie JSON |
| `--watch` | Rafraîchissement continu (5s) |
| `--brief` | Vue compacte |

## Affichage Standard

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  🏢 PROXMOX CLUSTER STATUS                                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Cluster: production-cluster     Version: 9.1.2     Nodes: 3/3 Online       ║
║  Quorum: ✅ OK (3/3)             Uptime Leader: pve01 (45d 12h)             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─ NODE: pve01 ──────────────────────────────────────────────────────────┐ ║
║  │ Status: 🟢 Online    IP: 10.0.0.11    Kernel: 6.17.2-1-pve            │ ║
║  │ CPU:  ████████░░░░░░░░ 48%  (24/48 cores)                             │ ║
║  │ RAM:  ██████████░░░░░░ 62%  (198/320 GB)                              │ ║
║  │ VMs:  12 running | CTs: 8 running | HA: 5 services                    │ ║
║  │ Load: 2.45 1.82 1.54                                                  │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  ┌─ NODE: pve02 ──────────────────────────────────────────────────────────┐ ║
║  │ Status: 🟢 Online    IP: 10.0.0.12    Kernel: 6.17.2-1-pve            │ ║
║  │ CPU:  ██████░░░░░░░░░░ 35%  (24/48 cores)                             │ ║
║  │ RAM:  ████████░░░░░░░░ 51%  (163/320 GB)                              │ ║
║  │ VMs:  10 running | CTs: 5 running | HA: 4 services                    │ ║
║  │ Load: 1.85 1.42 1.28                                                  │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  ┌─ NODE: pve03 ──────────────────────────────────────────────────────────┐ ║
║  │ Status: 🟢 Online    IP: 10.0.0.13    Kernel: 6.17.2-1-pve            │ ║
║  │ CPU:  ████░░░░░░░░░░░░ 28%  (24/48 cores)                             │ ║
║  │ RAM:  ██████░░░░░░░░░░ 45%  (144/320 GB)                              │ ║
║  │ VMs:  8 running  | CTs: 6 running | HA: 3 services                    │ ║
║  │ Load: 1.22 0.98 0.85                                                  │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  💾 STOCKAGE                                                                 ║
║  ┌───────────────┬──────────┬─────────────────┬─────────────────────────┐   ║
║  │ Storage       │ Type     │ Usage           │ Status                  │   ║
║  ├───────────────┼──────────┼─────────────────┼─────────────────────────┤   ║
║  │ local-zfs     │ ZFS      │ 45% (2.1/4.8T)  │ 🟢 ONLINE               │   ║
║  │ ceph-pool     │ RBD      │ 38% (15/40T)    │ 🟢 HEALTH_OK            │   ║
║  │ pbs-store     │ PBS      │ 52% (8.3/16T)   │ 🟢 Connected            │   ║
║  │ nfs-backup    │ NFS      │ 61% (6.1/10T)   │ 🟢 Mounted              │   ║
║  └───────────────┴──────────┴─────────────────┴─────────────────────────┘   ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  🔄 HA STATUS                                                                ║
║  Groups: 2 active | Services: 12 managed | Fencing: ✅ Enabled              ║
║  Last Failover: 2025-01-15 03:42 (pve02→pve03, auto-recovery)               ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  📊 CLUSTER TOTALS                                                           ║
║  VMs: 30 running / 35 total | CTs: 19 running / 22 total                    ║
║  vCPUs: 156 allocated | RAM: 505 GB allocated | Storage: 28 TB used         ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Commandes Bash Utilisées

```bash
# ═══════════════════════════════════════════════════════════════════════════
# STATUS CLUSTER
# ═══════════════════════════════════════════════════════════════════════════

# Version Proxmox
pveversion -v

# Status cluster complet
pvecm status

# Status quorum
pvecm expected 1  # Vérifier quorum

# Liste nodes avec status
pvesh get /nodes --output-format=json-pretty | jq '.[] | {
  node: .node,
  status: .status,
  cpu: (.cpu * 100 | floor),
  maxcpu: .maxcpu,
  mem_used_gb: (.mem / 1073741824 | floor),
  mem_total_gb: (.maxmem / 1073741824 | floor),
  uptime_days: (.uptime / 86400 | floor)
}'

# ═══════════════════════════════════════════════════════════════════════════
# STATUS NODES DÉTAILLÉ
# ═══════════════════════════════════════════════════════════════════════════

# Info node spécifique
pvesh get /nodes/pve01/status --output-format=json-pretty

# CPU info
cat /proc/cpuinfo | grep "model name" | head -1

# Load average
cat /proc/loadavg

# Kernel version
uname -r

# ═══════════════════════════════════════════════════════════════════════════
# STATUS RESSOURCES
# ═══════════════════════════════════════════════════════════════════════════

# Toutes les ressources cluster
pvesh get /cluster/resources --output-format=json | jq

# Filtrer par type
pvesh get /cluster/resources --type vm --output-format=json   # VMs uniquement
pvesh get /cluster/resources --type node --output-format=json  # Nodes
pvesh get /cluster/resources --type storage --output-format=json  # Stockage

# Compter VMs/CTs par état
pvesh get /cluster/resources --type vm --output-format=json | \
  jq 'group_by(.status) | map({status: .[0].status, count: length})'

# ═══════════════════════════════════════════════════════════════════════════
# STATUS STOCKAGE
# ═══════════════════════════════════════════════════════════════════════════

# Liste stockages avec usage
pvesm status

# Détails stockage JSON
pvesh get /storage --output-format=json-pretty

# Usage stockage spécifique
pvesh get /nodes/pve01/storage/local-zfs/status

# ═══════════════════════════════════════════════════════════════════════════
# STATUS CEPH (si configuré)
# ═══════════════════════════════════════════════════════════════════════════

# Santé Ceph
ceph -s

# Status cluster Ceph
ceph health detail

# OSDs status
ceph osd tree

# Pools
ceph df

# ═══════════════════════════════════════════════════════════════════════════
# STATUS HA
# ═══════════════════════════════════════════════════════════════════════════

# Status HA manager
ha-manager status

# Groupes HA
pvesh get /cluster/ha/groups --output-format=json-pretty

# Ressources HA
pvesh get /cluster/ha/resources --output-format=json-pretty

# Status services HA
pvesh get /cluster/ha/status/current --output-format=json-pretty

# ═══════════════════════════════════════════════════════════════════════════
# TÂCHES RÉCENTES
# ═══════════════════════════════════════════════════════════════════════════

# Tâches en cours
pvesh get /cluster/tasks --output-format=json | jq '.[] | select(.status == "running")'

# 10 dernières tâches
pvesh get /nodes/pve01/tasks --output-format=json | jq '.[0:10]'

# Tâches échouées
pvesh get /cluster/tasks --output-format=json | jq '.[] | select(.status == "error")'
```

## Script Diagnostic Complet

```bash
#!/bin/bash
# pve-status-full.sh - Diagnostic complet cluster Proxmox

echo "═══════════════════════════════════════════════════════════════"
echo " PROXMOX VE CLUSTER STATUS - $(date)"
echo "═══════════════════════════════════════════════════════════════"

echo -e "\n[1/7] VERSION INFO"
pveversion -v

echo -e "\n[2/7] CLUSTER STATUS"
pvecm status 2>/dev/null || echo "Mode standalone (pas de cluster)"

echo -e "\n[3/7] NODES STATUS"
pvesh get /nodes --output-format=json-pretty 2>/dev/null | \
  jq -r '.[] | "  \(.node): \(.status) | CPU: \(.cpu*100|floor)% | RAM: \(.mem/1073741824|floor)/\(.maxmem/1073741824|floor) GB"'

echo -e "\n[4/7] STORAGE STATUS"
pvesm status

echo -e "\n[5/7] VM/CT COUNT"
echo "  VMs running: $(qm list 2>/dev/null | grep -c running || echo 0)"
echo "  VMs stopped: $(qm list 2>/dev/null | grep -c stopped || echo 0)"
echo "  CTs running: $(pct list 2>/dev/null | grep -c running || echo 0)"
echo "  CTs stopped: $(pct list 2>/dev/null | grep -c stopped || echo 0)"

echo -e "\n[6/7] HA STATUS"
ha-manager status 2>/dev/null || echo "  HA non configuré"

echo -e "\n[7/7] CEPH STATUS"
ceph -s 2>/dev/null || echo "  Ceph non configuré"

echo -e "\n═══════════════════════════════════════════════════════════════"
echo " STATUS CHECK COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
```

## Alertes et Indicateurs

| Indicateur | 🟢 OK | 🟡 Warning | 🔴 Critical |
|------------|-------|------------|-------------|
| CPU | < 70% | 70-85% | > 85% |
| RAM | < 80% | 80-90% | > 90% |
| Storage | < 70% | 70-85% | > 85% |
| Quorum | N/N nodes | N-1 nodes | < majority |
| Ceph | HEALTH_OK | HEALTH_WARN | HEALTH_ERR |

## Exemples d'Utilisation

```bash
# Vue complète
/pve-status

# État des nodes uniquement
/pve-status nodes

# Stockage avec détails
/pve-status storage --json

# Surveillance continue
/pve-status --watch

# Node spécifique
/pve-status --node pve01
```

## Voir Aussi
- `/pve-cluster` - Gestion cluster
- `/pve-ha` - Haute disponibilité
- `/pve-monitor` - Monitoring avancé
- `/pve-diag` - Diagnostic et dépannage
