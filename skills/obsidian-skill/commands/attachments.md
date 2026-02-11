# Commande: /obs-attachments

Gerer les pieces jointes du vault (images, PDF, fichiers).

## Syntaxe

```
/obs-attachments [action] [options]
```

## Actions

### Lister les attachments

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$Attachments = Get-ChildItem -Path $VaultPath -Recurse -Include "*.png","*.jpg","*.jpeg","*.gif","*.webp","*.pdf","*.svg" |
    Where-Object { $_.FullName -notmatch '\.obsidian' }

$ByType = $Attachments | Group-Object Extension | Sort-Object Count -Descending
$TotalSize = ($Attachments | Measure-Object -Property Length -Sum).Sum / 1MB

Write-Output "Total: $($Attachments.Count) fichiers ($([math]::Round($TotalSize, 1)) MB)"
$ByType | ForEach-Object { "  $($_.Name): $($_.Count) fichiers" }
```

### Trouver les attachments orphelins

```powershell
# Fichiers non references dans aucune note
$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md"
$AllContent = ($Notes | ForEach-Object { Get-Content $_.FullName -Raw }) -join "`n"

$Orphans = $Attachments | Where-Object {
    $AllContent -notmatch [regex]::Escape($_.Name)
}

Write-Output "`nAttachments orphelins: $($Orphans.Count)"
$Orphans | ForEach-Object {
    "  - $($_.Name) ($([math]::Round($_.Length / 1KB, 1)) KB)"
}
```

### Nettoyer les orphelins

```powershell
$Orphans | ForEach-Object {
    Write-Output "Supprime: $($_.Name)"
    Remove-Item $_.FullName -WhatIf  # -WhatIf pour dry-run
}
```

## Options

| Option | Description |
|--------|-------------|
| `list` | Lister tous les attachments |
| `orphans` | Trouver les non-references |
| `clean` | Supprimer les orphelins |
| `large` | Fichiers > 5 MB |
| `--dry-run` | Preview sans action |

## Exemples

```powershell
/obs-attachments list              # Inventaire complet
/obs-attachments orphans           # Non-references
/obs-attachments clean --dry-run   # Preview nettoyage
/obs-attachments large             # Gros fichiers
```

## Voir Aussi

- `/obs-clean` - Nettoyage general
- `/obs-stats` - Statistiques du vault
