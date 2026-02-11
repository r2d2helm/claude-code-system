# /pai-release-install — Installer depuis release v2.5

Installer PAI depuis la release pre-configuree v2.5. Methode recommandee pour une premiere installation.

## Syntaxe

```
/pai-release-install [--no-wizard]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `--no-wizard` | Copier sans lancer le wizard interactif | Non |

## Source

`/home/r2d2helm/Personal_AI_Infrastructure/Releases/v2.5/.claude/`

## Procedure

1. Verifier prerequis (`/pai-prereqs`)
2. **CRITIQUE** : Sauvegarder `~/.claude/settings.json` existant :
   ```bash
   cp ~/.claude/settings.json ~/.claude/settings.json.bak-$(date +%Y%m%d-%H%M%S)
   ```
3. Sauvegarder tout skills/ custom existant
4. Copier la release vers `~/.claude/` :
   ```bash
   cp -r /home/r2d2helm/Personal_AI_Infrastructure/Releases/v2.5/.claude/* ~/.claude/
   ```
5. **FUSION settings.json** (ne pas ecraser) :
   - Lire le backup settings.json
   - Lire le nouveau settings.json PAI
   - Preserver : `mcpServers`, sections custom utilisateur
   - Ajouter : hooks PAI, permissions PAI, env PAI, contextFiles, daidentity, principal
   - Fusionner les tableaux permissions.ask
6. Configurer identite R2D2 :
   - `daidentity.name` = "R2D2"
   - `daidentity.fullName` = "R2D2 - Personal AI"
   - Demander `principal.name`
   - Demander `principal.timezone`
7. Si Bun disponible, lancer le wizard :
   ```bash
   cd ~/.claude && bun run INSTALL.ts
   ```
8. Executer `/pai-verify` pour confirmer l'installation
9. Rappeler de redemarrer Claude Code pour activer les hooks
