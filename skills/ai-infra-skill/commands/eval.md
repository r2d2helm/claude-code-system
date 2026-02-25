# Commande: /ai-eval

Evaluer les performances des modeles LLM.

## Syntaxe

```
/ai-eval [model] [options]
```

## Tests de Base

### Latence

```bash
# Mesurer le temps de reponse
time curl -s http://192.168.1.163:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "{model}", "messages": [{"role": "user", "content": "ping"}], "max_tokens": 10}'
```

### Comparaison Multi-Modeles

```bash
# Tester la meme requete sur plusieurs modeles
for MODEL in claude-sonnet gpt-4o local-llama; do
  echo "=== $MODEL ==="
  time curl -s http://192.168.1.163:4000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d "{\"model\": \"$MODEL\", \"messages\": [{\"role\": \"user\", \"content\": \"Explique Docker en une phrase.\"}], \"max_tokens\": 100}" | python3 -c "import sys,json; r=json.load(sys.stdin); print(r['choices'][0]['message']['content']); print(f'Tokens: {r[\"usage\"][\"total_tokens\"]}')"
  echo
done
```

### Qualite RAG

```bash
# Questions de reference pour evaluer le RAG
QUESTIONS=(
  "Qu'est-ce que le skill proxmox ?"
  "Comment sauvegarder PostgreSQL ?"
  "Quelle est l'IP de VM 103 ?"
)

for Q in "${QUESTIONS[@]}"; do
  echo "Q: $Q"
  # Adapter au endpoint RAG
  curl -s http://192.168.1.161:8000/search -d "query=$Q" | python3 -m json.tool
  echo
done
```

## Metriques d'Evaluation

| Metrique | Bon | Moyen | Mauvais |
|----------|-----|-------|---------|
| Latence (TTFB) | < 1s | 1-5s | > 5s |
| Latence (total) | < 5s | 5-15s | > 15s |
| Pertinence RAG | > 0.8 | 0.5-0.8 | < 0.5 |
| Cout/requete | < $0.01 | $0.01-0.05 | > $0.05 |
