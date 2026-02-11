# Lister les folios d'un projet QET

Affiche la liste des folios avec leurs statistiques.

## Actions

1. Charger le fichier .qet
2. Pour chaque `<diagram>` :
   - Numero d'ordre
   - Titre
   - Nombre d'elements
   - Nombre de conducteurs
   - Nombre de textes libres
   - Nombre de formes
   - Dimensions (cols x rows)
3. Afficher sous forme de tableau

## Format de sortie

```
# Folios du projet "Nom"

| # | Titre | Elements | Cond. | Textes | Formes | Taille |
|---|-------|----------|-------|--------|--------|--------|
| 1 | RDC1  | 58       | 12    | 3      | 45     | 17x8   |
| 2 | RDC2  | 49       | 10    | 2      | 38     | 17x9   |
...

Total: 8 folios, 219 elements, 44 conducteurs
```

## Exemple

```
/qet-folio-list "projet.qet"
```

$ARGUMENTS
