# Commande: /obs-health

Diagnostic complet de la santé du vault Obsidian.

## Syntaxe

```
/obs-health [options]
```

## Modes

### /obs-health (complet)

Analyse complète du vault :

```
╔══════════════════════════════════════════════════════════════╗
║                    🏥 SANTÉ DU VAULT                         ║
║                    Knowledge                                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📍 Chemin: C:\Users\r2d2\Documents\Knowledge                ║
║  📅 Analyse: 2026-02-04 14:30:22                             ║
║                                                              ║
║  ═══════════════════════════════════════════════════════════ ║
║                                                              ║
║  SCORE GLOBAL: 78/100                                        ║
║  ████████████████████████████████████░░░░░░░░░░              ║
║                                                              ║
║  ═══════════════════════════════════════════════════════════ ║
║                                                              ║
║  📊 STATISTIQUES:                                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Notes totales       : 456                               │ ║
║  │ Mots totaux         : 125,430                           │ ║
║  │ Liens internes      : 1,234                             │ ║
║  │ Tags uniques        : 89                                │ ║
║  │ Attachments         : 156 (234 MB)                      │ ║
║  │ Taille vault        : 289 MB                            │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  🔍 PROBLÈMES DÉTECTÉS:                                      ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ❌ Liens cassés           : 3      (-5 pts)             │ ║
║  │ ⚠️ Notes orphelines       : 12     (-8 pts)             │ ║
║  │ ⚠️ Tags incohérents       : 5      (-4 pts)             │ ║
║  │ ✅ Doublons               : 0      (OK)                 │ ║
║  │ ⚠️ Frontmatter manquant   : 23     (-5 pts)             │ ║
║  │ ℹ️ Attachments orphelins  : 8      (info)               │ ║
║  │ ✅ Notes vides            : 0      (OK)                 │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📈 TENDANCES (30 jours):                                    ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Notes créées        : +45                               │ ║
║  │ Notes modifiées     : 123                               │ ║
║  │ Liens ajoutés       : +234                              │ ║
║  │ Score évolution     : +3 pts                            │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  💡 RECOMMANDATIONS PRIORITAIRES:                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 1. [URGENT] Réparer 3 liens cassés                      │ ║
║  │    → /obs-links fix                                     │ ║
║  │                                                         │ ║
║  │ 2. [IMPORTANT] Connecter 12 notes orphelines            │ ║
║  │    → /obs-links suggest                                 │ ║
║  │                                                         │ ║
║  │ 3. [SUGGÉRÉ] Normaliser 5 tags similaires               │ ║
║  │    → /obs-tags merge                                    │ ║
║  │                                                         │ ║
║  │ 4. [OPTIONNEL] Ajouter frontmatter à 23 notes           │ ║
║  │    → /obs-frontmatter add                               │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-health --quick

Check rapide (30 secondes) :

```
╔══════════════════════════════════════════════════════════════╗
║  🏥 QUICK HEALTH CHECK                                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Score: 78/100  ████████████████░░░░                         ║
║                                                              ║
║  ❌ 3 liens cassés                                           ║
║  ⚠️ 12 notes orphelines                                      ║
║  ✅ Pas de doublons                                          ║
║                                                              ║
║  → /obs-health pour détails complets                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-health --report

Génère un rapport Markdown détaillé :

```powershell
/obs-health --report --output="Health-Report-2026-02-04.md"
```

## Script PowerShell

