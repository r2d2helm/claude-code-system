# Transformer un element QET

Redimensionne, pivote, inverse ou exporte un element .elmt.

## Actions

| Action | Description |
|--------|-------------|
| `scale <file> <factor>` | Redimensionner un element |
| `flip <file> <axis>` | Inverser horizontalement (h) ou verticalement (v) |
| `rotate <file> <angle>` | Pivoter de 90, 180 ou 270 degres |
| `export-svg <file>` | Exporter un element en SVG |

## Scale (Redimensionnement)

### Via QET_ElementScaler (GitHub)

Outil Python du projet QElectroTech :

```
python qet_element_scaler.py element.elmt --scale 2.0 --output element_2x.elmt
```

### Via PowerShell

```powershell
function Scale-QetElement {
    param(
        [string]$Path,
        [double]$Factor,
        [string]$OutputPath
    )
    [xml]$elmt = [System.IO.File]::ReadAllText($Path)
    $def = $elmt.definition

    # Redimensionner la bounding box
    $def.width = [string]([int]$def.width * $Factor)
    $def.height = [string]([int]$def.height * $Factor)
    $def.hotspot_x = [string]([int]$def.hotspot_x * $Factor)
    $def.hotspot_y = [string]([int]$def.hotspot_y * $Factor)

    # Redimensionner les primitives
    foreach ($node in $def.description.ChildNodes) {
        foreach ($attr in @('x','y','x1','y1','x2','y2','diameter','width','height')) {
            if ($node.HasAttribute($attr)) {
                $val = [double]$node.GetAttribute($attr)
                $node.SetAttribute($attr, [string]($val * $Factor))
            }
        }
    }

    # Sauvegarder
    $settings = New-Object System.Xml.XmlWriterSettings
    $settings.Indent = $true
    $settings.Encoding = [System.Text.UTF8Encoding]::new($false)
    $writer = [System.Xml.XmlWriter]::Create($OutputPath, $settings)
    $elmt.Save($writer)
    $writer.Close()
}
```

## Flip (Inversion)

### Horizontal (miroir axe Y)

```powershell
# Inverser toutes les coordonnees X
foreach ($node in $def.description.ChildNodes) {
    foreach ($attr in @('x','x1','x2')) {
        if ($node.HasAttribute($attr)) {
            $val = [double]$node.GetAttribute($attr)
            $node.SetAttribute($attr, [string](-$val))
        }
    }
}
```

### Vertical (miroir axe X)

```powershell
# Inverser toutes les coordonnees Y
foreach ($node in $def.description.ChildNodes) {
    foreach ($attr in @('y','y1','y2')) {
        if ($node.HasAttribute($attr)) {
            $val = [double]$node.GetAttribute($attr)
            $node.SetAttribute($attr, [string](-$val))
        }
    }
}
```

## Rotate (Rotation)

Rotation de 90 degres : `(x, y) → (-y, x)`

```powershell
foreach ($node in $def.description.ChildNodes) {
    if ($node.HasAttribute('x') -and $node.HasAttribute('y')) {
        $x = [double]$node.GetAttribute('x')
        $y = [double]$node.GetAttribute('y')
        $node.SetAttribute('x', [string](-$y))
        $node.SetAttribute('y', [string]($x))
    }
    # Mettre a jour l'orientation des terminaux
    if ($node.LocalName -eq 'terminal') {
        $orient = $node.GetAttribute('orientation')
        $map = @{ 'n'='w'; 'w'='s'; 's'='e'; 'e'='n' }
        $node.SetAttribute('orientation', $map[$orient])
    }
}
```

## Export SVG

### Via QET_ElementScaler

```
python qet_element_scaler.py element.elmt --export-svg --output element.svg
```

### Primitives QET → SVG

| QET | SVG |
|-----|-----|
| `<line>` | `<line>` |
| `<circle>` | `<circle>` |
| `<arc>` | `<path>` avec arc |
| `<rect>` | `<rect>` |
| `<polygon>` | `<polygon>` |
| `<text>` | `<text>` |

## Exemple

```
/qet-element-transform scale "element.elmt" 2.0
/qet-element-transform flip "element.elmt" h
/qet-element-transform rotate "element.elmt" 90
/qet-element-transform export-svg "element.elmt"
```

$ARGUMENTS
