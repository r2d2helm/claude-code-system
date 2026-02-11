# Operations PowerShell sur les fichiers QET

> Reference extraite du skill QElectroTech - snippets PowerShell pour manipuler les fichiers .qet et .elmt

## Charger un projet

```powershell
[xml]$project = [System.IO.File]::ReadAllText('projet.qet')
```

## Lister les folios

```powershell
$project.project.SelectNodes('diagram') | ForEach-Object {
    [PSCustomObject]@{
        Order = $_.order
        Title = $_.title
        Elements = $_.elements.element.Count
    }
}
```

## Compter les elements par type

```powershell
$project.project.SelectNodes('//element[@type]') | ForEach-Object {
    $_.type -replace 'embed://import/',''
} | Group-Object | Sort-Object Count -Descending
```

## Extraire la nomenclature

```powershell
$project.project.SelectNodes('//element') | ForEach-Object {
    $info = $_.elementInformations
    [PSCustomObject]@{
        Type    = ($_.type -split '/')[-1] -replace '\.elmt$',''
        Label   = ($info.elementInformation | Where-Object name -eq 'label').'#text'
        Comment = ($info.elementInformation | Where-Object name -eq 'comment').'#text'
        Folio   = $_.ParentNode.ParentNode.title
        X       = $_.x
        Y       = $_.y
    }
}
```

## Creer un element simple

```powershell
$elmt = @'
<definition version="0.100.0" type="element" link_type="simple"
            width="30" height="30" hotspot_x="15" hotspot_y="15">
    <uuid uuid="{NEW-GUID}"/>
    <names>
        <name lang="fr">Mon Element</name>
        <name lang="en">My Element</name>
    </names>
    <informations>Auteur: r2d2</informations>
    <description>
        <circle x="-10" y="-10" diameter="20"
                style="line-style:normal;line-weight:normal;filling:none;color:black"
                antialias="true"/>
        <terminal x="0" y="-15" orientation="n" type="Generic"/>
    </description>
</definition>
'@ -replace 'NEW-GUID', [guid]::NewGuid().ToString()
[System.IO.File]::WriteAllText('element.elmt', $elmt,
    [System.Text.UTF8Encoding]::new($false))
```

## Sauvegarder en UTF-8 sans BOM

```powershell
$settings = New-Object System.Xml.XmlWriterSettings
$settings.Indent = $true
$settings.IndentChars = '    '
$settings.Encoding = [System.Text.UTF8Encoding]::new($false)
$writer = [System.Xml.XmlWriter]::Create('output.qet', $settings)
$doc.Save($writer)
$writer.Close()
```
