# Commande: /file-mirror

Creer un miroir exact d'un dossier (copie parfaite, supprime les extras).

## Syntaxe

```
/file-mirror <source> <destination> [options]
```

## Actions

### Preview (dry-run)

```powershell
$Source = $args[0]
$Dest = $args[1]

# Simuler le miroir sans modifier
$Output = robocopy $Source $Dest /MIR /XD ".git" "node_modules" "__pycache__" /L /NFL /NDL /NJH /NJS /FP
$Lines = $Output -split "`n" | Where-Object { $_.Trim() }

# Compter les actions
$New = ($Lines | Where-Object { $_ -match '^\s*New' }).Count
$Extra = ($Lines | Where-Object { $_ -match '^\*EXTRA' }).Count

Write-Output "PREVIEW miroir: $Source -> $Dest"
Write-Output "  Fichiers a copier: $New"
Write-Output "  Fichiers a supprimer (extras): $Extra"
Write-Output ""
Write-Output "Utiliser --confirm pour executer"
```

### Miroir exact

```powershell
$Source = $args[0]
$Dest = $args[1]

if (-not (Test-Path $Dest)) { New-Item -ItemType Directory -Path $Dest -Force | Out-Null }

robocopy $Source $Dest /MIR /XD ".git" "node_modules" "__pycache__" ".venv" /XF "*.tmp" "Thumbs.db" /NFL /NDL /NJH /NJS /R:2 /W:1

Write-Output "Miroir termine: $Source -> $Dest"
```

### Miroir avec exclusions

```powershell
$Source = $args[0]
$Dest = $args[1]
$ExcludeDirs = @(".git", "node_modules", "__pycache__", ".venv", "bin", "obj")
$ExcludeFiles = @("*.tmp", "*.log", "*.bak", "Thumbs.db", "desktop.ini")

$XD = $ExcludeDirs | ForEach-Object { "/XD `"$_`"" }
$XF = $ExcludeFiles | ForEach-Object { "/XF `"$_`"" }

robocopy $Source $Dest /MIR $XD $XF /NFL /NDL /NJH /NJS /R:2 /W:1

Write-Output "Miroir (avec exclusions): $Source -> $Dest"
```

## Options

| Option | Description |
|--------|-------------|
| `--preview` | Simuler sans modifier (dry-run) |
| `--confirm` | Executer le miroir |
| `--exclude` | Patterns supplementaires a exclure |
| `--log` | Ecrire un log dans le dossier destination |

## Exemples

```powershell
/file-mirror C:\Projets D:\Mirror\Projets --preview   # Preview
/file-mirror C:\Projets D:\Mirror\Projets --confirm    # Executer
/file-mirror C:\Data D:\Mirror --exclude "*.log"       # Avec exclusions
```

## Voir Aussi

- `/file-sync` - Synchronisation bidirectionnelle
- `/file-backup` - Sauvegarde avec rotation
