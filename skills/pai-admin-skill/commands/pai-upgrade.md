# /pai-upgrade — Mettre a jour PAI

Mettre a jour PAI depuis le depot git.

## Syntaxe

```
/pai-upgrade [--check | --apply]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `--check` | Verifier si mise a jour disponible | Oui |
| `--apply` | Appliquer la mise a jour | Non |

## Procedure

### --check (defaut)
1. Aller dans le depot : `cd /home/r2d2helm/Personal_AI_Infrastructure/`
2. Verifier le remote : `git remote -v`
3. Fetch : `git fetch origin`
4. Comparer : `git log HEAD..origin/main --oneline`
5. Afficher les nouvelles versions si disponibles

### --apply
1. **Sauvegarder d'abord** : Executer `/pai-backup`
2. Mettre a jour le depot :
   ```bash
   cd /home/r2d2helm/Personal_AI_Infrastructure/
   git pull origin main
   ```
3. Verifier nouvelle version dans Releases/
4. **FUSIONNER** settings.json (pas ecraser) :
   - Preserver mcpServers, sections custom
   - Mettre a jour hooks, env, permissions PAI
5. Mettre a jour les fichiers CORE si necessaire
6. Reinstaller les hooks mis a jour
7. Executer `/pai-verify`
8. Rappeler de redemarrer Claude Code
