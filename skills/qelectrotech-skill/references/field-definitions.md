# Champs d'Information QET

> Reference extraite du skill QElectroTech - definitions des champs elements et conducteurs

## Champs Element (elementInformations)

| Champ | Description | Exemple |
|-------|-------------|---------|
| `label` | Designation de repere | `K1`, `Q1`, `F1` |
| `formula` | Formule auto-numerotation | `%{F}-%{l}%{c}` |
| `comment` | Commentaire libre | `Contacteur principal` |
| `function` | Fonction de l'element | `Commande moteur` |
| `description` | Description detaillee | `Contacteur 3P 25A` |
| `designation` | Reference catalogue | `LC1D25BD` |
| `manufacturer` | Fabricant | `Schneider Electric` |
| `manufacturer_reference` | Reference fabricant | `LC1D25BD` |
| `supplier` | Fournisseur | `Rexel` |
| `quantity` | Quantite | `1` |
| `unity` | Unite | `pce` |
| `plant` | Installation/Usine | `=A1` |
| `location` | Localisation | `+S1.G2` |
| `AUX1` a `AUX4` | Champs auxiliaires | Libre |

## Champs Conducteur (conductor)

| Champ | Attribut XML | Description |
|-------|-------------|-------------|
| Numero | `num` | Identifiant du fil (`W1`, `L1`, `N`) |
| Fonction | `function` | Role du conducteur |
| Tension/Protocole | `tension_protocol` | `230V AC`, `24V DC`, `Modbus` |
| Couleur | `conductor_color` | Couleur du fil (`BK`, `BU`, `GNYE`) |
| Section | `conductor_section` | Section en mm2 (`1.5`, `2.5`, `6`) |
| Formule | `formula` | Auto-numerotation conducteur |
| Cable | `cable` | Nom du cable parent (`C1`, `C2`) |
| Bus | `bus` | Nom du bus (`CAN`, `Modbus`) |

## Orientation des Elements

### Attribut orientation

L'attribut `orientation` d'un element dans un diagramme controle les rotations autorisees :

```
orientation="DYYY" (4 caracteres)
```

| Position | Signification | Valeurs |
|----------|--------------|---------|
| 1er (D) | Orientation par defaut | `D` (defaut) |
| 2e | Rotation 90 CW | `Y` (autorise) / `N` (interdit) |
| 3e | Rotation 180 | `Y` / `N` |
| 4e | Rotation 270 CW | `Y` / `N` |

## Types de terminaisons de lignes

| Valeur | Description | Usage |
|--------|-------------|-------|
| `none` | Pas de terminaison | Fil standard |
| `simple` | Trait perpendiculaire | Terre |
| `triangle` | Fleche triangulaire | Sens du courant |
| `circle` | Cercle | Point de connexion |
| `diamond` | Losange | Marqueur special |

Attributs dans `<line>` : `end1="none"` et `end2="triangle"`, avec `length1` et `length2` pour la taille.
