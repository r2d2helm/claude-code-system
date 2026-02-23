# Commande: /lx-docker

Gestion des conteneurs Docker sur serveur Linux.

## Syntaxe

```
/lx-docker [action] [options]
```

## Actions

### Conteneurs

```bash
# Lister les conteneurs en cours
docker ps

# Lister tous les conteneurs (inclus arretes)
docker ps -a

# Demarrer / arreter / redemarrer
docker start mon-conteneur
docker stop mon-conteneur
docker restart mon-conteneur

# Logs d'un conteneur
docker logs -f --tail 100 mon-conteneur

# Executer une commande dans un conteneur
docker exec -it mon-conteneur bash

# Inspecter un conteneur
docker inspect mon-conteneur

# Supprimer un conteneur arrete
docker rm mon-conteneur

# Forcer la suppression
docker rm -f mon-conteneur
```

### Images

```bash
# Lister les images locales
docker images

# Telecharger une image
docker pull nginx:latest

# Construire une image depuis Dockerfile
docker build -t mon-app:latest .

# Supprimer une image
docker rmi nginx:latest

# Supprimer les images inutilisees
docker image prune -a
```

### Docker Compose

```bash
# Demarrer les services
docker compose up -d

# Arreter les services
docker compose down

# Voir les logs
docker compose logs -f

# Reconstruire et demarrer
docker compose up -d --build

# Etat des services
docker compose ps

# Executer commande dans un service
docker compose exec web bash
```

### Reseau et volumes

```bash
# Lister les reseaux
docker network ls

# Creer un reseau
docker network create mon-reseau

# Lister les volumes
docker volume ls

# Inspecter un volume
docker volume inspect mon-volume

# Nettoyage complet (volumes orphelins, images, cache)
docker system prune -a --volumes
```

### Monitoring

```bash
# Utilisation ressources en temps reel
docker stats

# Espace disque utilise par Docker
docker system df

# Verifier l'etat du daemon
systemctl status docker
```

## Options

| Option | Description |
|--------|-------------|
| `ps` | Lister les conteneurs |
| `logs` | Voir les logs |
| `compose` | Gestion Docker Compose |
| `prune` | Nettoyage espace disque |
| `stats` | Monitoring ressources |

## Exemples

```bash
/lx-docker ps                    # Lister conteneurs
/lx-docker logs mon-app          # Logs d'un conteneur
/lx-docker compose up            # Demarrer services compose
/lx-docker prune                 # Nettoyage complet
```

## Voir Aussi

- `/lx-services` - Gestion du service Docker
- `/lx-firewall` - Ouvrir les ports pour les conteneurs
- `/lx-disk` - Verifier l'espace disque
