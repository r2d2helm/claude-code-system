# Commande: /ai-models

Gerer les modeles LLM disponibles via LiteLLM.

## Syntaxe

```
/ai-models [action] [model]
```

## Lister les Modeles

```bash
# Via API
curl -s http://192.168.1.163:4000/v1/models | python3 -m json.tool

# Via config
ssh root@192.168.1.163 "cat /opt/litellm/config.yaml | grep 'model_name\|model:'"
```

## Ajouter un Modele

```yaml
# Ajouter dans /opt/litellm/config.yaml
model_list:
  # ... modeles existants ...
  - model_name: {alias}
    litellm_params:
      model: {provider}/{model_id}
      api_key: os.environ/{ENV_VAR}
      # api_base: http://... (pour local)
```

```bash
# Recharger
ssh root@192.168.1.163 "docker restart litellm"
```

## Providers Supportes

| Provider | Format model | API Key |
|----------|-------------|---------|
| Anthropic | `anthropic/claude-*` | ANTHROPIC_API_KEY |
| OpenAI | `openai/gpt-*` | OPENAI_API_KEY |
| Ollama (local) | `ollama/{model}` | Pas de cle |
| Mistral | `mistral/{model}` | MISTRAL_API_KEY |
| Google | `gemini/{model}` | GOOGLE_API_KEY |

## Tester un Modele

```bash
curl -s http://192.168.1.163:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"{model_name}\", \"messages\": [{\"role\": \"user\", \"content\": \"Reponds en une phrase: qui es-tu?\"}], \"max_tokens\": 100}" | python3 -m json.tool
```
