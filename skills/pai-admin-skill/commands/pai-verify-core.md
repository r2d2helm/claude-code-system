# /pai-verify-core — Verifier CORE skill

Verifier l'integrite du CORE skill PAI.

## Syntaxe

```
/pai-verify-core
```

## Procedure

1. Verifier SKILL.md : `ls ~/.claude/skills/PAI/SKILL.md`
2. Verifier SYSTEM/ : `ls ~/.claude/skills/PAI/SYSTEM/` (attendu: 19 fichiers)
3. Verifier USER/ : `ls ~/.claude/skills/PAI/USER/`
4. Verifier AISTEERINGRULES :
   - `ls ~/.claude/skills/PAI/SYSTEM/AISTEERINGRULES.md`
   - `ls ~/.claude/skills/PAI/USER/AISTEERINGRULES.md`
5. Verifier DAIDENTITY : `ls ~/.claude/skills/PAI/USER/DAIDENTITY.md`
6. Verifier Workflows/ : `ls ~/.claude/skills/PAI/Workflows/` (attendu: 4)
7. Verifier Tools/ : `ls ~/.claude/skills/PAI/Tools/` (attendu: 4)
8. Verifier contextFiles dans settings.json pointe vers SKILL.md
9. Afficher tableau resultats
