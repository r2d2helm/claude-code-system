# Generer un devis a partir d'un projet QET

Cree un devis estimatif base sur la nomenclature du projet.

## Actions

1. Extraire la nomenclature (comme /qet-bom)
2. Appliquer les prix unitaires (base de prix configurable)
3. Ajouter les fournitures annexes (cables, gaines, boites, etc.)
4. Calculer la main d'oeuvre estimee
5. Generer le devis formate

## Base de prix par defaut (estimations moyennes Europe 2025-2026)

### Appareillage

| Element | Prix unitaire HT |
|---------|-----------------|
| Prise 2P+T simple | 5-15 EUR |
| Double prise 2P+T | 10-25 EUR |
| Interrupteur simple | 5-12 EUR |
| Va-et-vient | 8-15 EUR |
| Bouton poussoir | 6-12 EUR |
| Point lumineux (douille) | 3-8 EUR |
| Detecteur mouvement | 15-40 EUR |
| Prise RJ45 Cat6 | 10-25 EUR |
| Prise TV/FM | 8-20 EUR |

### Protection

| Element | Prix unitaire HT |
|---------|-----------------|
| Disjoncteur 10A/16A | 8-15 EUR |
| Disjoncteur 20A | 10-18 EUR |
| Disjoncteur 32A | 12-22 EUR |
| Interrupteur diff. 40A/30mA | 30-60 EUR |
| Interrupteur diff. 63A/30mA | 40-80 EUR |
| Tableau 1 rangee (13 modules) | 20-40 EUR |
| Tableau 2 rangees (26 modules) | 35-70 EUR |
| Tableau 3 rangees (39 modules) | 50-100 EUR |
| Parafoudre | 40-80 EUR |

### Cables (au metre)

| Cable | Prix/m HT |
|-------|----------|
| H07VU 1.5mm2 | 0.30-0.50 EUR |
| H07VU 2.5mm2 | 0.50-0.80 EUR |
| H07VU 6mm2 | 1.20-1.80 EUR |
| XGB 3G1.5mm2 | 0.80-1.20 EUR |
| XGB 3G2.5mm2 | 1.20-1.80 EUR |
| XGB 5G1.5mm2 | 1.20-1.60 EUR |
| Cable RJ45 Cat6 | 0.50-1.00 EUR |
| Cable coaxial TV | 0.40-0.80 EUR |

### Main d'oeuvre (estimation)

| Poste | Cout estime |
|-------|-------------|
| Point lumineux complet | 25-45 EUR/point |
| Prise complete | 20-35 EUR/point |
| Interrupteur complet | 20-35 EUR/point |
| Tableau electrique (montage+cablage) | 200-500 EUR |
| Mise en service + verification | 100-200 EUR |

## Format de sortie

```
# DEVIS ESTIMATIF
Projet: "Nom"
Date: DD/MM/YYYY

## 1. Appareillage
| Designation | Qte | PU HT | Total HT |
|-------------|-----|-------|----------|
| Prise 2P+T | 24 | 10 EUR | 240 EUR |
...
Sous-total: XXX EUR

## 2. Protection
...

## 3. Cables et fournitures
...

## 4. Main d'oeuvre
...

## TOTAL
| | Montant |
|---|---------|
| Fournitures HT | XXX EUR |
| Main d'oeuvre HT | XXX EUR |
| **Total HT** | **XXX EUR** |
| TVA 20% | XXX EUR |
| **Total TTC** | **XXX EUR** |
```

## Exemple

```
/qet-devis "projet.qet"
/qet-devis "projet.qet" --prices custom_prices.json
```

$ARGUMENTS
