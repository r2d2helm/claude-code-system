# Importer un DXF comme element QET

Convertit un fichier DXF en element .elmt QElectroTech.

## Methodes de conversion

### 1. dxf2elmt (Recommande)

Outil officiel en Rust du projet QElectroTech :

- **Depot** : `qelectrotech/dxf2elmt` (GitHub)
- **Langage** : Rust
- **Formats** : DXF R12/R14 → .elmt

```
dxf2elmt input.dxf -o output.elmt
```

Options :
| Option | Description |
|--------|-------------|
| `-o <file>` | Fichier de sortie .elmt |
| `--scale <factor>` | Facteur d'echelle |
| `--name <name>` | Nom de l'element |
| `--author <name>` | Auteur |

### 2. Pipeline SVG intermediaire

Si dxf2elmt n'est pas disponible :

1. **DXF → SVG** via LibreCAD ou Inkscape :
   ```
   inkscape input.dxf --export-filename=temp.svg
   ```

2. **SVG → .elmt** manuellement :
   - Extraire les chemins SVG
   - Convertir en primitives QET (`<line>`, `<arc>`, `<circle>`, `<polygon>`)
   - Ajouter les terminaux et metadata

### 3. DXF → QET via qet_gen_element

Pour des elements parametriques :

```
python qet_gen_element.py --from-dxf input.dxf --output element.elmt
```

## Correspondance DXF → QET

| Entite DXF | Primitive QET |
|------------|---------------|
| LINE | `<line x1="" y1="" x2="" y2=""/>` |
| CIRCLE | `<circle x="" y="" diameter=""/>` |
| ARC | `<arc x="" y="" width="" height="" start="" angle=""/>` |
| POLYLINE / LWPOLYLINE | `<polygon>` avec points |
| TEXT / MTEXT | `<text>` ou `<dynamic_text>` |
| ELLIPSE | `<arc>` (approximation) |

## Limitations

- Les layers DXF ne sont pas preserves (QET n'a pas de calques)
- Les blocs DXF imbriques sont aplatis
- Les hachures sont converties en remplissage basique
- Les splines sont approximees par des polylignes
- Les dimensions DXF ne sont pas importees

## Actions PowerShell

### Conversion basique

```powershell
$dxfPath = "C:\Users\r2d2\Desktop\symbol.dxf"
$elmtPath = "C:\Users\r2d2\Desktop\symbol.elmt"

# Si dxf2elmt est installe
& dxf2elmt $dxfPath -o $elmtPath --name "Mon Symbole" --author "r2d2"

# Verifier le resultat
[xml]$elmt = [System.IO.File]::ReadAllText($elmtPath)
Write-Host "Element: $($elmt.definition.names.name | Where-Object lang -eq 'fr' | ForEach-Object '#text')"
Write-Host "Primitives: $($elmt.definition.description.ChildNodes.Count)"
```

## Exemple

```
/qet-dxf-import "symbol.dxf"
/qet-dxf-import "symbol.dxf" --name "Vanne 3 voies" --scale 0.5
/qet-dxf-import "symbol.dxf" --method svg
```

$ARGUMENTS
