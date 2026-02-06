# Commande: /obs-links

Gérer les liens internes du vault Obsidian.

## Syntaxe

```
/obs-links [action] [options]
```

## Actions

### /obs-links broken

Trouver tous les liens cassés (pointant vers des notes inexistantes) :

```
╔══════════════════════════════════════════════════════════════╗
║                   🔗 LIENS CASSÉS                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Trouvés: 5 liens cassés dans 3 notes                        ║
║                                                              ║
║  📄 Projets/MultiPass/Architecture.md                        ║
║  │                                                           ║
║  ├─ [[API-Design]]                                           ║
║  │  └─ ❌ Note n'existe pas                                  ║
║  │  └─ 💡 Similaire: "API-Documentation" (85%)               ║
║  │                                                           ║
║  └─ [[Database-Schema]]                                      ║
║     └─ ❌ Note n'existe pas                                  ║
║     └─ 💡 Aucune suggestion                                  ║
║                                                              ║
║  📄 Concepts/C_Zettelkasten.md                               ║
║  │                                                           ║
║  └─ [[Luhmann-Biography]]                                    ║
║     └─ ❌ Note n'existe pas                                  ║
║     └─ 💡 Similaire: "R_Luhmann-Bio" (90%)                   ║
║                                                              ║
║  📄 _Daily/2026-02-01.md                                     ║
║  │                                                           ║
║  ├─ [[Meeting-Notes]]                                        ║
║  │  └─ ❌ Note n'existe pas                                  ║
║  │                                                           ║
║  └─ [[Todo-List]]                                            ║
║     └─ ❌ Note n'existe pas                                  ║
║                                                              ║
║  ─────────────────────────────────────────────────────────── ║
║                                                              ║
║  [1] Créer notes manquantes                                  ║
║  [2] Remplacer par suggestions                               ║
║  [3] Supprimer liens cassés                                  ║
║  [4] Exporter liste                                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-links fix

Réparer automatiquement les liens cassés :

```
╔══════════════════════════════════════════════════════════════╗
║                   🔧 RÉPARATION LIENS                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Mode: Interactif                                            ║
║                                                              ║
║  ─────────────────────────────────────────────────────────── ║
║                                                              ║
║  📄 Projets/MultiPass/Architecture.md                        ║
║  Lien cassé: [[API-Design]]                                  ║
║                                                              ║
║  Options:                                                    ║
║  [1] Créer note "API-Design.md"                              ║
║  [2] Remplacer par "API-Documentation" (85% similaire)       ║
║  [3] Supprimer le lien                                       ║
║  [4] Ignorer                                                 ║
║  [5] Ignorer tous similaires                                 ║
║                                                              ║
║  Choix: _                                                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-links unlinked

Notes sans aucun lien (ni entrant ni sortant) :