```powershell
function Get-VaultHealth {
    param(
        [string]$VaultPath = "$env:USERPROFILE\Documents\Knowledge",
        [switch]$Quick,
        [switch]$Report
    )
    
    $StartTime = Get-Date
    $Score = 100
    $Issues = @()
    
    Write-Host "`n🏥 Analyse du vault: $VaultPath`n" -ForegroundColor Cyan
    
    # === STATISTIQUES DE BASE ===
    $Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" -ErrorAction SilentlyContinue
    $Attachments = Get-ChildItem -Path $VaultPath -Recurse -Include "*.png","*.jpg","*.jpeg","*.gif","*.pdf","*.webp" -ErrorAction SilentlyContinue
    
    $Stats = @{
        TotalNotes = $Notes.Count
        TotalAttachments = $Attachments.Count
        TotalSize = ($Notes + $Attachments | Measure-Object -Property Length -Sum).Sum
        TotalWords = 0
        TotalLinks = 0
        TotalTags = @()
    }
    
    # === ANALYSE DES NOTES ===
    $AllLinks = @{}
    $AllBacklinks = @{}
    $BrokenLinks = @()
    $NoteNames = $Notes | ForEach-Object { $_.BaseName }
    
    foreach ($Note in $Notes) {
        $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
        if (!$Content) { continue }
        
        # Compter mots
        $Stats.TotalWords += ($Content -split '\s+').Count
        
        # Extraire liens
        $Links = [regex]::Matches($Content, '\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
        $Stats.TotalLinks += $Links.Count
        
        foreach ($Link in $Links) {
            $Target = $Link.Groups[1].Value
            
            # Vérifier si lien cassé
            if ($Target -notin $NoteNames -and $Target -notmatch '^https?://') {
                $BrokenLinks += [PSCustomObject]@{
                    Source = $Note.Name
                    Target = $Target
                }
            }
            
            # Collecter backlinks
            if (!$AllBacklinks[$Target]) { $AllBacklinks[$Target] = @() }
            $AllBacklinks[$Target] += $Note.BaseName
        }
        
        # Extraire tags
        $Tags = [regex]::Matches($Content, '#[\w/-]+') | ForEach-Object { $_.Value }
        $Stats.TotalTags += $Tags
        
        # Collecter liens sortants
        $AllLinks[$Note.BaseName] = $Links | ForEach-Object { $_.Groups[1].Value }
    }
    
    # === DÉTECTION DES PROBLÈMES ===
    
    # 1. Liens cassés (-5 pts par lien, max -20)
    $BrokenCount = ($BrokenLinks | Select-Object -Unique Source, Target).Count
    if ($BrokenCount -gt 0) {
        $Penalty = [Math]::Min($BrokenCount * 5, 20)
        $Score -= $Penalty
        $Issues += [PSCustomObject]@{
            Type = "ERROR"
            Category = "Liens cassés"
            Count = $BrokenCount
            Penalty = $Penalty
            Fix = "/obs-links fix"
        }
    }
    
    # 2. Notes orphelines (-1 pt par note, max -15)
    $Orphans = $Notes | Where-Object {
        $Name = $_.BaseName
        $HasBacklinks = $AllBacklinks[$Name].Count -gt 0
        $HasOutlinks = $AllLinks[$Name].Count -gt 0
        !$HasBacklinks -and !$HasOutlinks -and $Name -notmatch '^_|^INDEX|^README'
    }
    if ($Orphans.Count -gt 0) {
        $Penalty = [Math]::Min($Orphans.Count, 15)
        $Score -= $Penalty
        $Issues += [PSCustomObject]@{
            Type = "WARNING"
            Category = "Notes orphelines"
            Count = $Orphans.Count
            Penalty = $Penalty
            Fix = "/obs-links suggest"
        }
    }
    
    # 3. Tags similaires/incohérents
    $UniqueTags = $Stats.TotalTags | Select-Object -Unique
    $SimilarTags = @()
    foreach ($Tag in $UniqueTags) {
        $Similar = $UniqueTags | Where-Object { 
            $_ -ne $Tag -and (
                $_.ToLower() -eq $Tag.ToLower() -or
                $_ -replace '-', '' -eq ($Tag -replace '-', '')
            )
        }
        if ($Similar) { $SimilarTags += $Tag }
    }
    if ($SimilarTags.Count -gt 0) {
        $Penalty = [Math]::Min($SimilarTags.Count, 10)
        $Score -= $Penalty
        $Issues += [PSCustomObject]@{
            Type = "WARNING"
            Category = "Tags incohérents"
            Count = $SimilarTags.Count
            Penalty = $Penalty
            Fix = "/obs-tags merge"
        }
    }
    
    # 4. Frontmatter manquant
    $NoFrontmatter = $Notes | Where-Object {
        $Content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
        $Content -and $Content -notmatch '^---\s*\r?\n'
    }
    if ($NoFrontmatter.Count -gt 0 -and $NoFrontmatter.Count -gt ($Notes.Count * 0.1)) {
        $Penalty = [Math]::Min([Math]::Floor($NoFrontmatter.Count / 5), 10)
        $Score -= $Penalty
        $Issues += [PSCustomObject]@{
            Type = "INFO"
            Category = "Frontmatter manquant"
            Count = $NoFrontmatter.Count
            Penalty = $Penalty
            Fix = "/obs-frontmatter add"
        }
    }
    
    # 5. Notes vides
    $EmptyNotes = $Notes | Where-Object {
        $Content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
        !$Content -or $Content.Trim().Length -lt 10
    }
    if ($EmptyNotes.Count -gt 0) {
        $Penalty = [Math]::Min($EmptyNotes.Count * 2, 10)
        $Score -= $Penalty
        $Issues += [PSCustomObject]@{
            Type = "WARNING"
            Category = "Notes vides"
            Count = $EmptyNotes.Count
            Penalty = $Penalty
            Fix = "/obs-empty"
        }
    }
    
    # === AFFICHAGE ===
    $Score = [Math]::Max($Score, 0)
    $BarLength = [Math]::Floor($Score / 2.5)
    $Bar = "█" * $BarLength + "░" * (40 - $BarLength)
    
    $ScoreColor = switch ($Score) {
        { $_ -ge 80 } { "Green" }
        { $_ -ge 60 } { "Yellow" }
        default { "Red" }
    }
    
    Write-Host "  SCORE GLOBAL: $Score/100" -ForegroundColor $ScoreColor
    Write-Host "  $Bar" -ForegroundColor $ScoreColor
    Write-Host ""
    
    Write-Host "  📊 STATISTIQUES:" -ForegroundColor Yellow
    Write-Host "  ┌─────────────────────────────────────────┐"
    Write-Host "  │ Notes totales       : $($Stats.TotalNotes.ToString().PadLeft(6))"
    Write-Host "  │ Mots totaux         : $($Stats.TotalWords.ToString('N0').PadLeft(6))"
    Write-Host "  │ Liens internes      : $($Stats.TotalLinks.ToString().PadLeft(6))"
    Write-Host "  │ Tags uniques        : $(($UniqueTags.Count).ToString().PadLeft(6))"
    Write-Host "  │ Attachments         : $($Stats.TotalAttachments.ToString().PadLeft(6))"
    Write-Host "  │ Taille vault        : $('{0:N1} MB' -f ($Stats.TotalSize / 1MB))"
    Write-Host "  └─────────────────────────────────────────┘"
    Write-Host ""
    
    if ($Issues.Count -gt 0) {
        Write-Host "  🔍 PROBLÈMES DÉTECTÉS:" -ForegroundColor Yellow
        Write-Host "  ┌─────────────────────────────────────────┐"
        foreach ($Issue in $Issues | Sort-Object { $_.Type }) {
            $Icon = switch ($Issue.Type) {
                "ERROR" { "❌" }
                "WARNING" { "⚠️" }
                default { "ℹ️" }
            }
            Write-Host "  │ $Icon $($Issue.Category.PadRight(20)) : $($Issue.Count.ToString().PadLeft(3)) (-$($Issue.Penalty) pts)"
        }
        Write-Host "  └─────────────────────────────────────────┘"
        Write-Host ""
        
        Write-Host "  💡 RECOMMANDATIONS:" -ForegroundColor Yellow
        foreach ($Issue in $Issues | Sort-Object Penalty -Descending | Select-Object -First 3) {
            Write-Host "  → $($Issue.Fix)" -ForegroundColor Cyan
        }
    } else {
        Write-Host "  ✅ Aucun problème détecté !" -ForegroundColor Green
    }
    
    $Duration = (Get-Date) - $StartTime
    Write-Host "`n  ⏱️ Analyse terminée en $($Duration.TotalSeconds.ToString('N1'))s" -ForegroundColor DarkGray
    
    return @{
        Score = $Score
        Stats = $Stats
        Issues = $Issues
        BrokenLinks = $BrokenLinks
        Orphans = $Orphans
    }
}
```

## Options

| Option | Description |
|--------|-------------|
| `--quick` | Analyse rapide (stats de base) |
| `--report` | Générer rapport Markdown |
| `--output=file` | Fichier de sortie pour rapport |
| `--json` | Sortie JSON |
| `--fix` | Proposer corrections automatiques |

## Exemples

```powershell
# Analyse complète
/obs-health

# Check rapide
/obs-health --quick

# Générer rapport
/obs-health --report --output="vault-health.md"

# Analyse d'un vault spécifique
/obs-health --vault="D:\Obsidian\Work"
```
