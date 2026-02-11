# Normes et Standards Electriques

> Reference extraite du skill QElectroTech - NF C 15-100, NF EN 12464-1, IEC 60617

## Eclairage Tertiaire NF EN 12464-1

| Local | Eclairement (lux) | UGR max | Ra min |
|-------|-------------------|---------|--------|
| Bureau individuel | 500 | 19 | 80 |
| Bureau open space | 500 | 19 | 80 |
| Salle de reunion | 500 | 19 | 80 |
| Accueil / Reception | 300 | 22 | 80 |
| Couloir / Circulation | 100 | 28 | 40 |
| Escaliers | 150 | 25 | 40 |
| Sanitaires | 200 | 25 | 80 |
| Archives / Stockage | 100 | 25 | 60 |
| Atelier mecanique | 300 | 22 | 80 |
| Atelier electronique | 1500 | 16 | 90 |
| Salle serveur | 200 | 25 | 60 |
| Parking interieur | 75 | 25 | 40 |

## NF C 15-100 (Residentiel France/Europe)

### Nombre minimum de points par piece

| Piece | Prises | Eclairage | Circuits dedies | Notes |
|-------|--------|-----------|-----------------|-------|
| Sejour (< 28m2) | 5 | 1 centre + 1 applique | - | 1 prise par tranche de 4m2 |
| Sejour (> 28m2) | 7 | 1 centre + 2 appliques | - | +1 prise comm. (RJ45/TV) |
| Chambre | 3 | 1 centre | - | 1 prise a cote lit |
| Cuisine | 6 (dont 4 au plan) | 1 centre | Four, Plaques, Lave-V. | Circuit specialise 32A plaques |
| SdB Vol.1 | 0 | 1 (IP44) | Chauffe-eau | Volumes 0,1,2 strictement reglementes |
| SdB Vol.2 | 1 | 1 | - | IP44 obligatoire |
| SdB Vol.3+ | 1 | 1 | Lave-linge | Prises standard |
| WC | 1 | 1 | - | - |
| Couloir | 1 | 1/4m | - | Detecteur mouvement recommande |
| Garage | 1 | 1 | - | Prise 16A pour borne VE recommande |
| Exterieur | 1 | 1 par acces | - | IP44/IP65 obligatoire |

### Circuits et protections

| Circuit | Section cable | Disjoncteur | Points max | Differentiel |
|---------|--------------|-------------|------------|--------------|
| Eclairage | 1.5 mm2 | 10A ou 16A | 8 points | 30mA type AC |
| Prises standard | 2.5 mm2 | 16A ou 20A | 8 prises | 30mA type AC |
| Prises cuisine | 2.5 mm2 | 20A | 6 prises | 30mA type A |
| Lave-linge | 2.5 mm2 | 20A | Dedie | 30mA type A |
| Lave-vaisselle | 2.5 mm2 | 20A | Dedie | 30mA type A |
| Seche-linge | 2.5 mm2 | 20A | Dedie | 30mA type A |
| Four | 2.5 mm2 | 20A | Dedie | 30mA type A |
| Plaques cuisson | 6 mm2 | 32A | Dedie | 30mA type A |
| Chauffe-eau | 2.5 mm2 | 20A | Dedie | 30mA type AC |
| VMC | 1.5 mm2 | 2A | Dedie | 30mA type AC |
| Volets roulants | 1.5 mm2 | 16A | - | 30mA type AC |
| Chauffage | 1.5 ou 2.5 mm2 | 10A/20A | selon puissance | 30mA type AC |

### Tableau electrique (TGBT)

| Puissance | Rangees min | Inter. diff. | Disjoncteurs typ. |
|-----------|-------------|--------------|-------------------|
| 3 kVA (T1) | 1 | 1x 40A/30mA type A | 6-8 |
| 6 kVA (T2-T3) | 2 | 2x 40A/30mA (1 type A) | 10-16 |
| 9 kVA (T4) | 3 | 2-3x 40A/30mA | 16-24 |
| 12 kVA (T5+) | 4 | 3-4x 63A/30mA | 24-36 |

### Volumes salle de bain

```
Volume 0 : Baignoire/douche         -> RIEN (sauf TBTS 12V)
Volume 1 : Au-dessus bain (2.25m)   -> Eclairage IP44/IPX5, TBTS 12V
Volume 2 : 60cm autour (2.25m)      -> Classe II, IP44, chauffage
Hors volume : Au-dela de 60cm       -> Tout equip. classe I/II autorise
```

## IEC 60617 - Symboles

QElectroTech utilise la norme IEC 60617 pour tous les symboles electriques:
- Section 11: Dispositifs de connexion et elements associes
- Section 12: Commande et protection
- Section 13: Signalisation et mesure
- Les noms d'elements incluent souvent la reference normative (ex: `11-13-04`)
