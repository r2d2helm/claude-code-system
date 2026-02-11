# Analyser les conducteurs d'un projet QET

Liste et analyse tous les conducteurs (fils) d'un projet.

## Actions

1. Charger le .qet
2. Parcourir tous les `<diagram>` > `<conductors>` > `<conductor>`
3. Pour chaque conducteur, extraire les attributs complets :
   - Terminals connectes (terminal1, terminal2) avec UUIDs
   - Type (multi, single)
   - Numerotation (num)
   - Texte affiche (displaytext)
   - `function` : role du conducteur
   - `tension_protocol` : tension et protocole (`230V AC`, `24V DC`, `Modbus`)
   - `conductor_color` : couleur du fil (`BK`, `BU`, `GNYE`)
   - `conductor_section` : section en mm2
   - `formula` : formule d'auto-numerotation
   - `cable` : nom du cable parent
   - `bus` : nom du bus
4. Croiser avec les elements pour identifier les connexions via UUID des terminaux
5. Propagation des noms de cables (pattern qet_parse_alpha) :
   - Cables multi-conducteurs : `C1-L1`, `C1-N`, `C1-PE`
   - Numeration automatique des fils dans un cable
6. Generer le rapport

## Format de sortie

```
# Conducteurs - Projet "Nom"

## Folio 1 : RDC
| Conducteur | De | Vers | Type | Section | Num |
|------------|-----|------|------|---------|-----|
| W1 | Inter1 (T0) | Lampe1 (T1) | multi | 1.5mm2 | W1.001 |
...

## Resume
- Total conducteurs: N
- Par folio: F1=X, F2=Y, ...
```

## Exemple

```
/qet-conductors "projet.qet"
/qet-conductors "projet.qet" --folio 1
```

$ARGUMENTS
