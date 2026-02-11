# Gerer les cartouches QElectroTech

Creer, lister et appliquer des cartouches personnalises (.titleblock).

## Actions

| Action | Description |
|--------|-------------|
| `list` | Lister les cartouches disponibles (systeme + utilisateur) |
| `show <name>` | Afficher la structure d'un cartouche |
| `create <name>` | Creer un nouveau cartouche personnalise |
| `apply <name> <project>` | Appliquer un cartouche a un projet |

## Cartouches par defaut

| Template | Description |
|----------|-------------|
| `default` | Simple : auteur, titre, fichier, date, folio |
| `A4_1` | Format A4 standard |
| `DIN_A4` | Format DIN A4 allemand |
| `ISO7200_A4_V1` | Norme ISO 7200 |
| `double-logo` | Avec 2 logos (client + bureau etude) |
| `single-logo` | Avec 1 logo |
| `page_de garde` | Page de garde projet |
| `DIN_A3` | Format A3 |
| `ANSI_D` | Format americain D |
| `GostFrame` | Format russe GOST |

## Structure XML (.titleblock)

```xml
<titleblocktemplate name="mon_cartouche">
    <information>Description du cartouche</information>
    <logos>
        <logo name="logo1" type="png" storage="base64">
            <!-- Donnees base64 du logo -->
        </logo>
    </logos>
    <grid cols="t22%;r100%;t22%;" rows="25;25;25;25;">
        <field valign="center" row="0" col="0" name="author"
               displaylabel="true" align="left" hadjust="true">
            <value>
                <translation lang="fr">%author</translation>
            </value>
            <label>
                <translation lang="fr">Auteur</translation>
                <translation lang="en">Author</translation>
            </label>
        </field>
    </grid>
</titleblocktemplate>
```

## Variables disponibles dans les cartouches

| Variable | Description |
|----------|-------------|
| `%title` | Titre du folio |
| `%author` | Auteur du projet |
| `%date` | Date du folio |
| `%folio` | Pagination (ex: 1/8) |
| `%filename` | Nom du fichier |
| `%plant` | Installation / Usine |
| `%machine` | Machine |
| `%locmach` | Localisation machine |
| `%indexrev` | Indice de revision |
| `%version` | Version QET |

## Grille du cartouche

La grille utilise un systeme colonnes x lignes :
- **Colonnes** : `t<size>%` (taille fixe) ou `r<size>%` (taille relative)
- **Lignes** : hauteur en pixels, separees par `;`
- Les champs occupent une cellule (row/col) avec possibilite de `rowspan`/`colspan`

## Actions PowerShell

### Lister les cartouches
```powershell
$qetPath = "C:\Program Files\QElectroTech\qelectrotech-0.100.1+git8595-x86-win64-readytouse"
Get-ChildItem "$qetPath\titleblocks\*.titleblock" | ForEach-Object { $_.BaseName }
```

### Appliquer a un projet
```powershell
[xml]$project = [System.IO.File]::ReadAllText($projectPath)
$project.project.newdiagrams.inset.SetAttribute('customtitleblock', $titleblockName)
```

## Exemple

```
/qet-titleblock list
/qet-titleblock show "ISO7200_A4_V1"
/qet-titleblock create "MonEntreprise"
/qet-titleblock apply "MonEntreprise" "projet.qet"
```

$ARGUMENTS
