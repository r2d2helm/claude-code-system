# Wizard: Déploiement Ceph sur Proxmox

## Mode d'emploi
Ce wizard guide le déploiement de Ceph (stockage distribué) sur un cluster Proxmox VE 9+. Minimum 3 nodes requis.

---

## Questions Interactives

### 1. Prérequis

**Q1.1: Combien de nodes dans le cluster?**
```
Nodes: _____ (minimum 3 pour Ceph)
```

**Q1.2: Réseau dédié Ceph?**

| Option | Réseau | Usage |
|--------|--------|-------|
| A | Réseau unique | Public = Cluster (simple, moins performant) |
| B | Deux réseaux | Public + Cluster séparés (recommandé prod) |

```
Choix: ___
Public Network:  _______________ (ex: 10.10.10.0/24)
Cluster Network: _______________ (ex: 10.10.30.0/24, si option B)
```

---

### 2. Monitors (MON)

**Q2.1: Sur quels nodes installer les monitors?**
```
[ ] Node 1: _______________
[ ] Node 2: _______________
[ ] Node 3: _______________
(recommandé: tous les nodes, nombre impair)
```

---

### 3. OSDs (Disques de Stockage)

**Q3.1: Quels disques utiliser pour les OSDs?**
```
Node 1:
  OSD 1: _______________ (ex: /dev/sdb)
  OSD 2: _______________ (ex: /dev/sdc)

Node 2:
  OSD 1: _______________
  OSD 2: _______________

Node 3:
  OSD 1: _______________
  OSD 2: _______________
```

**Q3.2: Type de disque?**

| Option | Type | DB/WAL |
|--------|------|--------|
| A | SSD/NVMe uniquement | Sur le même disque |
| B | HDD + SSD pour DB/WAL | SSD séparé pour accélérer |

```
Choix: ___
Si B, disque DB/WAL par node: _______________
```

---

### 4. Pools

**Q4.1: Créer un pool RBD (disques VM)?**
```
Nom: _______________ (ex: ceph-pool)
Taille (replicas): _____ (recommandé: 3)
Min size: _____ (recommandé: 2)
```

**Q4.2: Activer CephFS (système de fichiers)?**
```
[ ] Oui - Pour stockage partagé (ISO, templates, backups)
[ ] Non
```

---

## Génération de Commandes

### Étape 1: Initialiser Ceph

```bash
# Sur un seul node
pveceph init --network PUBLIC_NETWORK --cluster-network CLUSTER_NETWORK
```

### Étape 2: Créer les Monitors

```bash
# Sur CHAQUE node monitor
pveceph mon create
```

### Étape 3: Créer les OSDs

```bash
# Sur chaque node, pour chaque disque
pveceph osd create /dev/sdX

# Avec DB/WAL séparé
pveceph osd create /dev/sdX --db_dev /dev/nvmeY
```

### Étape 4: Créer le Pool

```bash
pveceph pool create POOL_NAME --size 3 --min_size 2 --pg_autoscale_mode on
```

### Étape 5: CephFS (optionnel)

```bash
# Créer les MDS (Metadata Servers) sur 2-3 nodes
pveceph mds create

# Créer le pool CephFS
pveceph fs create --pg_num 64 --add-storage 1
```

### Étape 6: Vérifier

```bash
ceph status
ceph osd tree
ceph df
rados bench -p POOL_NAME 30 write --no-cleanup
rados bench -p POOL_NAME 30 seq
```

---

## Configuration Production (3 Nodes)

```bash
# Init
pveceph init --network 10.10.10.0/24 --cluster-network 10.10.30.0/24

# Monitors (sur chaque node)
pveceph mon create  # répéter sur node 2 et 3

# OSDs (exemple: 2 SSD par node)
# Node 1
pveceph osd create /dev/sdb
pveceph osd create /dev/sdc
# Node 2 & 3: idem

# Pool VMs
pveceph pool create vm-pool --size 3 --min_size 2 --pg_autoscale_mode on

# CephFS pour ISOs/backups
pveceph mds create  # sur 2 nodes
pveceph fs create --pg_num 64 --add-storage 1
```

---

## Best Practices 2026

| Règle | Raison |
|-------|--------|
| Minimum 3 nodes/monitors | Quorum Ceph (PAXOS) |
| Réseau cluster dédié 10G+ | Réplication OSD intensive |
| SSD/NVMe pour OSD | Performance I/O |
| Replica 3, min_size 2 | Tolérance 1 panne, pas de perte |
| pg_autoscale_mode on | PGs gérés automatiquement |
| Pas de Ceph sur 2 nodes | Risque de split-brain |

---

## Commande Associée

Voir `/px-ceph` pour les opérations Ceph.
