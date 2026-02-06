# Commande: /file-organize

Organiser automatiquement les fichiers par type, date ou catégorie personnalisée.

## Syntaxe

```
/file-organize [chemin] [mode] [options]
```

## Modes d'Organisation

### /file-organize downloads

Organiser le dossier Téléchargements :

```
╔══════════════════════════════════════════════════════════════╗
║           📁 ORGANISATION DOWNLOADS                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📊 ANALYSE:                                                 ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Fichiers trouvés    : 247                               │ ║
║  │ Taille totale       : 12.4 GB                           │ ║
║  │ Types détectés      : 15                                │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📋 PLAN D'ORGANISATION:                                     ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Documents  (42)  → Downloads\Documents\                 │ ║
║  │ Images     (89)  → Downloads\Images\                    │ ║
║  │ Videos     (12)  → Downloads\Videos\                    │ ║
║  │ Archives   (34)  → Downloads\Archives\                  │ ║
║  │ Installers (28)  → Downloads\Installers\                │ ║
║  │ Autres     (42)  → Downloads\Autres\                    │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Exécuter  [2] Prévisualiser  [3] Personnaliser          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
# Organiser Downloads par type
$Downloads = "$env:USERPROFILE\Downloads"
$Rules = @{
    "Documents"  = @(".pdf",".doc",".docx",".txt",".odt",".rtf",".xls",".xlsx",".ppt",".pptx")
    "Images"     = @(".jpg",".jpeg",".png",".gif",".webp",".svg",".bmp",".ico",".tiff")
    "Videos"     = @(".mp4",".mkv",".avi",".mov",".wmv",".flv",".webm")
    "Audio"      = @(".mp3",".wav",".flac",".m4a",".aac",".ogg",".wma")
    "Archives"   = @(".zip",".rar",".7z",".tar",".gz",".bz2")
    "Installers" = @(".exe",".msi",".msix",".appx",".dmg")
    "Code"       = @(".py",".js",".ts",".ps1",".sh",".bat",".cmd",".json",".xml",".yaml")
}

foreach ($Category in $Rules.Keys) {
    $DestPath = Join-Path $Downloads $Category
    if (!(Test-Path $DestPath)) { New-Item -ItemType Directory -Path $DestPath -Force }
    
    foreach ($Ext in $Rules[$Category]) {
        Get-ChildItem -Path $Downloads -Filter "*$Ext" -File | 
            Move-Item -Destination $DestPath -Force
    }
}

# Déplacer le reste dans "Autres"
$OthersPath = Join-Path $Downloads "Autres"
if (!(Test-Path $OthersPath)) { New-Item -ItemType Directory -Path $OthersPath -Force }
Get-ChildItem -Path $Downloads -File | Move-Item -Destination $OthersPath -Force
```

### /file-organize by-date [chemin]

Organiser par date (YYYY/YYYY-MM) :

```
╔══════════════════════════════════════════════════════════════╗
║           📅 ORGANISATION PAR DATE                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Structure créée:                                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Pictures\                                               │ ║
║  │ ├── 2024\                                               │ ║
║  │ │   ├── 2024-01\ (23 fichiers)                          │ ║
║  │ │   ├── 2024-02\ (45 fichiers)                          │ ║
║  │ │   └── ...                                             │ ║
║  │ ├── 2025\                                               │ ║
║  │ │   ├── 2025-01\ (67 fichiers)                          │ ║
║  │ │   └── 2025-02\ (34 fichiers)                          │ ║
║  │ └── 2026\                                               │ ║
║  │     └── 2026-02\ (12 fichiers)                          │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Total: 456 fichiers organisés dans 24 dossiers              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
# Organiser par date de modification
param(
    [string]$SourcePath = "$env:USERPROFILE\Pictures",
    [string]$DateFormat = "yyyy-MM"
)

Get-ChildItem -Path $SourcePath -File -Recurse | ForEach-Object {
    $Year = $_.LastWriteTime.ToString("yyyy")
    $YearMonth = $_.LastWriteTime.ToString("yyyy-MM")
    
    $DestFolder = Join-Path $SourcePath $Year $YearMonth
    if (!(Test-Path $DestFolder)) {
        New-Item -ItemType Directory -Path $DestFolder -Force | Out-Null
    }
    
    if ($_.DirectoryName -ne $DestFolder) {
        Move-Item -Path $_.FullName -Destination $DestFolder -Force
    }
}

Write-Host "✅ Fichiers organisés par date"
```

