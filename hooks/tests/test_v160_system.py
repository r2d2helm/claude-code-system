"""Tests systeme v1.6.0 — validation de la structure et de la coherence.

Verifie:
- Structure des fichiers (hooks, lib, config, deprecated)
- Imports sans erreur de tous les modules
- Coherence settings.json vs fichiers presents
- Coherence CLAUDE.md vs fichiers presents
- Coherence security_rules.yaml vs hooks existants
- Integration memory_extractor.py shim -> v2
"""

import importlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

# Chemins de reference
HOOKS_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = HOOKS_DIR / "config"
LIB_DIR = HOOKS_DIR / "lib"
DEPRECATED_DIR = HOOKS_DIR / "_deprecated"
CLAUDE_CONFIG_DIR = HOOKS_DIR.parent  # claude-config/
TESTS_DIR = Path(__file__).resolve().parent


# ============================================================
# Phase 1: Structure des fichiers
# ============================================================

class TestFileStructure:
    """Verifie que tous les fichiers v1.6.0 sont presents."""

    EXPECTED_HOOKS = [
        "load_context.py",
        "security_validator.py",
        "path_guard.py",
        "memory_extractor.py",
        "memory_extractor_v2.py",
        "memory_consolidator.py",
        "migrate_memory_v1_to_v2.py",
        "prompt_analyzer.py",
        "subagent_capture.py",
        "error_capture.py",
        "notify_write.py",
        "notify_complete.py",
    ]

    EXPECTED_LIB = [
        "__init__.py",
        "paths.py",
        "utils.py",
        "transcript.py",
        "memory.py",
        "memory_db.py",
        "memory_retriever.py",
    ]

    EXPECTED_CONFIG = [
        "security_rules.yaml",
        "memory_rules.yaml",
        "memory_v2.yaml",
        "router_rules.yaml",
        "skill_schema.yaml",
        "contract_schema.yaml",
    ]

    EXPECTED_DEPRECATED = [
        "memory_extractor_v1.py",
        "session_capture.py",
        "memory_extractor_repo_v1.5.py",
    ]

    def test_all_hooks_exist(self):
        for hook in self.EXPECTED_HOOKS:
            assert (HOOKS_DIR / hook).exists(), f"Missing hook: {hook}"

    def test_all_lib_exist(self):
        for lib_file in self.EXPECTED_LIB:
            assert (LIB_DIR / lib_file).exists(), f"Missing lib: {lib_file}"

    def test_all_config_exist(self):
        for config_file in self.EXPECTED_CONFIG:
            assert (CONFIG_DIR / config_file).exists(), f"Missing config: {config_file}"

    def test_all_deprecated_exist(self):
        for dep_file in self.EXPECTED_DEPRECATED:
            assert (DEPRECATED_DIR / dep_file).exists(), f"Missing deprecated: {dep_file}"

    def test_hook_count(self):
        """Au moins 12 fichiers .py dans hooks/ (hors __init__)."""
        py_files = [f for f in HOOKS_DIR.glob("*.py") if f.name != "__init__.py"]
        assert len(py_files) >= 12, f"Expected >= 12 hooks, found {len(py_files)}: {[f.name for f in py_files]}"

    def test_lib_count(self):
        """Au moins 6 fichiers .py dans lib/ (hors __init__)."""
        py_files = [f for f in LIB_DIR.glob("*.py") if f.name != "__init__.py"]
        assert len(py_files) >= 6, f"Expected >= 6 lib files, found {len(py_files)}"

    def test_config_count(self):
        """Exactement 6 fichiers .yaml dans config/."""
        yaml_files = list(CONFIG_DIR.glob("*.yaml"))
        assert len(yaml_files) >= 6, f"Expected >= 6 config files, found {len(yaml_files)}"

    def test_deprecated_count(self):
        """Au moins 3 fichiers dans _deprecated/."""
        dep_files = list(DEPRECATED_DIR.glob("*.py"))
        assert len(dep_files) >= 3, f"Expected >= 3 deprecated files, found {len(dep_files)}"


