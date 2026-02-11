# Commande: /obs-hotkeys

Gerer les raccourcis clavier Obsidian.

## Syntaxe

```
/obs-hotkeys [action] [options]
```

## Actions

### Lister les raccourcis personnalises

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$HotkeysFile = "$VaultPath\.obsidian\hotkeys.json"

if (Test-Path $HotkeysFile) {
    $Hotkeys = Get-Content $HotkeysFile -Raw | ConvertFrom-Json
    $Hotkeys.PSObject.Properties | ForEach-Object {
        [PSCustomObject]@{
            Commande = $_.Name
            Raccourci = ($_.Value | ForEach-Object {
                $Parts = @()
                if ($_.modifiers -contains 'Ctrl') { $Parts += 'Ctrl' }
                if ($_.modifiers -contains 'Shift') { $Parts += 'Shift' }
                if ($_.modifiers -contains 'Alt') { $Parts += 'Alt' }
                $Parts += $_.key
                $Parts -join '+'
            }) -join ', '
        }
    } | Format-Table -AutoSize
} else {
    Write-Output "Aucun raccourci personnalise"
}
```

### Raccourcis par defaut utiles

| Raccourci | Action |
|-----------|--------|
| Ctrl+N | Nouvelle note |
| Ctrl+O | Ouvrir note (quick switcher) |
| Ctrl+P | Palette de commandes |
| Ctrl+E | Basculer edition/lecture |
| Ctrl+K | Inserer lien |
| Ctrl+Shift+F | Recherche globale |
| Ctrl+G | Ouvrir le graphe |

### Detecter les conflits

```powershell
# Trouver les raccourcis en double
$Shortcuts = @{}
$Hotkeys.PSObject.Properties | ForEach-Object {
    $Key = ($_.Value | ForEach-Object { $_.key }) -join ','
    if ($Shortcuts.ContainsKey($Key)) {
        Write-Warning "CONFLIT: $Key -> $($Shortcuts[$Key]) vs $($_.Name)"
    }
    $Shortcuts[$Key] = $_.Name
}
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister les raccourcis personnalises |
| `defaults` | Raccourcis par defaut |
| `conflicts` | Detecter les conflits |
| `search <key>` | Chercher un raccourci |

## Exemples

```powershell
/obs-hotkeys list              # Raccourcis personnalises
/obs-hotkeys defaults          # Raccourcis par defaut
/obs-hotkeys conflicts         # Conflits de raccourcis
/obs-hotkeys search Ctrl+G     # Chercher un raccourci
```

## Voir Aussi

- `/obs-config` - Configuration Obsidian
- `/obs-plugins` - Gerer les plugins
