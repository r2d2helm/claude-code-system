"""Stop hook: capture un resume de session dans les logs.

NOTE: Supersede par memory_extractor.py qui ajoute l'extraction d'insights.
Ce fichier est conserve comme fallback leger.
"""

import sys
from pathlib import Path

# Ajouter le dossier hooks au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import LOGS_DIR
from lib.transcript import parse_transcript
from lib.utils import read_stdin_json, log_audit, append_jsonl, now_paris


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
