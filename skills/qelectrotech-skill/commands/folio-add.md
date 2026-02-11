# Ajouter un folio a un projet QET

Ajoute un ou plusieurs folios vides a un projet existant.

## Parametres

- **Fichier** : Chemin du .qet
- **Titre** : Nom du nouveau folio
- **Position** : Apres quel folio existant (defaut: a la fin)
- **Dimensions** : cols/rows (defaut: 17x8 = A4 paysage)

## Actions

1. Charger le projet XML
2. Determiner le prochain numero d'ordre
3. Creer un noeud `<diagram>` avec :
   - `order` = prochain numero
   - `title` = titre fourni
   - `cols`/`rows`/`colsize`/`rowsize` depuis `<newdiagrams>` ou parametres
   - `<defaultconductor>` copie depuis `<newdiagrams>`
   - Sections vides : `<elements>`, `<conductors>`, `<inputs>`, `<shapes>`
4. Inserer le diagram avant `<collection>` dans le XML
5. Renumeroter tous les folios si insertion au milieu
6. Sauvegarder

## Exemple

```
/qet-folio-add projet.qet "Garage" --after 3
/qet-folio-add projet.qet "Cave" "Grenier"
```

$ARGUMENTS
