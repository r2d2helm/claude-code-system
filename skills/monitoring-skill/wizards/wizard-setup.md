---
name: mon-wizard setup
description: Deploiement guide de la stack monitoring
---

# Wizard : Setup Stack Monitoring

## Etapes

### 1. Prerequis
- [ ] VM 100 accessible (SSH root@192.168.1.162)
- [ ] Docker installe et fonctionnel
- [ ] Ports disponibles : 8091, 19999, 3003, 8082, 8084, 45876

### 2. Deployer les containers
```bash
ssh root@192.168.1.162 "cd /opt/monitoring && docker compose up -d"
```

### 3. Creer le superuser Beszel
```bash
ssh root@192.168.1.162 "docker exec beszel-hub /beszel superuser create <email> <password>"
```

### 4. Configurer l'agent
1. Recuperer la cle du hub : `GET /api/beszel/getkey`
2. Mettre la cle dans .env : `BESZEL_AGENT_KEY=<key>`
3. Ajouter le systeme dans le hub via API
4. Redemarrer l'agent

### 5. Configurer ntfy
1. Creer un utilisateur admin
2. Creer les topics : monitoring-critical, monitoring-warning, monitoring-info

### 6. Configurer Uptime Kuma
1. Acceder a http://192.168.1.162:3003
2. Creer un compte admin
3. Ajouter les monitors (voir /mon-uptime)

### 7. Installer agents distants
- Proxmox : Beszel agent natif + Netdata kickstart
- Windows : Beszel agent binaire

### 8. Configurer MCP
1. Ajouter beszel-assistant dans .claude.json
2. Ajouter netdata MCP dans .claude.json
3. Redemarrer Claude Code

### 9. Valider
Executer `/mon-health` pour verifier que tout fonctionne.
