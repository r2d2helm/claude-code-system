# Importer un element dans un projet QET

Ajoute la definition d'un element de la bibliotheque systeme dans la collection embarquee d'un projet.

## Parametres

- **Fichier projet** : Chemin du .qet
- **Element** : Chemin de l'element dans la bibliotheque ou fichier .elmt

## Actions

1. Charger le projet .qet
2. Charger la definition de l'element (.elmt)
3. Determiner le chemin de categorie correct dans la collection
4. Verifier si l'element existe deja (deduplication)
5. Creer les categories intermediaires si necessaires (avec noms multilangues)
6. Inserer la definition `<element name="xxx.elmt"><definition>...</definition></element>`
7. Sauvegarder

## Utilite

Quand on cree un projet par script (sans passer par QET GUI), les elements places avec `type="embed://import/..."` doivent avoir leur definition dans la `<collection>`. Cette commande permet d'ajouter les definitions necessaires.

## Exemple

```
/qet-element-import projet.qet "10_electric/11_singlepole/500_home_installation/30_architectural/pc1.elmt"
/qet-element-import projet.qet "C:\custom\mon_element.elmt" --category "custom"
```

$ARGUMENTS
