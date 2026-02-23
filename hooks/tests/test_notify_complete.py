"""Tests pour notify_complete.py — notification OS de fin de tache."""

import json
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

import pytest

from notify_complete import main, notify


class TestNotify:
    def test_linux_uses_notify_send(self, monkeypatch):
        """Sur Linux, notify-send est appele."""
        monkeypatch.setattr("os.name", "posix")
        monkeypatch.setattr("sys.platform", "linux")

        with patch("notify_complete.subprocess.run") as mock_run:
            notify("Claude Code", "Session abc terminee")
            mock_run.assert_called_once()
            args = mock_run.call_args
            cmd = args[0][0]  # Premier argument positionnel = la liste de commandes
            assert cmd[0] == "notify-send"
            assert cmd[1] == "Claude Code"
            assert "abc" in cmd[2]

    def test_macos_uses_osascript(self, monkeypatch):
        """Sur macOS, osascript est appele."""
        monkeypatch.setattr("os.name", "posix")
        monkeypatch.setattr("sys.platform", "darwin")

        with patch("notify_complete.subprocess.run") as mock_run:
            notify("Claude Code", "Done")
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert cmd[0] == "osascript"

    def test_windows_uses_powershell(self, monkeypatch):
        """Sur Windows, powershell est appele."""
        monkeypatch.setattr("os.name", "nt")
        monkeypatch.setattr("sys.platform", "win32")

        with patch("notify_complete.subprocess.run") as mock_run:
            notify("Claude Code", "Done")
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert cmd[0] == "powershell"

    def test_fallback_on_exception(self, monkeypatch, capsys):
        """Si subprocess echoue, fallback sur stderr."""
        monkeypatch.setattr("os.name", "posix")
        monkeypatch.setattr("sys.platform", "linux")

        with patch("notify_complete.subprocess.run", side_effect=FileNotFoundError("notify-send not found")):
            notify("Claude Code", "Session done")

        captured = capsys.readouterr()
        assert "[hook] Claude Code: Session done" in captured.err

    def test_subprocess_timeout(self, monkeypatch):
        """subprocess.run est appele avec timeout=5."""
        monkeypatch.setattr("os.name", "posix")
        monkeypatch.setattr("sys.platform", "linux")

        with patch("notify_complete.subprocess.run") as mock_run:
            notify("Title", "Msg")
            kwargs = mock_run.call_args[1]
            assert kwargs.get("timeout") == 5
            assert kwargs.get("capture_output") is True


class TestMainNotifyComplete:
    def test_session_id_extracted(self, monkeypatch):
        """Le session_id est extrait du JSON stdin et utilise dans la notification."""
        input_data = {"session_id": "abcdef1234567890"}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with patch("notify_complete.notify") as mock_notify:
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

            mock_notify.assert_called_once()
            call_args = mock_notify.call_args[0]
            assert call_args[0] == "Claude Code"
            # Short ID = 8 premiers caracteres
            assert "abcdef12" in call_args[1]
            assert "terminee" in call_args[1]

    def test_short_session_id_formatting(self, monkeypatch):
        """Un session_id > 8 chars est tronque a 8."""
        input_data = {"session_id": "1234567890abcdef"}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with patch("notify_complete.notify") as mock_notify:
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

            message = mock_notify.call_args[0][1]
            assert "12345678" in message
            # Le session_id complet ne doit pas apparaitre
            assert "1234567890abcdef" not in message

    def test_short_session_id_kept_as_is(self, monkeypatch):
        """Un session_id <= 8 chars est garde tel quel."""
        input_data = {"session_id": "abc"}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with patch("notify_complete.notify") as mock_notify:
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

            message = mock_notify.call_args[0][1]
            assert "abc" in message
            assert "terminee" in message

    def test_empty_session_id_fallback(self, monkeypatch):
        """Session_id vide -> message fallback 'Task completed'."""
        input_data = {"session_id": ""}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with patch("notify_complete.notify") as mock_notify:
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

            message = mock_notify.call_args[0][1]
            assert message == "Task completed"

    def test_missing_session_id_fallback(self, monkeypatch):
        """Cle session_id absente -> message fallback 'Task completed'."""
        input_data = {}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with patch("notify_complete.notify") as mock_notify:
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

            message = mock_notify.call_args[0][1]
            assert message == "Task completed"

    def test_fail_open_invalid_json(self, monkeypatch):
        """JSON invalide -> fail-open, exit 0."""
        monkeypatch.setattr("sys.stdin", StringIO("{{invalid"))

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_fail_open_empty_stdin(self, monkeypatch):
        """Stdin vide -> fail-open, exit 0."""
        monkeypatch.setattr("sys.stdin", StringIO(""))

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_notify_called_with_correct_title(self, monkeypatch):
        """Le titre de la notification est toujours 'Claude Code'."""
        input_data = {"session_id": "test-session-id"}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(input_data)))

        with patch("notify_complete.notify") as mock_notify:
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

            title = mock_notify.call_args[0][0]
            assert title == "Claude Code"
