"""Tests pour lib/paths.py, lib/utils.py, lib/transcript.py."""

import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

import pytest


class TestPaths:
    def test_paths_are_path_objects(self):
        from lib.paths import CLAUDE_DIR, HOOKS_DIR, VAULT_PATH, SKILLS_DIR, LOGS_DIR
        assert isinstance(CLAUDE_DIR, Path)
        assert isinstance(HOOKS_DIR, Path)
        assert isinstance(VAULT_PATH, Path)
        assert isinstance(SKILLS_DIR, Path)
        assert isinstance(LOGS_DIR, Path)

    def test_paths_relative_to_home(self):
        from lib.paths import CLAUDE_DIR, VAULT_PATH
        home = Path.home()
        assert str(CLAUDE_DIR).startswith(str(home))
        assert str(VAULT_PATH).startswith(str(home))

    def test_memory_dir_under_data(self):
        from lib.paths import MEMORY_DIR, DATA_DIR
        assert MEMORY_DIR.parent == DATA_DIR


class TestUtils:
    def test_read_stdin_json_valid(self, mock_stdin):
        from lib.utils import read_stdin_json
        mock_stdin({"key": "value"})
        result = read_stdin_json()
        assert result == {"key": "value"}

    def test_read_stdin_json_empty(self, monkeypatch):
        from io import StringIO
        from lib.utils import read_stdin_json
        monkeypatch.setattr("sys.stdin", StringIO(""))
        result = read_stdin_json()
        assert result == {}

    def test_read_stdin_json_invalid(self, monkeypatch):
        from io import StringIO
        from lib.utils import read_stdin_json
        monkeypatch.setattr("sys.stdin", StringIO("not json"))
        result = read_stdin_json()
        assert result == {}

    def test_now_paris_returns_iso_format(self):
        from lib.utils import now_paris
        result = now_paris()
        assert "T" in result
        assert "+" in result or "Z" in result

    def test_append_jsonl_creates_file(self, tmp_path):
        from lib.utils import append_jsonl
        path = tmp_path / "test.jsonl"
        append_jsonl(path, {"foo": "bar"})
        assert path.exists()
        line = path.read_text(encoding="utf-8").strip()
        assert json.loads(line) == {"foo": "bar"}

    def test_append_jsonl_appends(self, tmp_path):
        from lib.utils import append_jsonl
        path = tmp_path / "test.jsonl"
        append_jsonl(path, {"a": 1})
        append_jsonl(path, {"b": 2})
        lines = path.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 2
        assert json.loads(lines[0]) == {"a": 1}
        assert json.loads(lines[1]) == {"b": 2}

    def test_append_jsonl_creates_parent(self, tmp_path):
        from lib.utils import append_jsonl
        path = tmp_path / "sub" / "dir" / "test.jsonl"
        append_jsonl(path, {"nested": True})
        assert path.exists()


class TestTranscript:
    def test_parse_transcript_basic(self, sample_transcript):
        from lib.transcript import parse_transcript
        result = parse_transcript(str(sample_transcript))
        assert result["message_count"] == 5
        assert "Read" in result["tools_used"]
        assert "Write" in result["tools_used"]
        assert "Bash" in result["tools_used"]
        assert "Edit" in result["tools_used"]

    def test_parse_transcript_files_modified(self, sample_transcript):
        from lib.transcript import parse_transcript
        result = parse_transcript(str(sample_transcript))
        assert "/bar.md" in result["files_modified"]
        assert "/baz.py" in result["files_modified"]
        assert "/foo.md" not in result["files_modified"]  # Read, not Write

    def test_parse_transcript_bash_commands(self, sample_transcript):
        from lib.transcript import parse_transcript
        result = parse_transcript(str(sample_transcript))
        assert result["bash_commands_count"] == 1
        assert "git status" in result["bash_commands_sample"][0]

    def test_parse_transcript_timestamps(self, sample_transcript):
        from lib.transcript import parse_transcript
        result = parse_transcript(str(sample_transcript))
        assert result["first_timestamp"] == "2026-02-11T10:00:00Z"
        assert result["last_timestamp"] == "2026-02-11T10:03:00Z"

    def test_parse_transcript_missing_file(self, tmp_path):
        from lib.transcript import parse_transcript
        result = parse_transcript(str(tmp_path / "nonexistent.jsonl"))
        assert "error" in result

    def test_parse_transcript_max_lines(self, tmp_path):
        from lib.transcript import parse_transcript
        # Create a long transcript
        transcript = tmp_path / "long.jsonl"
        with open(transcript, "w", encoding="utf-8") as f:
            for i in range(300):
                entry = {"type": "assistant", "timestamp": f"2026-02-11T10:{i:02d}:00Z",
                         "message": {"content": [{"type": "text", "text": f"msg {i}"}]}}
                f.write(json.dumps(entry) + "\n")
        result = parse_transcript(str(transcript), max_lines=50)
        # Should only parse last 50 lines, not all 300
        assert result["message_count"] == 50

