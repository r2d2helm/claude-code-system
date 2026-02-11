# Wizard : Projet Electrique Residentiel

Assistant interactif pour creer un projet electrique complet pour une maison ou un appartement.

## Etape 1 : Informations generales

Demander :
- Nom du projet (ex: "Maison Dupont")
- Type : Maison individuelle / Appartement
- Neuf ou renovation
- Surface totale approximative
- Nombre d'etages (RDC, etages)
- Puissance souscrite (3, 6, 9, 12 kVA)

## Etape 2 : Liste des pieces

Demander pour chaque etage :
- Noms des pieces
- Surface approximative de chaque piece
- Type : sejour, chambre, cuisine, sdb, wc, couloir, garage, cave, exterieur

Proposer un template type :
```
RDC: Entree, Salon, Cuisine, SdB, WC, Couloir
Etage 1: Chambre 1, Chambre 2, Chambre 3, SdB etage, Couloir
Exterieur: Jardin, Terrasse, Garage
```

## Etape 3 : Besoins par piece

Pour chaque piece, determiner selon NF C 15-100 :
- Nombre de prises minimum
- Nombre de points lumineux minimum
- Circuits dedies necessaires
- Besoins speciaux (alarme, VDI, domotique)

Afficher un tableau recapitulatif :
```
| Piece | Prises | Lumieres | Dedies | VDI | Special |
|-------|--------|----------|--------|-----|---------|
| Salon | 7 | 2 | - | 2 RJ45, 1 TV | - |
| Cuisine | 6+4 | 1 | Four,Plaques,LV | 1 RJ45 | Hotte |
...
```

## Etape 4 : Organisation des circuits

Regrouper les points en circuits selon les regles :
- Circuits eclairage (max 8 pts, 1.5mm2, 10A)
- Circuits prises (max 8 prises, 2.5mm2, 20A)
- Circuits dedies (1 appareil, calibre adapte)
- Circuits speciaux (VMC, chauffe-eau, volets)

Afficher la liste des circuits avec protection :
```
| Circuit | Type | Points | Cable | Disj. | Diff. |
|---------|------|--------|-------|-------|-------|
| C1 | Eclairage RDC | 7 pts | 1.5mm2 | 10A | AC |
| C2 | Eclairage Etage | 6 pts | 1.5mm2 | 10A | AC |
| C3 | Prises Salon | 7 prises | 2.5mm2 | 20A | AC |
...
```

## Etape 5 : Conception du tableau electrique

Dimensionner le TGBT :
- Nombre de rangees
- Repartition des differentiels (Type A et AC)
- Placement des disjoncteurs
- Reserve minimum 20%

Afficher le schema du tableau (texte).

## Etape 6 : Organisation des folios

Proposer l'organisation des folios du projet QET :
- 1 folio par zone/etage (plans architecturaux unifilaires)
- 1 folio tableau electrique
- 1 folio recapitulatif
- 1 folio devis optionnel

## Etape 7 : Generation du projet

Creer le fichier .qet avec :
- Tous les folios configures
- Titres descriptifs
- Collection vide (sera peuplee lors de l'edition dans QET)
- Proprietes du projet renseignees

## Etape 8 : Rapport et prochaines etapes

Generer :
- Resume du projet (nombre de points, circuits, couts estimes)
- Liste des materiaux necessaires
- Devis estimatif
- Ouvrir dans QElectroTech pour dessiner les plans

$ARGUMENTS
