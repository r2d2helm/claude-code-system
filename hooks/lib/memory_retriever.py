"""Moteur de recuperation contextuelle pour Memory v2.

Fournit des memoires pertinentes pour injection dans additionalContext.
Deux modes:
- startup: memoires recentes haute-importance + facts haute-confiance (max 500 chars)
- per_prompt: memoires matchant les keywords du message (max 300 chars)

Scoring: effective_score = keyword_match * importance_score * decay_score * recency_boost
"""

import re
from datetime import datetime, timedelta
from pathlib import Path

from .paths import CONFIG_DIR
from .memory_db import (
    get_recent_memories, get_high_confidence_facts, search_memories,
    get_facts, increment_access, log_retrieval,
)

# Import hybrid search (fail-open si absent)
try:
    from .memory_search import search as hybrid_search
    from .embeddings import is_available as embeddings_available
    HAS_HYBRID = True
except Exception:
    HAS_HYBRID = False

    def embeddings_available():
        return False

# ============================================================
# Configuration
# ============================================================

def _load_retrieval_config() -> dict:
    """Charge la section retrieval de memory_v2.yaml."""
    defaults = {
        "startup": {
            "max_chars": 500,
            "max_facts": 5,
            "max_memories": 5,
            "facts_min_confidence": 0.7,
            "memories_min_importance": 6.0,
            "memories_days_back": 7,
        },
        "per_prompt": {
            "max_chars": 300,
            "max_results": 3,
            "min_message_length": 20,
            "skip_commands": True,
        },
        "scoring": {
            "recency_boost_7d": 0.5,
            "recency_boost_14d": 0.3,
        },
    }
    try:
        config_path = CONFIG_DIR / "memory_v2.yaml"
        if config_path.exists():
            import yaml
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            retrieval = raw.get("retrieval", {})
            for key in defaults:
                if key in retrieval and isinstance(retrieval[key], dict):
                    defaults[key].update(retrieval[key])
    except Exception as e:
        import logging
        logging.warning("memory_retriever: config load failed, using defaults: %s", e)
    return defaults


_RETRIEVAL_CONFIG = None


def _get_retrieval_config() -> dict:
    global _RETRIEVAL_CONFIG
    if _RETRIEVAL_CONFIG is None:
        _RETRIEVAL_CONFIG = _load_retrieval_config()
    return _RETRIEVAL_CONFIG


# ============================================================
# Scoring
# ============================================================

def _compute_recency_boost(created_at: str) -> float:
    """Calcule le bonus de recence."""
    if not created_at:
        return 0.0
    config = _get_retrieval_config()
    scoring = config.get("scoring", {})
    boost_7d = scoring.get("recency_boost_7d", 0.5)
    boost_14d = scoring.get("recency_boost_14d", 0.3)

    try:
        # Parse ISO timestamp via fromisoformat (Python 3.11+)
        ts_clean = created_at.replace("Z", "+00:00")
        created = datetime.fromisoformat(ts_clean)
        now = datetime.now(created.tzinfo) if created.tzinfo else datetime.now()
        age_days = (now - created).days
        if age_days < 7:
            return boost_7d
        if age_days < 14:
            return boost_14d
        return 0.0
    except (ValueError, TypeError):
        return 0.0


def _compute_keyword_match(content: str, tags_str: str, keywords: list[str]) -> float:
    """Calcule la proportion de keywords trouves dans content+tags."""
    if not keywords:
        return 1.0  # Pas de filtre keyword = match total
    content_lower = (content + " " + tags_str).lower()
    matched = sum(1 for kw in keywords if kw.lower() in content_lower)
    return matched / len(keywords)


def _effective_score(memory: dict, keywords: list[str] | None = None) -> float:
    """Calcule le score effectif d'une memoire."""
    importance = memory.get("importance_score", 5.0)
    decay = memory.get("decay_score", 1.0)
    recency = _compute_recency_boost(memory.get("created_at", ""))

    kw_match = 1.0
    if keywords:
        kw_match = _compute_keyword_match(
            memory.get("content", ""),
            memory.get("tags", "[]"),
            keywords,
        )

    return kw_match * importance * decay + recency


# ============================================================
# Retrieval modes
# ============================================================

