"""Couche SQLite pour le systeme de memoire v2.

Schema: sessions, memories, facts, retrieval_log
Mode WAL pour performance concurrente.
Toutes les operations sont fail-open (retournent des valeurs par defaut en erreur).
Erreurs loguees via log_audit pour observabilite.
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

from .paths import DATA_DIR
from .utils import now_paris, log_audit

DB_PATH = DATA_DIR / "memory.db"

# ============================================================
# Schema
# ============================================================

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    duration_s INTEGER DEFAULT 0,
    complexity INTEGER DEFAULT 0,
    message_count INTEGER DEFAULT 0,
    files_modified INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    working_directory TEXT,
    skills_used TEXT DEFAULT '[]',
    topics TEXT DEFAULT '[]',
    summary_json TEXT DEFAULT '{}',
    trivial INTEGER DEFAULT 0,
    success INTEGER DEFAULT 1,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    tags TEXT DEFAULT '[]',
    importance_score REAL DEFAULT 5.0,
    access_count INTEGER DEFAULT 0,
    last_accessed TEXT,
    created_at TEXT NOT NULL,
    decay_score REAL DEFAULT 1.0,
    source_context TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL,
    confidence REAL DEFAULT 0.5,
    source_sessions TEXT DEFAULT '[]',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS retrieval_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_id INTEGER,
    fact_id INTEGER,
    session_id TEXT NOT NULL,
    hook_event TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    session_success INTEGER
);

CREATE INDEX IF NOT EXISTS idx_memories_session ON memories(session_id);
CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type);
CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance_score);
CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at);
CREATE INDEX IF NOT EXISTS idx_facts_key ON facts(key);
CREATE INDEX IF NOT EXISTS idx_retrieval_session ON retrieval_log(session_id);
CREATE INDEX IF NOT EXISTS idx_retrieval_timestamp ON retrieval_log(timestamp);
"""


def _log_db_error(func_name: str, error: Exception) -> None:
    """Log une erreur DB via log_audit (fail-open)."""
    try:
        log_audit("memory_db", f"error_{func_name}", {
            "error": str(error)[:200],
            "type": type(error).__name__,
        })
    except Exception:
        pass


def _get_connection() -> sqlite3.Connection:
    """Cree ou ouvre la connexion SQLite avec WAL mode."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=5.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=3000")
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema() -> None:
    """Cree les tables si absentes."""
    conn = None
    try:
        conn = _get_connection()
        conn.executescript(_SCHEMA_SQL)
    except Exception as e:
        _log_db_error("ensure_schema", e)
    finally:
        if conn:
            conn.close()


# ============================================================
# Sessions CRUD
# ============================================================

def upsert_session(session_data: dict) -> None:
    """Insert ou update une session (INSERT OR REPLACE)."""
    conn = None
    try:
        conn = _get_connection()
        conn.execute(
            """INSERT OR REPLACE INTO sessions
            (id, timestamp, duration_s, complexity, message_count,
             files_modified, errors_count, working_directory,
             skills_used, topics, summary_json, trivial, success, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session_data.get("id", "unknown"),
                session_data.get("timestamp", now_paris()),
                session_data.get("duration_s", 0),
                session_data.get("complexity", 0),
                session_data.get("message_count", 0),
                session_data.get("files_modified", 0),
                session_data.get("errors_count", 0),
                session_data.get("working_directory", ""),
                json.dumps(session_data.get("skills_used", []), ensure_ascii=False),
                json.dumps(session_data.get("topics", []), ensure_ascii=False),
                json.dumps(session_data.get("summary_json", {}), ensure_ascii=False),
                1 if session_data.get("trivial", False) else 0,
                1 if session_data.get("success", True) else 0,
                session_data.get("created_at", now_paris()),
            ),
        )
        conn.commit()
    except Exception as e:
        _log_db_error("upsert_session", e)
    finally:
        if conn:
            conn.close()


def get_session(session_id: str) -> dict | None:
    """Recupere une session par ID."""
    conn = None
    try:
        conn = _get_connection()
        row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if row:
            return dict(row)
        return None
    except Exception as e:
        _log_db_error("get_session", e)
        return None
    finally:
        if conn:
            conn.close()


