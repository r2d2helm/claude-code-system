# Commande: /press-review

Revue de presse complete avec scan web, analyse et generation de note vault.

## Syntaxe

```
/press-review [--category=IT|Business|Concurrence|Strategique] [--days=N] [--dry-run]
```

## Arguments

| Argument | Description | Defaut |
|----------|-------------|--------|
| `--category` | Filtrer sur une seule categorie | Toutes |
| `--days` | Couvrir les N derniers jours | 1 |
| `--dry-run` | Previsualiser sans ecrire la note vault | false |

## Processus

### 1. Charger la configuration

- Lire `data/sources.json` pour les sources actives et requetes de recherche
- Lire `data/seldon-keywords.json` pour le scoring
- Determiner les categories a couvrir (toutes ou filtre)

### 2. Scanner les sources (WebSearch)

Pour chaque categorie active :
- Lancer les requetes de recherche definies dans `sources.json`
- Ajouter le filtre temporel (date du jour ou plage --days)
- Collecter les resultats (titre, URL, snippet)
- Limite : max 5 WebSearch par execution

### 3. Approfondir les articles pertinents (WebFetch)

- Trier les resultats par pertinence (mots-cles Seldon dans le snippet)
- WebFetch sur les 10 articles les plus prometteurs
- Extraire : titre complet, date, auteur, contenu principal
- Limite : max 10 WebFetch par execution

### 4. Analyser et scorer

Pour chaque article :
- **Resume** : 2-3 phrases de synthese
- **Points cles** : liste a puces des informations importantes
- **Score Seldon** : appliquer le scoring depuis seldon-keywords.json
  - Compter les mots-cles haute pertinence (+2), moyenne (+1), boosters (+1)
  - Score final = min(5, somme / 2 arrondi superieur)
- **Categorie** : classer dans IT/Business/Concurrence/Strategique

### 5. Generer la note vault

- Utiliser le template `templates/press-review-note.md`
- Chemin : `C:\Users\r2d2\Documents\Knowledge\References\YYYY-MM-DD_Press-Review.md`
- Si `--category` : suffixer le nom (`YYYY-MM-DD_Press-Review-IT.md`)
- Remplir : tableau recapitulatif + analyse detaillee par categorie
- Section "Pertinence Plan Seldon" : opportunites, menaces, actions suggerees
- Skip si `--dry-run`

### 6. Lier a la Daily Note

- Ouvrir/creer la Daily Note `Knowledge\_Daily\YYYY-MM-DD.md`
- Ajouter le wikilink `[[YYYY-MM-DD_Press-Review]]` dans la section du jour
- Skip si `--dry-run`

### 7. Afficher le recapitulatif console

Afficher un tableau structure :

```
=== Revue de Presse - 2026-03-25 ===

| # | Titre                          | Cat.    | Score | Source         |
|---|--------------------------------|---------|-------|----------------|
| 1 | AI Act : nouvelles obligations | Strat.  | 5/5   | Politico EU    |
| 2 | CVE critique Docker Engine     | IT/Tech | 4/5   | CERT-BE        |
| 3 | Cheque cyber Wallonie prolonge | Biz/Reg | 5/5   | Digital Wallonia|

Articles scannes : 24 | Retenus : 8 | Score moyen : 3.4/5
Note vault : Knowledge/References/2026-03-25_Press-Review.md
```

## Exemples

### Revue complete du jour
```
/press-review
```

### Revue IT uniquement sur 3 jours
```
/press-review --category=IT --days=3
```

### Preview sans ecriture
```
/press-review --dry-run
```

### Revue strategique de la semaine
```
/press-review --category=Strategique --days=7
```
