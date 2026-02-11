# Commande: /dk-swarm

Gestion du mode Docker Swarm (init, services, nodes, stack).

## Syntaxe

```
/dk-swarm [action] [options]
```

## Actions

### Initialisation et Nodes

```bash
# Initialiser le Swarm (manager)
docker swarm init --advertise-addr <IP>

# Obtenir le token worker
docker swarm join-token worker

# Obtenir le token manager
docker swarm join-token manager

# Rejoindre un Swarm (depuis un node)
docker swarm join --token <TOKEN> <MANAGER-IP>:2377

# Lister les nodes
docker node ls

# Inspecter un node
docker node inspect <node-id> --pretty

# Promouvoir un worker en manager
docker node promote <node-id>

# Retirer un node
docker node rm <node-id>
```

### Services

```bash
# Creer un service
docker service create --name web --replicas 3 -p 80:80 nginx:latest

# Lister les services
docker service ls

# Details d'un service
docker service ps web

# Logs d'un service
docker service logs web --follow

# Scaler un service
docker service scale web=5

# Mettre a jour l'image
docker service update --image nginx:1.27 web

# Rolling update avec options
docker service update --image nginx:1.27 \
  --update-parallelism 2 \
  --update-delay 10s \
  --rollback-parallelism 1 web

# Rollback
docker service rollback web

# Supprimer un service
docker service rm web
```

### Stacks (Compose en Swarm)

```bash
# Deployer une stack depuis compose
docker stack deploy -c docker-compose.yml mystack

# Lister les stacks
docker stack ls

# Services d'une stack
docker stack services mystack

# Supprimer une stack
docker stack rm mystack
```

## Options

| Option | Description |
|--------|-------------|
| `init` | Initialiser le Swarm |
| `join` | Rejoindre un Swarm |
| `services` | Lister les services |
| `scale` | Modifier le nombre de replicas |
| `deploy` | Deployer une stack |

## Exemples

```bash
/dk-swarm init                   # Initialiser le Swarm
/dk-swarm services               # Lister tous les services
/dk-swarm scale web=5            # Scaler a 5 replicas
/dk-swarm deploy mystack         # Deployer une stack
```

## Voir Aussi

- `/dk-compose` - Docker Compose (mode standalone)
- `/dk-network` - Gestion des reseaux overlay
