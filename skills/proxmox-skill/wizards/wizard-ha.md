# Wizard: Configuration Haute Disponibilité

## Mode d'emploi
Ce wizard configure la Haute Disponibilité (HA) sur un cluster Proxmox VE 9+ pour protéger les VMs/CTs contre les pannes de nodes. Nécessite un cluster de minimum 3 nodes.

---

## Questions Interactives

### 1. Prérequis

**Q1.1: Le cluster a-t-il au moins 3 nodes?**
```
[ ] Oui (obligatoire pour HA)
[ ] Non → Créer un cluster d'abord (voir wizard-cluster)
```

**Q1.2: Le fencing est-il configuré?**
```
[ ] Oui - IPMI/iLO/iDRAC/watchdog configuré
[ ] Non → Configurer le watchdog logiciel
```

---

### 2. Groupe HA

**Q2.1: Nom du groupe HA?**
```
Nom: _______________ (ex: ha-group-prod, ha-web-servers)
```

**Q2.2: Quels nodes dans ce groupe?**
```
[ ] Node 1: _______________
[ ] Node 2: _______________
[ ] Node 3: _______________
```

**Q2.3: Politique de restriction?**

| Option | Politique | Effet |
|--------|-----------|-------|
| A | Non restreint (défaut) | VMs peuvent tourner sur tous les nodes |
| B | Restreint | VMs uniquement sur les nodes du groupe |

```
Choix: ___
```

**Q2.4: Nodes sans failover (nofailback)?**
```
[ ] Oui - Pas de retour automatique au node d'origine après recovery
[ ] Non - Retour automatique (défaut)
```

---

### 3. Ressources HA

**Q3.1: Quelles VMs/CTs protéger?**
```
VM/CT 1: _____ (VMID, ex: 100)
VM/CT 2: _____ (VMID)
VM/CT 3: _____ (VMID)
```

**Q3.2: État souhaité pour chaque ressource?**

| Option | État | Comportement |
|--------|------|-------------|
| A | started | Toujours démarrée (défaut) |
| B | stopped | Toujours arrêtée (protection migration) |
| C | ignored | Pas de gestion HA |

```
Choix par VM: ___
```

**Q3.3: Max restart (tentatives avant failover)?**
```
Max restart: _____ (défaut: 1, recommandé: 2-3)
```

**Q3.4: Max relocate (failovers max)?**
```
Max relocate: _____ (défaut: 1, recommandé: 2)
```

---

## Génération de Commandes

### Configurer le Watchdog (si pas de fencing hardware)

```bash
# Activer le watchdog logiciel
apt install watchdog
systemctl enable --now watchdog

# Vérifier
ha-manager status
```

### Créer un Groupe HA

```bash
ha-manager groupadd GROUP_NAME \
  --nodes "node1,node2,node3" \
  --restricted 0 \
  --nofailback 0
```

### Ajouter des Ressources HA

```bash
# Ajouter une VM/CT au HA
ha-manager add vm:VMID \
  --group GROUP_NAME \
  --state started \
  --max_restart 2 \
  --max_relocate 2

# Répéter pour chaque VM/CT
```

### Vérifier l'État HA

```bash
ha-manager status
ha-manager config
pvesh get /cluster/ha/resources
pvesh get /cluster/ha/groups
```

---

## Configuration Production

```bash
# Groupe HA production
ha-manager groupadd ha-prod --nodes "pve1,pve2,pve3" --restricted 1 --nofailback 0

# Protéger les VMs critiques
ha-manager add vm:100 --group ha-prod --state started --max_restart 2 --max_relocate 2
ha-manager add vm:101 --group ha-prod --state started --max_restart 2 --max_relocate 2
ha-manager add ct:200 --group ha-prod --state started --max_restart 3 --max_relocate 2

# Vérifier
ha-manager status
```

---

## Best Practices 2026

| Règle | Raison |
|-------|--------|
| Minimum 3 nodes | Quorum HA nécessite majorité |
| Fencing obligatoire | Éviter split-brain (STONITH) |
| Stockage partagé | VMs doivent être accessibles depuis tous les nodes (Ceph, NFS, iSCSI) |
| Tester le failover | Simuler une panne avant production |
| max_restart 2-3 | Tentatives locales avant migration |
| Pas de HA sur stockage local | Migration impossible sans stockage partagé |

---

## Commande Associée

Voir `/px-ha` pour les opérations HA.
