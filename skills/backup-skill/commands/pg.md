# Commande: /bak-pg

Backup et restauration specifique PostgreSQL sur VM 104 (192.168.1.164).

## Syntaxe

```
/bak-pg [action] [options]
```

## Backup

```bash
# Dump format custom (recommande : compresse, restauration selective)
ssh r2d2helm@192.168.1.164 "pg_dump -Fc -U postgres -h localhost {dbname} -f /mnt/nfs/backups/postgresql/pg-{dbname}-$(date +%Y-%m-%d_%H%M%S).dump"

# Dump toutes les bases
ssh r2d2helm@192.168.1.164 "pg_dumpall -U postgres -h localhost -f /mnt/nfs/backups/postgresql/pg-all-$(date +%Y-%m-%d_%H%M%S).sql"

# Dump compresse SQL
ssh r2d2helm@192.168.1.164 "pg_dump -U postgres -h localhost {dbname} | gzip > /mnt/nfs/backups/postgresql/pg-{dbname}-$(date +%Y-%m-%d_%H%M%S).sql.gz"

# Dump d'une table specifique
ssh r2d2helm@192.168.1.164 "pg_dump -Fc -U postgres -h localhost -t {table} {dbname} -f /tmp/pg-{table}.dump"

# Dump schema only (structure sans donnees)
ssh r2d2helm@192.168.1.164 "pg_dump -Fc -U postgres -h localhost --schema-only {dbname} -f /tmp/pg-{dbname}-schema.dump"
```

## Restauration

```bash
# Restaurer un dump custom
ssh r2d2helm@192.168.1.164 "pg_restore -U postgres -h localhost -d {dbname} --clean --if-exists {dumpfile}.dump"

# Restaurer dans une nouvelle base
ssh r2d2helm@192.168.1.164 "createdb -U postgres {newdb} && pg_restore -U postgres -h localhost -d {newdb} {dumpfile}.dump"

# Restaurer une table specifique
ssh r2d2helm@192.168.1.164 "pg_restore -U postgres -h localhost -d {dbname} -t {table} {dumpfile}.dump"

# Restaurer un dump SQL
ssh r2d2helm@192.168.1.164 "gunzip -c {file}.sql.gz | psql -U postgres -h localhost -d {dbname}"
```

## Diagnostic

```bash
# Verifier la connexion
ssh r2d2helm@192.168.1.164 "pg_isready -h localhost"

# Lister les bases
ssh r2d2helm@192.168.1.164 "psql -U postgres -h localhost -l"

# Taille des bases
ssh r2d2helm@192.168.1.164 "psql -U postgres -h localhost -c \"SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC;\""

# Connexions actives
ssh r2d2helm@192.168.1.164 "psql -U postgres -h localhost -c \"SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;\""
```

## Bases Connues (VM 104)

| Base | Usage | Taille estimee |
|------|-------|----------------|
| postgres | Defaut | Minimal |
| taskyn | Gestion de projet Taskyn | Variable |
| supabase* | Stack Supabase (sur VM 103) | Variable |

## Options pg_dump Importantes

| Option | Description |
|--------|-------------|
| `-Fc` | Format custom (compresse, restauration selective) |
| `-Fp` | Format plain SQL |
| `-Fd` | Format directory (parallele) |
| `--clean` | Generer DROP avant CREATE |
| `--if-exists` | IF EXISTS avec --clean |
| `-j N` | Parallelisme (format directory) |
| `-t table` | Table specifique |
| `--schema-only` | Structure sans donnees |
| `--data-only` | Donnees sans structure |
