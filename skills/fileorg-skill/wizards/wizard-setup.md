# Wizard: Setup Initial Organisation

Configuration complète du système d'organisation de fichiers.

## Déclenchement

```
/file-wizard setup
```

## Étapes du Wizard (6)

### Étape 1: Analyse État Actuel

```
╔══════════════════════════════════════════════════════════════╗
║           📁 WIZARD ORGANISATION FICHIERS                    ║
║               Étape 1/6 : Analyse                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔍 ANALYSE DE VOTRE SYSTÈME...                              ║
║                                                              ║
║  📊 ÉTAT ACTUEL:                                             ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Documents   : 4,567 fichiers │ 45.6 GB │ Score: 45/100  │ ║
║  │ Pictures    : 12,345 fichiers│ 89.2 GB │ Score: 62/100  │ ║
║  │ Downloads   : 892 fichiers   │ 23.4 GB │ Score: 28/100  │ ║
║  │ Desktop     : 156 fichiers   │ 2.3 GB  │ Score: 35/100  │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ⚠️ PROBLÈMES DÉTECTÉS:                                      ║
║  • 1,234 fichiers sans date ISO (27%)                        ║
║  • 567 fichiers avec espaces/caractères spéciaux             ║
║  • 234 doublons potentiels (4.5 GB)                          ║
║  • 89 dossiers vides                                         ║
║  • Desktop encombré (156 fichiers)                           ║
║                                                              ║
║  Score global: 42/100 ████████░░░░░░░░░░░░░░                 ║
║                                                              ║
║  [1] Continuer avec configuration  [2] Rapport détaillé      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 2: Choix du Profil

```
╔══════════════════════════════════════════════════════════════╗
║           📁 WIZARD ORGANISATION FICHIERS                    ║
║                Étape 2/6 : Profil                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Quel profil correspond le mieux à votre usage ?             ║
║                                                              ║
║  [1] 👤 PERSONNEL                                            ║
║      Documents administratifs, photos, médias                ║
║      Structure: Administratif, Projets, Personnel            ║
║                                                              ║
║  [2] 💼 PROFESSIONNEL                                        ║
║      Travail, clients, projets d'entreprise                  ║
║      Structure: Clients, Projets, Admin, Resources           ║
║                                                              ║
║  [3] 💻 DÉVELOPPEUR                                          ║
║      Code, projets dev, documentation technique              ║
║      Structure: Projects, Code, Docs, Tools                  ║
║                                                              ║
║  [4] 🎨 CRÉATIF                                              ║
║      Design, médias, portfolio                               ║
║      Structure: Clients, Portfolio, Assets, Archive          ║
║                                                              ║
║  [5] 🔧 PERSONNALISÉ                                         ║
║      Créer votre propre structure                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 3: Structure des Dossiers

```
╔══════════════════════════════════════════════════════════════╗
║           📁 WIZARD ORGANISATION FICHIERS                    ║
║              Étape 3/6 : Structure                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📂 STRUCTURE PROPOSÉE (Profil: Personnel):                  ║
║                                                              ║
║  Documents\                                                  ║
║  ├── _INBOX\              # Fichiers à trier                 ║
║  ├── _ARCHIVE\            # Anciens fichiers par année       ║
║  │   └── {YYYY}\                                             ║
║  ├── Administratif\                                          ║
║  │   ├── Banque\                                             ║
║  │   ├── Impots\                                             ║
║  │   ├── Assurances\                                         ║
║  │   └── Factures\                                           ║
║  ├── Projets\                                                ║
║  │   └── {NomProjet}\                                        ║
║  ├── Travail\                                                ║
║  └── Personnel\                                              ║
║                                                              ║
║  [x] Créer dossier _INBOX pour nouveaux fichiers             ║
║  [x] Créer structure _ARCHIVE par année                      ║
║  [ ] Migrer fichiers existants automatiquement               ║
║                                                              ║
║  [1] Appliquer  [2] Modifier  [3] Prévisualiser              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script création structure:**
```powershell
$BasePath = "$env:USERPROFILE\Documents"

$Structure = @(
    "_INBOX",
    "_ARCHIVE\2024",
    "_ARCHIVE\2025",
    "_ARCHIVE\2026",
    "Administratif\Banque",
    "Administratif\Impots",
    "Administratif\Assurances",
    "Administratif\Factures",
    "Projets",
    "Travail",
    "Personnel"
)

