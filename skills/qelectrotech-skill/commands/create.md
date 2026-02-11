# Creer un nouveau projet QElectroTech

Cree un fichier `.qet` multi-folios structure et pret a l'emploi.

## Parametres

- **Nom du projet** : Titre du projet (ex: "Maison Dupont")
- **Nombre de folios** : Combien de pages/folios
- **Chemin de sortie** : Ou sauvegarder le fichier .qet
- **Titres des folios** : Liste des noms pour chaque folio
- **--titleblock** : Nom du cartouche a utiliser (defaut: `default`)
- **--author** : Auteur du projet
- **--plant** : Installation / Usine (IEC 81346 `=`)
- **--autonumber** : Activer l'auto-numerotation (element, conductor, folio)

## Actions

1. **Demander les parametres** si non fournis :
   - Nom du projet
   - Type : residential, tertiaire, industriel
   - Nombre de folios et leurs titres
   - Chemin de sortie (defaut: Bureau)

2. **Generer le XML** du projet avec :
   - En-tete `<project>` avec titre et version 0.90
   - `<properties>` avec date, chemin, nom fichier, et variables projet :
     - `plant`, `machine`, `locmach`, `indexrev` dans `<properties>`
   - `<newdiagrams>` avec config par defaut (grille 17x8, cartouche default)
   - `<inset>` avec variables cartouche :
     - `plant="{{PLANT}}"`, `author="{{AUTHOR}}"`, `title="{{TITLE}}"`
     - `folio="%id/%total"`, `indexrev="{{INDEXREV}}"`
   - Un `<diagram>` par folio avec :
     - `order` sequentiel (1, 2, 3...)
     - `title` = nom du folio
     - `<defaultconductor>` type multi
     - Sections vides : `<elements>`, `<conductors>`, `<inputs>`, `<shapes>`
   - Config auto-numerotation si `--autonumber` :
     - `<conductors_autonums>` avec pattern `%{F}-%{id}`
     - `<element_autonums>` avec pattern par type
     - `<folio_autonums>` avec pattern sequentiel
   - `<collection>` avec categorie import vide (sera peuplee par QET)

3. **Sauvegarder** en UTF-8 sans BOM

4. **Proposer d'ouvrir** dans QElectroTech

## Template par defaut pour projet residentiel

Folios types :
1. RDC - Piece 1, Piece 2, Piece 3
2. RDC - Piece 4, Piece 5, Piece 6
3. Etage 1
4. Etage 2
5. Exterieur / Jardin
6. Tableau electrique
7. Recapitulatif circuits
8. Devis materiaux

## Exemple d'utilisation

```
/qet-create "Maison Martin" 6 folios
/qet-create residential --rooms "Salon,Cuisine,SdB,Chambre1,Chambre2"
```

$ARGUMENTS
