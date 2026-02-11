"""Constantes de chemins pour les hooks Claude Code."""

from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
HOOKS_DIR = CLAUDE_DIR / "hooks"
VAULT_PATH = Path.home() / "Documents" / "Knowledge"
SKILLS_DIR = CLAUDE_DIR / "skills"
LOGS_DIR = HOOKS_DIR / "logs"
CONFIG_DIR = HOOKS_DIR / "config"
