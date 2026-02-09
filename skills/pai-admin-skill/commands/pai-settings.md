# /pai-settings — Voir/valider settings.json

Voir et valider le fichier settings.json de PAI.

## Syntaxe

```
/pai-settings [action]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `action` | `show`, `validate`, `diff` | `show` |

## Procedure

### show
1. Lire `~/.claude/settings.json`
2. Afficher les sections principales :
   - `paiVersion`
   - `daidentity` (nom, persona)
   - `principal` (nom)
   - `hooks` (nombre par evenement)
   - `permissions` (allow/deny count)
   - `env` (variables definies, sans valeurs sensibles)
   - `mcpServers` (noms des serveurs)
   - `contextFiles` (fichiers charges)

### validate
1. Lire `~/.claude/settings.json`
2. Verifier structure obligatoire :
   - `hooks` existe et contient les 7 evenements
   - `permissions` existe avec `allow` et `deny`
   - `env` contient `TIME_ZONE`, `ELEVENLABS_API_KEY`
   - `contextFiles` contient au moins `SKILL.md`
3. Verifier coherence hooks :
   - Chaque hook reference un fichier `.hook.ts` existant dans `~/.claude/hooks/`
   - Les matchers sont valides (pas de regex cassee)
4. Verifier permissions :
   - `Bash(rm -rf *)` dans deny
   - `Bash(chmod 777)` dans deny
5. Afficher rapport : section | statut | detail

### diff
1. Lire `~/.claude/settings.json` (installe)
2. Lire `/home/r2d2helm/Personal_AI_Infrastructure/Releases/v2.5/.claude/settings.json` (reference)
3. Comparer section par section :
   - Hooks manquants ou en trop
   - Permissions differentes
   - Variables env manquantes
4. Afficher tableau des differences
