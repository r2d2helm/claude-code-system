---
name: supabase-skill
description: "Administration Supabase : auth, database PostgreSQL, storage, edge functions, realtime, RLS, migrations."
prefix: /supa-*
---

# Super Agent Supabase Administration

Agent intelligent pour administrer la stack Supabase self-hosted sur VM 103 : authentification, base de donnees, storage, edge functions, migrations.

## Philosophie

> "Supabase est un Firebase open-source. Self-hosted, on controle tout."

## Stack Supabase (VM 103 - 192.168.1.163)

| Service | Container | Port | Role |
|---------|-----------|------|------|
| Kong | supabase-kong | :8000 | API Gateway |
| Auth (GoTrue) | supabase-auth | :9999 | Authentification |
| REST (PostgREST) | supabase-rest | :3000 | API REST auto-generee |
| Realtime | supabase-realtime | :4000 | Websockets temps reel |
| Storage | supabase-storage | :5000 | Stockage fichiers (S3-compatible) |
| Studio | supabase-studio | :3000 | Dashboard web |
| PostgreSQL | supabase-db | :5432 | Base de donnees principale |
| Meta | supabase-meta | :8080 | Metadata API |

## Commandes Slash

### Base de Donnees

| Commande | Description |
|----------|-------------|
| `/supa-db` | Operations base de donnees (tables, schemas, requetes) |
| `/supa-migration` | Gerer les migrations (create, apply, rollback, status) |
| `/supa-rls` | Gerer les Row Level Security policies |

### Authentification

| Commande | Description |
|----------|-------------|
| `/supa-auth` | Gerer l'authentification (users, providers, tokens) |

### Storage & Services

| Commande | Description |
|----------|-------------|
| `/supa-storage` | Gerer le stockage (buckets, fichiers, policies) |
| `/supa-edge` | Edge functions (deploy, logs, test) |
| `/supa-status` | Status complet de la stack Supabase |

### Administration

| Commande | Description |
|----------|-------------|
| `/supa-logs` | Logs de tous les services Supabase |
| `/supa-config` | Configuration des services (.env, kong, auth) |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/supa-wizard setup` | Installation et configuration initiale Supabase |
| `/supa-wizard migration` | Creation guidee d'une migration |

## Operations Courantes

### Status de la Stack

```bash
# Tous les containers Supabase
ssh root@192.168.1.163 "docker ps --filter 'name=supabase' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"

# Health check API
curl -s http://192.168.1.163:8000/rest/v1/ -H "apikey: {ANON_KEY}"

# Version
curl -s http://192.168.1.163:8000/rest/v1/rpc/version
```

### Base de Donnees

```bash
# Connexion directe
ssh root@192.168.1.163 "docker exec -it supabase-db psql -U supabase_admin -d postgres"

# Lister les tables
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c '\dt public.*'"

# Taille des tables
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c \"SELECT tablename, pg_size_pretty(pg_total_relation_size('public.' || tablename)) FROM pg_tables WHERE schemaname='public' ORDER BY pg_total_relation_size('public.' || tablename) DESC;\""
```

### Migrations

```bash
# Creer une migration
cat > /opt/supabase/migrations/$(date +%Y%m%d%H%M%S)_description.sql << 'EOF'
-- Migration: description
CREATE TABLE IF NOT EXISTS public.my_table (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at timestamptz DEFAULT now(),
  name text NOT NULL
);

-- RLS
ALTER TABLE public.my_table ENABLE ROW LEVEL SECURITY;
EOF

# Appliquer une migration
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -f /docker-entrypoint-initdb.d/migrations/{file}.sql"

# Lister les migrations appliquees
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c 'SELECT * FROM supabase_migrations.schema_migrations ORDER BY version DESC LIMIT 10;'"
```

### Row Level Security (RLS)

```sql
-- Activer RLS sur une table
ALTER TABLE public.my_table ENABLE ROW LEVEL SECURITY;

-- Policy : lecture pour tous les users authentifies
CREATE POLICY "Users can read" ON public.my_table
  FOR SELECT USING (auth.role() = 'authenticated');

-- Policy : ecriture par le proprietaire
CREATE POLICY "Owner can write" ON public.my_table
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Lister les policies
SELECT * FROM pg_policies WHERE schemaname = 'public';
```

### Authentification

```bash
# Lister les users
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c 'SELECT id, email, created_at, last_sign_in_at FROM auth.users;'"

# Creer un user
curl -s http://192.168.1.163:8000/auth/v1/admin/users \
  -H "Authorization: Bearer {SERVICE_ROLE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password", "email_confirm": true}'
```

### Storage

```bash
# Lister les buckets
curl -s http://192.168.1.163:8000/storage/v1/bucket \
  -H "Authorization: Bearer {SERVICE_ROLE_KEY}"

# Creer un bucket
curl -s http://192.168.1.163:8000/storage/v1/bucket \
  -H "Authorization: Bearer {SERVICE_ROLE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name": "avatars", "public": false}'
```

## Configuration

### Fichiers cles (VM 103)

```
/opt/supabase/
├── docker-compose.yml      # Stack complete
├── .env                    # Variables (ANON_KEY, SERVICE_ROLE_KEY, JWT_SECRET)
├── volumes/
│   ├── db/data/            # Donnees PostgreSQL
│   ├── storage/            # Fichiers uploades
│   └── functions/          # Edge functions
└── migrations/             # SQL migrations
```

### Variables Critiques (.env)

| Variable | Description |
|----------|-------------|
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL |
| `JWT_SECRET` | Secret pour signer les JWT |
| `ANON_KEY` | Cle publique (frontend) |
| `SERVICE_ROLE_KEY` | Cle admin (backend, bypass RLS) |
| `DASHBOARD_USERNAME` | Login Studio |
| `DASHBOARD_PASSWORD` | Password Studio |

## Integration avec les Autres Skills

| Skill | Relation |
|-------|----------|
| **docker-skill** | Containers Supabase |
| **backup-skill** | `/bak-pg` pour backup PostgreSQL Supabase |
| **security-skill** | RLS, credentials, audit |
| **devops-skill** | Deploiement et migrations |
| **monitoring-skill** | Health des containers Supabase |

## Troubleshooting

### Container qui restart en boucle

```bash
# Identifier le container
docker ps -a --filter 'name=supabase' --filter 'status=restarting'

# Voir les logs
docker logs supabase-{service} --tail 50

# Causes frequentes : .env mal configure, PostgreSQL pas demarre
```

### API retourne 401/403

1. Verifier les cles (ANON_KEY, SERVICE_ROLE_KEY)
2. Verifier les RLS policies
3. Verifier que Kong route correctement

### Migration echouee

1. Voir l'erreur : `docker exec supabase-db psql -U supabase_admin -d postgres -c "SELECT * FROM supabase_migrations.schema_migrations ORDER BY version DESC LIMIT 1;"`
2. Rollback manuel si necessaire
3. Ne jamais modifier une migration deja appliquee, en creer une nouvelle
