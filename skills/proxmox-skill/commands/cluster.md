# /pve-cluster - Gestion Cluster Corosync

## Description
Gestion complète des clusters Proxmox VE : création, extension, certificats, quorum et maintenance.

## Syntaxe
```
/pve-cluster <action> [options]
```

## Actions Disponibles

| Action | Description |
|--------|-------------|
| `status` | État détaillé du cluster |
| `create` | Créer un nouveau cluster |
| `join` | Joindre un node au cluster |
| `remove` | Retirer un node du cluster |
| `nodes` | Lister les nodes avec détails |
| `expected` | Ajuster expected votes |
| `qdevice` | Gérer QDevice (2 nodes) |
| `certs` | Gestion certificats |
| `corosync` | Configuration Corosync |
| `links` | Gérer liens réseau cluster |
| `--wizard` | Assistant création cluster |

---

## Action: status

### Affichage
```
╔══════════════════════════════════════════════════════════════════════╗
║                    🏢 CLUSTER STATUS                                  ║
╠══════════════════════════════════════════════════════════════════════╣
║  Cluster Name: pve-prod                                              ║
║  Config Version: 14                                                  ║
║  Quorum: ✅ Yes (4/5 votes)                                          ║
║  Expected Votes: 5                                                   ║
║  Highest Expected: 5                                                 ║
╠══════════════════════════════════════════════════════════════════════╣
║  NODES                                                               ║
╠════════════╦═══════════╦═══════════╦═══════════╦════════════════════╣
║ Node       ║ ID        ║ State     ║ Votes     ║ IP                 ║
╠════════════╬═══════════╬═══════════╬═══════════╬════════════════════╣
║ pve01      ║ 1         ║ 🟢 online ║ 1         ║ 10.0.1.11          ║
║ pve02      ║ 2         ║ 🟢 online ║ 1         ║ 10.0.1.12          ║
║ pve03      ║ 3         ║ 🟢 online ║ 1         ║ 10.0.1.13          ║
║ pve04      ║ 4         ║ 🟡 offline║ 1         ║ 10.0.1.14          ║
║ qdevice   ║ 0         ║ 🟢 online ║ 1         ║ 10.0.1.100         ║
╚════════════╩═══════════╩═══════════╩═══════════╩════════════════════╝
```

### Commandes
```bash
# État cluster
pvecm status

# Quorum détaillé
pvecm expected

# État Corosync
corosync-quorumtool -s

# Nodes et votes
pvecm nodes
```

---

## Action: create

### Usage
```
/pve-cluster create <cluster_name> [options]
```

### Options
| Option | Description | Défaut |
|--------|-------------|--------|
| `--link0` | IP réseau principal | IP du node |
| `--link1` | IP réseau secondaire (redundancy) | - |
| `--votes` | Nombre de votes | 1 |
| `--ring0_addr` | Adresse ring0 | - |
| `--ring1_addr` | Adresse ring1 (si dual-link) | - |

### Best Practices Création

#### Réseau
```
┌─────────────────────────────────────────────────────────────┐
│  CONFIGURATION RÉSEAU RECOMMANDÉE                           │
├─────────────────────────────────────────────────────────────┤
│  Link0 (Principal):    VLAN Management (10.0.1.0/24)       │
│  Link1 (Backup):       VLAN Corosync dédié (10.0.2.0/24)   │
│  MTU:                  Identique sur tous les links        │
│  Latence:              < 2ms entre nodes                   │
│  Firewall:             Ports 5405-5412 UDP ouverts         │
└─────────────────────────────────────────────────────────────┘
```

### Commandes
```bash
# Créer cluster simple
pvecm create pve-prod

# Créer avec link unique
pvecm create pve-prod --link0 10.0.1.11

# Créer avec dual-link (haute disponibilité)
pvecm create pve-prod \
  --link0 10.0.1.11 \
  --link1 10.0.2.11

# Vérifier création
pvecm status
```

---

## Action: join

### Usage
```
/pve-cluster join <ip_existing_node> [options]
```

### Prérequis Join
```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️  PRÉREQUIS AVANT JOIN                                  │
├─────────────────────────────────────────────────────────────┤
│  1. Hostname unique et résolu sur tous les nodes           │
│  2. /etc/hosts cohérent (pas 127.0.1.1)                   │
│  3. Même version Proxmox VE (x.y.z identique)             │
│  4. Pas de VMs/CTs sur le nouveau node                    │
│  5. Connectivité réseau vérifiée (ping)                   │
│  6. SSH root fonctionnel entre nodes                       │
│  7. NTP synchronisé (< 1 seconde de delta)                │
│  8. Fingerprint SSH accepté                                │
└─────────────────────────────────────────────────────────────┘
```

