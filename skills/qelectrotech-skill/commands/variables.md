# Gerer les variables projet/folio QET

Affiche, modifie et supprime les variables d'un projet QElectroTech.

## Actions

| Action | Description |
|--------|-------------|
| `list <project>` | Lister toutes les variables du projet |
| `set <project> <name> <value>` | Definir une variable |
| `get <project> <name>` | Lire la valeur d'une variable |
| `delete <project> <name>` | Supprimer une variable |

## Hierarchie des variables

Les variables sont resolues par ordre de priorite :

```
Element (elementInformations) > Folio (inset) > Projet (properties/newdiagrams)
```

## Variables Projet (newdiagrams > inset)

| Variable | Attribut XML | Description |
|----------|-------------|-------------|
| Auteur | `author` | Auteur du projet |
| Installation | `plant` | Installation / Usine (IEC: `=`) |
| Machine | `machine` | Machine |
| Localisation | `locmach` | Localisation machine |
| Revision | `indexrev` | Indice de revision |

## Variables Folio (diagram)

| Variable | Attribut XML | Description |
|----------|-------------|-------------|
| Titre | `title` | Titre du folio |
| Folio | `folio` | Pagination (`%id/%total`) |
| Date | `date` | Date du folio |

## Variables Properties

| Variable | Noeud XML | Description |
|----------|-----------|-------------|
| Date sauvegarde | `<property name="saveddate">` | Auto-remplie par QET |
| Chemin fichier | `<property name="savedfilepath">` | Auto-remplie par QET |
| Nom fichier | `<property name="savedfilename">` | Auto-remplie par QET |
| Heure | `<property name="savedtime">` | Auto-remplie par QET |

## Actions PowerShell

### Lister les variables

```powershell
[xml]$project = [System.IO.File]::ReadAllText($projectPath)

# Variables projet (inset)
$inset = $project.project.newdiagrams.inset
Write-Host "=== Variables Projet ==="
Write-Host "  author: $($inset.author)"
Write-Host "  plant: $($inset.plant)"
Write-Host "  locmach: $($inset.locmach)"
Write-Host "  indexrev: $($inset.indexrev)"

# Variables properties
Write-Host "=== Properties ==="
$project.project.properties.property | ForEach-Object {
    Write-Host "  $($_.name): $($_.'#text')"
}

# Variables par folio
Write-Host "=== Folios ==="
$project.project.SelectNodes('diagram') | ForEach-Object {
    Write-Host "  Folio $($_.order): title=$($_.title), date=$($_.date)"
}
```

### Definir une variable

```powershell
[xml]$project = [System.IO.File]::ReadAllText($projectPath)
$project.project.newdiagrams.inset.SetAttribute('plant', '=A1')
$project.project.newdiagrams.inset.SetAttribute('author', 'r2d2')
# Sauvegarder en UTF-8 sans BOM
$settings = New-Object System.Xml.XmlWriterSettings
$settings.Indent = $true
$settings.Encoding = [System.Text.UTF8Encoding]::new($false)
$writer = [System.Xml.XmlWriter]::Create($projectPath, $settings)
$project.Save($writer)
$writer.Close()
```

## Exemple

```
/qet-variables list "projet.qet"
/qet-variables set "projet.qet" author "r2d2"
/qet-variables set "projet.qet" plant "=A1"
/qet-variables get "projet.qet" indexrev
```

$ARGUMENTS
