# Commande: /obs-clean

Nettoyer et optimiser le vault Obsidian.

## Syntaxe

```
/obs-clean [action] [options]
```

## Actions

### /obs-clean (analyse)

Analyser ce qui peut être nettoyé :

```
╔══════════════════════════════════════════════════════════════╗
║                    🧹 ANALYSE NETTOYAGE                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📊 ÉLÉMENTS DÉTECTÉS:                                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Type                      Nombre    Taille   Action     │ ║
║  │ ───────────────────────────────────────────────────────│ ║
║  │ 📄 Notes vides              5       2 KB     Supprimer  │ ║
║  │ 📎 Attachments orphelins   12      45 MB     Supprimer  │ ║
║  │ 📁 Dossiers vides           3       0 KB     Supprimer  │ ║
║  │ 🔄 Fichiers temporaires     8      12 KB     Supprimer  │ ║
║  │ 📋 Doublons potentiels      2      89 KB     Examiner   │ ║
║  │ 🗂️ Cache Obsidian          --      234 MB    Nettoyer   │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  💾 ESPACE RÉCUPÉRABLE: ~280 MB                              ║
║                                                              ║
║  ⚠️ AVERTISSEMENTS:                                          ║
║  • 12 attachments non référencés seront supprimés            ║
║  • Le cache Obsidian sera reconstruit au prochain lancement  ║
║                                                              ║
║  [1] Nettoyer tout  [2] Sélectionner  [3] Annuler            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-clean --all

Nettoyage complet automatique :

```
╔══════════════════════════════════════════════════════════════╗
║                    🧹 NETTOYAGE EN COURS                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [████████████████████████████████████████] 100%             ║
║                                                              ║
║  ✅ Notes vides supprimées          : 5                      ║
║  ✅ Attachments orphelins supprimés : 12 (45 MB)             ║
║  ✅ Dossiers vides supprimés        : 3                      ║
║  ✅ Fichiers temporaires supprimés  : 8                      ║
║  ✅ Cache Obsidian nettoyé          : 234 MB                 ║
║                                                              ║
║  📊 RÉSUMÉ:                                                  ║
║  • Fichiers supprimés : 28                                   ║
║  • Espace libéré      : 279 MB                               ║
║  • Temps              : 4.2s                                 ║
║                                                              ║
║  💡 Redémarrez Obsidian pour reconstruire le cache           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-clean empty

Supprimer notes vides :

```
╔══════════════════════════════════════════════════════════════╗
║                    📄 NOTES VIDES                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Trouvées: 5 notes vides ou quasi-vides                      ║
║                                                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Fichier                          Taille    Contenu      │ ║
║  │ ───────────────────────────────────────────────────────│ ║
║  │ _Inbox/Untitled.md               0 KB      (vide)       │ ║
║  │ _Inbox/New-Note.md               0.1 KB    "# "         │ ║
║  │ Conversations/Draft.md           0.2 KB    frontmatter  │ ║
║  │ Code/test.md                     0 KB      (vide)       │ ║
║  │ Projets/temp.md                  0.1 KB    "---"        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Supprimer toutes  [2] Sélectionner  [3] Annuler         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-clean attachments

Gérer les attachments (images, PDF, etc.) :

```
╔══════════════════════════════════════════════════════════════╗
║                    📎 ATTACHMENTS                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📊 STATISTIQUES:                                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Type          Fichiers    Taille    Référencés          │ ║
║  │ ───────────────────────────────────────────────────────│ ║
║  │ Images PNG       45       23 MB        42 ✅            │ ║
║  │ Images JPG       38       45 MB        35 ✅            │ ║
║  │ PDF              34      156 MB        32 ✅            │ ║
║  │ Autres           12        8 MB        10 ✅            │ ║
║  │ ─────────────────────────────────────────────────────── │ ║
║  │ TOTAL           129      232 MB       119               │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ⚠️ ORPHELINS (non référencés): 10 fichiers (45 MB)          ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ _Attachments/image-2025-old.png        (12 MB)          │ ║
║  │ _Attachments/screenshot-123.png        (2 MB)           │ ║
║  │ _Attachments/document-backup.pdf       (25 MB)          │ ║
║  │ ... (+7 autres)                                         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Supprimer orphelins  [2] Déplacer vers archive          ║
║  [3] Exporter liste       [4] Annuler                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-clean duplicates

