"""Tests pour lib/memory_db.py — couche SQLite Memory v2.

Teste le schema, les CRUD sessions/memories/facts,
le retrieval log, et les helpers de consolidation.
"""

import json
import sqlite3
from pathlib import Path

import pytest


# ============================================================
# Fixture: DB isolee en tmp_path
# ============================================================

@pytest.fixture(autouse=True)
def isolated_db(monkeypatch, tmp_path):
    """Redirige DB_PATH vers un fichier temporaire pour chaque test."""
    db_file = tmp_path / "test_memory.db"
    from lib import memory_db
    monkeypatch.setattr(memory_db, "DB_PATH", db_file)
    # Re-initialiser le schema dans la nouvelle DB
    memory_db.ensure_schema()
    return db_file


# ============================================================
# Schema
# ============================================================

class TestSchema:
    def test_tables_created(self, isolated_db):
        conn = sqlite3.connect(str(isolated_db))
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()]
        conn.close()
        assert "sessions" in tables
        assert "memories" in tables
        assert "facts" in tables
        assert "retrieval_log" in tables

    def test_indexes_created(self, isolated_db):
        conn = sqlite3.connect(str(isolated_db))
        indexes = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index'"
        ).fetchall()]
        conn.close()
        assert "idx_memories_session" in indexes
        assert "idx_memories_type" in indexes
        assert "idx_memories_importance" in indexes
        assert "idx_facts_key" in indexes

    def test_wal_mode(self, isolated_db):
        from lib.memory_db import _get_connection
        conn = _get_connection()
        mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
        conn.close()
        assert mode == "wal"

    def test_ensure_schema_idempotent(self):
        """Appeler ensure_schema() deux fois ne crash pas."""
        from lib.memory_db import ensure_schema
        ensure_schema()
        ensure_schema()


# ============================================================
# Sessions CRUD
# ============================================================

class TestSessionsCRUD:
    def test_upsert_and_get(self):
        from lib.memory_db import upsert_session, get_session
        upsert_session({
            "id": "sess-001",
            "duration_s": 120,
            "complexity": 3,
            "message_count": 10,
            "files_modified": 2,
            "errors_count": 1,
            "working_directory": "/tmp/test",
            "skills_used": ["docker-skill"],
            "topics": ["docker", "compose"],
        })
        s = get_session("sess-001")
        assert s is not None
        assert s["id"] == "sess-001"
        assert s["duration_s"] == 120
        assert s["complexity"] == 3
        assert s["message_count"] == 10
        assert s["files_modified"] == 2
        assert s["errors_count"] == 1
        assert json.loads(s["skills_used"]) == ["docker-skill"]
        assert json.loads(s["topics"]) == ["docker", "compose"]

    def test_get_nonexistent_returns_none(self):
        from lib.memory_db import get_session
        assert get_session("nonexistent") is None

    def test_upsert_replaces(self):
        from lib.memory_db import upsert_session, get_session
        upsert_session({"id": "sess-002", "duration_s": 60})
        upsert_session({"id": "sess-002", "duration_s": 180})
        s = get_session("sess-002")
        assert s["duration_s"] == 180

    def test_default_values(self):
        from lib.memory_db import upsert_session, get_session
        upsert_session({"id": "sess-003"})
        s = get_session("sess-003")
        assert s["complexity"] == 0
        assert s["trivial"] == 0
        assert s["success"] == 1

    def test_trivial_session(self):
        from lib.memory_db import upsert_session, get_session
        upsert_session({"id": "sess-004", "trivial": True})
        s = get_session("sess-004")
        assert s["trivial"] == 1


# ============================================================
# Memories CRUD
# ============================================================

