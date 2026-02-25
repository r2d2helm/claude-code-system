# Commande: /devops-deploy

Deployer un service sur une VM du homelab.

## Syntaxe

```
/devops-deploy [service] [vm] [options]
```

## Deploiement Standard (Docker Compose)

```bash
# 1. Pre-deploy : backup + verification espace
ssh root@{IP} "df -h / && docker compose -f /opt/{service}/docker-compose.yml ps"

# 2. Pull des nouvelles images
ssh root@{IP} "cd /opt/{service} && docker compose pull"

# 3. Deploy (recreate les containers modifies)
ssh root@{IP} "cd /opt/{service} && docker compose up -d --remove-orphans"

# 4. Verification
ssh root@{IP} "cd /opt/{service} && docker compose ps && docker compose logs --tail 20"

# 5. Health check
curl -s http://{IP}:{PORT}/health || curl -s http://{IP}:{PORT}/
```

## Deploiement avec Downtime Zero

```bash
# Pull d'abord (pas d'arret)
ssh root@{IP} "cd /opt/{service} && docker compose pull"

# Recreer un par un
ssh root@{IP} "cd /opt/{service} && docker compose up -d --no-deps --build {container}"
```

## Deploiement Complet (rebuild)

```bash
# Arreter, rebuild, redemarrer
ssh root@{IP} "cd /opt/{service} && docker compose down && docker compose build --no-cache && docker compose up -d"
```

## Par VM

| VM | Services principaux | Chemin |
|----|---------------------|--------|
| 100 | beszel, uptime-kuma, netdata, dozzle, ntfy | /opt/{service}/ |
| 103 | supabase, litellm, langfuse, taskyn, monitoring | /opt/{service}/ |
| 104 | postgres-shared, monitoring | /opt/{service}/ |
| 105 | rag-indexer, taskyn | /opt/{service}/ |

## Post-Deploy Checklist

- [ ] Containers UP (`docker ps`)
- [ ] Logs sans erreur (`docker logs --tail 20`)
- [ ] Endpoint accessible (`curl`)
- [ ] Uptime Kuma vert
- [ ] Notifier via ntfy si critique