Détecter et gérer les doublons :

```
╔══════════════════════════════════════════════════════════════╗
║                    🔄 DOUBLONS DÉTECTÉS                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Méthode: Hash MD5 du contenu                                ║
║                                                              ║
║  Groupe 1 (contenu identique):                               ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 📄 Concepts/C_Docker-Intro.md           (créé: 2026-01) │ ║
║  │ 📄 _Inbox/Docker-Notes.md               (créé: 2026-02) │ ║
║  │    → Suggestion: Garder C_Docker-Intro.md (plus ancien) │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Groupe 2 (très similaire - 95%):                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 📄 Projets/API/Endpoints.md                             │ ║
║  │ 📄 Projets/API/API-Endpoints.md                         │ ║
║  │    → Différence: 3 lignes                               │ ║
║  │    → Suggestion: Fusionner                              │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Supprimer doublons  [2] Examiner chaque  [3] Annuler    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-clean cache

Nettoyer le cache Obsidian :

```powershell
/obs-clean cache
```

Supprime :
- `.obsidian/cache`
- `.obsidian/workspace.json` (optionnel)
- Index de recherche corrompu

## Script PowerShell

```powershell
function Invoke-VaultCleanup {
    param(
        [string]$VaultPath = "$env:USERPROFILE\Documents\Knowledge",
        [switch]$DryRun,
        [switch]$All
    )
    
    $Results = @{
        EmptyNotes = @()
        OrphanAttachments = @()
        EmptyFolders = @()
        TempFiles = @()
        Duplicates = @()
        SpaceSaved = 0
    }
    
    Write-Host "`n🧹 Analyse du vault: $VaultPath`n" -ForegroundColor Cyan
    
    # === NOTES VIDES ===
    $Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
    foreach ($Note in $Notes) {
        $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
        $ContentLength = if ($Content) { 
            ($Content -replace '---[\s\S]*?---', '').Trim().Length 
        } else { 0 }
        
        if ($ContentLength -lt 10) {
            $Results.EmptyNotes += $Note
            $Results.SpaceSaved += $Note.Length
        }
    }
    Write-Host "  📄 Notes vides: $($Results.EmptyNotes.Count)" -ForegroundColor Yellow
    
    # === ATTACHMENTS ORPHELINS ===
    $AllContent = $Notes | ForEach-Object { Get-Content $_.FullName -Raw } | Out-String
    $Attachments = Get-ChildItem -Path $VaultPath -Recurse -Include "*.png","*.jpg","*.jpeg","*.gif","*.pdf","*.webp","*.svg"
    
    foreach ($Att in $Attachments) {
        $Referenced = $AllContent -match [regex]::Escape($Att.Name)
        if (!$Referenced) {
            $Results.OrphanAttachments += $Att
            $Results.SpaceSaved += $Att.Length
        }
    }
    Write-Host "  📎 Attachments orphelins: $($Results.OrphanAttachments.Count)" -ForegroundColor Yellow
    
    # === DOSSIERS VIDES ===
    $Folders = Get-ChildItem -Path $VaultPath -Recurse -Directory
    foreach ($Folder in $Folders) {
        $Items = Get-ChildItem -Path $Folder.FullName -Force
        if ($Items.Count -eq 0) {
            $Results.EmptyFolders += $Folder
        }
    }
    Write-Host "  📁 Dossiers vides: $($Results.EmptyFolders.Count)" -ForegroundColor Yellow
    
    # === FICHIERS TEMPORAIRES ===
    $TempPatterns = @("*.tmp", "*.bak", "*.swp", "*~", ".DS_Store", "Thumbs.db")
    foreach ($Pattern in $TempPatterns) {
        $TempFiles = Get-ChildItem -Path $VaultPath -Recurse -Filter $Pattern -Force
        foreach ($Temp in $TempFiles) {
            $Results.TempFiles += $Temp
            $Results.SpaceSaved += $Temp.Length
        }
    }
    Write-Host "  🔄 Fichiers temporaires: $($Results.TempFiles.Count)" -ForegroundColor Yellow
    
    # === RÉSUMÉ ===
    Write-Host "`n  💾 Espace récupérable: $([Math]::Round($Results.SpaceSaved / 1MB, 2)) MB" -ForegroundColor Green
    
    # === NETTOYAGE ===
    if (!$DryRun -and ($All -or (Read-Host "`nProcéder au nettoyage? [O/N]") -in @('O','o','Y','y'))) {
        
        # Supprimer notes vides
        foreach ($Note in $Results.EmptyNotes) {
            Remove-Item $Note.FullName -Force
        }
        
        # Supprimer attachments orphelins
        foreach ($Att in $Results.OrphanAttachments) {
            Remove-Item $Att.FullName -Force
        }
        
        # Supprimer dossiers vides
        foreach ($Folder in $Results.EmptyFolders) {
            Remove-Item $Folder.FullName -Force -ErrorAction SilentlyContinue
        }
        
        # Supprimer fichiers temporaires
        foreach ($Temp in $Results.TempFiles) {
            Remove-Item $Temp.FullName -Force
        }
        
        Write-Host "`n✅ Nettoyage terminé!" -ForegroundColor Green
    }
    
    return $Results
}

