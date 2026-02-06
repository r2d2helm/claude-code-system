# Wizard: Organisation Photos

Organisation complète de bibliothèque photos.

## Déclenchement

```
/file-wizard photos
```

## Étapes du Wizard (4)

### Étape 1: Analyse Bibliothèque

```
╔══════════════════════════════════════════════════════════════╗
║           📷 WIZARD ORGANISATION PHOTOS                      ║
║                Étape 1/4 : Analyse                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔍 ANALYSE: C:\Users\r2d2\Pictures                          ║
║                                                              ║
║  📊 STATISTIQUES:                                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Photos totales     : 12,345                             │ ║
║  │ Taille totale      : 89.2 GB                            │ ║
║  │ Période            : 2018-2026 (8 ans)                  │ ║
║  │ Formats            : JPG (85%), PNG (10%), RAW (5%)     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📅 DISTRIBUTION PAR ANNÉE:                                  ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 2026 : ████░░░░░░░░░░░░░░░░░░░░░░░░░░ 456 (4%)         │ ║
║  │ 2025 : ██████████████░░░░░░░░░░░░░░░░ 2,345 (19%)      │ ║
║  │ 2024 : ████████████████████░░░░░░░░░░ 3,456 (28%)      │ ║
║  │ 2023 : ██████████████░░░░░░░░░░░░░░░░ 2,234 (18%)      │ ║
║  │ <2023: ████████████████████░░░░░░░░░░ 3,854 (31%)      │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ⚠️ PROBLÈMES DÉTECTÉS:                                      ║
║  • 4,567 photos avec noms génériques (IMG_, DSC_, Photo)     ║
║  • 234 doublons potentiels (2.1 GB)                          ║
║  • 89 captures d'écran mélangées                             ║
║  • Pas de structure par date                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 2: Structure Cible

```
╔══════════════════════════════════════════════════════════════╗
║           📷 WIZARD ORGANISATION PHOTOS                      ║
║               Étape 2/4 : Structure                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📂 STRUCTURE PROPOSÉE:                                      ║
║                                                              ║
║  Pictures\                                                   ║
║  ├── {YYYY}\                    # Par année                  ║
║  │   └── {YYYY-MM}\             # Par mois                   ║
║  │       └── {YYYY-MM-DD}_Description_001.jpg                ║
║  ├── Albums\                    # Albums thématiques         ║
║  │   ├── Vacances-2025-Bretagne\                             ║
║  │   └── Anniversaire-Marie\                                 ║
║  ├── Screenshots\               # Captures d'écran           ║
║  ├── Wallpapers\                # Fonds d'écran              ║
║  └── _Import\                   # Photos à trier             ║
║                                                              ║
║  Format de nommage:                                          ║
║  [x] Date ISO en préfixe (YYYY-MM-DD)                        ║
║  [x] Numéro séquentiel (001, 002...)                         ║
║  [ ] Conserver nom original                                  ║
║  [ ] Ajouter événement/lieu                                  ║
║                                                              ║
║  [1] Appliquer  [2] Modifier  [3] Prévisualiser              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 3: Traitement

```
╔══════════════════════════════════════════════════════════════╗
║           📷 WIZARD ORGANISATION PHOTOS                      ║
║              Étape 3/4 : Traitement                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔄 ORGANISATION EN COURS...                                 ║
║                                                              ║
║  [████████████████████████░░░░░░░░░░░░░░░░] 60%              ║
║  7,407 / 12,345 photos traitées                              ║
║                                                              ║
║  Actions en cours:                                           ║
║  ✓ Création structure année/mois                             ║
║  ✓ Déplacement photos 2018-2023                              ║
║  ✓ Déplacement photos 2024                                   ║
║  ⏳ Déplacement photos 2025-2026                              ║
║  ⏳ Renommage avec date EXIF                                  ║
║  ⏳ Séparation screenshots                                    ║
║                                                              ║
║  Temps estimé restant: 3 minutes                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script organisation photos:**
```powershell
param(
    [string]$SourcePath = "$env:USERPROFILE\Pictures",
    [switch]$UseExifDate
)

# Créer structure
$Years = 2018..2026
foreach ($Year in $Years) {
    1..12 | ForEach-Object {
        $Month = "{0:D2}" -f $_
        $Path = Join-Path $SourcePath "$Year\$Year-$Month"
        if (!(Test-Path $Path)) {
            New-Item -ItemType Directory -Path $Path -Force | Out-Null
        }
    }
}

# Dossiers spéciaux
@("Albums", "Screenshots", "Wallpapers", "_Import") | ForEach-Object {
    $Path = Join-Path $SourcePath $_
    if (!(Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

# Organiser photos par date
Get-ChildItem -Path $SourcePath -File -Recurse | 
    Where-Object { $_.Extension -in @('.jpg','.jpeg','.png','.gif','.webp','.heic') } |
    ForEach-Object {
        # Utiliser date EXIF si disponible, sinon LastWriteTime
        $Date = $_.LastWriteTime
        
        # Séparer screenshots
        if ($_.Name -match 'Screenshot|Screen Shot|Capture') {
            $Dest = Join-Path $SourcePath "Screenshots"
        } else {
            $Year = $Date.ToString("yyyy")
            $YearMonth = $Date.ToString("yyyy-MM")
            $Dest = Join-Path $SourcePath "$Year\$YearMonth"
        }
        
        # Nouveau nom avec date ISO
        $DateStr = $Date.ToString("yyyy-MM-dd")
        $Counter = 1
        do {
            $NewName = "{0}_{1:D3}{2}" -f $DateStr, $Counter, $_.Extension
            $NewPath = Join-Path $Dest $NewName
            $Counter++
        } while (Test-Path $NewPath)
        
        if ($_.DirectoryName -ne $Dest) {
            Move-Item -Path $_.FullName -Destination $NewPath
        }
    }
```

### Étape 4: Résumé

```
╔══════════════════════════════════════════════════════════════╗
║           📷 WIZARD ORGANISATION PHOTOS                      ║
║                Étape 4/4 : Terminé                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🎉 ORGANISATION TERMINÉE!                                   ║
║                                                              ║
║  📊 RÉSUMÉ:                                                  ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Photos organisées    : 12,345                           │ ║
║  │ Photos renommées     : 8,234                            │ ║
║  │ Screenshots séparés  : 89                               │ ║
║  │ Dossiers créés       : 96 (8 ans × 12 mois)             │ ║
║  │ Doublons détectés    : 234 (voir rapport)               │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📁 NOUVELLE STRUCTURE:                                      ║
║  Pictures\                                                   ║
║  ├── 2024\ (3,456 photos)                                    ║
║  ├── 2025\ (2,345 photos)                                    ║
║  ├── 2026\ (456 photos)                                      ║
║  ├── Albums\ (vide - à créer manuellement)                   ║
║  ├── Screenshots\ (89 fichiers)                              ║
║  └── _Import\ (vide)                                         ║
║                                                              ║
║  💡 SUGGESTIONS:                                             ║
║  • Créer des albums dans Albums\ pour événements             ║
║  • Revoir doublons: /file-duplicates "$env:USERPROFILE\Pictures"
║  • Sauvegarder: /file-backup "$env:USERPROFILE\Pictures"     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
