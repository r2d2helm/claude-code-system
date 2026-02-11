# Wizard : Configuration Voix ElevenLabs

Assistant interactif pour configurer le systeme vocal PAI avec ElevenLabs.

## Etape 1 : Prerequis

1. Verifier Bun installe : `which bun`
2. Verifier mpg123 installe : `which mpg123`
   - Si absent : `sudo apt install mpg123`
3. Verifier VoiceServer installe :
   ```bash
   ls ~/.claude/VoiceServer/server.ts
   ```
   - Si absent → Installer d'abord : `/pai-pack-install pai-voice-system`

## Etape 2 : Cle API ElevenLabs

Demander via AskUserQuestion :
- "Avez-vous une cle API ElevenLabs ?"
  - Oui, je l'ai
  - Non, je veux m'inscrire
  - Non, je veux utiliser sans voix (mode silencieux)

Si oui :
1. Demander la cle (ne pas afficher en clair dans les logs)
2. Ecrire dans ~/.claude/.env :
   ```bash
   echo "ELEVENLABS_API_KEY=<cle>" >> ~/.claude/.env
   chmod 600 ~/.claude/.env
   ```

Si inscription :
1. Indiquer : "Allez sur https://elevenlabs.io pour creer un compte"
2. "Le plan gratuit offre 10 000 caracteres/mois"
3. "Trouvez votre cle API dans Profile > API Keys"
4. Revenir a ce wizard une fois la cle obtenue

## Etape 3 : Selection voix

Demander via AskUserQuestion :
- "Quel type de voix pour R2D2 ?"
  - Voix masculine professionnelle
  - Voix feminine professionnelle
  - Voix neutre/androgyne
  - Je choisirai plus tard

Mettre a jour settings.json :
```json
{
  "daidentity": {
    "voiceId": "<id-voix-selectionnee>",
    "voice": {
      "stability": 0.35,
      "similarity_boost": 0.80,
      "style": 0.90,
      "speed": 1.1,
      "use_speaker_boost": true,
      "volume": 0.8
    }
  }
}
```

## Etape 4 : Auto-start

Demander via AskUserQuestion :
- "Voulez-vous que le serveur vocal demarre automatiquement ?"
  - Oui (systemd service)
  - Non (demarrage manuel)

Si oui :
```bash
mkdir -p ~/.config/systemd/user/
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

systemctl --user daemon-reload
systemctl --user enable pai-voice.service
systemctl --user start pai-voice.service
```

## Etape 5 : Test

1. Verifier que le serveur tourne :
   ```bash
   curl -s http://localhost:8888/health
   ```
2. Tester TTS :
   ```bash
   curl -X POST http://localhost:8888/speak \
     -H "Content-Type: application/json" \
     -d '{"text":"R2D2 voice system operational","voice":"default"}'
   ```
3. Verifier que le son est audible
4. Si pas de son : verifier mpg123, PulseAudio, volume systeme
5. Confirmer le succes
