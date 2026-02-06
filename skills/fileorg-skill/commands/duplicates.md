# Commande: /file-duplicates

Détecter et gérer les fichiers en double.

## Syntaxe

```
/file-duplicates [chemin] [options]
```

## Modes de Détection

### /file-duplicates scan [chemin]

Scanner pour trouver les doublons :

```
╔══════════════════════════════════════════════════════════════╗
║           🔍 SCAN DOUBLONS: Documents                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ⏳ Scan en cours...                                         ║
║  [████████████████████████████░░░░░░░░░░░░] 75%              ║
║  Analysés: 4,567 / 6,123 fichiers                            ║
║                                                              ║
║  📊 RÉSULTATS PRÉLIMINAIRES:                                 ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Méthode           │ Groupes │ Fichiers │ Taille         │ ║
║  │ ──────────────────┼─────────┼──────────┼──────────────  │ ║
║  │ Hash identique    │ 156     │ 412      │ 3.2 GB         │ ║
║  │ Nom identique     │ 89      │ 234      │ 1.8 GB         │ ║
║  │ Taille identique  │ 234     │ 567      │ 2.5 GB         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Doublons confirmés (hash): 156 groupes                      ║
║  Espace récupérable: 3.2 GB                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
param(
    [string]$Path = ".",
    [ValidateSet("Hash","Name","Size")]
    [string]$Method = "Hash"
)

Write-Host "🔍 Scan des doublons dans $Path (méthode: $Method)..."

$Files = Get-ChildItem -Path $Path -File -Recurse -ErrorAction SilentlyContinue

switch ($Method) {
    "Hash" {
        # Grouper par hash MD5 (plus fiable)
        $Duplicates = $Files | ForEach-Object {
            $Hash = (Get-FileHash $_.FullName -Algorithm MD5 -ErrorAction SilentlyContinue).Hash
            [PSCustomObject]@{
                Path = $_.FullName
                Name = $_.Name
                Size = $_.Length
                Hash = $Hash
                Date = $_.LastWriteTime
            }
        } | Where-Object { $_.Hash } | Group-Object Hash | Where-Object Count -gt 1
    }
    "Name" {
        $Duplicates = $Files | Group-Object Name | Where-Object Count -gt 1
    }
    "Size" {
        $Duplicates = $Files | Group-Object Length | Where-Object Count -gt 1
    }
}

$TotalGroups = $Duplicates.Count
$TotalFiles = ($Duplicates | ForEach-Object { $_.Count } | Measure-Object -Sum).Sum
$TotalSize = ($Duplicates | ForEach-Object { 
    ($_.Group | Select-Object -Skip 1) | ForEach-Object { $_.Length }
} | Measure-Object -Sum).Sum

Write-Host "`n📊 RÉSULTATS:"
Write-Host "  Groupes de doublons: $TotalGroups"
Write-Host "  Fichiers en double: $TotalFiles"
Write-Host "  Espace récupérable: $([math]::Round($TotalSize/1GB,2)) GB"

return $Duplicates
```

### /file-duplicates list [chemin]

Afficher liste détaillée des doublons :

```
╔══════════════════════════════════════════════════════════════╗
║           📋 LISTE DES DOUBLONS                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  GROUPE 1 (3 fichiers, 45 MB)                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Hash: 5d41402abc4b2a76b9719d911017c592                  │ ║
║  │                                                         │ ║
║  │ ★ Documents\Rapports\2026-02-01_Rapport_v03.pdf        │ ║
║  │   15 MB | 2026-02-01 | ✅ GARDER (plus récent)          │ ║
║  │                                                         │ ║
║  │   Downloads\Rapport.pdf                                 │ ║
║  │   15 MB | 2026-01-15 | 🗑️ Supprimer                    │ ║
║  │                                                         │ ║
║  │   Desktop\Rapport (1).pdf                               │ ║
║  │   15 MB | 2026-01-20 | 🗑️ Supprimer                    │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  GROUPE 2 (2 fichiers, 120 MB)                               ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Hash: 7d793037a0760186574b0282f2f435e7                  │ ║
║  │                                                         │ ║
║  │ ★ Pictures\2025\2025-08_Vacances_001.jpg               │ ║
║  │   60 MB | 2025-08-15 | ✅ GARDER (meilleur nom)         │ ║
║  │                                                         │ ║
║  │   Pictures\IMG_4521.jpg                                 │ ║
║  │   60 MB | 2025-08-15 | 🗑️ Supprimer                    │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ... (154 groupes de plus)                                   ║
║                                                              ║
║  [1] Supprimer doublons  [2] Exporter liste  [3] Manuel      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /file-duplicates delete [chemin]

Supprimer les doublons automatiquement :

