# Gerer les references croisees QET

Gere les liaisons Master/Slave et les references croisees entre elements.

## Actions

| Action | Description |
|--------|-------------|
| `list <project>` | Lister toutes les references croisees du projet |
| `create <master> <slave>` | Creer une liaison master/slave |
| `check <project>` | Verifier la coherence des references croisees |
| `config <project>` | Configurer les formules de labels xref |

## Types de references croisees

| Type | Description | Exemple |
|------|-------------|---------|
| `coil` | Bobine / Contacts | Relais K1 (bobine) → K1 (contact NO/NC) |
| `protection` | Protection / Commande | Disjoncteur Q1 → Contact auxiliaire Q1 |
| `commutator` | Commutateur / Contacts | Interrupteur S1 → Contact S1 |

## Configuration XML

Les references croisees sont configurees dans `<newdiagrams>` > `<xrefs>` :

```xml
<xrefs>
    <xref type="coil" displayhas="cross" snapto="label"
          master_label="%f-%l%c"
          slave_label="(%f-%l%c)"
          showpowerctc="true" offset="0"
          delayprefix="" switchprefix="" powerprefix=""/>
    <xref type="protection" displayhas="cross" snapto="label"
          master_label="%f-%l%c"
          slave_label="(%f-%l%c)"/>
    <xref type="commutator" displayhas="cross" snapto="label"
          master_label="%f-%l%c"
          slave_label="(%f-%l%c)"/>
</xrefs>
```

## Attributs xref

| Attribut | Description | Valeurs |
|----------|-------------|---------|
| `displayhas` | Mode d'affichage | `cross` (tableau croise), `contacts` (liste contacts) |
| `snapto` | Base du label | `label` (etiquette), `comment` (commentaire) |
| `master_label` | Formule label maitre | `%f-%l%c` (folio-ligne-colonne) |
| `slave_label` | Formule label esclave | `(%f-%l%c)` (entre parentheses) |
| `showpowerctc` | Montrer contacts puissance | `true`/`false` |
| `offset` | Decalage d'affichage | `0` |
| `delayprefix` | Prefixe contacts temporises | Texte libre |
| `switchprefix` | Prefixe contacts commutation | Texte libre |
| `powerprefix` | Prefixe contacts puissance | Texte libre |

## Elements Master/Slave

### Element Master (link_type="master")

L'element master doit avoir `<kindInformations>` :

```xml
<kindInformations>
    <kindInformation name="type" show="1">coil</kindInformation>
</kindInformations>
```

### Element Slave (link_type="slave")

L'element slave est lie au master dans le diagramme. Le label du slave affiche automatiquement la reference croisee vers le master.

## Actions PowerShell

### Lister les references croisees

```powershell
[xml]$project = [System.IO.File]::ReadAllText($projectPath)
$masters = $project.SelectNodes('//element') | Where-Object {
    $def = $_.type
    # Verifier link_type dans la collection
    $true
}
```

### Verifier la coherence

```powershell
# Verifier que chaque slave a un master correspondant
$elements = $project.SelectNodes('//element')
$labels = $elements | ForEach-Object {
    ($_.elementInformations.elementInformation | Where-Object name -eq 'label').'#text'
}
# Detecter les labels orphelins
```

## Exemple

```
/qet-crossref list "projet.qet"
/qet-crossref check "projet.qet"
/qet-crossref config "projet.qet" --master-label "%f-%l%c" --slave-label "(%f-%l%c)"
```

$ARGUMENTS
