# /pai-fix-hooks — Correctifs hooks courants

Appliquer des correctifs pour les problemes de hooks courants.

## Syntaxe

```
/pai-fix-hooks [probleme]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `probleme` | `missing`, `registration`, `permissions`, `all` | `all` |

## Procedure

### missing — Hooks fichiers manquants
1. Lister les hooks attendus (15)
2. Verifier chaque fichier dans ~/.claude/hooks/
3. Si manquant, copier depuis le depot PAI :
   ```bash
   cp /home/r2d2helm/Personal_AI_Infrastructure/Releases/v2.5/.claude/hooks/<hook>.hook.ts ~/.claude/hooks/
   ```

### registration — Hooks non enregistres
1. Lire settings.json hooks section
2. Comparer avec la liste attendue (voir lib/knowledge/hooks-reference.md)
3. Ajouter les hooks manquants dans settings.json
4. Attention : fusionner, pas ecraser les hooks existants

### permissions — Fichiers non executables
1. Verifier permissions des fichiers .hook.ts :
   ```bash
   ls -la ~/.claude/hooks/*.hook.ts
   ```
2. Rendre executables si necessaire :
   ```bash
   chmod +x ~/.claude/hooks/*.hook.ts
   ```

### all
1. Executer missing, registration, permissions dans l'ordre
2. Afficher resume des corrections
3. Rappeler de redemarrer Claude Code
