---
name: docker-skill
description: "Administration Docker et conteneurs : images, containers, compose, volumes, networks, registries, securite."
---

# Super Agent Docker Administration

Agent intelligent pour administrer Docker : containers, images, compose, volumes, reseaux.

## Philosophie

> "Un container bien orchestre est une application indestructible."

## Compatibilite

| Composant | Support |
|-----------|---------|
| Docker Engine | 24+ |
| Docker Desktop | 4.x+ (Windows/Mac) |
| Docker Compose | v2+ |
| Platforms | Windows, Linux, macOS |

## Commandes Slash

### Containers

| Commande | Description |
|----------|-------------|
| `/dk-ps` | Lister et gerer les containers |
| `/dk-logs` | Logs des containers |
| `/dk-exec` | Executer dans un container |
| `/dk-stats` | Stats CPU/memoire/reseau |

### Images

| Commande | Description |
|----------|-------------|
| `/dk-images` | Gerer les images |
| `/dk-build` | Build d'images |

### Infrastructure

| Commande | Description |
|----------|-------------|
| `/dk-compose` | Operations Docker Compose |
| `/dk-volume` | Gestion des volumes |
| `/dk-network` | Gestion des reseaux |
| `/dk-prune` | Nettoyage ressources inutilisees |

### Avance

| Commande | Description |
|----------|-------------|
| `/dk-registry` | Operations registry (login, push, pull, tag) |
| `/dk-swarm` | Gestion Swarm (init, services, stacks, nodes) |
| `/dk-security` | Scan de securite (CVE, audit, Dockerfile) |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/dk-wizard compose` | Creer un docker-compose.yml |
| `/dk-wizard dockerfile` | Creer un Dockerfile |
| `/dk-wizard setup` | Installer Docker |

## Best Practices

- **1 process par container** : eviter les multi-services dans un container
- **Images minimales** : utiliser `alpine` ou `distroless` quand possible
- **Tags explicites** : jamais `:latest` en production, toujours versionner
- **Multi-stage builds** : separer build et runtime pour reduire la taille
- **Non-root** : utiliser `USER` dans le Dockerfile, eviter `--privileged`
- **Healthchecks** : toujours definir un `HEALTHCHECK` dans le Dockerfile
- **Secrets** : jamais de secrets dans les images, utiliser Docker Secrets ou env vars
- **.dockerignore** : exclure `node_modules`, `.git`, `*.log` du build context

## References

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/build/building/best-practices/)
- [Docker Compose Specification](https://docs.docker.com/compose/compose-file/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Docker Hub](https://hub.docker.com/)
