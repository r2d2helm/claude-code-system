"""Tests pour load_context.py — get_active_skills, count_vault_notes."""

from pathlib import Path

import pytest

from load_context import get_active_skills, count_vault_notes


class TestGetActiveSkills:
    def test_skills_from_skill_md(self, tmp_path, monkeypatch):
        import load_context
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        skill_md = skills_dir / "SKILL.md"
        skill_md.write_text(
            "| Skill | Description |\n"
            "|-------|-------------|\n"
            "| 🐳 docker-skill | Docker admin | Actif |\n"
            "| 🐧 linux-skill | Linux admin | Actif |\n"
            "| ⏳ future-skill | Not ready | Prevu |\n",
            encoding="utf-8",
        )
        monkeypatch.setattr(load_context, "SKILLS_DIR", skills_dir)
        result = get_active_skills()
        assert "docker-skill" in result
        assert "linux-skill" in result
        assert "future-skill" not in result

    def test_fallback_to_directories(self, tmp_path, monkeypatch):
        import load_context
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        # SKILL.md exists but has no "Actif" lines
        (skills_dir / "SKILL.md").write_text("# Meta-router\nNo table here.", encoding="utf-8")
        (skills_dir / "docker-skill").mkdir()
        (skills_dir / "linux-skill").mkdir()
        (skills_dir / "other-stuff").mkdir()  # doesn't end with -skill
        monkeypatch.setattr(load_context, "SKILLS_DIR", skills_dir)
        result = get_active_skills()
        assert "docker-skill" in result
        assert "linux-skill" in result
        assert "other-stuff" not in result

    def test_missing_skill_md(self, tmp_path, monkeypatch):
        import load_context
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        # No SKILL.md file at all
        monkeypatch.setattr(load_context, "SKILLS_DIR", skills_dir)
        result = get_active_skills()
        assert result == []

    def test_nonexistent_dir(self, tmp_path, monkeypatch):
        import load_context
        monkeypatch.setattr(load_context, "SKILLS_DIR", tmp_path / "nonexistent")
        result = get_active_skills()
        assert result == []


class TestCountVaultNotes:
    def test_counts_md_files(self, tmp_vault, monkeypatch):
        import load_context
        monkeypatch.setattr(load_context, "VAULT_PATH", tmp_vault)
        count = count_vault_notes()
        # tmp_vault has 3 .md files (C_Test.md, C_Python.md, 2026-02-11.md)
        assert count == 3

    def test_empty_vault(self, tmp_path, monkeypatch):
        import load_context
        vault = tmp_path / "vault"
        vault.mkdir()
        monkeypatch.setattr(load_context, "VAULT_PATH", vault)
        count = count_vault_notes()
        assert count == 0

    def test_missing_vault(self, tmp_path, monkeypatch):
        import load_context
        monkeypatch.setattr(load_context, "VAULT_PATH", tmp_path / "nonexistent")
        count = count_vault_notes()
        assert count == 0
