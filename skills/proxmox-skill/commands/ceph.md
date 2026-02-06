# 💎 /pve-ceph - Administration Ceph

## Description
Gestion Ceph hyper-convergé sur Proxmox VE 9+ (Ceph Squid 19.2.x).

## Syntaxe
```
/pve-ceph [action] [options]
```

## Prérequis Ceph

### Minimum Production
- **Nodes**: 3 minimum (pour quorum MON)
- **OSDs**: 3+ par node (9+ total recommandé)
- **Réseau**: 10GbE dédié séparé du management
- **RAM**: 1-2 GB par OSD
- **CPU**: 1 core par OSD

### Réseau Requis
```
┌─────────────────────────────────────────────────────┐
│                   Architecture Ceph                  │
├─────────────────────────────────────────────────────┤
│  Node 1            Node 2            Node 3         │
│  ┌─────┐          ┌─────┐          ┌─────┐        │
│  │ MON │          │ MON │          │ MON │        │
│  │ MGR │          │ MGR │          │ MGR │        │
│  │ OSD │          │ OSD │          │ OSD │        │
│  │ OSD │          │ OSD │          │ OSD │        │
│  │ OSD │          │ OSD │          │ OSD │        │
│  └──┬──┘          └──┬──┘          └──┬──┘        │
│     │                │                │            │
│  ───┴────────────────┴────────────────┴────────    │
│            Réseau Public (10GbE)                    │
│  ───────────────────────────────────────────────    │
│            Réseau Cluster (10GbE optionnel)         │
└─────────────────────────────────────────────────────┘
```

## Actions Disponibles

### `status` - État du cluster Ceph
```bash
# Status complet
ceph -s

# Via Proxmox
pveceph status

# Santé détaillée
ceph health detail

# Performance temps réel
ceph -w
```

### `init` - Initialiser Ceph
```bash
# Initialiser Ceph sur le premier node
pveceph init --network 10.10.0.0/24

# Avec réseau cluster séparé
pveceph init \
  --network 10.10.0.0/24 \
  --cluster-network 10.20.0.0/24
```

### `mon create` - Créer un Monitor
```bash
# Créer MON sur node courant
pveceph mon create

# Sur node spécifique
pveceph mon create --mon-address 10.10.0.11
```

### `mgr create` - Créer un Manager
```bash
# Créer MGR
pveceph mgr create
```

### `osd create` - Créer des OSDs
```bash
# OSD simple sur disque
pveceph osd create /dev/sdb

# OSD avec DB séparé (SSD)
pveceph osd create /dev/sdb --db_dev /dev/nvme0n1

# OSD avec WAL et DB séparés
pveceph osd create /dev/sdb \
  --db_dev /dev/nvme0n1 \
  --wal_dev /dev/nvme0n1

# OSD chiffré
pveceph osd create /dev/sdb --encrypted 1
```

### `pool create` - Créer un Pool
```bash
# Pool RBD pour VMs (réplication 3)
pveceph pool create vm-pool \
  --pg_num 128 \
  --size 3 \
  --min_size 2 \
  --application rbd

# Pool avec Erasure Coding (4+2)
ceph osd pool create ec-pool 128 erasure
ceph osd pool set ec-pool allow_ec_overwrites true
ceph osd pool application enable ec-pool rbd
```

### `pool list` - Lister les pools
```bash
# Pools Proxmox
pveceph pool ls

# Détails pools
ceph osd pool ls detail

# Statistiques pools
ceph df
```

### `osd list` - Lister les OSDs
```bash
# Liste OSDs
ceph osd tree

# Status OSDs
ceph osd status

# Détails OSD spécifique
ceph osd find {osd_id}
```

### `osd out/in` - Maintenance OSD
```bash
# Retirer OSD du cluster
ceph osd out {osd_id}

# Réintégrer OSD
ceph osd in {osd_id}

# Mode noout temporaire (maintenance)
ceph osd set noout
ceph osd unset noout
```

### `osd destroy` - Supprimer un OSD
```bash
# Procedure complète destruction OSD
ceph osd out {osd_id}
ceph osd crush remove osd.{osd_id}
ceph auth del osd.{osd_id}
ceph osd rm {osd_id}

# Via Proxmox (fait tout)
pveceph osd destroy {osd_id}
```

