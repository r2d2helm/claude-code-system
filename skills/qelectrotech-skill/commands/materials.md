# Calculer les materiaux necessaires

Estime les quantites de cables, gaines et fournitures pour un projet.

## Actions

1. Analyser le projet (nombre de points par type et par folio/piece)
2. Estimer les longueurs de cables en fonction de :
   - Type de circuit (eclairage 1.5mm2, prises 2.5mm2, etc.)
   - Distance estimee (parametrable, defaut: 15m par point depuis le tableau)
   - Marge de securite (+15%)
3. Estimer les fournitures annexes :
   - Gaines ICTA (1 par circuit)
   - Boites d'encastrement (1 par point)
   - Connecteurs/dominos
   - Attaches, colliers, chevilles
4. Generer la liste des materiaux

## Regles d'estimation des cables

| Circuit | Cable | Longueur estimee/point |
|---------|-------|----------------------|
| Eclairage | H07VU 1.5mm2 | 12-15m |
| Prises | H07VU 2.5mm2 | 12-15m |
| Prise dediee (four, LV...) | H07VU 2.5mm2 | 15-20m |
| Plaques cuisson | H07VU 6mm2 | 15-20m |
| VMC | H07VU 1.5mm2 | 20m |
| Volets roulants | H07VU 1.5mm2 | 15m |
| VDI (RJ45) | Cat6 UTP | 20-25m |
| TV | Coaxial | 15-20m |

## Fournitures annexes (par point)

| Fourniture | Quantite/point |
|------------|---------------|
| Boite d'encastrement | 1 |
| Gaine ICTA 20mm | 15m (eclairage) |
| Gaine ICTA 25mm | 15m (prises) |
| Connecteur Wago 3 poles | 2 |
| Tire-fil | 1 par gaine |

## Exemple

```
/qet-materials "projet.qet"
/qet-materials "projet.qet" --distance 20
```

$ARGUMENTS
