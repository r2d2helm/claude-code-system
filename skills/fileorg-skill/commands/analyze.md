# Commande: /file-analyze

Analyser structure de fichiers, statistiques et qualité d'organisation.

## Syntaxe

```
/file-analyze [chemin] [mode]
```

## Modes d'Analyse

### /file-analyze [chemin]

Analyse complète d'un dossier :

```
╔══════════════════════════════════════════════════════════════╗
║           📊 ANALYSE: C:\Users\r2d2\Documents                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📁 STRUCTURE                                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Dossiers totaux    : 234                                │ ║
║  │ Fichiers totaux    : 4,567                              │ ║
║  │ Taille totale      : 45.6 GB                            │ ║
║  │ Profondeur max     : 7 niveaux ⚠️                       │ ║
║  │ Dossiers vides     : 23 ⚠️                              │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📈 DISTRIBUTION PAR TYPE                                    ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Documents  : ████████████████████░░░░░░░░ 45% (2,055)   │ ║
║  │ Images     : ██████████░░░░░░░░░░░░░░░░░░ 25% (1,142)   │ ║
║  │ Vidéos     : █████░░░░░░░░░░░░░░░░░░░░░░░ 12% (548)     │ ║
║  │ Archives   : ███░░░░░░░░░░░░░░░░░░░░░░░░░ 8% (365)      │ ║
║  │ Autres     : ███░░░░░░░░░░░░░░░░░░░░░░░░░ 10% (457)     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📅 DISTRIBUTION PAR ÂGE                                     ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ < 1 mois   : ████████░░░░░░░░░░░░░░░░░░░░ 20% (913)     │ ║
║  │ 1-6 mois   : ██████████████░░░░░░░░░░░░░░ 35% (1,599)   │ ║
║  │ 6-12 mois  : ████████░░░░░░░░░░░░░░░░░░░░ 20% (913)     │ ║
║  │ > 1 an     : ██████████░░░░░░░░░░░░░░░░░░ 25% (1,142)   │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ⚡ TOP 10 PLUS GROS FICHIERS                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 1. Backup-VM.vhdx              │ 12.5 GB │ 2025-12     │ ║
║  │ 2. Video-Conference.mp4        │ 3.2 GB  │ 2026-01     │ ║
║  │ 3. Archive-2024.zip            │ 2.8 GB  │ 2025-01     │ ║
║  │ ...                                                     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
param([string]$Path = ".")

$Files = Get-ChildItem -Path $Path -File -Recurse -ErrorAction SilentlyContinue
$Folders = Get-ChildItem -Path $Path -Directory -Recurse -ErrorAction SilentlyContinue

# Statistiques de base
$TotalSize = ($Files | Measure-Object -Property Length -Sum).Sum
$TotalFiles = $Files.Count
$TotalFolders = $Folders.Count

# Profondeur maximale
$MaxDepth = ($Files | ForEach-Object { 
    ($_.FullName -split '\\').Count - ($Path -split '\\').Count 
} | Measure-Object -Maximum).Maximum

# Dossiers vides
$EmptyFolders = $Folders | Where-Object { 
    (Get-ChildItem $_.FullName -Force).Count -eq 0 
}

# Distribution par extension
$ByExtension = $Files | Group-Object Extension | 
    Sort-Object Count -Descending | 
    Select-Object -First 10

# Distribution par âge
$Now = Get-Date
$ByAge = @{
    "< 1 mois" = ($Files | Where-Object { $_.LastWriteTime -gt $Now.AddMonths(-1) }).Count
    "1-6 mois" = ($Files | Where-Object { $_.LastWriteTime -le $Now.AddMonths(-1) -and $_.LastWriteTime -gt $Now.AddMonths(-6) }).Count
    "6-12 mois" = ($Files | Where-Object { $_.LastWriteTime -le $Now.AddMonths(-6) -and $_.LastWriteTime -gt $Now.AddYears(-1) }).Count
    "> 1 an" = ($Files | Where-Object { $_.LastWriteTime -le $Now.AddYears(-1) }).Count
}

# Plus gros fichiers
$LargestFiles = $Files | Sort-Object Length -Descending | Select-Object -First 10

# Affichage
Write-Host "`n📊 ANALYSE: $Path"
Write-Host "Fichiers: $TotalFiles | Dossiers: $TotalFolders | Taille: $([math]::Round($TotalSize/1GB,2)) GB"
Write-Host "Profondeur max: $MaxDepth | Dossiers vides: $($EmptyFolders.Count)"
```

### /file-analyze audit [chemin]

Audit qualité du nommage :

```
╔══════════════════════════════════════════════════════════════╗
║           📋 AUDIT QUALITÉ: Documents                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🎯 SCORE D'ORGANISATION: 62/100                             ║
║     ████████████████████████████░░░░░░░░░░░░░░░░░░           ║
║                                                              ║
║  ✅ POINTS POSITIFS                                          ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✓ Pas de fichiers à la racine excessive                 │ ║
║  │ ✓ Extensions cohérentes                                 │ ║
║  │ ✓ Taille moyenne des dossiers acceptable                │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ⚠️ PROBLÈMES DÉTECTÉS                                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ❌ 156 fichiers sans date ISO (35%)         -15 pts     │ ║
║  │ ❌ 89 fichiers avec espaces (20%)           -10 pts     │ ║
║  │ ❌ 34 fichiers avec accents (8%)            -5 pts      │ ║
║  │ ❌ 23 dossiers vides                        -3 pts      │ ║
║  │ ❌ Profondeur > 4 niveaux (7 max)           -5 pts      │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  💡 RECOMMANDATIONS                                          ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 1. /file-rename iso-date . --recursive                  │ ║
║  │ 2. /file-rename normalize .                             │ ║
║  │ 3. /file-empty delete                                   │ ║
║  │ 4. /file-flatten . --max-depth=4                        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
param([string]$Path = ".")