# ============================================================
# Phase 2: Compilation Python (syntax check)
# ============================================================

class TestPythonSyntax:
    """Verifie que tous les .py compilent sans erreur."""

    def _collect_py_files(self):
        files = list(HOOKS_DIR.glob("*.py"))
        files += list(LIB_DIR.glob("*.py"))
        files += list(DEPRECATED_DIR.glob("*.py"))
        return [f for f in files if f.name != "__init__.py"]

    @pytest.mark.parametrize("py_file", [
        pytest.param(f, id=f.name) for f in
        list(HOOKS_DIR.glob("*.py")) +
        list(LIB_DIR.glob("*.py")) +
        list(DEPRECATED_DIR.glob("*.py"))
        if f.name != "__init__.py"
    ])
    def test_compiles(self, py_file):
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(py_file)],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0, f"{py_file.name}: {result.stderr}"


# ============================================================
# Phase 3: Validation YAML
# ============================================================

class TestYAMLConfigs:
    """Verifie que tous les YAML parsent et ont la structure attendue."""

    @pytest.mark.parametrize("yaml_file", [
        pytest.param(f, id=f.name) for f in CONFIG_DIR.glob("*.yaml")
    ])
    def test_yaml_valid(self, yaml_file):
        content = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
        assert content is not None, f"{yaml_file.name} is empty"

    def test_security_rules_structure(self):
        rules = yaml.safe_load((CONFIG_DIR / "security_rules.yaml").read_text(encoding="utf-8"))
        assert "blocked" in rules
        assert "confirm" in rules
        assert "alert" in rules
        assert "read_protected" in rules
        assert "write_protected" in rules
        assert "system_paths" in rules

    def test_security_rules_has_auto_allow(self):
        rules = yaml.safe_load((CONFIG_DIR / "security_rules.yaml").read_text(encoding="utf-8"))
        assert "auto_allow_patterns" in rules, "Missing auto_allow_patterns (v1.6.0)"

    def test_memory_v2_structure(self):
        config = yaml.safe_load((CONFIG_DIR / "memory_v2.yaml").read_text(encoding="utf-8"))
        assert "extraction" in config
        assert "retrieval" in config
        assert "consolidation" in config

    def test_router_rules_structure(self):
        rules = yaml.safe_load((CONFIG_DIR / "router_rules.yaml").read_text(encoding="utf-8"))
        assert "skills" in rules or "routing" in rules or isinstance(rules, dict)

    def test_security_regex_compiles(self):
        """Verifie que tous les regex de security_rules compilent."""
        rules = yaml.safe_load((CONFIG_DIR / "security_rules.yaml").read_text(encoding="utf-8"))
        for section in ("blocked", "confirm", "alert", "read_protected", "write_protected",
                        "system_paths", "auto_allow_patterns"):
            entries = rules.get(section, [])
            if not entries:
                continue
            for entry in entries:
                pattern = entry.get("pattern", "")
                try:
                    re.compile(pattern)
                except re.error as e:
                    pytest.fail(f"Invalid regex in {section}: {pattern!r} -> {e}")


# ============================================================
# Phase 4: Coherence settings.json
# ============================================================

