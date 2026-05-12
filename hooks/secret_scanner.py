"""PreToolUse hook (Bash): Scanner de secrets avant git commit.

Intercepte les commandes git commit et verifie que les fichiers stages
ne contiennent pas de secrets (cles API, tokens, mots de passe).

18 patterns couverts: Anthropic, OpenAI, AWS, GitHub, Slack, Stripe, JWT,
private keys, Generic API keys, passwords in URLs.

Exit 2 = bloque le commit. Exit 0 = laisse passer.
Fail-open: exit 0 en cas d'erreur interne.
"""

import sys
import json
import re
import subprocess

# 18 patterns de secrets a detecter
SECRET_PATTERNS = [
    (r'sk-ant-api\w{2}-[\w-]{80,}', 'Anthropic API Key'),
    (r'sk-[a-zA-Z0-9]{20,}', 'OpenAI API Key'),
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
    (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Access Token'),
    (r'gho_[a-zA-Z0-9]{36}', 'GitHub OAuth Token'),
    (r'ghu_[a-zA-Z0-9]{36}', 'GitHub User Token'),
    (r'ghs_[a-zA-Z0-9]{36}', 'GitHub Server Token'),
    (r'xoxb-[0-9]{11,}-[0-9]{11,}-[a-zA-Z0-9]{24}', 'Slack Bot Token'),
    (r'xoxp-[0-9]{11,}-[0-9]{11,}-[a-zA-Z0-9]{24}', 'Slack User Token'),
    (r'sk_live_[a-zA-Z0-9]{24,}', 'Stripe Live Key'),
    (r'rk_live_[a-zA-Z0-9]{24,}', 'Stripe Restricted Key'),
    (r'-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----', 'Private Key'),
    (r'-----BEGIN OPENSSH PRIVATE KEY-----', 'OpenSSH Private Key'),
    (r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}', 'JWT Token'),
    (r'(?i)password\s*[:=]\s*["\'][^"\']{8,}["\']', 'Hardcoded Password'),
    (r'(?i)api[_-]?key\s*[:=]\s*["\'][a-zA-Z0-9]{16,}["\']', 'Generic API Key'),
    (r'(?i)secret\s*[:=]\s*["\'][a-zA-Z0-9+/=]{16,}["\']', 'Generic Secret'),
    (r'://[^:]+:[^@]{8,}@', 'Password in URL'),
]

COMPILED_PATTERNS = [(re.compile(p), name) for p, name in SECRET_PATTERNS]

# Fichiers a ignorer (faux positifs connus)
# secret_scanner.py contient les regex de detection en clair -> auto-exclu
IGNORE_FILES = {'.env.example', '.env.template', 'package-lock.json', 'bun.lockb',
                'secret_scanner.py'}

def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")

    # Seulement intercepter git commit
    if "git commit" not in command:
        sys.exit(0)

    # Recuperer les fichiers stages
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, timeout=10
        )
        staged_files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
    except Exception:
        sys.exit(0)  # Fail-open

    if not staged_files:
        sys.exit(0)

    # Scanner chaque fichier
    findings = []
    for filepath in staged_files:
        if any(filepath.endswith(ig) for ig in IGNORE_FILES):
            continue
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", filepath],
                capture_output=True, text=True, timeout=10
            )
            diff_content = result.stdout
            for pattern, name in COMPILED_PATTERNS:
                matches = pattern.findall(diff_content)
                if matches:
                    # Filtrer les faux positifs (lignes supprimees)
                    for line in diff_content.split('\n'):
                        if line.startswith('+') and not line.startswith('+++'):
                            if pattern.search(line):
                                findings.append(f"  {name} dans {filepath}")
                                break
        except Exception:
            continue

    if findings:
        msg = "SECRET SCANNER: Secrets detectes dans les fichiers stages!\n"
        msg += "\n".join(findings)
        msg += "\n\nCommit bloque. Retirez les secrets avant de commiter."
        print(json.dumps({
            "decision": "block",
            "reason": msg
        }))
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
