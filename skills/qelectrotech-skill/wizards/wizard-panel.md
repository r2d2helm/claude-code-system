# Wizard : Tableau Electrique

Assistant pour concevoir un tableau electrique (TGBT) residentiel conforme NF C 15-100.

## Etape 1 : Parametres

Demander :
- Puissance souscrite (3, 6, 9, 12 kVA)
- Monophase ou triphase
- Nombre de circuits existants (si renovation)
- Position du tableau (garage, entree, etc.)

## Etape 2 : Inventaire des circuits

Lister tous les circuits necessaires :
- Eclairage (nombre de circuits)
- Prises (nombre de circuits)
- Circuits dedies (four, plaques, lave-linge, lave-vaisselle, seche-linge, congelateur)
- Circuits speciaux (VMC, chauffe-eau, volets roulants, portail, borne VE)
- Alarme, VDI, domotique

## Etape 3 : Protection differentielle

Determiner :
- Nombre d'interrupteurs differentiels 30mA necessaires
- Types (A, AC, Hpi)
- Calibres (40A ou 63A)
- Repartition des circuits sous chaque differentiel

Regles :
- Au moins 1 ID type A (cuisine, lave-linge, plaques, recharge VE)
- Max 8 circuits par differentiel
- Equilibrer les puissances
- Separer eclairage et prises d'une meme piece (continuite de service)

## Etape 4 : Dimensionnement

Pour chaque circuit :
- Calibre du disjoncteur
- Section du cable
- Type de differentiel parent
- Position dans le tableau (module)

Calcul du nombre de modules total et nombre de rangees.

## Etape 5 : Schema du tableau

Generer le schema textuel du tableau :

```
TABLEAU ELECTRIQUE - XX modules (Y rangees)
============================================

RANGEE 1 : ID 40A/30mA Type A [2 modules]
[ID 40A/A] [C1:20A] [C2:20A] [C3:20A] [C4:32A] [C5:20A] [--] [--]
            Prises   LavVais  LavLing  Plaques  Four    Reserve
            Cuisine

RANGEE 2 : ID 40A/30mA Type AC [2 modules]
[ID 40A/AC] [C6:10A] [C7:10A] [C8:20A] [C9:20A] [C10:20A] [C11:2A] [--]
             Ecl.RDC  Ecl.Et   Prises   Prises   Chauffe   VMC    Reserve
                               Salon    Chambres  eau

Reserve : 30% (conforme > 20%)
```

## Etape 6 : Generation

Proposer :
- Ajouter un folio "Tableau electrique" au projet QET existant
- Ou creer un projet dedie
- Generer la nomenclature des composants du tableau
- Estimer le cout du tableau

$ARGUMENTS
