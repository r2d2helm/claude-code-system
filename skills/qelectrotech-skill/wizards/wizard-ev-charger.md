# Wizard Borne de Recharge - Installation IRVE

Assistant interactif pour creer un projet d'infrastructure de recharge pour vehicules electriques (IRVE).

## Etapes

### Etape 1 : Type d'installation IRVE

| Type | Description | Puissance |
|------|-------------|-----------|
| Domestique | Maison individuelle, 1 point de charge | 3.7 - 7.4 kW |
| Copropriete | Parking collectif, multi-points | 3.7 - 22 kW |
| Professionnel | Entreprise, flotte, acces public | 7.4 - 22 kW |

- **Nombre de bornes** : 1 a N
- **Monophase ou triphase** : selon puissance

### Etape 2 : Dimensionnement

| Puissance | Courant | Cable | Type |
|-----------|---------|-------|------|
| 3.7 kW (mono) | 16A | 2.5 mm2 | Mode 2/3 |
| 7.4 kW (mono) | 32A | 6 mm2 | Mode 3 |
| 11 kW (tri) | 16A | 2.5 mm2 | Mode 3 |
| 22 kW (tri) | 32A | 6 mm2 | Mode 3 |

Verifications :
- Puissance souscrite suffisante
- Chute de tension < 5% (longueur cable)
- Section cable selon longueur et mode de pose

### Etape 3 : Protection specifique

Generer le schema de protection :

#### Differentiel
| Configuration | Type differentiel |
|---------------|-------------------|
| Borne avec detection DC intregree | 30mA type A |
| Borne sans detection DC | 30mA type B (ou type A + RDC-DD) |

> **NF C 15-100 section 722** : chaque point de charge doit avoir sa propre protection differentielle dediee.

#### Disjoncteur
- Calibre selon puissance : 20A (3.7kW), 32A (7.4kW), 20A tri (11kW), 32A tri (22kW)
- Courbe C standard

#### Parafoudre
- Obligatoire si installation en zone AQ2
- Recommande dans tous les cas (electronique sensible)
- Type 2 minimum

### Etape 4 : Raccordement au TGBT

Generer le schema de raccordement :

#### Domestique
- Depart dedie depuis le TGBT existant
- 1 differentiel + 1 disjoncteur

#### Copropriete
- Coffret dedie en pied de colonne ou parking
- Comptage individuel ou collectif
- Gestion de charge dynamique (pilotage)
- Interrupteur general avec contact sec pour delestage

#### Professionnel
- Armoire IRVE dediee
- Comptage dedie
- Supervision / OCPP
- Possibilite de delestage / smart charging

### Etape 5 : Generation du projet

1. Creer le fichier .qet avec folios :
   - Page de garde
   - Schema unifilaire IRVE
   - Schema detaille protection par borne
   - Raccordement TGBT / armoire dediee
   - Schema de communication (si pilotage)
   - Nomenclature
2. Sauvegarder et proposer d'ouvrir

## Normes applicables

- NF C 15-100 section 722 : Alimentation des vehicules electriques
- Decret IRVE 2017-26 : Obligations de pre-equipement
- NF EN 61851 : Systeme de charge conductive
- IEC 62196 : Prises et connecteurs (Type 2)

## Fabricants IRVE references

| Fabricant | Gamme |
|-----------|-------|
| Schneider Electric | EVlink Home, Pro, Parking |
| ABB | Terra AC, Terra DC |
| Legrand | Green'up, Premium |
| Wallbox | Pulsar Plus, Copper SB |
| Hager | witty |

## Exemple

```
/qet-wizard ev-charger
/qet-wizard ev-charger --type domestique --power 7.4kW
/qet-wizard ev-charger --type copro --bornes 10 --power 11kW
```

$ARGUMENTS
