# Commande: /ai-embed

Operations d'embedding (generer, comparer, tester).

## Syntaxe

```
/ai-embed [action] [options]
```

## Generer des Embeddings

```bash
# Via LiteLLM (OpenAI-compatible)
curl -s http://192.168.1.163:4000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "text-embedding-3-small", "input": "Comment configurer Docker"}' | python3 -m json.tool

# Batch
curl -s http://192.168.1.163:4000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "text-embedding-3-small", "input": ["texte 1", "texte 2", "texte 3"]}'
```

## Comparer la Similarite

```python
# Script Python rapide
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Comparer deux textes via leurs embeddings
# similarity > 0.8 = tres similaire
# similarity 0.5-0.8 = lie
# similarity < 0.5 = different
```

## Modeles d'Embedding

| Modele | Dimensions | Vitesse | Qualite |
|--------|-----------|---------|---------|
| text-embedding-3-small | 1536 | Rapide | Bonne |
| text-embedding-3-large | 3072 | Moyen | Excellente |
| nomic-embed-text (local) | 768 | Local | Bonne |

## Bonnes Pratiques

- **Meme modele** pour indexation et recherche
- **Normaliser** les embeddings avant stockage
- **Batch** les requetes pour reduire la latence
- **Cache** les embeddings de documents statiques
