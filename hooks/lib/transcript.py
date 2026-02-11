"""Fonctions partagees pour parser les transcripts Claude Code."""

import json
from pathlib import Path
from collections import Counter


def parse_transcript(transcript_path: str, max_lines: int = 200) -> dict:
    """Parse les dernieres lignes du transcript JSONL.

    Retourne un dict avec les metriques extraites:
    - message_count, tools_used, files_modified
    - bash_commands_count, bash_commands_sample
    - first_timestamp, last_timestamp
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
