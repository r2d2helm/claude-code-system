"""Fixtures partagees pour les tests des hooks Claude Code."""

import json
import sys
from io import StringIO
from pathlib import Path

import pytest

# Ajouter le dossier hooks au path pour les imports
HOOKS_DIR = Path(__file__).resolve().parent.parent
if str(HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(HOOKS_DIR))


@pytest.fixture
def mock_stdin(monkeypatch):
    """Retourne une fonction pour mocker stdin avec du JSON."""
    def _mock(data: dict):
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(data)))
    return _mock


@pytest.fixture
def tmp_logs(tmp_path):
    """Cree un dossier logs temporaire."""
    logs = tmp_path / "logs"
    logs.mkdir()
    return logs


@pytest.fixture
def tmp_vault(tmp_path):
    """Cree un mini-vault Obsidian pour tests."""
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "_Inbox").mkdir()
    (vault / "Concepts").mkdir()
    (vault / "_Daily").mkdir()

    (vault / "Concepts" / "C_Test.md").write_text(
        "---\ntitle: Test\ndate: 2026-02-11\ntype: concept\n"
        "status: seedling\ntags:\n  - test\n---\n\n# Test\n\nContenu test.\n",
        encoding="utf-8",
    )
    (vault / "Concepts" / "C_Python.md").write_text(
        "---\ntitle: Python\ndate: 2026-02-11\ntype: concept\n"
        "status: growing\ntags:\n  - dev/python\n---\n\n# Python\n\n[[C_Test]]\n",
        encoding="utf-8",
    )
    (vault / "_Daily" / "2026-02-11.md").write_text(
        "---\ntitle: 2026-02-11\ndate: 2026-02-11\ntype: daily\n"
        "status: evergreen\ntags:\n  - daily\n---\n\n# 2026-02-11\n",
        encoding="utf-8",
    )
    return vault


@pytest.fixture
def sample_transcript(tmp_path):
    """Cree un transcript JSONL realiste."""
    transcript = tmp_path / "transcript.jsonl"
    entries = [
        {
            "type": "assistant",
            "timestamp": "2026-02-11T10:00:00Z",
            "message": {"content": [
                {"type": "tool_use", "name": "Read", "input": {"file_path": "/foo.md"}},
            ]},
        },
        {
            "type": "assistant",
            "timestamp": "2026-02-11T10:01:00Z",
            "message": {"content": [
                {"type": "tool_use", "name": "Write", "input": {"file_path": "/bar.md"}},
                {"type": "tool_use", "name": "Bash", "input": {"command": "git status"}},
            ]},
        },
        {
            "type": "assistant",
            "timestamp": "2026-02-11T10:02:00Z",
            "message": {"content": [
                {"type": "text", "text": "The issue was a missing import statement in the module."},
            ]},
        },
        {
            "type": "assistant",
            "timestamp": "2026-02-11T10:03:00Z",
            "message": {"content": [
                {"type": "tool_use", "name": "Edit", "input": {"file_path": "/baz.py"}},
                {"type": "text", "text": "Fixed by adding the correct import at the top of the file."},
            ]},
        },
        {"type": "tool_result", "content": "Error: file not found"},
    ]
    with open(transcript, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
    return transcript


@pytest.fixture
def sample_security_rules(tmp_path):
    """Cree un fichier security_rules.yaml minimal pour tests."""
    rules = tmp_path / "security_rules.yaml"
    rules.write_text(
        'blocked:\n'
        '  - pattern: "rm\\\\s+-rf\\\\s+/"\n'
        '    reason: "Suppression recursive racine"\n'
        '  - pattern: "format\\\\s+[a-zA-Z]:"\n'
        '    reason: "Formatage disque"\n'
        '  - pattern: "curl\\\\s+.*\\\\|\\\\s*bash"\n'
        '    reason: "Script distant"\n'
        'confirm:\n'
        '  - pattern: "git\\\\s+push.*--force"\n'
        '    reason: "Force push"\n'
        '  - pattern: "DROP\\\\s+TABLE"\n'
        '    reason: "Drop table"\n'
        'alert:\n'
        '  - pattern: "pip\\\\s+install"\n'
        '    reason: "Installation package"\n'
        'read_protected:\n'
        '  - pattern: "\\\\.credentials\\\\.json$"\n'
        '    reason: "Credentials"\n'
        '  - pattern: "\\\\.env$"\n'
        '    reason: "Env file"\n'
        '  - pattern: "id_rsa"\n'
        '    reason: "SSH key"\n'
        'write_protected:\n'
        '  - pattern: "_Templates"\n'
        '    reason: "Templates proteges"\n'
        '  - pattern: "\\\\.claude[\\\\\\\\/]agents[\\\\\\\\/]"\n'
        '    reason: "Agents proteges"\n'
        'system_paths:\n'
        '  - pattern: "CLAUDE\\\\.md$"\n'
        '    reason: "Fichier systeme"\n'
        '  - pattern: "SKILL\\\\.md$"\n'
        '    reason: "Meta-router"\n',
        encoding="utf-8",
    )
    return rules


@pytest.fixture
def patch_paths(monkeypatch, tmp_path, tmp_logs):
    """Remplace les constantes de paths.py avec des chemins temporaires."""
    from lib import paths as paths_mod

    monkeypatch.setattr(paths_mod, "LOGS_DIR", tmp_logs)
    monkeypatch.setattr(paths_mod, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(paths_mod, "MEMORY_DIR", tmp_path / "memory")
    monkeypatch.setattr(paths_mod, "VAULT_PATH", tmp_path / "vault")
    monkeypatch.setattr(paths_mod, "HOOKS_DIR", tmp_path)
    monkeypatch.setattr(paths_mod, "DATA_DIR", tmp_path / "data")
    (tmp_path / "memory").mkdir(exist_ok=True)
    (tmp_path / "vault" / "_Inbox").mkdir(parents=True, exist_ok=True)