foreach ($Folder in $Structure) {
    $Path = Join-Path $BasePath $Folder
    if (!(Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "✓ Créé: $Folder"
    }
}
```

### Étape 4: Convention de Nommage

```
╔══════════════════════════════════════════════════════════════╗
║           📁 WIZARD ORGANISATION FICHIERS                    ║
║              Étape 4/6 : Nommage                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📝 CONVENTION DE NOMMAGE:                                   ║
║                                                              ║
║  Format standard:                                            ║
║  {DATE}_{CATEGORIE}_{DESCRIPTION}_{VERSION}.{EXT}            ║
║                                                              ║
║  Exemples:                                                   ║
║  2026-02-03_Facture_EDF-Janvier_v01.pdf                      ║
║  2026-02-03_Photo_Vacances-Bretagne_001.jpg                  ║
║                                                              ║
║  Règles:                                                     ║
║  [x] Date ISO en préfixe (YYYY-MM-DD)                        ║
║  [x] Underscores entre éléments                              ║
║  [x] Tirets entre mots                                       ║
║  [x] Pas d'espaces ni accents                                ║
║  [x] Versions avec zéros (v01, v02)                          ║
║  [x] Maximum 50 caractères                                   ║
║                                                              ║
║  Appliquer aux fichiers existants ?                          ║
║  [1] Oui, renommer maintenant                                ║
║  [2] Non, appliquer seulement aux nouveaux                   ║
║  [3] Prévisualiser les changements                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 5: Nettoyage Initial

```
╔══════════════════════════════════════════════════════════════╗
║           📁 WIZARD ORGANISATION FICHIERS                    ║
║              Étape 5/6 : Nettoyage                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🧹 NETTOYAGE INITIAL:                                       ║
║                                                              ║
║  Actions recommandées:                                       ║
║                                                              ║
║  [x] Supprimer 89 dossiers vides                             ║
║  [x] Nettoyer fichiers temporaires (2.3 GB)                  ║
║  [x] Organiser Downloads par type                            ║
║  [x] Déplacer fichiers Desktop vers _INBOX                   ║
║                                                              ║
║  Actions optionnelles:                                       ║
║  [ ] Supprimer doublons (234 fichiers, 4.5 GB)               ║
║      ⚠️ Vérification manuelle recommandée                    ║
║  [ ] Archiver fichiers > 1 an                                ║
║  [ ] Vider corbeille (1.2 GB)                                ║
║                                                              ║
║  Espace à libérer: ~8 GB                                     ║
║                                                              ║
║  [1] Exécuter nettoyage  [2] Passer  [3] Détails             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 6: Automatisation

```
╔══════════════════════════════════════════════════════════════╗
║           📁 WIZARD ORGANISATION FICHIERS                    ║
║             Étape 6/6 : Automatisation                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ⚙️ CONFIGURATION AUTOMATISATION:                            ║
║                                                              ║
║  Tâches planifiées:                                          ║
║                                                              ║
║  [x] Organiser Downloads automatiquement                     ║
║      Fréquence: Quotidien à 20:00                            ║
║                                                              ║
║  [x] Nettoyer fichiers temporaires                           ║
║      Fréquence: Hebdomadaire (Dimanche 03:00)                ║
║                                                              ║
║  [ ] Scanner doublons                                        ║
║      Fréquence: Mensuel (1er du mois)                        ║
║                                                              ║
║  [ ] Archiver fichiers anciens                               ║
║      Fréquence: Mensuel (fichiers > 1 an)                    ║
║                                                              ║
║  [ ] Rapport d'organisation par email                        ║
║      Fréquence: Hebdomadaire                                 ║
║                                                              ║
║  [1] Configurer  [2] Passer  [3] Manuel uniquement           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Finalisation

```
╔══════════════════════════════════════════════════════════════╗
║           📁 WIZARD ORGANISATION FICHIERS                    ║
║                   ✅ TERMINÉ                                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🎉 CONFIGURATION TERMINÉE!                                  ║
║                                                              ║
║  Résumé des actions:                                         ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✓ Structure créée (15 dossiers)                         │ ║
║  │ ✓ Convention de nommage définie                         │ ║
║  │ ✓ 89 dossiers vides supprimés                           │ ║
║  │ ✓ 2.3 GB de fichiers temp nettoyés                      │ ║
║  │ ✓ Downloads organisé par type                           │ ║
║  │ ✓ 2 tâches planifiées créées                            │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📊 NOUVEAU SCORE: 78/100 (+36 pts!)                         ║
║  ████████████████████████████████░░░░░░░░                    ║
║                                                              ║
║  📄 README créé: Documents\README-Organisation.md            ║
║                                                              ║
║  Prochaines étapes suggérées:                                ║
║  • Trier les fichiers dans _INBOX                            ║
║  • Revoir les doublons détectés                              ║
║  • Renommer photos avec /file-rename iso-date                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Script README généré:**
```powershell
$ReadmeContent = @"
# 📁 Organisation des Fichiers

## Structure
- **_INBOX**: Fichiers à trier
- **_ARCHIVE**: Anciens fichiers par année
- **Administratif**: Documents officiels
- **Projets**: Projets en cours
- **Travail**: Documents professionnels
- **Personnel**: Documents privés

## Convention de Nommage
Format: `{DATE}_{CATEGORIE}_{DESCRIPTION}_{VERSION}.{EXT}`
Exemple: `2026-02-03_Facture_EDF-Janvier_v01.pdf`

### Règles
- Date ISO: YYYY-MM-DD
- Pas d'espaces (utiliser - ou _)
- Pas d'accents ni caractères spéciaux
- Versions: v01, v02, v03...

## Automatisation
- Downloads organisé: Quotidien 20:00
- Nettoyage temp: Dimanche 03:00

## Commandes Utiles
- `/file-organize downloads` - Organiser téléchargements
- `/file-rename iso-date .` - Ajouter dates ISO
- `/file-clean temp` - Nettoyer fichiers temporaires
- `/file-analyze audit .` - Vérifier organisation

Configuré le: $(Get-Date -Format "yyyy-MM-dd")
"@

$ReadmeContent | Out-File "$env:USERPROFILE\Documents\README-Organisation.md" -Encoding UTF8
```
