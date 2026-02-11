# /pai-memory — Inspecter MEMORY/

Inspecter le systeme de memoire PAI (History, Learning, Signals).

## Syntaxe

```
/pai-memory [tier] [--stats]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `tier` | `history`, `learning`, `signals`, `state` | Tous |
| `--stats` | Afficher statistiques uniquement | Non |

## Procedure

1. Verifier que MEMORY/ existe : `ls ~/.claude/MEMORY/`
2. Si tier specifie, inspecter uniquement ce tier
3. Pour chaque tier :
   - **History** : Compter sessions, afficher les 5 dernieres
   - **Learning** : Compter insights, afficher les 5 derniers
   - **Signals** : Compter ratings et sentiment entries
   - **STATE** : Afficher etat courant (current-work, session-state)
4. Si `--stats`, afficher tableau resume :
   ```
   | Tier | Fichiers | Dernier | Taille |
   |------|----------|---------|--------|
   | History | 42 | 2026-02-09 | 128K |
   | Learning | 15 | 2026-02-08 | 32K |
   | Signals | 23 | 2026-02-09 | 8K |
   ```
5. Signaler si des tiers sont vides (hooks probablement inactifs)
