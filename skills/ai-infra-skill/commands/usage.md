# Commande: /ai-usage

Stats d'utilisation des modeles LLM (tokens, couts, latence).

## Syntaxe

```
/ai-usage [periode]
```

## Via LiteLLM

```bash
# Logs de depense
curl -s http://192.168.1.163:4000/spend/logs?start_date=$(date -d '-7 days' +%Y-%m-%d) | python3 -m json.tool

# Par modele
curl -s http://192.168.1.163:4000/spend/tags | python3 -m json.tool

# Par cle API
curl -s http://192.168.1.163:4000/spend/keys | python3 -m json.tool
```

## Via Langfuse

```bash
# Dashboard web
# http://192.168.1.163:3000

# API : traces recentes
curl -s http://192.168.1.163:3000/api/public/traces?limit=20 \
  -H "Authorization: Basic {base64_pk:sk}" | python3 -m json.tool

# Couts
curl -s http://192.168.1.163:3000/api/public/metrics/daily \
  -H "Authorization: Basic {base64_pk:sk}" | python3 -m json.tool
```

## Metriques Cles

| Metrique | Description | Seuil alerte |
|----------|-------------|-------------|
| Tokens/jour | Consommation quotidienne | > 100K tokens |
| Cout/jour | Depense quotidienne | > $5 |
| Latence P95 | Temps de reponse | > 10s |
| Erreurs | Taux d'echec | > 5% |
| Cache hit | Requetes servies du cache | < 20% |
