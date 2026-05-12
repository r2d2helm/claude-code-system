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

> Voir aussi : [cluster-ha.md](cluster-ha.md) pour les règles de quorum, bonnes pratiques HA, troubleshooting et fencing.

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
│  2. /etc/hosts cohérent (pas de 127.0.1.1)                │
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
# Hostname invalide → hostnamectl set-hostname pve02 + corriger /etc/hosts
# Problème certificat → pvecm updatecerts
# Join échoué (DESTRUCTIF, nouveau node seulement) :
systemctl stop pve-cluster corosync && pmxcfs -l
rm -rf /etc/corosync/* /etc/pve/corosync.conf /var/lib/corosync/*
killall pmxcfs && systemctl start pve-cluster
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

# Si le node était vivant et refusé (DESTRUCTIF - sur le node retiré) :
systemctl stop pve-cluster corosync && pmxcfs -l
rm -rf /etc/corosync/* /etc/pve/corosync.conf /var/lib/corosync/*
killall pmxcfs && systemctl start pve-cluster
```

---

## Action: qdevice

### Description
QDevice fournit un vote externe pour les clusters à 2 nodes, permettant le quorum même si un node tombe.

Architecture : pve01 (vote:1) + QDevice (vote:1) + pve02 (vote:1) = 3 votes, quorum=2. Chaque node peut tomber sans perdre le quorum.

### Prérequis QDevice Server
VM dédiée légère (1 vCPU, 512MB RAM), Debian/Ubuntu, port TCP 5403 ouvert, NE PAS exécuter sur un node du cluster.

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
pvecm qdevice remove
# Sur le serveur QDevice : systemctl stop corosync-qnetd && apt remove corosync-qnetd
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

### Certificats Custom (ACME/Let's Encrypt)
```bash
pvenode acme account register default mail@example.com
pvenode acme plugin add dns cloudflare --api CF_Token=xxx --data domain=pve.example.com
pvenode acme cert order && pvenode acme cert list
```

---

## Action: corosync

### Description
Configuration avancée de Corosync (timeouts, transport, crypto).

### Fichier Configuration
```bash
# Voir config actuelle
cat /etc/pve/corosync.conf
```

Sections clés : `logging`, `totem` (cluster_name, secauth, ip_version), `nodelist` (ring0_addr par node), `quorum`.

### Ajuster Timeouts (réseau lent)
```bash
# Dans /etc/pve/corosync.conf, section totem :
#   token: 5000          # Default 1000ms
#   consensus: 6000      # Doit être > token
#   join: 60
#   max_messages: 20

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

> Pour les bonnes pratiques HA, règles de quorum, maintenance et troubleshooting avancé : voir [cluster-ha.md](cluster-ha.md)
