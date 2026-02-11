# Commande: /obs-plugins

Gerer les plugins community Obsidian.

## Syntaxe

```
/obs-plugins [action] [options]
```

## Actions

### Lister les plugins installes

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$PluginsPath = Join-Path $VaultPath ".obsidian\plugins"

$Plugins = Get-ChildItem -Path $PluginsPath -Directory | ForEach-Object {
    $Manifest = Join-Path $_.FullName "manifest.json"
    if (Test-Path $Manifest) {
        $Info = Get-Content $Manifest -Raw | ConvertFrom-Json
        [PSCustomObject]@{
            Nom = $Info.name
            Version = $Info.version
            ID = $Info.id
            Auteur = $Info.author
        }
    }
} | Sort-Object Nom

Write-Output "Plugins installes: $($Plugins.Count)"
$Plugins | Format-Table -AutoSize
```

### Verifier les plugins actifs

```powershell
$CommunityPlugins = Get-Content "$VaultPath\.obsidian\community-plugins.json" -Raw | ConvertFrom-Json
Write-Output "Plugins actifs: $($CommunityPlugins.Count)"
$CommunityPlugins | ForEach-Object { "  - $_" }
```

### Informations sur un plugin

```powershell
$PluginId = $args[0]
$Manifest = Get-Content "$PluginsPath\$PluginId\manifest.json" -Raw | ConvertFrom-Json
$DataFile = Join-Path "$PluginsPath\$PluginId" "data.json"

Write-Output "Plugin: $($Manifest.name) v$($Manifest.version)"
Write-Output "Auteur: $($Manifest.author)"
Write-Output "Description: $($Manifest.description)"
Write-Output "Config: $(if (Test-Path $DataFile) { 'Oui' } else { 'Non' })"
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister les plugins |
| `active` | Plugins actifs uniquement |
| `info <id>` | Details d'un plugin |
| `disable <id>` | Desactiver un plugin |
| `enable <id>` | Activer un plugin |

## Exemples

```powershell
/obs-plugins list                 # Tous les plugins
/obs-plugins active               # Plugins actifs
/obs-plugins info dataview        # Info sur Dataview
```

## Voir Aussi

- `/obs-config` - Configuration Obsidian
- `/obs-hotkeys` - Raccourcis clavier
