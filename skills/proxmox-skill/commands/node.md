# /pve-node - Gestion des Nodes Proxmox

## Description
Administration des nodes individuels du cluster Proxmox VE.
Configuration systeme, mises a jour, services et maintenance.

## Syntaxe
```
/pve-node <action> [node-name] [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `list` | `/pve-node list` | Lister les nodes |
| `info` | `/pve-node info [node]` | Informations detaillees |
| `update` | `/pve-node update [node]` | Mises a jour systeme |
| `services` | `/pve-node services [node]` | Etat des services PVE |
| `config` | `/pve-node config [node]` | Configuration node |
| `task` | `/pve-node task [node]` | Taches recentes |
| `maintenance` | `/pve-node maintenance [node]` | Mode maintenance |

## Exemples

### Informations node

```bash
# Lister les nodes du cluster
pvesh get /nodes --output-format=json-pretty

# Informations detaillees d'un node
pvesh get /nodes/pve01/status --output-format=json-pretty

# Version Proxmox
pveversion -v

# Informations systeme
pvesh get /nodes/pve01/status --output-format=json | \
  jq '{cpu: .cpu, memory: .memory, uptime: .uptime, pveversion: .pveversion}'

# Abonnement
pvesubscription get

# DNS et reseau
pvesh get /nodes/pve01/dns --output-format=json-pretty
pvesh get /nodes/pve01/network --output-format=json-pretty
```

### Mises a jour

```bash
# Rafraichir les depots
apt update

# Lister les mises a jour disponibles
apt list --upgradable

# Mise a jour Proxmox (avec precaution)
apt dist-upgrade -s  # Simulation d'abord
apt dist-upgrade     # Appliquer

# Mise a jour via API
pvesh create /nodes/pve01/apt/update

# Lister les mises a jour via API
pvesh get /nodes/pve01/apt/update --output-format=json-pretty

# Changelog d'un paquet
pvesh get /nodes/pve01/apt/changelog --name proxmox-ve
```

### Services Proxmox

```bash
# Etat de tous les services PVE
pvesh get /nodes/pve01/services --output-format=json-pretty

# Etat d'un service specifique
pvesh get /nodes/pve01/services/pveproxy/state

# Redemarrer un service
pvesh create /nodes/pve01/services/pveproxy/restart

# Services critiques a verifier
systemctl status pvedaemon pveproxy pvestatd corosync pve-cluster
```

### Configuration node

```bash
# Voir la configuration
pvenode config get

# Configurer le domaine ACME
pvenode config set --acme domains=pve01.example.com

# Configurer le wakeonlan
pvenode config set --wakeonlan BC:24:11:AA:BB:CC

# Configurer description
pvenode config set --description "Node principal - Dell R750"

# Voir les taches recentes
pvesh get /nodes/pve01/tasks --limit 20 --output-format=json-pretty

# Details d'une tache
pvesh get /nodes/pve01/tasks/<UPID>/status
pvesh get /nodes/pve01/tasks/<UPID>/log
```

### Mode maintenance

```bash
# Migrer toutes les VMs avant maintenance
for vmid in $(qm list | awk '/running/ {print $1}'); do
  qm migrate "$vmid" pve02 --online
done

# Verifier qu'aucune VM ne tourne
qm list
pct list

# Desactiver le demarrage auto
# (pour eviter que les VMs redemarrent sur ce node apres reboot)

# Redemarrer le node
pvesh create /nodes/pve01/status --command reboot

# Arreter le node
pvesh create /nodes/pve01/status --command shutdown

# Verifier syslog
journalctl -u pvedaemon -n 50
journalctl -u corosync -n 50
```

### Syslog et diagnostic

```bash
# Voir le syslog via API
pvesh get /nodes/pve01/syslog --limit 50 --output-format=json-pretty

# Rapport systeme complet (pour support)
pvereport > /tmp/pvereport-$(hostname)-$(date +%Y%m%d).txt
```

## Notes

- Toujours migrer les VMs/CTs avant une maintenance node
- Verifier la version Proxmox sur tous les nodes avant une mise a jour cluster
- Les mises a jour majeures (ex: PVE 8 vers 9) necessitent une procedure specifique
- Le mode maintenance HA suspend les basculements automatiques
- Redemarrer les services PVE peut interrompre brievement l'acces Web UI

## Voir Aussi
- `/pve-cluster` - Gestion cluster
- `/pve-status` - Vue d'ensemble cluster
- `/pve-acme` - Certificats SSL
- `/pve-diag` - Diagnostic avance