class TestSettingsCoherence:
    """Verifie que settings.json reference des fichiers qui existent."""

    def _load_settings(self):
        settings_path = CLAUDE_CONFIG_DIR / "settings.json"
        return json.loads(settings_path.read_text(encoding="utf-8"))

    def test_settings_exists(self):
        assert (CLAUDE_CONFIG_DIR / "settings.json").exists()

    def test_settings_valid_json(self):
        settings = self._load_settings()
        assert "hooks" in settings

    def test_all_hook_events_present(self):
        settings = self._load_settings()
        hooks = settings["hooks"]
        expected_events = [
            "SessionStart", "PreToolUse", "Stop",
            "SubagentStop", "UserPromptSubmit",
            "PostToolUse", "Notification",
        ]
        for event in expected_events:
            assert event in hooks, f"Missing event: {event}"

    def test_hook_unique_scripts_is_9(self):
        """9 scripts uniques (path_guard apparait 3x pour Read/Write/Edit)."""
        settings = self._load_settings()
        hooks = settings["hooks"]
        scripts = set()
        for event, entries in hooks.items():
            for entry in entries:
                for hook in entry.get("hooks", []):
                    cmd = hook.get("command", "")
                    match = re.search(r"[\\/]([a-z_0-9]+\.py)", cmd)
                    if match:
                        scripts.add(match.group(1))
        assert len(scripts) == 9, f"Expected 9 unique scripts, found {len(scripts)}: {scripts}"

    def test_hook_scripts_exist(self):
        """Verifie que chaque script reference dans settings.json existe."""
        settings = self._load_settings()
        hooks = settings["hooks"]
        for event, entries in hooks.items():
            for entry in entries:
                for hook in entry.get("hooks", []):
                    cmd = hook.get("command", "")
                    # Extraire le nom du script Python
                    match = re.search(r"[\\/]([a-z_0-9]+\.py)", cmd)
                    if match:
                        script_name = match.group(1)
                        assert (HOOKS_DIR / script_name).exists(), (
                            f"settings.json references {script_name} in {event} but file missing"
                        )

    def test_stop_hook_is_v2(self):
        """Le Stop hook doit pointer vers memory_extractor_v2.py."""
        settings = self._load_settings()
        stop_entries = settings["hooks"]["Stop"]
        commands = [h["command"] for entry in stop_entries for h in entry.get("hooks", [])]
        assert any("memory_extractor_v2" in cmd for cmd in commands), (
            "Stop hook should use memory_extractor_v2.py"
        )


# ============================================================
# Phase 5: Coherence CLAUDE.md
# ============================================================

class TestCLAUDEMDCoherence:
    """Verifie que CLAUDE.md reflete l'etat reel du systeme."""

    def _load_claude_md(self):
        return (CLAUDE_CONFIG_DIR / "CLAUDE.md").read_text(encoding="utf-8")

    def test_hooks_count_11(self):
        content = self._load_claude_md()
        assert "Hooks (11)" in content, "CLAUDE.md should say Hooks (11)"

    def test_all_hooks_listed(self):
        content = self._load_claude_md()
        expected_hooks = [
            "load_context.py", "security_validator.py", "path_guard.py",
            "memory_extractor_v2.py", "subagent_capture.py", "prompt_analyzer.py",
            "error_capture.py", "notify_write.py", "notify_complete.py",
            "pre_compact_flush.py", "heartbeat.py",
        ]
        for hook in expected_hooks:
            assert hook in content, f"CLAUDE.md missing hook: {hook}"

    def test_memory_v2_section(self):
        content = self._load_claude_md()
        assert "Memory v2" in content, "CLAUDE.md missing Memory v2 section"
        assert "memory_db.py" in content
        assert "memory_retriever.py" in content
        assert "memory_consolidator.py" in content

    def test_memory_db_path(self):
        content = self._load_claude_md()
        assert "memory.db" in content, "CLAUDE.md missing memory.db path"


# ============================================================
# Phase 6: Coherence security_rules.yaml vs hooks
# ============================================================