$Files = Get-ChildItem -Path $Path -File -Recurse
$Score = 100
$Issues = @()

# Vérifier date ISO (YYYY-MM-DD)
$NoDateISO = $Files | Where-Object { $_.BaseName -notmatch '^\d{4}-\d{2}-\d{2}' }
if ($NoDateISO.Count -gt 0) {
    $Percent = [math]::Round(($NoDateISO.Count / $Files.Count) * 100)
    $Penalty = [math]::Min(25, [math]::Round($Percent / 4))
    $Score -= $Penalty
    $Issues += "❌ $($NoDateISO.Count) fichiers sans date ISO ($Percent%) -$Penalty pts"
}

# Vérifier espaces
$WithSpaces = $Files | Where-Object { $_.BaseName -match '\s' }
if ($WithSpaces.Count -gt 0) {
    $Percent = [math]::Round(($WithSpaces.Count / $Files.Count) * 100)
    $Penalty = [math]::Min(15, [math]::Round($Percent / 3))
    $Score -= $Penalty
    $Issues += "❌ $($WithSpaces.Count) fichiers avec espaces ($Percent%) -$Penalty pts"
}

# Vérifier accents
$WithAccents = $Files | Where-Object { $_.BaseName -match '[éèêëàâäùûüîïôöç]' }
if ($WithAccents.Count -gt 0) {
    $Percent = [math]::Round(($WithAccents.Count / $Files.Count) * 100)
    $Penalty = [math]::Min(10, [math]::Round($Percent / 2))
    $Score -= $Penalty
    $Issues += "❌ $($WithAccents.Count) fichiers avec accents ($Percent%) -$Penalty pts"
}

# Vérifier caractères spéciaux
$WithSpecial = $Files | Where-Object { $_.BaseName -match '[!@#$%^&*()\[\]{}|;:,<>?]' }
if ($WithSpecial.Count -gt 0) {
    $Score -= 5
    $Issues += "❌ $($WithSpecial.Count) fichiers avec caractères spéciaux -5 pts"
}

