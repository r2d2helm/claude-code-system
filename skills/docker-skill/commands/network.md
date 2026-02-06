# Commande: /dk-network

Gestion des reseaux Docker.

## Syntaxe

```
/dk-network [action] [options]
```

## Actions

```bash
# Lister les reseaux
docker network ls --format "table {{.ID}}\t{{.Name}}\t{{.Driver}}\t{{.Scope}}"

# Creer un reseau
docker network create <name>
docker network create --driver bridge --subnet 172.20.0.0/16 <name>

# Inspecter
docker network inspect <name>

# Connecter un container
docker network connect <network> <container>

# Deconnecter
docker network disconnect <network> <container>

# Supprimer
docker network rm <name>

# Nettoyer les reseaux inutilises
docker network prune -f
```

## Exemples

```bash
/dk-network                          # Lister
/dk-network create app-net           # Creer reseau
/dk-network connect app-net myapp    # Connecter container
```
