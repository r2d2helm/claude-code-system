# Commande: /file-large

Trouver les fichiers les plus volumineux.

## Syntaxe

```
/file-large [chemin] [options]
```

## Comportement

Scanne un dossier et liste les fichiers les plus gros, avec catégorisation par type et suggestions d'action.

## Script PowerShell

```powershell
param(
    [string]$Path = ".",
    [int]$Top = 20,
    [int]$MinSizeMB = 50
)

$Files = Get-ChildItem -Path $Path -File -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt ($MinSizeMB * 1MB) } |
    Sort-Object Length -Descending |
    Select-Object -First $Top

$TotalSize = ($Files | Measure-Object -Property Length -Sum).Sum

Write-Host ""
Write-Host "╔══════════════════════════════════════════════╗"
Write-Host "║     🐘 GROS FICHIERS (> $($MinSizeMB) MB)"
Write-Host "╠══════════════════════════════════════════════╣"
Write-Host "║                                              ║"
Write-Host "║  Trouvés: $($Files.Count) fichiers"
Write-Host "║  Total:   $('{0:N1} GB' -f ($TotalSize / 1GB))"
Write-Host "║                                              ║"

$i = 1
foreach ($File in $Files) {
    $sizeStr = if ($File.Length -gt 1GB) { "$('{0:N1} GB' -f ($File.Length / 1GB))" }
               else { "$('{0:N0} MB' -f ($File.Length / 1MB))" }
    $age = [math]::Round(((Get-Date) - $File.LastWriteTime).TotalDays)
    $ext = $File.Extension.ToUpper()

    Write-Host "║  $($i.ToString().PadLeft(2)). $($sizeStr.PadLeft(8)) | $($ext.PadRight(5)) | $($File.Name)"
    Write-Host "║      📅 $($File.LastWriteTime.ToString('yyyy-MM-dd')) ($age jours) | $($File.DirectoryName.Replace((Resolve-Path $Path).Path, ''))"
    $i++
}

Write-Host "║                                              ║"

# Catégorisation
$byType = $Files | Group-Object Extension | Sort-Object { ($_.Group | Measure-Object Length -Sum).Sum } -Descending
Write-Host "║  PAR TYPE:"
foreach ($t in $byType | Select-Object -First 5) {
    $typeSize = ($t.Group | Measure-Object Length -Sum).Sum
    Write-Host "║    $($t.Name.PadRight(6)) : $($t.Count) fichiers ($('{0:N1} GB' -f ($typeSize / 1GB)))"
}

Write-Host "║                                              ║"
Write-Host "║  Actions possibles:                          ║"
Write-Host "║  1. /file-archive pour les anciens           ║"
Write-Host "║  2. /file-duplicates pour vérifier doublons  ║"
Write-Host "║  3. Supprimer manuellement si obsolètes      ║"
Write-Host "║                                              ║"
Write-Host "╚══════════════════════════════════════════════╝"
```

## Options

| Option | Description |
|--------|-------------|
| `--top=N` | Nombre de fichiers à afficher (défaut: 20) |
| `--min-size=N` | Taille minimum en MB (défaut: 50) |
| `--type=ext` | Filtrer par extension |

## Exemples

```powershell
# Top 20 fichiers > 50 MB
/file-large Documents

# Top 10 fichiers > 100 MB
/file-large C:\Users --top=10 --min-size=100

# Seulement les vidéos
/file-large Downloads --type=.mp4
```
