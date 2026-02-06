# Wizard: Création de Cluster Proxmox

## Mode d'emploi
Ce wizard guide la création ou l'extension d'un cluster Proxmox VE 9+. Répondez aux questions pour générer les commandes personnalisées.

---

## Questions Interactives

### 1. Type d'Opération

**Q1.1: Que voulez-vous faire?**

| Option | Action |
|--------|--------|
| A | Créer un nouveau cluster |
| B | Ajouter un node à un cluster existant |
| C | Vérifier l'état du cluster |

```
Choix: ___
```

---

### 2. Configuration du Cluster (si création)

**Q2.1: Nom du cluster?**
```
Nom: _______________ (ex: pve-cluster-01, prod-cluster)
```

**Q2.2: Combien de nodes?**
```
Nodes: _____ (recommandé: 3, 5 ou 7 - nombre impair pour quorum)
```

**Q2.3: IPs des nodes?**
```
Node 1 (premier node): _______________
Node 2: _______________
Node 3: _______________
(ajouter si plus de 3)
```

**Q2.4: Réseau dédié Corosync?**
```
[ ] Oui - Interface dédiée (recommandé pour production)
[ ] Non - Utiliser le réseau principal
```

**Q2.5: Configuration des links Corosync?**
```
Link 0 (principal): _______________ (ex: 10.10.10.0/24)
Link 1 (backup):    _______________ (optionnel, ex: 10.10.20.0/24)
```

---

### 3. Rejoindre un Cluster (si ajout)

**Q3.1: IP du node existant?**
```
IP: _______________ (un node déjà dans le cluster)
```

**Q3.2: Mot de passe root du node existant?**
```
Password: _______________ (sera demandé interactivement)
```

**Q3.3: Fingerprint SSH accepté?**
```
[ ] Vérifier et accepter manuellement
[ ] Accepter automatiquement (--force)
```

---

## Génération de Commandes

### Créer un Nouveau Cluster

```bash
# Sur le PREMIER node uniquement
pvecm create CLUSTER_NAME \
  --link0 LINK0_IP \
  --link1 LINK1_IP

# Vérifier
pvecm status
```

### Ajouter un Node

```bash
# Sur le node À AJOUTER (pas sur le node existant!)
pvecm add EXISTING_NODE_IP \
  --link0 LINK0_IP \
  --link1 LINK1_IP

# Vérifier depuis n'importe quel node
pvecm status
pvecm nodes
```

### Vérifier l'État

```bash
# État global
pvecm status

# Liste des nodes
pvecm nodes

# Votes et quorum
pvecm expected

# État Corosync
systemctl status corosync
corosync-quorumtool -s
```

---

## Configurations Prêtes

### Cluster 3 Nodes Production

```bash
# Node 1 (créer le cluster)
pvecm create prod-cluster --link0 10.10.10.1 --link1 10.10.20.1

# Node 2 (rejoindre)
pvecm add 10.10.10.1 --link0 10.10.10.2 --link1 10.10.20.2

# Node 3 (rejoindre)
pvecm add 10.10.10.1 --link0 10.10.10.3 --link1 10.10.20.3
```

---

## Best Practices 2026

| Règle | Raison |
|-------|--------|
| Nombre impair de nodes | Quorum majoritaire sans tie-breaking |
| Réseau Corosync dédié | Évite les interférences avec le trafic VM |
| 2 links Corosync | Redondance réseau pour la communication cluster |
| Même version Proxmox | Compatibilité garantie entre nodes |
| DNS ou /etc/hosts | Résolution de noms fiable entre nodes |
| NTP synchronisé | Horloge cohérente pour le cluster |

---

## Commande Associée

Voir `/px-cluster` pour les opérations cluster.
