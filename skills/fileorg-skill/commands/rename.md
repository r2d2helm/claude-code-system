# Commande: /file-rename

Renommer fichiers selon les conventions de nommage standardisées.

## Syntaxe

```
/file-rename [chemin] [mode] [options]
```

## Modes de Renommage

### /file-rename iso-date [chemin]

Ajouter préfixe date ISO 8601 aux fichiers :

```
╔══════════════════════════════════════════════════════════════╗
║           📅 RENOMMAGE DATE ISO                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📋 PRÉVISUALISATION:                                        ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ AVANT                    →  APRÈS                       │ ║
║  │ ──────────────────────────────────────────────────────  │ ║
║  │ Facture EDF.pdf          →  2026-01-15_Facture-EDF.pdf  │ ║
║  │ Photo vacances.jpg       →  2025-08-22_Photo-vacances.jpg│ ║
║  │ Rapport final v2.docx    →  2026-02-01_Rapport-final_v02.docx│ ║
║  │ scan001.pdf              →  2026-02-03_scan001.pdf      │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Fichiers à renommer: 47                                     ║
║                                                              ║
║  [1] Appliquer  [2] Modifier  [3] Annuler                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
param(
    [string]$Path = ".",
    [switch]$UseCreationDate,
    [switch]$DryRun
)

Get-ChildItem -Path $Path -File | ForEach-Object {
    $Date = if ($UseCreationDate) { $_.CreationTime } else { $_.LastWriteTime }
    $DatePrefix = $Date.ToString("yyyy-MM-dd")
    
    # Nettoyer le nom existant
    $CleanName = $_.BaseName -replace '\s+', '-'
    $CleanName = $CleanName -replace '[^\w\-]', ''
    
    # Éviter double préfixe date
    if ($CleanName -notmatch '^\d{4}-\d{2}-\d{2}') {
        $NewName = "${DatePrefix}_${CleanName}$($_.Extension)"
    } else {
        $NewName = "${CleanName}$($_.Extension)"
    }
    
    if ($DryRun) {
        Write-Host "$($_.Name) → $NewName"
    } else {
        Rename-Item -Path $_.FullName -NewName $NewName
    }
}
```

### /file-rename normalize [chemin]

Normaliser les noms de fichiers :

```
╔══════════════════════════════════════════════════════════════╗
║           🔧 NORMALISATION DES NOMS                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📋 CORRECTIONS:                                             ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Problème                 →  Correction                  │ ║
║  │ ──────────────────────────────────────────────────────  │ ║
║  │ Mon Document (1).pdf     →  Mon-Document_01.pdf         │ ║
║  │ café & croissant.jpg     →  cafe-croissant.jpg          │ ║
║  │ RAPPORT FINAL!!!.docx    →  Rapport-Final.docx          │ ║
║  │ fichier   mal  nommé.txt →  fichier-mal-nomme.txt       │ ║
║  │ été_2025_été.png         →  ete-2025.png                │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Corrections: espaces (23), accents (12), spéciaux (8)       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
function Normalize-FileName {
    param([string]$Name)
    
    # Table de remplacement accents
    $Accents = @{
        'é'='e'; 'è'='e'; 'ê'='e'; 'ë'='e'
        'à'='a'; 'â'='a'; 'ä'='a'
        'ù'='u'; 'û'='u'; 'ü'='u'
        'î'='i'; 'ï'='i'
        'ô'='o'; 'ö'='o'
        'ç'='c'
        'É'='E'; 'È'='E'; 'Ê'='E'
        'À'='A'; 'Â'='A'
        'Ù'='U'; 'Û'='U'
        'Ô'='O'
        'Ç'='C'
    }
    
    # Remplacer accents
    foreach ($Key in $Accents.Keys) {
        $Name = $Name -replace $Key, $Accents[$Key]
    }
    
    # Remplacer espaces multiples par un tiret
    $Name = $Name -replace '\s+', '-'
    
    # Supprimer caractères spéciaux
    $Name = $Name -replace '[^\w\-\.]', ''
    
    # Supprimer tirets multiples
    $Name = $Name -replace '\-+', '-'
    
    # Nettoyer début et fin
    $Name = $Name.Trim('-')
    
    return $Name
}

Get-ChildItem -Path $Path -File | ForEach-Object {
    $NewName = Normalize-FileName -Name $_.BaseName
    $NewFullName = "$NewName$($_.Extension)"
    
    if ($_.Name -ne $NewFullName) {
        Rename-Item -Path $_.FullName -NewName $NewFullName
        Write-Host "✓ $($_.Name) → $NewFullName"
    }
}
```

### /file-rename version [chemin]

Gérer le versionnage des fichiers :