### Options
| Option | Description |
|--------|-------------|
| `--link0` | IP locale pour link0 |
| `--link1` | IP locale pour link1 |
| `--fingerprint` | Fingerprint SSH du node existant |
| `--use_ssh` | Utiliser SSH au lieu de mot de passe |

### Commandes
```bash
# Obtenir fingerprint sur node existant
pvecm expected 2>/dev/null; \
openssl x509 -in /etc/pve/pve-root-ca.pem -fingerprint -sha256 -noout

# Join simple (prompt password)
pvecm add 10.0.1.11

# Join avec fingerprint et dual-link
pvecm add 10.0.1.11 \
  --fingerprint AB:CD:EF:12:34:56:78:90:... \
  --link0 10.0.1.12 \
  --link1 10.0.2.12

# Vérifier join
pvecm status
pvecm nodes
```

### Troubleshooting Join
```bash
# Si hostname invalide
hostnamectl set-hostname pve02
# Editer /etc/hosts - supprimer 127.0.1.1

# Si problème certificat
pvecm updatecerts

# Si cluster corrompu après join échoué
# (⚠️ Destructif - nouveau node seulement)
systemctl stop pve-cluster corosync
pmxcfs -l
rm -rf /etc/corosync/*
rm -rf /etc/pve/corosync.conf
rm -f /var/lib/corosync/*
killall pmxcfs
systemctl start pve-cluster
```

---

## Action: remove

### Usage
```
/pve-cluster remove <nodename>
```

### Prérequis Suppression
```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️  AVANT SUPPRESSION D'UN NODE                           │
├─────────────────────────────────────────────────────────────┤
│  1. Migrer toutes les VMs/CTs vers autres nodes           │
│  2. Supprimer ressources HA du node                        │
│  3. Retirer réplications ZFS impliquant le node           │
│  4. Supprimer OSDs Ceph si applicable                      │
│  5. Node offline ou arrêté                                 │
└─────────────────────────────────────────────────────────────┘
```

### Commandes
```bash
# Sur le node à RETIRER (avant shutdown)
# Migrer VMs
for vmid in $(qm list | awk 'NR>1 {print $1}'); do
  qm migrate $vmid pve01 --online
done

# Migrer CTs
for ctid in $(pct list | awk 'NR>1 {print $1}'); do
  pct migrate $ctid pve01
done

# Supprimer du HA
ha-manager remove vm:100
ha-manager remove ct:200

# Sur un AUTRE node du cluster (après shutdown du node)
pvecm delnode pve04

# Nettoyer fichiers résiduels
rm -rf /etc/pve/nodes/pve04

# Si le node était vivant et refusé
# (Sur le node retiré - le reset complètement)
systemctl stop pve-cluster corosync
pmxcfs -l
rm -rf /etc/corosync/*
rm -rf /etc/pve/corosync.conf
rm -f /var/lib/corosync/*
killall pmxcfs
systemctl start pve-cluster
```

---

## Action: qdevice

### Description
QDevice fournit un vote externe pour les clusters à 2 nodes, permettant le quorum même si un node tombe.

### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    QDEVICE SETUP                            │
│                                                             │
│   ┌─────────┐         ┌─────────┐         ┌─────────┐      │
│   │  pve01  │◄───────►│ QDevice │◄───────►│  pve02  │      │
│   │ Vote: 1 │         │ Vote: 1 │         │ Vote: 1 │      │
│   └─────────┘         └─────────┘         └─────────┘      │
│                                                             │
│   Total Votes: 3    Quorum: 2    (Majority voting)         │
│                                                             │
│   Si pve01 down → pve02 + QDevice = 2 votes = Quorum ✅   │
│   Si pve02 down → pve01 + QDevice = 2 votes = Quorum ✅   │
│   Si QDevice down → pve01 + pve02 = 2 votes = Quorum ✅   │
└─────────────────────────────────────────────────────────────┘
```

### Prérequis QDevice Server
- VM ou serveur physique dédié (peut être léger: 1 vCPU, 512MB RAM)
- Debian 12/13 ou Ubuntu 22.04+
- Connectivité réseau avec tous les nodes
- Port TCP 5403 ouvert
- NE PAS exécuter sur un node du cluster

### Setup QDevice Server (externe)
```bash
# Sur le serveur QDevice (Debian/Ubuntu)
apt update
apt install -y corosync-qnetd

