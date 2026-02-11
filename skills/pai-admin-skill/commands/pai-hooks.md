# /pai-hooks — Lister/inspecter/tester les hooks

Gerer et inspecter les hooks PAI.

## Syntaxe

```
/pai-hooks [action] [nom-hook]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `action` | `list`, `inspect`, `test` | `list` |
| `nom-hook` | Nom du hook (sans .hook.ts) | Tous |

## Procedure

### list
1. Lister tous les fichiers .hook.ts dans `~/.claude/hooks/`
2. Pour chaque hook, extraire l'evenement (depuis settings.json)
3. Afficher tableau : Nom | Evenement | Matcher

### inspect <nom-hook>
1. Lire le fichier `~/.claude/hooks/<nom-hook>.hook.ts`
2. Afficher : evenement, matcher, description, exit codes possibles

### test <nom-hook>
1. Construire un payload JSON de test selon le type de hook
2. Executer : `echo '<payload>' | bun run ~/.claude/hooks/<nom-hook>.hook.ts`
3. Afficher exit code et sortie stdout
