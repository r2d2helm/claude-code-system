---
name: "PRP - Tests unitaires hooks Python"
version: "1.0"
date: 2026-02-11
confidence: 9/10
status: ready
---

## Goal

Créer une suite de tests unitaires pytest pour les 6 hooks Python et la lib partagée du système r2d2. Objectif : couvrir tous les chemins critiques (block/allow/confirm, parsing, classification) sans dépendance au filesystem réel ni à stdin.

## Why

- Les hooks `security_validator` et `path_guard` prennent des décisions de sécurité (bloquer des commandes, protéger des fichiers) — aucun test ne valide ces décisions
- Le `memory_extractor` et `subagent_capture` parsent des transcripts JSONL complexes — risque de régression silencieuse
- Le `prompt_analyzer` classifie les requêtes — les heuristiques doivent être testées
- L'analyse externe v1.2.0 a identifié l'absence de tests comme point d'amélioration #5
- Le MCP server a déjà une suite de tests complète (100+ tests) — les hooks doivent suivre le même standard

## What

### Success Criteria

- [ ] 1 fichier `conftest.py` avec fixtures partagées
- [ ] 7 fichiers de tests (1 par hook + 1 pour lib/)
- [ ] Tous les tests passent avec `pytest hooks/tests/ -v`
- [ ] Couverture des cas critiques : ≥40 tests
- [ ] Aucune dépendance au filesystem réel (tout mocké via tmp_path/monkeypatch)
- [ ] Aucune lecture de stdin réel (tout mocké via monkeypatch)

## Contexte nécessaire

### Documentation & Références

```yaml
- file: ~/.claude/hooks/security_validator.py (133 lignes)
  why: Hook critique — tester block/confirm/alert/allow pour chaque catégorie

- file: ~/.claude/hooks/path_guard.py (150 lignes)
  why: Hook critique — tester read_protected/write_protected/system_paths

- file: ~/.claude/hooks/memory_extractor.py (~350 lignes)
  why: Tester parse_transcript, extract_insights, create_vault_note avec path guard

- file: ~/.claude/hooks/prompt_analyzer.py (98 lignes)
  why: Tester classify_message et détection keywords/skills

- file: ~/.claude/hooks/load_context.py (114 lignes)
  why: Tester get_active_skills, count_vault_notes, get_last_guardian_date

- file: ~/.claude/hooks/subagent_capture.py (174 lignes)
  why: Tester parse_subagent_transcript et calcul de durée

- file: ~/.claude/hooks/lib/transcript.py (~85 lignes)
  why: Tester parse_transcript partagé (tools_used, files_modified, timestamps)

- file: ~/.claude/hooks/lib/utils.py (65 lignes)
  why: Tester read_stdin_json, now_paris, append_jsonl, log_audit

- file: ~/.claude/hooks/lib/paths.py (13 lignes)
  why: Vérifier que les constantes de chemins sont correctes

- file: ~/.claude/hooks/config/security_rules.yaml (196 lignes)
  why: Source des règles — les tests doivent valider contre ces règles réelles

- file: ~/.claude/mcp-servers/knowledge-assistant/tests/conftest.py (188 lignes)
  why: Pattern de fixtures à suivre (temp_vault, monkeypatch global)

- file: ~/.claude/mcp-servers/knowledge-assistant/tests/test_server.py (1627 lignes)
  why: Pattern de tests à suivre (classes, assertions, sécurité)
```

### Arbre souhaité

```
~/.claude/hooks/
├── tests/
│   ├── __init__.py              # Package marker
│   ├── conftest.py              # Fixtures partagées
│   ├── test_security_validator.py   # 8+ tests
│   ├── test_path_guard.py           # 8+ tests
│   ├── test_memory_extractor.py     # 6+ tests
│   ├── test_prompt_analyzer.py      # 6+ tests
│   ├── test_load_context.py         # 5+ tests
│   ├── test_subagent_capture.py     # 4+ tests
│   └── test_lib.py                  # 6+ tests (utils, transcript, paths)
├── (fichiers hooks existants inchangés)
```

