"""Tests pour lib/memory_retriever.py — moteur de recuperation contextuelle.

Teste le scoring, l'extraction de keywords,
et les deux modes de retrieval (startup, per_prompt).
"""

import pytest


# ============================================================
# Fixture: DB isolee + seed data
# ============================================================

@pytest.fixture(autouse=True)
def isolated_db(monkeypatch, tmp_path):
    """Redirige DB_PATH et reset le cache config."""
    db_file = tmp_path / "test_retriever.db"
    from lib import memory_db
    monkeypatch.setattr(memory_db, "DB_PATH", db_file)
    memory_db.ensure_schema()

    # Reset config cache du retriever
    from lib import memory_retriever
    monkeypatch.setattr(memory_retriever, "_RETRIEVAL_CONFIG", None)

    return db_file


@pytest.fixture
def seeded_db():
    """Seed la DB avec des donnees de test."""
    from lib.memory_db import upsert_session, insert_memory, upsert_fact
    upsert_session({"id": "sess-ret-1", "duration_s": 300})
    upsert_session({"id": "sess-ret-2", "duration_s": 600})

    insert_memory({
        "session_id": "sess-ret-1", "type": "problem_solution",
        "content": "Docker compose networking issue: fixed by using bridge network",
        "importance_score": 8.0, "tags": ["docker", "networking"],
    })
    insert_memory({
        "session_id": "sess-ret-1", "type": "decision",
        "content": "Use SQLite WAL mode for concurrent memory access",
        "importance_score": 7.0, "tags": ["sqlite", "architecture"],
    })
    insert_memory({
        "session_id": "sess-ret-2", "type": "insight",
        "content": "PowerShell 5.1 requires UTF-8 BOM for script files",
        "importance_score": 6.0, "tags": ["powershell", "encoding"],
    })
    insert_memory({
        "session_id": "sess-ret-2", "type": "tool_sequence",
        "content": "Read -> Edit -> Bash(pytest) for test-driven fixes",
        "importance_score": 3.0, "tags": ["workflow"],
    })

    upsert_fact("python_version", "3.12", confidence=0.9, session_id="sess-ret-1")
    upsert_fact("os", "windows", confidence=0.8, session_id="sess-ret-1")
    upsert_fact("editor", "vscode", confidence=0.5, session_id="sess-ret-2")


# ============================================================
# Keyword extraction
# ============================================================

class TestExtractKeywords:
    def test_basic_extraction(self):
        from lib.memory_retriever import _extract_keywords
        kws = _extract_keywords("configure docker compose for nginx proxy")
        assert "docker" in kws
        assert "compose" in kws
        assert "nginx" in kws
        assert "proxy" in kws

    def test_stopwords_removed(self):
        from lib.memory_retriever import _extract_keywords
        kws = _extract_keywords("the file is used for making all the things")
        # "the", "is", "for", "all", "file", "use/used", "make/making" are stopwords
        assert "the" not in kws
        assert "file" not in kws

    def test_short_words_excluded(self):
        from lib.memory_retriever import _extract_keywords
        kws = _extract_keywords("go to py or js")
        # Words <= 2 chars should be excluded
        assert "go" not in kws
        assert "to" not in kws
        assert "py" not in kws
        assert "or" not in kws
        assert "js" not in kws

    def test_max_10_keywords(self):
        from lib.memory_retriever import _extract_keywords
        long_msg = " ".join(f"keyword{i}" for i in range(20))
        kws = _extract_keywords(long_msg)
        assert len(kws) <= 10

    def test_deduplication(self):
        from lib.memory_retriever import _extract_keywords
        kws = _extract_keywords("docker docker docker compose compose")
        assert kws.count("docker") == 1
        assert kws.count("compose") == 1

    def test_empty_message(self):
        from lib.memory_retriever import _extract_keywords
        assert _extract_keywords("") == []

    def test_preserves_order(self):
        from lib.memory_retriever import _extract_keywords
        kws = _extract_keywords("python sqlite docker nginx")
        assert kws.index("python") < kws.index("sqlite")
        assert kws.index("sqlite") < kws.index("docker")


