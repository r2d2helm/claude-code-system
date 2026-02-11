# Système Vocal PAI v2.5

## Vue d'ensemble

Serveur HTTP TTS local utilisant ElevenLabs API (ou fallback macOS say). Donne une voix au DA pour notifications et alertes.

## Architecture

```
$PAI_DIR/VoiceServer/
├── server.ts              # Serveur HTTP Bun (port 8888)
├── install.sh             # Script installation
├── start.sh               # Démarrer le serveur
├── stop.sh                # Arrêter le serveur
├── restart.sh             # Redémarrer
├── status.sh              # Vérifier état
├── uninstall.sh           # Désinstallation propre
└── voices.json            # Configuration voix par agent
```

## Port et endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `http://localhost:8888/health` | GET | Health check |
| `http://localhost:8888/speak` | POST | TTS : `{ "text": "...", "voice": "..." }` |
| `http://localhost:8888/notify` | POST | Notification : `{ "message": "...", "type": "..." }` |

## Chaîne audio

### Linux (Ubuntu)
```
ElevenLabs API → MP3 → mpg123 (ou mpv fallback)
                                ↓
                        notify-send (notification desktop)
```

**Priorité lecteur audio Linux** : mpg123 → mpv → snap/mpv → warning utilisateur

### macOS
```
ElevenLabs API → MP3 → afplay
                         ↓
                  osascript (notification native)
```

## Détection plateforme

Le serveur utilise `process.platform` :
```typescript
if (process.platform === 'darwin') {
  // afplay + osascript
} else if (process.platform === 'linux') {
  // mpg123/mpv + notify-send
}
```

## Configuration voix (voices.json)

```json
{
  "default": {
    "voiceId": "21m00Tcm4TlvDq8ikWAM",
    "stability": 0.35,
    "similarity_boost": 0.80,
    "style": 0.90,
    "speed": 1.1
  },
  "architect": {
    "voiceId": "...",
    "stability": 0.40,
    "similarity_boost": 0.75
  },
  "engineer": {
    "voiceId": "...",
    "stability": 0.30,
    "similarity_boost": 0.85
  }
}
```

## Prérequis Linux

| Paquet | Commande installation | Rôle |
|--------|----------------------|------|
| mpg123 | `sudo apt install mpg123` | Lecture MP3 (prioritaire) |
| mpv | `sudo apt install mpv` | Lecture MP3 (fallback) |
| libnotify-bin | `sudo apt install libnotify-bin` | `notify-send` pour notifications desktop |
| Bun | `curl -fsSL https://bun.sh/install \| bash` | Runtime serveur |

## Auto-start Linux (systemd user service)

```ini
# ~/.config/systemd/user/pai-voice.service
[Unit]
Description=PAI Voice Server
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/.claude/VoiceServer
ExecStart=/home/%u/.bun/bin/bun run server.ts
Restart=on-failure
RestartSec=5
Environment=ELEVENLABS_API_KEY=your-key-here

[Install]
WantedBy=default.target
```

### Commandes systemd

```bash
# Activer auto-start
systemctl --user enable pai-voice.service

# Démarrer
systemctl --user start pai-voice.service

# Vérifier état
systemctl --user status pai-voice.service

# Logs
journalctl --user -u pai-voice.service -f

# Désactiver
systemctl --user disable pai-voice.service
```

## Auto-start macOS (LaunchAgent)

```xml
<!-- ~/Library/LaunchAgents/com.pai.voiceserver.plist -->
<plist version="1.0">
<dict>
    <key>Label</key><string>com.pai.voiceserver</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/bun</string>
        <string>run</string>
        <string>server.ts</string>
    </array>
    <key>WorkingDirectory</key><string>~/.claude/VoiceServer</string>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
</dict>
</plist>
```

## Clé API ElevenLabs

Stockée dans `$PAI_DIR/.env` :
```
ELEVENLABS_API_KEY=sk-...
```

Le serveur lit cette variable au démarrage. Sans clé, le fallback est utilisé (say sur macOS, pas de voix sur Linux).

## Diagnostic

```bash
# Vérifier que le serveur tourne
curl -s http://localhost:8888/health

# Tester TTS
curl -X POST http://localhost:8888/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"Test vocal","voice":"default"}'

# Vérifier mpg123
which mpg123 && echo "mpg123 OK" || echo "mpg123 ABSENT"

# Vérifier notify-send
which notify-send && echo "notify-send OK" || echo "notify-send ABSENT"

# Vérifier clé API
grep ELEVENLABS_API_KEY $PAI_DIR/.env

# Logs serveur (si systemd)
journalctl --user -u pai-voice.service --no-pager -n 20

# Port 8888 utilisé ?
ss -tlnp | grep 8888
```
