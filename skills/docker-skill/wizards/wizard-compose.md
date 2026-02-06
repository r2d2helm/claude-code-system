# Wizard: Docker Compose

Assistant interactif pour creer un fichier `docker-compose.yml`.

## Questions

1. **Nom du projet** : Nom du projet Docker Compose
2. **Services** : Quels services ? (web, api, db, redis, nginx, custom)
3. **Base de donnees** : PostgreSQL, MySQL, MongoDB, Redis, aucune
4. **Reverse proxy** : Nginx, Traefik, aucun
5. **Volumes** : Volumes persistants necessaires ?
6. **Reseau** : Reseau custom ou default ?
7. **Environnement** : Fichier .env ?

## Generation

Genere un `docker-compose.yml` complet avec :
- Services configures avec healthchecks
- Volumes nommes
- Reseau custom
- Variables d'environnement via .env
- Restart policies
- Labels pour reverse proxy

## Template de base

```yaml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "${APP_PORT:-3000}:3000"
    environment:
      - NODE_ENV=production
    volumes:
      - app-data:/app/data
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - app-net

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME:-app}
      POSTGRES_USER: ${DB_USER:-app}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - app-net

volumes:
  app-data:
  db-data:

networks:
  app-net:
    driver: bridge
```
