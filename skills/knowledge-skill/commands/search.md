# Commande: /know-search

Rechercher dans la base de connaissances.

## Syntaxe

```
/know-search "terme" [filtres]
```

## Modes de Recherche

### Recherche Simple

```
/know-search "proxmox"
```

```
╔══════════════════════════════════════════════════════════════╗
║           🔍 RECHERCHE: "proxmox"                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📊 RÉSULTATS: 12 notes trouvées                             ║
║                                                              ║
║  📁 CONVERSATIONS (5)                                        ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 📄 2026-02-03_Conv_Proxmox-Skill-Creation.md           │ ║
║  │    "Création du super agent Proxmox avec 20 commandes"  │ ║
║  │    Tags: #proxmox #skill #claude-code                   │ ║
║  │                                                         │ ║
║  │ 📄 2026-01-28_Conv_Proxmox-Cluster-HA.md               │ ║
║  │    "Configuration haute disponibilité cluster PVE"      │ ║
║  │    Tags: #proxmox #ha #cluster                          │ ║
║  │                                                         │ ║
║  │ ... (+3 autres)                                         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  💡 CONCEPTS (4)                                             ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 📝 C_Proxmox-API-Authentication.md                      │ ║
║  │    "Authentification API Proxmox avec tokens"           │ ║
║  │                                                         │ ║
║  │ 📝 C_Ceph-Integration-Proxmox.md                        │ ║
║  │    "Intégration Ceph dans cluster Proxmox"              │ ║
║  │                                                         │ ║
║  │ ... (+2 autres)                                         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  💻 CODE (3)                                                 ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 🔧 Code_Proxmox-VM-Create.ps1                           │ ║
║  │ 🔧 Code_Proxmox-Backup-Script.sh                        │ ║
║  │ 🔧 Code_Proxmox-API-Call.py                             │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Ouvrir note  [2] Filtrer  [3] Exporter résultats        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Recherche par Tag

```
/know-search tag:#proxmox/cluster
```

```
╔══════════════════════════════════════════════════════════════╗
║           🏷️ RECHERCHE TAG: #proxmox/cluster                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Notes avec ce tag: 8                                        ║
║                                                              ║
║  📄 2026-02-03_Conv_Proxmox-Cluster-Setup.md                 ║
║  📄 2026-01-28_Conv_Proxmox-HA-Config.md                     ║
║  📝 C_Corosync-Configuration.md                              ║
║  📝 C_Cluster-Quorum.md                                      ║
║  📝 C_Live-Migration.md                                      ║
║  🔧 Code_Cluster-Status-Check.sh                             ║
║  🔧 Code_HA-Failover-Test.sh                                 ║
║  📚 R_Proxmox-Cluster-Admin-Guide.md                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Recherche par Type

```
/know-search type:concept
```

Liste tous les concepts atomiques.

### Recherche par Date

```
/know-search date:2026-02
```

Notes de février 2026.

```
/know-search date:last-week
```

Notes de la dernière semaine.

### Recherche Combinée

```
/know-search "backup" tag:#proxmox type:code date:2026
```

