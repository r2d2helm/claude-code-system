# Commande: /know-export

Exporter la base de connaissances vers différents formats et outils.

## Syntaxe

```
/know-export [format] [options]
```

## Formats Supportés

### /know-export obsidian

Export optimisé pour Obsidian :

```
╔══════════════════════════════════════════════════════════════╗
║           📤 EXPORT OBSIDIAN                                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📁 CONFIGURATION:                                           ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Source      : C:\Users\r2d2\Documents\Knowledge         │ ║
║  │ Destination : C:\Users\r2d2\Obsidian\SecondBrain        │ ║
║  │ Notes       : 234                                       │ ║
║  │ Attachments : 45                                        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ⚙️ OPTIONS:                                                 ║
║  [x] Convertir liens en [[wikilinks]]                        ║
║  [x] Préserver frontmatter YAML                              ║
║  [x] Créer dossier .obsidian avec config                     ║
║  [x] Générer graph.json pour visualisation                   ║
║  [ ] Inclure fichiers attachés                               ║
║                                                              ║
║  [1] Exporter  [2] Configurer  [3] Prévisualiser             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script PowerShell:**
```powershell
param(
    [string]$SourcePath = "$env:USERPROFILE\Documents\Knowledge",
    [string]$DestPath = "$env:USERPROFILE\Obsidian\SecondBrain",
    [switch]$IncludeAttachments,
    [switch]$CreateConfig
)

# Créer structure Obsidian
$ObsidianConfig = Join-Path $DestPath ".obsidian"
if ($CreateConfig -and !(Test-Path $ObsidianConfig)) {
    New-Item -ItemType Directory -Path $ObsidianConfig -Force | Out-Null
    
    # app.json - Configuration de base
    $AppConfig = @{
        "alwaysUpdateLinks" = $true
        "newFileLocation" = "folder"
        "newFileFolderPath" = "_Inbox"
        "attachmentFolderPath" = "_Attachments"
    } | ConvertTo-Json
    $AppConfig | Out-File (Join-Path $ObsidianConfig "app.json") -Encoding UTF8
    
    # core-plugins.json
    $CorePlugins = @{
        "file-explorer" = $true
        "global-search" = $true
        "graph" = $true
        "backlink" = $true
        "tag-pane" = $true
        "daily-notes" = $true
        "templates" = $true
    } | ConvertTo-Json
    $CorePlugins | Out-File (Join-Path $ObsidianConfig "core-plugins.json") -Encoding UTF8
}

# Copier et convertir fichiers
Get-ChildItem -Path $SourcePath -Recurse -Filter "*.md" | ForEach-Object {
    $RelativePath = $_.FullName.Substring($SourcePath.Length + 1)
    $DestFile = Join-Path $DestPath $RelativePath
    $DestDir = Split-Path $DestFile -Parent
    
    if (!(Test-Path $DestDir)) {
        New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
    }
    
    # Lire et convertir contenu
    $Content = Get-Content $_.FullName -Raw -Encoding UTF8
    
    # Convertir liens Markdown en Wikilinks
    # [Texte](fichier.md) → [[fichier|Texte]]
    $Content = $Content -replace '\[([^\]]+)\]\(([^)]+)\.md\)', '[[$2|$1]]'
    
    # Sauvegarder
    $Content | Out-File -FilePath $DestFile -Encoding UTF8
}

