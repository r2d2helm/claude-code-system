# /pai-voice — Gestion voice server

Gerer le serveur vocal PAI (demarrer, arreter, etat).

## Syntaxe

```
/pai-voice <action>
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `action` | `start`, `stop`, `status`, `restart`, `install` | `status` |

## Procedure

### status
1. Tester health endpoint : `curl -s http://localhost:8888/health`
2. Verifier port : `ss -tlnp | grep 8888`
3. Verifier service systemd : `systemctl --user status pai-voice.service 2>/dev/null`
4. Afficher etat

### start
1. Verifier prerequis (Bun, mpg123)
2. Si systemd service configure :
   ```bash
   systemctl --user start pai-voice.service
   ```
3. Sinon, demarrer manuellement :
   ```bash
   cd ~/.claude/VoiceServer && nohup bun run server.ts > /tmp/pai-voice.log 2>&1 &
   ```
4. Attendre 2s et verifier health

### stop
1. Si systemd : `systemctl --user stop pai-voice.service`
2. Sinon : trouver et tuer le processus :
   ```bash
   pkill -f "bun run server.ts" || true
   ```

### restart
1. Executer stop puis start

### install
1. Rediriger vers `/pai-pack-install pai-voice-system`