# ============================================================
# Memories CRUD
# ============================================================

def insert_memory(memory_data: dict) -> int | None:
    """Insere une memoire. Retourne l'ID ou None."""
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.execute(
            """INSERT INTO memories
            (session_id, type, content, tags, importance_score,
             access_count, last_accessed, created_at, decay_score, source_context)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                memory_data.get("session_id", "unknown"),
                memory_data.get("type", "insight"),
                memory_data.get("content", ""),
                json.dumps(memory_data.get("tags", []), ensure_ascii=False),
                memory_data.get("importance_score", 5.0),
                memory_data.get("access_count", 0),
                memory_data.get("last_accessed"),
                memory_data.get("created_at", now_paris()),
                memory_data.get("decay_score", 1.0),
                memory_data.get("source_context"),
            ),
        )
        memory_id = cursor.lastrowid
        conn.commit()
        return memory_id
    except Exception as e:
        _log_db_error("insert_memory", e)
        return None
    finally:
        if conn:
            conn.close()


def search_memories(
    keywords: list[str] | None = None,
    memory_type: str | None = None,
    min_importance: float = 0.0,
    limit: int = 10,
    days_back: int | None = None,
) -> list[dict]:
    """Recherche des memoires par criteres multiples."""
    conn = None
    try:
        conn = _get_connection()
        conditions = []
        params = []

        if memory_type:
            conditions.append("type = ?")
            params.append(memory_type)

        if min_importance > 0:
            conditions.append("importance_score >= ?")
            params.append(min_importance)

        if days_back is not None:
            cutoff = (datetime.now() - timedelta(days=days_back)).isoformat()
            conditions.append("created_at >= ?")
            params.append(cutoff)

        # Filtrer par keywords en SQL si possible
        if keywords:
            kw_conditions = []
            for kw in keywords:
                kw_conditions.append("(content LIKE ? OR tags LIKE ?)")
                params.append(f"%{kw}%")
                params.append(f"%{kw}%")
            conditions.append("(" + " OR ".join(kw_conditions) + ")")

        where = ""
        if conditions:
            where = "WHERE " + " AND ".join(conditions)

        query = f"""SELECT * FROM memories {where}
                    ORDER BY importance_score * decay_score DESC
                    LIMIT ?"""
        params.append(limit)

        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        _log_db_error("search_memories", e)
        return []
    finally:
        if conn:
            conn.close()


def get_recent_memories(days: int = 7, min_importance: float = 5.0, limit: int = 10) -> list[dict]:
    """Recupere les memoires recentes haute-importance."""
    return search_memories(min_importance=min_importance, limit=limit, days_back=days)


def increment_access(memory_id: int) -> None:
    """Incremente access_count et met a jour last_accessed."""
    conn = None
    try:
        conn = _get_connection()
        conn.execute(
            """UPDATE memories SET access_count = access_count + 1,
               last_accessed = ? WHERE id = ?""",
            (now_paris(), memory_id),
        )
        conn.commit()
    except Exception as e:
        _log_db_error("increment_access", e)
    finally:
        if conn:
            conn.close()


def boost_importance(memory_id: int, delta: float = 0.5) -> None:
    """Booste l'importance d'une memoire (max 10.0)."""
    conn = None
    try:
        conn = _get_connection()
        conn.execute(
            """UPDATE memories SET importance_score = MIN(10.0, importance_score + ?)
               WHERE id = ?""",
            (delta, memory_id),
        )
        conn.commit()
    except Exception as e:
        _log_db_error("boost_importance", e)
    finally:
        if conn:
            conn.close()


# ============================================================
# Facts CRUD
# ============================================================

def upsert_fact(key: str, value: str, confidence: float = 0.5, session_id: str = "") -> None:
    """Insert ou update un fait. Si existe, merge source_sessions et augmente confiance."""
    if not key:
        return
    conn = None
    try:
        conn = _get_connection()
        now = now_paris()
        existing = conn.execute("SELECT * FROM facts WHERE key = ?", (key,)).fetchone()

        if existing:
            sessions = json.loads(existing["source_sessions"] or "[]")
            if session_id and session_id not in sessions:
                sessions.append(session_id)
            new_confidence = min(1.0, existing["confidence"] + 0.1)
            conn.execute(
                """UPDATE facts SET value = ?, confidence = ?,
                   source_sessions = ?, updated_at = ? WHERE key = ?""",
                (value, new_confidence, json.dumps(sessions), now, key),
            )
        else:
            sessions = [session_id] if session_id else []
            conn.execute(
                """INSERT INTO facts (key, value, confidence, source_sessions, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (key, value, confidence, json.dumps(sessions), now, now),
            )

        conn.commit()
    except Exception as e:
        _log_db_error("upsert_fact", e)
    finally:
        if conn:
            conn.close()


def get_facts(min_confidence: float = 0.3, prefix: str | None = None, limit: int = 20) -> list[dict]:
    """Recupere des faits par confiance et/ou prefixe de cle."""
    conn = None
    try:
        conn = _get_connection()
        conditions = ["confidence >= ?"]
        params: list = [min_confidence]

        if prefix:
            conditions.append("key LIKE ?")
            params.append(f"{prefix}%")

        where = "WHERE " + " AND ".join(conditions)
        query = f"SELECT * FROM facts {where} ORDER BY confidence DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        _log_db_error("get_facts", e)
        return []
    finally:
        if conn:
            conn.close()


def get_high_confidence_facts(min_confidence: float = 0.7, limit: int = 10) -> list[dict]:
    """Recupere les faits haute-confiance."""
    return get_facts(min_confidence=min_confidence, limit=limit)


# ============================================================
# Retrieval Log
# ============================================================

def log_retrieval(memory_id: int | None, fact_id: int | None,
                  session_id: str, hook_event: str) -> None:
    """Log un evenement de recuperation pour feedback loop."""
    conn = None
    try:
        conn = _get_connection()
        conn.execute(
            """INSERT INTO retrieval_log (memory_id, fact_id, session_id, hook_event, timestamp)
            VALUES (?, ?, ?, ?, ?)""",
            (memory_id, fact_id, session_id, hook_event, now_paris()),
        )
        conn.commit()
    except Exception as e:
        _log_db_error("log_retrieval", e)
    finally:
        if conn:
            conn.close()


def update_retrieval_success(session_id: str, success: bool) -> None:
    """Met a jour session_success pour toutes les retrievals d'une session."""
    conn = None
    try:
        conn = _get_connection()
        conn.execute(
            "UPDATE retrieval_log SET session_success = ? WHERE session_id = ?",
            (1 if success else 0, session_id),
        )
        conn.commit()
    except Exception as e:
        _log_db_error("update_retrieval_success", e)
    finally:
        if conn:
            conn.close()


def get_retrieved_memory_ids(session_id: str) -> list[int]:
    """Recupere les IDs de memoires servies durant une session."""
    conn = None
    try:
        conn = _get_connection()
        rows = conn.execute(
            "SELECT DISTINCT memory_id FROM retrieval_log WHERE session_id = ? AND memory_id IS NOT NULL",
            (session_id,),
        ).fetchall()
        return [r["memory_id"] for r in rows]
    except Exception as e:
        _log_db_error("get_retrieved_memory_ids", e)
        return []
    finally:
        if conn:
            conn.close()


def purge_old_retrieval_logs(max_age_days: int = 30) -> int:
    """Supprime les entrees de retrieval_log plus vieilles que max_age_days. Retourne le nombre supprime."""
    conn = None
    try:
        conn = _get_connection()
        cutoff = (datetime.now() - timedelta(days=max_age_days)).isoformat()
        cursor = conn.execute(
            "DELETE FROM retrieval_log WHERE timestamp < ?",
            (cutoff,),
        )
        purged = cursor.rowcount
        conn.commit()
        return purged
    except Exception as e:
        _log_db_error("purge_old_retrieval_logs", e)
        return 0
    finally:
        if conn:
            conn.close()


# ============================================================
# Consolidation helpers
# ============================================================

def apply_decay(days_threshold: int = 7, decay_factor: float = 0.9) -> int:
    """Applique decay aux memoires non accedees depuis N jours. Retourne le nombre affecte."""
    conn = None
    try:
        conn = _get_connection()
        cutoff = (datetime.now() - timedelta(days=days_threshold)).isoformat()
        cursor = conn.execute(
            """UPDATE memories SET decay_score = decay_score * ?
               WHERE (last_accessed IS NULL OR last_accessed < ?)
               AND decay_score > 0.01""",
            (decay_factor, cutoff),
        )
        affected = cursor.rowcount
        conn.commit()
        return affected
    except Exception as e:
        _log_db_error("apply_decay", e)
        return 0
    finally:
        if conn:
            conn.close()


def prune_low_score(min_effective_score: float = 0.5, min_age_days: int = 30) -> int:
    """Supprime les memoires avec score effectif bas et agees. Retourne le nombre supprime."""
    conn = None
    try:
        conn = _get_connection()
        cutoff = (datetime.now() - timedelta(days=min_age_days)).isoformat()
        cursor = conn.execute(
            """DELETE FROM memories
               WHERE importance_score * decay_score < ?
               AND created_at < ?""",
            (min_effective_score, cutoff),
        )
        pruned = cursor.rowcount
        conn.commit()
        return pruned
    except Exception as e:
        _log_db_error("prune_low_score", e)
        return 0
    finally:
        if conn:
            conn.close()


def promote_frequently_accessed(min_access: int = 3, boost: float = 1.0) -> int:
    """Booste les memoires frequemment accedees. Retourne le nombre promu."""
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.execute(
            """UPDATE memories SET importance_score = MIN(10.0, importance_score + ?)
               WHERE access_count >= ? AND importance_score < 9.0""",
            (boost, min_access),
        )
        promoted = cursor.rowcount
        conn.commit()
        return promoted
    except Exception as e:
        _log_db_error("promote_frequently_accessed", e)
        return 0
    finally:
        if conn:
            conn.close()


def get_all_memories_for_merge(min_importance: float = 3.0) -> list[dict]:
    """Recupere toutes les memoires actives pour analyse de merge."""
    conn = None
    try:
        conn = _get_connection()
        rows = conn.execute(
            """SELECT * FROM memories
               WHERE importance_score * decay_score >= ?
               ORDER BY type, created_at""",
            (min_importance,),
        ).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        _log_db_error("get_all_memories_for_merge", e)
        return []
    finally:
        if conn:
            conn.close()


def merge_memories(keep_id: int, remove_id: int) -> None:
    """Fusionne deux memoires: garde keep_id, supprime remove_id."""
    conn = None
    try:
        conn = _get_connection()
        removed = conn.execute("SELECT * FROM memories WHERE id = ?", (remove_id,)).fetchone()
        if removed:
            conn.execute(
                "UPDATE memories SET access_count = access_count + ? WHERE id = ?",
                (removed["access_count"], keep_id),
            )
            conn.execute("DELETE FROM memories WHERE id = ?", (remove_id,))
        conn.commit()
    except Exception as e:
        _log_db_error("merge_memories", e)
    finally:
        if conn:
            conn.close()


def get_stats() -> dict:
    """Retourne des statistiques sur la base memoire."""
    conn = None
    try:
        conn = _get_connection()
        stats = {}
        stats["sessions_count"] = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        stats["memories_count"] = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        stats["facts_count"] = conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
        stats["retrievals_count"] = conn.execute("SELECT COUNT(*) FROM retrieval_log").fetchone()[0]

        rows = conn.execute("SELECT type, COUNT(*) as cnt FROM memories GROUP BY type").fetchall()
        stats["memories_by_type"] = {r["type"]: r["cnt"] for r in rows}

        row = conn.execute("SELECT AVG(importance_score * decay_score) as avg_score FROM memories").fetchone()
        stats["avg_effective_score"] = round(row["avg_score"] or 0, 2)

        return stats
    except Exception as e:
        _log_db_error("get_stats", e)
        return {}
    finally:
        if conn:
            conn.close()


# Auto-init schema on import
ensure_schema()
