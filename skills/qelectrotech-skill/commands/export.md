# Exporter un projet QET

Exporte les donnees d'un projet QElectroTech vers differents formats.

## Modes d'export

### 1. Export CSV (Nomenclature/BOM)
Genere un fichier CSV avec tous les elements et leurs proprietes.
- Parsing XML direct, pas besoin de GUI
- Colonnes : Type, Label, Description, Folio, Position, Quantite

### 2. Export PDF (via GUI)
Ouvre QElectroTech et guide l'utilisateur pour exporter en PDF.
- Menu : Fichier > Exporter en PDF
- Chaque folio = une page

### 3. Export texte (Resume)
Genere un rapport texte/markdown du projet.

### 4. Export devis
Genere un tableau de devis avec quantites et prix estimatifs.

### 5. Pipeline DXF
QET n'exporte pas nativement en DXF. Pipeline de conversion :
1. Exporter en SVG via QET GUI (Fichier > Exporter en SVG)
2. Convertir SVG → DXF via Inkscape CLI : `inkscape input.svg --export-filename=output.dxf --export-type=dxf`
3. Format cible : DXF R14 (compatibilite maximale)

### 6. Export elements en SVG
Utiliser `QET_ElementScaler` (GitHub) pour convertir des `.elmt` en SVG :
```
python qet_element_scaler.py element.elmt --output element.svg --scale 2.0
```

### 7. Export borniers HTML
Utiliser `qet_terminal_tables` (GitHub) pour generer des tables de borniers :
```
python qet_terminal_tables.py projet.qet --output borniers.html
```

## Actions pour export CSV

1. Charger le fichier .qet
2. Parcourir tous les `<diagram>` et leurs `<element>`
3. Extraire pour chaque element :
   - Type (depuis le chemin `embed://`)
   - Label, comment, manufacturer, reference
   - Position (x, y) et folio
4. Grouper et compter les elements identiques
5. Exporter en CSV

## Exemple

```
/qet-export "projet.qet" csv
/qet-export "projet.qet" pdf
/qet-export "projet.qet" summary
```

$ARGUMENTS
