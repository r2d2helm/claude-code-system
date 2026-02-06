# Commande: /dk-stats

Statistiques d'utilisation des ressources Docker.

## Syntaxe

```
/dk-stats [container] [options]
```

## Actions

```bash
# Stats de tous les containers
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"

# Stats en temps reel
docker stats

# Stats d'un container specifique
docker stats <container> --no-stream

# Espace disque global
docker system df -v

# Info systeme Docker
docker info
```

## Options

| Option | Description |
|--------|-------------|
| `--no-stream` | Snapshot unique (pas de refresh) |
| `--format` | Format de sortie custom |
| `--all` | Inclure containers arretes |

## Exemples

```bash
/dk-stats                  # Snapshot de tous les containers
/dk-stats myapp            # Stats de myapp
/dk-stats --disk           # Utilisation disque
```
