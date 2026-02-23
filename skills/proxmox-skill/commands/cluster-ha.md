# /pve-cluster-ha - Haute Disponibilité et Bonnes Pratiques Cluster

## Description
Bonnes pratiques HA, règles de quorum, maintenance de nodes, fencing et troubleshooting avancé du cluster Proxmox VE.

> Voir aussi : [cluster.md](cluster.md) pour la création, join, remove, qdevice, certs et configuration Corosync.

---

## Wizard: Création Cluster Multi-Nodes

### Étape 1: Prérequis
```
┌─────────────────────────────────────────────────────────────┐
│  📋 CHECKLIST PRÉ-CLUSTER                                  │
├─────────────────────────────────────────────────────────────┤
│  [ ] Tous les nodes ont la même version PVE               │
│  [ ] Hostnames uniques et résolus                          │
│  [ ] /etc/hosts configuré (pas de 127.0.1.1)              │
│  [ ] NTP synchronisé sur tous les nodes                    │
│  [ ] Réseau management opérationnel                        │
│  [ ] Ports firewall ouverts (5405-5412 UDP, 22 TCP)       │
│  [ ] SSH root fonctionnel entre nodes                      │
│  [ ] Pas de VMs sur les nouveaux nodes                     │
└─────────────────────────────────────────────────────────────┘
```

### Étape 2: Configuration Réseau
```
Configuration réseau cluster:

[ ] Liens simples (1 réseau)
    └─ Pour: Homelab, environnements test

[x] Liens redondants (2 réseaux)
    └─ Pour: Production, haute disponibilité
    └─ Link0: VLAN Management
    └─ Link1: VLAN Corosync dédié

Votre choix: Liens redondants
```

### Étape 3: Créer sur Premier Node
```bash
# Sur pve01 (premier node)
pvecm create pve-prod \
  --link0 10.0.1.11 \
  --link1 10.0.2.11
```

### Étape 4: Joindre Autres Nodes
```bash
# Sur pve02
pvecm add 10.0.1.11 \
  --link0 10.0.1.12 \
  --link1 10.0.2.12

# Sur pve03
pvecm add 10.0.1.11 \
  --link0 10.0.1.13 \
  --link1 10.0.2.13
```

### Étape 5: Vérification
```bash
# État cluster
pvecm status

# Tous les nodes visibles
pvecm nodes

# Quorum OK
corosync-quorumtool -s
```

### Étape 6: QDevice (Optionnel - 2 nodes)
```bash
# Si cluster 2 nodes seulement
pvecm qdevice setup 10.0.1.100
```

---

## Bonnes Pratiques Cluster

### Architecture Recommandée
```
┌─────────────────────────────────────────────────────────────┐
│  ARCHITECTURE CLUSTER PRODUCTION                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Minimum: 3 nodes (quorum natif)                           │
│  Optimal: 5 nodes (tolérance 2 pannes)                     │
│  Maximum: 32 nodes                                          │
│                                                             │
│  Réseau:                                                    │
│  • Management: 1GbE minimum, VLAN dédié                    │
│  • Corosync: Liens redondants recommandés                  │
│  • Stockage: 10GbE+ dédié (Ceph, NFS)                     │
│  • VMs: Selon besoins                                      │
│                                                             │
│  Latence: < 2ms entre nodes                                │
│  NTP: Obligatoire, < 1s de delta                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Règles de Quorum
```
┌─────────────────────────────────────────────────────────────┐
│  RÈGLES QUORUM                                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Formule: Quorum = (N / 2) + 1                             │
│                                                             │
│  2 nodes: Quorum = 2 → ⚠️ QDevice OBLIGATOIRE             │
│  3 nodes: Quorum = 2 → Tolère 1 panne                      │
│  4 nodes: Quorum = 3 → Tolère 1 panne                      │
│  5 nodes: Quorum = 3 → Tolère 2 pannes                     │
│                                                             │
│  Sans quorum: Cluster READ-ONLY (pas de modifications)     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Maintenance Node
```bash
# Avant maintenance d'un node
# 1. Migrer les VMs
qm migrate <vmid> <target_node> --online

# 2. Mode maintenance HA
ha-manager set vm:100 --state disabled

# 3. Si besoin forcer quorum (DANGER - dernier recours)
pvecm expected 1

# Après maintenance
# 1. Réactiver HA
ha-manager set vm:100 --state started

# 2. Vérifier cluster
pvecm status
```

---

## Fencing et Isolation de Nodes

### Description
Le fencing (isolation) empêche un node défaillant de corrompre les données partagées. Proxmox HA utilise des watchdogs hardware et des fence agents.

### Types de Fencing Proxmox
```
┌─────────────────────────────────────────────────────────────┐
│  MÉCANISMES DE FENCING                                      │
├─────────────────────────────────────────────────────────────┤
│  1. Watchdog (défaut): /dev/watchdog                        │
│     └─ Si le node perd le quorum et ne répond plus         │
│        → Le watchdog redémarre le node automatiquement      │
│                                                             │
│  2. IPMI/iDRAC/iLO: Coupe alimentation via BMC             │
│     └─ Plus fiable, nécessite accès BMC configuré          │
│                                                             │
│  3. QEMU Guest Agent fence: Pour VMs imbriquées            │
└─────────────────────────────────────────────────────────────┘
```

### Configurer Watchdog HA
```bash
# Vérifier watchdog actif
systemctl status pve-ha-lrm

# Configuration HA dans /etc/pve/ha/crm-commands
ha-manager config

# Voir ressources HA
ha-manager status
```

### Fence Agent IPMI (exemple)
```bash
# Installer fence agents
apt install -y fence-agents

# Tester fencing IPMI
fence_ipmilan -a 10.0.0.10 -l admin -p password -o status

# Configurer dans HA resource
# Via GUI : Datacenter > HA > Fencing
```

---

## Troubleshooting Cluster

### Problème: Node ne peut pas join
```bash
# Vérifier hostname
hostname
cat /etc/hostname
cat /etc/hosts  # Pas de 127.0.1.1

# Vérifier connectivité
ping 10.0.1.11
ssh root@10.0.1.11

# Vérifier ports
nc -zvu 10.0.1.11 5405

# Vérifier versions
pveversion -v
```

### Problème: Perte de quorum
```bash
# Voir état
pvecm status
corosync-quorumtool -s

# Si nodes down attendus temporairement
pvecm expected <nombre_nodes_actifs>

# Si split-brain (éviter absolument)
# Choisir UN côté, sur les autres:
systemctl stop pve-cluster corosync
```

### Problème: Corosync ne démarre pas
```bash
# Logs
journalctl -u corosync -f

# Vérifier config
corosync-cfgtool -c

# Réinitialiser un node problématique (DESTRUCTIF)
systemctl stop pve-cluster
pmxcfs -l
rm /etc/corosync/corosync.conf
rm /var/lib/corosync/*
systemctl start pve-cluster
# Puis re-join le cluster
```

### Problème: Certificats invalides
```bash
# Forcer renouvellement
pvecm updatecerts --force

# Si certificat root corrompu (DANGER)
# Backup d'abord!
cp -a /etc/pve /root/pve-backup
pvecm updatecerts
```
