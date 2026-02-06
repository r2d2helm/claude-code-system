# Commande: /obs-tags

Gérer les tags du vault Obsidian.

## Syntaxe

```
/obs-tags [action] [options]
```

## Actions

### /obs-tags list

Lister tous les tags avec statistiques :

```
╔══════════════════════════════════════════════════════════════╗
║                    🏷️ LISTE DES TAGS                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Total: 89 tags uniques dans 456 notes                       ║
║                                                              ║
║  TOP 20 TAGS (par utilisation):                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │  #  Tag                          Notes    Occurrences   │ ║
║  │ ─────────────────────────────────────────────────────── │ ║
║  │  1. #dev                           78          134      │ ║
║  │  2. #infra                         65          112      │ ║
║  │  3. #proxmox                       45           89      │ ║
║  │  4. #powershell                    42           78      │ ║
║  │  5. #dev/python                    38           67      │ ║
║  │  6. #projet                        35           56      │ ║
║  │  7. #todo                          32           45      │ ║
║  │  8. #windows                       28           42      │ ║
║  │  9. #infra/docker                  25           38      │ ║
║  │ 10. #concept                       23           34      │ ║
║  │ ... (+79 autres)                                        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Voir hiérarchie  [2] Exporter  [3] Filtrer              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-tags hierarchy

Afficher la hiérarchie des tags :

```
╔══════════════════════════════════════════════════════════════╗
║                  🌳 HIÉRARCHIE DES TAGS                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  #dev (78 notes)                                             ║
║  ├── #dev/python (38)                                        ║
║  │   ├── #dev/python/flask (12)                              ║
║  │   └── #dev/python/automation (8)                          ║
║  ├── #dev/powershell (42)                                    ║
║  │   ├── #dev/powershell/scripts (15)                        ║
║  │   └── #dev/powershell/modules (7)                         ║
║  ├── #dev/javascript (18)                                    ║
║  └── #dev/api (15)                                           ║
║                                                              ║
║  #infra (65 notes)                                           ║
║  ├── #infra/proxmox (45)                                     ║
║  │   ├── #infra/proxmox/vm (20)                              ║
║  │   ├── #infra/proxmox/cluster (12)                         ║
║  │   └── #infra/proxmox/backup (8)                           ║
║  ├── #infra/docker (25)                                      ║
║  ├── #infra/windows (28)                                     ║
║  └── #infra/network (15)                                     ║
║                                                              ║
║  #projet (35 notes)                                          ║
║  ├── #projet/multipass (18)                                  ║
║  └── #projet/homelab (12)                                    ║
║                                                              ║
║  #status                                                     ║
║  ├── #todo (32)                                              ║
║  ├── #done (28)                                              ║
║  └── #inprogress (15)                                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-tags unused

Tags utilisés une seule fois (potentiellement orphelins) :

```
╔══════════════════════════════════════════════════════════════╗
║                  🗑️ TAGS PEU UTILISÉS                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Tags utilisés 1 seule fois (12):                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ #old-project         → Projets/Archive/OldApp.md        │ ║
║  │ #test123             → _Inbox/Test-Note.md              │ ║
║  │ #temp                → _Inbox/Temp-2026-01.md           │ ║
║  │ #draft-idea          → Concepts/C_Draft.md              │ ║
║  │ #migration           → Projets/Migration-2025.md        │ ║
║  │ ... (+7 autres)                                         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Tags similaires (possibles doublons):                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ #proxmox (45) ↔ #Proxmox (3) ↔ #pve (8)                 │ ║
║  │ #python (38) ↔ #Python (5)                               │ ║
║  │ #todo (32) ↔ #TODO (2) ↔ #to-do (1)                     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Supprimer tags orphelins  [2] Fusionner similaires      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-tags rename

Renommer un tag dans tout le vault :

```powershell
/obs-tags rename "#old-tag" "#new-tag"
```

```
╔══════════════════════════════════════════════════════════════╗
║                  ✏️ RENOMMER TAG                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Ancien: #Proxmox                                            ║
║  Nouveau: #proxmox                                           ║
║                                                              ║
║  Notes affectées: 3                                          ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ • Conversations/2026-01-15_Conv_Setup.md                │ ║
║  │ • Concepts/C_Virtualization.md                          │ ║
║  │ • Projets/Homelab/Config.md                             │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Confirmer le renommage ? [O/N]: _                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-tags merge

Fusionner plusieurs tags en un seul :

```powershell
/obs-tags merge "#Proxmox,#pve,#PVE" --into="#proxmox"
```

