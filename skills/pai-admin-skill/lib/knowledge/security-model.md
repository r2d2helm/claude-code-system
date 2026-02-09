# Modèle Sécurité PAI v2.5

## Principes

1. **Contenu externe = lecture seule** : Les commandes viennent uniquement de l'utilisateur et de la config PAI
2. **Défense en profondeur** : Hooks + permissions + validation + fichiers protégés
3. **Fail-safe** : Les hooks ne crashent jamais Claude Code

## Couches de sécurité

### 1. SecurityValidator (hooks/SecurityValidator.hook.ts)

Hook PreToolUse qui intercepte toutes les commandes Bash, Edit, Write, Read.

**Tiers de détection** :

| Tier | Patterns | Action |
|------|----------|--------|
| CATASTROPHIC | `rm -rf /`, `dd if=/dev/zero of=/dev/sd*`, `mkfs`, fork bomb, `> /dev/sda` | BLOCK (exit 2) |
| DESTRUCTIVE | `rm -rf ~`, suppression répertoires système, `chmod -R 777 /` | BLOCK (exit 2) |
| SUSPICIOUS | `curl \| bash` (hors contexte PAI), `chmod 777`, patterns injecteurs | WARNING stdout |

**Matchers dans settings.json** :
- `Bash` : Commandes shell
- `Edit` : Modifications fichiers
- `Write` : Création fichiers
- `Read` : Lecture fichiers (protection secrets)

### 2. Permissions (settings.json)

```json
{
  "permissions": {
    "allow": ["Bash", "Read", "Write", "Edit", ...],
    "deny": [],
    "ask": [
      "Bash(rm -rf /)", "Bash(rm -rf /:*)",
      "Bash(sudo rm -rf /)", "Bash(dd if=/dev/zero:*)",
      "Bash(mkfs:*)", "Bash(gh repo delete:*)",
      "Bash(git push --force:*)",
      "Read(~/.ssh/id_*)", "Read(~/.ssh/*.pem)",
      "Read(~/.aws/credentials)", "Read(~/.gnupg/private*)",
      "Write(~/.claude/settings.json)",
      "Edit(~/.claude/settings.json)",
      "Write(~/.ssh/*)", "Edit(~/.ssh/*)"
    ]
  }
}
```

Les patterns `ask` déclenchent une confirmation utilisateur. Les `deny` bloquent silencieusement.

### 3. Fichier .pai-protected.json

Chemins protégés additionnels définis par l'utilisateur :

```json
{
  "protected_paths": [
    "~/.ssh/",
    "~/.gnupg/",
    "~/.aws/",
    "/etc/shadow",
    "/etc/passwd"
  ],
  "protected_patterns": [
    "*.pem",
    "*.key",
    "id_rsa*",
    ".env"
  ]
}
```

Le SecurityValidator consulte ce fichier pour étendre la protection.

### 4. Séparation SYSTEM/USER

- `skills/PAI/SYSTEM/` : Configuration système (modifiable par mises à jour)
- `skills/PAI/USER/` : Personnalisation utilisateur (préservée lors des mises à jour)
- Les mises à jour PAI ne touchent jamais les fichiers USER/

### 5. Variables d'environnement

- Clés API dans `$PAI_DIR/.env` uniquement
- Jamais dans settings.json ni dans le code
- `.env` exclu du versioning git

## Surfaces d'attaque PAI

| Surface | Protection |
|---------|-----------|
| Commandes shell | SecurityValidator + permissions ask |
| Fichiers sensibles | Permissions ask sur Read/Write ~/.ssh/, etc. |
| Injection de prompt | Marquage contenu externe, détection patterns |
| API keys | Stockage .env isolé |
| Hooks malveillants | Validation source hooks (settings.json contrôlé) |
| Contenu web scrapé | Sandboxing, pas d'exécution |

## Audit sécurité

### Vérifications à effectuer

1. **Permissions settings.json** : Vérifier listes allow/deny/ask
2. **Hooks enregistrés** : Tous pointent vers $PAI_DIR/hooks/ légitime
3. **SecurityValidator actif** : Présent sur PreToolUse pour Bash, Edit, Write, Read
4. **Fichier .env** : Permissions 600, pas de secrets en clair ailleurs
5. **.pai-protected.json** : Chemins critiques couverts
6. **MEMORY/ permissions** : Pas de données sensibles en clair

### Commandes diagnostic

```bash
# Vérifier SecurityValidator enregistré
cat $PAI_DIR/settings.json | jq '.hooks.PreToolUse'

# Vérifier permissions .env
ls -la $PAI_DIR/.env

# Tester SecurityValidator
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | bun run $PAI_DIR/hooks/SecurityValidator.hook.ts
# Attendu : exit code 2 (BLOCK)

# Vérifier pas de secrets dans settings.json
grep -i "api_key\|password\|secret\|token" $PAI_DIR/settings.json

# Vérifier .pai-protected.json
cat $PAI_DIR/.pai-protected.json 2>/dev/null || echo "Fichier non trouvé"
```