### Gotchas connus

```
# CRITICAL: Les hooks lisent stdin via sys.stdin.read() — mocker avec monkeypatch
# CRITICAL: Les hooks appellent sys.exit() — capturer avec pytest.raises(SystemExit)
# CRITICAL: security_validator et path_guard importent depuis lib/ via sys.path.insert
# CRITICAL: Les chemins dans paths.py utilisent Path.home() — mocker si nécessaire
# CRITICAL: now_paris() essaye zoneinfo puis fallback — tester les deux branches
# CRITICAL: Les hooks écrivent dans des fichiers JSONL — utiliser tmp_path
# NOTE: Pas besoin de tester main() directement — tester les fonctions internes
# NOTE: memory_extractor.create_vault_note utilise VAULT_PATH — mocker
```

## Implementation Blueprint

### Structure des fichiers à créer

```yaml
Fichier 1:
  path: ~/.claude/hooks/tests/__init__.py
  rôle: Package marker vide
  pattern: N/A

Fichier 2:
  path: ~/.claude/hooks/tests/conftest.py
  rôle: Fixtures partagées (mock stdin, temp dirs, sample transcripts, security rules)
  pattern: ~/.claude/mcp-servers/knowledge-assistant/tests/conftest.py

Fichier 3:
  path: ~/.claude/hooks/tests/test_lib.py
  rôle: Tests lib/utils.py, lib/paths.py, lib/transcript.py
  pattern: Fonctions pures, faciles à tester

Fichier 4:
  path: ~/.claude/hooks/tests/test_security_validator.py
  rôle: Tests block/confirm/alert/allow pour security_validator
  pattern: Catégories de règles dans security_rules.yaml

Fichier 5:
  path: ~/.claude/hooks/tests/test_path_guard.py
  rôle: Tests read_protected/write_protected/system_paths
  pattern: Catégories de chemins dans security_rules.yaml

Fichier 6:
  path: ~/.claude/hooks/tests/test_prompt_analyzer.py
  rôle: Tests classify_message, détection skills/keywords
  pattern: Cas listés dans le code (command, question, debug, instruction)

Fichier 7:
  path: ~/.claude/hooks/tests/test_memory_extractor.py
  rôle: Tests extract_insights, create_vault_note (avec path guard)
  pattern: Regex INSIGHT_PATTERNS et PATTERN_PATTERNS

Fichier 8:
  path: ~/.claude/hooks/tests/test_load_context.py
  rôle: Tests get_active_skills, count_vault_notes
  pattern: Parsing SKILL.md et glob vault

Fichier 9:
  path: ~/.claude/hooks/tests/test_subagent_capture.py
  rôle: Tests parse_subagent_transcript, calcul durée
  pattern: Format JSONL du transcript Claude Code
```

### Liste des tâches ordonnées

