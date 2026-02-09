# /pai-security — Audit securite

Executer un audit de securite du systeme PAI.

## Syntaxe

```
/pai-security [--full]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `--full` | Audit complet (inclut tests actifs) | Non (passif) |

## Procedure

1. **Permissions settings.json** :
   - Verifier listes allow/deny/ask
   - Confirmer que les patterns dangereux sont dans `ask`
   - Verifier qu'aucun wildcard excessif dans `allow`

2. **SecurityValidator** :
   - Verifier hook enregistre sur PreToolUse pour Bash, Edit, Write, Read
   - Verifier fichier hook existe et est lisible

3. **Fichier .env** :
   - Verifier permissions : `stat -c %a ~/.claude/.env` (attendu: 600)
   - Verifier pas de secrets ailleurs dans settings.json

4. **.pai-protected.json** :
   - Verifier existence et contenu
   - Confirmer chemins critiques couverts (~/.ssh/, ~/.gnupg/, ~/.aws/)

5. **Separation SYSTEM/USER** :
   - Verifier que USER/ n'est pas versionne publiquement
   - Verifier pas de donnees personnelles dans SYSTEM/

6. **MEMORY/** :
   - Verifier pas de secrets dans les logs

7. Si `--full` :
   - Tester SecurityValidator avec payload dangereux
   - Verifier que exit code = 2 (BLOCK)

8. Afficher rapport :
   ```
   | Check | Etat | Details |
   |-------|------|---------|
   | Permissions | OK | 18 patterns ask |
   | SecurityValidator | OK | Actif sur 4 matchers |
   | .env perms | WARNING | Mode 644 (devrait etre 600) |
   ```
