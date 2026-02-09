# Base de connaissances Dépannage PAI v2.5

## Problèmes d'installation

### Bun non installé
**Symptôme** : `bun: command not found`
**Cause** : Bun pas installé ou PATH non configuré
**Solution** :
```bash
curl -fsSL https://bun.sh/install | bash
source ~/.bashrc
bun --version
```

### settings.json non trouvé
**Symptôme** : PAI ne démarre pas, erreur "settings.json not found"
**Cause** : Installation incomplète ou PAI_DIR mal configuré
**Solution** :
```bash
ls -la ~/.claude/settings.json
# Si absent, relancer le wizard :
cd ~/.claude && bun run INSTALL.ts
```

### PAI skill non trouvé
**Symptôme** : "PAI skill not found", pas de routage
**Cause** : CORE skill manquant ou contextFiles mal configuré
**Solution** :
```bash
ls -la ~/.claude/skills/PAI/SKILL.md
cat ~/.claude/settings.json | jq '.contextFiles'
# Vérifier que "skills/PAI/SKILL.md" est dans contextFiles
```

### JSON invalide dans settings.json
**Symptôme** : Hooks ne fonctionnent pas, erreurs parse
**Cause** : Virgule manquante, accolade non fermée, etc.
**Solution** :
```bash
cat ~/.claude/settings.json | jq . > /dev/null 2>&1
# Si erreur, identifier la ligne :
python3 -c "import json; json.load(open('$HOME/.claude/settings.json'))"
```

## Problèmes de hooks

### Hooks ne se déclenchent pas
**Symptôme** : Pas de greeting, pas de validation sécurité
**Causes possibles** :
1. Session pas redémarrée après installation
2. Hooks non enregistrés dans settings.json
3. Fichiers hooks manquants
**Solution** :
```bash
# 1. Vérifier enregistrement
cat ~/.claude/settings.json | jq '.hooks | keys'
# Attendu : PreToolUse, PostToolUse, SessionStart, SessionEnd, Stop, SubagentStop, UserPromptSubmit

# 2. Vérifier fichiers
ls -la ~/.claude/hooks/*.hook.ts

# 3. Redémarrer Claude Code
```

### SecurityValidator ne bloque pas
**Symptôme** : Commandes dangereuses passent
**Cause** : Hook non enregistré sur le bon matcher
**Solution** :
```bash
# Vérifier les matchers PreToolUse
cat ~/.claude/settings.json | jq '.hooks.PreToolUse'
# Doit contenir matchers pour Bash, Edit, Write, Read

# Tester manuellement
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | bun run ~/.claude/hooks/SecurityValidator.hook.ts
echo $?  # Attendu : 2
```

### Hook crashe avec erreur Bun
**Symptôme** : Erreur TypeScript dans les hooks
**Cause** : Version Bun incompatible ou dépendances manquantes
**Solution** :
```bash
bun --version  # Vérifier version récente
cd ~/.claude/hooks && bun install  # Si package.json présent
```

## Problèmes voix

### Voice server ne démarre pas
**Symptôme** : `curl http://localhost:8888/health` échoue
**Causes** :
1. Bun non installé
2. Port 8888 déjà utilisé
3. Erreur dans server.ts
**Solution** :
```bash
# Vérifier port
ss -tlnp | grep 8888

# Démarrer manuellement
cd ~/.claude/VoiceServer && bun run server.ts

# Si erreur, vérifier .env
grep ELEVENLABS_API_KEY ~/.claude/.env
```

### Pas de son sur Linux
**Symptôme** : Voice server OK mais aucun son
**Cause** : mpg123 non installé ou PulseAudio/PipeWire non actif
**Solution** :
```bash
# Vérifier mpg123
which mpg123 || sudo apt install mpg123

# Tester audio
echo "test" | mpg123 -  # ou
mpg123 /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null

# Vérifier PulseAudio
pactl info
```

### Notifications desktop absentes
**Symptôme** : Pas de popup notification
**Cause** : libnotify-bin non installé
**Solution** :
```bash
which notify-send || sudo apt install libnotify-bin
notify-send "Test" "Notification PAI"
```

## Problèmes observability

### Dashboard non accessible
**Symptôme** : `http://localhost:4000` ne répond pas
**Solution** :
```bash
# Vérifier état
~/.claude/observability/manage.sh status

# Vérifier port
ss -tlnp | grep 4000

# Démarrer
~/.claude/observability/manage.sh start

# Si erreur, vérifier dépendances
cd ~/.claude/observability/apps/server && bun install
cd ~/.claude/observability/apps/client && bun install && bun run build
```

## Problèmes mémoire

### MEMORY/ ne se remplit pas
**Symptôme** : Pas de sessions, pas d'apprentissages
**Cause** : Hooks Stop/SessionEnd non actifs
**Solution** :
```bash
ls -la ~/.claude/MEMORY/
# Vérifier structure
ls -la ~/.claude/MEMORY/History/
ls -la ~/.claude/MEMORY/Learning/
ls -la ~/.claude/MEMORY/Signals/

# Vérifier hooks
cat ~/.claude/settings.json | jq '.hooks.Stop'
cat ~/.claude/settings.json | jq '.hooks.SessionEnd'
```

## Problèmes de mise à jour

### Merge settings.json échoue
**Symptôme** : Perte de config MCP après mise à jour
**Cause** : Écrasement au lieu de fusion
**Prévention** :
```bash
# TOUJOURS backup avant update
cp ~/.claude/settings.json ~/.claude/settings.json.bak-$(date +%Y%m%d)

# Vérifier après update que mcpServers est préservé
cat ~/.claude/settings.json | jq '.mcpServers'
```

### Fichiers USER/ écrasés
**Symptôme** : Personnalisations perdues
**Cause** : Update destructif
**Prévention** : Le wizard PAI devrait préserver USER/. Si écrasé :
```bash
# Restaurer depuis backup
cp ~/.claude-BACKUP/skills/PAI/USER/* ~/.claude/skills/PAI/USER/
```

## Diagnostic automatique

Séquence de vérification complète :
```bash
echo "=== PAI Diagnostic ==="
echo "--- Système ---"
uname -a
lsb_release -d 2>/dev/null

echo "--- Prérequis ---"
which bun && bun --version || echo "ERREUR: Bun absent"
which git && git --version || echo "ERREUR: Git absent"
which mpg123 || echo "WARNING: mpg123 absent (voix)"
which notify-send || echo "WARNING: notify-send absent (notifications)"

echo "--- PAI Installation ---"
ls ~/.claude/settings.json 2>/dev/null && echo "settings.json OK" || echo "ERREUR: settings.json absent"
ls ~/.claude/skills/PAI/SKILL.md 2>/dev/null && echo "CORE SKILL OK" || echo "ERREUR: CORE absent"
ls ~/.claude/hooks/ 2>/dev/null && echo "hooks/ OK ($(ls ~/.claude/hooks/*.hook.ts 2>/dev/null | wc -l) hooks)" || echo "ERREUR: hooks/ absent"

echo "--- Services ---"
curl -s http://localhost:8888/health > /dev/null 2>&1 && echo "Voice Server OK" || echo "Voice Server DOWN"
curl -s http://localhost:4000/ > /dev/null 2>&1 && echo "Observability OK" || echo "Observability DOWN"

echo "--- Mémoire ---"
ls ~/.claude/MEMORY/ 2>/dev/null && echo "MEMORY/ OK" || echo "WARNING: MEMORY/ absent"
```
