# /pve-ha - Haute Disponibilite

## Description
Configuration et gestion de la haute disponibilite Proxmox VE.
Inclut groupes HA, ressources, fencing, QDevice et affinity rules (PVE 9+).

## Syntaxe
```
/pve-ha <action> [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `status` | `/pve-ha status` | Etat HA complet |
| `enable` | `/pve-ha enable <vmid>` | Activer HA pour VM/CT |
| `disable` | `/pve-ha disable <vmid>` | Desactiver HA |
| `migrate` | `/pve-ha migrate <vmid> <node>` | Migration manuelle |
| `group` | `/pve-ha group <action>` | Gerer groupes |
| `rules` | `/pve-ha rules <action>` | Affinity rules (PVE 9+) |
| `fencing` | `/pve-ha fencing` | Config fencing |
| `maintenance` | `/pve-ha maintenance <node>` | Mode maintenance |
| `qdevice` | `/pve-ha qdevice` | Gerer QDevice |

## Affichage Status HA

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║  🔄 HIGH AVAILABILITY STATUS                                                     ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  Cluster: production-cluster    Quorum: ✅ OK (3/3)    Fencing: ✅ Enabled      ║
║                                                                                  ║
║  ┌─ HA MANAGER ──────────────────────────────────────────────────────────────┐  ║
║  │ Manager Status: 🟢 Active on pve01                                        │  ║
║  │ Services Managed: 12                                                      │  ║
║  │ Last Failover: 2025-01-15 03:42 (VM 104: pve02 → pve03)                  │  ║
║  └───────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                  ║
║  ┌─ HA GROUPS ───────────────────────────────────────────────────────────────┐  ║
║  │ Group           │ Nodes              │ Priority │ Restricted │ Resources  │  ║
║  │─────────────────┼────────────────────┼──────────┼────────────┼────────────│  ║
║  │ production      │ pve01,pve02,pve03  │ 1,2,3    │ No         │ 8          │  ║
║  │ database        │ pve03,pve01        │ 1,2      │ Yes        │ 3          │  ║
║  │ web             │ pve01,pve02        │ 1,1      │ No         │ 4          │  ║
║  └───────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                  ║
║  ┌─ HA RESOURCES ────────────────────────────────────────────────────────────┐  ║
║  │ SID       │ State    │ Node   │ Group       │ Request │ Max Restart      │  ║
║  │───────────┼──────────┼────────┼─────────────┼─────────┼──────────────────│  ║
║  │ vm:100    │ started  │ pve01  │ production  │ started │ 3                │  ║
║  │ vm:101    │ started  │ pve02  │ production  │ started │ 3                │  ║
║  │ vm:104    │ started  │ pve03  │ database    │ started │ 1                │  ║
║  │ vm:105    │ started  │ pve01  │ database    │ started │ 1                │  ║
║  │ ct:1001   │ started  │ pve01  │ web         │ started │ 3                │  ║
║  │ ct:1002   │ started  │ pve02  │ web         │ started │ 3                │  ║
║  └───────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                  ║
║  ┌─ AFFINITY RULES (PVE 9+) ─────────────────────────────────────────────────┐  ║
║  │ Rule            │ Type           │ Resources        │ Status             │  ║
║  │─────────────────┼────────────────┼──────────────────┼────────────────────│  ║
║  │ db-separate     │ anti-affinity  │ vm:104,vm:105    │ 🟢 Satisfied       │  ║
║  │ web-together    │ affinity       │ ct:1001,ct:1002  │ 🟡 Best-effort     │  ║
║  │ db-prefer-pve03 │ node-affinity  │ vm:104           │ 🟢 Satisfied       │  ║
║  └───────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                  ║
║  ┌─ NODES STATUS ────────────────────────────────────────────────────────────┐  ║
║  │ Node    │ Status   │ Maintenance │ HA Services │ Fencing              │  ║
║  │─────────┼──────────┼─────────────┼─────────────┼──────────────────────│  ║
║  │ pve01   │ 🟢 online │ No          │ 4           │ watchdog + ipmi      │  ║
║  │ pve02   │ 🟢 online │ No          │ 3           │ watchdog + ipmi      │  ║
║  │ pve03   │ 🟢 online │ No          │ 5           │ watchdog + ipmi      │  ║
║  └───────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

## Commandes Bash

### Status HA

```bash
# Status complet HA Manager
ha-manager status

# Status détaillé JSON
pvesh get /cluster/ha/status/current --output-format=json-pretty

# Status d'une ressource spécifique
pvesh get /cluster/ha/resources/vm:100 --output-format=json-pretty

# Logs HA
journalctl -u pve-ha-lrm -f  # Local Resource Manager
journalctl -u pve-ha-crm -f  # Cluster Resource Manager
```

### Activer HA sur VM/CT

```bash
# Activer HA sur VM
ha-manager add vm:100 --state started --group production

# Activer HA sur CT
ha-manager add ct:1001 --state started --group web

# Options complètes
ha-manager add vm:100 \
  --state started \
  --group production \
  --max_restart 3 \
  --max_relocate 3 \
  --comment "Web server principal"

# Modifier ressource HA
ha-manager set vm:100 --state stopped
ha-manager set vm:100 --group database

# Désactiver HA
ha-manager remove vm:100
```

### Groupes HA

```bash
# Créer groupe HA
pvesh create /cluster/ha/groups \
  --group production \
  --nodes "pve01:1,pve02:2,pve03:3" \
  --comment "Production workloads"

