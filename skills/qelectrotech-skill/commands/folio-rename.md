# Renommer les folios d'un projet QET

Modifie les titres des folios d'un projet.

## Parametres

- **Fichier** : Chemin du .qet
- **Renommages** : Paires folio=nouveau_titre

## Actions

1. Charger le projet
2. Afficher les titres actuels
3. Appliquer les renommages (modifier l'attribut `title` de chaque `<diagram>`)
4. Sauvegarder

## Exemple

```
/qet-folio-rename projet.qet 1="RDC - Salon" 2="RDC - Cuisine"
/qet-folio-rename projet.qet --interactive
```

$ARGUMENTS
