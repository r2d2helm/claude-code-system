# Reorganiser les folios d'un projet QET

Change l'ordre des folios dans un projet.

## Parametres

- **Fichier** : Chemin du .qet
- **Nouvel ordre** : Liste des numeros dans le nouvel ordre (ex: 3,1,2,4)

## Actions

1. Charger le projet et lister les folios actuels
2. Afficher l'ordre actuel
3. Demander le nouvel ordre si non fourni
4. Valider (tous les folios presents, pas de doublons)
5. Reordonner les noeuds `<diagram>` dans le XML
6. Mettre a jour l'attribut `order` de chaque folio
7. Sauvegarder

## Exemple

```
/qet-folio-reorder projet.qet 3,1,2,4,5
/qet-folio-reorder projet.qet --move 5 --to 2
```

$ARGUMENTS
