# Exemples de Routing

> Extrait du meta-router SKILL.md — scénarios de routing détaillés

## Exemple 1: Détection Simple
```
User: "Comment voir l'état de mon cluster Proxmox?"
Router: Keywords [cluster, proxmox] → 🟠 proxmox-skill
Action: Charger /pve-cluster, répondre avec status cluster
```

## Exemple 2: Détection Windows
```
User: "Configure le firewall pour autoriser RDP"
Router: Keywords [firewall, rdp] → 🔵 windows-skill
Action: Charger /win-firewall, /win-rdp
```

## Exemple 3: Multi-Contexte
```
User: "Déploie un conteneur LXC Ubuntu puis configure SSH"
Router:
  - Phase 1: [conteneur, lxc] → 🟠 proxmox-skill (/pve-ct)
  - Phase 2: [ubuntu, ssh] → 🐧 linux-skill (/lx-ssh)
Action: Réponse séquentielle avec les deux contextes
```

## Exemple 4: Ambiguïté
```
User: "Fais un backup"
Router: Ambigu - backup existe dans plusieurs contextes
Action: Demander clarification (Proxmox? Windows? Docker?)
```

## Exemple 5: Commande Explicite
```
User: "/pve-status"
Router: Commande explicite → 🟠 proxmox-skill direct
Action: Exécuter sans analyse
```