# Démarrer le service
systemctl enable --now corosync-qnetd

# Vérifier
systemctl status corosync-qnetd
```

### Ajouter QDevice au Cluster
```bash
# Sur un node du cluster PVE
pvecm qdevice setup 10.0.1.100

# Vérifier intégration
pvecm status

# Voir votes
corosync-quorumtool -s
```

### Supprimer QDevice
```bash
# Retirer du cluster
pvecm qdevice remove

# Sur le serveur QDevice (optionnel)
systemctl stop corosync-qnetd
apt remove corosync-qnetd
```

---

## Action: certs

### Description
Gestion des certificats SSL du cluster Proxmox.

### Commandes
```bash
# Mettre à jour certificats sur tous les nodes
pvecm updatecerts

# Voir certificats actuels
openssl x509 -in /etc/pve/pve-root-ca.pem -text -noout
openssl x509 -in /etc/pve/local/pve-ssl.pem -text -noout

# Vérifier expiration
openssl x509 -in /etc/pve/local/pve-ssl.pem -enddate -noout

# Renouveler certificat node
pvecm updatecerts --force

# Fingerprint cluster (pour join)
pvesh get /cluster/config/join --output-format yaml | grep fingerprint
```

### Certificats Custom (Let's Encrypt / ACME)
```bash
# Configurer ACME
pvenode acme account register default mail@example.com

# Ajouter plugin DNS (exemple Cloudflare)
pvenode acme plugin add dns cloudflare \
  --api CF_Account_ID=xxx \
  --api CF_Token=xxx \
  --data domain=pve.example.com

# Commander certificat
pvenode acme cert order

# Vérifier
pvenode acme cert list
```

---

## Action: corosync

### Description
Configuration avancée de Corosync (timeouts, transport, crypto).

### Fichier Configuration
```bash
# Voir config actuelle
cat /etc/pve/corosync.conf

# Structure typique
logging {
  debug: off
  to_syslog: yes
}

totem {
  cluster_name: pve-prod
  config_version: 14
  interface {
    linknumber: 0
  }
  ip_version: ipv4-6
  link_mode: passive
  secauth: on
  version: 2
}

nodelist {
  node {
    name: pve01
    nodeid: 1
    quorum_votes: 1
    ring0_addr: 10.0.1.11
  }
  node {
    name: pve02
    nodeid: 2
    quorum_votes: 1
    ring0_addr: 10.0.1.12
  }
}

quorum {
  provider: corosync_votequorum
}
```

### Ajuster Timeouts (réseau lent)
```bash
# Editer via GUI ou directement
# /etc/pve/corosync.conf dans section totem:
totem {
  token: 5000          # Default 1000ms, augmenter si latence
  token_retransmits_before_loss_const: 10
  join: 60             # Temps pour rejoindre
  consensus: 6000      # Doit être > token
  max_messages: 20
}

# Après modification
systemctl restart corosync
```

---

## Action: links

### Description
Gestion des liens réseau redondants du cluster.

### Voir Liens Actuels
```bash
# Afficher configuration liens
pvecm status
corosync-cfgtool -s

# Vérifier connectivité
corosync-cfgtool -R  # Ring status
```

### Ajouter Link Redondant
```bash
# Ajouter link1 à un cluster existant
# Editer /etc/pve/corosync.conf
# Ajouter ring1_addr à chaque node

# Puis redémarrer Corosync sur chaque node
# (un par un pour éviter perte quorum)
systemctl restart corosync
```

### Tester Failover
```bash
# Simuler perte link0
ip link set vmbr0 down

# Vérifier failover sur link1
pvecm status

# Restaurer
ip link set vmbr0 up
```

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

---

## Commandes Rapides

```bash
# État cluster
pvecm status

# Liste nodes
pvecm nodes

# Créer cluster
pvecm create <name>

# Rejoindre cluster
pvecm add <ip>

# Retirer node
pvecm delnode <nodename>

# QDevice setup
pvecm qdevice setup <qdevice_ip>

# Mettre à jour certificats
pvecm updatecerts

# Voir config Corosync
cat /etc/pve/corosync.conf

# Ring status
corosync-cfgtool -s

# Quorum status
corosync-quorumtool -s
```
