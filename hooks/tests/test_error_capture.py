"""Tests pour error_capture.py — capture erreurs Bash et detection corrections."""

import json
import sys
from io import StringIO
from pathlib import Path

import pytest

from error_capture import main, _get_base_command, _find_recent_error


class TestGetBaseCommand:
    def test_simple_command(self):
        assert _get_base_command("git status") == "git"

    def test_single_word(self):
        assert _get_base_command("ls") == "ls"

    def test_command_with_flags(self):
        assert _get_base_command("apt install -y nginx") == "apt"

    def test_empty_string(self):
        assert _get_base_command("") == ""

    def test_whitespace_only(self):
        assert _get_base_command("   ") == ""

    def test_leading_whitespace(self):
        assert _get_base_command("  docker ps") == "docker"


class TestFindRecentError:
    def test_no_errors_file(self, monkeypatch, tmp_path):
        """Retourne None si le fichier errors.jsonl n'existe pas."""
        from lib import paths as paths_mod
        monkeypatch.setattr(paths_mod, "MEMORY_DIR", tmp_path / "memory")
        # Re-import to pick up patched path
        import error_capture
        monkeypatch.setattr(error_capture, "MEMORY_DIR", tmp_path / "memory")
        result = _find_recent_error("git", "session-123")
        assert result is None

    def test_finds_matching_error(self, monkeypatch, tmp_path):
        """Trouve une erreur recente avec la meme commande de base."""
        mem_dir = tmp_path / "memory"
        mem_dir.mkdir()
        errors_file = mem_dir / "errors.jsonl"

        entry = {
            "session_id": "sess-abc",
            "command": "git push origin main",
            "error_type": "exit_code_1",
            "exit_code": 1,
            "stderr_preview": "rejected",
        }
        errors_file.write_text(json.dumps(entry) + "\n", encoding="utf-8")

        import error_capture
        monkeypatch.setattr(error_capture, "MEMORY_DIR", mem_dir)

        result = _find_recent_error("git", "sess-abc")
        assert result is not None
        assert result["command"] == "git push origin main"

    def test_no_match_different_session(self, monkeypatch, tmp_path):
        """Ne trouve pas d'erreur si le session_id differe."""
        mem_dir = tmp_path / "memory"
        mem_dir.mkdir()
        errors_file = mem_dir / "errors.jsonl"

        entry = {
            "session_id": "other-session",
            "command": "git push",
            "error_type": "exit_code_1",
        }
        errors_file.write_text(json.dumps(entry) + "\n", encoding="utf-8")

        import error_capture
        monkeypatch.setattr(error_capture, "MEMORY_DIR", mem_dir)

        result = _find_recent_error("git", "sess-abc")
        assert result is None

    def test_no_match_different_base_command(self, monkeypatch, tmp_path):
        """Ne trouve pas d'erreur si la commande de base differe."""
        mem_dir = tmp_path / "memory"
        mem_dir.mkdir()
        errors_file = mem_dir / "errors.jsonl"

        entry = {
            "session_id": "sess-abc",
            "command": "npm install",
            "error_type": "exit_code_1",
        }
        errors_file.write_text(json.dumps(entry) + "\n", encoding="utf-8")

        import error_capture
        monkeypatch.setattr(error_capture, "MEMORY_DIR", mem_dir)

        result = _find_recent_error("git", "sess-abc")
        assert result is None


