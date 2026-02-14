"""Tests pour subagent_capture.py — parse_subagent_transcript."""

import json
from pathlib import Path

import pytest

from subagent_capture import parse_subagent_transcript


class TestParseSubagentTranscript:
    def _make_transcript(self, tmp_path, entries):
        """Helper: write JSONL transcript and return path string."""
        path = tmp_path / "subagent.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e) + "\n")
        return str(path)

    def test_missing_file(self, tmp_path):
        result = parse_subagent_transcript(str(tmp_path / "nonexistent.jsonl"))
        assert "error" in result

    def test_empty_file(self, tmp_path):
        path = tmp_path / "empty.jsonl"
        path.write_text("", encoding="utf-8")
        result = parse_subagent_transcript(str(path))
        assert result["message_count"] == 0
        assert result["tools_used"] == {}

    def test_basic_parsing(self, tmp_path):
        entries = [
            {
                "type": "assistant",
                "timestamp": "2026-02-11T10:00:00Z",
                "message": {"content": [
                    {"type": "tool_use", "name": "Read", "input": {"file_path": "/foo.md"}},
                    {"type": "tool_use", "name": "Write", "input": {"file_path": "/bar.md"}},
                ]},
            },
            {
                "type": "assistant",
                "timestamp": "2026-02-11T10:02:00Z",
                "message": {"content": [
                    {"type": "text", "text": "I have completed the requested changes to the file."},
                ]},
            },
        ]
        result = parse_subagent_transcript(self._make_transcript(tmp_path, entries))
        assert result["message_count"] == 2
        assert result["tools_used"]["Read"] == 1
        assert result["tools_used"]["Write"] == 1
        assert "/bar.md" in result["files_modified"]
        assert "/foo.md" not in result["files_modified"]  # Read != modified
        assert result["duration_s"] == 120

    def test_detects_agent_name(self, tmp_path):
        entries = [{
            "type": "assistant",
            "timestamp": "2026-02-11T10:00:00Z",
            "message": {"content": [{
                "type": "tool_use",
                "name": "Task",
                "input": {
                    "description": "Build the skill",
                    "subagent_type": "skill-builder",
                },
            }]},
        }]
        result = parse_subagent_transcript(self._make_transcript(tmp_path, entries))
        assert result["agent_name"] == "skill-builder"
        assert result["description"] == "Build the skill"

    def test_files_modified_from_edit(self, tmp_path):
        entries = [{
            "type": "assistant",
            "timestamp": "2026-02-11T10:00:00Z",
            "message": {"content": [{
                "type": "tool_use",
                "name": "Edit",
                "input": {"file_path": "/src/main.py"},
            }]},
        }]
        result = parse_subagent_transcript(self._make_transcript(tmp_path, entries))
        assert "/src/main.py" in result["files_modified"]

    def test_outcome_summary(self, tmp_path):
        entries = [{
            "type": "assistant",
            "timestamp": "2026-02-11T10:00:00Z",
            "message": {"content": [{
                "type": "text",
                "text": "Successfully deployed the container to production environment.",
            }]},
        }]
        result = parse_subagent_transcript(self._make_transcript(tmp_path, entries))
        assert "deployed" in result["outcome_summary"].lower()

    def test_max_lines_limits(self, tmp_path):
        """Only last max_lines should be parsed."""
        entries = []
        for i in range(100):
            entries.append({
                "type": "assistant",
                "timestamp": f"2026-02-11T10:{i:02d}:00Z",
                "message": {"content": [{"type": "text", "text": f"Step {i} complete."}]},
            })
        result = parse_subagent_transcript(
            self._make_transcript(tmp_path, entries), max_lines=10
        )
        assert result["message_count"] == 10

    def test_no_duration_without_timestamps(self, tmp_path):
        entries = [{
            "type": "assistant",
            "message": {"content": [{"type": "text", "text": "Quick response text here."}]},
        }]
        result = parse_subagent_transcript(self._make_transcript(tmp_path, entries))
        assert result["duration_s"] is None
