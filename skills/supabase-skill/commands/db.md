# Commande: /supa-db

Operations base de donnees Supabase (VM 103).

## Syntaxe

```
/supa-db [action] [options]
```

## Connexion

```bash
# Shell PostgreSQL
ssh root@192.168.1.163 "docker exec -it supabase-db psql -U supabase_admin -d postgres"

# Commande unique
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c '{SQL}'"
```

## Tables

```bash
# Lister les tables public
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c '\dt public.*'"

# Schema d'une table
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c '\d public.{table}'"

# Taille des tables
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c \"
SELECT tablename,
  pg_size_pretty(pg_total_relation_size('public.' || tablename)) as size,
  (SELECT count(*) FROM public.\\\"\" || tablename || \"\\\") as rows
FROM pg_tables WHERE schemaname='public'
ORDER BY pg_total_relation_size('public.' || tablename) DESC;\""
```

## Requetes Utiles

```sql
-- Connexions actives
SELECT pid, usename, application_name, state, query_start
FROM pg_stat_activity WHERE datname = 'postgres';

-- Tables les plus volumineuses
SELECT schemaname, tablename,
  pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename))
FROM pg_tables ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC LIMIT 10;

-- Index inutilises
SELECT indexrelname, idx_scan FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND indexrelname NOT LIKE '%pkey%';
```