class TestDSTFallback:
    """Tests pour _compute_paris_offset (fallback DST dynamique)."""

    def test_winter_cet(self):
        from lib.utils import _compute_paris_offset
        # 15 janvier 2026 12:00 UTC -> CET (UTC+1)
        now = datetime(2026, 1, 15, 12, 0, tzinfo=timezone.utc)
        assert _compute_paris_offset(now) == timedelta(hours=1)

    def test_summer_cest(self):
        from lib.utils import _compute_paris_offset
        # 15 juillet 2026 12:00 UTC -> CEST (UTC+2)
        now = datetime(2026, 7, 15, 12, 0, tzinfo=timezone.utc)
        assert _compute_paris_offset(now) == timedelta(hours=2)

    def test_march_transition_before(self):
        from lib.utils import _compute_paris_offset
        # 2026: dernier dimanche de mars = 29 mars
        # Juste avant la transition (29 mars 00:59 UTC) -> encore CET
        now = datetime(2026, 3, 29, 0, 59, tzinfo=timezone.utc)
        assert _compute_paris_offset(now) == timedelta(hours=1)

    def test_march_transition_after(self):
        from lib.utils import _compute_paris_offset
        # 29 mars 2026 01:00 UTC -> bascule CEST (UTC+2)
        now = datetime(2026, 3, 29, 1, 0, tzinfo=timezone.utc)
        assert _compute_paris_offset(now) == timedelta(hours=2)

    def test_october_transition_before(self):
        from lib.utils import _compute_paris_offset
        # 2026: dernier dimanche d'octobre = 25 octobre
        # Juste avant (25 oct 00:59 UTC) -> encore CEST
        now = datetime(2026, 10, 25, 0, 59, tzinfo=timezone.utc)
        assert _compute_paris_offset(now) == timedelta(hours=2)

    def test_october_transition_after(self):
        from lib.utils import _compute_paris_offset
        # 25 octobre 2026 01:00 UTC -> bascule CET (UTC+1)
        now = datetime(2026, 10, 25, 1, 0, tzinfo=timezone.utc)
        assert _compute_paris_offset(now) == timedelta(hours=1)


class TestTranscriptRobustness:
    """Tests de robustesse pour parse_transcript."""

    def test_malformed_json_lines(self, tmp_path):
        from lib.transcript import parse_transcript
        transcript = tmp_path / "malformed.jsonl"
        lines = [
            "not json",
            json.dumps({"type": "assistant", "timestamp": "2026-01-01T00:00:00Z",
                        "message": {"content": [{"type": "text", "text": "hello"}]}}),
            "{broken",
        ]
        transcript.write_text(chr(10).join(lines) + chr(10), encoding="utf-8")
        result = parse_transcript(str(transcript))
        assert result["malformed_lines"] == 2
        assert result["message_count"] == 1

    def test_message_is_none(self, tmp_path):
        from lib.transcript import parse_transcript
        transcript = tmp_path / "msg_none.jsonl"
        entry = {"type": "assistant", "timestamp": "2026-01-01T00:00:00Z", "message": None}
        transcript.write_text(json.dumps(entry) + chr(10), encoding="utf-8")
        result = parse_transcript(str(transcript))
        assert result["message_count"] == 1
        assert result["tools_used"] == {}

    def test_content_is_string_not_list(self, tmp_path):
        from lib.transcript import parse_transcript
        transcript = tmp_path / "content_str.jsonl"
        entry = {"type": "assistant", "timestamp": "2026-01-01T00:00:00Z",
                 "message": {"content": "just a string"}}
        transcript.write_text(json.dumps(entry) + chr(10), encoding="utf-8")
        result = parse_transcript(str(transcript))
        assert result["message_count"] == 1
        assert result["tools_used"] == {}

    def test_missing_message_key(self, tmp_path):
        from lib.transcript import parse_transcript
        transcript = tmp_path / "no_msg.jsonl"
        entry = {"type": "assistant", "timestamp": "2026-01-01T00:00:00Z"}
        transcript.write_text(json.dumps(entry) + chr(10), encoding="utf-8")
        result = parse_transcript(str(transcript))
        assert result["message_count"] == 1
        assert result["tools_used"] == {}

    def test_command_non_string(self, tmp_path):
        from lib.transcript import parse_transcript
        transcript = tmp_path / "cmd_int.jsonl"
        entry = {"type": "assistant", "timestamp": "2026-01-01T00:00:00Z",
                 "message": {"content": [{"type": "tool_use", "name": "Bash",
                 "input": {"command": 12345}}]}}
        transcript.write_text(json.dumps(entry) + chr(10), encoding="utf-8")
        result = parse_transcript(str(transcript))
        assert result["bash_commands_count"] == 0
