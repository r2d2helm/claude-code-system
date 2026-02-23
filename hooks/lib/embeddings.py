"""Wrapper FastEmbed pour embeddings locaux.

Modele: all-MiniLM-L6-v2 (384 dimensions, ~80MB).
Lazy loading: le modele n'est charge qu'au premier appel.
Fail-open: retourne None si FastEmbed n'est pas installe.

Inspire du Second Brain (Dynamous Community).
"""

import struct
from pathlib import Path
from typing import Optional

from .paths import DATA_DIR

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
MODELS_DIR = DATA_DIR / "models"

_model = None
_available: Optional[bool] = None


def is_available() -> bool:
    """Verifie si FastEmbed est installe."""
    global _available
    if _available is None:
        try:
            from fastembed import TextEmbedding  # noqa: F401
            _available = True
        except ImportError:
            _available = False
    return _available


def _get_model():
    """Charge le modele FastEmbed (lazy loading)."""
    global _model
    if _model is None:
        if not is_available():
            return None
        from fastembed import TextEmbedding
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        _model = TextEmbedding(
            model_name=MODEL_NAME,
            cache_dir=str(MODELS_DIR),
        )
    return _model


def embed_text(text: str) -> Optional[list[float]]:
    """Genere un embedding pour un texte. Retourne None si indisponible."""
    try:
        model = _get_model()
        if model is None:
            return None
        embeddings = list(model.embed([text]))
        if embeddings:
            return embeddings[0].tolist()
        return None
    except Exception:
        return None


def embed_batch(texts: list[str]) -> list[Optional[list[float]]]:
    """Genere des embeddings pour une liste de textes."""
    try:
        model = _get_model()
        if model is None:
            return [None] * len(texts)
        results = list(model.embed(texts))
        return [r.tolist() for r in results]
    except Exception:
        return [None] * len(texts)


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Calcule la similarite cosinus entre deux vecteurs."""
    if len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def embedding_to_blob(embedding: list[float]) -> bytes:
    """Serialise un embedding en bytes pour stockage SQLite."""
    return struct.pack(f"{len(embedding)}f", *embedding)


def blob_to_embedding(blob: bytes) -> list[float]:
    """Deserialise un blob SQLite en liste de floats."""
    count = len(blob) // 4
    return list(struct.unpack(f"{count}f", blob))
