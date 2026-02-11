# Commande: /obs-duplicates

Detecter les notes avec contenu similaire ou identique.

## Syntaxe

```
/obs-duplicates [options]
```

## Actions

### Detecter les doublons exacts (hash)

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" |
    Where-Object { $_.FullName -notmatch '_Templates|\.obsidian' }

$Hashes = @{}
foreach ($Note in $Notes) {
    $Hash = (Get-FileHash $Note.FullName -Algorithm MD5).Hash
    if ($Hashes.ContainsKey($Hash)) {
        Write-Output "DOUBLON EXACT:"
        Write-Output "  - $($Hashes[$Hash])"
        Write-Output "  - $($Note.FullName)"
    } else {
        $Hashes[$Hash] = $Note.FullName
    }
}
```

### Detecter les titres similaires

```powershell
$NoteNames = $Notes | ForEach-Object { $_.BaseName }
$Similar = @()
for ($i = 0; $i -lt $NoteNames.Count; $i++) {
    for ($j = $i + 1; $j -lt $NoteNames.Count; $j++) {
        $Name1 = $NoteNames[$i].ToLower() -replace '[_-]', ' '
        $Name2 = $NoteNames[$j].ToLower() -replace '[_-]', ' '
        if ($Name1 -eq $Name2 -or $Name1 -like "*$Name2*" -or $Name2 -like "*$Name1*") {
            Write-Output "TITRE SIMILAIRE: $($NoteNames[$i]) <-> $($NoteNames[$j])"
        }
    }
}
```

## Options

| Option | Description |
|--------|-------------|
| `--exact` | Doublons exacts uniquement (hash) |
| `--title` | Titres similaires |
| `--tags` | Notes avec memes tags |
| `--merge` | Proposer de fusionner |

## Exemples

```powershell
/obs-duplicates                # Detection complete
/obs-duplicates --exact        # Hash uniquement
/obs-duplicates --title        # Titres similaires
```

## Voir Aussi

- `/obs-clean` - Nettoyage general
- `/obs-empty` - Notes vides
