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

```bash
/dk-compose up            # Demarrer le projet
/dk-compose down          # Arreter tout
/dk-compose logs api      # Logs du service api
/dk-compose -f prod.yml up  # Fichier compose custom
```
