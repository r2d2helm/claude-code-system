# Commande: /supa-migration

Gerer les migrations de schema Supabase.

## Syntaxe

```
/supa-migration [action] [options]
```

## Creer une Migration

```bash
# Generer le fichier
TIMESTAMP=$(date +%Y%m%d%H%M%S)
ssh root@192.168.1.163 "cat > /opt/supabase/migrations/${TIMESTAMP}_{description}.sql << 'EOF'
-- Migration: {description}
-- Date: $(date +%Y-%m-%d)

{SQL_STATEMENTS}
EOF"
```

## Appliquer

```bash
# Appliquer une migration
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -f /docker-entrypoint-initdb.d/migrations/{file}.sql"

# Appliquer toutes les migrations en attente
ssh root@192.168.1.163 "for f in /opt/supabase/migrations/*.sql; do docker exec supabase-db psql -U supabase_admin -d postgres -f \$f; done"
```

## Status

```bash
# Migrations appliquees
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c 'SELECT * FROM supabase_migrations.schema_migrations ORDER BY version DESC LIMIT 10;'"
```

## Rollback

```bash
# Creer une migration de rollback
ssh root@192.168.1.163 "cat > /opt/supabase/migrations/${TIMESTAMP}_rollback_{description}.sql << 'EOF'
-- Rollback: {description}
DROP TABLE IF EXISTS public.{table};
-- ou ALTER TABLE, DROP COLUMN, etc.
EOF"
```

## Bonnes Pratiques

- **Nommage** : `{timestamp}_{description}.sql`
- **Idempotent** : utiliser `IF NOT EXISTS`, `IF EXISTS`
- **Tester** sur staging avant production
- **Jamais** modifier une migration deja appliquee
- **Backup** avant toute migration destructive