class TestMemoriesCRUD:
    def _seed_session(self):
        from lib.memory_db import upsert_session
        upsert_session({"id": "sess-mem"})

    def test_insert_returns_id(self):
        self._seed_session()
        from lib.memory_db import insert_memory
        mem_id = insert_memory({
            "session_id": "sess-mem",
            "type": "problem_solution",
            "content": "Fixed the import error by adding missing __init__.py",
            "importance_score": 7.0,
        })
        assert mem_id is not None
        assert isinstance(mem_id, int)
        assert mem_id > 0

    def test_search_by_type(self):
        self._seed_session()
        from lib.memory_db import insert_memory, search_memories
        insert_memory({"session_id": "sess-mem", "type": "decision", "content": "Use SQLite"})
        insert_memory({"session_id": "sess-mem", "type": "insight", "content": "Fast enough"})

        results = search_memories(memory_type="decision")
        assert len(results) == 1
        assert results[0]["type"] == "decision"

    def test_search_by_importance(self):
        self._seed_session()
        from lib.memory_db import insert_memory, search_memories
        insert_memory({"session_id": "sess-mem", "type": "insight", "content": "Low score", "importance_score": 2.0})
        insert_memory({"session_id": "sess-mem", "type": "insight", "content": "High score", "importance_score": 8.0})

        results = search_memories(min_importance=7.0)
        assert len(results) == 1
        assert "High score" in results[0]["content"]

    def test_search_by_keywords(self):
        self._seed_session()
        from lib.memory_db import insert_memory, search_memories
        insert_memory({"session_id": "sess-mem", "type": "insight", "content": "Docker compose networking issue"})
        insert_memory({"session_id": "sess-mem", "type": "insight", "content": "Python import path problem"})

        results = search_memories(keywords=["docker"])
        assert len(results) == 1
        assert "Docker" in results[0]["content"]

    def test_search_empty_returns_all(self):
        self._seed_session()
        from lib.memory_db import insert_memory, search_memories
        insert_memory({"session_id": "sess-mem", "type": "insight", "content": "A"})
        insert_memory({"session_id": "sess-mem", "type": "insight", "content": "B"})

        results = search_memories()
        assert len(results) == 2

    def test_get_recent_memories(self):
        self._seed_session()
        from lib.memory_db import insert_memory, get_recent_memories
        insert_memory({"session_id": "sess-mem", "type": "insight", "content": "Recent high", "importance_score": 8.0})
        insert_memory({"session_id": "sess-mem", "type": "insight", "content": "Recent low", "importance_score": 2.0})

        results = get_recent_memories(days=1, min_importance=7.0)
        assert len(results) == 1

    def test_increment_access(self):
        self._seed_session()
        from lib.memory_db import insert_memory, search_memories, increment_access
        mem_id = insert_memory({"session_id": "sess-mem", "type": "insight", "content": "Test"})
        increment_access(mem_id)
        increment_access(mem_id)

        results = search_memories()
        found = [m for m in results if m["id"] == mem_id]
        assert found[0]["access_count"] == 2
        assert found[0]["last_accessed"] is not None

    def test_boost_importance(self):
        self._seed_session()
        from lib.memory_db import insert_memory, search_memories, boost_importance
        mem_id = insert_memory({"session_id": "sess-mem", "type": "insight", "content": "Boost me", "importance_score": 5.0})
        boost_importance(mem_id, 2.0)

        results = search_memories()
        found = [m for m in results if m["id"] == mem_id]
        assert found[0]["importance_score"] == 7.0

    def test_boost_importance_capped_at_10(self):
        self._seed_session()
        from lib.memory_db import insert_memory, search_memories, boost_importance
        mem_id = insert_memory({"session_id": "sess-mem", "type": "insight", "content": "Max", "importance_score": 9.5})
        boost_importance(mem_id, 5.0)

        results = search_memories()
        found = [m for m in results if m["id"] == mem_id]
        assert found[0]["importance_score"] == 10.0


# ============================================================
# Facts CRUD
# ============================================================

