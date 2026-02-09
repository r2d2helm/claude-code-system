# Adaptations Linux/Ubuntu pour PAI v2.5

## Statut plateforme

PAI supporte Linux (Ubuntu/Debian) en tant que plateforme de premier rang depuis les correctifs de compatibilité.

## Différences clés macOS → Linux

| Composant | macOS | Linux (Ubuntu) |
|-----------|-------|----------------|
| Audio TTS | `afplay` | `mpg123` (prioritaire) → `mpv` → `snap/mpv` |
| Notifications | `osascript` | `notify-send` (libnotify) |
| Auto-start voix | LaunchAgent plist | systemd user service |
| Auto-start chemin | `~/Library/LaunchAgents/` | `~/.config/systemd/user/` |
| sed in-place | `sed -i ''` (BSD) | `sed -i` (GNU) |
| Homebrew PATH | `/opt/homebrew/bin` | Non applicable |
| Logs système | `~/Library/Logs/` | `~/.config/pai/` ou journalctl |
| Gestionnaire paquets | `brew` | `apt` |

## Paquets à installer

```bash
# Prérequis essentiels
sudo apt update
sudo apt install -y git curl

# Audio (pour voice-system)
sudo apt install -y mpg123

# Notifications desktop
sudo apt install -y libnotify-bin

# Runtime Bun
curl -fsSL https://bun.sh/install | bash
source ~/.bashrc

# Optionnel : mpv comme fallback audio
sudo apt install -y mpv
```

## Détection plateforme dans le code

### Scripts shell
```bash
OS_TYPE="$(uname -s)"
if [ "$OS_TYPE" = "Darwin" ]; then
  # macOS
elif [ "$OS_TYPE" = "Linux" ]; then
  # Linux
fi
```

### TypeScript (Bun)
```typescript
if (process.platform === 'darwin') {
  // macOS
} else if (process.platform === 'linux') {
  // Linux
}
```

## sed GNU vs BSD

PAI a corrigé toutes les occurrences de `sed -i ''` (BSD) pour utiliser la détection plateforme :

```bash
if [ "$(uname -s)" = "Darwin" ]; then
  sed -i '' 's/old/new/' file
else
  sed -i 's/old/new/' file
fi
```

## systemd user service pour voice server

```bash
# Créer le répertoire
mkdir -p ~/.config/systemd/user/

# Créer le fichier service
cat > ~/.config/systemd/user/pai-voice.service << 'EOF'
[Unit]
Description=PAI Voice Server
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/.claude/VoiceServer
ExecStart=%h/.bun/bin/bun run server.ts
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

# Recharger et activer
systemctl --user daemon-reload
systemctl --user enable pai-voice.service
systemctl --user start pai-voice.service
```

## PATH Bun sur Linux

Bun s'installe dans `~/.bun/bin/`. Ajouter au PATH :

```bash
# Ajouté automatiquement par l'installeur Bun dans ~/.bashrc ou ~/.zshrc
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
```

Vérifier :
```bash
which bun
bun --version
```

## Problèmes connus Linux

### 1. manage.sh observability
Le script référence `/opt/homebrew/bin` — corrigé avec vérification conditionnelle :
```bash
[ -d "/opt/homebrew/bin" ] && export PATH="/opt/homebrew/bin:$PATH"
```

### 2. Exemples avec chemins /Users/
La documentation PAI utilise parfois des chemins macOS (`/Users/...`). Sur Linux, utiliser `$HOME` ou `/home/username/`.

### 3. paplay mentionné mais non utilisé
La doc INSTALL.md mentionne `paplay` mais le code utilise mpg123/mpv. Non bloquant.

### 4. MenuBar App (macOS uniquement)
SwiftBar/BitBar pour observability et voice ne sont pas disponibles sur Linux. Le contrôle se fait via CLI (manage.sh, start.sh/stop.sh).

## Vérification compatibilité Linux

```bash
# Système
uname -s     # Attendu : Linux
lsb_release -d  # Attendu : Ubuntu XX.XX

# Prérequis
which git && echo "git OK"
which curl && echo "curl OK"
which bun && echo "bun OK"
which mpg123 && echo "mpg123 OK"
which notify-send && echo "notify-send OK"

# Services systemd user
systemctl --user list-unit-files | grep pai

# Ports
ss -tlnp | grep -E "8888|4000"
```