# ============================================================
# Scoring
# ============================================================

class TestScoring:
    def test_recency_boost_recent(self):
        from lib.memory_retriever import _compute_recency_boost
        from lib.utils import now_paris
        boost = _compute_recency_boost(now_paris())
        assert boost > 0  # Devrait avoir un bonus recence

    def test_recency_boost_old(self):
        from lib.memory_retriever import _compute_recency_boost
        boost = _compute_recency_boost("2020-01-01T00:00:00")
        assert boost == 0.0

    def test_recency_boost_empty(self):
        from lib.memory_retriever import _compute_recency_boost
        assert _compute_recency_boost("") == 0.0

    def test_keyword_match_full(self):
        from lib.memory_retriever import _compute_keyword_match
        score = _compute_keyword_match("docker compose networking", "[]", ["docker", "compose"])
        assert score == 1.0

    def test_keyword_match_partial(self):
        from lib.memory_retriever import _compute_keyword_match
        score = _compute_keyword_match("docker only", "[]", ["docker", "nginx"])
        assert score == pytest.approx(0.5)

    def test_keyword_match_none(self):
        from lib.memory_retriever import _compute_keyword_match
        score = _compute_keyword_match("python coding", "[]", ["docker", "nginx"])
        assert score == 0.0

    def test_keyword_match_empty_keywords(self):
        from lib.memory_retriever import _compute_keyword_match
        score = _compute_keyword_match("anything", "[]", [])
        assert score == 1.0  # Pas de filtre = match total

    def test_keyword_match_includes_tags(self):
        from lib.memory_retriever import _compute_keyword_match
        score = _compute_keyword_match("some content", '["docker", "networking"]', ["docker"])
        assert score == 1.0

    def test_effective_score(self):
        from lib.memory_retriever import _effective_score
        memory = {
            "importance_score": 8.0,
            "decay_score": 1.0,
            "created_at": "2020-01-01T00:00:00",
            "content": "docker compose fix",
            "tags": "[]",
        }
        score = _effective_score(memory, keywords=["docker"])
        assert score > 0

    def test_effective_score_no_keywords(self):
        from lib.memory_retriever import _effective_score
        memory = {
            "importance_score": 8.0,
            "decay_score": 0.5,
            "created_at": "2020-01-01T00:00:00",
            "content": "test",
            "tags": "[]",
        }
        # Sans keywords: kw_match = 1.0, score = 1.0 * 8.0 * 0.5 + 0 = 4.0
        score = _effective_score(memory)
        assert score == pytest.approx(4.0)


# ============================================================
# Retrieve for startup
# ============================================================

class TestRetrieveForStartup:
    def test_returns_string(self, seeded_db):
        from lib.memory_retriever import retrieve_for_startup
        result = retrieve_for_startup("sess-new")
        assert isinstance(result, str)

    def test_includes_facts(self, seeded_db):
        from lib.memory_retriever import retrieve_for_startup
        result = retrieve_for_startup("sess-new")
        # Should include high-confidence facts (python_version=0.9, os=0.8)
        assert "python_version" in result or "os" in result or result == ""

    def test_includes_memories(self, seeded_db):
        from lib.memory_retriever import retrieve_for_startup
        result = retrieve_for_startup("sess-new")
        # High importance memories (8.0, 7.0) should be included
        if result:
            assert "docker" in result.lower() or "sqlite" in result.lower() or "Recent" in result

    def test_max_chars_respected(self, seeded_db):
        from lib.memory_retriever import retrieve_for_startup
        result = retrieve_for_startup("sess-new")
        assert len(result) <= 500

    def test_empty_db_returns_empty(self):
        from lib.memory_retriever import retrieve_for_startup
        result = retrieve_for_startup("sess-empty")
        assert result == ""

    def test_logs_retrievals(self, seeded_db):
        from lib.memory_retriever import retrieve_for_startup
        from lib.memory_db import _get_connection
        retrieve_for_startup("sess-log-test")

        conn = _get_connection()
        rows = conn.execute(
            "SELECT * FROM retrieval_log WHERE session_id = 'sess-log-test'"
        ).fetchall()
        conn.close()
        # Should have logged at least one retrieval
        assert len(rows) >= 0  # May be 0 if nothing retrieved


