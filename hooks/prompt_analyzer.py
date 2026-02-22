"""UserPromptSubmit hook: analyse les requetes utilisateur.

Detecte les commandes skill, mots-cles techniques, et classifie
le type de requete. Log dans prompt-log.jsonl.
Injecte additionalContext = routing skills + keywords + memory context.

IMPORTANT: Ne log PAS le message complet (vie privee).
Seulement preview (100 chars), type, et metadata.
"""

import sys
import re
import json
from pathlib import Path

# Ajouter le dossier hooks au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import LOGS_DIR, CONFIG_DIR
from lib.context_cache import get_or_compute_context
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris, output_json

# Regex pour detecter les commandes skill (/prefix-action)
SKILL_COMMAND_RE = re.compile(r"/([\w][\w-]*)")

# Mots-cles techniques fallback
_FALLBACK_KEYWORDS = {
    "docker", "proxmox", "windows", "linux", "vault",
    "obsidian", "backup", "deploy", "debug", "fix",
    "qet", "qelectrotech", "sop", "prp", "skill",
    "maintenance", "firewall", "network", "container",
    "vm", "lxc", "cluster", "ceph", "zfs",
    "git", "hook", "mcp", "agent", "router",
}


def _load_router_rules() -> dict:
    """Charge les regles de routage depuis router_rules.yaml."""
    rules_file = CONFIG_DIR / "router_rules.yaml"
    try:
        if rules_file.exists():
            try:
                import yaml
                return yaml.safe_load(rules_file.read_text(encoding="utf-8")) or {}
            except ImportError:
                pass
    except Exception:
        pass
    return {}


def _detect_skill_from_keywords(message_lower: str, router_rules: dict) -> list[str]:
    """Detecte les skills probables via les keywords du routeur."""
    skills_data = router_rules.get("skills", {})
    disambiguation = router_rules.get("disambiguation", {})
    matched_skills = []

    for skill_name, skill_info in skills_data.items():
        primary = skill_info.get("primary", [])
        secondary = skill_info.get("secondary", [])

        # Primary keywords = high confidence match
        for kw in primary:
            if kw.lower() in message_lower:
                matched_skills.append(skill_name)
                break
        else:
            # Secondary keywords = lower confidence, only if 2+ match
            sec_count = sum(1 for kw in secondary if kw.lower() in message_lower)
            if sec_count >= 2:
                matched_skills.append(skill_name)

    # Disambiguation for ambiguous keywords (when multiple skills matched or keyword is ambiguous)
    for ambiguous_kw, rules in disambiguation.items():
        if ambiguous_kw in message_lower:
            for rule in rules:
                context_words = rule.get("context", [])
                if any(ctx in message_lower for ctx in context_words):
                    skill = rule.get("skill", "")
                    if skill and skill not in matched_skills:
                        matched_skills.append(skill)
                    break

    return matched_skills


def _get_technical_keywords(message_lower: str, router_rules: dict) -> list[str]:
    """Extrait les mots-cles techniques detectes."""
    all_keywords = set()

    # Collect all keywords from router rules
    for skill_info in router_rules.get("skills", {}).values():
        for kw in skill_info.get("primary", []):
            all_keywords.add(kw.lower())
        for kw in skill_info.get("secondary", []):
            all_keywords.add(kw.lower())

    # Fallback if no rules loaded
    if not all_keywords:
        all_keywords = _FALLBACK_KEYWORDS

    return [kw for kw in all_keywords if kw in message_lower]

# Prefixes de questions en francais et anglais
QUESTION_STARTERS = (
    "pourquoi", "comment", "quoi", "quel", "quelle",
    "est-ce", "peut-on", "how", "what", "why", "where",
    "when", "which", "can", "does", "is",
)


def classify_message(message: str) -> str:
    """Classifie le message: command|question|instruction|debug."""
    stripped = message.strip()

    if stripped.startswith("/"):
        return "command"

    lower = stripped.lower()
    if "?" in stripped or lower.startswith(QUESTION_STARTERS):
        return "question"

    if any(kw in lower for kw in ("fix", "debug", "error", "bug", "crash", "traceback")):
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
        explicit_skills = SKILL_COMMAND_RE.findall(message)

        # Load router rules from cache (shared with load_context)
        ctx_cache = get_or_compute_context()
        router_rules = ctx_cache.get("router_rules", _load_router_rules())
        message_lower = message.lower()
        routed_skills = _detect_skill_from_keywords(message_lower, router_rules)
        keywords = _get_technical_keywords(message_lower, router_rules)

        entry = {
            "timestamp": now_paris(),
            "session_id": session_id,
            "message_type": msg_type,
            "explicit_commands": explicit_skills[:5],
            "routed_skills": routed_skills[:3],
            "keywords": keywords[:10],
            "message_length": len(message),
            "message_preview": message[:100],
        }

        append_jsonl(LOGS_DIR / "prompt-log.jsonl", entry)

        log_audit("prompt_analyzer", "user_input", {
            "type": msg_type,
            "explicit": explicit_skills[:5],
            "routed": routed_skills[:3],
            "keywords_count": len(keywords),
        })

        # Inject additionalContext for skill routing + memory
        context_parts = []
        if explicit_skills:
            context_parts.append(f"Detected skill commands: {', '.join(explicit_skills[:3])}")
        if routed_skills:
            context_parts.append(f"Routed skills: {', '.join(routed_skills[:3])}")
        if keywords:
            context_parts.append(f"Technical keywords: {', '.join(keywords[:5])}")
        if msg_type == "debug":
            context_parts.append("Request type: debugging/troubleshooting")

        # Memory v2: injection contextuelle de memoires par prompt
        try:
            from lib.memory_retriever import retrieve_for_prompt
            memory_context = retrieve_for_prompt(message, session_id)
            if memory_context:
                context_parts.append(f"Memory: {memory_context}")
        except Exception:
            pass  # Fail-open

        if context_parts:
            output_json({"additionalContext": " | ".join(context_parts)})

    except Exception as e:
        log_audit("prompt_analyzer", "error", {"error": str(e)})

    sys.exit(0)


if __name__ == "__main__":
    main()
