# /pai-verify-voice — Verifier voice system

Verifier le systeme vocal PAI.

## Syntaxe

```
/pai-verify-voice
```

## Procedure

1. Verifier VoiceServer/ existe : `ls ~/.claude/VoiceServer/`
2. Verifier fichiers : server.ts, start.sh, stop.sh, status.sh, voices.json
3. Verifier mpg123 installe : `which mpg123`
4. Verifier notify-send installe : `which notify-send`
5. Verifier ELEVENLABS_API_KEY dans .env : `grep ELEVENLABS_API_KEY ~/.claude/.env`
6. Tester health endpoint : `curl -s http://localhost:8888/health`
7. Verifier port 8888 : `ss -tlnp | grep 8888`
8. Verifier systemd service (optionnel) : `systemctl --user status pai-voice.service`
9. Afficher tableau resultats
