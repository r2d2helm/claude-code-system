# /pai-status — Etat complet du systeme PAI

Afficher l'etat complet de l'installation PAI.

## Syntaxe

```
/pai-status
```

## Procedure

1. Verifier si PAI est installe : `ls ~/.claude/settings.json`
2. Si non installe, afficher message et proposer `/pai-install`
3. Si installe, collecter :
   - Version PAI : `cat ~/.claude/settings.json | jq -r '.paiVersion'`
   - Nom DA : `cat ~/.claude/settings.json | jq -r '.daidentity.name'`
   - Nom principal : `cat ~/.claude/settings.json | jq -r '.principal.name'`
   - Nombre hooks : `ls ~/.claude/hooks/*.hook.ts 2>/dev/null | wc -l`
   - Nombre skills : `ls ~/.claude/skills/ 2>/dev/null | wc -l`
   - MEMORY : `ls ~/.claude/MEMORY/ 2>/dev/null`
   - Voice server : `curl -s http://localhost:8888/health 2>/dev/null`
   - Observability : `curl -s http://localhost:4000/ 2>/dev/null`
   - Bun version : `bun --version`
4. Afficher tableau complet
