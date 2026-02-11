# Commande: /obs-wizard audit

Wizard d'audit complet du vault en 6 etapes guidees.

## Syntaxe

```
/obs-wizard audit [options]
```

## Etapes du Wizard

### Etape 1 : Inventaire

```powershell
$VaultPath = "$env:USERPROFILE\Documents\Knowledge"
$Notes = Get-ChildItem -Path $VaultPath -Recurse -Filter "*.md" |
    Where-Object { $_.FullName -notmatch '_Templates|\.obsidian|\.git' }

Write-Output "=== INVENTAIRE ==="
Write-Output "Notes: $($Notes.Count)"
Write-Output "Par dossier:"
$Notes | Group-Object { Split-Path (Split-Path $_.FullName) -Leaf } |
    Sort-Object Count -Descending | ForEach-Object { "  $($_.Name): $($_.Count)" }
```

### Etape 2 : Liens

```powershell
# Liens casses et orphelins (voir /obs-links broken + /obs-orphans)
```

### Etape 3 : Tags

```powershell
# Tags incohérents, doublons, rares (voir /obs-tags list + /obs-tags unused)
```

### Etape 4 : Frontmatter

```powershell
# Notes sans frontmatter ou frontmatter incomplet (voir /obs-frontmatter validate)
$Missing = $Notes | Where-Object {
    $Content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    $Content -notmatch '(?s)^---\s*\n'
}
Write-Output "Sans frontmatter: $($Missing.Count)"
```

### Etape 5 : Qualite

```powershell
# Notes vides, doublons, attachments orphelins
# (voir /obs-empty, /obs-duplicates, /obs-attachments orphans)
```

### Etape 6 : Score et recommandations

```
Score Global: XX/100
- Liens: XX/20
- Connectivite: XX/20
- Tags: XX/15
- Frontmatter: XX/15
- Doublons: XX/10
- Structure: XX/10
- Attachments: XX/10

Recommandations:
1. ...
2. ...
3. ...
```

## Options

| Option | Description |
|--------|-------------|
| `--quick` | Audit rapide (etapes 1+2+6) |
| `--full` | Audit complet (6 etapes) |
| `--fix` | Corriger automatiquement les problemes simples |

## Exemples

```powershell
/obs-wizard audit               # Audit complet
/obs-wizard audit --quick       # Audit rapide
/obs-wizard audit --fix         # Audit + corrections
```

## Voir Aussi

- `/obs-health` - Diagnostic rapide
- `/obs-wizard cleanup` - Nettoyage guide
- `/guardian-health` - Health check vault-guardian
