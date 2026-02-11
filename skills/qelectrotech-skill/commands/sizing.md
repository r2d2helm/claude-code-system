# Dimensionner cables et protections

Calcule les sections de cables et calibres de protection pour un circuit.

## Parametres

- **Type de circuit** : eclairage, prises, dedie, moteur
- **Puissance** : en Watts ou Amperes
- **Longueur** : distance tableau -> dernier point (en metres)
- **Methode de pose** : encastre, apparent, goulotte

## Actions

1. Determiner le courant d'emploi (Ib)
2. Choisir le calibre de protection (In >= Ib)
3. Determiner le courant admissible (Iz) selon methode de pose
4. Verifier section cable (Iz >= In)
5. Verifier la chute de tension (< 3% eclairage, < 5% autres)
6. Proposer la solution

## Tables de dimensionnement

### Section cables cuivre (methode de pose B1 - encastre sous isolant)

| Section | Iz max (A) | Usage type |
|---------|-----------|------------|
| 1.5 mm2 | 16A | Eclairage, VMC, volets |
| 2.5 mm2 | 21A | Prises, circuits dedies |
| 4 mm2 | 27A | Circuits puissants |
| 6 mm2 | 34A | Plaques cuisson, cuisson |
| 10 mm2 | 46A | Recharge VE, gros consommateurs |
| 16 mm2 | 61A | Alimentation tableau secondaire |

### Calibres disjoncteurs

| Calibre | Courant nominal | Usage |
|---------|-----------------|-------|
| 2A | 2A | VMC |
| 10A | 10A | Eclairage (recommande) |
| 16A | 16A | Eclairage, prises (avec 1.5mm2 max) |
| 20A | 20A | Prises standard, circuits dedies |
| 25A | 25A | Circuits puissants |
| 32A | 32A | Plaques cuisson |
| 40A | 40A | Recharge VE |

### Chute de tension

Formule simplifiee (monophase):
```
DeltaU = 2 x L x Ib x rho / S
```
- L = longueur en metres
- Ib = courant en amperes
- rho = resistivite cuivre = 0.0225 ohm.mm2/m
- S = section en mm2

Limites :
- Eclairage : 3% max (6.9V sur 230V)
- Autres usages : 5% max (11.5V sur 230V)

## Exemple

```
/qet-sizing eclairage 800W 20m
/qet-sizing prises 3600W 25m
/qet-sizing dedie "four" 3000W 15m
/qet-sizing "plaques cuisson" 7200W 12m
```

$ARGUMENTS
