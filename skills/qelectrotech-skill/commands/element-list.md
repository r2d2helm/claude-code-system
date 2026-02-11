# Lister les elements d'un projet QET

Affiche tous les elements utilises dans un projet avec statistiques.

## Actions

1. Charger le fichier .qet
2. Parcourir tous les `<diagram>` > `<elements>` > `<element>`
3. Pour chaque element :
   - Extraire le type depuis `embed://import/path/nom.elmt`
   - Extraire le label depuis `<elementInformations>`
   - Noter la position (x, y) et le folio
4. Grouper par type et compter
5. Afficher le tableau

## Format de sortie

```
# Elements du projet "Nom"

## Par type (quantites)
| Element | Nom | Quantite | Folios |
|---------|-----|----------|--------|
| pc1.elmt | Prise 2P+T | 24 | 1,2,3,4 |
| lampe.elmt | Lampe | 18 | 1,2,3,5 |
| interrupteur_unipolaire.elmt | Inter simple | 12 | 1,2,3 |
...

## Par folio
| Folio | Elements | Prises | Lampes | Inters | Autres |
|-------|----------|--------|--------|--------|--------|
| 1 - RDC | 58 | 15 | 8 | 6 | 29 |
...

Total: 164 elements places, 14 types uniques
```

## Exemple

```
/qet-element-list "projet.qet"
/qet-element-list "projet.qet" --folio 1
```

$ARGUMENTS