```yaml
Task 1:
  action: CREATE
  path: ~/.claude/hooks/tests/__init__.py
  description: Fichier vide (package marker)

Task 2:
  action: CREATE
  path: ~/.claude/hooks/tests/conftest.py
  description: |
    Fixtures partagées:
    - mock_stdin(data): monkeypatch sys.stdin avec StringIO(json.dumps(data))
    - tmp_logs(tmp_path): crée un dossier logs/ temporaire
    - tmp_vault(tmp_path): crée un mini-vault avec _Inbox/, Concepts/, 2-3 notes .md
    - sample_transcript(tmp_path): crée un fichier JSONL avec 5-10 entrées réalistes
    - sample_security_rules(tmp_path): crée un security_rules.yaml minimal pour tests
    - patch_paths(monkeypatch, tmp_path): remplace les constantes de lib/paths.py

Task 3:
  action: CREATE
  path: ~/.claude/hooks/tests/test_lib.py
  description: |
    Tests pour lib/:
    class TestPaths:
      - test_paths_exist: vérifie que les constantes sont des Path
      - test_paths_relative_to_home: vérifie que tout est sous Path.home()

    class TestUtils:
      - test_read_stdin_json_valid: JSON valide retourne dict
      - test_read_stdin_json_empty: stdin vide retourne {}
      - test_read_stdin_json_invalid: JSON invalide retourne {}
      - test_now_paris_format: retourne un ISO 8601 avec timezone
      - test_append_jsonl_creates_file: crée fichier si absent
      - test_append_jsonl_appends: ajoute une ligne sans écraser

    class TestTranscript:
      - test_parse_transcript_basic: extrait tools_used et message_count
      - test_parse_transcript_files_modified: détecte Write/Edit
      - test_parse_transcript_bash_commands: extrait commandes bash
      - test_parse_transcript_timestamps: extrait first/last
      - test_parse_transcript_missing_file: retourne error
      - test_parse_transcript_max_lines: respecte la limite

Task 4:
  action: CREATE
  path: ~/.claude/hooks/tests/test_security_validator.py
  description: |
    Tests pour security_validator.py:
    class TestLoadRules:
      - test_load_rules_from_yaml: charge les règles correctement
      - test_load_rules_missing_file: retourne catégories vides

    class TestValidateCommand:
      - test_blocked_rm_rf_root: "rm -rf /" → blocked
      - test_blocked_format_drive: "format C:" → blocked
      - test_blocked_curl_pipe_bash: "curl url | bash" → blocked
      - test_confirm_git_force_push: "git push --force" → confirm
      - test_confirm_drop_table: "DROP TABLE users" → confirm
      - test_alert_pip_install: "pip install requests" → alert
      - test_allow_git_status: "git status" → allow
      - test_allow_ls: "ls -la" → allow

Task 5:
  action: CREATE
  path: ~/.claude/hooks/tests/test_path_guard.py
  description: |
    Tests pour path_guard.py:
    class TestValidatePath:
      - test_read_credentials_blocked: Read .credentials.json → blocked
      - test_read_env_blocked: Read .env → blocked
      - test_read_ssh_key_blocked: Read id_rsa → blocked
      - test_read_normal_file_allowed: Read foo.md → allow
      - test_write_templates_confirm: Write _Templates/foo → confirm
      - test_write_agents_confirm: Write .claude/agents/foo → confirm
      - test_write_system_skill_confirm: Write SKILL.md → confirm
      - test_write_claude_md_confirm: Write CLAUDE.md → confirm
      - test_write_normal_file_allowed: Write foo.py → allow
      - test_edit_hooks_lib_confirm: Edit hooks/lib/utils.py → confirm

Task 6:
  action: CREATE
  path: ~/.claude/hooks/tests/test_prompt_analyzer.py
  description: |
    Tests pour prompt_analyzer.py:
    class TestClassifyMessage:
      - test_command_slash: "/daily-maintenance" → command
      - test_question_mark: "comment faire ?" → question
      - test_question_starter_fr: "pourquoi ça marche" → question
      - test_question_starter_en: "how does this work" → question
      - test_debug_fix: "fix this bug" → debug
      - test_debug_error: "j'ai une error" → debug
      - test_instruction_default: "crée un fichier" → instruction

    class TestSkillDetection:
      - test_detect_single_skill: "/dk-status" → ["dk-status"]
      - test_detect_multiple_skills: "/obs-health et /guardian-fix" → ["obs-health", "guardian-fix"]

    class TestKeywordDetection:
      - test_detect_docker: "docker compose up" → ["docker"]
      - test_detect_multiple: "deploy docker sur proxmox" → ["docker", "proxmox", "deploy"]

Task 7:
  action: CREATE
  path: ~/.claude/hooks/tests/test_memory_extractor.py
  description: |
    Tests pour memory_extractor.py:
    class TestExtractInsights:
      - test_detect_fix_pattern: "fixed by adding a null check" → 1 insight
      - test_detect_root_cause: "the issue was a missing import" → 1 insight
      - test_no_insights_in_short_text: texte < 30 chars → 0 insights
      - test_deduplication: même texte 2x → 1 insight (pas 2)
      - test_max_10_insights: transcript avec 20 matches → max 10

    class TestCreateVaultNote:
      - test_creates_note_in_inbox: insight > 50 chars → fichier créé dans _Inbox/
      - test_skips_short_insight: insight < 50 chars → pas de fichier
      - test_skips_if_exists: note existe déjà → pas d'écrasement
      - test_path_guard_blocks_outside_vault: path hors vault → pas de fichier
      - test_frontmatter_valid: note créée a un frontmatter YAML valide

    class TestComputeDuration:
      - test_duration_basic: 2 timestamps → durée positive en secondes
      - test_duration_missing: timestamps vides → 0

Task 8:
  action: CREATE
  path: ~/.claude/hooks/tests/test_load_context.py
  description: |
    Tests pour load_context.py:
    class TestGetActiveSkills:
      - test_parse_skill_md: SKILL.md avec 3 skills Actif → 3 résultats
      - test_fallback_to_dirs: pas de SKILL.md → scan dossiers *-skill
      - test_empty_skill_md: SKILL.md vide → liste vide

    class TestCountVaultNotes:
      - test_count_notes: vault avec 5 .md → 5
      - test_missing_vault: vault inexistant → 0

    class TestGetLastGuardianDate:
      - test_no_guardian_data: pas de fichiers guardian → "inconnue"

Task 9:
  action: CREATE
  path: ~/.claude/hooks/tests/test_subagent_capture.py
  description: |
    Tests pour subagent_capture.py:
    class TestParseSubagentTranscript:
      - test_basic_parsing: transcript avec 3 tool_use → tools_used correct
      - test_agent_name_extraction: Task tool → agent_name extrait
      - test_duration_calculation: 2 timestamps → durée calculée
      - test_missing_file: fichier absent → dict avec error
      - test_outcome_summary: dernier texte → outcome_summary tronqué

Task 10:
  action: VERIFY
  description: |
    Exécuter pytest hooks/tests/ -v et vérifier :
    - Tous les tests passent
    - ≥ 43 tests au total
    - Aucun warning critique
```