class TestFactsCRUD:
    def test_upsert_new_fact(self):
        from lib.memory_db import upsert_fact, get_facts
        upsert_fact("python_version", "3.12", confidence=0.8, session_id="s1")

        facts = get_facts(min_confidence=0.5)
        assert len(facts) == 1
        assert facts[0]["key"] == "python_version"
        assert facts[0]["value"] == "3.12"
        assert facts[0]["confidence"] == 0.8

    def test_upsert_existing_increases_confidence(self):
        from lib.memory_db import upsert_fact, get_facts
        upsert_fact("os", "windows", confidence=0.5, session_id="s1")
        upsert_fact("os", "windows", confidence=0.5, session_id="s2")

        facts = get_facts(prefix="os")
        assert len(facts) == 1
        assert facts[0]["confidence"] == 0.6  # 0.5 + 0.1

    def test_upsert_merges_sessions(self):
        from lib.memory_db import upsert_fact, get_facts
        upsert_fact("editor", "vscode", session_id="s1")
        upsert_fact("editor", "vscode", session_id="s2")

        facts = get_facts(prefix="editor")
        sessions = json.loads(facts[0]["source_sessions"])
        assert "s1" in sessions
        assert "s2" in sessions

    def test_get_facts_by_prefix(self):
        from lib.memory_db import upsert_fact, get_facts
        upsert_fact("tool.docker", "installed")
        upsert_fact("tool.python", "3.12")
        upsert_fact("config.theme", "dark")

        facts = get_facts(prefix="tool.")
        assert len(facts) == 2
        keys = [f["key"] for f in facts]
        assert "tool.docker" in keys
        assert "tool.python" in keys

    def test_get_high_confidence_facts(self):
        from lib.memory_db import upsert_fact, get_high_confidence_facts
        upsert_fact("high", "yes", confidence=0.9)
        upsert_fact("low", "no", confidence=0.3)

        facts = get_high_confidence_facts(min_confidence=0.7)
        assert len(facts) == 1
        assert facts[0]["key"] == "high"

    def test_confidence_capped_at_1(self):
        from lib.memory_db import upsert_fact, get_facts
        upsert_fact("cap", "test", confidence=0.95)
        upsert_fact("cap", "test", confidence=0.95)  # +0.1 -> min(1.0, 1.05)

        facts = get_facts(prefix="cap")
        assert facts[0]["confidence"] == 1.0


# ============================================================
# Retrieval Log
# ============================================================

class TestRetrievalLog:
    def test_log_retrieval(self):
        from lib.memory_db import log_retrieval, _get_connection
        log_retrieval(memory_id=1, fact_id=None, session_id="sess-r1", hook_event="SessionStart")

        conn = _get_connection()
        rows = conn.execute("SELECT * FROM retrieval_log WHERE session_id = 'sess-r1'").fetchall()
        conn.close()
        assert len(rows) == 1
        assert rows[0]["hook_event"] == "SessionStart"
        assert rows[0]["memory_id"] == 1

    def test_update_retrieval_success(self):
        from lib.memory_db import log_retrieval, update_retrieval_success, _get_connection
        log_retrieval(1, None, "sess-r2", "SessionStart")
        log_retrieval(2, None, "sess-r2", "UserPromptSubmit")
        update_retrieval_success("sess-r2", True)

        conn = _get_connection()
        rows = conn.execute("SELECT session_success FROM retrieval_log WHERE session_id = 'sess-r2'").fetchall()
        conn.close()
        assert all(r[0] == 1 for r in rows)

    def test_get_retrieved_memory_ids(self):
        from lib.memory_db import log_retrieval, get_retrieved_memory_ids
        log_retrieval(10, None, "sess-r3", "SessionStart")
        log_retrieval(20, None, "sess-r3", "UserPromptSubmit")
        log_retrieval(10, None, "sess-r3", "UserPromptSubmit")  # duplicate

        ids = get_retrieved_memory_ids("sess-r3")
        assert sorted(ids) == [10, 20]


# ============================================================
# Consolidation helpers
# ============================================================

