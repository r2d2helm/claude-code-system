# Commande: /ai-rag

Pipeline RAG : indexation, recherche, status (VM 105).

## Syntaxe

```
/ai-rag [action] [options]
```

## Status

```bash
# Container RAG
ssh r2d2helm@192.168.1.161 "docker ps --filter 'name=rag' --format 'table {{.Names}}\t{{.Status}}'"

# Logs
ssh r2d2helm@192.168.1.161 "docker logs rag-indexer --tail 20"

# Taille de l'index
ssh r2d2helm@192.168.1.161 "du -sh /opt/rag-indexer/data/"
```

## Indexation

```bash
# Indexer un repertoire de documents
ssh r2d2helm@192.168.1.161 "cd /opt/rag-indexer && python index.py --source /path/to/docs"

# Indexer le vault Obsidian (si synchronise)
ssh r2d2helm@192.168.1.161 "cd /opt/rag-indexer && python index.py --source /mnt/nfs/knowledge"

# Re-indexer tout
ssh r2d2helm@192.168.1.161 "cd /opt/rag-indexer && python index.py --rebuild"

# Status de l'index
ssh r2d2helm@192.168.1.161 "cd /opt/rag-indexer && python index.py --status"
```

## Recherche

```bash
# Recherche semantique
ssh r2d2helm@192.168.1.161 "cd /opt/rag-indexer && python search.py --query 'comment configurer Docker'"

# Avec nombre de resultats
ssh r2d2helm@192.168.1.161 "cd /opt/rag-indexer && python search.py --query 'backup PostgreSQL' --top-k 5"
```

## Pipeline

```
Documents → Chunking → Embedding → pgvector (VM 104)
                                        │
Query → Embedding → Similarity Search → │ → Top-K results
                                        └──→ LLM (LiteLLM) → Answer
```

## Configuration

| Parametre | Valeur recommandee |
|-----------|-------------------|
| Chunk size | 512-1024 tokens |
| Chunk overlap | 50-100 tokens |
| Embedding model | text-embedding-3-small |
| Top-K | 5-10 resultats |
| Similarity threshold | > 0.7 |
