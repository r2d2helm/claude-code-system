# Fusionner des fichiers QET

Combine plusieurs fichiers `.qet` en un seul projet multi-folios avec deduplication des elements.

## Parametres

- **Fichiers source** : Liste des .qet a fusionner (chemin ou glob)
- **Ordre** : Ordre des folios dans le projet final
- **Titres** : Renommer optionnellement les folios
- **Sortie** : Chemin du fichier de sortie

## Actions

1. **Lister les fichiers** source et afficher un apercu (nom, taille, nb elements)
2. **Demander confirmation** de l'ordre et des exclusions eventuelles
3. **Pour chaque fichier source** :
   - Charger le XML avec `[xml]`
   - Extraire le noeud `<diagram>`
   - Mettre a jour `order` (sequentiel) et `title` (si renommage)
   - Importer dans le document de sortie
4. **Fusionner les collections** :
   - Parcourir recursivement les `<category>` de chaque source
   - Deduplication par chemin : si meme `category/name` + `element/name`, garder une seule copie
   - Conserver toute la hierarchie : `import > 10_electric > 11_singlepole > ...`
5. **Construire le projet final** :
   - `<project>` avec nouveau titre
   - `<properties>` avec date du jour
   - `<newdiagrams>` depuis le premier fichier source
   - Tous les `<diagram>` ordonnes
   - `<collection>` fusionnee
6. **Sauvegarder** en UTF-8 sans BOM
7. **Verifier** que toutes les refs `embed://` sont couvertes par la collection
8. **Proposer d'ouvrir** le resultat

## Points critiques

- Les references `embed://import/path/element.elmt` dans les elements de diagramme DOIVENT correspondre exactement aux chemins dans la collection fusionnee
- La fusion est recursive : sous-categories imbriquees sont gerees
- Elements identiques (meme nom dans meme chemin) = un seul exemplaire garde

## Exemple

```
/qet-merge "C:\NELU ELEC\*.qet" --output "C:\Desktop\COMPLET.qet"
/qet-merge file1.qet file2.qet file3.qet --titles "RDC,Etage,Recap"
```

$ARGUMENTS
