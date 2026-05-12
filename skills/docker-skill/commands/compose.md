# Commande: /dk-compose

Operations Docker Compose.

## Syntaxe

```
/dk-compose [action] [options]
```

## Actions

```bash
# Demarrer les services
docker compose up -d

# Arreter les services
docker compose down

# Voir les logs
docker compose logs -f [service]

# Status des services
docker compose ps

# Redemarrer un service
docker compose restart [service]

# Rebuild et redemarrer
docker compose up -d --build

# Pull les dernieres images
docker compose pull

# Executer dans un service
docker compose exec [service] [command]
```

## Options

| Option | Description |
|--------|-------------|
| `-f file` | Fichier compose specifique |
| `--profile` | Activer un profil |
| `--env-file` | Fichier d'environnement |
| `-d` | Mode detache |
| `--build` | Rebuild avant up |
| `--force-recreate` | Recreer les containers |

## Exemples

Demarrer tous les services en arriere-plan :
```bash
docker compose up -d
```

Arreter et supprimer les containers, reseaux et volumes orphelins :
```bash
docker compose down --remove-orphans
```

Suivre les logs d'un service en temps reel :
```bash
docker compose logs -f api
```

Rebuild et redemarrer un service apres modification du Dockerfile :
```bash
docker compose up -d --build api
```

Scaler un service a 3 instances :
```bash
docker compose up -d --scale worker=3
```
