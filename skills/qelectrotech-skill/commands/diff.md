# Comparer deux versions d'un projet QET

Compare deux fichiers .qet pour identifier les differences.

## Modes de comparaison

| Mode | Description |
|------|-------------|
| `summary` | Resume des differences (ajouts, suppressions, modifications) |
| `detailed` | Detail element par element et conducteur par conducteur |
| `folios` | Comparaison folio par folio uniquement |

## Aspects compares

### 1. Folios

- Folios ajoutes / supprimes
- Folios renommes (meme order, titre different)
- Folios reordonnes

### 2. Elements

- Elements ajoutes (nouveaux dans version B)
- Elements supprimes (absents dans version B)
- Elements modifies :
  - Position (x, y) changee
  - Label modifie
  - Informations (manufacturer, designation...) modifiees

### 3. Conducteurs

- Conducteurs ajoutes / supprimes
- Numerotation modifiee
- Attributs modifies (section, couleur, cable)

### 4. Collection

- Elements ajoutes a la collection
- Elements supprimes de la collection
- Definitions modifiees (version, graphisme)

### 5. Proprietes

- Variables projet modifiees (author, plant, indexrev...)
- Configuration auto-numerotation modifiee
- Configuration cross-references modifiee

## Format de sortie

```
# Comparaison : v1.qet ↔ v2.qet

## Resume
- Folios : +1 ajoute, -0 supprime, 2 modifies
- Elements : +12 ajoutes, -3 supprimes, 8 modifies
- Conducteurs : +15 ajoutes, -2 supprimes, 5 modifies
- Collection : +5 elements, -1 element
- Properties : 2 modifiees

## Folios modifies
| Folio | Modification |
|-------|-------------|
| F3 "Cuisine" | +4 elements, +6 conducteurs |
| F5 "Exterieur" | Renomme ("Jardin" → "Exterieur") |
| F9 "Borniers" | Nouveau folio |

## Elements ajoutes (12)
| Folio | Type | Label | Position |
|-------|------|-------|----------|
| F3 | pc1.elmt | PC12 | (420,320) |
...

## Elements supprimes (3)
...

## Elements modifies (8)
| Folio | Label | Champ | Avant | Apres |
|-------|-------|-------|-------|-------|
| F1 | K1 | manufacturer | "" | "Schneider" |
...
```

## Actions PowerShell

### Comparaison basique

```powershell
[xml]$v1 = [System.IO.File]::ReadAllText($path1)
[xml]$v2 = [System.IO.File]::ReadAllText($path2)

$folios1 = $v1.project.SelectNodes('diagram')
$folios2 = $v2.project.SelectNodes('diagram')

Write-Host "Folios: $($folios1.Count) → $($folios2.Count)"
Write-Host "Elements: $($v1.SelectNodes('//element').Count) → $($v2.SelectNodes('//element').Count)"
Write-Host "Conducteurs: $($v1.SelectNodes('//conductor').Count) → $($v2.SelectNodes('//conductor').Count)"
```

## Exemple

```
/qet-diff "projet_v1.qet" "projet_v2.qet"
/qet-diff "projet_v1.qet" "projet_v2.qet" --mode detailed
/qet-diff "projet_v1.qet" "projet_v2.qet" --mode folios
```

$ARGUMENTS
