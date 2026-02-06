# Commande: /file-clean

Nettoyer fichiers temporaires, inutiles et libérer de l'espace disque.

## Syntaxe

```
/file-clean [mode] [options]
```

## Modes de Nettoyage

### /file-clean temp

Nettoyer fichiers temporaires Windows :

```
╔══════════════════════════════════════════════════════════════╗
║           🧹 NETTOYAGE FICHIERS TEMPORAIRES                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📊 ANALYSE DES FICHIERS TEMPORAIRES:                        ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Emplacement              │ Fichiers │ Taille           │ ║
║  │ ─────────────────────────┼──────────┼────────────────  │ ║
║  │ %TEMP%                   │ 1,234    │ 2.3 GB           │ ║
║  │ Windows\Temp             │ 456      │ 890 MB           │ ║
║  │ Prefetch                 │ 234      │ 120 MB           │ ║
║  │ Recent                   │ 156      │ 12 MB            │ ║
║  │ Thumbnails               │ 2,345    │ 450 MB           │ ║
║  │ Browser Cache            │ 5,678    │ 1.8 GB           │ ║
║  │ ─────────────────────────┼──────────┼────────────────  │ ║
║  │ TOTAL                    │ 10,103   │ 5.6 GB           │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Nettoyer tout  [2] Sélectionner  [3] Annuler            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
# Nettoyage complet fichiers temporaires
$TempLocations = @(
    $env:TEMP,
    "$env:LOCALAPPDATA\Temp",
    "C:\Windows\Temp",
    "$env:LOCALAPPDATA\Microsoft\Windows\INetCache",
    "$env:LOCALAPPDATA\Microsoft\Windows\Explorer"
)

$TotalSize = 0
$TotalFiles = 0

foreach ($Location in $TempLocations) {
    if (Test-Path $Location) {
        $Files = Get-ChildItem -Path $Location -File -Recurse -ErrorAction SilentlyContinue
        $Size = ($Files | Measure-Object -Property Length -Sum).Sum
        $Count = $Files.Count
        
        Write-Host "Nettoyage $Location..."
        Write-Host "  $Count fichiers, $([math]::Round($Size/1MB,2)) MB"
        
        # Supprimer fichiers > 7 jours
        $Files | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } | 
            Remove-Item -Force -ErrorAction SilentlyContinue
        
        $TotalSize += $Size
        $TotalFiles += $Count
    }
}

Write-Host "`n✅ Nettoyé: $TotalFiles fichiers, $([math]::Round($TotalSize/1GB,2)) GB libérés"
```

### /file-clean downloads [jours]

Nettoyer anciens téléchargements :

```
╔══════════════════════════════════════════════════════════════╗
║           📥 NETTOYAGE DOWNLOADS                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Fichiers > 30 jours trouvés:                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Catégorie       │ Fichiers │ Taille    │ Action         │ ║
║  │ ────────────────┼──────────┼───────────┼──────────────  │ ║
║  │ Installers .exe │ 45       │ 3.2 GB    │ 🗑️ Supprimer   │ ║
║  │ Archives .zip   │ 23       │ 1.5 GB    │ 🗑️ Supprimer   │ ║
║  │ Documents .pdf  │ 12       │ 120 MB    │ 📦 Archiver    │ ║
║  │ Images          │ 34       │ 450 MB    │ 📦 Archiver    │ ║
║  │ Autres          │ 28       │ 890 MB    │ ❓ Réviser     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Espace récupérable: 6.2 GB                                  ║
║                                                              ║
║  [1] Nettoyer installers/archives (4.7 GB)                   ║
║  [2] Tout supprimer (6.2 GB)                                 ║
║  [3] Revoir manuellement                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
param(
    [int]$Days = 30,
    [switch]$DryRun
)

$Downloads = "$env:USERPROFILE\Downloads"
$OldFiles = Get-ChildItem -Path $Downloads -File -Recurse | 
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$Days) }

# Catégoriser
$Installers = $OldFiles | Where-Object { $_.Extension -in @('.exe','.msi','.msix') }
$Archives = $OldFiles | Where-Object { $_.Extension -in @('.zip','.rar','.7z') }
$Docs = $OldFiles | Where-Object { $_.Extension -in @('.pdf','.doc','.docx') }

Write-Host "Fichiers > $Days jours dans Downloads:"
Write-Host "  Installers: $($Installers.Count) ($([math]::Round(($Installers | Measure-Object Length -Sum).Sum/1GB,2)) GB)"
Write-Host "  Archives: $($Archives.Count) ($([math]::Round(($Archives | Measure-Object Length -Sum).Sum/1GB,2)) GB)"
Write-Host "  Documents: $($Docs.Count) ($([math]::Round(($Docs | Measure-Object Length -Sum).Sum/1MB,0)) MB)"

