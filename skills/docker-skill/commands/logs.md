# Commande: /dk-logs

Logs des containers Docker.

## Syntaxe

```
/dk-logs [container] [options]
```

## Actions

```bash
# Logs d'un container
docker logs <container>

# Suivre en temps reel
docker logs -f <container>

# Dernières N lignes
docker logs --tail 100 <container>

# Avec timestamps
docker logs -t <container>

# Depuis une date
docker logs --since "2026-02-06T10:00:00" <container>

# Compose: logs de tous les services
docker compose logs -f
docker compose logs -f <service>
```

## Options

| Option | Description |
|--------|-------------|
| `-f` | Suivre en temps reel |
| `--tail N` | Dernières N lignes |
| `-t` | Ajouter timestamps |
| `--since` | Depuis une date/duree |
| `--until` | Jusqu'a une date/duree |

## Exemples

```bash
/dk-logs myapp              # Tous les logs
/dk-logs myapp --tail 50    # 50 dernieres lignes
/dk-logs myapp -f           # Suivre en direct
```
