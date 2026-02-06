# Commande: /file-structure

Analyser ou créer une structure de dossiers.

## Syntaxe

```
/file-structure [action] [chemin] [options]
```

## Actions

### /file-structure analyze [chemin]

Analyser la structure existante d'un dossier :

```powershell
param([string]$Path = ".")

$Folders = Get-ChildItem -Path $Path -Directory -Recurse -ErrorAction SilentlyContinue
$Files = Get-ChildItem -Path $Path -File -Recurse -ErrorAction SilentlyContinue
$EmptyFolders = $Folders | Where-Object { (Get-ChildItem $_.FullName -Force -ErrorAction SilentlyContinue).Count -eq 0 }

# Profondeur
$BaseParts = ($Path -split '[\\/]').Count
$Depths = $Files | ForEach-Object { ($_.FullName -split '[\\/]').Count - $BaseParts }
$MaxDepth = ($Depths | Measure-Object -Maximum).Maximum
$AvgDepth = [math]::Round(($Depths | Measure-Object -Average).Average, 1)

# Fichiers par dossier
$FilesPerFolder = $Folders | ForEach-Object {
    @{ Name = $_.Name; Count = (Get-ChildItem $_.FullName -File -ErrorAction SilentlyContinue).Count }
}
$OverloadedFolders = $FilesPerFolder | Where-Object { $_.Count -gt 100 }

Write-Host ""
Write-Host "╔══════════════════════════════════════════════╗"
Write-Host "║     📁 ANALYSE STRUCTURE                      ║"
Write-Host "╠══════════════════════════════════════════════╣"
Write-Host "║                                              ║"
Write-Host "║  Dossiers:           $($Folders.Count.ToString().PadLeft(6))              ║"
Write-Host "║  Fichiers:           $($Files.Count.ToString().PadLeft(6))              ║"
Write-Host "║  Profondeur max:     $($MaxDepth.ToString().PadLeft(6))              ║"
Write-Host "║  Profondeur moyenne: $($AvgDepth.ToString().PadLeft(6))              ║"
Write-Host "║  Dossiers vides:     $($EmptyFolders.Count.ToString().PadLeft(6))              ║"
Write-Host "║  Dossiers surchargés:$($OverloadedFolders.Count.ToString().PadLeft(6)) (>100 fichiers) ║"
Write-Host "║                                              ║"

if ($MaxDepth -gt 4) {
    Write-Host "║  ⚠️ Profondeur > 4: considérer /file-flatten ║"
}
if ($EmptyFolders.Count -gt 0) {
    Write-Host "║  ⚠️ Dossiers vides: considérer /file-empty   ║"
}
Write-Host "║                                              ║"
Write-Host "╚══════════════════════════════════════════════╝"
```

### /file-structure apply [template]

Appliquer une structure prédéfinie :

| Template | Description |
|----------|-------------|
| `personal` | Structure Documents personnels (PARA) |
| `developer` | Structure projet développeur |
| `business` | Structure entreprise |
| `creative` | Structure créatif/designer |

```powershell
# Exemple: appliquer structure personal
param([string]$BasePath, [string]$Template = "personal")

$structures = @{
    "personal" = @(
        "_INBOX",
        "_ARCHIVE",
        "Administratif\Banque",
        "Administratif\Impots",
        "Administratif\Assurances",
        "Administratif\Factures",
        "Projets",
        "Travail",
        "Personnel"
    )
    "developer" = @(
        "01-Projects",
        "02-Libraries",
        "03-Scripts",
        "04-Config",
        "05-Archive"
    )
}

$dirs = $structures[$Template]
foreach ($dir in $dirs) {
    $fullPath = Join-Path $BasePath $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -Path $fullPath -ItemType Directory -Force | Out-Null
        Write-Host "Created: $dir"
    }
}
```

## Options

| Option | Description |
|--------|-------------|
| `analyze` | Analyser la structure existante |
| `apply [template]` | Appliquer un template |
| `--dry-run` | Simuler sans créer |