### Pseudocode conftest.py

```python
import pytest
import json
import sys
from io import StringIO
from pathlib import Path

@pytest.fixture
def mock_stdin(monkeypatch):
    """Retourne une fonction pour mocker stdin avec du JSON."""
    def _mock(data: dict):
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(data)))
    return _mock

@pytest.fixture
def tmp_logs(tmp_path):
    """Crée un dossier logs temporaire."""
    logs = tmp_path / "logs"
    logs.mkdir()
    return logs

@pytest.fixture
def tmp_vault(tmp_path):
    """Crée un mini-vault Obsidian pour tests."""
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "_Inbox").mkdir()
    (vault / "Concepts").mkdir()
    # Créer 2-3 notes de test
    (vault / "Concepts" / "C_Test.md").write_text(
        "---\ntitle: Test\ntype: concept\nstatus: seedling\n---\n# Test\n",
        encoding="utf-8"
    )
    (vault / "Concepts" / "C_Python.md").write_text(
        "---\ntitle: Python\ntype: concept\nstatus: growing\n---\n# Python\n[[C_Test]]\n",
        encoding="utf-8"
    )
    return vault

@pytest.fixture
def sample_transcript(tmp_path):
    """Crée un transcript JSONL réaliste."""
    transcript = tmp_path / "transcript.jsonl"
    entries = [
        {"type": "assistant", "timestamp": "2026-02-11T10:00:00Z",
         "message": {"content": [
             {"type": "tool_use", "name": "Read", "input": {"file_path": "/foo.md"}},
         ]}},
        {"type": "assistant", "timestamp": "2026-02-11T10:01:00Z",
         "message": {"content": [
             {"type": "tool_use", "name": "Write", "input": {"file_path": "/bar.md"}},
             {"type": "tool_use", "name": "Bash", "input": {"command": "git status"}},
         ]}},
        {"type": "assistant", "timestamp": "2026-02-11T10:02:00Z",
         "message": {"content": [
             {"type": "text", "text": "The issue was a missing import statement."},
         ]}},
        {"type": "tool_result", "content": "Error: file not found"},
    ]
    with open(transcript, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
    return transcript

@pytest.fixture
def sample_security_rules(tmp_path):
    """Crée un fichier security_rules.yaml minimal."""
    rules = tmp_path / "security_rules.yaml"
    rules.write_text("""
blocked:
  - pattern: "rm\\\\s+-rf\\\\s+/"
    reason: "Suppression recursive racine"
  - pattern: "format\\\\s+[a-zA-Z]:"
    reason: "Formatage disque"
confirm:
  - pattern: "git\\\\s+push.*--force"
    reason: "Force push"
alert:
  - pattern: "pip\\\\s+install"
    reason: "Installation package"
read_protected:
  - pattern: "\\\\.credentials\\\\.json$"
    reason: "Credentials"
  - pattern: "\\\\.env$"
    reason: "Env file"
write_protected:
  - pattern: "_Templates"
    reason: "Templates proteges"
system_paths:
  - pattern: "CLAUDE\\\\.md$"
    reason: "Fichier systeme"
""", encoding="utf-8")
    return rules

@pytest.fixture
def patch_paths(monkeypatch, tmp_path, tmp_logs):
    """Remplace les constantes de paths.py avec des chemins temporaires."""
    import hooks.lib.paths as paths_mod
    monkeypatch.setattr(paths_mod, "LOGS_DIR", tmp_logs)
    monkeypatch.setattr(paths_mod, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(paths_mod, "MEMORY_DIR", tmp_path / "memory")
    monkeypatch.setattr(paths_mod, "VAULT_PATH", tmp_path / "vault")
    monkeypatch.setattr(paths_mod, "HOOKS_DIR", tmp_path)
    (tmp_path / "memory").mkdir(exist_ok=True)
```