```
╔══════════════════════════════════════════════════════════════╗
║                   🏝️ NOTES SANS LIENS                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Trouvées: 15 notes non connectées                           ║
║                                                              ║
║  SANS LIENS ENTRANTS (personne ne pointe vers):              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 📄 _Inbox/Note-Rapide-2026-01-15.md                     │ ║
║  │ 📄 Conversations/2026-01-20_Conv_Docker.md              │ ║
║  │ 📄 Code/Python/script-test.md                           │ ║
║  │ 📄 Concepts/C_Microservices.md                          │ ║
║  │ ... (+8 autres)                                         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  SANS LIENS SORTANTS (ne pointe vers rien):                  ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 📄 Références/R_AWS-Documentation.md                    │ ║
║  │ 📄 Code/Bash/backup-script.md                           │ ║
║  │ 📄 Projets/OldProject/Notes.md                          │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Voir suggestions de liens                               ║
║  [2] Exporter liste                                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-links suggest

Suggérer des connexions basées sur le contenu :

```
╔══════════════════════════════════════════════════════════════╗
║                   💡 SUGGESTIONS DE LIENS                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Analyse du contenu pour trouver des connexions...           ║
║                                                              ║
║  📄 Concepts/C_Microservices.md                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Suggestions basées sur les mots-clés:                   │ ║
║  │                                                         │ ║
║  │ → [[C_API-Gateway]]         (mots communs: 5)           │ ║
║  │ → [[C_Docker-Containers]]   (mots communs: 4)           │ ║
║  │ → [[Conv_Architecture]]     (mots communs: 3)           │ ║
║  │                                                         │ ║
║  │ Tags similaires:                                        │ ║
║  │ → [[C_Kubernetes]] (#architecture, #cloud)              │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📄 Code/Python/api-client.md                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ → [[C_REST-API]]            (code similaire)            │ ║
║  │ → [[R_Python-Requests]]     (même langage)              │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Ajouter liens suggérés  [2] Exporter                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-links stats

Statistiques sur les liens du vault :

```
╔══════════════════════════════════════════════════════════════╗
║                   📊 STATISTIQUES LIENS                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  RÉSUMÉ:                                                     ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Liens totaux         : 1,234                            │ ║
║  │ Liens uniques        : 456                              │ ║
║  │ Liens cassés         : 5                                │ ║
║  │ Liens externes       : 89                               │ ║
║  │ Moyenne liens/note   : 2.7                              │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  TOP 10 NOTES LES PLUS LIÉES (backlinks):                    ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 1. INDEX.md                        (45 backlinks)       │ ║
║  │ 2. C_Proxmox-Administration.md     (23 backlinks)       │ ║
║  │ 3. C_PowerShell-Basics.md          (19 backlinks)       │ ║
║  │ 4. Conv_2026-02-03_Setup.md        (15 backlinks)       │ ║
║  │ 5. C_Docker-Basics.md              (12 backlinks)       │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  NOTES HUB (beaucoup de liens sortants):                     ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 1. MOC_Infrastructure.md           (34 liens)           │ ║
║  │ 2. INDEX.md                        (28 liens)           │ ║
║  │ 3. P_MultiPass_Overview.md         (22 liens)           │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Script PowerShell

```powershell
function Find-BrokenLinks {
    param(
        [string]$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
    )
    
    $Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
    $NoteNames = $Notes | ForEach-Object { $_.BaseName }
    $BrokenLinks = @()
    
    foreach ($Note in $Notes) {
        $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
        if (!$Content) { continue }
        
        # Extraire tous les wikilinks
        $Links = [regex]::Matches($Content, '\[\[([^\]|#]+)(?:[|#][^\]]+)?\]\]')
        
        foreach ($Link in $Links) {
            $Target = $Link.Groups[1].Value.Trim()
            
            # Ignorer liens externes
            if ($Target -match '^https?://') { continue }
            
            # Vérifier si la note existe
            if ($Target -notin $NoteNames) {
                # Chercher note similaire
                $Similar = $NoteNames | Where-Object {
                    $_ -like "*$Target*" -or $Target -like "*$_*"
                } | Select-Object -First 1
                
                $BrokenLinks += [PSCustomObject]@{
                    SourceFile = $Note.FullName
                    SourceName = $Note.Name
                    BrokenLink = $Target
                    LineNumber = ($Content.Substring(0, $Link.Index) -split "`n").Count
                    Suggestion = $Similar
                }
            }
        }
    }
    
    return $BrokenLinks
}

function Repair-BrokenLink {
    param(
        [string]$FilePath,
        [string]$OldLink,
        [string]$NewLink,
        [switch]$CreateNote
    )
    
    $Content = Get-Content $FilePath -Raw
    
    if ($CreateNote) {
        # Créer la note manquante
        $VaultPath = Split-Path (Split-Path $FilePath -Parent) -Parent
        $NewNotePath = Join-Path $VaultPath "_Inbox\$NewLink.md"
        
        $Template = @"
---
title: $NewLink
date: $(Get-Date -Format "yyyy-MM-dd")
type: note
tags: []
---

# $NewLink

<!-- Note créée automatiquement -->
"@
        $Template | Out-File $NewNotePath -Encoding UTF8
        Write-Host "✅ Note créée: $NewNotePath"
    }
    else {
        # Remplacer le lien
        $Content = $Content -replace "\[\[$OldLink\]\]", "[[$NewLink]]"
        $Content = $Content -replace "\[\[$OldLink\|", "[[$NewLink|"
        $Content | Out-File $FilePath -Encoding UTF8 -NoNewline
        Write-Host "✅ Lien remplacé: [[$OldLink]] → [[$NewLink]]"
    }
}

function Get-LinkStats {
    param([string]$VaultPath)
    
    $Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
    $LinkCounts = @{}
    $BacklinkCounts = @{}
    $TotalLinks = 0
    $ExternalLinks = 0
    
    foreach ($Note in $Notes) {
        $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
        if (!$Content) { continue }
        
        # Liens sortants
        $Links = [regex]::Matches($Content, '\[\[([^\]|#]+)')
        $LinkCounts[$Note.BaseName] = $Links.Count
        $TotalLinks += $Links.Count
        
        # Compter backlinks
        foreach ($Link in $Links) {
            $Target = $Link.Groups[1].Value
            if (!$BacklinkCounts[$Target]) { $BacklinkCounts[$Target] = 0 }
            $BacklinkCounts[$Target]++
        }
        
        # Liens externes
        $ExternalLinks += ([regex]::Matches($Content, 'https?://[^\s\)\]>]+')).Count
    }
    
    return @{
        TotalLinks = $TotalLinks
        ExternalLinks = $ExternalLinks
        TopLinked = $BacklinkCounts.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 10
        TopLinkers = $LinkCounts.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 10
        Average = [Math]::Round($TotalLinks / $Notes.Count, 1)
    }
}

function Find-SuggestedLinks {
    param(
        [string]$NotePath,
        [string]$VaultPath
    )
    
    $Note = Get-Item $NotePath
    $Content = Get-Content $NotePath -Raw
    $AllNotes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" | 
        Where-Object { $_.FullName -ne $NotePath }
    
    # Extraire mots-clés (mots > 4 caractères, pas communs)
    $StopWords = @("pour", "dans", "avec", "cette", "comme", "plus", "être", "avoir", "faire")
    $Words = [regex]::Matches($Content, '\b[a-zA-ZÀ-ÿ]{5,}\b') | 
        ForEach-Object { $_.Value.ToLower() } |
        Where-Object { $_ -notin $StopWords } |
        Group-Object | Sort-Object Count -Descending |
        Select-Object -First 20 -ExpandProperty Name
    
    # Extraire liens existants
    $ExistingLinks = [regex]::Matches($Content, '\[\[([^\]|]+)') | 
        ForEach-Object { $_.Groups[1].Value }
    
    $Suggestions = @()
    
    foreach ($OtherNote in $AllNotes) {
        if ($OtherNote.BaseName -in $ExistingLinks) { continue }
        
        $OtherContent = Get-Content $OtherNote.FullName -Raw -ErrorAction SilentlyContinue
        if (!$OtherContent) { continue }
        
        # Compter mots communs
        $CommonWords = $Words | Where-Object { $OtherContent -match $_ }
        
        if ($CommonWords.Count -ge 3) {
            $Suggestions += [PSCustomObject]@{
                Note = $OtherNote.BaseName
                Path = $OtherNote.FullName
                CommonWords = $CommonWords.Count
                Keywords = $CommonWords -join ", "
            }
        }
    }
    
    return $Suggestions | Sort-Object CommonWords -Descending | Select-Object -First 5
}
```

## Options

| Option | Description |
|--------|-------------|
| `--auto` | Mode automatique (pas d'interaction) |
| `--dry-run` | Prévisualiser sans modifier |
| `--backup` | Créer backup avant modification |
| `--export=file` | Exporter résultats |
| `--vault=path` | Vault spécifique |

## Exemples

```powershell
# Trouver liens cassés
/obs-links broken

# Réparer automatiquement
/obs-links fix --auto

# Statistiques
/obs-links stats

# Suggestions pour une note
/obs-links suggest --note="C_Microservices.md"

# Exporter liste des liens cassés
/obs-links broken --export="broken-links.csv"
```
