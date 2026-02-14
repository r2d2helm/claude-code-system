"""SubagentStop hook: capture un resume des resultats de chaque subagent.

Lit le transcript JSONL du subagent, extrait les metriques cles,
et log un resume dans subagent-log.jsonl.
"""

import sys
import json
from pathlib import Path
from collections import Counter

# Ajouter le dossier hooks au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import LOGS_DIR
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris


def parse_subagent_transcript(transcript_path: str, max_lines: int = 50) -> dict:
    """Parse les dernieres lignes du transcript subagent.

    Retourne un dict avec les metriques extraites.
    """
    tools_used = Counter()
    files_modified = set()
    agent_name = "unknown"
    description = ""
    first_timestamp = None
    last_timestamp = None
    outcome_summary = ""
    message_count = 0

    try:
        path = Path(transcript_path)
        if not path.exists():
            return {"error": "transcript not found"}

        # Lire les dernieres max_lines lignes pour performance (deque O(1))
        from collections import deque as _deque
        lines = _deque(maxlen=max_lines)
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                lines.append(line)

        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            message_count += 1

            # Extraire timestamps
            ts = entry.get("timestamp")
            if ts:
                if first_timestamp is None:
                    first_timestamp = ts
                last_timestamp = ts

            if entry.get("type") != "assistant":
                continue

            content = entry.get("message", {}).get("content", [])
            if not isinstance(content, list):
                continue

            for block in content:
                if not isinstance(block, dict):
                    continue

                if block.get("type") == "tool_use":
                    tool_name = block.get("name", "")
                    tool_input = block.get("input", {})
                    tools_used[tool_name] += 1

                    # Detecter le nom de l'agent depuis un appel Task
                    if tool_name == "Task":
                        desc = tool_input.get("description", "")
                        if desc:
                            description = desc
                        agent_type = tool_input.get("subagent_type", "")
                        if agent_type:
                            agent_name = agent_type

                    # Extraire fichiers modifies
                    if tool_name in ("Write", "Edit", "NotebookEdit"):
                        fp = tool_input.get("file_path") or tool_input.get("notebook_path")
                        if fp:
                            files_modified.add(fp)

                # Extraire la derniere reponse texte comme outcome
                if block.get("type") == "text":
                    text = block.get("text", "")
                    if text and len(text) > 10:
                        outcome_summary = text[:200]

    except Exception as e:
        return {"error": str(e)}

    # Calculer duree approximative
    duration_s = None
    if first_timestamp and last_timestamp:
        try:
            from datetime import datetime
            fmt_patterns = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ",
                            "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z"]
            t1 = t2 = None
            for fmt in fmt_patterns:
                try:
                    t1 = datetime.strptime(first_timestamp, fmt)
                    break
                except ValueError:
                    continue
            for fmt in fmt_patterns:
                try:
                    t2 = datetime.strptime(last_timestamp, fmt)
                    break
                except ValueError:
                    continue
            if t1 and t2:
                duration_s = int((t2 - t1).total_seconds())
        except Exception:
            pass

    return {
        "agent_name": agent_name,
        "description": description,
        "message_count": message_count,
        "tools_used": dict(tools_used),
        "files_modified": list(files_modified),
        "duration_s": duration_s,
        "outcome_summary": outcome_summary,
    }


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
            "tools": len(result.get("tools_used", {})),
            "files_modified": len(result.get("files_modified", [])),
        })

    except Exception as e:
        log_audit("subagent_capture", "error", {"error": str(e)})

    # Toujours exit 0 - logging silencieux
    sys.exit(0)


if __name__ == "__main__":
    main()
