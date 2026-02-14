"""PostToolUse hook (Write): notifie quand un fichier markdown est ecrit.

Cross-platform: fonctionne sur Windows et Linux.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.utils import read_stdin_json


def main():
    try:
        input_data = read_stdin_json()
        tool_input = input_data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")

        if file_path and file_path.endswith(".md"):
            print(f"[hook] Markdown saved: {file_path}", file=sys.stderr)

    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
