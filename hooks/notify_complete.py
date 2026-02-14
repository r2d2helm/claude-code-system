"""Notification hook: notifie quand une tache Claude Code est terminee.

Cross-platform:
- Windows: utilise win10toast ou Windows.Forms messagebox
- Linux: utilise notify-send (libnotify)
- macOS: utilise osascript
- Fallback: print sur stderr
"""

import os
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.utils import read_stdin_json


def notify(title: str, message: str) -> None:
    """Send desktop notification cross-platform."""
    try:
        if os.name == "nt":
            # Windows
            subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 f"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; "
                 f"[System.Windows.Forms.MessageBox]::Show('{message}', '{title}', 'OK', 'Information') | Out-Null"],
                capture_output=True, timeout=5,
            )
        elif sys.platform == "darwin":
            # macOS
            subprocess.run(
                ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
                capture_output=True, timeout=5,
            )
        else:
            # Linux - notify-send
            subprocess.run(
                ["notify-send", title, message],
                capture_output=True, timeout=5,
            )
    except Exception:
        print(f"[hook] {title}: {message}", file=sys.stderr)


def main():
    try:
        input_data = read_stdin_json()
        session_id = input_data.get("session_id", "")
        short_id = session_id[:8] if len(session_id) > 8 else session_id
        message = f"Session {short_id} terminee" if short_id else "Task completed"
        notify("Claude Code", message)
    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