### /file-organize by-project [chemin]

Créer structure projet standard :

```
╔══════════════════════════════════════════════════════════════╗
║           📂 STRUCTURE PROJET                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Nom du projet: MultiPass-Website                            ║
║                                                              ║
║  Structure créée:                                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ MultiPass-Website\                                      │ ║
║  │ ├── 00-Admin\          # Contrats, briefs, planning     │ ║
║  │ ├── 01-Recherche\      # Études, benchmarks             │ ║
║  │ ├── 02-Design\         # Maquettes, assets              │ ║
║  │ ├── 03-Development\    # Code source                    │ ║
║  │ ├── 04-Content\        # Textes, médias                 │ ║
║  │ ├── 05-Livrables\      # Exports finaux                 │ ║
║  │ ├── 06-Archive\        # Anciennes versions             │ ║
║  │ └── README.md          # Documentation projet           │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
param([string]$ProjectName, [string]$BasePath = "$env:USERPROFILE\Documents\Projets")

$ProjectPath = Join-Path $BasePath $ProjectName
$Folders = @(
    "00-Admin",
    "01-Recherche",
    "02-Design",
    "03-Development",
    "04-Content",
    "05-Livrables",
    "06-Archive"
)

foreach ($Folder in $Folders) {
    New-Item -ItemType Directory -Path (Join-Path $ProjectPath $Folder) -Force | Out-Null
}

# Créer README
$ReadmeContent = @"
# $ProjectName

## Structure
- **00-Admin**: Contrats, briefs, planning
- **01-Recherche**: Études, benchmarks, références
- **02-Design**: Maquettes, wireframes, assets
- **03-Development**: Code source, configs
- **04-Content**: Textes, médias, contenus
- **05-Livrables**: Exports finaux clients
- **06-Archive**: Anciennes versions

## Conventions de nommage
- Date ISO: YYYY-MM-DD
- Versions: v01, v02...
- Pas d'espaces ni caractères spéciaux

Créé le: $(Get-Date -Format "yyyy-MM-dd")
"@

$ReadmeContent | Out-File -FilePath (Join-Path $ProjectPath "README.md") -Encoding UTF8
Write-Host "✅ Structure projet '$ProjectName' créée"
```

### /file-organize auto [chemin]

Organisation automatique intelligente :

```
╔══════════════════════════════════════════════════════════════╗
║           🤖 ORGANISATION AUTOMATIQUE                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Analyse IA des fichiers...                                  ║
║                                                              ║
║  📋 DÉTECTION:                                               ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Factures détectées      : 23 → Administratif\Factures\  │ ║
║  │ Photos vacances         : 156 → Pictures\2025\Vacances\ │ ║
║  │ Rapports travail        : 12 → Travail\Rapports\        │ ║
║  │ Captures écran          : 45 → Pictures\Screenshots\    │ ║
║  │ Fichiers code           : 34 → Dev\Projects\            │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Appliquer suggestions                                   ║
║  [2] Modifier manuellement                                   ║
║  [3] Annuler                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Options

| Option | Description | Exemple |
|--------|-------------|---------|
| `--dry-run` | Simuler sans déplacer | `/file-organize downloads --dry-run` |
| `--recursive` | Inclure sous-dossiers | `/file-organize . --recursive` |
| `--by-type` | Organiser par extension | `/file-organize . --by-type` |
| `--by-date` | Organiser par date | `/file-organize . --by-date` |
| `--verbose` | Afficher détails | `/file-organize . --verbose` |
| `--undo` | Annuler dernière organisation | `/file-organize --undo` |

## Exemples

```powershell
# Organiser Téléchargements par type
/file-organize downloads

# Organiser Photos par date
/file-organize "$env:USERPROFILE\Pictures" --by-date

# Simuler organisation sans exécuter
/file-organize downloads --dry-run

# Créer structure projet
/file-organize by-project "MonProjet"

# Organisation automatique intelligente
/file-organize auto "$env:USERPROFILE\Documents"
```
