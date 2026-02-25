# Commande: /ai-litellm

Status et gestion du proxy LiteLLM (VM 103).

## Syntaxe

```
/ai-litellm [action]
```

## Operations

### Status

```bash
# Health check
curl -s http://192.168.1.163:4000/health | python3 -m json.tool

# Logs
ssh root@192.168.1.163 "docker logs litellm --tail 30"

# Container status
ssh root@192.168.1.163 "docker ps --filter 'name=litellm' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
```

### Configuration

```bash
# Voir la config
ssh root@192.168.1.163 "cat /opt/litellm/config.yaml"

# Recharger apres modification
ssh root@192.168.1.163 "docker restart litellm"
```

### Test Rapide

```bash
# Tester un appel
curl -s http://192.168.1.163:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "claude-sonnet", "messages": [{"role": "user", "content": "Hello"}], "max_tokens": 50}'

# Lister les modeles disponibles
curl -s http://192.168.1.163:4000/v1/models | python3 -m json.tool
```

### Metriques

```bash
# Utilisation recente
curl -s http://192.168.1.163:4000/spend/logs | python3 -m json.tool

# Couts par modele
curl -s http://192.168.1.163:4000/spend/tags | python3 -m json.tool
```
