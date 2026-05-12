---
name: monitoring-skill
description: "Monitoring temps reel homelab : Beszel, Netdata, Uptime Kuma, Dozzle, ntfy. Metriques, alertes, containers, logs."
prefix: /mon-*
---

# Super Agent Monitoring Homelab

Agent intelligent pour le monitoring temps reel du homelab : metriques systeme, containers Docker, disponibilite services, logs, alertes.

## Philosophie

> "Un homelab non surveille est un homelab en sursis."

## Stack Monitoring

| Outil | Role | Port | URL |
|-------|------|------|-----|
| **Beszel Hub** | Metriques systeme + Docker stats | 8091 | http://192.168.1.162:8091 |
| **Beszel Agent** | Agent local (host network) | 45876 | - |
| **Netdata** | Metriques detaillees + ML anomalies | 19999 | http://192.168.1.162:19999 |
| **Uptime Kuma** | Disponibilite services | 3003 | http://192.168.1.162:3003 |
| **Dozzle** | Logs Docker temps reel | 8082 | http://192.168.1.162:8082 |
| **ntfy** | Notifications push | 8084 | http://192.168.1.162:8084 |

## MCP Servers

| Serveur | Type | Outils |
|---------|------|--------|
| **beszel-assistant** | stdio (Python) | beszel_systems, beszel_system_detail, beszel_containers, beszel_alerts, beszel_overview |
| **netdata-vm100** | http | Outils Netdata MCP natifs (metriques, charts, alarms) |
| **netdata-proxmox** | http | Outils Netdata MCP natifs (si deploye) |

## Machines Surveillees

| Machine | IP | OS | Agent |
|---------|----|----|-------|
| VM 100 | 192.168.1.162 | Ubuntu 24.04 | Beszel + Netdata |
| Proxmox Host | 192.168.1.215 | Proxmox VE | Beszel + Netdata (natif) |
| Windows 11 | locale | Windows 11 | Beszel (optionnel) |

## Commandes Slash

### Dashboard

| Commande | Description |
|----------|-------------|
| `/mon-status` | Dashboard complet : systemes, top containers, alertes |
| `/mon-health` | Sante de la stack monitoring elle-meme |

### Systemes

| Commande | Description |
|----------|-------------|
| `/mon-systems` | Liste tous les hotes avec CPU/RAM/Disk |
| `/mon-metrics` | Metriques detaillees Netdata (CPU, RAM, IO, network) |

### Containers

| Commande | Description |
|----------|-------------|
| `/mon-containers` | Stats Docker par conteneur (CPU, RAM, network) |
| `/mon-logs` | Logs Docker temps reel via Dozzle |

### Alertes & Notifications

| Commande | Description |
|----------|-------------|
| `/mon-alerts` | Alertes Beszel actives et historique |
| `/mon-uptime` | Disponibilite services (Uptime Kuma) |
| `/mon-notify` | Tester une notification ntfy |

### Configuration

| Commande | Description |
|----------|-------------|
| `/mon-config` | Configuration de la stack monitoring |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/mon-wizard setup` | Deploiement guide de la stack |
| `/mon-wizard alert-rule` | Creer une regle d'alerte |

## Credentials

| Service | Email | Password |
|---------|-------|----------|
| Beszel Hub | r2d2helm@gmail.com | Jarvis2025 |
| Uptime Kuma | (setup via UI) | - |
| ntfy | (admin a creer) | - |

## Integration avec les autres skills

- **docker-skill** : `/dk-*` pour les operations Docker, `/mon-containers` pour le monitoring
- **linux-skill** : `/lx-*` pour l'admin systeme, `/mon-metrics` pour les metriques
- **proxmox-skill** : `/pve-*` pour la gestion VMs, `/mon-systems` pour l'etat des hotes

## Troubleshooting

### Agent Beszel "down"
1. Verifier que l'agent tourne : `docker ps | grep beszel-agent`
2. Verifier les logs : `docker logs beszel-agent`
3. Verifier la cle : variable KEY dans .env doit correspondre a la cle du hub
4. Verifier la connectivite : le hub doit pouvoir joindre l'IP:45876 de l'agent

### Netdata pas de donnees
1. Verifier le container : `docker ps | grep netdata`
2. Dashboard accessible : http://192.168.1.162:19999
3. Verifier les logs : `docker logs netdata`

### ntfy notifications non recues
1. Tester manuellement : `curl -d "test" http://192.168.1.162:8084/monitoring-info`
2. Verifier l'auth : auth-default-access dans server.yml
