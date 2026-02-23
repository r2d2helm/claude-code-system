"""Hook PreCompact: sauvegarde le contexte conversation avant auto-compaction.

Appele par Claude Code avant la compaction automatique du contexte.
Extrait les derniers tours de conversation du transcript JSONL et les
stocke dans Memory v2 comme memoires de type 'pre_compact'.

Aucune dependance externe (pas d'Agent SDK). Pure Python + Memory v2.
Design fail-open: exit 0 en cas d'erreur.

Inspire du Second Brain (Dynamous Community), adapte pour AdminSysteme.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Ajouter hooks au path
_HOOKS_DIR = Path(__file__).resolve().parent
if str(_HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(_HOOKS_DIR))

from lib.paths import LOGS_DIR
from lib.utils import read_stdin_json, log_audit, now_paris

# ============================================================
# Configuration
# ============================================================

MAX_TURNS = 30
MAX_CONTEXT_CHARS = 10_000


# ============================================================
# Extraction du contexte conversation
# ============================================================

def _extract_text_from_content(content) -> str:
    """Extrait le texte lisible d'un champ content (str ou list de blocks)."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text", "")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts)

    return ""


def _extract_conversation_turns(transcript_path: str) -> list[dict]:
    """Lit le transcript JSONL et extrait les derniers tours de conversation."""
    turns = []

    try:
        path = Path(transcript_path)
        if not path.exists():
            return []

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Le transcript Claude Code niche le message sous "message"
                msg = entry.get("message")
                if isinstance(msg, dict):
                    role = msg.get("role")
                    content = msg.get("content", "")
                else:
                    role = entry.get("role")
                    content = entry.get("content", "")

                if role not in ("user", "assistant"):
                    continue

                text = _extract_text_from_content(content).strip()
                if not text:
                    continue

                turns.append({"role": role, "text": text})

    except Exception:
        return []

    return turns[-MAX_TURNS:]


def _summarize_turns(turns: list[dict]) -> str:
    """Genere un resume compact des tours de conversation."""
    if not turns:
        return ""

    parts = []
    for turn in turns:
        label = "U" if turn["role"] == "user" else "A"
        # Garder les 200 premiers chars de chaque tour
        text = turn["text"][:200]
        if len(turn["text"]) > 200:
            text += "..."
        parts.append(f"[{label}] {text}")

    summary = "\n".join(parts)

    # Tronquer au max global
    if len(summary) > MAX_CONTEXT_CHARS:
        summary = summary[-MAX_CONTEXT_CHARS:]
        # Trouver la prochaine limite de tour apres la troncature
        boundary = summary.find("\n[")
        if boundary > 0:
            summary = summary[boundary + 1:]

    return summary


# ============================================================
# Stockage Memory v2
# ============================================================

def _store_context_memories(session_id: str, turns: list[dict]) -> int:
    """Stocke le contexte pre-compaction dans Memory v2.

    Strategie: on cree UNE memoire condensee avec le resume des tours.
    Importance haute (7.0) car c'est du contexte qu'on perd sinon.
    """
    try:
        from lib.memory_db import insert_memory

        summary = _summarize_turns(turns)
        if not summary:
            return 0

        # Extraire les topics des messages utilisateur pour les tags
        user_texts = " ".join(t["text"] for t in turns if t["role"] == "user")
        tags = ["pre_compact", "context_save"]

        memory_id = insert_memory({
            "session_id": session_id,
            "type": "pre_compact",
            "content": summary[:500],
            "importance_score": 7.0,
            "tags": tags,
            "source_context": f"pre_compact_flush - {len(turns)} turns",
        })

        return 1 if memory_id else 0

    except Exception:
        return 0


# ============================================================
# Main
# ============================================================

def main():
    try:
        input_data = read_stdin_json()
        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")

        if not transcript_path:
            log_audit("pre_compact_flush", "skip", {"reason": "no transcript_path"})
            sys.exit(0)

        # Extraire les tours de conversation
        turns = _extract_conversation_turns(transcript_path)

        if not turns:
            log_audit("pre_compact_flush", "skip", {"reason": "no turns extracted"})
            sys.exit(0)

        # Stocker dans Memory v2
        stored = _store_context_memories(session_id, turns)

        log_audit("pre_compact_flush", "flush", {
            "session_id": session_id,
            "turns_extracted": len(turns),
            "memories_stored": stored,
        })

    except Exception as e:
        log_audit("pre_compact_flush", "error", {"error": str(e)})

    # Toujours exit 0 - fail-open
    sys.exit(0)


if __name__ == "__main__":
    main()