# Vérifier profondeur
$MaxDepth = ($Files | ForEach-Object { ($_.FullName -split '\\').Count } | Measure-Object -Maximum).Maximum
$BaseDepth = ($Path -split '\\').Count
$Depth = $MaxDepth - $BaseDepth
if ($Depth -gt 4) {
    $Score -= 5
    $Issues += "❌ Profondeur excessive: $Depth niveaux (max recommandé: 4) -5 pts"
}

Write-Host "`n🎯 SCORE D'ORGANISATION: $Score/100"
if ($Issues.Count -gt 0) {
    Write-Host "`n⚠️ PROBLÈMES DÉTECTÉS:"
    $Issues | ForEach-Object { Write-Host "  $_" }
}
```

### /file-analyze tree [chemin]

Afficher arborescence visuelle :

```
╔══════════════════════════════════════════════════════════════╗
║           🌲 ARBORESCENCE: Documents                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Documents\                                     [45.6 GB]    ║
║  ├── _INBOX\                                   [2.3 GB]     ║
║  │   └── 34 fichiers à trier                               ║
║  ├── Administratif\                            [1.2 GB]     ║
║  │   ├── Banque\                    [450 MB]               ║
║  │   ├── Impots\                    [320 MB]               ║
║  │   └── Factures\                  [430 MB]               ║
║  ├── Projets\                                  [28.5 GB]    ║
║  │   ├── MultiPass\                 [12.3 GB]              ║
║  │   ├── ClientA\                   [8.2 GB]               ║
║  │   └── ClientB\                   [8.0 GB]               ║
║  ├── Travail\                                  [8.6 GB]     ║
║  └── Personnel\                                [5.0 GB]     ║
║                                                              ║
║  Légende: [Taille] 🟢<100 fichiers 🟡100-500 🔴>500         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
function Show-Tree {
    param(
        [string]$Path,
        [int]$Depth = 0,
        [int]$MaxDepth = 3,
        [string]$Indent = ""
    )
    
    if ($Depth -ge $MaxDepth) { return }
    
    $Items = Get-ChildItem -Path $Path -Directory | Sort-Object Name
    $LastIndex = $Items.Count - 1
    
    for ($i = 0; $i -lt $Items.Count; $i++) {
        $Item = $Items[$i]
        $IsLast = ($i -eq $LastIndex)
        $Connector = if ($IsLast) { "└── " } else { "├── " }
        $NextIndent = $Indent + $(if ($IsLast) { "    " } else { "│   " })
        
        $Size = (Get-ChildItem $Item.FullName -Recurse -File -ErrorAction SilentlyContinue | 
            Measure-Object -Property Length -Sum).Sum
        $SizeStr = if ($Size -gt 1GB) { "$([math]::Round($Size/1GB,1)) GB" }
                   elseif ($Size -gt 1MB) { "$([math]::Round($Size/1MB,0)) MB" }
                   else { "$([math]::Round($Size/1KB,0)) KB" }
        
        Write-Host "$Indent$Connector$($Item.Name)\" -NoNewline
        Write-Host " [$SizeStr]" -ForegroundColor DarkGray
        
        Show-Tree -Path $Item.FullName -Depth ($Depth + 1) -MaxDepth $MaxDepth -Indent $NextIndent
    }
}

Show-Tree -Path $Path -MaxDepth 3
```

## Rapports

### /file-analyze report [chemin]

Générer rapport complet en Markdown ou HTML :

```powershell
# Générer rapport Markdown
/file-analyze report "$env:USERPROFILE\Documents" --format=md

# Générer rapport HTML
/file-analyze report "$env:USERPROFILE\Documents" --format=html --open
```

## Options

| Option | Description |
|--------|-------------|
| `--format=md` | Rapport Markdown |
| `--format=html` | Rapport HTML |
| `--format=json` | Export JSON |
| `--depth=N` | Profondeur d'analyse |
| `--include-hidden` | Inclure fichiers cachés |
| `--open` | Ouvrir rapport après génération |
