"""Tests pour path_guard.py — read_protected/write_protected/system_paths."""

import pytest

from path_guard import load_path_rules, validate_path


class TestLoadPathRules:
    def test_load_rules_from_yaml(self, sample_security_rules, monkeypatch):
        import path_guard
        monkeypatch.setattr(path_guard, "CONFIG_DIR", sample_security_rules.parent)
        # Reset cached rules
        path_guard._compiled_rules = None
        rules = load_path_rules()
        assert "read_protected" in rules
        assert "write_protected" in rules
        assert "system_paths" in rules
        assert len(rules["read_protected"]) >= 2

    def test_load_rules_missing_file(self, tmp_path, monkeypatch):
        import path_guard
        monkeypatch.setattr(path_guard, "CONFIG_DIR", tmp_path / "nonexistent")
        path_guard._compiled_rules = None
        rules = load_path_rules()
        assert rules == {"read_protected": [], "write_protected": [], "system_paths": []}


class TestValidatePath:
    @pytest.fixture(autouse=True)
    def _setup_rules(self, sample_security_rules, monkeypatch):
        import path_guard
        monkeypatch.setattr(path_guard, "CONFIG_DIR", sample_security_rules.parent)
        path_guard._compiled_rules = None

    # --- Read protected ---
    def test_read_credentials_blocked(self):
        cat, reason, _ = validate_path("Read", "C:/Users/test/.credentials.json")
        assert cat == "blocked"
        assert "credentials" in reason.lower()

    def test_read_env_blocked(self):
        cat, _, _ = validate_path("Read", "C:/project/.env")
        assert cat == "blocked"

    def test_read_ssh_key_blocked(self):
        cat, _, _ = validate_path("Read", "C:/Users/test/.ssh/id_rsa")
        assert cat == "blocked"

    def test_read_normal_file_allowed(self):
        cat, _, _ = validate_path("Read", "C:/Users/test/foo.md")
        assert cat == "allow"

    # --- Write protected ---
    def test_write_templates_confirm(self):
        cat, _, _ = validate_path("Write", "C:/vault/_Templates/Template-Concept.md")
        assert cat == "confirm"

    def test_write_agents_confirm(self):
        cat, _, _ = validate_path("Edit", "C:/Users/test/.claude/agents/builder.md")
        assert cat == "confirm"

    # --- System paths ---
    def test_write_claude_md_confirm(self):
        cat, _, _ = validate_path("Write", "C:/Users/test/.claude/CLAUDE.md")
        assert cat == "confirm"

    def test_write_skill_md_confirm(self):
        cat, _, _ = validate_path("Edit", "C:/Users/test/.claude/skills/SKILL.md")
        assert cat == "confirm"

    def test_write_normal_file_allowed(self):
        cat, _, _ = validate_path("Write", "C:/Users/test/project/foo.py")
        assert cat == "allow"

    # --- Read does not check write_protected ---
    def test_read_templates_allowed(self):
        """Read should NOT block write_protected paths."""
        cat, _, _ = validate_path("Read", "C:/vault/_Templates/Template.md")
        assert cat == "allow"

    def test_read_claude_md_allowed(self):
        """Read should NOT block system_paths (only write/edit does)."""
        cat, _, _ = validate_path("Read", "C:/Users/test/.claude/CLAUDE.md")
        assert cat == "allow"
