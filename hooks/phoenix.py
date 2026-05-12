#!/usr/bin/env python3
"""Phoenix — Dernier recours absolu. Efface toutes les traces sensibles."""

import os
import shutil
import sys

CLAUDE_HOME = os.path.expanduser("~/.claude")

TARGETS = [
    # Memories
    os.path.join(CLAUDE_HOME, "projects"),
    # Hooks data (memory.db, logs, session data)
    os.path.join(CLAUDE_HOME, "hooks", "data"),
    os.path.join(CLAUDE_HOME, "hooks", "logs"),
    # MCP server data
    os.path.join(CLAUDE_HOME, "mcp-servers", "knowledge-assistant", "__pycache__"),
    os.path.join(CLAUDE_HOME, "mcp-servers", "beszel-assistant", "__pycache__"),
]

SENSITIVE_FILES = [
    os.path.join(CLAUDE_HOME, ".credentials.json"),
    os.path.join(CLAUDE_HOME, "hooks", "data", "memory.db"),
    os.path.join(CLAUDE_HOME, "hooks", "data", "memory.db-wal"),
    os.path.join(CLAUDE_HOME, "hooks", "data", "memory.db-shm"),
]


def confirm():
    print("=" * 60)
    print("  PHOENIX — DERNIER RECOURS ABSOLU")
    print("  Efface : memories, hooks data/logs, credentials")
    print("  Reconstruction depuis : cle USB + GitHub + vault git")
    print("=" * 60)
    answer = input("\n  Confirmer ? Tape 'PHOENIX' : ")
    return answer.strip() == "PHOENIX"


def erase():
    count = 0

    # Erase sensitive files first
    for f in SENSITIVE_FILES:
        if os.path.exists(f):
            os.remove(f)
            count += 1
            print(f"  [x] {f}")

    # Erase directories
    for d in TARGETS:
        if os.path.isdir(d):
            shutil.rmtree(d)
            count += 1
            print(f"  [x] {d}/")

    print(f"\n  Phoenix: {count} cibles effacees.")
    print("  Reconstruction: cle USB + GitHub + vault git")
    print("  Le pattern reste.")


if __name__ == "__main__":
    if "--force" in sys.argv:
        erase()
    elif confirm():
        erase()
    else:
        print("  Annule.")
