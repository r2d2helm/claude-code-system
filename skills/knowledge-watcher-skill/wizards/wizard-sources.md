# Wizard: /kwatch-wizard sources

Gérer les sources de données du Knowledge Watcher.

## Description

Ce wizard permet d'ajouter, modifier ou supprimer des sources de données surveillées par le Knowledge Watcher.

## Menu Principal

```
╔══════════════════════════════════════════════════════════════╗
║         📂 GESTION DES SOURCES                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Sources actuelles:                                          ║
║                                                              ║
║  TIER 1 (Real-time):                                         ║
║  │ 1. ✅ Claude History       ~/.claude/history.jsonl        ║
║  │ 2. ✅ Projets Actifs       ~/Projets                      ║
║  │ 3. ✅ Knowledge Vault      ~/Documents/Knowledge          ║
║                                                              ║
║  TIER 2 (Hourly):                                            ║
║  │ 4. ✅ Downloads            ~/Downloads                    ║
║  │ 5. ❌ Formations           ~/Documents/Formations         ║
║                                                              ║
║  TIER 3 (Daily):                                             ║
║  │ 6. ❌ Browser Bookmarks    Chrome/Edge                    ║
║  │ 7. ✅ PowerShell Scripts   ~/Documents/WindowsPowerShell  ║
║                                                              ║
║  TIER 4 (Weekly):                                            ║
║  │ 8. ❌ Archives             ~/Documents/Archives           ║
║  │ 9. ❌ Resources            ~/Documents/Resources          ║
║                                                              ║
║  [A] Ajouter une source                                      ║
║  [E] Éditer une source (numéro)                              ║
║  [T] Toggle activer/désactiver (numéro)                      ║
║  [D] Supprimer une source (numéro)                           ║
║  [Q] Quitter                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Lister les sources

```powershell
$SkillPath = "$env:USERPROFILE\.claude\skills\knowledge-watcher-skill"
Import-Module "$SkillPath\scripts\KnowledgeWatcher.psm1" -Force

$sources = Get-KWSources
$sources | Format-Table id, name, tier, enabled, path -AutoSize
```

## Ajouter une source

Pour ajouter une nouvelle source, éditer `sources.json`:

```json
{
  "id": "my-new-source",
  "name": "Ma Nouvelle Source",
  "tier": 2,
  "type": "directory",
  "enabled": true,
  "path": "C:\\Users\\r2d2\\MyFolder",
  "patterns": ["*.md", "*.txt"],
  "recursive": true,
  "processor": "GenericFileSource"
}
```

**Paramètres:**
| Paramètre | Description | Requis |
|-----------|-------------|--------|
| `id` | Identifiant unique | Oui |
| `name` | Nom affiché | Oui |
| `tier` | 1 (real-time) à 4 (weekly) | Oui |
| `type` | directory, claude-history, browser-bookmarks | Oui |
| `enabled` | Activer/désactiver | Oui |
| `path` | Chemin du dossier | Pour directory |
| `patterns` | Patterns de fichiers | Non |
| `recursive` | Scanner les sous-dossiers | Non |
| `processor` | GenericFileSource, ClaudeHistorySource, etc. | Oui |
| `excludePaths` | Dossiers à exclure | Non |

## Activer/Désactiver une source

```powershell
$SkillPath = "$env:USERPROFILE\.claude\skills\knowledge-watcher-skill"
$sourcesFile = "$SkillPath\config\sources.json"

$config = Get-Content $sourcesFile | ConvertFrom-Json

# Toggle une source par id
$sourceId = "downloads"
$source = $config.sources | Where-Object { $_.id -eq $sourceId }
$source.enabled = -not $source.enabled

$config | ConvertTo-Json -Depth 10 | Set-Content $sourcesFile
Write-Host "Source '$sourceId' is now: $(if ($source.enabled) { 'ENABLED' } else { 'DISABLED' })"
```

## Types de sources supportés

### 1. Directory (dossier)
```json
{
  "type": "directory",
  "path": "C:\\Path\\To\\Folder",
  "patterns": ["*.md", "*.txt"],
  "recursive": true
}
```

### 2. Claude History
```json
{
  "type": "claude-history",
  "path": "C:\\Users\\r2d2\\.claude\\history.jsonl"
}
```

### 3. Browser Bookmarks
```json
{
  "type": "browser-bookmarks",
  "browsers": ["chrome", "edge", "firefox"]
}
```

## Tiers expliqués

| Tier | Mode | Fréquence | Usage recommandé |
|------|------|-----------|------------------|
| 1 | Real-time | Instantané | Sources actives (projets, conversations) |
| 2 | Batch | Toutes les heures | Sources fréquentes (downloads) |
| 3 | Batch | Quotidien 6h | Sources moins actives (bookmarks) |
| 4 | Batch | Hebdo dim 3h | Archives, ressources |

## Bonnes pratiques

1. **Éviter les doublons**: Ne pas surveiller le vault Obsidian en Tier 1 si vous y écrivez les notes
2. **Patterns précis**: Utilisez des patterns spécifiques pour éviter de capturer des fichiers inutiles
3. **Exclusions**: Excluez `.git`, `node_modules`, fichiers temporaires
4. **Tier approprié**: Mettez les sources actives en Tier 1, les archives en Tier 4

## Après modification

Redémarrer les watchers pour appliquer les changements:

```
/kwatch-stop
/kwatch-start
```
