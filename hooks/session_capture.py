"""Stop hook: capture un resume de session dans les logs.

Lit le transcript JSONL, extrait les metriques cles,
et log un resume dans session-log.jsonl.
"""

import sys
import json
from pathlib import Path
from collections import Counter

# Ajouter le dossier hooks au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import LOGS_DIR
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris


def parse_transcript(transcript_path: str, max_lines: int = 200) -> dict:
    """Parse les dernieres lignes du transcript JSONL.

    Retourne un dict avec les metriques extraites.
    """
    tools_used = Counter()
    files_modified = set()
    bash_commands = []
    message_count = 0
    first_timestamp = None
    last_timestamp = None

    try:
        path = Path(transcript_path)
        if not path.exists():
            return {"error": "transcript not found"}

        # Lire les dernieres max_lines lignes pour performance
        lines = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                lines.append(line)
                if len(lines) > max_lines:
                    lines.pop(0)

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

            # Format reel du transcript Claude Code:
            # type="assistant" -> message.content = [{ type: "tool_use", name: "...", input: {...} }]
            if entry.get("type") != "assistant":
                continue

            content = entry.get("message", {}).get("content", [])
            if not isinstance(content, list):
                continue

            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue

                tool_name = block.get("name", "")
                tool_input = block.get("input", {})

                tools_used[tool_name] += 1

                # Extraire fichiers modifies (Write, Edit)
                if tool_name in ("Write", "Edit", "NotebookEdit"):
                    fp = tool_input.get("file_path") or tool_input.get("notebook_path")
                    if fp:
                        files_modified.add(fp)

                # Extraire commandes Bash
                if tool_name == "Bash":
                    cmd = tool_input.get("command", "")
                    if cmd:
                        bash_commands.append(cmd[:100])

    except Exception as e:
        return {"error": str(e)}

    return {
        "message_count": message_count,
        "tools_used": dict(tools_used),
        "files_modified": list(files_modified),
        "bash_commands_count": len(bash_commands),
        "bash_commands_sample": bash_commands[:10],
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
    }


def main():
    try:
        input_data = read_stdin_json()
        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")

        metrics = {}
        if transcript_path:
            metrics = parse_transcript(transcript_path)

        session_summary = {
            "timestamp": now_paris(),
            "session_id": session_id,
            "metrics": metrics,
        }

        # Append dans session-log.jsonl
        append_jsonl(LOGS_DIR / "session-log.jsonl", session_summary)

        log_audit("session_capture", "session_end", {
            "session_id": session_id,
            "messages": metrics.get("message_count", 0),
            "tools": len(metrics.get("tools_used", {})),
            "files_modified": len(metrics.get("files_modified", [])),
        })

    except Exception as e:
        log_audit("session_capture", "error", {"error": str(e)})

    # Toujours exit 0 - logging silencieux
    sys.exit(0)


if __name__ == "__main__":
    main()
