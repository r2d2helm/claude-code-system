# /pai-env — Verifier variables d'environnement

Verifier les variables d'environnement requises par PAI.

## Syntaxe

```
/pai-env [--fix]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `--fix` | Proposer corrections pour les variables manquantes | Non |

## Procedure

1. Lire `~/.claude/settings.json` section `env`
2. Verifier chaque variable attendue :

| Variable | Source | Obligatoire |
|----------|--------|-------------|
| `TIME_ZONE` | settings.json env | Oui |
| `ELEVENLABS_API_KEY` | settings.json env ou `~/.claude/.env` | Non (voice uniquement) |
| `ANTHROPIC_API_KEY` | environnement shell | Non (Claude Code le gere) |
| `BUN_INSTALL` | environnement shell | Oui (si Bun installe) |
| `PATH` | contient `~/.bun/bin` | Oui (si Bun installe) |

3. Pour chaque variable :
   - Verifier si definie dans settings.json `env`
   - Verifier si definie dans `~/.claude/.env`
   - Verifier si disponible dans l'environnement shell (`echo $VAR`)
4. Afficher tableau :
   ```
   | Variable | settings.json | .env | Shell | Statut |
   |----------|--------------|------|-------|--------|
   | TIME_ZONE | America/New_York | - | - | OK |
   | ELEVENLABS_API_KEY | - | ek_... | - | OK |
   ```

### --fix
5. Pour chaque variable manquante obligatoire :
   - `TIME_ZONE` : demander le fuseau horaire, ajouter dans settings.json env
   - `BUN_INSTALL` : verifier `~/.bun/`, proposer `export BUN_INSTALL="$HOME/.bun"` dans `~/.bashrc`
   - `PATH` : proposer ajout `~/.bun/bin` dans `~/.bashrc`
6. Pour les variables optionnelles manquantes :
   - `ELEVENLABS_API_KEY` : proposer wizard-voice-setup
