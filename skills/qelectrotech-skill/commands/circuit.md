# Concevoir un circuit electrique

Guide la conception d'un circuit electrique selon les normes NF C 15-100.

## Parametres

- **Type** : eclairage, prises, dedie, special
- **Piece(s)** : Piece(s) concernee(s)
- **Puissance** : Puissance totale prevue (optionnel)

## Actions

1. **Identifier le type de circuit** et les contraintes :
   - Eclairage : max 8 points, cable 1.5mm2, disj. 10A ou 16A
   - Prises standard : max 8 prises, cable 2.5mm2, disj. 16A ou 20A
   - Prise dediee : 1 appareil, cable 2.5mm2, disj. 20A
   - Plaques cuisson : cable 6mm2, disj. 32A
   - VMC : cable 1.5mm2, disj. 2A

2. **Calculer les besoins** :
   - Nombre de points par piece (selon NF C 15-100)
   - Regroupement en circuits (max points par circuit)
   - Section de cable appropriee
   - Protection (calibre disjoncteur)
   - Type de differentiel (AC ou A)

3. **Proposer le schema** :
   - Elements necessaires
   - Ordre de cablage
   - Protection au tableau
   - References des symboles QET

## Regles NF C 15-100 par type

### Circuit Eclairage
- Cable : 1.5 mm2
- Protection : disjoncteur 10A (recommande) ou 16A
- Max : 8 points lumineux par circuit
- Differentiel : 30mA type AC
- Element QET : `lampe.elmt`, `lampe_1.elmt`, `point_eclairage_*.elmt`

### Circuit Prises
- Cable : 2.5 mm2
- Protection : disjoncteur 16A ou 20A
- Max : 8 prises simples par circuit (5 si multipostes)
- Differentiel : 30mA type AC (ou A pour cuisine)
- Element QET : `pc1.elmt` a `pc6.elmt`

### Circuit Dedie
- Cable : 2.5 mm2
- Protection : disjoncteur 20A
- 1 appareil par circuit : lave-linge, lave-vaisselle, seche-linge, four, congelateur
- Differentiel : 30mA type A obligatoire (lave-linge, plaques)
- Element QET : symbole specifique ou `pc1.elmt` avec label

### Circuit Plaques/Cuisson
- Cable : 6 mm2
- Protection : disjoncteur 32A
- 1 seul point
- Differentiel : 30mA type A obligatoire
- Element QET : symbole dedie ou `pc1.elmt` avec label "32A"

### Circuit VMC
- Cable : 1.5 mm2
- Protection : disjoncteur 2A
- Pas d'interrupteur (alimentation directe)
- Differentiel : 30mA type AC

## Exemple

```
/qet-circuit eclairage "Salon, Couloir, Entree"
/qet-circuit prises "Cuisine" --count 6
/qet-circuit dedie "Lave-linge"
/qet-circuit plaques
```

$ARGUMENTS