def retrieve_for_startup(session_id: str = "") -> str:
    """Recupere les memoires a injecter au demarrage.

    Retourne une string formatee (max 500 chars) ou "" si rien de pertinent.
    """
    try:
        config = _get_retrieval_config()
        startup = config.get("startup", {})
        max_chars = startup.get("max_chars", 500)

        # 1. Facts haute-confiance
        facts = get_high_confidence_facts(
            min_confidence=startup.get("facts_min_confidence", 0.7),
            limit=startup.get("max_facts", 5),
        )

        # 2. Memoires recentes haute-importance
        memories = get_recent_memories(
            days=startup.get("memories_days_back", 7),
            min_importance=startup.get("memories_min_importance", 6.0),
            limit=startup.get("max_memories", 5),
        )

        if not facts and not memories:
            return ""

        # Formatter
        parts = []

        if facts:
            fact_lines = []
            for f in facts:
                fact_lines.append(f"- {f['key']}: {f['value'][:60]}")
                # Log retrieval
                if session_id:
                    log_retrieval(None, f.get("id"), session_id, "SessionStart", search_mode="startup")
            parts.append("Facts: " + "; ".join(f"{f['key']}: {f['value'][:40]}" for f in facts))

        if memories:
            mem_lines = []
            for m in memories:
                mem_lines.append(f"[{m['type']}] {m['content'][:60]}")
                # Increment access + log retrieval
                if m.get("id"):
                    increment_access(m["id"])
                    if session_id:
                        log_retrieval(m["id"], None, session_id, "SessionStart", search_mode="startup")
            parts.append("Recent: " + "; ".join(
                f"{m['content'][:50]}" for m in memories
            ))

        result = " | ".join(parts)
        return result[:max_chars]

    except Exception:
        return ""


def retrieve_for_prompt(message: str, session_id: str = "") -> str:
    """Recupere les memoires pertinentes pour un prompt utilisateur.

    Retourne une string formatee (max 300 chars) ou "" si pas pertinent.
    """
    try:
        config = _get_retrieval_config()
        prompt_cfg = config.get("per_prompt", {})
        max_chars = prompt_cfg.get("max_chars", 300)
        min_length = prompt_cfg.get("min_message_length", 20)
        skip_commands = prompt_cfg.get("skip_commands", True)
        max_results = prompt_cfg.get("max_results", 3)

        # Skip conditions
        if not message or len(message) < min_length:
            return ""
        if skip_commands and message.strip().startswith("/"):
            return ""

        # Extraire keywords du message
        keywords = _extract_keywords(message)
        if not keywords:
            return ""

        # v3: utiliser recherche hybride si embeddings disponibles
        if HAS_HYBRID and embeddings_available():
            hybrid_results = hybrid_search(
                query=message,
                mode="hybrid",
                limit=max_results,
                session_id=session_id,
                log_retrieval_event="UserPromptSubmit",
            )
        else:
            # Fallback: recherche keyword classique
            hybrid_results = []
            raw_memories = search_memories(keywords=keywords, limit=max_results * 2)
            for m in raw_memories:
                score = _effective_score(m, keywords)
                if score > 0.5:
                    hybrid_results.append({**m, "score": score})
            hybrid_results.sort(key=lambda x: x["score"], reverse=True)
            hybrid_results = hybrid_results[:max_results]
            # Log retrieval pour fallback
            for m in hybrid_results:
                if m.get("id"):
                    increment_access(m["id"])
                    if session_id:
                        log_retrieval(m["id"], None, session_id, "UserPromptSubmit", search_mode="keyword_fallback")

        # Chercher facts par prefixe
        matching_facts = []
        for kw in keywords[:3]:
            matching_facts.extend(get_facts(prefix=kw, limit=2))

        if not hybrid_results and not matching_facts:
            return ""

        # Formatter le resultat
        parts = []

        for m in hybrid_results[:max_results]:
            mode_tag = m.get("mode", "kw")
            parts.append(f"[{m.get('type', '?')}|{mode_tag}] {m.get('content', '')[:70]}")

        for f in matching_facts[:2]:
            parts.append(f"[fact] {f['key']}: {f['value'][:50]}")
            if session_id:
                log_retrieval(None, f.get("id"), session_id, "UserPromptSubmit", search_mode="fact_lookup")

        if not parts:
            return ""

        result = " | ".join(parts)
        return result[:max_chars]

    except Exception:
        return ""


# ============================================================
# Keyword extraction
# ============================================================

# Stopwords compacte (subset pour performance)
_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "have", "has",
    "had", "do", "does", "did", "will", "would", "could", "should", "can",
    "to", "of", "in", "for", "on", "with", "at", "by", "from", "as", "and",
    "but", "or", "not", "no", "if", "so", "this", "that", "it", "its",
    "le", "la", "les", "de", "du", "des", "un", "une", "et", "en", "est",
    "que", "qui", "dans", "pour", "pas", "sur", "avec", "ce", "je", "nous",
    "file", "use", "using", "used", "need", "want", "let", "now", "get",
    "make", "just", "also", "how", "what", "where", "when", "which", "all",
    "me", "my", "you", "your", "we", "our", "they", "them", "their",
}


def _extract_keywords(message: str) -> list[str]:
    """Extrait les mots-cles significatifs d'un message."""
    words = re.findall(r"\b[a-zA-Z_][\w.-]{2,}\b", message.lower())
    keywords = [w for w in words if w not in _STOPWORDS]
    # Deduplier en gardant l'ordre
    seen = set()
    unique = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique.append(kw)
    return unique[:10]
