# Commande: /ai-langfuse

Status et gestion de Langfuse (observabilite LLM) sur VM 103.

## Syntaxe

```
/ai-langfuse [action]
```

## Status

```bash
# Container
ssh root@192.168.1.163 "docker ps --filter 'name=langfuse' --format 'table {{.Names}}\t{{.Status}}'"

# Logs
ssh root@192.168.1.163 "docker logs langfuse --tail 20"

# Web UI : http://192.168.1.163:3000
```

## Traces

```bash
# Traces recentes
curl -s "http://192.168.1.163:3000/api/public/traces?limit=10" \
  -H "Authorization: Basic {base64_credentials}" | python3 -m json.tool

# Trace specifique
curl -s "http://192.168.1.163:3000/api/public/traces/{trace_id}" \
  -H "Authorization: Basic {base64_credentials}" | python3 -m json.tool
```

## Sessions

```bash
# Lister les sessions
curl -s "http://192.168.1.163:3000/api/public/sessions?limit=10" \
  -H "Authorization: Basic {base64_credentials}" | python3 -m json.tool
```

## Prompt Management

```bash
# Lister les prompts versiones
curl -s "http://192.168.1.163:3000/api/public/v2/prompts" \
  -H "Authorization: Basic {base64_credentials}" | python3 -m json.tool

# Creer un prompt
curl -s "http://192.168.1.163:3000/api/public/v2/prompts" \
  -H "Authorization: Basic {base64_credentials}" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-prompt", "prompt": "Tu es un assistant...", "labels": ["production"]}'
```
