# Commande: /ai-prompts

Gestion des prompts versiones via Langfuse.

## Syntaxe

```
/ai-prompts [action] [name]
```

## Lister

```bash
curl -s "http://192.168.1.163:3000/api/public/v2/prompts" \
  -H "Authorization: Basic {base64_credentials}" | python3 -m json.tool
```

## Obtenir un Prompt

```bash
# Derniere version
curl -s "http://192.168.1.163:3000/api/public/v2/prompts/{name}" \
  -H "Authorization: Basic {base64_credentials}" | python3 -m json.tool

# Version specifique
curl -s "http://192.168.1.163:3000/api/public/v2/prompts/{name}?version={n}" \
  -H "Authorization: Basic {base64_credentials}" | python3 -m json.tool
```

## Creer / Mettre a Jour

```bash
curl -s "http://192.168.1.163:3000/api/public/v2/prompts" \
  -H "Authorization: Basic {base64_credentials}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "{name}",
    "prompt": "Tu es un assistant specialise en {domain}. Reponds de maniere concise.",
    "config": {"temperature": 0.7, "max_tokens": 500},
    "labels": ["production"]
  }'
```

## Bonnes Pratiques

- **Versionner** tous les prompts de production dans Langfuse
- **Labels** : `production`, `staging`, `experiment`
- **Tester** avant de promouvoir en production
- **Mesurer** les performances via les traces Langfuse
