# /pai-logs — Lire les logs MEMORY/

Consulter les logs et historique dans MEMORY/.

## Syntaxe

```
/pai-logs [type] [--last <n>]
```

## Parametres

| Parametre | Description | Defaut |
|-----------|-------------|--------|
| `type` | `sessions`, `learnings`, `ratings`, `sentiment` | `sessions` |
| `--last` | Nombre d'entrees a afficher | 5 |

## Procedure

1. Selon le type :
   - **sessions** : Lire les derniers fichiers dans `MEMORY/History/`
   - **learnings** : Lire les derniers fichiers dans `MEMORY/Learning/insights/`
   - **ratings** : Lire les derniers fichiers dans `MEMORY/Signals/ratings/`
   - **sentiment** : Lire les derniers fichiers dans `MEMORY/Signals/sentiment/`
2. Trier par date (plus recent en premier)
3. Afficher les N derniers
4. Pour les sessions, afficher un resume (date, duree, actions principales)