function Find-OrphanAttachments {
    param([string]$VaultPath)
    
    $Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
    $AllContent = $Notes | ForEach-Object { Get-Content $_.FullName -Raw } | Out-String
    
    $Attachments = Get-ChildItem -Path $VaultPath -Recurse -Include "*.png","*.jpg","*.jpeg","*.gif","*.pdf","*.webp"
    $Orphans = @()
    
    foreach ($Att in $Attachments) {
        if ($AllContent -notmatch [regex]::Escape($Att.Name)) {
            $Orphans += [PSCustomObject]@{
                Name = $Att.Name
                Path = $Att.FullName
                Size = $Att.Length
                LastModified = $Att.LastWriteTime
            }
        }
    }
    
    return $Orphans
}

function Find-DuplicateNotes {
    param([string]$VaultPath)
    
    $Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
    $Hashes = @{}
    $Duplicates = @()
    
    foreach ($Note in $Notes) {
        $Content = Get-Content $Note.FullName -Raw
        # Ignorer frontmatter pour le hash
        $Content = $Content -replace '---[\s\S]*?---', ''
        $Hash = [System.BitConverter]::ToString(
            [System.Security.Cryptography.MD5]::Create().ComputeHash(
                [System.Text.Encoding]::UTF8.GetBytes($Content.Trim())
            )
        )
        
        if ($Hashes[$Hash]) {
            $Duplicates += [PSCustomObject]@{
                Original = $Hashes[$Hash]
                Duplicate = $Note.FullName
                Hash = $Hash
            }
        } else {
            $Hashes[$Hash] = $Note.FullName
        }
    }
    
    return $Duplicates
}

function Clear-ObsidianCache {
    param([string]$VaultPath)
    
    $CachePath = Join-Path $VaultPath ".obsidian\cache"
    $WorkspacePath = Join-Path $VaultPath ".obsidian\workspace.json"
    
    $Cleared = 0
    
    if (Test-Path $CachePath) {
        $Size = (Get-ChildItem $CachePath -Recurse | Measure-Object -Property Length -Sum).Sum
        Remove-Item $CachePath -Recurse -Force
        $Cleared += $Size
        Write-Host "✅ Cache supprimé: $([Math]::Round($Size / 1MB, 2)) MB"
    }
    
    return $Cleared
}
```

## Options

| Option | Description |
|--------|-------------|
| `--all` | Nettoyer tout automatiquement |
| `--dry-run` | Prévisualiser sans supprimer |
| `--backup` | Backup avant nettoyage |
| `--force` | Pas de confirmation |
| `--exclude=pattern` | Exclure fichiers/dossiers |

## Exemples

```powershell
# Analyser
/obs-clean

# Nettoyer tout
/obs-clean --all

# Supprimer notes vides uniquement
/obs-clean empty

# Nettoyer attachments orphelins
/obs-clean attachments --delete

# Prévisualiser
/obs-clean --dry-run

# Nettoyer cache Obsidian
/obs-clean cache
```