```
╔══════════════════════════════════════════════════════════════╗
║           🔍 RECHERCHE AVANCÉE                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Filtres appliqués:                                          ║
║  • Terme: "backup"                                           ║
║  • Tag: #proxmox                                             ║
║  • Type: code                                                ║
║  • Date: 2026                                                ║
║                                                              ║
║  📊 RÉSULTATS: 3 notes                                       ║
║                                                              ║
║  🔧 2026-02-03_Proxmox-Backup-vzdump.sh                      ║
║     Relevance: ████████████████████ 95%                      ║
║                                                              ║
║  🔧 2026-01-15_Backup-PBS-Config.sh                          ║
║     Relevance: ████████████████░░░░ 80%                      ║
║                                                              ║
║  🔧 2026-01-10_Backup-Verification.ps1                       ║
║     Relevance: ██████████████░░░░░░ 70%                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Script PowerShell

```powershell
function Search-Knowledge {
    param(
        [string]$Query,
        [string]$Tag,
        [ValidateSet("all","conversation","concept","code","reference")]
        [string]$Type = "all",
        [string]$DateFilter,
        [string]$KnowledgePath = "$env:USERPROFILE\Documents\Knowledge"
    )
    
    # Construire pattern de recherche
    $SearchPattern = "*"
    if ($Type -ne "all") {
        $TypePrefix = @{
            "conversation" = "Conv_"
            "concept" = "C_"
            "code" = "Code_"
            "reference" = "R_"
        }
        $SearchPattern = "$($TypePrefix[$Type])*"
    }
    
    # Rechercher fichiers
    $Files = Get-ChildItem -Path $KnowledgePath -Recurse -Filter "*.md" |
        Where-Object { $_.Name -like $SearchPattern }
    
    # Filtrer par contenu
    if ($Query) {
        $Files = $Files | Where-Object {
            (Get-Content $_.FullName -Raw) -match $Query
        }
    }
    
    # Filtrer par tag
    if ($Tag) {
        $Files = $Files | Where-Object {
            $Content = Get-Content $_.FullName -Raw
            $Content -match "tags:.*$Tag"
        }
    }
    
    # Filtrer par date
    if ($DateFilter) {
        switch -Regex ($DateFilter) {
            '^\d{4}-\d{2}$' {
                $Files = $Files | Where-Object { $_.Name -match "^$DateFilter" }
            }
            '^last-week$' {
                $WeekAgo = (Get-Date).AddDays(-7)
                $Files = $Files | Where-Object { $_.LastWriteTime -gt $WeekAgo }
            }
            '^last-month$' {
                $MonthAgo = (Get-Date).AddMonths(-1)
                $Files = $Files | Where-Object { $_.LastWriteTime -gt $MonthAgo }
            }
        }
    }
    
    # Afficher résultats
    Write-Host "`n🔍 Résultats: $($Files.Count) notes trouvées`n"
    
    foreach ($File in $Files) {
        $Content = Get-Content $File.FullName -Raw
        
        # Extraire titre du frontmatter
        if ($Content -match 'title:\s*(.+)') {
            $Title = $Matches[1]
        } else {
            $Title = $File.BaseName
        }
        
        # Extraire tags
        if ($Content -match 'tags:\s*\[([^\]]+)\]') {
            $Tags = $Matches[1]
        } else {
            $Tags = ""
        }
        
        # Extraire extrait avec le terme
        $Excerpt = ""
        if ($Query -and $Content -match ".{0,50}$Query.{0,50}") {
            $Excerpt = "...$($Matches[0])..."
        }
        
        Write-Host "📄 $($File.Name)"
        Write-Host "   $Title" -ForegroundColor Cyan
        if ($Excerpt) { Write-Host "   $Excerpt" -ForegroundColor DarkGray }
        if ($Tags) { Write-Host "   Tags: $Tags" -ForegroundColor DarkYellow }
        Write-Host ""
    }
    
    return $Files
}

# Alias
Set-Alias -Name ks -Value Search-Knowledge
```

## Options

| Option | Description |
|--------|-------------|
| `tag:#tag` | Filtrer par tag |
| `type:type` | Filtrer par type (conversation, concept, code) |
| `date:YYYY-MM` | Filtrer par date |
| `date:last-week` | Dernière semaine |
| `date:last-month` | Dernier mois |
| `--in=folder` | Chercher dans dossier spécifique |
| `--limit=N` | Limiter résultats |
| `--export=file` | Exporter résultats |

## Exemples

```powershell
# Recherche simple
/know-search "docker"

# Par tag
/know-search tag:#infra/windows

# Par type
/know-search type:code "backup"

# Dernière semaine
/know-search date:last-week

# Combiné
/know-search "API" tag:#proxmox type:concept

# Exporter résultats
/know-search "PowerShell" --export=results.md
```