```
╔══════════════════════════════════════════════════════════════╗
║                  🔀 FUSIONNER TAGS                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Tags à fusionner:                                           ║
║  • #Proxmox (3 notes)                                        ║
║  • #pve (8 notes)                                            ║
║  • #PVE (2 notes)                                            ║
║                                                              ║
║  → Fusionner vers: #proxmox (45 notes existantes)            ║
║                                                              ║
║  Résultat: #proxmox aura 58 notes                            ║
║                                                              ║
║  Notes modifiées: 13                                         ║
║                                                              ║
║  Confirmer ? [O/N]: _                                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /obs-tags add

Ajouter un tag à plusieurs notes :

```powershell
/obs-tags add "#review" --folder="Conversations" --since="2026-01-01"
```

### /obs-tags remove

Retirer un tag de notes :

```powershell
/obs-tags remove "#temp" --all
```

## Script PowerShell

```powershell
function Get-VaultTags {
    param(
        [string]$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
    )
    
    $Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
    $TagStats = @{}
    $TagNotes = @{}
    
    foreach ($Note in $Notes) {
        $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
        if (!$Content) { continue }
        
        # Extraire tags (format #tag ou #tag/subtag)
        $Tags = [regex]::Matches($Content, '#[\w/-]+') | ForEach-Object { $_.Value }
        
        foreach ($Tag in $Tags) {
            if (!$TagStats[$Tag]) { 
                $TagStats[$Tag] = 0 
                $TagNotes[$Tag] = @()
            }
            $TagStats[$Tag]++
            if ($Note.Name -notin $TagNotes[$Tag]) {
                $TagNotes[$Tag] += $Note.Name
            }
        }
    }
    
    return @{
        Stats = $TagStats.GetEnumerator() | Sort-Object Value -Descending
        Notes = $TagNotes
        Total = $TagStats.Count
    }
}

function Get-TagHierarchy {
    param([hashtable]$TagStats)
    
    $Hierarchy = @{}
    
    foreach ($Tag in $TagStats.Keys) {
        $Parts = $Tag -split '/'
        $Current = $Hierarchy
        
        foreach ($Part in $Parts) {
            if (!$Current[$Part]) {
                $Current[$Part] = @{
                    Count = 0
                    Children = @{}
                }
            }
            $Current = $Current[$Part].Children
        }
    }
    
    return $Hierarchy
}

function Find-SimilarTags {
    param([string[]]$Tags)
    
    $Groups = @{}
    
    foreach ($Tag in $Tags) {
        $Normalized = $Tag.ToLower() -replace '[^a-z0-9]', ''
        
        if (!$Groups[$Normalized]) {
            $Groups[$Normalized] = @()
        }
        $Groups[$Normalized] += $Tag
    }
    
    # Retourner groupes avec plus d'un tag
    return $Groups.GetEnumerator() | 
        Where-Object { $_.Value.Count -gt 1 } |
        ForEach-Object { $_.Value }
}

function Rename-Tag {
    param(
        [string]$VaultPath,
        [string]$OldTag,
        [string]$NewTag,
        [switch]$DryRun
    )
    
    $Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
    $Modified = @()
    
    foreach ($Note in $Notes) {
        $Content = Get-Content $Note.FullName -Raw
        
        if ($Content -match [regex]::Escape($OldTag)) {
            if (!$DryRun) {
                $NewContent = $Content -replace [regex]::Escape($OldTag), $NewTag
                $NewContent | Out-File $Note.FullName -Encoding UTF8 -NoNewline
            }
            $Modified += $Note.Name
        }
    }
    
    return $Modified
}

function Merge-Tags {
    param(
        [string]$VaultPath,
        [string[]]$SourceTags,
        [string]$TargetTag,
        [switch]$DryRun
    )
    
    $TotalModified = @()
    
    foreach ($SourceTag in $SourceTags) {
        if ($SourceTag -eq $TargetTag) { continue }
        
        $Modified = Rename-Tag -VaultPath $VaultPath -OldTag $SourceTag -NewTag $TargetTag -DryRun:$DryRun
        $TotalModified += $Modified
    }
    
    return $TotalModified | Select-Object -Unique
}

function Add-TagToNotes {
    param(
        [string]$VaultPath,
        [string]$Tag,
        [string]$Folder,
        [datetime]$Since
    )
    
    $Path = if ($Folder) { Join-Path $VaultPath $Folder } else { $VaultPath }
    $Notes = Get-ChildItem -Path $Path -Recurse -Filter "*.md"
    
    if ($Since) {
        $Notes = $Notes | Where-Object { $_.LastWriteTime -ge $Since }
    }
    
    foreach ($Note in $Notes) {
        $Content = Get-Content $Note.FullName -Raw
        
        # Vérifier si tag déjà présent
        if ($Content -match [regex]::Escape($Tag)) { continue }
        
        # Ajouter dans frontmatter ou à la fin
        if ($Content -match '^---\s*\r?\n([\s\S]*?)\r?\n---') {
            $Frontmatter = $Matches[1]
            if ($Frontmatter -match 'tags:\s*\[([^\]]*)\]') {
                $ExistingTags = $Matches[1]
                $NewTags = "$ExistingTags, $Tag"
                $Content = $Content -replace "tags:\s*\[[^\]]*\]", "tags: [$NewTags]"
            }
        } else {
            # Ajouter à la fin du premier paragraphe
            $Content = $Content -replace '(\r?\n\r?\n)', "`n$Tag`$1"
        }
        
        $Content | Out-File $Note.FullName -Encoding UTF8 -NoNewline
    }
}
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Prévisualiser sans modifier |
| `--backup` | Backup avant modification |
| `--folder=path` | Limiter à un dossier |
| `--since=date` | Notes depuis date |
| `--export=file` | Exporter résultats |

## Exemples

```powershell
# Lister tous les tags
/obs-tags list

# Voir hiérarchie
/obs-tags hierarchy

# Renommer tag
/obs-tags rename "#old" "#new"

# Fusionner tags similaires
/obs-tags merge "#Proxmox,#pve" --into="#proxmox"

# Ajouter tag aux notes récentes
/obs-tags add "#review" --since="2026-02-01"

# Exporter liste des tags
/obs-tags list --export="tags.csv"
```
