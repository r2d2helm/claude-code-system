# Commande: /obs-tags merge

Fusionner deux tags en un seul dans tout le vault.

## Syntaxe

```
/obs-tags merge <tag1> <tag2> <target> [options]
```

## Actions

### Fusionner

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$Tag1 = $args[0]
$Tag2 = $args[1]
$Target = $args[2]

$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
$Modified = 0

foreach ($Note in $Notes) {
    $Content = Get-Content $Note.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $Content) { continue }
    $NewContent = $Content

    # Remplacer les deux tags par le target
    $NewContent = $NewContent -replace "(?<=\s|^)#$([regex]::Escape($Tag1))(?=\s|$)", "#$Target"
    $NewContent = $NewContent -replace "(?<=\s|^)#$([regex]::Escape($Tag2))(?=\s|$)", "#$Target"

    # Frontmatter
    $NewContent = $NewContent -replace "(?<=^\s*-\s+)$([regex]::Escape($Tag1))(?=\s*$)", $Target
    $NewContent = $NewContent -replace "(?<=^\s*-\s+)$([regex]::Escape($Tag2))(?=\s*$)", $Target

    if ($NewContent -ne $Content) {
        [System.IO.File]::WriteAllText($Note.FullName, $NewContent,
            [System.Text.UTF8Encoding]::new($false))
        $Modified++
    }
}

Write-Output "$Modified notes modifiees: #$Tag1 + #$Tag2 -> #$Target"
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Afficher sans modifier |

## Exemples

```powershell
/obs-tags merge proxmox pve infra/proxmox    # Fusionner variantes
/obs-tags merge ai/gpt ai/openai ai/llm      # Unifier sous un tag
```

## Voir Aussi

- `/obs-tags rename` - Renommer un tag
- `/obs-tags unused` - Tags rares
