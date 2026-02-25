# Commande: /supa-config

Configuration des services Supabase.

## Syntaxe

```
/supa-config [action]
```

## Voir la Configuration

```bash
# docker-compose.yml
ssh root@192.168.1.163 "cat /opt/supabase/docker-compose.yml"

# Variables d'environnement (masquer les secrets)
ssh root@192.168.1.163 "cat /opt/supabase/.env | sed 's/=.*/=***/' "

# Config Kong (API Gateway)
ssh root@192.168.1.163 "cat /opt/supabase/volumes/api/kong.yml 2>/dev/null"
```

## Modifier

```bash
# Editer le .env
ssh root@192.168.1.163 "nano /opt/supabase/.env"

# Appliquer les changements
ssh root@192.168.1.163 "cd /opt/supabase && docker compose down && docker compose up -d"
```

## Variables Critiques

| Variable | Description | Ou |
|----------|-------------|----|
| `POSTGRES_PASSWORD` | Mot de passe DB | .env |
| `JWT_SECRET` | Secret pour signer les JWT (min 32 chars) | .env |
| `ANON_KEY` | Cle publique frontend | .env |
| `SERVICE_ROLE_KEY` | Cle admin backend | .env |
| `SITE_URL` | URL du frontend | .env |
| `DASHBOARD_USERNAME` | Login Studio | .env |
| `DASHBOARD_PASSWORD` | Password Studio | .env |

## Regenerer les Cles JWT

```bash
# Les cles ANON et SERVICE_ROLE sont des JWT signes avec JWT_SECRET
# Pour regenerer : changer JWT_SECRET puis regenerer les cles
# Outil : https://supabase.com/docs/guides/self-hosting#api-keys

# ATTENTION : changer les cles casse toutes les connexions existantes
```