```
╔══════════════════════════════════════════════════════════════╗
║           🗑️ SUPPRESSION DOUBLONS                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Stratégie de conservation:                                  ║
║                                                              ║
║  [1] Garder le plus RÉCENT (recommandé pour documents)       ║
║  [2] Garder le plus ANCIEN (recommandé pour photos)          ║
║  [3] Garder le MEILLEUR NOM (date ISO, pas de (1))           ║
║  [4] Garder dans dossier PRIORITAIRE                         ║
║      Documents > Pictures > Downloads > Desktop              ║
║                                                              ║
║  ⚠️ Cette action est irréversible!                           ║
║                                                              ║
║  Résumé:                                                     ║
║  • 156 groupes de doublons                                   ║
║  • 256 fichiers à supprimer                                  ║
║  • 3.2 GB à libérer                                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
param(
    [string]$Path = ".",
    [ValidateSet("Newest","Oldest","BestName","Priority")]
    [string]$Keep = "Newest",
    [switch]$DryRun
)

$Duplicates = # ... résultat du scan

foreach ($Group in $Duplicates) {
    $Files = $Group.Group
    
    $ToKeep = switch ($Keep) {
        "Newest" { $Files | Sort-Object Date -Descending | Select-Object -First 1 }
        "Oldest" { $Files | Sort-Object Date | Select-Object -First 1 }
        "BestName" { 
            $Files | Sort-Object { 
                # Score: date ISO = 10, pas de (1) = 5, pas d'espaces = 3
                $Score = 0
                if ($_.Name -match '^\d{4}-\d{2}-\d{2}') { $Score += 10 }
                if ($_.Name -notmatch '\(\d+\)') { $Score += 5 }
                if ($_.Name -notmatch '\s') { $Score += 3 }
                $Score
            } -Descending | Select-Object -First 1
        }
        "Priority" {
            $Priority = @("Documents","Pictures","Downloads","Desktop")
            $Files | Sort-Object { 
                $Path = $_.Path
                $Index = $Priority.Count
                for ($i = 0; $i -lt $Priority.Count; $i++) {
                    if ($Path -match $Priority[$i]) { $Index = $i; break }
                }
                $Index
            } | Select-Object -First 1
        }
    }
    
    $ToDelete = $Files | Where-Object { $_.Path -ne $ToKeep.Path }
    
    foreach ($File in $ToDelete) {
        if ($DryRun) {
            Write-Host "🗑️ $($File.Path)"
        } else {
            Remove-Item -Path $File.Path -Force
        }
    }
    
    Write-Host "✅ Gardé: $($ToKeep.Path)"
}
```

### /file-duplicates compare [dossier1] [dossier2]

Comparer deux dossiers :

```
╔══════════════════════════════════════════════════════════════╗
║           🔄 COMPARAISON: Documents vs Backup                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📊 RÉSULTAT:                                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Identiques (hash)       : 4,234 fichiers                │ ║
║  │ Uniquement Documents    : 123 fichiers                  │ ║
║  │ Uniquement Backup       : 45 fichiers                   │ ║
║  │ Modifiés (même nom)     : 67 fichiers                   │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Actions suggérées:                                          ║
║  [1] Synchroniser (Documents → Backup)                       ║
║  [2] Voir fichiers uniques                                   ║
║  [3] Voir fichiers modifiés                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Options

| Option | Description |
|--------|-------------|
| `--method=hash` | Comparaison par hash (défaut, plus fiable) |
| `--method=name` | Comparaison par nom |
| `--method=size` | Comparaison par taille |
| `--keep=newest` | Garder le plus récent |
| `--keep=oldest` | Garder le plus ancien |
| `--keep=bestname` | Garder le meilleur nom |
| `--dry-run` | Simuler sans supprimer |
| `--min-size=N` | Ignorer fichiers < N MB |
| `--extensions=.pdf,.jpg` | Filtrer par extensions |
| `--exclude=folder` | Exclure dossier |
| `--export=file.csv` | Exporter résultats |

## Exemples

```powershell
# Scanner Documents pour doublons
/file-duplicates scan "$env:USERPROFILE\Documents"

# Scanner avec méthode par nom
/file-duplicates scan . --method=name

# Supprimer doublons en gardant le plus récent
/file-duplicates delete . --keep=newest

# Simuler suppression
/file-duplicates delete . --keep=bestname --dry-run

# Comparer deux dossiers
/file-duplicates compare "C:\Documents" "D:\Backup\Documents"

# Exporter liste des doublons
/file-duplicates scan . --export=doublons.csv
```

## Exclusions par Défaut

Ces dossiers sont ignorés par défaut :
- `node_modules`
- `.git`
- `AppData`
- `Windows`
- `Program Files`

Utiliser `--no-exclude` pour tout scanner.
