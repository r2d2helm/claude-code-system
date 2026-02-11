# /pai-verify — Verification complete du systeme PAI

Executer toutes les verifications PAI : CORE, hooks, voice, observability.

## Syntaxe

```
/pai-verify [composant]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `composant` | `core`, `hooks`, `voice`, `observability` | Tous |

## Procedure

1. Verifier PAI installe : `ls ~/.claude/settings.json`
2. Verifier settings.json valide : `cat ~/.claude/settings.json | jq . > /dev/null`
3. Executer `/pai-verify-core`
4. Executer `/pai-verify-hooks`
5. Executer `/pai-verify-voice` (si VoiceServer/ existe)
6. Executer `/pai-verify-observability` (si observability/ existe)
7. Afficher tableau recapitulatif :
   ```
   | Composant | Etat | Details |
   |-----------|------|---------|
   | CORE | OK | SKILL.md, 19 SYSTEM/ docs |
   | Hooks | OK | 15/15 hooks actifs |
   | Voice | DOWN | Port 8888 inactif |
   | Observability | N/A | Non installe |
   ```
