# Wizard : Audit Securite Complet

Audit de securite interactif et methodique de l'installation PAI.

## Etape 1 : Inventaire

1. Lister tous les composants PAI installes
2. Identifier les surfaces d'attaque :
   - Fichiers de configuration
   - Hooks executables
   - Services reseau (ports ouverts)
   - Fichiers contenant des secrets
   - Permissions fichiers

## Etape 2 : SecurityValidator

1. Verifier que SecurityValidator est actif :
   ```bash
   cat ~/.claude/settings.json | jq '.hooks.PreToolUse[] | select(.matcher == "Bash")'
   ```
2. Verifier les matchers (doit couvrir Bash, Edit, Write, Read)
3. Tester avec payloads dangereux :
   ```bash
   # Test CATASTROPHIC
   echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | bun run ~/.claude/hooks/SecurityValidator.hook.ts
   # Attendu : exit 2

   # Test ALLOW
   echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | bun run ~/.claude/hooks/SecurityValidator.hook.ts
   # Attendu : exit 0
   ```
4. Afficher resultats tests

## Etape 3 : Permissions fichiers

1. Verifier .env :
   ```bash
   stat -c "%a %U" ~/.claude/.env 2>/dev/null
   ```
   - Attendu : 600 (lecture/ecriture proprietaire uniquement)
   - Si 644 ou plus : `chmod 600 ~/.claude/.env`

2. Verifier settings.json :
   ```bash
   stat -c "%a" ~/.claude/settings.json
   ```

3. Verifier hooks :
   ```bash
   ls -la ~/.claude/hooks/*.hook.ts
   ```

4. Verifier pas de fichiers world-writable :
   ```bash
   find ~/.claude/ -perm -o+w -type f 2>/dev/null
   ```

## Etape 4 : Secrets

1. Scanner settings.json pour secrets :
   ```bash
   grep -iE "api_key|password|secret|token|private" ~/.claude/settings.json
   ```
   - Aucun secret ne doit etre dans settings.json
   - Tous les secrets doivent etre dans .env

2. Scanner MEMORY/ pour fuites :
   ```bash
   grep -riE "api_key|password|secret|token" ~/.claude/MEMORY/ 2>/dev/null | head -10
   ```

3. Verifier .pai-protected.json :
   ```bash
   cat ~/.claude/.pai-protected.json 2>/dev/null
   ```
   - Verifier que ~/.ssh/, ~/.gnupg/, ~/.aws/ sont proteges

## Etape 5 : Services reseau

1. Lister les ports PAI ouverts :
   ```bash
   ss -tlnp | grep -E "8888|4000"
   ```
2. Verifier que les services ecoutent uniquement sur localhost :
   - Voice server : doit etre sur 127.0.0.1:8888
   - Observability : doit etre sur 127.0.0.1:4000
3. Si expose sur 0.0.0.0 → WARNING : reconfigurer pour localhost uniquement

## Etape 6 : Rapport et recommandations

Generer un rapport structure :
```
=== Audit Securite PAI ===
Date: YYYY-MM-DD

[PASS] SecurityValidator actif (4 matchers)
[PASS] SecurityValidator bloque rm -rf /
[WARN] .env permissions 644 → corrige a 600
[PASS] Pas de secrets dans settings.json
[PASS] MEMORY/ propre
[WARN] .pai-protected.json absent → creer
[PASS] Services ecoutent sur localhost

Score: 5/7 checks passes, 2 warnings

Recommandations :
1. Creer .pai-protected.json avec chemins sensibles
2. Verifier regulierement les logs MEMORY/
```

Proposer d'appliquer les corrections automatiquement.
