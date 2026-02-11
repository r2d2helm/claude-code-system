# Concevoir un tableau electrique

Guide la conception d'un tableau electrique (TGBT) residentiel.

## Parametres

- **Puissance** : Puissance souscrite (3, 6, 9, 12 kVA)
- **Pieces** : Liste des pieces de la maison
- **Type** : monophase (defaut) ou triphase

## Actions

1. **Recenser les circuits** necessaires a partir des pieces :
   - Circuits eclairage (1 par zone, max 8 points)
   - Circuits prises (1 par zone, max 8 prises)
   - Circuits dedies (lave-linge, four, plaques, etc.)
   - Circuits speciaux (VMC, chauffe-eau, volets)

2. **Dimensionner les protections** :
   - Disjoncteur general (AGCP) selon puissance souscrite
   - Interrupteurs differentiels 30mA :
     - Au moins 1 type A (obligatoire pour cuisine, lave-linge, plaques)
     - Repartir equilibrement les circuits sous les differentiels
   - Disjoncteurs divisionnaires par circuit
   - **Parafoudre** :
     - Obligatoire en zone AQ2 (risque foudre eleve)
     - Recommande partout si equipements sensibles (informatique, domotique)
     - Type 2 minimum, Type 1+2 si paratonnerre
     - Elements QET : `90_overvoltage_protections/`

3. **Organiser le tableau** :
   - Nombre de rangees necessaires
   - Repartition par rangee (1 differentiel + ses disjoncteurs par rangee)
   - **Peignes de raccordement** :
     - Peigne horizontal : relie les disjoncteurs d'une rangee (phase + neutre)
     - Peigne vertical : relie les differentiels entre rangees
     - Elements QET : `114_connections/`
   - **Bornier de terre** :
     - Barre de terre collective raccordee au piquet de terre
     - Liaison equipotentielle principale (LEP)
     - Elements QET : `130_terminals_terminal_strips/`
   - Reserve minimum 20% (norme)

### References .elmt pour composants tableau

| Composant | Chemin elements |
|-----------|----------------|
| Disjoncteurs | `10_allpole/200_fuses_protective_gears/11_circuit_breakers/` |
| Differentiels | `10_allpole/200_fuses_protective_gears/50_residual_current/` |
| Parafoudres | `10_allpole/200_fuses_protective_gears/90_overvoltage_protections/` |
| Interrupteurs-sectionneurs | `10_allpole/200_fuses_protective_gears/20_disconnecting_switches/` |
| Bornes / Borniers | `10_allpole/130_terminals_terminal_strips/` |
| Contacteurs | `10_allpole/310_relays_contactors/` |

4. **Generer le schema** du tableau (texte structure)

## Regles de dimensionnement

### Disjoncteur de branchement (AGCP)
| Puissance | Calibre | Type |
|-----------|---------|------|
| 3 kVA | 15/45A | 1P+N |
| 6 kVA | 15/45A | 1P+N |
| 9 kVA | 10/30A ou 15/45A | 1P+N |
| 12 kVA | 15/45A ou 30/60A | 1P+N |

### Interrupteurs differentiels
| Type | Usage | Calibre min |
|------|-------|-------------|
| AC | Eclairage, prises standard, volets | 40A |
| A | Cuisine, lave-linge, plaques, informatique | 40A |
| Hpi/Hi | Congelateur, alarme (haute immunite) | 40A |

### Repartition equilibree
- Max 8 circuits par differentiel
- Equilibrer les puissances entre les differentiels
- Ne pas mettre eclairage et prises du meme local sous le meme differentiel (continuite de service)

## Format de sortie

```
# Tableau Electrique - Projet "Nom"

## Rangee 1 : Interrupteur diff. 40A/30mA Type A
| Pos | Calibre | Circuit | Cable | Pieces |
|-----|---------|---------|-------|--------|
| 1-2 | ID 40A/30mA Type A | - | - | - |
| 3 | 20A | Prises cuisine | 2.5mm2 | Cuisine |
| 4 | 20A | Lave-vaisselle | 2.5mm2 | Cuisine |
| 5 | 20A | Lave-linge | 2.5mm2 | SdB |
| 6 | 32A | Plaques cuisson | 6mm2 | Cuisine |
| 7 | 20A | Four | 2.5mm2 | Cuisine |
| 8-13 | Reserve | - | - | - |

## Rangee 2 : Interrupteur diff. 40A/30mA Type AC
| Pos | Calibre | Circuit | Cable | Pieces |
|-----|---------|---------|-------|--------|
| 1-2 | ID 40A/30mA Type AC | - | - | - |
| 3 | 16A | Eclairage RDC | 1.5mm2 | Salon,Hall,Cuisine |
| 4 | 16A | Eclairage Etage | 1.5mm2 | Ch1,Ch2,SdB |
| 5 | 20A | Prises Salon | 2.5mm2 | Salon |
| 6 | 20A | Prises Chambres | 2.5mm2 | Ch1,Ch2 |
| 7 | 20A | Chauffe-eau | 2.5mm2 | SdB |
| 8 | 2A | VMC | 1.5mm2 | Combles |
...

## Resume
- Rangees: 2 (26 modules)
- Differentiels: 1 Type A + 1 Type AC
- Disjoncteurs: 12
- Reserve: 30% (conforme > 20%)
```

## Exemple

```
/qet-panel 9kVA "Salon,Cuisine,SdB,Chambre1,Chambre2,Garage"
/qet-panel 6kVA --rooms "Salon,Cuisine,SdB,Ch1" --type mono
```

$ARGUMENTS
