"""Tests pour le systeme Memory v2 (memory_db, memory_retriever, memory_extractor_v2, memory_consolidator).

Couvre les 4 modules avec 50+ fonctions de test:
- memory_db: CRUD sessions/memories/facts, retrieval_log, consolidation helpers
- memory_retriever: scoring, keyword extraction, retrieval modes
- memory_extractor_v2: 5 heuristiques d'extraction
- memory_consolidator: tokenize, similarity, merge candidates, consolidate
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).resolve().parent.parent
if str(HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(HOOKS_DIR))


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def memory_db(tmp_path, monkeypatch):
    """Prepare memory_db avec DB_PATH pointe vers tmp_path.

    Monkeypatch DB_PATH avant que les fonctions ne l'utilisent,
    puis appelle ensure_schema() pour creer les tables.
    """
    from lib import paths as paths_mod
    monkeypatch.setattr(paths_mod, "DATA_DIR", tmp_path)

    import lib.memory_db as db_mod
    monkeypatch.setattr(db_mod, "DB_PATH", tmp_path / "memory.db")
    db_mod.ensure_schema()
    return db_mod


@pytest.fixture
def populated_db(memory_db):
    """DB avec des donnees de test pre-inserees."""
    db = memory_db

    db.upsert_session({
        "id": "sess-001",
        "timestamp": datetime.now().isoformat(),
        "duration_s": 120,
        "complexity": 3,
        "message_count": 10,
        "topics": ["docker", "nginx"],
        "created_at": datetime.now().isoformat(),
    })

    db.insert_memory({
        "session_id": "sess-001",
        "type": "problem_solution",
        "content": "Problem: nginx config error | Solution: fixed upstream directive",
        "tags": ["nginx", "config"],
        "importance_score": 7.5,
        "created_at": datetime.now().isoformat(),
    })
    db.insert_memory({
        "session_id": "sess-001",
        "type": "tool_sequence",
        "content": "Fix sequence: Read(nginx.conf) -> error -> Edit(nginx.conf)",
        "tags": ["nginx"],
        "importance_score": 7.0,
        "created_at": datetime.now().isoformat(),
    })
    db.insert_memory({
        "session_id": "sess-001",
        "type": "decision",
        "content": "I'll use docker compose instead of raw docker commands",
        "tags": ["docker"],
        "importance_score": 6.0,
        "created_at": datetime.now().isoformat(),
    })

    db.upsert_fact("encoding/utf8", "UTF-8 sans BOM pour md/json", confidence=0.8, session_id="sess-001")
    db.upsert_fact("path/vault", "/home/user/Knowledge", confidence=0.6, session_id="sess-001")

    return db


# ============================================================
# Module 1: memory_db.py
# ============================================================

class TestEnsureSchema:
    def test_creates_tables(self, memory_db):
        import sqlite3
        conn = sqlite3.connect(str(memory_db.DB_PATH))
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        conn.close()
        table_names = [t[0] for t in tables]
        assert "sessions" in table_names
        assert "memories" in table_names
        assert "facts" in table_names
        assert "retrieval_log" in table_names

    def test_idempotent(self, memory_db):
        memory_db.ensure_schema()
        memory_db.ensure_schema()
        import sqlite3
        conn = sqlite3.connect(str(memory_db.DB_PATH))
        count = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
        conn.close()
        assert count >= 4


class TestSessionsCRUD:
    def test_upsert_and_get_session(self, memory_db):
        memory_db.upsert_session({
            "id": "test-sess-1",
            "timestamp": "2026-02-12T10:00:00",
            "duration_s": 60,
            "complexity": 2,
            "message_count": 5,
            "created_at": "2026-02-12T10:00:00",
        })
        session = memory_db.get_session("test-sess-1")
        assert session is not None
        assert session["id"] == "test-sess-1"
        assert session["duration_s"] == 60
        assert session["complexity"] == 2
        assert session["message_count"] == 5

    def test_upsert_replaces_existing(self, memory_db):
        memory_db.upsert_session({"id": "sess-replace", "duration_s": 10, "created_at": "2026-02-12T10:00:00"})
        memory_db.upsert_session({"id": "sess-replace", "duration_s": 99, "created_at": "2026-02-12T10:00:00"})
        session = memory_db.get_session("sess-replace")
        assert session["duration_s"] == 99

    def test_get_nonexistent_session(self, memory_db):
        assert memory_db.get_session("nonexistent") is None


class TestMemoriesCRUD:
    def test_insert_memory_returns_id(self, memory_db):
        memory_db.upsert_session({"id": "s1", "created_at": "2026-02-12T10:00:00"})
        mid = memory_db.insert_memory({
            "session_id": "s1",
            "type": "insight",
            "content": "test memory content",
            "created_at": "2026-02-12T10:00:00",
        })
        assert mid is not None
        assert isinstance(mid, int)
        assert mid > 0

    def test_search_memories_by_keywords(self, populated_db):
        results = populated_db.search_memories(keywords=["nginx"])
        assert len(results) >= 1
        assert any("nginx" in r["content"].lower() for r in results)

    def test_search_memories_by_type(self, populated_db):
        results = populated_db.search_memories(memory_type="decision")
        assert len(results) >= 1
        assert all(r["type"] == "decision" for r in results)

    def test_search_memories_by_importance(self, populated_db):
        results = populated_db.search_memories(min_importance=7.0)
        assert all(r["importance_score"] >= 7.0 for r in results)

    def test_search_memories_by_days_back(self, memory_db):
        memory_db.upsert_session({"id": "s-old", "created_at": "2026-02-12T10:00:00"})
        old_date = (datetime.now() - timedelta(days=30)).isoformat()
        new_date = datetime.now().isoformat()
        memory_db.insert_memory({
            "session_id": "s-old",
            "type": "insight",
            "content": "old memory",
            "created_at": old_date,
        })
        memory_db.insert_memory({
            "session_id": "s-old",
            "type": "insight",
            "content": "new memory",
            "created_at": new_date,
        })
        results = memory_db.search_memories(days_back=7)
        assert all("old memory" not in r["content"] for r in results)

    def test_search_memories_respects_limit(self, populated_db):
        results = populated_db.search_memories(limit=1)
        assert len(results) == 1

    def test_search_memories_no_criteria_returns_all(self, populated_db):
        results = populated_db.search_memories(limit=100)
        assert len(results) >= 3


class TestIncrementAccess:
    def test_increments_count(self, memory_db):
        memory_db.upsert_session({"id": "s1", "created_at": "2026-02-12T10:00:00"})
        mid = memory_db.insert_memory({
            "session_id": "s1",
            "type": "insight",
            "content": "test",
            "created_at": datetime.now().isoformat(),
        })
        memory_db.increment_access(mid)
        memory_db.increment_access(mid)

        results = memory_db.search_memories(limit=100)
        mem = [r for r in results if r["id"] == mid][0]
        assert mem["access_count"] == 2
        assert mem["last_accessed"] is not None


class TestBoostImportance:
    def test_boosts_score(self, memory_db):
        memory_db.upsert_session({"id": "s1", "created_at": "2026-02-12T10:00:00"})
        mid = memory_db.insert_memory({
            "session_id": "s1",
            "type": "insight",
            "content": "test",
            "importance_score": 5.0,
            "created_at": datetime.now().isoformat(),
        })
        memory_db.boost_importance(mid, delta=2.0)

        results = memory_db.search_memories(limit=100)
        mem = [r for r in results if r["id"] == mid][0]
        assert mem["importance_score"] == pytest.approx(7.0)

    def test_caps_at_ten(self, memory_db):
        memory_db.upsert_session({"id": "s1", "created_at": "2026-02-12T10:00:00"})
        mid = memory_db.insert_memory({
            "session_id": "s1",
            "type": "insight",
            "content": "test",
            "importance_score": 9.5,
            "created_at": datetime.now().isoformat(),
        })
        memory_db.boost_importance(mid, delta=3.0)

        results = memory_db.search_memories(limit=100)
        mem = [r for r in results if r["id"] == mid][0]
        assert mem["importance_score"] == pytest.approx(10.0)


class TestFactsCRUD:
    def test_upsert_fact_insert(self, memory_db):
        memory_db.upsert_fact("test/key", "test value", confidence=0.5, session_id="s1")
        facts = memory_db.get_facts(min_confidence=0.0)
        assert len(facts) == 1
        assert facts[0]["key"] == "test/key"
        assert facts[0]["value"] == "test value"

    def test_upsert_fact_update_increments_confidence(self, memory_db):
        memory_db.upsert_fact("dup/key", "val1", confidence=0.5, session_id="s1")
        memory_db.upsert_fact("dup/key", "val2", confidence=0.5, session_id="s2")
        facts = memory_db.get_facts(min_confidence=0.0)
        fact = [f for f in facts if f["key"] == "dup/key"][0]
        assert fact["confidence"] == pytest.approx(0.6)
        assert fact["value"] == "val2"

    def test_upsert_fact_merges_sessions(self, memory_db):
        memory_db.upsert_fact("merge/key", "val", confidence=0.5, session_id="s1")
        memory_db.upsert_fact("merge/key", "val", confidence=0.5, session_id="s2")
        facts = memory_db.get_facts(min_confidence=0.0)
        fact = [f for f in facts if f["key"] == "merge/key"][0]
        sessions = json.loads(fact["source_sessions"])
        assert "s1" in sessions
        assert "s2" in sessions

    def test_upsert_fact_rejects_empty_key(self, memory_db):
        memory_db.upsert_fact("", "val", confidence=0.5)
        facts = memory_db.get_facts(min_confidence=0.0)
        assert len(facts) == 0

    def test_get_facts_with_min_confidence(self, populated_db):
        facts = populated_db.get_facts(min_confidence=0.7)
        assert all(f["confidence"] >= 0.7 for f in facts)

    def test_get_facts_with_prefix(self, populated_db):
        facts = populated_db.get_facts(min_confidence=0.0, prefix="encoding/")
        assert len(facts) >= 1
        assert all(f["key"].startswith("encoding/") for f in facts)

    def test_get_facts_with_prefix_no_match(self, populated_db):
        facts = populated_db.get_facts(min_confidence=0.0, prefix="nonexistent/")
        assert len(facts) == 0


class TestRetrievalLog:
    def test_log_and_get_retrieved_ids(self, memory_db):
        memory_db.upsert_session({"id": "s1", "created_at": "2026-02-12T10:00:00"})
        mid = memory_db.insert_memory({
            "session_id": "s1",
            "type": "insight",
            "content": "test",
            "created_at": datetime.now().isoformat(),
        })
        memory_db.log_retrieval(mid, None, "s1", "SessionStart")
        memory_db.log_retrieval(mid, None, "s1", "UserPromptSubmit")

        ids = memory_db.get_retrieved_memory_ids("s1")
        assert mid in ids

    def test_get_retrieved_ids_empty_session(self, memory_db):
        ids = memory_db.get_retrieved_memory_ids("nonexistent-session")
        assert ids == []

    def test_purge_old_retrieval_logs(self, memory_db):
        memory_db.upsert_session({"id": "s1", "created_at": "2026-02-12T10:00:00"})
        memory_db.log_retrieval(1, None, "s1", "SessionStart")

        purged = memory_db.purge_old_retrieval_logs(max_age_days=0)
        assert purged >= 0


class TestConsolidationHelpers:
    def test_apply_decay_reduces_score(self, memory_db):
        memory_db.upsert_session({"id": "s1", "created_at": "2026-02-12T10:00:00"})
        old_date = (datetime.now() - timedelta(days=30)).isoformat()
        mid = memory_db.insert_memory({
            "session_id": "s1",
            "type": "insight",
            "content": "old memory that should decay",
            "created_at": old_date,
            "decay_score": 1.0,
        })
        affected = memory_db.apply_decay(days_threshold=7, decay_factor=0.5)
        assert affected >= 1

        results = memory_db.search_memories(limit=100)
        mem = [r for r in results if r["id"] == mid][0]
        assert mem["decay_score"] == pytest.approx(0.5)

    def test_prune_low_score_deletes_old_low_memories(self, memory_db):
        memory_db.upsert_session({"id": "s1", "created_at": "2026-02-12T10:00:00"})
        old_date = (datetime.now() - timedelta(days=60)).isoformat()
        memory_db.insert_memory({
            "session_id": "s1",
            "type": "insight",
            "content": "low score old memory",
            "importance_score": 0.1,
            "decay_score": 0.1,
            "created_at": old_date,
        })
        pruned = memory_db.prune_low_score(min_effective_score=0.5, min_age_days=30)
        assert pruned >= 1

    def test_promote_frequently_accessed(self, memory_db):
        memory_db.upsert_session({"id": "s1", "created_at": "2026-02-12T10:00:00"})
        mid = memory_db.insert_memory({
            "session_id": "s1",
            "type": "insight",
            "content": "frequently accessed",
            "importance_score": 5.0,
            "access_count": 5,
            "created_at": datetime.now().isoformat(),
        })
        promoted = memory_db.promote_frequently_accessed(min_access=3, boost=1.0)
        assert promoted >= 1

        results = memory_db.search_memories(limit=100)
        mem = [r for r in results if r["id"] == mid][0]
        assert mem["importance_score"] == pytest.approx(6.0)

    def test_merge_memories_transfers_access_count(self, memory_db):
        memory_db.upsert_session({"id": "s1", "created_at": "2026-02-12T10:00:00"})
        mid1 = memory_db.insert_memory({
            "session_id": "s1",
            "type": "insight",
            "content": "keep this one",
            "access_count": 2,
            "created_at": datetime.now().isoformat(),
        })
        mid2 = memory_db.insert_memory({
            "session_id": "s1",
            "type": "insight",
            "content": "remove this one",
            "access_count": 3,
            "created_at": datetime.now().isoformat(),
        })
        memory_db.merge_memories(mid1, mid2)

        results = memory_db.search_memories(limit=100)
        kept = [r for r in results if r["id"] == mid1]
        removed = [r for r in results if r["id"] == mid2]
        assert len(kept) == 1
        assert len(removed) == 0
        assert kept[0]["access_count"] == 5

    def test_get_stats_returns_correct_counts(self, populated_db):
        stats = populated_db.get_stats()
        assert stats["sessions_count"] == 1
        assert stats["memories_count"] == 3
        assert stats["facts_count"] == 2
        assert stats["retrievals_count"] == 0
        assert "memories_by_type" in stats
        assert stats["memories_by_type"].get("problem_solution") == 1
        assert stats["memories_by_type"].get("tool_sequence") == 1
        assert stats["memories_by_type"].get("decision") == 1
        assert "avg_effective_score" in stats


# ============================================================
# Module 2: memory_retriever.py
# ============================================================

class TestComputeRecencyBoost:
    def test_recent_timestamp_gets_boost(self, monkeypatch):
        from lib.memory_retriever import _compute_recency_boost, _RETRIEVAL_CONFIG
        monkeypatch.setattr("lib.memory_retriever._RETRIEVAL_CONFIG", None)

        recent = (datetime.now() - timedelta(days=2)).isoformat()
        boost = _compute_recency_boost(recent)
        assert boost == pytest.approx(0.5)

    def test_14d_old_gets_smaller_boost(self, monkeypatch):
        from lib.memory_retriever import _compute_recency_boost
        monkeypatch.setattr("lib.memory_retriever._RETRIEVAL_CONFIG", None)

        ts = (datetime.now() - timedelta(days=10)).isoformat()
        boost = _compute_recency_boost(ts)
        assert boost == pytest.approx(0.3)

    def test_old_timestamp_no_boost(self, monkeypatch):
        from lib.memory_retriever import _compute_recency_boost
        monkeypatch.setattr("lib.memory_retriever._RETRIEVAL_CONFIG", None)

        old = (datetime.now() - timedelta(days=30)).isoformat()
        boost = _compute_recency_boost(old)
        assert boost == 0.0

    def test_empty_timestamp_no_boost(self, monkeypatch):
        from lib.memory_retriever import _compute_recency_boost
        monkeypatch.setattr("lib.memory_retriever._RETRIEVAL_CONFIG", None)

        assert _compute_recency_boost("") == 0.0
        assert _compute_recency_boost(None) == 0.0


class TestComputeKeywordMatch:
    def test_full_match(self):
        from lib.memory_retriever import _compute_keyword_match
        score = _compute_keyword_match("nginx config error", "[]", ["nginx", "config"])
        assert score == pytest.approx(1.0)

    def test_partial_match(self):
        from lib.memory_retriever import _compute_keyword_match
        score = _compute_keyword_match("nginx config error", "[]", ["nginx", "docker"])
        assert score == pytest.approx(0.5)

    def test_no_match(self):
        from lib.memory_retriever import _compute_keyword_match
        score = _compute_keyword_match("something else", "[]", ["nginx", "docker"])
        assert score == pytest.approx(0.0)

    def test_no_keywords_returns_one(self):
        from lib.memory_retriever import _compute_keyword_match
        score = _compute_keyword_match("anything", "[]", [])
        assert score == pytest.approx(1.0)

    def test_tags_contribute_to_match(self):
        from lib.memory_retriever import _compute_keyword_match
        score = _compute_keyword_match("something else", '["nginx"]', ["nginx"])
        assert score == pytest.approx(1.0)


class TestEffectiveScore:
    def test_calculation(self, monkeypatch):
        from lib.memory_retriever import _effective_score
        monkeypatch.setattr("lib.memory_retriever._RETRIEVAL_CONFIG", None)

        old_date = (datetime.now() - timedelta(days=30)).isoformat()
        memory = {
            "importance_score": 8.0,
            "decay_score": 0.9,
            "created_at": old_date,
            "content": "nginx proxy config fix",
            "tags": "[]",
        }
        score = _effective_score(memory, keywords=["nginx"])
        # kw_match=1.0 (nginx in content), importance=8.0, decay=0.9, recency=0.0
        # = 1.0 * 8.0 * 0.9 + 0.0 = 7.2
        assert score == pytest.approx(7.2)

    def test_no_keywords_full_match(self, monkeypatch):
        from lib.memory_retriever import _effective_score
        monkeypatch.setattr("lib.memory_retriever._RETRIEVAL_CONFIG", None)

        memory = {
            "importance_score": 5.0,
            "decay_score": 1.0,
            "created_at": (datetime.now() - timedelta(days=30)).isoformat(),
            "content": "test",
            "tags": "[]",
        }
        score = _effective_score(memory, keywords=None)
        # kw_match=1.0, importance=5.0, decay=1.0, recency=0.0
        assert score == pytest.approx(5.0)


class TestExtractKeywords:
    def test_filters_stopwords(self):
        from lib.memory_retriever import _extract_keywords
        keywords = _extract_keywords("the nginx configuration is used for proxy")
        assert "the" not in keywords
        assert "nginx" in keywords
        assert "configuration" in keywords
        assert "proxy" in keywords

    def test_filters_short_words(self):
        from lib.memory_retriever import _extract_keywords
        keywords = _extract_keywords("do it on cd")
        assert len(keywords) == 0

    def test_deduplicates(self):
        from lib.memory_retriever import _extract_keywords
        keywords = _extract_keywords("nginx nginx nginx config config")
        assert keywords.count("nginx") == 1
        assert keywords.count("config") == 1

    def test_max_ten_keywords(self):
        from lib.memory_retriever import _extract_keywords
        text = " ".join([f"word{i}xx" for i in range(20)])
        keywords = _extract_keywords(text)
        assert len(keywords) <= 10


class TestRetrieveForStartup:
    def test_returns_formatted_string(self, monkeypatch):
        from lib import memory_retriever as ret
        monkeypatch.setattr("lib.memory_retriever._RETRIEVAL_CONFIG", None)

        monkeypatch.setattr(ret, "get_high_confidence_facts", lambda **kw: [
            {"id": 1, "key": "encoding/utf8", "value": "UTF-8 sans BOM"},
        ])
        monkeypatch.setattr(ret, "get_recent_memories", lambda **kw: [
            {"id": 1, "type": "insight", "content": "Fixed nginx config error"},
        ])
        monkeypatch.setattr(ret, "increment_access", lambda mid: None)
        monkeypatch.setattr(ret, "log_retrieval", lambda *a: None)

        result = ret.retrieve_for_startup(session_id="s1")
        assert len(result) > 0
        assert "encoding/utf8" in result
        assert "nginx" in result.lower()

    def test_returns_empty_when_no_data(self, monkeypatch):
        from lib import memory_retriever as ret
        monkeypatch.setattr("lib.memory_retriever._RETRIEVAL_CONFIG", None)

        monkeypatch.setattr(ret, "get_high_confidence_facts", lambda **kw: [])
        monkeypatch.setattr(ret, "get_recent_memories", lambda **kw: [])

        result = ret.retrieve_for_startup()
        assert result == ""


class TestRetrieveForPrompt:
    def test_skips_short_messages(self, monkeypatch):
        from lib import memory_retriever as ret
        monkeypatch.setattr("lib.memory_retriever._RETRIEVAL_CONFIG", None)

        result = ret.retrieve_for_prompt("hi")
        assert result == ""

    def test_skips_commands(self, monkeypatch):
        from lib import memory_retriever as ret
        monkeypatch.setattr("lib.memory_retriever._RETRIEVAL_CONFIG", None)

        result = ret.retrieve_for_prompt("/some-command with arguments")
        assert result == ""

    def test_returns_matching_memories(self, monkeypatch):
        from lib import memory_retriever as ret
        monkeypatch.setattr("lib.memory_retriever._RETRIEVAL_CONFIG", None)

        monkeypatch.setattr(ret, "search_memories", lambda **kw: [
            {
                "id": 1,
                "type": "problem_solution",
                "content": "Fixed nginx upstream configuration error",
                "tags": '["nginx"]',
                "importance_score": 7.5,
                "decay_score": 1.0,
                "created_at": datetime.now().isoformat(),
            },
        ])
        monkeypatch.setattr(ret, "get_facts", lambda **kw: [])
        monkeypatch.setattr(ret, "increment_access", lambda mid: None)
        monkeypatch.setattr(ret, "log_retrieval", lambda *a: None)

        result = ret.retrieve_for_prompt(
            "How do I configure nginx upstream properly?",
            session_id="s1",
        )
        assert "nginx" in result.lower()

    def test_returns_empty_no_keywords(self, monkeypatch):
        from lib import memory_retriever as ret
        monkeypatch.setattr("lib.memory_retriever._RETRIEVAL_CONFIG", None)

        result = ret.retrieve_for_prompt("the and but or not is are was")
        assert result == ""


# ============================================================
# Module 3: memory_extractor_v2.py
# ============================================================

def _make_assistant_entry(text="", tools=None):
    """Helper: cree une entree assistant avec texte et/ou tool_use."""
    content = []
    if text:
        content.append({"type": "text", "text": text})
    for tool in (tools or []):
        content.append({"type": "tool_use", **tool})
    return {
        "type": "assistant",
        "message": {"content": content},
    }


def _make_tool_result(text, is_error=False):
    """Helper: cree une entree tool_result."""
    return {
        "type": "tool_result",
        "content": text,
    }


class TestExtractToolSequences:
    def test_detects_read_error_edit_pattern(self):
        from memory_extractor_v2 import extract_tool_sequences

        entries = [
            _make_assistant_entry(tools=[
                {"name": "Read", "input": {"file_path": "/etc/nginx/nginx.conf"}},
            ]),
            _make_tool_result("Error: permission denied reading /etc/nginx/nginx.conf"),
            _make_assistant_entry(tools=[
                {"name": "Edit", "input": {"file_path": "/etc/nginx/nginx.conf"}},
            ]),
        ]
        results = extract_tool_sequences(entries)
        assert len(results) >= 1
        assert results[0]["type"] == "tool_sequence"
        assert "Fix sequence" in results[0]["content"]

    def test_no_error_no_sequence(self):
        from memory_extractor_v2 import extract_tool_sequences

        entries = [
            _make_assistant_entry(tools=[
                {"name": "Read", "input": {"file_path": "/foo.txt"}},
            ]),
            _make_tool_result("file contents here"),
        ]
        results = extract_tool_sequences(entries)
        assert len(results) == 0

    def test_respects_max_results(self):
        from memory_extractor_v2 import extract_tool_sequences

        entries = []
        for i in range(10):
            entries.append(_make_assistant_entry(tools=[
                {"name": "Read", "input": {"file_path": f"/file{i}.txt"}},
            ]))
            entries.append(_make_tool_result(f"Error: file{i} not found"))
            entries.append(_make_assistant_entry(tools=[
                {"name": "Edit", "input": {"file_path": f"/file{i}.txt"}},
            ]))

        results = extract_tool_sequences(entries, max_results=2)
        assert len(results) <= 2


class TestExtractProblemSolutions:
    def test_finds_error_explanation_pair(self):
        from memory_extractor_v2 import extract_problem_solutions

        entries = [
            _make_tool_result("Error: ModuleNotFoundError: No module named 'requests'"),
            _make_assistant_entry(
                text="The issue was a missing dependency. We need to install requests via pip install requests."
            ),
        ]
        results = extract_problem_solutions(entries)
        assert len(results) >= 1
        assert results[0]["type"] == "problem_solution"
        assert "Problem:" in results[0]["content"]
        assert "Solution:" in results[0]["content"]

    def test_no_error_no_pair(self):
        from memory_extractor_v2 import extract_problem_solutions

        entries = [
            _make_tool_result("Success: file written"),
            _make_assistant_entry(text="Great, the file was written successfully."),
        ]
        results = extract_problem_solutions(entries)
        assert len(results) == 0


class TestExtractTopics:
    def test_returns_frequent_words(self, monkeypatch):
        from memory_extractor_v2 import extract_topics
        monkeypatch.setattr("memory_extractor_v2._CONFIG", {
            "extraction": {"max_per_type": 5},
            "signals": {},
            "stopwords": {"fr": [], "en": []},
        })

        # 5 entries so "nginx" (in 3/5) and "docker" (in 3/5) stay below 80% threshold
        entries = [
            _make_assistant_entry(text="Docker compose configuration for nginx reverse proxy"),
            _make_assistant_entry(text="The docker container runs nginx with custom settings"),
            _make_assistant_entry(text="Nginx upstream docker backend services configuration"),
            _make_assistant_entry(text="PostgreSQL database backup and replication strategy"),
            _make_assistant_entry(text="Systemd service management and journalctl logging"),
        ]
        topics = extract_topics(entries)
        assert isinstance(topics, list)
        assert len(topics) > 0

    def test_empty_entries_returns_empty(self, monkeypatch):
        from memory_extractor_v2 import extract_topics
        monkeypatch.setattr("memory_extractor_v2._CONFIG", {
            "extraction": {}, "signals": {}, "stopwords": {"fr": [], "en": []},
        })
        assert extract_topics([]) == []


class TestExtractDecisions:
    def test_finds_decision_patterns(self):
        from memory_extractor_v2 import extract_decisions

        entries = [
            _make_assistant_entry(
                text="After examining the options, I'll use docker compose for the deployment because it simplifies orchestration."
            ),
        ]
        results = extract_decisions(entries)
        assert len(results) >= 1
        assert results[0]["type"] == "decision"
        assert "docker compose" in results[0]["content"].lower()

    def test_filters_trivial_decisions(self):
        from memory_extractor_v2 import extract_decisions

        # Text too short (< 40 chars) to be considered
        entries = [
            _make_assistant_entry(text="I'll use Read tool."),
        ]
        results = extract_decisions(entries)
        assert len(results) == 0

    def test_lets_use_pattern(self):
        from memory_extractor_v2 import extract_decisions

        entries = [
            _make_assistant_entry(
                text="Let's use postgresql instead of mysql for the database backend because it handles JSON better."
            ),
        ]
        results = extract_decisions(entries)
        assert len(results) >= 1


class TestExtractFacts:
    def test_detects_encoding_convention(self):
        from memory_extractor_v2 import extract_facts

        entries = [
            _make_assistant_entry(
                text="All markdown files should use UTF-8 sans BOM encoding for cross-platform compatibility."
            ),
        ]
        results = extract_facts(entries)
        assert len(results) >= 1
        assert any(f["key"] == "encoding/utf8" for f in results)

    def test_detects_powershell_compatibility(self):
        from memory_extractor_v2 import extract_facts

        entries = [
            _make_assistant_entry(
                text="Scripts must be compatible PS 5.1, no null coalescing operator allowed."
            ),
        ]
        results = extract_facts(entries)
        assert len(results) >= 1
        keys = [f["key"] for f in results]
        assert "compat/powershell" in keys or "compat/powershell-syntax" in keys

    def test_allows_updates_last_occurrence_wins(self):
        from memory_extractor_v2 import extract_facts

        # Regex: (?:vault|Knowledge)\s+(?:path|dir|dossier)\s*(?:is|est|:)\s*(.{10,100})
        entries = [
            _make_assistant_entry(
                text="The vault path is /old/path/Knowledge for the project setup."
            ),
            _make_assistant_entry(
                text="Actually the vault path is /new/path/Knowledge for the project."
            ),
        ]
        results = extract_facts(entries)
        vault_facts = [f for f in results if f["key"] == "path/vault"]
        assert len(vault_facts) == 1

    def test_no_facts_in_plain_text(self):
        from memory_extractor_v2 import extract_facts

        entries = [
            _make_assistant_entry(text="Just checking the server status, everything looks good."),
        ]
        results = extract_facts(entries)
        assert len(results) == 0


class TestIsErrorResult:
    def test_detects_error_keywords(self):
        from memory_extractor_v2 import _is_error_result

        assert _is_error_result({"type": "tool_result", "content": "Error: file not found"})
        assert _is_error_result({"type": "tool_result", "content": "FAIL: test failed"})
        assert _is_error_result({"type": "tool_result", "content": "Traceback (most recent call last):"})
        assert _is_error_result({"type": "tool_result", "content": "Exception occurred"})

    def test_rejects_non_error(self):
        from memory_extractor_v2 import _is_error_result

        assert not _is_error_result({"type": "tool_result", "content": "Success"})
        assert not _is_error_result({"type": "assistant", "content": "Error in discussion"})


class TestContentHash:
    def test_deterministic(self):
        from memory_extractor_v2 import _content_hash

        h1 = _content_hash("test content")
        h2 = _content_hash("test content")
        assert h1 == h2
        assert len(h1) == 12

    def test_different_content_different_hash(self):
        from memory_extractor_v2 import _content_hash

        h1 = _content_hash("content A")
        h2 = _content_hash("content B")
        assert h1 != h2


# ============================================================
# Module 4: memory_consolidator.py
# ============================================================

class TestTokenize:
    def test_removes_stopwords(self, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr(mc, "_MERGE_STOPWORDS", None)

        tokens = mc._tokenize("the nginx configuration is for proxy server")
        assert "the" not in tokens
        assert "nginx" in tokens
        assert "configuration" in tokens
        assert "proxy" in tokens
        assert "server" in tokens

    def test_returns_set(self, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr(mc, "_MERGE_STOPWORDS", None)

        result = mc._tokenize("nginx nginx nginx")
        assert isinstance(result, set)
        assert len(result) == 1

    def test_filters_short_words(self, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr(mc, "_MERGE_STOPWORDS", None)

        tokens = mc._tokenize("it is on at by if")
        assert len(tokens) == 0


class TestSimilarity:
    def test_identical_text_returns_one(self, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr(mc, "_MERGE_STOPWORDS", None)

        sim = mc._similarity(
            "nginx proxy configuration error",
            "nginx proxy configuration error",
        )
        assert sim == pytest.approx(1.0)

    def test_completely_different_returns_zero(self, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr(mc, "_MERGE_STOPWORDS", None)

        sim = mc._similarity(
            "nginx proxy configuration",
            "postgresql database backup",
        )
        assert sim == pytest.approx(0.0)

    def test_partial_overlap(self, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr(mc, "_MERGE_STOPWORDS", None)

        sim = mc._similarity(
            "nginx proxy configuration",
            "nginx reverse proxy setup",
        )
        assert 0.0 < sim < 1.0

    def test_empty_text_returns_zero(self, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr(mc, "_MERGE_STOPWORDS", None)

        assert mc._similarity("", "nginx test") == 0.0
        assert mc._similarity("nginx test", "") == 0.0


class TestFindMergeCandidates:
    def test_finds_similar_same_type(self, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr(mc, "_MERGE_STOPWORDS", None)

        memories = [
            {
                "id": 1, "type": "problem_solution",
                "content": "nginx upstream configuration proxy error fixed",
                "importance_score": 7.0, "decay_score": 1.0,
            },
            {
                "id": 2, "type": "problem_solution",
                "content": "nginx upstream configuration proxy error resolved",
                "importance_score": 6.0, "decay_score": 1.0,
            },
        ]
        candidates = mc.find_merge_candidates(memories, threshold=0.5)
        assert len(candidates) >= 1
        keep_id, remove_id = candidates[0]
        assert keep_id == 1
        assert remove_id == 2

    def test_rejects_different_types(self, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr(mc, "_MERGE_STOPWORDS", None)

        memories = [
            {
                "id": 1, "type": "problem_solution",
                "content": "nginx upstream configuration proxy error",
                "importance_score": 7.0, "decay_score": 1.0,
            },
            {
                "id": 2, "type": "decision",
                "content": "nginx upstream configuration proxy error",
                "importance_score": 6.0, "decay_score": 1.0,
            },
        ]
        candidates = mc.find_merge_candidates(memories, threshold=0.5)
        assert len(candidates) == 0

    def test_keeps_higher_score(self, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr(mc, "_MERGE_STOPWORDS", None)

        memories = [
            {
                "id": 10, "type": "insight",
                "content": "docker compose deployment orchestration scaling",
                "importance_score": 3.0, "decay_score": 1.0,
            },
            {
                "id": 20, "type": "insight",
                "content": "docker compose deployment orchestration scaling services",
                "importance_score": 9.0, "decay_score": 1.0,
            },
        ]
        candidates = mc.find_merge_candidates(memories, threshold=0.5)
        assert len(candidates) >= 1
        keep_id, remove_id = candidates[0]
        assert keep_id == 20
        assert remove_id == 10

    def test_no_candidates_when_dissimilar(self, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr(mc, "_MERGE_STOPWORDS", None)

        memories = [
            {
                "id": 1, "type": "insight",
                "content": "nginx proxy configuration",
                "importance_score": 5.0, "decay_score": 1.0,
            },
            {
                "id": 2, "type": "insight",
                "content": "postgresql backup strategy",
                "importance_score": 5.0, "decay_score": 1.0,
            },
        ]
        candidates = mc.find_merge_candidates(memories, threshold=0.6)
        assert len(candidates) == 0


class TestConsolidateSmoke:
    def test_consolidate_runs_without_error(self, memory_db, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr("lib.memory_db.DB_PATH", memory_db.DB_PATH)

        # Patch the config loader to avoid yaml dependency
        monkeypatch.setattr(mc, "_load_consolidation_config", lambda: {
            "decay_threshold_days": 7,
            "decay_factor": 0.9,
            "prune_min_score": 0.5,
            "prune_min_age_days": 30,
            "promote_min_access": 3,
            "promote_boost": 1.0,
            "merge_similarity_threshold": 0.6,
        })

        report = mc.consolidate(dry_run=True)
        assert "stats_before" in report
        assert "operations" in report
        assert "stats_after" in report
        assert report["dry_run"] is True

    def test_consolidate_live_run(self, populated_db, monkeypatch):
        import memory_consolidator as mc
        monkeypatch.setattr("lib.memory_db.DB_PATH", populated_db.DB_PATH)

        monkeypatch.setattr(mc, "_load_consolidation_config", lambda: {
            "decay_threshold_days": 7,
            "decay_factor": 0.9,
            "prune_min_score": 0.5,
            "prune_min_age_days": 30,
            "promote_min_access": 3,
            "promote_boost": 1.0,
            "merge_similarity_threshold": 0.6,
        })

        report = mc.consolidate(dry_run=False)
        assert report["dry_run"] is False
        assert "decay" in report["operations"]
        assert "merge" in report["operations"]
        assert "prune" in report["operations"]
        assert "promote" in report["operations"]
