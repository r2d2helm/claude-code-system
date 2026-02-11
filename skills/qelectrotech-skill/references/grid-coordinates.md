# Grille et Coordonnees QET

> Reference extraite du skill QElectroTech - grille, dimensions folio, references croisees

## Grille par defaut

| Parametre | Valeur | Description |
|-----------|--------|-------------|
| Grille standard | 10 px | Pas de grille par defaut |
| Grille cabinet | 9 px | 1 HP (hauteur de pole) = 18 mm = 36 px |
| Grille fine | 1 px | Pour positionnement precis |

## Dimensions folio A4

| Attribut | Valeur | Description |
|----------|--------|-------------|
| `cols` | 17 | Nombre de colonnes |
| `rows` | 8 | Nombre de lignes |
| `colsize` | 60 | Largeur colonne en px |
| `rowsize` | 80 | Hauteur ligne en px |
| Largeur totale | 1020 px | 17 x 60 |
| Hauteur totale | 640 px | 8 x 80 |
| Coordonnee max | (1020, 640) | Coin bas-droit |

## Systeme de coordonnees des references croisees

Les references croisees utilisent la notation `%f-%l%c` :
- `%f` = numero de folio
- `%l` = lettre de ligne (A-H pour 8 lignes)
- `%c` = numero de colonne (1-17 pour 17 colonnes)

Exemple : `1-B3` = Folio 1, Ligne B, Colonne 3