### Pseudocode test_security_validator.py (exemple)

```python
import pytest
from hooks.security_validator import load_rules, validate_command

class TestLoadRules:
    def test_load_rules_from_yaml(self, sample_security_rules, monkeypatch, patch_paths):
        monkeypatch.setattr("hooks.security_validator.CONFIG_DIR", sample_security_rules.parent)
        rules = load_rules()
        assert len(rules["blocked"]) >= 2
        assert len(rules["confirm"]) >= 1
        assert len(rules["alert"]) >= 1

    def test_load_rules_missing_file(self, tmp_path, monkeypatch, patch_paths):
        monkeypatch.setattr("hooks.security_validator.CONFIG_DIR", tmp_path / "nonexistent")
        rules = load_rules()
        assert rules == {"blocked": [], "confirm": [], "alert": []}

class TestValidateCommand:
    def test_blocked_rm_rf_root(self, sample_security_rules, monkeypatch, patch_paths):
        monkeypatch.setattr("hooks.security_validator.CONFIG_DIR", sample_security_rules.parent)
        cat, reason, _ = validate_command("rm -rf /")
        assert cat == "blocked"

    def test_allow_git_status(self, sample_security_rules, monkeypatch, patch_paths):
        monkeypatch.setattr("hooks.security_validator.CONFIG_DIR", sample_security_rules.parent)
        cat, _, _ = validate_command("git status")
        assert cat == "allow"
```

### Points d'intégration

