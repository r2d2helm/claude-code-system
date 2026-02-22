"""Recherche hybride keyword + semantic pour Memory v2.

Trois modes:
- keyword: recherche par mots-cles dans content+tags (existant, via LIKE)
- semantic: recherche par similarite cosinus sur embeddings
- hybrid: combinaison ponderee (0.7 semantic + 0.3 keyword)

Scores normalises 0-1 pour coherence entre modes.
Fail-open: si embeddings indisponibles, fallback automatique sur keyword.

Inspire du Second Brain (Dynamous Community).
"""

import re
from typing import Optional

from .memory_db import search_memories, get_all_vectors, increment_access, log_retrieval
from .embeddings import (
    is_available as embeddings_available,
    embed_text,
    blob_to_embedding,
    cosine_similarity,
)

# ============================================================
# Configuration
# ============================================================

HYBRID_VECTOR_WEIGHT = 0.7
HYBRID_KEYWORD_WEIGHT = 0.3
DEFAULT_LIMIT = 10

# Stopwords compacte FR+EN
_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "have", "has",
    "had", "do", "does", "did", "will", "would", "could", "should", "can",
    "to", "of", "in", "for", "on", "with", "at", "by", "from", "as", "and",
    "but", "or", "not", "no", "if", "so", "this", "that", "it", "its",
    "le", "la", "les", "de", "du", "des", "un", "une", "et", "en", "est",
    "que", "qui", "dans", "pour", "pas", "sur", "avec", "ce", "je", "nous",
    "me", "my", "you", "your", "we", "our", "they", "them", "their",
}


# ============================================================
# Keyword search (normalise)
# ============================================================

def _extract_keywords(text: str) -> list[str]:
    """Extrait les mots-cles significatifs d'un texte."""
    words = re.findall(r"\b[a-zA-Z_][\w.-]{2,}\b", text.lower())
    seen = set()
    unique = []
    for w in words:
        if w not in _STOPWORDS and w not in seen:
            seen.add(w)
            unique.append(w)
    return unique[:15]


def _keyword_score(content: str, tags: str, keywords: list[str]) -> float:
    """Calcule un score keyword normalise 0-1."""
    if not keywords:
        return 0.0
    text = (content + " " + tags).lower()
    matched = sum(1 for kw in keywords if kw in text)
    return matched / len(keywords)


def keyword_search(
    query: str,
    limit: int = DEFAULT_LIMIT,
    min_importance: float = 0.0,
    days_back: Optional[int] = None,
) -> list[dict]:
    """Recherche par mots-cles. Retourne des resultats avec score normalise."""
    keywords = _extract_keywords(query)
    if not keywords:
        return []

    raw = search_memories(
        keywords=keywords,
        min_importance=min_importance,
        limit=limit * 3,
        days_back=days_back,
    )

    results = []
    for m in raw:
        score = _keyword_score(m.get("content", ""), m.get("tags", "[]"), keywords)
        if score > 0:
            results.append({**m, "score": score, "mode": "keyword"})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


# ============================================================
# Semantic search
# ============================================================

def semantic_search(
    query: str,
    limit: int = DEFAULT_LIMIT,
) -> list[dict]:
    """Recherche par similarite cosinus. Retourne des resultats avec score normalise 0-1."""
    if not embeddings_available():
        return []

    query_embedding = embed_text(query)
    if query_embedding is None:
        return []

    all_vectors = get_all_vectors()
    if not all_vectors:
        return []

    results = []
    for v in all_vectors:
        try:
            stored_embedding = blob_to_embedding(v["embedding"])
            sim = cosine_similarity(query_embedding, stored_embedding)
            # Normaliser: cosine sim va de -1 a 1, on mappe sur 0-1
            normalized = (sim + 1) / 2
            results.append({
                "id": v["memory_id"],
                "content": v["content"],
                "type": v["type"],
                "tags": v["tags"],
                "importance_score": v["importance_score"],
                "decay_score": v["decay_score"],
                "created_at": v["created_at"],
                "access_count": v["access_count"],
                "score": normalized,
                "mode": "semantic",
            })
        except Exception:
            continue

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


# ============================================================
# Hybrid search
# ============================================================

def hybrid_search(
    query: str,
    limit: int = DEFAULT_LIMIT,
    vector_weight: float = HYBRID_VECTOR_WEIGHT,
    keyword_weight: float = HYBRID_KEYWORD_WEIGHT,
    min_importance: float = 0.0,
    days_back: Optional[int] = None,
) -> list[dict]:
    """Recherche hybride: combine keyword et semantic.

    Si embeddings indisponibles, fallback automatique sur keyword.
    Scores normalises 0-1 pour les deux modes.
    """
    kw_results = keyword_search(query, limit=limit * 2, min_importance=min_importance, days_back=days_back)

    # Fallback keyword-only si pas d'embeddings
    if not embeddings_available():
        for r in kw_results:
            r["mode"] = "keyword_only"
        return kw_results[:limit]

    sem_results = semantic_search(query, limit=limit * 2)

    if not sem_results:
        for r in kw_results:
            r["mode"] = "keyword_only"
        return kw_results[:limit]

    # Merge par memory_id
    scores: dict[int, dict] = {}

    for r in kw_results:
        mid = r.get("id")
        if mid is None:
            continue
        scores[mid] = {
            **r,
            "kw_score": r["score"],
            "sem_score": 0.0,
            "score": keyword_weight * r["score"],
            "mode": "hybrid",
        }

    for r in sem_results:
        mid = r.get("id")
        if mid is None:
            continue
        if mid in scores:
            scores[mid]["sem_score"] = r["score"]
            scores[mid]["score"] = (
                vector_weight * r["score"]
                + keyword_weight * scores[mid]["kw_score"]
            )
        else:
            scores[mid] = {
                **r,
                "kw_score": 0.0,
                "sem_score": r["score"],
                "score": vector_weight * r["score"],
                "mode": "hybrid",
            }

    results = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    return results[:limit]


# ============================================================
# Convenience: search with auto-mode
# ============================================================

def search(
    query: str,
    mode: str = "hybrid",
    limit: int = DEFAULT_LIMIT,
    min_importance: float = 0.0,
    days_back: Optional[int] = None,
    session_id: str = "",
    log_retrieval_event: str = "",
) -> list[dict]:
    """Point d'entree principal. Mode: keyword, semantic, hybrid.

    Si log_retrieval_event est non-vide, log les resultats dans retrieval_log
    et incremente access_count (closed-loop).
    """
    if mode == "keyword":
        results = keyword_search(query, limit, min_importance, days_back)
    elif mode == "semantic":
        results = semantic_search(query, limit)
    else:
        results = hybrid_search(query, limit, min_importance=min_importance, days_back=days_back)

    # Closed-loop: log retrieval + increment access
    if log_retrieval_event and session_id:
        for r in results:
            mid = r.get("id")
            if mid:
                increment_access(mid)
                search_mode = r.get("mode", mode)
                log_retrieval(mid, None, session_id, log_retrieval_event, search_mode=search_mode)

    return results
