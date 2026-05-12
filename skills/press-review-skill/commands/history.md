# Commande: /press-history

Consulter l'historique des revues de presse effectuees.

## Syntaxe

```
/press-history [--month=YYYY-MM] [--limit=N]
```

## Arguments

| Argument | Description | Defaut |
|----------|-------------|--------|
| `--month` | Filtrer par mois | Tous |
| `--limit` | Nombre de revues a afficher | 10 |

## Processus

### 1. Charger l'historique

- Lire `data/history.json`
- Filtrer par mois si `--month` specifie
- Trier par date decroissante

### 2. Afficher le tableau

```
=== Historique des revues ===

| Date       | Type    | Articles | Score moy | Categories            | Note vault |
|------------|---------|----------|-----------|----------------------|------------|
| 2026-03-25 | review  | 12       | 3.8       | IT, Biz, Strat       | Oui        |
| 2026-03-24 | quick   | 8        | -         | Toutes                | Non        |
| 2026-03-22 | review  | 15       | 3.2       | Toutes                | Oui        |
| 2026-03-20 | digest  | -        | 3.5       | Hebdo                 | Oui        |

Total : 4 revues ce mois | 35 articles analyses | Score moyen : 3.5
```

### 3. Details d'une revue

Si une seule revue correspond (ex: `--month=2026-03 --limit=1`), afficher les details :
- Liste des articles avec titre, source, score
- Lien vers la note vault si elle existe

## Format history.json

```json
{
  "reviews": [
    {
      "date": "2026-03-25",
      "type": "review",
      "categories": ["IT_Tech", "Business_Reglementaire", "Strategique"],
      "articles_found": 24,
      "articles_retained": 12,
      "avg_score": 3.8,
      "vault_note": "References/2026-03-25_Press-Review.md",
      "duration_seconds": 145
    }
  ]
}
```

## Exemples

### 10 dernieres revues
```
/press-history
```

### Revues de mars 2026
```
/press-history --month=2026-03
```

### 5 dernieres revues
```
/press-history --limit=5
```
