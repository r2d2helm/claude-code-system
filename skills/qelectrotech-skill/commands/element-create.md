# Creer un element personnalise QET

Genere un fichier `.elmt` avec l'editeur XML.

## Parametres

- **Nom** : Nom de l'element (multilangue fr/en)
- **Type** : simple, master, slave, terminale
- **Dimensions** : Largeur x Hauteur
- **Bornes** : Nombre et positions des terminaux
- **Forme** : Description de la forme geometrique

## Structure d'un .elmt

```xml
<definition version="0.100.0" type="element" link_type="simple"
            orientation="DYYY"
            width="W" height="H" hotspot_x="X" hotspot_y="Y">
    <uuid uuid="{GUID}"/>
    <names>
        <name lang="fr">Nom FR</name>
        <name lang="en">Name EN</name>
    </names>
    <informations>Auteur: r2d2</informations>
    <kindInformations>
        <!-- Pour master/slave : definit le type de liaison -->
        <!-- <kindInformation name="type" show="1">coil</kindInformation> -->
    </kindInformations>
    <elementInformations>
        <elementInformation name="label" show="1"></elementInformation>
        <elementInformation name="formula" show="1"></elementInformation>
        <elementInformation name="description" show="1"></elementInformation>
        <elementInformation name="designation" show="1"></elementInformation>
        <elementInformation name="manufacturer" show="1"></elementInformation>
        <elementInformation name="manufacturer_reference" show="1"></elementInformation>
        <elementInformation name="comment" show="0"></elementInformation>
        <elementInformation name="function" show="0"></elementInformation>
        <elementInformation name="plant" show="0"></elementInformation>
        <elementInformation name="location" show="0"></elementInformation>
    </elementInformations>
    <description>
        <!-- Primitives graphiques -->
        <!-- Terminaux de connexion -->
        <!-- Texte dynamique -->
    </description>
</definition>
```

## Primitives disponibles

| Primitive | Attributs |
|-----------|-----------|
| `<line>` | x1, y1, x2, y2, style, antialias, end1, end2 |
| `<circle>` | x, y, diameter, style, antialias |
| `<arc>` | x, y, width, height, start, angle, style |
| `<rect>` | x, y, width, height, rx, ry, style |
| `<polygon>` | closed, style + points |
| `<text>` | x, y, text, size, rotation, color |
| `<dynamic_text>` | x, y, text_from, info_name, font, uuid |
| `<terminal>` | x, y, orientation (n/s/e/w), name, type, uuid |

## Styles

```
style="line-style:normal;line-weight:normal;filling:none;color:black"
```

- line-style: normal, dashed, dotted, dashdotted
- line-weight: thin, normal, hight, eleve
- filling: none, black, white, red, green, blue, orange, yellow, cyan, magenta, lightgray, darkgray
- color: black, red, blue, etc. ou #RRGGBB

## Orientations des terminaux

- `n` = nord (vers le haut) - connexion depuis le haut
- `s` = sud (vers le bas) - connexion depuis le bas
- `e` = est (vers la droite) - connexion depuis la droite
- `w` = ouest (vers la gauche) - connexion depuis la gauche

## Orientation

L'attribut `orientation="DYYY"` sur `<definition>` controle les rotations autorisees :
- Position 1 : `D` = orientation par defaut
- Positions 2-4 : `Y` (autorise) ou `N` (interdit) pour les rotations 90/180/270

Exemple : `orientation="DYYY"` = toutes rotations autorisees, `orientation="DNNN"` = rotation interdite.

## Types de terminaisons de lignes

Les attributs `end1` et `end2` sur `<line>` definissent les extremites :

| Valeur | Rendu |
|--------|-------|
| `none` | Pas de terminaison |
| `simple` | Trait perpendiculaire |
| `triangle` | Fleche triangulaire |
| `circle` | Cercle |
| `diamond` | Losange |

Attributs `length1` et `length2` controlent la taille (defaut: `1.5`).

## Types d'elements avances

### Master (link_type="master")
Element maitre pour references croisees (bobine de relais, contacteur).
Ajouter `<kindInformations>` avec `type="coil"`, `type="protection"` ou `type="commutator"`.

### Slave (link_type="slave")
Element esclave lie a un master (contacts NO/NC).
Le label affiche automatiquement la reference croisee vers le master.

### Terminale (link_type="terminale")
Element de borne pour borniers. Convention de nommage : `BlockName:TerminalNumber`.
Les terminaux utilisent les UUIDs pour le suivi des connexions.

## Regles

1. Le hotspot est le point de reference pour le placement (generalement centre ou terminal principal)
2. Les coordonnees sont relatives au hotspot (0,0)
3. Width/height definissent la bounding box pour l'editeur
4. Chaque terminal doit avoir un UUID unique
5. Les terminaux doivent etre sur le bord de l'element
6. Le style doit utiliser le format exact avec points-virgules
7. Toujours definir les `elementInformations` avec les champs standards
8. Pour les elements master/slave, configurer `<kindInformations>` avec le type xref

## Exemples courants

### Prise simple avec terre
- Demi-cercle (arc 180 degres)
- Trait vertical pour la terre
- 1 terminal en haut

### Interrupteur
- Ligne oblique + point
- 2 terminaux (haut et bas)

### Lampe
- Cercle avec croix
- 1 terminal en haut

## Exemple

```
/qet-element-create "Prise USB" simple --terminals 1 --shape circle
/qet-element-create "Borne" terminale --terminals 2
```

$ARGUMENTS
