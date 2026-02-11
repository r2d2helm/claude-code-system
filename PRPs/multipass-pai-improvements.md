# PRP: Ameliorations structurelles MultiPass-AdminSysteme inspirees de PAI

## Goal

Etendre le systeme de hooks MultiPass avec 2 nouveaux evenements (SubagentStop, UserPromptSubmit), ajouter un systeme de memoire automatique (extraction d'insights depuis les sessions), et renforcer la securite avec une protection Read/Write/Edit basee sur une separation SYSTEM/USER des chemins.

## Why

- **Hooks etendus** : Actuellement 3 hooks sur 5 evenements. SubagentStop et UserPromptSubmit sont inutilises alors qu'ils offrent de la visibilite sur l'orchestration multi-agents et l'analyse des requetes utilisateur.
- **Memoire auto** : `session_capture.py` log des metriques (tools, files, commands) mais n'extrait aucun insight exploitable. Les connaissances acquises en session sont perdues sauf capture manuelle via `/know-save`.
- **Securite etendue** : `security_validator.py` ne protege que les commandes Bash. Read/Write/Edit n'ont aucune protection - un prompt malveillant pourrait lire `.credentials.json` ou ecraser `_Templates/`. La separation SYSTEM/USER n'existe pas.
- **Impact** : Ces 4 ameliorations transforment le systeme d'un outil reactif en infrastructure proactive avec apprentissage continu et protection en profondeur.

## What

### Comportement attendu

1. **SubagentStop** (`subagent_capture.py`) : A chaque fin de subagent, capture le nom de l'agent, sa description, son resultat resume, et log dans `hooks/logs/subagent-log.jsonl`.
2. **UserPromptSubmit** (`prompt_analyzer.py`) : A chaque soumission utilisateur, detecte des patterns (commandes skill, mots-cles techniques, questions) et log dans `hooks/logs/prompt-log.jsonl`. Peut injecter du contexte additionnel (`modified_input` non utilise en v1 - reserve pour v2).
3. **Memory Extractor** (`memory_extractor.py`) : Au Stop, analyse le transcript pour extraire insights (problemes resolus, decisions, patterns techniques) et les persiste dans `hooks/data/memory/`. Cree des notes vault pour les insights significatifs.
4. **Path Guard** (`path_guard.py`) : PreToolUse pour Read/Write/Edit. Bloque l'acces aux chemins sensibles (secrets) et demande confirmation pour les chemins systeme proteges.

### Success Criteria

- [ ] 5 hooks Python enregistres dans settings.json (3 existants + subagent_capture + prompt_analyzer + memory_extractor remplace session_capture + path_guard)
- [ ] SubagentStop log chaque fin de subagent dans subagent-log.jsonl
- [ ] UserPromptSubmit log chaque requete dans prompt-log.jsonl
- [ ] Stop extrait des insights et les persiste dans hooks/data/memory/
- [ ] Read sur .credentials.json ou *.env est bloque (exit 2)
- [ ] Write/Edit sur _Templates/ ou hooks/lib/ demande confirmation
- [ ] Tous les hooks existants continuent de fonctionner (regression zero)
- [ ] CLAUDE.md mis a jour avec la documentation des nouveaux hooks

## Contexte necessaire

### Documentation & References

```yaml
# MUST READ - Contexte a charger

- file: C:\Users\r2d2\.claude\hooks\session_capture.py
  why: "Hook Stop actuel - sera etendu par memory_extractor.py (doit garder toutes les fonctionnalites existantes)"

- file: C:\Users\r2d2\.claude\hooks\security_validator.py
  why: "Pattern a suivre pour path_guard.py - meme structure (load_rules, validate, main, exit codes)"

- file: C:\Users\r2d2\.claude\hooks\load_context.py
  why: "Pattern pour output additionalContext - utilise par prompt_analyzer en v2"

- file: C:\Users\r2d2\.claude\hooks\lib\utils.py
  why: "Fonctions partagees a reutiliser : read_stdin_json, output_json, log_audit, append_jsonl, now_paris"

- file: C:\Users\r2d2\.claude\hooks\lib\paths.py
  why: "Constantes de chemins - ajouter MEMORY_DIR et DATA_DIR"

- file: C:\Users\r2d2\.claude\hooks\config\security_rules.yaml
  why: "Structure des regles - ajouter sections read_protected et write_protected"

- file: C:\Users\r2d2\.claude\settings.json
  why: "Format d'enregistrement des hooks - ajouter SubagentStop, UserPromptSubmit, PreToolUse(Read/Write/Edit)"

- file: C:\Users\r2d2\.claude\CLAUDE.md
  why: "Instructions systeme a mettre a jour (section Hooks, nouveaux chemins)"
```

### Arbre actuel du systeme

```
~/.claude/hooks/
├── __init__.py
├── load_context.py          # SessionStart - injecte contexte
├── security_validator.py    # PreToolUse(Bash) - valide commandes
├── session_capture.py       # Stop - log metriques session
├── lib/
│   ├── __init__.py
│   ├── paths.py             # CLAUDE_DIR, HOOKS_DIR, VAULT_PATH, SKILLS_DIR, LOGS_DIR, CONFIG_DIR
│   └── utils.py             # read_stdin_json, output_json, log_audit, append_jsonl, now_paris
├── config/
│   └── security_rules.yaml  # 154 regles (blocked/confirm/alert) pour Bash
└── logs/
    ├── hooks-audit.jsonl    # Audit trail de tous les hooks
    └── session-log.jsonl    # Resume des sessions
```

### Arbre souhaite avec nouveaux fichiers

```
~/.claude/hooks/
├── __init__.py
├── load_context.py              # [INCHANGE] SessionStart
├── security_validator.py        # [INCHANGE] PreToolUse(Bash)
├── session_capture.py           # [DEPRECIE] Remplace par memory_extractor.py
├── memory_extractor.py          # [NOUVEAU] Stop - metriques + extraction insights
├── subagent_capture.py          # [NOUVEAU] SubagentStop - log resultats subagents
├── prompt_analyzer.py           # [NOUVEAU] UserPromptSubmit - analyse requetes
├── path_guard.py                # [NOUVEAU] PreToolUse(Read,Write,Edit) - protection chemins
├── lib/
│   ├── __init__.py
│   ├── paths.py                 # [MODIFIE] +MEMORY_DIR, +DATA_DIR
│   └── utils.py                 # [INCHANGE]
├── config/
│   ├── security_rules.yaml      # [MODIFIE] +read_protected, +write_protected, +system_paths
│   └── memory_rules.yaml        # [NOUVEAU] Patterns d'extraction d'insights
├── data/
│   └── memory/
│       ├── insights.jsonl       # Insights extraits automatiquement
│       ├── patterns.jsonl       # Patterns techniques detectes
│       └── signals.jsonl        # Signaux de session (duree, complexite, satisfaction)
└── logs/
    ├── hooks-audit.jsonl        # [INCHANGE] Audit trail
    ├── session-log.jsonl        # [INCHANGE] Metriques sessions
    ├── subagent-log.jsonl       # [NOUVEAU] Log des subagents
    └── prompt-log.jsonl         # [NOUVEAU] Log des requetes utilisateur
```

### Gotchas connus du systeme

```
# CRITICAL: Tous les hooks DOIVENT exit 0 en cas d'erreur (fail-open)
# CRITICAL: Seul exit 2 avec {"decision":"block","reason":"..."} bloque Claude Code
# CRITICAL: stdin JSON = donnees differentes selon l'evenement :
#   - SessionStart: { session_id }
#   - PreToolUse: { tool_name, tool_input: { command|file_path|... } }
#   - PostToolUse: { tool_name, tool_input, tool_result }
#   - Stop: { session_id, transcript_path }
#   - SubagentStop: { session_id, transcript_path }  (meme format que Stop)
#   - UserPromptSubmit: { session_id, message }
# CRITICAL: matcher "" = tous les outils, "Bash" = Bash uniquement (case-sensitive exact match)
# CRITICAL: UTF-8 sans BOM pour .py, .md, .json, .yaml
# CRITICAL: PS 5.1 compatible si scripts PowerShell
# CRITICAL: Ne pas bloquer le flux Claude Code - hooks doivent etre rapides (<500ms)
```

### Protocole Hook Claude Code (reference)

```
Evenement declenche
    |
    v
Claude Code envoie JSON sur stdin du hook
    |
    v
Hook lit stdin (read_stdin_json)
    |
    v
Hook traite les donnees
    |
    v
Hook ecrit JSON sur stdout (output_json) si necessaire
    |
    v
Hook sort avec exit code:
  - 0 : allow (ou allow avec output)
  - 2 : block (doit inclure {"decision":"block","reason":"..."} sur stdout)
    |
    v
Claude Code reagit selon le code + output

Outputs possibles par evenement:
  SessionStart    -> { "additionalContext": "texte injecte" }
  PreToolUse      -> { "decision": "block", "reason": "..." }  (exit 2)
                  -> {} ou rien (exit 0 = allow)
  PostToolUse     -> pas de decision, side-effects uniquement
  Stop            -> pas de decision, side-effects uniquement
  SubagentStop    -> pas de decision, side-effects uniquement
  UserPromptSubmit-> { "modified_input": "texte modifie" } (optionnel, v2)
                  -> {} ou rien (exit 0 = pass-through)
  Notification    -> pas de decision, side-effects uniquement
```

## Implementation Blueprint

### Structure des fichiers a creer

```yaml
Fichier 1:
  path: ~/.claude/hooks/subagent_capture.py
  role: "Hook SubagentStop - capture les resultats des subagents"
  pattern: "session_capture.py (meme structure: parse transcript + log)"

Fichier 2:
  path: ~/.claude/hooks/prompt_analyzer.py
  role: "Hook UserPromptSubmit - analyse les requetes utilisateur"
  pattern: "load_context.py (lecture stdin + log + exit 0)"

Fichier 3:
  path: ~/.claude/hooks/memory_extractor.py
  role: "Hook Stop etendu - metriques session + extraction insights"
  pattern: "session_capture.py (remplace, garde parse_transcript + ajoute extraction)"

Fichier 4:
  path: ~/.claude/hooks/path_guard.py
  role: "Hook PreToolUse pour Read/Write/Edit - protection des chemins"
  pattern: "security_validator.py (meme structure: load_rules, validate, exit 2/0)"

Fichier 5:
  path: ~/.claude/hooks/config/memory_rules.yaml
  role: "Configuration des patterns d'extraction d'insights"
  pattern: "security_rules.yaml (categories + patterns regex)"

Fichier 6 (MODIFIE):
  path: ~/.claude/hooks/lib/paths.py
  role: "Ajouter DATA_DIR et MEMORY_DIR"

Fichier 7 (MODIFIE):
  path: ~/.claude/hooks/config/security_rules.yaml
  role: "Ajouter sections read_protected et write_protected"

Fichier 8 (MODIFIE):
  path: ~/.claude/settings.json
  role: "Enregistrer les 4 nouveaux hooks"

Fichier 9 (MODIFIE):
  path: ~/.claude/CLAUDE.md
  role: "Documenter les nouveaux hooks et chemins"
```

### Liste des taches ordonnees

```yaml
Task 1:
  action: MODIFY
  path: ~/.claude/hooks/lib/paths.py
  description: |
    Ajouter 2 nouvelles constantes:
      DATA_DIR = HOOKS_DIR / "data"
      MEMORY_DIR = DATA_DIR / "memory"
  pattern: "Suivre le style existant (constantes Path simples)"

Task 2:
  action: CREATE
  path: ~/.claude/hooks/config/memory_rules.yaml
  description: |
    Definir les patterns d'extraction d'insights:
    - insights: patterns regex pour detecter des resolutions de problemes,
      decisions techniques, workarounds trouves
    - patterns: patterns regex pour detecter des patterns techniques recurrents
      (encodage, permissions, chemins, configurations)
    - signals: regles pour calculer complexite/satisfaction de session
      (nombre tools, duree, erreurs, files modifies)
  pattern: "security_rules.yaml (structure categories + items avec pattern/reason)"

Task 3:
  action: MODIFY
  path: ~/.claude/hooks/config/security_rules.yaml
  description: |
    Ajouter 3 nouvelles sections apres "alert":

    read_protected:
      - pattern: "\\.credentials\\.json$"
        reason: "Fichier de credentials"
      - pattern: "\\.env$|\\.env\\."
        reason: "Variables d'environnement"
      - pattern: "\\\\secrets\\\\|/secrets/"
        reason: "Dossier secrets"

    write_protected:
      - pattern: "\\\\_Templates\\\\|/_Templates/"
        reason: "Templates vault proteges"
      - pattern: "\\.claude\\\\hooks\\\\lib\\\\|\\.claude/hooks/lib/"
        reason: "Librairie hooks systeme"
      - pattern: "\\.claude\\\\agents\\\\|\\.claude/agents/"
        reason: "Definitions des subagents"
      - pattern: "\\.claude\\\\settings\\.json$"
        reason: "Configuration Claude Code"

    system_paths:
      - pattern: "\\.claude\\\\skills\\\\SKILL\\.md$"
        reason: "Meta-router (fichier systeme critique)"
      - pattern: "\\.claude\\\\hooks\\\\(load_context|security_validator|session_capture)\\.py$"
        reason: "Hooks systeme"
  pattern: "Format existant (YAML, categorie -> liste de {pattern, reason})"

Task 4:
  action: CREATE
  path: ~/.claude/hooks/subagent_capture.py
  description: |
    Hook SubagentStop. Stdin recoit { session_id, transcript_path }.

    1. read_stdin_json()
    2. Extraire session_id et transcript_path
    3. Lire les dernieres 50 lignes du transcript pour trouver:
       - Le nom de l'agent (chercher "Task" tool_use avec description)
       - Le resultat (derniere reponse de l'agent)
       - La duree approximative (premier/dernier timestamp)
    4. Construire un resume structure:
       { timestamp, session_id, agent_name, description, duration_s,
         tools_used: {}, files_modified: [], outcome_summary: str }
    5. append_jsonl(LOGS_DIR / "subagent-log.jsonl", summary)
    6. log_audit("subagent_capture", "subagent_end", summary)
    7. sys.exit(0)

    Fail-open: try/except global -> log_audit error -> exit 0
  pattern: "session_capture.py (parse_transcript + main + fail-open)"

Task 5:
  action: CREATE
  path: ~/.claude/hooks/prompt_analyzer.py
  description: |
    Hook UserPromptSubmit. Stdin recoit { session_id, message }.

    1. read_stdin_json()
    2. Extraire session_id et message
    3. Analyser le message:
       a. Detecter les commandes skill (regex: /[a-z]+-[a-z]+/)
       b. Detecter les mots-cles techniques (liste predeterminee)
       c. Classifier le type: command | question | instruction | debug
       d. Calculer la longueur/complexite
    4. Log dans prompt-log.jsonl:
       { timestamp, session_id, message_type, skills_detected: [],
         keywords: [], message_length, message_preview: str[:100] }
    5. log_audit("prompt_analyzer", "user_input", { type, skills })
    6. sys.exit(0)  -- pas de modified_input en v1

    Fail-open: try/except global -> log_audit error -> exit 0

    IMPORTANT: Ne PAS logger le message complet (vie privee).
    Seulement preview (100 chars), type, et metadata.
  pattern: "load_context.py (simple: read stdin, process, log, exit 0)"

Task 6:
  action: CREATE
  path: ~/.claude/hooks/memory_extractor.py
  description: |
    Hook Stop etendu. Remplace session_capture.py.
    Stdin recoit { session_id, transcript_path }.

    PARTIE 1 - Metriques (reprise de session_capture.py):
    1. read_stdin_json()
    2. parse_transcript(transcript_path) -> metriques identiques a l'actuel
    3. append_jsonl(LOGS_DIR / "session-log.jsonl", session_summary)

    PARTIE 2 - Extraction d'insights (NOUVEAU):
    4. Charger memory_rules.yaml
    5. Parcourir les messages assistant du transcript pour extraire:
       a. INSIGHTS: Texte contenant des resolutions, decisions, corrections
          - Regex: "fix|resolved|solution|workaround|found that|the issue was"
          - Extraire le contexte (3 lignes avant/apres)
          - Deduplication par hash du contenu
       b. PATTERNS: Patterns techniques recurrents
          - Regex: "always|never|must|convention|rule|pattern"
          - Associer au skill concerne si detectable
       c. SIGNALS: Metriques de session
          - Duree (premier/dernier timestamp)
          - Complexite (nombre unique de tools, nombre de fichiers)
          - Erreurs (nombre de tool_result avec "error"|"Error"|"FAIL")
    6. Persister:
       - Insights -> DATA_DIR/memory/insights.jsonl
       - Patterns -> DATA_DIR/memory/patterns.jsonl
       - Signals -> DATA_DIR/memory/signals.jsonl
    7. Si un insight est "significatif" (>50 chars, contient un fix ou decision):
       - Creer une note vault dans Knowledge/_Inbox/
       - Format: YYYY-MM-DD_insight_NNN.md avec frontmatter
       - Le guardian ou l'utilisateur triera depuis _Inbox/

    PARTIE 3 - Audit:
    8. log_audit("memory_extractor", "session_end", { metrics + insights_count })
    9. sys.exit(0)

    Structure insight JSONL:
    { timestamp, session_id, type: "insight"|"pattern"|"signal",
      content: str, context: str, skill: str|null, confidence: float }

    Fail-open obligatoire. max_lines=200 pour le transcript (performance).
  pattern: "session_capture.py (garder TOUT le code existant, ajouter partie 2)"

Task 7:
  action: CREATE
  path: ~/.claude/hooks/path_guard.py
  description: |
    Hook PreToolUse pour Read, Write, Edit.
    Stdin recoit { tool_name, tool_input }.

    1. read_stdin_json()
    2. Extraire tool_name et file_path depuis tool_input:
       - Read: tool_input.file_path
       - Write: tool_input.file_path
       - Edit: tool_input.file_path
    3. Si pas de file_path -> exit 0 (allow)
    4. Normaliser le chemin (Path.resolve())
    5. Charger les regles depuis security_rules.yaml:
       - Si tool_name == "Read": verifier read_protected
       - Si tool_name in ("Write", "Edit"): verifier write_protected + system_paths
    6. Pour chaque regle matchee:
       - read_protected: exit 2 + block (acces refuse)
       - write_protected: exit 0 + decision block (confirmation)
       - system_paths: exit 0 + decision block (confirmation)
    7. Si aucune regle matchee: exit 0 silencieux (allow)

    log_audit pour chaque decision (blocked, confirm, allow).
    Fail-open: try/except global -> exit 0

    ATTENTION: Le matcher dans settings.json ne supporte qu'un seul outil.
    Il faut TROIS entrees PreToolUse separees:
      - matcher: "Read" -> path_guard.py
      - matcher: "Write" -> path_guard.py
      - matcher: "Edit" -> path_guard.py
    Le hook recoit tool_name dans le stdin pour differencier.
  pattern: "security_validator.py (load_rules, validate, main, exit codes)"

Task 8:
  action: MODIFY
  path: ~/.claude/settings.json
  description: |
    Ajouter les nouveaux hooks. Structure finale:

    hooks:
      SessionStart:       [load_context.py]          (INCHANGE)
      PreToolUse:         [security_validator.py(Bash),
                           path_guard.py(Read),
                           path_guard.py(Write),
                           path_guard.py(Edit)]
      PostToolUse:        [powershell Write]          (INCHANGE)
      Stop:               [memory_extractor.py]       (REMPLACE session_capture.py)
      SubagentStop:       [subagent_capture.py]       (NOUVEAU)
      UserPromptSubmit:   [prompt_analyzer.py]        (NOUVEAU)
      Notification:       [messagebox]                (INCHANGE)

    Utiliser le meme format:
    {
      "matcher": "Read",
      "hooks": [{ "type": "command", "command": "python C:\\Users\\r2d2\\.claude\\hooks\\path_guard.py" }]
    }

    ATTENTION: PreToolUse est un tableau - ajouter 3 nouvelles entrees au tableau existant
    (ne pas ecraser security_validator.py pour Bash).
  pattern: "Format existant dans settings.json"

Task 9:
  action: CREATE
  path: ~/.claude/hooks/data/memory/.gitkeep
  description: "Creer le dossier data/memory/ avec .gitkeep"

Task 10:
  action: MODIFY
  path: ~/.claude/CLAUDE.md
  description: |
    Mettre a jour les sections suivantes:

    1. Ajouter dans "## Architecture Agents" une sous-section "### Hooks (6)":
       | Hook | Evenement | Matcher | Description |
       |------|-----------|---------|-------------|
       | load_context.py | SessionStart | * | Charge contexte systeme |
       | security_validator.py | PreToolUse | Bash | Valide commandes shell |
       | path_guard.py | PreToolUse | Read,Write,Edit | Protege chemins sensibles |
       | memory_extractor.py | Stop | * | Metriques + extraction insights |
       | subagent_capture.py | SubagentStop | * | Log resultats subagents |
       | prompt_analyzer.py | UserPromptSubmit | * | Analyse requetes utilisateur |

    2. Ajouter dans "## Chemins importants":
       | Memory data | ~/.claude/hooks/data/memory/ |
       | Hooks logs | ~/.claude/hooks/logs/ |

    3. Ajouter regle 18:
       "18. **Fail-open** : tous les hooks exit 0 en cas d'erreur, jamais bloquer Claude Code"

    4. Mettre a jour le commentaire hooks existant (3 → 6 hooks)

Task 11:
  action: MODIFY
  path: C:\Users\r2d2\Documents\MultiPass-AdminSysteme\claude-config\CLAUDE.md
  description: "Memes modifications que Task 10 mais dans le repo package"

Task 12:
  action: MODIFY
  path: C:\Users\r2d2\Documents\MultiPass-AdminSysteme\claude-config\settings.json
  description: |
    Copie sanitisee de settings.json avec les nouveaux hooks.
    Remplacer C:\Users\r2d2 par %USERPROFILE% dans les chemins.
```

### Pseudocode par tache

```python
# ============================================================
# Task 4 - subagent_capture.py
# PATTERN: Suivre session_capture.py
# ============================================================
"""SubagentStop hook: capture les resultats des subagents."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.paths import LOGS_DIR
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris

def parse_subagent_transcript(transcript_path: str, max_lines: int = 50) -> dict:
    """Parse les dernieres lignes du transcript subagent."""
    # Lire les dernieres max_lines lignes
    # Chercher: tool_use "Task" -> input.description = nom agent
    # Compter tools_used, files_modified
    # Extraire premier/dernier timestamp pour duree
    # Extraire derniere reponse texte comme outcome_summary[:200]
    ...

def main():
    try:
        input_data = read_stdin_json()
        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")

        result = {}
        if transcript_path:
            result = parse_subagent_transcript(transcript_path)

        summary = {
            "timestamp": now_paris(),
            "session_id": session_id,
            **result,
        }

        append_jsonl(LOGS_DIR / "subagent-log.jsonl", summary)
        log_audit("subagent_capture", "subagent_end", {
            "session_id": session_id,
            "agent": result.get("agent_name", "unknown"),
        })
    except Exception as e:
        log_audit("subagent_capture", "error", {"error": str(e)})
    sys.exit(0)

# ============================================================
# Task 5 - prompt_analyzer.py
# PATTERN: Suivre load_context.py (simple)
# GOTCHA: Ne PAS logger le message complet (vie privee)
# ============================================================
"""UserPromptSubmit hook: analyse les requetes utilisateur."""
import sys, re, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.paths import LOGS_DIR
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris

SKILL_COMMAND_RE = re.compile(r"/([\w-]+)")
TECHNICAL_KEYWORDS = {"docker", "proxmox", "windows", "linux", "vault",
                       "obsidian", "backup", "deploy", "debug", "fix",
                       "qet", "sop", "prp", "skill", "maintenance"}

def classify_message(message: str) -> str:
    """Classifie le message: command|question|instruction|debug."""
    if message.startswith("/"):
        return "command"
    if "?" in message or message.lower().startswith(("pourquoi", "comment", "quoi", "what", "how", "why")):
        return "question"
    if any(kw in message.lower() for kw in ("fix", "debug", "error", "bug", "crash")):
        return "debug"
    return "instruction"

def main():
    try:
        input_data = read_stdin_json()
        session_id = input_data.get("session_id", "unknown")
        message = input_data.get("message", "")

        if not message:
            sys.exit(0)

        msg_type = classify_message(message)
        skills = SKILL_COMMAND_RE.findall(message)
        keywords = [kw for kw in TECHNICAL_KEYWORDS if kw in message.lower()]

        entry = {
            "timestamp": now_paris(),
            "session_id": session_id,
            "message_type": msg_type,
            "skills_detected": skills[:5],
            "keywords": keywords[:10],
            "message_length": len(message),
            "message_preview": message[:100],
        }

        append_jsonl(LOGS_DIR / "prompt-log.jsonl", entry)
        log_audit("prompt_analyzer", "user_input", {
            "type": msg_type, "skills": skills[:5]
        })
    except Exception as e:
        log_audit("prompt_analyzer", "error", {"error": str(e)})
    sys.exit(0)

# ============================================================
# Task 6 - memory_extractor.py
# PATTERN: session_capture.py (garder parse_transcript IDENTIQUE)
# GOTCHA: max_lines=200, fail-open, performance <500ms
# ============================================================
"""Stop hook etendu: metriques session + extraction insights."""
import sys, json, re, hashlib
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.paths import LOGS_DIR, MEMORY_DIR
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris

# PARTIE 1: parse_transcript() - COPIE EXACTE de session_capture.py
# (garder les 100 lignes existantes sans modification)

# PARTIE 2: extract_insights()
INSIGHT_PATTERNS = [
    re.compile(r"(?:fix|resolved|solution|workaround|the issue was|found that|problem was)(.{20,200})", re.I),
]
PATTERN_PATTERNS = [
    re.compile(r"(?:always|never|must|convention|rule|pattern|important)(.{20,150})", re.I),
]

def extract_insights(transcript_path: str, max_lines: int = 200) -> dict:
    """Extrait insights et patterns du transcript."""
    insights = []
    patterns = []
    seen_hashes = set()
    errors_count = 0

    # Lire les dernieres max_lines lignes
    # Pour chaque message assistant, chercher les patterns
    # Deduplication par hash MD5 du contenu
    # Retourner { insights: [...], patterns: [...], errors_count: int }
    ...

def create_vault_note(insight: dict, vault_path: Path) -> None:
    """Cree une note dans _Inbox/ pour un insight significatif."""
    # Seulement si contenu > 50 chars et contient fix/decision
    # Format: YYYY-MM-DD_insight_NNN.md avec frontmatter
    # Type: troubleshooting, status: seedling, tags: [ai/auto-memory]
    ...

# PARTIE 3: main()
def main():
    try:
        input_data = read_stdin_json()
        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")

        # Metriques (partie 1 - identique a session_capture)
        metrics = {}
        if transcript_path:
            metrics = parse_transcript(transcript_path)

        session_summary = {"timestamp": now_paris(), "session_id": session_id, "metrics": metrics}
        append_jsonl(LOGS_DIR / "session-log.jsonl", session_summary)

        # Extraction insights (partie 2)
        memory = {}
        if transcript_path:
            memory = extract_insights(transcript_path)

        for insight in memory.get("insights", []):
            append_jsonl(MEMORY_DIR / "insights.jsonl", insight)
            if len(insight.get("content", "")) > 50:
                create_vault_note(insight, VAULT_PATH)

        for pattern in memory.get("patterns", []):
            append_jsonl(MEMORY_DIR / "patterns.jsonl", pattern)

        signal = {
            "timestamp": now_paris(), "session_id": session_id,
            "duration_s": ..., "complexity": ..., "errors": memory.get("errors_count", 0),
        }
        append_jsonl(MEMORY_DIR / "signals.jsonl", signal)

        log_audit("memory_extractor", "session_end", {
            "session_id": session_id,
            "messages": metrics.get("message_count", 0),
            "insights": len(memory.get("insights", [])),
            "patterns": len(memory.get("patterns", [])),
        })
    except Exception as e:
        log_audit("memory_extractor", "error", {"error": str(e)})
    sys.exit(0)

# ============================================================
# Task 7 - path_guard.py
# PATTERN: security_validator.py (load_rules + validate + exit codes)
# GOTCHA: 3 matchers dans settings.json (Read, Write, Edit) pointant vers le meme fichier
# GOTCHA: tool_name dans stdin pour differencier le contexte
# ============================================================
"""PreToolUse hook (Read/Write/Edit): protege les chemins sensibles."""
import sys, re, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.paths import CONFIG_DIR
from lib.utils import read_stdin_json, log_audit, output_json

_compiled_rules = None

def load_path_rules() -> dict:
    """Charge les regles de protection des chemins."""
    # Charger security_rules.yaml
    # Compiler les regex pour read_protected, write_protected, system_paths
    ...

def validate_path(tool_name: str, file_path: str) -> tuple:
    """Valide un chemin. Retourne (category, reason, pattern) ou ('allow', '', '')."""
    rules = load_path_rules()
    resolved = str(Path(file_path).resolve())

    if tool_name == "Read":
        for rule in rules.get("read_protected", []):
            if rule["regex"].search(resolved):
                return "blocked", rule["reason"], rule["pattern"]

    if tool_name in ("Write", "Edit"):
        for rule in rules.get("write_protected", []):
            if rule["regex"].search(resolved):
                return "confirm", rule["reason"], rule["pattern"]
        for rule in rules.get("system_paths", []):
            if rule["regex"].search(resolved):
                return "confirm", rule["reason"], rule["pattern"]

    return "allow", "", ""

def main():
    try:
        input_data = read_stdin_json()
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        file_path = tool_input.get("file_path", "") or tool_input.get("notebook_path", "")

        if not file_path:
            sys.exit(0)

        category, reason, pattern = validate_path(tool_name, file_path)

        if category == "blocked":
            log_audit("path_guard", "blocked", {"tool": tool_name, "path": file_path[:200], "reason": reason})
            print(json.dumps({"decision": "block", "reason": f"SECURITE: Acces refuse - {reason}"}))
            sys.exit(2)

        elif category == "confirm":
            log_audit("path_guard", "confirm", {"tool": tool_name, "path": file_path[:200], "reason": reason})
            output_json({"decision": "block", "reason": f"ATTENTION: {reason}. Confirmation requise."})
            sys.exit(0)

        else:
            sys.exit(0)

    except SystemExit:
        raise
    except Exception as e:
        log_audit("path_guard", "error", {"error": str(e)})
        sys.exit(0)
```

### Points d'integration

```yaml
ROUTER:
  - Pas de modification du meta-router (les hooks ne sont pas des skills)
  - Les hooks sont transparents pour le routage

VAULT:
  - memory_extractor.py cree des notes dans Knowledge/_Inbox/
  - Format: YYYY-MM-DD_insight_NNN.md
  - Template: frontmatter minimal (title, date, type: troubleshooting, status: seedling, tags: [ai/auto-memory])
  - Le guardian ou l'utilisateur triera depuis _Inbox/
  - NE PAS creer de notes dans Concepts/ ou Conversations/ automatiquement

MCP:
  - Pas d'impact sur knowledge-assistant
  - Les notes _Inbox/ seront indexees au prochain rebuild

CLAUDE.MD:
  - Mise a jour section Hooks (3 → 6 hooks)
  - Mise a jour Chemins importants (+2 chemins)
  - Ajout regle 18 (fail-open)

SETTINGS.JSON:
  - 4 nouvelles entrees dans hooks {}
  - PreToolUse: 3 nouveaux matchers (Read, Write, Edit)
  - Stop: remplacer session_capture.py par memory_extractor.py
  - SubagentStop: nouveau
  - UserPromptSubmit: nouveau

MULTIPASS REPO:
  - Copier les fichiers modifies dans claude-config/
  - Sanitiser les chemins (%USERPROFILE%)
  - Mettre a jour CHANGELOG.md
```

## Validation Loop

### Niveau 1 : Structure & Syntax

```powershell
# Verifier que les nouveaux fichiers existent
$files = @(
    "$env:USERPROFILE\.claude\hooks\subagent_capture.py",
    "$env:USERPROFILE\.claude\hooks\prompt_analyzer.py",
    "$env:USERPROFILE\.claude\hooks\memory_extractor.py",
    "$env:USERPROFILE\.claude\hooks\path_guard.py",
    "$env:USERPROFILE\.claude\hooks\config\memory_rules.yaml",
    "$env:USERPROFILE\.claude\hooks\data\memory\.gitkeep"
)
$files | ForEach-Object {
    if (Test-Path $_) { Write-Output "OK: $_" }
    else { Write-Warning "MISSING: $_" }
}

# Verifier l'encodage UTF-8 sans BOM
$files | Where-Object { $_ -match '\.py$' } | ForEach-Object {
    $bytes = [System.IO.File]::ReadAllBytes($_)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        Write-Warning "BOM detecte: $_"
    } else {
        Write-Output "UTF-8 OK: $_"
    }
}

# Verifier la syntaxe Python
python -c "import py_compile; py_compile.compile('$env:USERPROFILE\.claude\hooks\subagent_capture.py', doraise=True)"
python -c "import py_compile; py_compile.compile('$env:USERPROFILE\.claude\hooks\prompt_analyzer.py', doraise=True)"
python -c "import py_compile; py_compile.compile('$env:USERPROFILE\.claude\hooks\memory_extractor.py', doraise=True)"
python -c "import py_compile; py_compile.compile('$env:USERPROFILE\.claude\hooks\path_guard.py', doraise=True)"

# Verifier le JSON de settings.json
python -c "import json; json.load(open('$env:USERPROFILE\.claude\settings.json'))"

# Verifier le YAML des rules
python -c "import yaml; yaml.safe_load(open('$env:USERPROFILE\.claude\hooks\config\security_rules.yaml'))"
python -c "import yaml; yaml.safe_load(open('$env:USERPROFILE\.claude\hooks\config\memory_rules.yaml'))"
```

### Niveau 2 : Fonctionnel

```powershell
# Test subagent_capture.py avec stdin simule
$testInput = '{"session_id":"test-123","transcript_path":""}'
$testInput | python "$env:USERPROFILE\.claude\hooks\subagent_capture.py"
# Attendre: exit 0, ligne ajoutee dans subagent-log.jsonl

# Test prompt_analyzer.py
$testInput = '{"session_id":"test-123","message":"/daily-maintenance"}'
$testInput | python "$env:USERPROFILE\.claude\hooks\prompt_analyzer.py"
# Attendre: exit 0, ligne ajoutee dans prompt-log.jsonl avec type "command"

# Test memory_extractor.py (sans transcript)
$testInput = '{"session_id":"test-123","transcript_path":""}'
$testInput | python "$env:USERPROFILE\.claude\hooks\memory_extractor.py"
# Attendre: exit 0, ligne ajoutee dans session-log.jsonl

# Test path_guard.py - Read sur .credentials.json (doit bloquer)
$testInput = '{"tool_name":"Read","tool_input":{"file_path":"C:\\Users\\r2d2\\.credentials.json"}}'
$testInput | python "$env:USERPROFILE\.claude\hooks\path_guard.py"
# Attendre: exit 2, output {"decision":"block","reason":"...credentials..."}

# Test path_guard.py - Write sur fichier normal (doit passer)
$testInput = '{"tool_name":"Write","tool_input":{"file_path":"C:\\Users\\r2d2\\test.md"}}'
$testInput | python "$env:USERPROFILE\.claude\hooks\path_guard.py"
# Attendre: exit 0, pas d'output

# Test path_guard.py - Edit sur _Templates (doit confirmer)
$testInput = '{"tool_name":"Edit","tool_input":{"file_path":"C:\\Users\\r2d2\\Documents\\Knowledge\\_Templates\\test.md"}}'
$testInput | python "$env:USERPROFILE\.claude\hooks\path_guard.py"
# Attendre: exit 0, output {"decision":"block","reason":"...Templates..."}

# Verifier que les hooks existants fonctionnent toujours
$testInput = '{"session_id":"test-123"}'
$testInput | python "$env:USERPROFILE\.claude\hooks\load_context.py"
# Attendre: exit 0, output {"additionalContext":"..."}

$testInput = '{"tool_input":{"command":"ls"}}'
$testInput | python "$env:USERPROFILE\.claude\hooks\security_validator.py"
# Attendre: exit 0 (allow)
```

### Niveau 3 : Integration

```powershell
# Verifier settings.json est valide et complet
$settings = Get-Content "$env:USERPROFILE\.claude\settings.json" | ConvertFrom-Json
$events = $settings.hooks.PSObject.Properties.Name
$expected = @("SessionStart", "PreToolUse", "PostToolUse", "Stop", "SubagentStop", "UserPromptSubmit", "Notification")
$expected | ForEach-Object {
    if ($events -contains $_) { Write-Output "OK: $_" }
    else { Write-Warning "MISSING event: $_" }
}

# Verifier que PreToolUse a 4 matchers (Bash + Read + Write + Edit)
$preToolUse = $settings.hooks.PreToolUse
$matchers = $preToolUse | ForEach-Object { $_.matcher }
@("Bash", "Read", "Write", "Edit") | ForEach-Object {
    if ($matchers -contains $_) { Write-Output "OK matcher: $_" }
    else { Write-Warning "MISSING matcher: $_" }
}

# Verifier CLAUDE.md mentionne 6 hooks
Select-String -Path "$env:USERPROFILE\.claude\CLAUDE.md" -Pattern "memory_extractor|subagent_capture|prompt_analyzer|path_guard" | Measure-Object
# Attendre: >= 4 matches

# Verifier la coherence avec le repo package
$liveHooks = (Get-ChildItem "$env:USERPROFILE\.claude\hooks\*.py" -File).Name | Sort-Object
$repoHooks = (Get-ChildItem "$env:USERPROFILE\Documents\MultiPass-AdminSysteme\claude-config\hooks\*.py" -File).Name | Sort-Object
Compare-Object $liveHooks $repoHooks
# Attendre: aucune difference

# Score de sante vault inchange
# /guardian-health --quick -> score >= 98/100
```

## Checklist de validation finale

- [ ] 4 nouveaux fichiers Python crees avec UTF-8 sans BOM
- [ ] memory_rules.yaml cree avec patterns d'extraction
- [ ] security_rules.yaml etendu avec read_protected, write_protected, system_paths
- [ ] paths.py modifie avec DATA_DIR et MEMORY_DIR
- [ ] settings.json mis a jour avec 7 evenements (4 nouveaux hooks)
- [ ] Dossier data/memory/ cree
- [ ] Tous les hooks compilent (py_compile)
- [ ] Tests fonctionnels passent (stdin simule)
- [ ] path_guard.py bloque Read sur .credentials.json (exit 2)
- [ ] path_guard.py demande confirmation Write sur _Templates/ (exit 0 + block)
- [ ] path_guard.py laisse passer Write sur fichiers normaux (exit 0 silencieux)
- [ ] Hooks existants non casses (regression zero)
- [ ] CLAUDE.md live mis a jour (6 hooks, chemins, regle 18)
- [ ] CLAUDE.md repo mis a jour + sanitise
- [ ] settings.json repo mis a jour + sanitise
- [ ] CHANGELOG.md mis a jour (v1.1.0)
- [ ] Aucun secret expose dans les fichiers

---

## Anti-Patterns a eviter

- Ne pas modifier session_capture.py directement - creer memory_extractor.py comme remplacement propre
- Ne pas logger le contenu complet des messages utilisateur (vie privee)
- Ne pas bloquer Claude Code en cas d'erreur de hook (TOUJOURS fail-open)
- Ne pas creer de notes vault dans Concepts/ automatiquement - utiliser _Inbox/ uniquement
- Ne pas hardcoder des chemins absolus dans les hooks Python (utiliser Path.home() via paths.py)
- Ne pas oublier les 3 matchers separes pour path_guard.py (Read, Write, Edit)
- Ne pas melanger la logique de validation Bash (security_validator) avec la validation de chemins (path_guard)
- Ne pas depasser 500ms par hook (limiter max_lines pour les transcripts)

---

**Score de confiance : 8/10**

Justification:
- +3 : Architecture claire avec patterns existants a suivre (security_validator, session_capture)
- +2 : Shared lib (utils.py, paths.py) simplifie l'implementation
- +2 : Tests fonctionnels detailles avec stdin simule
- +1 : Separation claire des responsabilites (1 hook = 1 fichier = 1 evenement)
- -1 : extract_insights() necessite du tuning des regex (les patterns de detection d'insights sont approximatifs)
- -1 : Le format exact du stdin pour SubagentStop et UserPromptSubmit n'est pas documente officiellement - base sur le comportement observe de PAI
