# Commande: /obs-tags rename

Renommer un tag dans tout le vault (frontmatter et inline).

## Syntaxe

```
/obs-tags rename <old-tag> <new-tag> [options]
```

## Actions

### Renommer un tag

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$OldTag = $args[0]
$NewTag = $args[1]

$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
$Modified = 0

foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $Content) { continue }
    $NewContent = $Content

    # Remplacer inline tags (#old -> #new)
    $NewContent = $NewContent -replace "(?<=\s|^)#$([regex]::Escape($OldTag))(?=\s|$)", "#$NewTag"

    # Remplacer dans frontmatter tags array
    $NewContent = $NewContent -replace "(?<=^\s*-\s+)$([regex]::Escape($OldTag))(?=\s*$)", $NewTag

    if ($NewContent -ne $Content) {
        [System.IO.File]::WriteAllText($Note.FullName, $NewContent,
            [System.Text.UTF8Encoding]::new($false))
        $Modified++
        Write-Output "Modifie: $($Note.Name)"
    }
}

Write-Output "`n$Modified notes modifiees: #$OldTag -> #$NewTag"
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Afficher sans modifier |
| `--inline-only` | Tags inline uniquement |
| `--frontmatter-only` | Frontmatter uniquement |

## Exemples

```powershell
/obs-tags rename dev/powershell dev/ps       # Raccourcir un tag
/obs-tags rename Proxmox infra/proxmox       # Hierarchiser un tag
/obs-tags rename dev/python dev/py --dry-run # Preview
```

## Voir Aussi

- `/obs-tags merge` - Fusionner des tags
- `/obs-tags list` - Lister tous les tags