class TestConsolidation:
    def _seed(self):
        from lib.memory_db import upsert_session, insert_memory
        upsert_session({"id": "sess-cons"})
        return insert_memory

    def test_apply_decay(self):
        insert_memory = self._seed()
        from lib.memory_db import apply_decay, search_memories
        insert_memory({
            "session_id": "sess-cons", "type": "insight",
            "content": "Old memory", "decay_score": 1.0,
        })
        affected = apply_decay(days_threshold=0, decay_factor=0.5)
        assert affected >= 1

        results = search_memories()
        assert results[0]["decay_score"] == pytest.approx(0.5)

    def test_prune_low_score(self):
        insert_memory = self._seed()
        from lib.memory_db import prune_low_score, search_memories
        insert_memory({
            "session_id": "sess-cons", "type": "insight",
            "content": "Will survive", "importance_score": 8.0, "decay_score": 1.0,
        })
        insert_memory({
            "session_id": "sess-cons", "type": "insight",
            "content": "Will be pruned", "importance_score": 0.1, "decay_score": 0.1,
        })
        pruned = prune_low_score(min_effective_score=0.5, min_age_days=0)
        assert pruned >= 1

        results = search_memories()
        contents = [m["content"] for m in results]
        assert "Will survive" in contents
        assert "Will be pruned" not in contents

    def test_promote_frequently_accessed(self):
        insert_memory = self._seed()
        from lib.memory_db import promote_frequently_accessed, search_memories, increment_access
        mem_id = insert_memory({
            "session_id": "sess-cons", "type": "insight",
            "content": "Popular", "importance_score": 5.0,
        })
        for _ in range(5):
            increment_access(mem_id)

        promoted = promote_frequently_accessed(min_access=3, boost=1.5)
        assert promoted >= 1

        results = search_memories()
        found = [m for m in results if m["id"] == mem_id]
        assert found[0]["importance_score"] == 6.5

    def test_merge_memories(self):
        insert_memory = self._seed()
        from lib.memory_db import merge_memories, search_memories, increment_access
        id1 = insert_memory({"session_id": "sess-cons", "type": "insight", "content": "Keep"})
        id2 = insert_memory({"session_id": "sess-cons", "type": "insight", "content": "Remove"})
        increment_access(id2)
        increment_access(id2)

        merge_memories(keep_id=id1, remove_id=id2)

        results = search_memories()
        ids = [m["id"] for m in results]
        assert id1 in ids
        assert id2 not in ids
        # access_count transferred
        kept = [m for m in results if m["id"] == id1]
        assert kept[0]["access_count"] == 2

    def test_get_all_memories_for_merge(self):
        insert_memory = self._seed()
        from lib.memory_db import get_all_memories_for_merge
        insert_memory({"session_id": "sess-cons", "type": "insight", "content": "A", "importance_score": 5.0})
        insert_memory({"session_id": "sess-cons", "type": "insight", "content": "B", "importance_score": 1.0})

        results = get_all_memories_for_merge(min_importance=3.0)
        contents = [m["content"] for m in results]
        assert "A" in contents
        assert "B" not in contents


# ============================================================
# Stats
# ============================================================

class TestStats:
    def test_get_stats(self):
        from lib.memory_db import upsert_session, insert_memory, upsert_fact, log_retrieval, get_stats
        upsert_session({"id": "sess-stats"})
        insert_memory({"session_id": "sess-stats", "type": "insight", "content": "Test"})
        insert_memory({"session_id": "sess-stats", "type": "decision", "content": "Choice"})
        upsert_fact("key1", "val1")
        log_retrieval(1, None, "sess-stats", "SessionStart")

        stats = get_stats()
        assert stats["sessions_count"] == 1
        assert stats["memories_count"] == 2
        assert stats["facts_count"] == 1
        assert stats["retrievals_count"] == 1
        assert stats["memories_by_type"]["insight"] == 1
        assert stats["memories_by_type"]["decision"] == 1
        assert stats["avg_effective_score"] > 0
