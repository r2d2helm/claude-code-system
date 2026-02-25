# Commande: /devops-rollback

Rollback vers la version precedente d'un service.

## Syntaxe

```
/devops-rollback [service] [vm]
```

## Rollback Docker Compose

```bash
# 1. Identifier la version precedente
ssh root@{IP} "docker images --format '{{.Repository}}:{{.Tag}} {{.CreatedAt}}' | grep {service} | head -5"

# 2. Arreter le service actuel
ssh root@{IP} "cd /opt/{service} && docker compose down"

# 3. Restaurer le docker-compose.yml precedent (si backup)
ssh root@{IP} "cp /opt/{service}/docker-compose.yml.bak /opt/{service}/docker-compose.yml"

# 4. Redemarrer avec l'ancienne version
ssh root@{IP} "cd /opt/{service} && docker compose up -d"

# 5. Verifier
ssh root@{IP} "cd /opt/{service} && docker compose ps && docker compose logs --tail 10"
```

## Rollback avec Tag Specifique

```bash
# Modifier le tag dans docker-compose.yml
ssh root@{IP} "sed -i 's/image: {image}:latest/image: {image}:{old_tag}/' /opt/{service}/docker-compose.yml"

# Redemarrer
ssh root@{IP} "cd /opt/{service} && docker compose up -d"
```

## Rollback PostgreSQL

```bash
# Restaurer depuis le dernier dump
ssh r2d2helm@192.168.1.164 "pg_restore -U postgres -h localhost -d {dbname} --clean --if-exists /mnt/nfs/backups/postgresql/pg-{dbname}-{date}.dump"
```

## Precautions

- **Toujours sauvegarder** la config actuelle avant rollback
- **Verifier les migrations** : un rollback DB peut necessiter un rollback de schema
- **Tester** que le service fonctionne apres rollback
- **Documenter** la raison du rollback
