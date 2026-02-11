# Commande: /obs-config

Gerer la configuration Obsidian (.obsidian/).

## Syntaxe

```
/obs-config [action] [options]
```

## Actions

### Afficher la configuration

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$ConfigPath = Join-Path $VaultPath ".obsidian"

# Fichiers de config
Get-ChildItem -Path $ConfigPath -Filter "*.json" -File | ForEach-Object {
    [PSCustomObject]@{
        Fichier = $_.Name
        Taille = "$([math]::Round($_.Length / 1KB, 1)) KB"
        Modifie = $_.LastWriteTime.ToString('yyyy-MM-dd')
    }
} | Format-Table -AutoSize
```

### Lire un parametre

```powershell
$AppConfig = Get-Content "$ConfigPath\app.json" -Raw | ConvertFrom-Json
Write-Output "Theme: $($AppConfig.theme)"
Write-Output "Spell check: $($AppConfig.spellcheck)"
```

### Backup de la configuration

```powershell
$BackupPath = "$env:USERPROFILE\Documents\Backups\obsidian-config"
if (-not (Test-Path $BackupPath)) { New-Item -ItemType Directory -Path $BackupPath -Force }

Copy-Item -Path "$ConfigPath\*.json" -Destination $BackupPath -Force
Write-Output "Config sauvegardee dans $BackupPath"
```

## Options

| Option | Description |
|--------|-------------|
| `show` | Afficher la configuration |
| `get <key>` | Lire un parametre |
| `backup` | Sauvegarder la config |
| `restore` | Restaurer depuis backup |

## Exemples

```powershell
/obs-config show              # Liste des fichiers config
/obs-config backup            # Backup de la config
/obs-config restore           # Restaurer la config
```

## Voir Aussi

- `/obs-plugins` - Gerer les plugins
- `/obs-hotkeys` - Gerer les raccourcis
