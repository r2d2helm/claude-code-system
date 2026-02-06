# Commande: /dk-images

Gerer les images Docker.

## Syntaxe

```
/dk-images [action] [options]
```

## Actions

```bash
# Lister les images
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}"

# Pull une image
docker pull <image>:<tag>

# Supprimer une image
docker rmi <image>

# Tagger une image
docker tag <source> <target>:<tag>

# Images dangling (sans tag)
docker images -f "dangling=true"

# Nettoyer les dangling
docker image prune -f

# Historique d'une image
docker history <image>
```

## Options

| Option | Description |
|--------|-------------|
| `--all` | Inclure images intermediaires |
| `--filter dangling=true` | Images sans tag |
| `--format` | Format de sortie |

## Exemples

```bash
/dk-images                    # Lister toutes les images
/dk-images pull nginx:latest  # Pull nginx
/dk-images prune              # Nettoyer dangling
```
