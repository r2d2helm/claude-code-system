# Commande: /obs-templates

Gerer les templates du vault (_Templates/).

## Syntaxe

```
/obs-templates [action] [options]
```

## Actions

### Lister les templates

```powershell
$TemplatePath = "$env:USERPROFILE\Documents\Knowledge\_Templates"
Get-ChildItem -Path $TemplatePath -Filter "*.md" | ForEach-Object {
    $Content = Get-Content $_.FullName -Raw
    $Lines = ($Content -split '\n').Count
    [PSCustomObject]@{
        Template = $_.BaseName
        Lignes = $Lines
    }
} | Format-Table -AutoSize
```

### Valider les templates

```powershell
# Verifier que chaque template a un frontmatter valide
Get-ChildItem -Path $TemplatePath -Filter "*.md" | ForEach-Object {
    $Content = Get-Content $_.FullName -Raw
    $HasFrontmatter = $Content -match '(?s)^---\s*\n.+?\n---'
    [PSCustomObject]@{
        Template = $_.BaseName
        Frontmatter = if ($HasFrontmatter) { "OK" } else { "MANQUANT" }
    }
} | Format-Table -AutoSize
```

### Appliquer un template a une note

```powershell
# Copier un template vers une nouvelle note
$Template = Get-Content "$TemplatePath\Template-Concept.md" -Raw
$NewNote = $Template -replace '\{\{title\}\}', $NoteName
$NewNote = $NewNote -replace '\{\{date\}\}', (Get-Date -Format 'yyyy-MM-dd')
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister les templates disponibles |
| `validate` | Verifier la validite des templates |
| `apply` | Appliquer un template a une note |
| `create` | Creer un nouveau template |

## Exemples

```powershell
/obs-templates list                    # Lister les templates
/obs-templates validate                # Verifier tous les templates
/obs-templates apply Concept MyNote    # Creer note depuis template
```

## Voir Aussi

- `/obs-frontmatter` - Gerer les metadonnees
- `/obs-structure` - Structure du vault
