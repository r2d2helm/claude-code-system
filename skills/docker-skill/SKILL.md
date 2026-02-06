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
| `/dk-registry` | Operations registry [PREVU] |
| `/dk-swarm` | Gestion Swarm [PREVU] |
| `/dk-security` | Scan de securite [PREVU] |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/dk-wizard compose` | Creer un docker-compose.yml |
| `/dk-wizard dockerfile` | Creer un Dockerfile |
| `/dk-wizard setup` | Installer Docker |
