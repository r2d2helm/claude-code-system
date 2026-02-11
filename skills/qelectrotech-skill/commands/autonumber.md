# Configurer l'auto-numerotation QET

Configure les regles d'auto-numerotation pour les elements, conducteurs et folios.

## Types d'auto-numerotation

| Type | Noeud XML | Description |
|------|-----------|-------------|
| Element | `<element_autonums>` | Numerotation automatique des elements places |
| Conducteur | `<conductors_autonums>` | Numerotation automatique des fils |
| Folio | `<folio_autonums>` | Numerotation automatique des folios |

## Variables disponibles

| Variable | Description | Exemple |
|----------|-------------|---------|
| `%{F}` | Numero du folio (2 chiffres) | `01`, `02` |
| `%{f}` | Numero du folio (1 chiffre) | `1`, `2` |
| `%{M}` | Machine / Installation | `M1` |
| `%{LM}` | Localisation machine | `ARM1` |
| `%{l}` | Lettre de ligne (row) | `A`, `B` |
| `%{c}` | Numero de colonne | `1`, `2` |
| `%{id}` | Compteur auto-increment | `001`, `002` |

## Structure XML

### Auto-numerotation des conducteurs

```xml
<conductors_autonums freeze_new_conductors="false" current_autonum="default">
    <conductor_autonum title="default">
        <formula text="W%{F}.%{id}" count="1"/>
    </conductor_autonum>
    <conductor_autonum title="puissance">
        <formula text="L%{id}" count="1"/>
    </conductor_autonum>
</conductors_autonums>
```

### Auto-numerotation des elements

```xml
<element_autonums freeze_new_elements="false" current_autonum="default">
    <element_autonum title="default">
        <formula text="%{F}-%{l}%{c}" count="1"/>
    </element_autonum>
</element_autonums>
```

### Auto-numerotation des folios

```xml
<folio_autonums>
    <folio_autonum title="default">
        <formula text="F%{id}" count="1"/>
    </folio_autonum>
</folio_autonums>
```

## Actions PowerShell

### Ajouter une regle de numerotation

```powershell
[xml]$project = [System.IO.File]::ReadAllText($projectPath)
$autonum = $project.CreateElement('conductor_autonum')
$autonum.SetAttribute('title', 'puissance')
$formula = $project.CreateElement('formula')
$formula.SetAttribute('text', 'L%{id}')
$formula.SetAttribute('count', '1')
$autonum.AppendChild($formula)
$project.project.newdiagrams.conductors_autonums.AppendChild($autonum)
```

### Geler la numerotation

```powershell
$project.project.newdiagrams.conductors_autonums.SetAttribute('freeze_new_conductors', 'true')
$project.project.newdiagrams.element_autonums.SetAttribute('freeze_new_elements', 'true')
```

## Exemple

```
/qet-autonumber conductors "W%{F}.%{id}"
/qet-autonumber elements "%{F}-%{l}%{c}"
/qet-autonumber folios "F%{id}"
/qet-autonumber freeze conductors
```

$ARGUMENTS
