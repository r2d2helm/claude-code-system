# Wizard: RAG Pipeline

Creation guidee d'un pipeline RAG de bout en bout.

## Questions

1. **Sources** : Quels documents indexer ? (vault Obsidian, docs projet, PDF)
2. **Modele embedding** : text-embedding-3-small (API) ou nomic-embed (local) ?
3. **Vector store** : pgvector (VM 104) ?
4. **LLM** : Quel modele pour la generation ? (Claude, GPT-4, local)

## Architecture

```
Sources → Loader → Chunker → Embedder → pgvector
                                            │
User Query → Embedder → Search ─────────────┘
                           │
                    Top-K chunks + Query → LLM → Response
```

## Processus

### Etape 1 : Preparer les sources

```bash
# Synchroniser le vault vers la VM
rsync -avz --exclude='.git' --exclude='_Attachments' \
  "C:\Users\r2d2\Documents\Knowledge/" \
  r2d2helm@192.168.1.161:/mnt/nfs/knowledge/
```

### Etape 2 : Configurer le chunking

| Parametre | Valeur | Raison |
|-----------|--------|--------|
| Chunk size | 512 tokens | Equilibre contexte/precision |
| Overlap | 50 tokens | Continuite entre chunks |
| Separateurs | `\n\n`, `\n`, `. ` | Couper aux frontieres naturelles |

### Etape 3 : Generer les embeddings

```bash
# Indexer les documents
ssh r2d2helm@192.168.1.161 "cd /opt/rag-indexer && python index.py \
  --source /mnt/nfs/knowledge \
  --model text-embedding-3-small \
  --chunk-size 512 \
  --overlap 50"
```

### Etape 4 : Tester la recherche

```bash
# Requetes de test
ssh r2d2helm@192.168.1.161 "cd /opt/rag-indexer && python search.py \
  --query 'Comment configurer Proxmox' --top-k 5"
```

### Etape 5 : Evaluer la qualite

Creer un jeu de test (questions + reponses attendues) et mesurer :
- Recall@5 : la bonne reponse est-elle dans les 5 premiers chunks ?
- Pertinence : score moyen de similarite des resultats
- Qualite reponse : la reponse generee est-elle correcte ?