### `crush` - Gestion CRUSH map
```bash
# Voir règles CRUSH
ceph osd crush rule ls

# Voir arbre CRUSH
ceph osd crush tree

# Créer règle réplication
ceph osd crush rule create-replicated rule-ssd default host ssd
```

## Configuration Avancée

### Tuning Performance
```bash
# Paramètres PG
ceph osd pool set {pool} pg_autoscale_mode on

# Cache tiering (si SSD+HDD)
ceph osd tier add {cold-pool} {hot-pool}
ceph osd tier cache-mode {hot-pool} writeback
ceph osd tier set-overlay {cold-pool} {hot-pool}

# Scrub scheduling
ceph osd set noscrub  # Temporaire pendant heures de pointe
ceph osd unset noscrub
```

### Intégration Proxmox Storage
```bash
# Ajouter pool Ceph comme storage
pvesm add rbd ceph-pool \
  --pool vm-pool \
  --content images,rootdir \
  --krbd 1

# Vérifier
pvesm status | grep ceph
```

### CephFS (Optionnel)
```bash
# Créer MDS
pveceph mds create

# Créer filesystem
ceph fs new cephfs cephfs_metadata cephfs_data

# Monter CephFS
mount -t ceph mon1:6789:/ /mnt/cephfs -o name=admin,secret={key}
```

## Monitoring Ceph

### Dashboard Ceph
```bash
# Activer dashboard
ceph mgr module enable dashboard
ceph dashboard create-self-signed-cert
ceph dashboard ac-user-create admin administrator

# Accès: https://{node}:8443
```

### Métriques Prometheus
```bash
# Activer module Prometheus
ceph mgr module enable prometheus

# Endpoint: http://{node}:9283/metrics
```

### Alertes
```bash
# Voir toutes les alertes
ceph health detail

# Alertes en temps réel
ceph -w

# Logs Ceph
journalctl -u ceph-mon@{node} -f
journalctl -u ceph-osd@{osd_id} -f
```

## Recovery & Maintenance

### État Recovery
```bash
# Progress recovery
ceph -s | grep recovery

# Details par pool
ceph pg stat

# PGs problématiques
ceph pg dump_stuck
```

### Replace Failed OSD
```bash
# 1. Marquer out
ceph osd out {osd_id}

# 2. Attendre rebalancing
ceph -w  # Attendre "active+clean"

# 3. Supprimer
pveceph osd destroy {osd_id} --cleanup

# 4. Remplacer disque physique

# 5. Créer nouvel OSD
pveceph osd create /dev/sdX
```

### Upgrade Ceph
```bash
# Vérifier version
ceph versions

# Upgrade via apt
apt update && apt dist-upgrade

# Redémarrer services dans l'ordre
systemctl restart ceph-mon.target
systemctl restart ceph-mgr.target
systemctl restart ceph-osd.target
```

## Commandes Diagnostiques

```bash
# Health complet
ceph health detail

# Statistiques I/O
ceph iostat

# Latence OSDs
ceph osd perf

# Utilisation
ceph df detail

# PG distribution
ceph osd pool get {pool} pg_num
ceph osd pool get {pool} pgp_num

# Logs
ceph log last 100
```

## Best Practices 2025-2026

### Infrastructure
1. **Minimum 3 nodes** avec MON sur chaque
2. **Réseau 10GbE dédié** séparé du management
3. **Jumbo frames** MTU 9000 sur réseau Ceph
4. **SSD pour journal/DB** si HDD pour data

### Pools
1. **Réplication 3** pour production (size=3, min_size=2)
2. **PG Autoscaling** activé par défaut
3. **Erasure Coding** uniquement pour archives/cold data

### Performance
1. **BlueStore** uniquement (défaut depuis Luminous)
2. **OSD par disque** (pas de RAID logiciel)
3. **NVMe pour WAL/DB** si budget permet
4. **Recovery throttling** pendant heures de pointe

### Fichiers Configuration
| Fichier | Description |
|---------|-------------|
| `/etc/pve/ceph.conf` | Configuration Ceph cluster |
| `/etc/ceph/ceph.conf` | Symlink vers config |
| `/var/lib/ceph/` | Données Ceph |
