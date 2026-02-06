# Commande: /dk-prune

Nettoyage des ressources Docker inutilisees.

## Syntaxe

```
/dk-prune [target] [options]
```

## Actions

```bash
# Nettoyage complet (containers, images, reseaux, cache)
docker system prune -af --volumes

# Containers arretes
docker container prune -f

# Images dangling
docker image prune -f

# Toutes les images non utilisees
docker image prune -af

# Volumes orphelins
docker volume prune -f

# Reseaux inutilises
docker network prune -f

# Build cache
docker builder prune -af

# Espace disque utilise
docker system df
```

## Options

| Option | Description |
|--------|-------------|
| `-f` | Forcer sans confirmation |
| `-a` | Inclure toutes les ressources |
| `--volumes` | Inclure les volumes (system prune) |
| `--filter` | Filtrer par label ou date |

## Exemples

```bash
/dk-prune                  # Voir l'espace utilise
/dk-prune all              # Tout nettoyer
/dk-prune images           # Nettoyer images seulement
/dk-prune --dry-run        # Simuler le nettoyage
```
