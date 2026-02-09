# /pai-fix-settings — Reparer settings.json

Diagnostiquer et reparer les problemes dans settings.json.

## Syntaxe

```
/pai-fix-settings [probleme]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `probleme` | `json`, `hooks`, `env`, `merge`, `all` | `all` |

## Procedure

### json — Reparer JSON invalide
1. Tester : `cat ~/.claude/settings.json | jq . > /dev/null`
2. Si invalide :
   - Identifier l'erreur (ligne, position)
   - Tenter correction automatique (virgules, accolades)
   - Si impossible, restaurer depuis backup
3. Sauvegarder avant modification

### hooks — Reparer section hooks
1. Verifier que chaque hook reference un fichier existant
2. Corriger les chemins (s'assurer que ${PAI_DIR} est utilise)
3. Ajouter les hooks manquants

### env — Reparer variables env
1. Verifier PAI_DIR defini et valide
2. Corriger si pointe vers repertoire inexistant

### merge — Re-fusionner avec template PAI
1. Sauvegarder settings.json actuel
2. Lire template PAI depuis release v2.5
3. Fusionner intelligemment (preserver mcpServers, custom)
4. Ecrire le resultat

### all
1. Sauvegarder : `cp ~/.claude/settings.json ~/.claude/settings.json.bak`
2. Executer json, env, hooks dans l'ordre
3. Valider le resultat
