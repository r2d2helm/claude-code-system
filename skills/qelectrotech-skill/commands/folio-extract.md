# Extraire un folio d'un projet QET

Extrait un folio specifique en fichier .qet independant.

## Parametres

- **Fichier source** : Chemin du .qet multi-folios
- **Folio** : Numero ou titre du folio a extraire
- **Sortie** : Chemin du fichier de sortie

## Actions

1. Charger le projet source
2. Identifier le folio demande (par numero ou titre)
3. Creer un nouveau document XML avec :
   - `<project>` avec le titre du folio
   - `<properties>` avec date du jour
   - `<newdiagrams>` copie depuis le source
   - Le `<diagram>` extrait (order = 1)
   - `<collection>` contenant UNIQUEMENT les elements references par ce folio
4. Sauvegarder en UTF-8 sans BOM

## Points critiques

- Analyser les refs `embed://` du folio extrait pour ne copier que les elements necessaires
- La collection extraite doit etre auto-suffisante

## Exemple

```
/qet-folio-extract projet.qet 3 --output "RDC3.qet"
/qet-folio-extract projet.qet "Cuisine"
```

$ARGUMENTS