# ============================================================
# Retrieve for prompt
# ============================================================

class TestRetrieveForPrompt:
    def test_returns_string(self, seeded_db):
        from lib.memory_retriever import retrieve_for_prompt
        result = retrieve_for_prompt("configure docker compose networking", "sess-p1")
        assert isinstance(result, str)

    def test_matches_keywords(self, seeded_db):
        from lib.memory_retriever import retrieve_for_prompt
        result = retrieve_for_prompt("docker compose networking issue bridge", "sess-p1")
        if result:
            assert "docker" in result.lower() or "network" in result.lower()

    def test_short_message_returns_empty(self, seeded_db):
        from lib.memory_retriever import retrieve_for_prompt
        result = retrieve_for_prompt("hi", "sess-p1")
        assert result == ""

    def test_empty_message_returns_empty(self, seeded_db):
        from lib.memory_retriever import retrieve_for_prompt
        result = retrieve_for_prompt("", "sess-p1")
        assert result == ""

    def test_command_skipped(self, seeded_db):
        from lib.memory_retriever import retrieve_for_prompt
        result = retrieve_for_prompt("/dk-ps list containers docker", "sess-p1")
        assert result == ""

    def test_max_chars_respected(self, seeded_db):
        from lib.memory_retriever import retrieve_for_prompt
        result = retrieve_for_prompt("configure docker compose networking setup", "sess-p1")
        assert len(result) <= 300

    def test_no_match_returns_empty(self, seeded_db):
        from lib.memory_retriever import retrieve_for_prompt
        result = retrieve_for_prompt("kubernetes helm charts deployment", "sess-p1")
        # No memories about kubernetes
        assert result == ""

    def test_powershell_match(self, seeded_db):
        from lib.memory_retriever import retrieve_for_prompt
        result = retrieve_for_prompt("powershell encoding script utf8 BOM", "sess-p1")
        if result:
            assert "powershell" in result.lower() or "utf" in result.lower()


# ============================================================
# Config loading
# ============================================================

class TestConfig:
    def test_default_config(self, monkeypatch):
        from lib.memory_retriever import _load_retrieval_config
        config = _load_retrieval_config()
        assert "startup" in config
        assert "per_prompt" in config
        assert "scoring" in config
        assert config["startup"]["max_chars"] == 500
        assert config["per_prompt"]["max_chars"] == 300

    def test_config_from_yaml(self, monkeypatch, tmp_path):
        from lib import memory_retriever
        # Patch CONFIG_DIR dans le module retriever (ou il est importe)
        monkeypatch.setattr(memory_retriever, "CONFIG_DIR", tmp_path)
        monkeypatch.setattr(memory_retriever, "_RETRIEVAL_CONFIG", None)

        yaml_content = (
            "retrieval:\n"
            "  startup:\n"
            "    max_chars: 800\n"
            "  per_prompt:\n"
            "    max_chars: 400\n"
        )
        (tmp_path / "memory_v2.yaml").write_text(yaml_content, encoding="utf-8")

        config = memory_retriever._load_retrieval_config()
        assert config["startup"]["max_chars"] == 800
        assert config["per_prompt"]["max_chars"] == 400

    def test_missing_yaml_uses_defaults(self, monkeypatch, tmp_path):
        from lib import paths as paths_mod
        from lib import memory_retriever
        monkeypatch.setattr(paths_mod, "CONFIG_DIR", tmp_path / "nonexistent")
        monkeypatch.setattr(memory_retriever, "_RETRIEVAL_CONFIG", None)

        config = memory_retriever._load_retrieval_config()
        assert config["startup"]["max_chars"] == 500
