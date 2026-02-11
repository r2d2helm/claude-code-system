"""Tests pour memory_extractor.py — extract_insights, create_vault_note, duration."""

import json
from pathlib import Path

import pytest

from memory_extractor import (
    extract_insights,
    _compute_duration_s,
    _content_hash,
    create_vault_note,
)


class TestContentHash:
    def test_returns_string(self):
        assert isinstance(_content_hash("hello"), str)

    def test_length_12(self):
        assert len(_content_hash("some text")) == 12

    def test_deterministic(self):
        assert _content_hash("test") == _content_hash("test")

    def test_different_inputs(self):
        assert _content_hash("a") != _content_hash("b")


class TestComputeDuration:
    def test_valid_timestamps(self):
        result = _compute_duration_s(
            "2026-02-11T10:00:00Z",
            "2026-02-11T10:05:00Z",
        )
        assert result == 300

    def test_empty_timestamps(self):
        assert _compute_duration_s("", "") == 0

    def test_none_first(self):
        assert _compute_duration_s("", "2026-02-11T10:00:00Z") == 0

    def test_none_last(self):
        assert _compute_duration_s("2026-02-11T10:00:00Z", "") == 0

    def test_same_timestamp(self):
        ts = "2026-02-11T10:00:00Z"
        assert _compute_duration_s(ts, ts) == 0

    def test_format_with_milliseconds(self):
        result = _compute_duration_s(
            "2026-02-11T10:00:00.000Z",
            "2026-02-11T10:01:30.500Z",
        )
        assert result == 90

    def test_negative_returns_zero(self):
        """If last < first, should return 0."""
        result = _compute_duration_s(
            "2026-02-11T10:05:00Z",
            "2026-02-11T10:00:00Z",
        )
        assert result == 0


class TestExtractInsights:
    def _make_transcript(self, tmp_path, entries):
        """Helper: write JSONL transcript and return path."""
        path = tmp_path / "transcript.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e) + "\n")
        return str(path)

    def test_missing_file(self, tmp_path):
        result = extract_insights(str(tmp_path / "nonexistent.jsonl"))
        assert result["insights"] == []
        assert result["patterns"] == []
        assert result["errors_count"] == 0

    def test_empty_file(self, tmp_path):
        path = tmp_path / "empty.jsonl"
        path.write_text("", encoding="utf-8")
        result = extract_insights(str(path))
        assert result["insights"] == []

    def test_finds_insight(self, tmp_path):
        entries = [{
            "type": "assistant",
            "timestamp": "2026-02-11T10:00:00Z",
            "message": {"content": [{
                "type": "text",
                "text": "The issue was a missing import statement in the module configuration."
            }]},
        }]
        result = extract_insights(self._make_transcript(tmp_path, entries))
        assert len(result["insights"]) >= 1
        assert "missing import" in result["insights"][0]["content"].lower()

    def test_finds_pattern(self, tmp_path):
        entries = [{
            "type": "assistant",
            "timestamp": "2026-02-11T10:00:00Z",
            "message": {"content": [{
                "type": "text",
                "text": "You should always use UTF-8 encoding when writing files on Windows."
            }]},
        }]
        result = extract_insights(self._make_transcript(tmp_path, entries))
        assert len(result["patterns"]) >= 1

    def test_counts_errors(self, tmp_path):
        entries = [
            {"type": "tool_result", "content": "Error: file not found"},
            {"type": "tool_result", "content": "Traceback (most recent call last)"},
            {"type": "tool_result", "content": "OK success"},
        ]
        result = extract_insights(self._make_transcript(tmp_path, entries))
        assert result["errors_count"] == 2

    def test_deduplication(self, tmp_path):
        """Same text twice should not produce duplicate insights."""
        text = "The issue was a missing import statement in the module configuration."
        entries = [
            {"type": "assistant", "timestamp": "2026-02-11T10:00:00Z",
             "message": {"content": [{"type": "text", "text": text}]}},
            {"type": "assistant", "timestamp": "2026-02-11T10:01:00Z",
             "message": {"content": [{"type": "text", "text": text}]}},
        ]
        result = extract_insights(self._make_transcript(tmp_path, entries))
        hashes = [i["hash"] for i in result["insights"]]
        assert len(hashes) == len(set(hashes))

    def test_max_lines_limits(self, tmp_path):
        """Only last max_lines should be parsed."""
        entries = []
        for i in range(100):
            entries.append({
                "type": "assistant",
                "timestamp": f"2026-02-11T10:{i:02d}:00Z",
                "message": {"content": [{"type": "text", "text": f"Message {i}"}]},
            })
        result = extract_insights(self._make_transcript(tmp_path, entries), max_lines=10)
        # Should not crash, and should process only last 10 lines
        assert result["errors_count"] == 0


class TestCreateVaultNote:
    def test_creates_note(self, tmp_path, monkeypatch):
        import memory_extractor
        vault = tmp_path / "vault"
        inbox = vault / "_Inbox"
        inbox.mkdir(parents=True)
        monkeypatch.setattr(memory_extractor, "VAULT_PATH", vault)

        insight = {
            "content": "The fix was to add the missing import at the top of the module file always.",
            "hash": "abc123def456",
        }
        create_vault_note(insight, "session-001")

        notes = list(inbox.glob("*.md"))
        assert len(notes) == 1
        content = notes[0].read_text(encoding="utf-8")
        assert "Auto-insight" in content
        assert "abc123" in content
        assert "seedling" in content

    def test_short_content_skipped(self, tmp_path, monkeypatch):
        import memory_extractor
        vault = tmp_path / "vault"
        inbox = vault / "_Inbox"
        inbox.mkdir(parents=True)
        monkeypatch.setattr(memory_extractor, "VAULT_PATH", vault)

        insight = {"content": "too short", "hash": "abc"}
        create_vault_note(insight, "session-001")

        notes = list(inbox.glob("*.md"))
        assert len(notes) == 0

    def test_no_overwrite_existing(self, tmp_path, monkeypatch):
        import memory_extractor
        vault = tmp_path / "vault"
        inbox = vault / "_Inbox"
        inbox.mkdir(parents=True)
        monkeypatch.setattr(memory_extractor, "VAULT_PATH", vault)

        insight = {
            "content": "The fix was to add the missing import at the top of the module file always.",
            "hash": "abc123def456",
        }
        create_vault_note(insight, "session-001")
        first_notes = list(inbox.glob("*.md"))
        first_content = first_notes[0].read_text(encoding="utf-8")

        # Call again — should not overwrite
        create_vault_note(insight, "session-002")
        second_content = first_notes[0].read_text(encoding="utf-8")
        assert first_content == second_content

    def test_missing_inbox_skips(self, tmp_path, monkeypatch):
        import memory_extractor
        vault = tmp_path / "vault"
        vault.mkdir(parents=True)
        # No _Inbox directory
        monkeypatch.setattr(memory_extractor, "VAULT_PATH", vault)

        insight = {
            "content": "The fix was to add the missing import at the top of the module file always.",
            "hash": "abc123def456",
        }
        # Should not raise
        create_vault_note(insight, "session-001")
