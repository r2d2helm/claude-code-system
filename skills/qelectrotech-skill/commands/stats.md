# Statistiques avancees d'un projet QET

Genere des statistiques detaillees et des metriques de qualite sur un projet.

## Metriques calculees

### Densite par folio

| Metrique | Description |
|----------|-------------|
| Elements/folio | Nombre moyen d'elements par folio |
| Conducteurs/folio | Nombre moyen de conducteurs par folio |
| Ratio conducteurs/elements | Indicateur de complexite du cablage |
| Folio le plus charge | Folio avec le plus d'elements |
| Folio le plus vide | Folio avec le moins d'elements |

### Couverture collection

| Metrique | Description |
|----------|-------------|
| Elements uniques utilises | Nombre de definitions differentes placees |
| Total definitions collection | Nombre de definitions dans `<collection>` |
| Taux d'utilisation | % de la collection effectivement utilise |
| Elements orphelins | Definitions presentes mais non utilisees |

### Complexite par folio

| Metrique | Description |
|----------|-------------|
| Score complexite | Elements + Conducteurs + Shapes + Inputs |
| Repartition complexite | Distribution de la complexite entre folios |
| Folios simples (< 10 elem) | Folios de garde, recapitulatif, etc. |
| Folios complexes (> 50 elem) | Schemas detailles, tableaux |

### Repartition par categorie

| Categorie | Description |
|-----------|-------------|
| Appareillage | Prises, interrupteurs, detecteurs |
| Eclairage | Lampes, spots, projecteurs |
| Protection | Disjoncteurs, differentiels, fusibles |
| Commande | Contacteurs, relais, boutons |
| VDI | Prises RJ45, TV/FM |
| Distribution | Coffrets, borniers, peignes |
| Securite | Alarmes, cameras, detecteurs |

## Format de sortie

```
# Statistiques - projet.qet

## Vue d'ensemble
- Folios : 8
- Elements : 156 (42 types uniques)
- Conducteurs : 234
- Taille fichier : 2.4 MB
- Collection : 45 definitions (93% utilisation)

## Densite
| Folio | Titre | Elements | Conducteurs | Complexite |
|-------|-------|----------|-------------|------------|
| 1 | RDC Salon | 28 | 42 | Elevee |
| 2 | RDC Cuisine | 32 | 51 | Elevee |
| 3 | Etage | 22 | 35 | Moyenne |
| 4 | SdB | 14 | 18 | Faible |
| 5 | Exterieur | 8 | 12 | Faible |
| 6 | TGBT | 35 | 45 | Elevee |
| 7 | Recapitulatif | 12 | 0 | Faible |
| 8 | Devis | 5 | 0 | Minimale |
| **Moy.** | | **19.5** | **25.4** | |

## Repartition
| Categorie | Quantite | % |
|-----------|----------|---|
| Appareillage | 45 | 29% |
| Eclairage | 28 | 18% |
| Protection | 24 | 15% |
| Commande | 18 | 12% |
| VDI | 12 | 8% |
| Distribution | 16 | 10% |
| Securite | 8 | 5% |
| Autre | 5 | 3% |

## Qualite
- UUIDs uniques : 100%
- Elements avec label : 89%
- Conducteurs numerotes : 76%
- Cross-refs coherentes : 100%
```

## Exemple

```
/qet-stats "projet.qet"
/qet-stats "projet.qet" --folio 3
/qet-stats "projet.qet" --category
```

$ARGUMENTS
