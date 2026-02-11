# Wizard Industriel - Installation Electrique Industrielle

Assistant interactif pour creer un projet electrique industriel complet.

## Etapes

### Etape 1 : Type d'installation

Demander a l'utilisateur :

- **Type** :
  - Atelier de production
  - Ligne de conditionnement
  - Station de pompage
  - HVAC / CVC
  - Process chimique
  - Autre (preciser)
- **Tension** : 400V tri, 230V mono, mixte
- **Regime de neutre** : TT (defaut France), TN-S, TN-C, IT

### Etape 2 : Inventaire des machines

Pour chaque machine, demander :

| Champ | Exemple |
|-------|---------|
| Nom | `Convoyeur C1` |
| Puissance (kW) | `5.5` |
| Type demarrage | Direct, Etoile-Triangle, VFD |
| Tension | 400V tri, 230V mono |
| Courant nominal (A) | `12` (ou calcul auto) |
| Localisation IEC 81346 | `+S1.G2` |

### Etape 3 : Schemas de puissance

Generer pour chaque machine les schemas selon le type de demarrage :

#### Demarrage direct
- Sectionneur Q
- Contacteur principal KM
- Relais thermique F
- Moteur M
- Folios : 1 par moteur

#### Demarrage etoile-triangle
- Sectionneur Q
- Contacteur ligne KM1
- Contacteur etoile KM2
- Contacteur triangle KM3
- Temporisation
- Relais thermique F
- Moteur M

#### Variateur de frequence (VFD)
- Sectionneur Q
- Fusibles HPC
- Variateur U
- Moteur M
- Filtre CEM si necessaire

### Etape 4 : Schemas de commande

Pour chaque machine, generer le circuit de commande :

- Alimentation 24V DC (ou 230V AC selon choix)
- Boutons marche/arret (S1/S2)
- Voyants (H1 marche, H2 defaut)
- Contacts auxiliaires
- Interface automate si applicable (entrees/sorties)

### Etape 5 : TGBT Industriel

Dimensionner le tableau general :
- Disjoncteur general (calibre selon puissance totale)
- Departs moteurs par rangee
- Alimentation commande (transfo 400V/24V)
- Alimentation prises de service
- Eclairage atelier
- Prises de courant industrielles (CEE 16A/32A)
- Compensation reactive si cos phi < 0.85

### Etape 6 : Borniers

Generer les borniers de raccordement :
- Bornier puissance (X1) : phases, neutre, terre
- Bornier commande (X2) : 24V, signaux
- Bornier automate (X3) : E/S TOR et analogiques
- Convention nommage IEC 81346 : `BlockName:TerminalNumber`

### Etape 7 : Generation du projet

1. Creer le fichier .qet avec les folios :
   - Page de garde
   - Schema general (unifilaire)
   - 1 folio puissance par machine
   - 1 folio commande par machine
   - Folio TGBT
   - Folio borniers
   - Nomenclature
2. Configurer l'auto-numerotation
3. Configurer les references croisees
4. Sauvegarder et proposer d'ouvrir

## Normes industrielles

- NF C 15-100 : Installation BT
- IEC 60204-1 : Securite machines electriques
- IEC 81346 : Designation de reference
- IEC 60617 : Symboles graphiques

## Exemple

```
/qet-wizard industrial
/qet-wizard industrial --machines "Pompe P1:5.5kW:VFD,Convoyeur C1:2.2kW:Direct"
```

$ARGUMENTS