if (-not $DryRun) {
    # Supprimer installers et archives (généralement safe)
    $Installers + $Archives | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Installers et archives supprimés"
}
```

### /file-clean duplicates

Supprimer fichiers en double :

```
╔══════════════════════════════════════════════════════════════╗
║           🔄 SUPPRESSION DOUBLONS                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Doublons détectés: 234 groupes (567 fichiers)               ║
║  Espace récupérable: 4.5 GB                                  ║
║                                                              ║
║  Stratégie de conservation:                                  ║
║  [1] Garder le plus récent                                   ║
║  [2] Garder le plus ancien                                   ║
║  [3] Garder celui avec le meilleur nom                       ║
║  [4] Choisir manuellement                                    ║
║                                                              ║
║  Exemple de groupe:                                          ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✅ GARDER: Documents\Rapport_v03.pdf (2026-02-01)       │ ║
║  │ 🗑️ DELETE: Downloads\Rapport.pdf (2026-01-15)          │ ║
║  │ 🗑️ DELETE: Desktop\Rapport (1).pdf (2026-01-20)        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /file-clean empty

Supprimer dossiers vides :

```
╔══════════════════════════════════════════════════════════════╗
║           📂 DOSSIERS VIDES                                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Dossiers vides trouvés: 47                                  ║
║                                                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Documents\Ancien Projet\                                │ ║
║  │ Documents\Test\                                         │ ║
║  │ Downloads\Extracted\Temp\                               │ ║
║  │ Pictures\Album Vide\                                    │ ║
║  │ ... (+43 autres)                                        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Supprimer tous  [2] Voir liste complète  [3] Annuler    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
param(
    [string]$Path = "$env:USERPROFILE",
    [switch]$Delete
)

# Trouver tous les dossiers vides (récursivement, du plus profond)
$EmptyFolders = @()
do {
    $Found = Get-ChildItem -Path $Path -Directory -Recurse | 
        Where-Object { (Get-ChildItem $_.FullName -Force).Count -eq 0 }
    
    if ($Found) {
        $EmptyFolders += $Found
        if ($Delete) {
            $Found | Remove-Item -Force
        }
    }
} while ($Found.Count -gt 0 -and $Delete)

Write-Host "`n📂 Dossiers vides: $($EmptyFolders.Count)"
$EmptyFolders | ForEach-Object { Write-Host "  $($_.FullName)" }

if (-not $Delete) {
    Write-Host "`nUtilisez --delete pour supprimer"
}
```

### /file-clean recycle

Gérer la corbeille :

```
╔══════════════════════════════════════════════════════════════╗
║           🗑️ GESTION CORBEILLE                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Contenu de la corbeille:                                    ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Éléments        : 1,234                                 │ ║
║  │ Taille totale   : 8.5 GB                                │ ║
║  │ Plus ancien     : 2025-06-15 (8 mois)                   │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Vider complètement                                      ║
║  [2] Supprimer éléments > 30 jours                           ║
║  [3] Supprimer éléments > 1 GB                               ║
║  [4] Annuler                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
# Vider la corbeille
Clear-RecycleBin -Force -Confirm:$false

# Ou avec confirmation
Clear-RecycleBin -Confirm
```

## Nettoyage Complet

### /file-clean full

Nettoyage complet du système :

```powershell
# Exécute toutes les opérations de nettoyage
/file-clean full
```

Inclut:
- Fichiers temporaires
- Cache navigateurs
- Miniatures Windows
- Anciens logs
- Prefetch
- Windows Update cache
- Corbeille (> 30 jours)
- Dossiers vides

## Planification

### /file-clean schedule

Configurer nettoyage automatique :

```powershell
# Nettoyage hebdomadaire
/file-clean schedule weekly --day=sunday --time=03:00

# Nettoyage mensuel
/file-clean schedule monthly --day=1 --time=02:00
```

**Script tâche planifiée:**
```powershell
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\Scripts\cleanup.ps1"
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 3am
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable
Register-ScheduledTask -TaskName "Weekly File Cleanup" -Action $Action -Trigger $Trigger -Settings $Settings
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Simuler sans supprimer |
| `--days=N` | Fichiers plus vieux que N jours |
| `--size=N` | Fichiers plus gros que N MB |
| `--force` | Pas de confirmation |
| `--verbose` | Afficher chaque fichier |
| `--log` | Enregistrer dans fichier log |
