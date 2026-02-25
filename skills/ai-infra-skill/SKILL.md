---
name: ai-infra-skill
description: "Infrastructure AI : LiteLLM, Langfuse, RAG, modeles LLM, embeddings, vector stores, evaluation, observabilite AI."
prefix: /ai-*
---

# Super Agent AI Infrastructure

Agent intelligent pour gerer l'infrastructure AI du homelab r2d2 : proxys LLM, observabilite, RAG, embeddings, evaluation.

## Philosophie

> "L'IA est aussi fiable que l'infrastructure qui la porte."

## Stack AI

| Service | VM | Port | Role |
|---------|-----|------|------|
| LiteLLM | 103 | :4000 | Proxy LLM unifie (OpenAI-compatible) |
| Langfuse | 103 | :3000 | Observabilite et tracing LLM |
| RAG Indexer | 105 | - | Indexation et recherche vectorielle |
| PostgreSQL (pgvector) | 104 | :5432 | Vector store |

## Architecture

```
Clients (Claude Code, Apps)
        │
        ▼
   LiteLLM Proxy (.163:4000)
   ┌─────────────────────────┐
   │  Routing, rate limiting  │
   │  Caching, load balancing │
   └─────────┬───────────────┘
             │
   ┌─────────┼──────────┐
   │         │          │
   ▼         ▼          ▼
 Anthropic  OpenAI   Ollama (local)
 Claude     GPT-4    Llama, Mistral

        Langfuse (.163:3000)
        ┌───────────────────┐
        │ Traces, costs     │
        │ Evaluations       │
        │ Prompt management │
        └───────────────────┘

   RAG Pipeline (.161)
   ┌─────────────────────┐
   │ Indexer → Embeddings │
   │ pgvector → Search    │
   └─────────────────────┘
```

## Commandes Slash

### LiteLLM

| Commande | Description |
|----------|-------------|
| `/ai-litellm` | Status et gestion du proxy LiteLLM |
| `/ai-models` | Lister, ajouter, configurer les modeles disponibles |
| `/ai-usage` | Stats d'utilisation (tokens, couts, latence) |

### Langfuse

| Commande | Description |
|----------|-------------|
| `/ai-langfuse` | Status et gestion de Langfuse (traces, sessions) |
| `/ai-eval` | Evaluer les performances des modeles |
| `/ai-prompts` | Gestion des prompts versiones |

### RAG

| Commande | Description |
|----------|-------------|
| `/ai-rag` | Pipeline RAG (indexation, recherche, status) |
| `/ai-embed` | Operations d'embedding (generer, comparer, tester) |
| `/ai-vector` | Gestion du vector store pgvector |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/ai-wizard setup` | Configuration initiale de la stack AI |
| `/ai-wizard rag` | Creation d'un pipeline RAG de bout en bout |

## LiteLLM - Guide Rapide

### Configuration

```yaml
# /opt/litellm/config.yaml (VM 103)
model_list:
  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-sonnet-4-20250514
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: local-llama
    litellm_params:
      model: ollama/llama3.2
      api_base: http://localhost:11434
```

### Operations

```bash
# Status
ssh root@192.168.1.163 "docker logs litellm --tail 20"

# Tester un modele
curl -s http://192.168.1.163:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "claude-sonnet", "messages": [{"role": "user", "content": "ping"}]}'

# Lister les modeles
curl -s http://192.168.1.163:4000/v1/models | python3 -m json.tool

# Health check
curl -s http://192.168.1.163:4000/health
```

## Langfuse - Guide Rapide

### Operations

```bash
# Status
ssh root@192.168.1.163 "docker logs langfuse --tail 20"

# Web UI
# http://192.168.1.163:3000

# API - Lister les traces recentes
curl -s http://192.168.1.163:3000/api/public/traces?limit=10 \
  -H "Authorization: Basic $(echo -n 'pk:sk' | base64)"
```

### Metriques cles

- **Latence P50/P95** par modele
- **Cout total** par jour/semaine/mois
- **Taux d'erreur** par provider
- **Tokens** utilises par modele

## RAG Pipeline - Guide Rapide

### Indexation

```bash
# Indexer des documents
ssh r2d2helm@192.168.1.161 "cd /opt/rag-indexer && python index.py --source /path/to/docs"

# Verifier l'index
ssh r2d2helm@192.168.1.161 "cd /opt/rag-indexer && python index.py --status"
```

### Recherche

```bash
# Requete vectorielle
ssh r2d2helm@192.168.1.161 "cd /opt/rag-indexer && python search.py --query 'ma question'"
```

### pgvector (VM 104)

```sql
-- Verifier l'extension
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Taille des embeddings
SELECT count(*), pg_size_pretty(pg_total_relation_size('embeddings')) FROM embeddings;

-- Recherche de similarite
SELECT content, 1 - (embedding <=> '[0.1, 0.2, ...]') AS similarity
FROM embeddings ORDER BY embedding <=> '[0.1, 0.2, ...]' LIMIT 5;
```

## Integration avec les Autres Skills

| Skill | Relation |
|-------|----------|
| **docker-skill** | Containers LiteLLM, Langfuse, RAG |
| **monitoring-skill** | Metriques services AI via Netdata/Beszel |
| **devops-skill** | Deploiement et mises a jour de la stack |
| **backup-skill** | Sauvegarde configs et donnees pgvector |
| **knowledge-skill** | RAG indexe les notes du vault Obsidian |

## Best Practices

- **Rate limiting** : configurer des limites par utilisateur/modele dans LiteLLM
- **Fallback** : definir des modeles de fallback (Claude → GPT-4 → local)
- **Caching** : activer le cache semantique pour reduire les couts
- **Monitoring** : surveiller les couts quotidiens via Langfuse
- **Embeddings** : utiliser le meme modele pour indexation et recherche
- **Chunking** : 512-1024 tokens par chunk pour le RAG
- **Evaluation** : tester regulierement la qualite du RAG avec des questions connues
