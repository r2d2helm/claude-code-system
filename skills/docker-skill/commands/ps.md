# Commande: /dk-ps

Lister et gerer les containers Docker.

## Syntaxe

```
/dk-ps [action] [options]
```

## Actions

### Lister les containers

```bash
# Tous les containers (y compris arretes)
docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

# Containers actifs seulement
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

# Filtrer par nom
docker ps -a --filter "name=myapp"

# Filtrer par status
docker ps -a --filter "status=exited"
```

### Actions sur un container

```bash
# Demarrer
docker start <name|id>

# Arreter (graceful)
docker stop <name|id>

# Redemarrer
docker restart <name|id>

# Supprimer
docker rm <name|id>

# Forcer l'arret + supprimer
docker rm -f <name|id>
```

### Inspecter

```bash
docker inspect <name|id> --format '{{json .State}}'
docker inspect <name|id> --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## Options

| Option | Description |
|--------|-------------|
| `--filter` | Filtrer par name, status, image |
| `--all` | Inclure les containers arretes |
| `--quiet` | Afficher seulement les IDs |

## Exemples

Lister les containers actifs avec ports et status :
```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
```

Filtrer les containers par nom :
```bash
docker ps -a --filter "name=myapp"
```

Afficher uniquement les IDs des containers arretes :
```bash
docker ps -a --filter "status=exited" -q
```

Lister tous les containers avec leur taille disque :
```bash
docker ps -a --size --format "table {{.Names}}\t{{.Image}}\t{{.Size}}"
```
