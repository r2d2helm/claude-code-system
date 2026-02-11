# Commande: /obs-rename

Renommer une note selon les conventions du vault et mettre a jour les backlinks.

## Syntaxe

```
/obs-rename <note> <new-name> [options]
```

## Actions

### Renommer avec mise a jour des backlinks

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$OldName = $args[0]
$NewName = $args[1]

# Trouver la note
$Note = Get-ChildItem -Path $VaultPath -Recurse -Filter "$OldName.md" | Select-Object -First 1
if (-not $Note) { Write-Error "Note '$OldName' non trouvee"; return }

# Renommer le fichier
$NewPath = Join-Path $Note.DirectoryName "$NewName.md"
Rename-Item -Path $Note.FullName -NewName "$NewName.md"

# Mettre a jour tous les backlinks dans le vault
$AllNotes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
$Updated = 0
foreach ($N in $AllNotes) {
    $Content = Get-Content $N.FullName -Raw -ErrorAction SilentlyContinue
    if ($Content -match "\[\[$([regex]::Escape($OldName))") {
        $NewContent = $Content -replace "\[\[$([regex]::Escape($OldName))\]\]", "[[$NewName]]"
        $NewContent = $NewContent -replace "\[\[$([regex]::Escape($OldName))\|", "[[$NewName|"
        [System.IO.File]::WriteAllText($N.FullName, $NewContent,
            [System.Text.UTF8Encoding]::new($false))
        $Updated++
    }
}

Write-Output "Renomme: $OldName -> $NewName ($Updated backlinks mis a jour)"
```

### Conventions de nommage

| Type | Format | Exemple |
|------|--------|---------|
| Concept | `C_Name` | `C_Docker-Compose` |
| Conversation | `YYYY-MM-DD_Conv_Description` | `2026-02-11_Conv_Audit-Skills` |
| Daily | `YYYY-MM-DD` | `2026-02-11` |
| Troubleshooting | `YYYY-MM-DD_Fix_Description` | `2026-02-11_Fix_Path-Guard` |

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Afficher sans renommer |
| `--convention` | Appliquer convention automatiquement |

## Exemples

```powershell
/obs-rename Docker C_Docker                    # Ajouter prefixe concept
/obs-rename old-note 2026-02-11_Conv_Session   # Convention conversation
/obs-rename MyNote C_MyNote --dry-run          # Preview
```

## Voir Aussi

- `/obs-move` - Deplacer une note
- `/obs-frontmatter` - Gerer les metadonnees
