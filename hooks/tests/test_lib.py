"""Tests pour lib/paths.py, lib/utils.py, lib/transcript.py."""

import json
from pathlib import Path

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