Write-Host "✅ Export Obsidian terminé: $DestPath"
Write-Host "   Notes exportées: $((Get-ChildItem $DestPath -Recurse -Filter '*.md').Count)"
```

### /know-export notion

Export pour import Notion (CSV) :

```
╔══════════════════════════════════════════════════════════════╗
║           📤 EXPORT NOTION                                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Format: CSV compatible Notion Import                        ║
║                                                              ║
║  Colonnes exportées:                                         ║
║  • Title                                                     ║
║  • Date                                                      ║
║  • Type                                                      ║
║  • Tags (multi-select)                                       ║
║  • Content                                                   ║
║  • Related (relations)                                       ║
║                                                              ║
║  Fichier: knowledge-export-2026-02-04.csv                    ║
║  Notes: 234                                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script:**
```powershell
param([string]$SourcePath, [string]$OutputFile = "notion-export.csv")

$Notes = @()

Get-ChildItem -Path $SourcePath -Recurse -Filter "*.md" | ForEach-Object {
    $Content = Get-Content $_.FullName -Raw
    
    # Parser frontmatter
    $Title = if ($Content -match 'title:\s*(.+)') { $Matches[1] } else { $_.BaseName }
    $Date = if ($Content -match 'date:\s*(.+)') { $Matches[1] } else { $_.LastWriteTime.ToString("yyyy-MM-dd") }
    $Type = if ($Content -match 'type:\s*(.+)') { $Matches[1] } else { "note" }
    $Tags = if ($Content -match 'tags:\s*\[([^\]]+)\]') { $Matches[1] -replace '"', '' } else { "" }
    
    # Extraire contenu (sans frontmatter)
    $Body = $Content -replace '(?s)^---.*?---\s*', ''
    
    $Notes += [PSCustomObject]@{
        Title = $Title
        Date = $Date
        Type = $Type
        Tags = $Tags
        Content = $Body.Substring(0, [Math]::Min(1000, $Body.Length))
    }
}

$Notes | Export-Csv -Path $OutputFile -NoTypeInformation -Encoding UTF8
Write-Host "✅ Export Notion: $OutputFile ($($Notes.Count) notes)"
```

### /know-export json

Export JSON complet :

```powershell
/know-export json --output=knowledge-backup.json
```

```json
{
  "exported": "2026-02-04T08:30:00",
  "stats": {
    "total_notes": 234,
    "conversations": 89,
    "concepts": 67,
    "code": 45
  },
  "notes": [
    {
      "id": "20260204-083000",
      "title": "Configuration Super Agent Windows",
      "date": "2026-02-04",
      "type": "conversation",
      "tags": ["windows", "claude-code", "skill"],
      "content": "...",
      "links": ["Concept1", "Concept2"],
      "path": "Conversations/2026-02-04_Conv_Windows-Agent.md"
    }
  ]
}
```

### /know-export html

Générer site statique navigable :

```
╔══════════════════════════════════════════════════════════════╗
║           📤 EXPORT HTML                                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🌐 SITE GÉNÉRÉ:                                             ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ knowledge-site\                                         │ ║
║  │ ├── index.html          # Page d'accueil                │ ║
║  │ ├── search.html         # Recherche                     │ ║
║  │ ├── tags.html           # Index des tags                │ ║
║  │ ├── graph.html          # Visualisation graphe          │ ║
║  │ ├── notes\              # Notes converties              │ ║
║  │ ├── css\                # Styles                        │ ║
║  │ └── js\                 # Scripts (search, graph)       │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Ouvrir: file:///C:/knowledge-site/index.html                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### /know-export backup

Backup complet avec versioning :

```powershell
/know-export backup --dest="D:\Backups\Knowledge"
```

```
╔══════════════════════════════════════════════════════════════╗
║           💾 BACKUP KNOWLEDGE BASE                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📁 Backup créé:                                             ║
║  D:\Backups\Knowledge\2026-02-04_Knowledge-Backup.zip        ║
║                                                              ║
║  📊 Contenu:                                                 ║
║  • 234 notes Markdown                                        ║
║  • 45 fichiers code                                          ║
║  • 12 attachments                                            ║
║  • Taille: 45 MB                                             ║
║                                                              ║
║  🔄 Rotation: 5 derniers backups conservés                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Options

| Option | Description |
|--------|-------------|
| `--dest=path` | Chemin de destination |
| `--include-attachments` | Inclure pièces jointes |
| `--format=md/html/pdf` | Format de sortie |
| `--filter=tag` | Filtrer par tag |
| `--since=date` | Depuis date |
| `--compress` | Compresser en ZIP |

## Exemples

```powershell
# Export Obsidian
/know-export obsidian --dest="C:\Obsidian\Vault"

# Export Notion
/know-export notion --output="notion-import.csv"

# Backup complet
/know-export backup --dest="D:\Backups" --compress

# Export HTML navigable
/know-export html --dest="C:\knowledge-site"

# Export partiel (tag spécifique)
/know-export obsidian --filter="#proxmox"
```
