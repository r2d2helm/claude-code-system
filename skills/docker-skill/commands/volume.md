# Commande: /dk-volume

Gestion des volumes Docker.

## Syntaxe

```
/dk-volume [action] [options]
```

## Actions

```bash
# Lister les volumes
docker volume ls --format "table {{.Name}}\t{{.Driver}}\t{{.Mountpoint}}"

# Creer un volume
docker volume create <name>

# Inspecter
docker volume inspect <name>

# Supprimer
docker volume rm <name>

# Volumes orphelins (non utilises)
docker volume ls -f "dangling=true"

# Nettoyer les orphelins
docker volume prune -f
```

## Exemples

```bash
/dk-volume                # Lister les volumes
/dk-volume create data    # Creer le volume "data"
/dk-volume prune          # Nettoyer orphelins
```
