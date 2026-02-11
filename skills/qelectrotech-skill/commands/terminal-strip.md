# Generer des borniers QET

Cree et gere les borniers (terminal strips) dans un projet QElectroTech.

## Convention de nommage

Format IEC 81346 : `BlockName:TerminalNumber`

| Exemple | Description |
|---------|-------------|
| `X1:1` | Bornier X1, borne 1 |
| `X1:PE` | Bornier X1, borne de terre |
| `X2:1` | Bornier X2, borne 1 |
| `-X1:1` | Composant X1, borne 1 (notation IEC complete) |

## Tags metadata (qet_tb_generator)

| Tag | Description | Exemple |
|-----|-------------|---------|
| `%p` | Plant / Installation | `=A1` |
| `%t` | Type de borne | `SAK 2.5` |
| `%h` | Hierarchie | `+S1.G2` |
| `%n` | Numero de borne | `1`, `2`, `PE` |
| `%b` | Nom du bornier (block) | `X1`, `X2` |
| `%r` | Reference croisee | `K1:A1` |
| `%z` | Zone | `Zone 1` |
| `%s` | Section du fil | `2.5 mm2` |

## Terminal Strip Editor (v0.100)

A partir de QET v0.100, un editeur de borniers integre est disponible :
- Acces : Menu > Projet > Editeur de borniers
- Permet de visualiser et organiser les bornes par bornier
- Genere automatiquement les tables de borniers
- Supporte le drag & drop pour reorganiser les bornes

## Elements de type terminale

Les bornes utilisent `link_type="terminale"` :

```xml
<definition version="0.100.0" type="element" link_type="terminale"
            width="14" height="37" hotspot_x="7" hotspot_y="18">
    <uuid uuid="{GUID}"/>
    <names>
        <name lang="fr">Borne</name>
    </names>
    <elementInformations>
        <elementInformation name="label" show="1">X1:1</elementInformation>
    </elementInformations>
    <description>
        <terminal x="0" y="-17" orientation="n" type="Generic" uuid="{T1-UUID}"/>
        <terminal x="0" y="18" orientation="s" type="Generic" uuid="{T2-UUID}"/>
        <!-- Graphisme de la borne -->
    </description>
</definition>
```

## Outils externes

### qet_tb_generator (PyPI)

Generateur de borniers avec metadata IEC 81346 :

```
pip install qet_tb_generator
qet_tb_generator projet.qet --output borniers.html
```

### qet_terminal_tables (GitHub)

Tables de borniers HTML :

```
python qet_terminal_tables.py projet.qet --output tables.html
```

### QET_Klemmenplan (GitHub)

Plans de borniers (Klemmenplan) pour documentation :

```
python qet_klemmenplan.py projet.qet --output klemmenplan.pdf
```

## Actions PowerShell

### Lister les borniers

```powershell
[xml]$project = [System.IO.File]::ReadAllText($projectPath)
$bornes = $project.SelectNodes('//element') | Where-Object {
    $_.type -match 'terminal'
} | ForEach-Object {
    $label = ($_.elementInformations.elementInformation | Where-Object name -eq 'label').'#text'
    if ($label -match '(.+):(.+)') {
        [PSCustomObject]@{
            Block = $Matches[1]
            Terminal = $Matches[2]
            Folio = $_.ParentNode.ParentNode.title
        }
    }
}
$bornes | Group-Object Block | ForEach-Object {
    "$($_.Name) : $($_.Count) bornes"
}
```

## Exemple

```
/qet-terminal-strip list "projet.qet"
/qet-terminal-strip create X1 10 bornes
/qet-terminal-strip export "projet.qet" --format html
```

$ARGUMENTS