# Groupe avec restriction (VMs uniquement sur ces nodes)
pvesh create /cluster/ha/groups \
  --group database \
  --nodes "pve03:1,pve01:2" \
  --restricted 1 \
  --nofailback 0

# Groupe sans failback automatique
pvesh create /cluster/ha/groups \
  --group critical \
  --nodes "pve01:1,pve02:2,pve03:3" \
  --nofailback 1

# Lister groupes
pvesh get /cluster/ha/groups --output-format=json-pretty

# Modifier groupe
pvesh set /cluster/ha/groups/production --nodes "pve01:1,pve02:1,pve03:2"

# Supprimer groupe
pvesh delete /cluster/ha/groups/old-group
```

### Affinity Rules (PVE 9+)

```bash
# ═══════════════════════════════════════════════════════════════════════════
# AFFINITY RULES - NOUVEAUTÉ PVE 9.0+
# ═══════════════════════════════════════════════════════════════════════════

# Anti-affinity: VMs sur nodes différents (ex: DB master/replica)
pvesh create /cluster/ha/rules \
  --rule db-separate \
  --type negative \
  --resources "vm:104,vm:105" \
  --strict 1 \
  --comment "DB master et replica sur nodes différents"

# Affinity: VMs ensemble sur même node (best-effort)
pvesh create /cluster/ha/rules \
  --rule web-together \
  --type positive \
  --resources "ct:1001,ct:1002" \
  --strict 0 \
  --comment "Web containers ensemble si possible"

# Node affinity: VM préfère certains nodes
pvesh create /cluster/ha/rules \
  --rule db-prefer-pve03 \
  --type location \
  --resources "vm:104" \
  --nodes "pve03:100,pve01:50,pve02:10"

# Lister règles
pvesh get /cluster/ha/rules --output-format=json-pretty

# Modifier règle
pvesh set /cluster/ha/rules/db-separate --strict 0

# Supprimer règle
pvesh delete /cluster/ha/rules/old-rule

# ══ NOTES AFFINITY RULES ══
# strict=1: Règle obligatoire, sinon VM ne démarre pas
# strict=0: Best-effort, VM démarre même si non satisfait
# negative: Anti-affinity (resources séparées)
# positive: Affinity (resources ensemble)
# location: Préférence de node avec scores
```

### Fencing

```bash
# ═══════════════════════════════════════════════════════════════════════════
# FENCING - OBLIGATOIRE EN PRODUCTION
# ═══════════════════════════════════════════════════════════════════════════

# Vérifier watchdog
cat /dev/watchdog
dmesg | grep -i watchdog

# Configurer IPMI fencing
pvesh set /cluster/ha/fence/pve01 \
  --type ipmi \
  --ip 10.0.0.101 \
  --username admin \
  --password "ipmipass"

# Configurer fencing agent personnalisé
cat > /etc/pve/ha/fence.cfg << 'EOF'
pve01: ipmi,ip=10.0.0.101,username=admin,password=***
pve02: ipmi,ip=10.0.0.102,username=admin,password=***
pve03: ipmi,ip=10.0.0.103,username=admin,password=***
EOF

# Test fencing (ATTENTION: va shutdown le node!)
# fence_ipmi -a 10.0.0.101 -l admin -p pass -o status

# Watchdog software (solution de base)
# Actif par défaut via pve-ha-lrm

# ══ FENCING BEST PRACTICES ══
# - IPMI/iLO/DRAC: Recommandé pour serveurs
# - Watchdog: Minimum requis, backup
# - Double fencing: IPMI + watchdog = plus sûr
# - Tester régulièrement!
```

### QDevice (Clusters 2 Nodes)

```bash
# ═══════════════════════════════════════════════════════════════════════════
# QDEVICE - Pour clusters 2 nodes ou quorum externe
# ═══════════════════════════════════════════════════════════════════════════

# Sur le serveur QDevice (Debian/Ubuntu externe au cluster)
apt install corosync-qdevice corosync-qnetd

# Configurer qnetd
systemctl enable corosync-qnetd
systemctl start corosync-qnetd

# Sur les nodes Proxmox
pvecm qdevice setup 192.168.1.200

# Vérifier status
pvecm status
# Doit montrer "Qdevice" dans la sortie

# Supprimer QDevice
pvecm qdevice remove

# ══ POURQUOI QDEVICE? ══
# Cluster 2 nodes: Pas de quorum si 1 node tombe
# QDevice: Fournit un "vote" externe
# Permet failover automatique avec seulement 2 nodes
```

### Mode Maintenance

```bash
# Activer maintenance (migre VMs, désactive node pour HA)
ha-manager crm-command node-maintenance enable pve02

# Désactiver maintenance
ha-manager crm-command node-maintenance disable pve02

# Status maintenance
pvesh get /cluster/ha/status/manager_status | jq '.node_maintenance'

# Alternative: cgroup migration manuelle
for vm in $(qm list | awk '/pve02/{print $1}'); do
  qm migrate $vm pve01 --online
done
```

### Migration HA

```bash
# Migration manuelle (HA gère le tracking)
ha-manager migrate vm:100 pve02

# Relocaliser ressource (comme migrate mais urgent)
ha-manager relocate vm:100 pve03

# Request état spécifique
ha-manager set vm:100 --state stopped
ha-manager set vm:100 --state started
```

## Voir Aussi
- `/pve-cluster` - Gestion cluster Corosync
- `/pve-storage` - Stockage partage
- `/pve-migrate` - Migration VMs

> Voir aussi : [[ha-advanced]]