class TestMainErrorCapture:
    def _run_main(self, monkeypatch, tmp_path, input_data):
        """Helper: mock stdin, paths, et execute main(). Retourne memory dir."""
        mem_dir = tmp_path / "memory"
        mem_dir.mkdir(parents=True, exist_ok=True)
        logs_dir = tmp_path / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        import error_capture
        from lib import paths as paths_mod
        monkeypatch.setattr(error_capture, "MEMORY_DIR", mem_dir)
        monkeypatch.setattr(paths_mod, "LOGS_DIR", logs_dir)

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

        return mem_dir

    def test_error_nonzero_exit_code(self, monkeypatch, tmp_path):
        """Erreur detectee avec exit_code != 0 -> ecrit dans errors.jsonl."""
        input_data = {
            "session_id": "sess-001",
            "tool_input": {"command": "git push origin main"},
            "tool_result": {
                "stdout": "",
                "stderr": "rejected",
                "exit_code": 1,
            },
        }
        mem_dir = self._run_main(monkeypatch, tmp_path, input_data)
        errors_file = mem_dir / "errors.jsonl"
        assert errors_file.exists()

        lines = errors_file.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 1
        entry = json.loads(lines[0])
        assert entry["error_type"] == "exit_code_1"
        assert entry["session_id"] == "sess-001"
        assert "git push" in entry["command"]

    def test_error_stderr_keywords(self, monkeypatch, tmp_path):
        """Erreur detectee via keyword dans stderr (exit_code absent)."""
        input_data = {
            "session_id": "sess-002",
            "tool_input": {"command": "python script.py"},
            "tool_result": {
                "stdout": "",
                "stderr": "Traceback (most recent call last):\n  File ...",
                "exit_code": None,
            },
        }
        mem_dir = self._run_main(monkeypatch, tmp_path, input_data)
        errors_file = mem_dir / "errors.jsonl"
        assert errors_file.exists()

        entry = json.loads(errors_file.read_text(encoding="utf-8").strip())
        assert entry["error_type"] == "stderr_error"

    def test_stderr_fatal_keyword(self, monkeypatch, tmp_path):
        """Le mot 'fatal' dans stderr declenche la detection."""
        input_data = {
            "session_id": "sess-003",
            "tool_input": {"command": "git clone bad-url"},
            "tool_result": {
                "stdout": "",
                "stderr": "fatal: repository 'bad-url' not found",
                "exit_code": None,
            },
        }
        mem_dir = self._run_main(monkeypatch, tmp_path, input_data)
        errors_file = mem_dir / "errors.jsonl"
        assert errors_file.exists()

    def test_stderr_permission_denied(self, monkeypatch, tmp_path):
        """Le mot 'permission denied' dans stderr declenche la detection."""
        input_data = {
            "session_id": "sess-004",
            "tool_input": {"command": "cat /etc/shadow"},
            "tool_result": {
                "stdout": "",
                "stderr": "cat: /etc/shadow: Permission denied",
                "exit_code": None,
            },
        }
        mem_dir = self._run_main(monkeypatch, tmp_path, input_data)
        errors_file = mem_dir / "errors.jsonl"
        assert errors_file.exists()

    def test_successful_command_no_error(self, monkeypatch, tmp_path):
        """Commande reussie (exit 0, pas d'erreur) -> pas d'errors.jsonl."""
        input_data = {
            "session_id": "sess-005",
            "tool_input": {"command": "echo hello"},
            "tool_result": {
                "stdout": "hello",
                "stderr": "",
                "exit_code": 0,
            },
        }
        mem_dir = self._run_main(monkeypatch, tmp_path, input_data)
        errors_file = mem_dir / "errors.jsonl"
        # Pas d'erreur enregistree
        if errors_file.exists():
            content = errors_file.read_text(encoding="utf-8").strip()
            assert content == ""

    def test_correction_detected(self, monkeypatch, tmp_path):
        """Commande reussie apres erreur recente = correction detectee."""
        mem_dir = tmp_path / "memory"
        mem_dir.mkdir(parents=True, exist_ok=True)
        logs_dir = tmp_path / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Pre-remplir errors.jsonl avec une erreur git
        error_entry = {
            "timestamp": "2026-02-12T10:00:00+01:00",
            "session_id": "sess-fix",
            "command": "git push origin main",
            "error_type": "exit_code_1",
            "exit_code": 1,
            "stderr_preview": "rejected",
        }
        errors_file = mem_dir / "errors.jsonl"
        errors_file.write_text(json.dumps(error_entry) + "\n", encoding="utf-8")

        # Commande reussie avec le meme base command (git)
        input_data = {
            "session_id": "sess-fix",
            "tool_input": {"command": "git push --force origin main"},
            "tool_result": {
                "stdout": "Everything up-to-date",
                "stderr": "",
                "exit_code": 0,
            },
        }

        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        import error_capture
        from lib import paths as paths_mod
        monkeypatch.setattr(error_capture, "MEMORY_DIR", mem_dir)
        monkeypatch.setattr(paths_mod, "LOGS_DIR", logs_dir)

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

        corrections_file = mem_dir / "corrections.jsonl"
        assert corrections_file.exists()
        correction = json.loads(corrections_file.read_text(encoding="utf-8").strip())
        assert correction["session_id"] == "sess-fix"
        assert "git push" in correction["error_command"]
        assert "git push --force" in correction["fix_command"]

    def test_no_correction_different_base_command(self, monkeypatch, tmp_path):
        """Pas de correction si la commande de base differe."""
        mem_dir = tmp_path / "memory"
        mem_dir.mkdir(parents=True, exist_ok=True)
        logs_dir = tmp_path / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Erreur npm
        error_entry = {
            "timestamp": "2026-02-12T10:00:00+01:00",
            "session_id": "sess-diff",
            "command": "npm install broken-pkg",
            "error_type": "exit_code_1",
            "exit_code": 1,
            "stderr_preview": "not found",
        }
        errors_file = mem_dir / "errors.jsonl"
        errors_file.write_text(json.dumps(error_entry) + "\n", encoding="utf-8")

        # Commande git reussie (base command differente)
        input_data = {
            "session_id": "sess-diff",
            "tool_input": {"command": "git status"},
            "tool_result": {
                "stdout": "On branch main",
                "stderr": "",
                "exit_code": 0,
            },
        }

        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        import error_capture
        from lib import paths as paths_mod
        monkeypatch.setattr(error_capture, "MEMORY_DIR", mem_dir)
        monkeypatch.setattr(paths_mod, "LOGS_DIR", logs_dir)

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

        corrections_file = mem_dir / "corrections.jsonl"
        if corrections_file.exists():
            content = corrections_file.read_text(encoding="utf-8").strip()
            assert content == ""

    def test_empty_command_exits_early(self, monkeypatch, tmp_path):
        """Commande vide -> exit 0 immediatement, rien ecrit."""
        input_data = {
            "session_id": "sess-empty",
            "tool_input": {"command": ""},
            "tool_result": {},
        }
        mem_dir = self._run_main(monkeypatch, tmp_path, input_data)
        errors_file = mem_dir / "errors.jsonl"
        corrections_file = mem_dir / "corrections.jsonl"
        # Rien ne doit etre ecrit
        assert not errors_file.exists() or errors_file.read_text(encoding="utf-8").strip() == ""
        assert not corrections_file.exists()

    def test_fail_open_always_exits_zero(self, monkeypatch, tmp_path):
        """Meme avec des donnees invalides, le hook exit 0 (fail-open)."""
        # stdin invalide (pas du JSON)
        monkeypatch.setattr("sys.stdin", StringIO("not json at all"))

        logs_dir = tmp_path / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        from lib import paths as paths_mod
        monkeypatch.setattr(paths_mod, "LOGS_DIR", logs_dir)

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_fail_open_missing_tool_result(self, monkeypatch, tmp_path):
        """Donnees partielles (tool_result absent) -> exit 0."""
        input_data = {
            "session_id": "sess-partial",
            "tool_input": {"command": "ls"},
        }
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        mem_dir = tmp_path / "memory"
        mem_dir.mkdir(parents=True, exist_ok=True)
        logs_dir = tmp_path / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        import error_capture
        from lib import paths as paths_mod
        monkeypatch.setattr(error_capture, "MEMORY_DIR", mem_dir)
        monkeypatch.setattr(paths_mod, "LOGS_DIR", logs_dir)

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_errors_jsonl_created_with_valid_json(self, monkeypatch, tmp_path):
        """Verifie que le fichier errors.jsonl contient du JSON valide."""
        input_data = {
            "session_id": "sess-json",
            "tool_input": {"command": "make build"},
            "tool_result": {
                "stdout": "",
                "stderr": "Error: missing target",
                "exit_code": 2,
            },
        }
        mem_dir = self._run_main(monkeypatch, tmp_path, input_data)
        errors_file = mem_dir / "errors.jsonl"
        assert errors_file.exists()

        for line in errors_file.read_text(encoding="utf-8").strip().split("\n"):
            entry = json.loads(line)  # Doit pas lever d'exception
            assert "timestamp" in entry
            assert "session_id" in entry
            assert "command" in entry
            assert "error_type" in entry