```yaml
ROUTER:
  - Aucun changement (tests internes, pas de commande skill)

VAULT:
  - Aucune note à créer (tests techniques, pas de knowledge capture)

MCP:
  - Pas d'impact sur knowledge-assistant

CLAUDE.MD:
  - Aucune modification nécessaire (les tests sont internes)

MULTIPASS REPO:
  - Copier tests/ dans claude-config/hooks/tests/ après validation
  - Ajouter entrée dans CHANGELOG.md
```

## Validation Loop

### Niveau 1 : Structure & Syntax

```powershell
# Vérifier que les 9 fichiers existent
$testDir = "$env:USERPROFILE\.claude\hooks\tests"
$files = @(
    "__init__.py", "conftest.py",
    "test_lib.py", "test_security_validator.py",
    "test_path_guard.py", "test_prompt_analyzer.py",
    "test_memory_extractor.py", "test_load_context.py",
    "test_subagent_capture.py"
)
foreach ($f in $files) {
    $path = Join-Path $testDir $f
    if (Test-Path $path) { Write-Host "OK: $f" }
    else { Write-Warning "MISSING: $f" }
}
```

### Niveau 2 : Fonctionnel

```bash
# Exécuter les tests
cd ~/.claude/hooks
python -m pytest tests/ -v --tb=short

# Vérifier le nombre de tests
python -m pytest tests/ --co -q | tail -1
# Expected: ≥ 43 tests collected
```

### Niveau 3 : Intégration

```bash
# Vérifier que les hooks existants fonctionnent encore
echo '{"tool_input": {"command": "git status"}}' | python security_validator.py
# Expected: exit 0 (allow)

echo '{"tool_name": "Read", "tool_input": {"file_path": "test.md"}}' | python path_guard.py
# Expected: exit 0 (allow)

echo '{"message": "hello"}' | python prompt_analyzer.py
# Expected: exit 0
```

## Checklist de validation finale

- [ ] 9 fichiers créés dans hooks/tests/
- [ ] conftest.py avec 6+ fixtures (mock_stdin, tmp_logs, tmp_vault, sample_transcript, sample_security_rules, patch_paths)
- [ ] test_security_validator.py : 8+ tests (blocked, confirm, alert, allow)
- [ ] test_path_guard.py : 8+ tests (read_protected, write_protected, system_paths, allow)
- [ ] test_prompt_analyzer.py : 10+ tests (classify, skills, keywords)
- [ ] test_memory_extractor.py : 10+ tests (insights, vault notes, duration, path guard)
- [ ] test_load_context.py : 5+ tests (skills, vault count, guardian)
- [ ] test_subagent_capture.py : 5+ tests (parsing, agent name, duration)
- [ ] test_lib.py : 6+ tests (utils, transcript, paths)
- [ ] `pytest tests/ -v` : tous les tests PASS
- [ ] Aucun hook existant cassé
- [ ] pytest installé (vérifier `pip show pytest`)

## Anti-Patterns à éviter

- Ne pas tester main() directement (appelle sys.exit) — tester les fonctions internes
- Ne pas lire le vrai security_rules.yaml dans les tests — utiliser la fixture sample_security_rules
- Ne pas écrire dans le vrai vault — utiliser tmp_path
- Ne pas dépendre de stdin réel — toujours mocker
- Ne pas hardcoder des chemins absolus dans les tests — utiliser tmp_path et monkeypatch
- Ne pas oublier le `sys.path.insert` nécessaire pour les imports hooks

---

**Score de confiance : 9/10**

Haut niveau de confiance car :
- Les hooks sont des fonctions Python pures avec I/O mockable
- Le pattern de tests existe déjà dans le MCP server (100+ tests)
- Tous les cas critiques sont listés explicitement
- Les fixtures couvrent toutes les dépendances externes (stdin, filesystem, config)

Risque résiduel : les imports hooks utilisent `sys.path.insert(0, parent)` ce qui peut nécessiter un ajustement du PYTHONPATH pour pytest. Solution : lancer `python -m pytest` depuis le dossier `hooks/` ou ajouter un `conftest.py` qui configure le path.