```
╔══════════════════════════════════════════════════════════════╗
║           🔢 GESTION DES VERSIONS                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📋 ANALYSE DES VERSIONS:                                    ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Fichier                  │ Versions │ Action            │ ║
║  │ ─────────────────────────┼──────────┼─────────────────  │ ║
║  │ Rapport-Analyse          │ 5        │ Garder v05        │ ║
║  │ ├── Rapport final.docx   │          │ → Archive         │ ║
║  │ ├── Rapport final2.docx  │          │ → Archive         │ ║
║  │ ├── Rapport FINAL.docx   │          │ → Archive         │ ║
║  │ └── Rapport v3.docx      │          │ → Archive         │ ║
║  │                          │          │                   │ ║
║  │ Proposition-Client       │ 3        │ Renommer          │ ║
║  │ ├── Proposition.pdf      │          │ → _v01.pdf        │ ║
║  │ ├── Proposition (1).pdf  │          │ → _v02.pdf        │ ║
║  │ └── Proposition new.pdf  │          │ → _v03.pdf        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Standardiser versions  [2] Archiver anciennes           ║
║  [3] Supprimer doublons     [4] Manuel                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
# Détecter et standardiser les versions
param([string]$Path = ".")

# Patterns de version courants
$VersionPatterns = @(
    '[-_]?v?(\d+)$',           # v1, v2, -v1
    '\s*\((\d+)\)$',           # (1), (2)
    '[-_]?(final\d*)$',        # final, final2
    '[-_]?(new|nouveau|old)$'  # new, old
)

function Get-NextVersion {
    param([string]$BaseName, [int]$Current = 0)
    return "{0}_v{1:D2}" -f $BaseName, ($Current + 1)
}

$Files = Get-ChildItem -Path $Path -File | Group-Object { 
    $Name = $_.BaseName
    foreach ($Pattern in $VersionPatterns) {
        $Name = $Name -replace $Pattern, ''
    }
    $Name.Trim()
}

foreach ($Group in $Files | Where-Object Count -gt 1) {
    Write-Host "`n📁 $($Group.Name) - $($Group.Count) versions détectées:"
    
    $Version = 1
    foreach ($File in $Group.Group | Sort-Object LastWriteTime) {
        $NewName = Get-NextVersion -BaseName $Group.Name -Current $Version
        Write-Host "  $($File.Name) → $NewName$($File.Extension)"
        $Version++
    }
}
```

### /file-rename bulk [chemin] [pattern]

Renommage en masse avec pattern :

```
╔══════════════════════════════════════════════════════════════╗
║           📝 RENOMMAGE EN MASSE                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Pattern: {date}_{type}_{numero:3}                           ║
║  Exemple: 2026-02-03_Photo_001.jpg                           ║
║                                                              ║
║  Tokens disponibles:                                         ║
║  {date}     - Date ISO (2026-02-03)                          ║
║  {year}     - Année (2026)                                   ║
║  {month}    - Mois (02)                                      ║
║  {day}      - Jour (03)                                      ║
║  {numero:N} - Numéro séquentiel (N = nb chiffres)            ║
║  {original} - Nom original                                   ║
║  {ext}      - Extension                                      ║
║  {type}     - Type personnalisé                              ║
║                                                              ║
║  Prévisualisation:                                           ║
║  IMG_001.jpg → 2026-02-03_Photo_001.jpg                      ║
║  IMG_002.jpg → 2026-02-03_Photo_002.jpg                      ║
║  ...                                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
param(
    [string]$Path,
    [string]$Pattern = "{date}_{original}",
    [string]$Type = "File",
    [switch]$DryRun
)

$Counter = 1
Get-ChildItem -Path $Path -File | Sort-Object Name | ForEach-Object {
    $Date = $_.LastWriteTime.ToString("yyyy-MM-dd")
    $Year = $_.LastWriteTime.ToString("yyyy")
    $Month = $_.LastWriteTime.ToString("MM")
    $Day = $_.LastWriteTime.ToString("dd")
    
    $NewName = $Pattern
    $NewName = $NewName -replace '\{date\}', $Date
    $NewName = $NewName -replace '\{year\}', $Year
    $NewName = $NewName -replace '\{month\}', $Month
    $NewName = $NewName -replace '\{day\}', $Day
    $NewName = $NewName -replace '\{original\}', $_.BaseName
    $NewName = $NewName -replace '\{type\}', $Type
    $NewName = $NewName -replace '\{numero:(\d+)\}', { "{0:D$($_.Groups[1].Value)}" -f $Counter }
    $NewName = $NewName -replace '\{numero\}', $Counter
    
    $NewFullName = "$NewName$($_.Extension)"
    
    if ($DryRun) {
        Write-Host "$($_.Name) → $NewFullName"
    } else {
        Rename-Item -Path $_.FullName -NewName $NewFullName
    }
    
    $Counter++
}
```

## Options Globales

| Option | Description |
|--------|-------------|
| `--dry-run` | Prévisualiser sans renommer |
| `--recursive` | Inclure sous-dossiers |
| `--lowercase` | Forcer minuscules |
| `--uppercase` | Forcer majuscules |
| `--pascalcase` | Appliquer PascalCase |
| `--backup` | Créer copie avant renommage |
| `--log` | Enregistrer les changements |

## Exemples

```powershell
# Ajouter date ISO à tous les fichiers
/file-rename iso-date "$env:USERPROFILE\Documents"

# Normaliser noms (espaces, accents)
/file-rename normalize "$env:USERPROFILE\Downloads"

# Prévisualiser sans exécuter
/file-rename iso-date . --dry-run

# Renommer photos en masse
/file-rename bulk "$env:USERPROFILE\Pictures" "{date}_Photo_{numero:3}"

# Standardiser versions
/file-rename version "$env:USERPROFILE\Documents\Rapports"
```
