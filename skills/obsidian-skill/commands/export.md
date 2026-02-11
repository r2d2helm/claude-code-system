# Commande: /obs-export

Exporter des notes ou le vault entier dans differents formats.

## Syntaxe

```
/obs-export [format] [source] [options]
```

## Actions

### Export JSON

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" |
    Where-Object { $_.FullName -notmatch '_Templates|\.obsidian|\.git' }

$Data = foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw
    $Frontmatter = @{}
    if ($Content -match '(?s)^---\s*\n(.+?)\n---') {
        # Parser le frontmatter basique
    }
    @{
        name = $Note.BaseName
        path = $Note.FullName.Replace($VaultPath, '').TrimStart('\')
        size = $Note.Length
        modified = $Note.LastWriteTime.ToString('yyyy-MM-dd')
    }
}

$Data | ConvertTo-Json -Depth 3 | Set-Content "vault-export.json"
Write-Output "Exporte: $($Data.Count) notes -> vault-export.json"
```

### Export CSV (metadonnees)

```powershell
$Data | ForEach-Object { [PSCustomObject]$_ } |
    Export-Csv -Path "vault-export.csv" -NoTypeInformation -Encoding UTF8
```

### Export HTML

```powershell
# Convertir une note Markdown en HTML basique
$Note = Get-Content "note.md" -Raw
# Utiliser un module comme PSMarkdown ou conversion manuelle
```

## Options

| Option | Description |
|--------|-------------|
| `json` | Export JSON (metadonnees + contenu) |
| `csv` | Export CSV (metadonnees uniquement) |
| `html` | Export HTML |
| `--output` | Chemin du fichier de sortie |
| `--folder` | Exporter un dossier specifique |

## Exemples

```powershell
/obs-export json                         # Export complet JSON
/obs-export csv --folder Concepts        # CSV des concepts
/obs-export html C_Docker                # Note en HTML
```

## Voir Aussi

- `/obs-sync` - Synchroniser le vault
- `/obs-backup` - Sauvegarder le vault
