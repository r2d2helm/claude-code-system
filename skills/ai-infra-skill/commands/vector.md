# Commande: /ai-vector

Gestion du vector store pgvector (VM 104).

## Syntaxe

```
/ai-vector [action]
```

## Status

```bash
# Verifier l'extension pgvector
ssh r2d2helm@192.168.1.164 "psql -U postgres -h localhost -c \"SELECT * FROM pg_extension WHERE extname = 'vector';\""

# Taille des tables d'embeddings
ssh r2d2helm@192.168.1.164 "psql -U postgres -h localhost -c \"SELECT tablename, pg_size_pretty(pg_total_relation_size('public.' || tablename)) FROM pg_tables WHERE schemaname = 'public' AND tablename LIKE '%embed%' ORDER BY pg_total_relation_size('public.' || tablename) DESC;\""

# Nombre de vecteurs
ssh r2d2helm@192.168.1.164 "psql -U postgres -h localhost -c \"SELECT count(*) FROM embeddings;\""
```

## Installation pgvector

```sql
-- Installer l'extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Creer une table d'embeddings
CREATE TABLE IF NOT EXISTS embeddings (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  metadata JSONB,
  embedding vector(1536),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index HNSW pour recherche rapide
CREATE INDEX ON embeddings USING hnsw (embedding vector_cosine_ops);
```

## Recherche Vectorielle

```sql
-- Top 5 plus similaires
SELECT id, content, metadata,
  1 - (embedding <=> '[0.1, 0.2, ...]') AS similarity
FROM embeddings
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 5;

-- Avec seuil de similarite
SELECT id, content,
  1 - (embedding <=> '[...]') AS similarity
FROM embeddings
WHERE 1 - (embedding <=> '[...]') > 0.7
ORDER BY embedding <=> '[...]'
LIMIT 10;
```

## Maintenance

```bash
# Vacuum et reindex
ssh r2d2helm@192.168.1.164 "psql -U postgres -h localhost -c 'VACUUM ANALYZE embeddings;'"

# Backup des embeddings
ssh r2d2helm@192.168.1.164 "pg_dump -Fc -U postgres -h localhost -t embeddings ragdb > /mnt/nfs/backups/postgresql/pg-embeddings-$(date +%Y-%m-%d).dump"
```
