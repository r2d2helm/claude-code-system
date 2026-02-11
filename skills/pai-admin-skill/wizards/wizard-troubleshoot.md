# Wizard : Depannage Interactif PAI

Arbre de decision interactif pour diagnostiquer et resoudre les problemes PAI.

## Point d'entree

Demander via AskUserQuestion :
- "Quel probleme rencontrez-vous ?"
  - PAI ne demarre pas / pas de greeting
  - Les hooks ne fonctionnent pas
  - Le serveur vocal ne marche pas
  - Le dashboard observability est inaccessible
  - Erreur dans settings.json
  - Autre probleme

## Branche : PAI ne demarre pas

1. Verifier settings.json existe :
   ```bash
   ls ~/.claude/settings.json
   ```
   - Si absent → "PAI n'est pas installe. Lancer /pai-install"
   - Si present → continuer

2. Verifier JSON valide :
   ```bash
   cat ~/.claude/settings.json | jq . > /dev/null
   ```
   - Si invalide → Executer `/pai-fix-settings json`
   - Si valide → continuer

3. Verifier contextFiles :
   ```bash
   cat ~/.claude/settings.json | jq '.contextFiles'
   ```
   - Si manquant ou vide → Ajouter "skills/PAI/SKILL.md"
   - Si present → verifier que les fichiers references existent

4. Verifier CORE skill :
   ```bash
   ls ~/.claude/skills/PAI/SKILL.md
   ```
   - Si absent → Reinstaller CORE : `/pai-pack-install pai-core-install`

## Branche : Hooks ne fonctionnent pas

1. "Avez-vous redemarre Claude Code apres l'installation ?"
   - Non → "Redemarrez Claude Code et retestez"
   - Oui → continuer

2. Verifier hooks enregistres :
   ```bash
   cat ~/.claude/settings.json | jq '.hooks | keys'
   ```
   - Si pas de hooks → Executer `/pai-fix-hooks registration`
   - Si hooks presents → continuer

3. Verifier fichiers hooks :
   ```bash
   ls ~/.claude/hooks/*.hook.ts | wc -l
   ```
   - Si < 15 → Executer `/pai-fix-hooks missing`
   - Si 15 → continuer

4. Tester un hook manuellement :
   ```bash
   echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | bun run ~/.claude/hooks/SecurityValidator.hook.ts
   echo $?
   ```
   - Si erreur Bun → Verifier version Bun, reinstaller si necessaire
   - Si exit 0 → Hooks fonctionnent, probleme peut etre specifique

## Branche : Serveur vocal

1. Verifier installation :
   ```bash
   ls ~/.claude/VoiceServer/server.ts
   ```
   - Si absent → "Voice system non installe. Lancer /pai-pack-install pai-voice-system"

2. Verifier prerequis :
   - `which bun` → Bun OK ?
   - `which mpg123` → mpg123 OK ?
   - Si manquant → installer

3. Verifier port :
   ```bash
   ss -tlnp | grep 8888
   ```
   - Si occupe par autre process → identifier et resoudre conflit
   - Si libre → demarrer le serveur

4. Demarrer et tester :
   ```bash
   cd ~/.claude/VoiceServer && bun run server.ts &
   sleep 2
   curl -s http://localhost:8888/health
   ```

5. Si pas de son mais serveur OK :
   - Verifier mpg123 fonctionne : `mpg123 --test /dev/null`
   - Verifier PulseAudio/PipeWire : `pactl info`
   - Verifier ELEVENLABS_API_KEY dans .env

## Branche : Dashboard observability

1. Verifier installation :
   ```bash
   ls ~/.claude/observability/manage.sh
   ```
   - Si absent → "Observability non installe. Lancer /pai-pack-install pai-observability-server"

2. Verifier dependances :
   ```bash
   ls ~/.claude/observability/apps/server/node_modules/
   ls ~/.claude/observability/apps/client/node_modules/
   ```
   - Si absent → `cd apps/server && bun install && cd ../client && bun install`

3. Demarrer et tester :
   ```bash
   ~/.claude/observability/manage.sh start
   sleep 3
   curl -s http://localhost:4000/
   ```

## Branche : Erreur settings.json

1. Executer `/pai-fix-settings all`
2. Si echec, proposer restauration depuis backup :
   ```bash
   ls ~/backups/pai/
   ```

## Branche : Autre

1. Executer `/pai-diagnose` pour diagnostic complet
2. Analyser le rapport
3. Proposer les corrections adaptees
4. Si non resolu, consulter `lib/knowledge/troubleshooting-kb.md`
