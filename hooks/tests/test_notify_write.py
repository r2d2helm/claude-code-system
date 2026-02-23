"""Tests pour notify_write.py — notification ecriture fichier markdown."""

import json
import sys
from io import StringIO

import pytest

from notify_write import main


class TestNotifyWriteMain:
    def test_markdown_file_detected(self, monkeypatch, capsys):
        """Un fichier .md declenche un message sur stderr."""
        input_data = {
            "tool_input": {"file_path": "/home/user/docs/notes.md"},
        }
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "[hook] Markdown saved:" in captured.err
        assert "notes.md" in captured.err

    def test_non_markdown_ignored(self, monkeypatch, capsys):
        """Un fichier non-.md ne produit pas de message."""
        input_data = {
            "tool_input": {"file_path": "/home/user/src/main.py"},
        }
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert captured.err == ""

    def test_json_file_ignored(self, monkeypatch, capsys):
        """Un fichier .json ne declenche pas de notification."""
        input_data = {
            "tool_input": {"file_path": "/config/settings.json"},
        }
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert captured.err == ""

    def test_empty_file_path(self, monkeypatch, capsys):
        """file_path vide -> pas de notification, exit 0."""
        input_data = {
            "tool_input": {"file_path": ""},
        }
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert captured.err == ""

    def test_missing_file_path_key(self, monkeypatch, capsys):
        """Cle file_path absente -> pas de notification, exit 0."""
        input_data = {
            "tool_input": {},
        }
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert captured.err == ""

    def test_missing_tool_input(self, monkeypatch, capsys):
        """tool_input absent -> pas de crash, exit 0."""
        input_data = {}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert captured.err == ""

    def test_exception_handling_invalid_json(self, monkeypatch, capsys):
        """JSON invalide sur stdin -> fail-open, exit 0."""
        monkeypatch.setattr("sys.stdin", StringIO("not valid json"))

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_exception_handling_empty_stdin(self, monkeypatch, capsys):
        """Stdin vide -> fail-open, exit 0."""
        monkeypatch.setattr("sys.stdin", StringIO(""))

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_md_extension_case_sensitive(self, monkeypatch, capsys):
        """L'extension .MD (majuscule) n'est pas detectee (endswith est case-sensitive)."""
        input_data = {
            "tool_input": {"file_path": "/docs/README.MD"},
        }
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        # .MD != .md, donc pas de notification
        assert captured.err == ""

    def test_markdown_with_nested_path(self, monkeypatch, capsys):
        """Chemin complexe avec .md -> notification correcte."""
        input_data = {
            "tool_input": {"file_path": "/home/user/vault/_Daily/2026-02-12.md"},
        }
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "[hook] Markdown saved:" in captured.err
        assert "2026-02-12.md" in captured.err