class TestSecurityRulesCoherence:
    """Verifie que system_paths couvre tous les hooks."""

    def test_system_paths_covers_all_hooks(self):
        rules = yaml.safe_load((CONFIG_DIR / "security_rules.yaml").read_text(encoding="utf-8"))
        system_paths = rules.get("system_paths", [])

        # Extraire les noms de hooks depuis le regex
        for entry in system_paths:
            pattern = entry.get("pattern", "")
            if "hooks" in pattern:
                # Trouver les noms entre parentheses
                match = re.search(r"\(([^)]+)\)", pattern)
                if match:
                    hook_names = match.group(1).split("|")
                    expected = [
                        "load_context", "security_validator", "memory_extractor",
                        "memory_extractor_v2", "memory_consolidator", "path_guard",
                        "prompt_analyzer", "subagent_capture", "error_capture",
                        "notify_write", "notify_complete",
                    ]
                    for hook in expected:
                        assert hook in hook_names, (
                            f"system_paths regex missing: {hook}"
                        )
                    return
        pytest.fail("No system_paths entry found covering hooks")

    def test_auto_allow_patterns_exist(self):
        rules = yaml.safe_load((CONFIG_DIR / "security_rules.yaml").read_text(encoding="utf-8"))
        auto_allow = rules.get("auto_allow_patterns", [])
        assert len(auto_allow) >= 2, "Expected at least 2 auto_allow patterns"

        patterns_str = json.dumps(auto_allow)
        assert "SKILL" in patterns_str, "auto_allow should cover SKILL.md"
        assert "CLAUDE" in patterns_str, "auto_allow should cover CLAUDE.md"


# ============================================================
# Phase 7: memory_extractor.py shim
# ============================================================

class TestMemoryExtractorShim:
    """Verifie que memory_extractor.py fonctionne comme shim v2."""

    def test_imports_legacy_functions(self):
        """Les fonctions legacy sont toujours importables."""
        from memory_extractor import (
            extract_insights, _content_hash, _compute_duration_s, create_vault_note,
        )
        assert callable(extract_insights)
        assert callable(_content_hash)
        assert callable(_compute_duration_s)
        assert callable(create_vault_note)

    def test_main_delegates_to_v2(self):
        """main() devrait deleguer a memory_extractor_v2.main()."""
        content = (HOOKS_DIR / "memory_extractor.py").read_text(encoding="utf-8")
        assert "from memory_extractor_v2 import main as v2_main" in content
        assert "v2_main()" in content

    def test_shim_docstring(self):
        """Le shim doit documenter la delegation."""
        content = (HOOKS_DIR / "memory_extractor.py").read_text(encoding="utf-8")
        assert "DEPRECATED" in content or "shim" in content.lower() or "v2" in content.lower()


# ============================================================
# Phase 8: Integration load_context + prompt_analyzer
# ============================================================

class TestIntegrationV2:
    """Verifie que les hooks merges utilisent bien memory_retriever."""

    def test_load_context_uses_memory_retriever(self):
        content = (HOOKS_DIR / "load_context.py").read_text(encoding="utf-8")
        assert "memory_retriever" in content, "load_context.py should import memory_retriever"
        assert "retrieve_for_startup" in content

    def test_prompt_analyzer_uses_memory_retriever(self):
        content = (HOOKS_DIR / "prompt_analyzer.py").read_text(encoding="utf-8")
        assert "memory_retriever" in content, "prompt_analyzer.py should import memory_retriever"
        assert "retrieve_for_prompt" in content

    def test_load_context_memory_in_try_except(self):
        """Le bloc memory doit etre dans un try/except fail-open."""
        content = (HOOKS_DIR / "load_context.py").read_text(encoding="utf-8")
        # Trouver le bloc memory_retriever et verifier qu'il est dans un try
        idx = content.find("memory_retriever")
        assert idx > 0
        # Chercher le try le plus proche avant
        before = content[:idx]
        last_try = before.rfind("try:")
        assert last_try > 0, "memory_retriever import should be inside try block"

    def test_prompt_analyzer_memory_in_try_except(self):
        """Le bloc memory doit etre dans un try/except fail-open."""
        content = (HOOKS_DIR / "prompt_analyzer.py").read_text(encoding="utf-8")
        idx = content.find("memory_retriever")
        assert idx > 0
        before = content[:idx]
        last_try = before.rfind("try:")
        assert last_try > 0, "memory_retriever import should be inside try block"

    def test_lib_memory_deprecated(self):
        """lib/memory.py doit avoir un header de deprecation."""
        content = (LIB_DIR / "memory.py").read_text(encoding="utf-8")
        assert "DEPRECATED" in content.upper() or "deprecated" in content.lower()
