# Wizard: AI Infrastructure Setup

Configuration initiale de la stack AI du homelab.

## Questions

1. **Providers** : Quels providers LLM utiliser ? (Anthropic, OpenAI, local Ollama)
2. **Observabilite** : Activer Langfuse pour le tracing ?
3. **RAG** : Besoin d'un pipeline RAG ?
4. **Budget** : Budget mensuel API LLM ?

## Processus

### Etape 1 : LiteLLM (VM 103)

```bash
# Creer le repertoire
ssh root@192.168.1.163 "mkdir -p /opt/litellm"

# docker-compose.yml
ssh root@192.168.1.163 "cat > /opt/litellm/docker-compose.yml << 'YAML'
version: '3.8'
services:
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    container_name: litellm
    restart: unless-stopped
    ports:
      - '4000:4000'
    volumes:
      - ./config.yaml:/app/config.yaml
    env_file:
      - .env
    command: ['--config', '/app/config.yaml']
YAML"

# .env avec les API keys
ssh root@192.168.1.163 "cat > /opt/litellm/.env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
EOF"
ssh root@192.168.1.163 "chmod 600 /opt/litellm/.env"

# Demarrer
ssh root@192.168.1.163 "cd /opt/litellm && docker compose up -d"
```

### Etape 2 : Langfuse (VM 103)

```bash
# docker-compose.yml pour Langfuse
# Necessite PostgreSQL (utiliser VM 104 ou local)
ssh root@192.168.1.163 "mkdir -p /opt/langfuse && cd /opt/langfuse && docker compose up -d"
```

### Etape 3 : pgvector (VM 104)

```bash
# Activer l'extension dans PostgreSQL
ssh r2d2helm@192.168.1.164 "psql -U postgres -h localhost -c 'CREATE EXTENSION IF NOT EXISTS vector;'"
```

### Etape 4 : Verification

```bash
# Tester LiteLLM
curl -s http://192.168.1.163:4000/health

# Tester Langfuse
curl -s http://192.168.1.163:3000

# Tester pgvector
ssh r2d2helm@192.168.1.164 "psql -U postgres -h localhost -c \"SELECT extversion FROM pg_extension WHERE extname = 'vector';\""
```
