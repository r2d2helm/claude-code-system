# Commande: /file-normalize

Normaliser les noms de fichiers (espaces, accents, caracteres speciaux).

## Syntaxe

```
/file-normalize <chemin> [options]
```

## Actions

### Normaliser les noms

```powershell
$Path = $args[0]
$Files = Get-ChildItem -Path $Path -File
$Modified = 0

foreach ($File in $Files) {
    $NewName = $File.BaseName
    # Remplacer espaces par tirets
    $NewName = $NewName -replace '\s+', '-'
    # Remplacer accents courants
    $NewName = $NewName -creplace '[àâä]', 'a'
    $NewName = $NewName -creplace '[éèêë]', 'e'
    $NewName = $NewName -creplace '[îï]', 'i'
    $NewName = $NewName -creplace '[ôö]', 'o'
    $NewName = $NewName -creplace '[ùûü]', 'u'
    $NewName = $NewName -creplace '[ç]', 'c'
    # Supprimer caracteres speciaux
    $NewName = $NewName -replace '[^\w\-.]', ''
    # Supprimer tirets multiples
    $NewName = $NewName -replace '-{2,}', '-'
    $NewName = $NewName.Trim('-')

    $FullNewName = "$NewName$($File.Extension)"
    if ($FullNewName -ne $File.Name) {
        Rename-Item -Path $File.FullName -NewName $FullNewName
        Write-Output "  $($File.Name) -> $FullNewName"
        $Modified++
    }
}

Write-Output "$Modified fichiers normalises"
```

### Regles de normalisation

| Avant | Apres | Regle |
|-------|-------|-------|
| `Mon Fichier.pdf` | `Mon-Fichier.pdf` | Espaces -> tirets |
| `Résumé été.doc` | `Resume-ete.doc` | Accents supprimes |
| `file@#$.txt` | `file.txt` | Caracteres speciaux supprimes |
| `a--b--c.md` | `a-b-c.md` | Tirets multiples reduits |

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview sans renommer |
| `--recursive` | Inclure sous-dossiers |
| `--rules` | Afficher les regles actives |

## Exemples

```powershell
/file-normalize C:\Users\r2d2\Downloads           # Normaliser
/file-normalize C:\Users\r2d2\Documents --dry-run  # Preview
/file-normalize . --recursive                      # Recursif
```

## Voir Aussi

- `/file-prefix` - Ajouter prefixe date
- `/file-rename` - Renommer selon convention
