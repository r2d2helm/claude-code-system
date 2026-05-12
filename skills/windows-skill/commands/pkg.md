# Gestion des Packages (Winget & Chocolatey)

Voir aussi: [[pkg-advanced]]

Administration des gestionnaires de packages Windows.

## Mode d'Utilisation
```
/pkg                        → État des gestionnaires et mises à jour
/pkg search "nom"           → Rechercher un package
/pkg install "nom"          → Installer un package
/pkg update                 → Mettre à jour tous les packages
/pkg list                   → Liste des packages installés (voir pkg-advanced)
/pkg info "nom"             → Informations sur un package
/pkg remove "nom"           → Désinstaller un package
/pkg export                 → Exporter la liste (voir pkg-advanced)
/pkg import                 → Importer depuis une liste (voir pkg-advanced)
/pkg cleanup                → Nettoyage du cache (voir pkg-advanced)
```

Arguments: $ARGUMENTS

---

## État des Gestionnaires (défaut)

```
GESTIONNAIRES DE PACKAGES
═══════════════════════════════════════════════════════════════

WINGET (Windows Package Manager):
├─ Version: 1.7.10582
├─ Sources:
│  ├─ winget (msstore): ✅ Actif (dernière màj: il y a 2h)
│  └─ msstore: ✅ Actif
├─ Packages installés (winget): 45
└─ Mises à jour disponibles: 8

CHOCOLATEY:
├─ Version: 2.2.2
├─ Sources:
│  └─ chocolatey (community): ✅ Actif
├─ Packages installés: 23
└─ Mises à jour disponibles: 3

MISES À JOUR DISPONIBLES:
┌────────────────────────────────┬─────────────┬─────────────┬────────┐
│ Package                        │ Actuelle    │ Disponible  │ Source │
├────────────────────────────────┼─────────────┼─────────────┼────────┤
│ Google.Chrome                  │ 122.0.6261  │ 122.0.6273  │ winget │
│ Mozilla.Firefox                │ 123.0       │ 123.0.1     │ winget │
│ Microsoft.VisualStudioCode     │ 1.86.0      │ 1.86.2      │ winget │
│ Python.Python.3.12             │ 3.12.1      │ 3.12.2      │ winget │
│ Git.Git                        │ 2.43.0      │ 2.44.0      │ winget │
│ nodejs                         │ 20.11.0     │ 20.11.1     │ choco  │
│ 7zip                           │ 23.01       │ 24.01       │ choco  │
│ notepadplusplus                │ 8.6.2       │ 8.6.4       │ choco  │
└────────────────────────────────┴─────────────┴─────────────┴────────┘

ESPACE CACHE:
├─ Winget: 234 MB (C:\Users\Jean\AppData\Local\Packages\...\LocalCache)
├─ Chocolatey: 512 MB (C:\ProgramData\chocolatey\lib)
└─ Total: 746 MB

ACTIONS RAPIDES:
1. Mettre à jour tous les packages: /pkg update
2. Rechercher un package: /pkg search "nom"
3. Nettoyer le cache: /pkg cleanup
```

---

## Mode `search "nom"`

```
RECHERCHE: "vscode"
═══════════════════════════════════════════════════════════════

RÉSULTATS WINGET:
┌────────────────────────────────────────┬────────────┬─────────────┐
│ Nom                                    │ ID         │ Version     │
├────────────────────────────────────────┼────────────┼─────────────┤
│ Microsoft Visual Studio Code           │ Microsoft.VisualStudioCode │ 1.86.2 │
│ Microsoft Visual Studio Code Insiders  │ Microsoft.VisualStudioCode.Insiders │ 1.87.0 │
│ VSCodium                               │ VSCodium.VSCodium │ 1.86.2 │
│ code-server                            │ coder.code-server │ 4.20.0 │
└────────────────────────────────────────┴────────────┴─────────────┘

RÉSULTATS CHOCOLATEY:
┌────────────────────────────────────────┬────────────┬─────────────┐
│ Nom                                    │ ID         │ Version     │
├────────────────────────────────────────┼────────────┼─────────────┤
│ Visual Studio Code                     │ vscode     │ 1.86.2      │
│ Visual Studio Code - Insiders         │ vscode-insiders │ 1.87.0 │
│ VSCodium                               │ vscodium   │ 1.86.2      │
└────────────────────────────────────────┴────────────┴─────────────┘

RECOMMANDATION:
├─ Package officiel: Microsoft.VisualStudioCode (winget)
└─ Alternative OSS: VSCodium.VSCodium (sans télémétrie)

Pour installer: /pkg install "Microsoft.VisualStudioCode"
Pour plus d'infos: /pkg info "Microsoft.VisualStudioCode"
```

---

## Mode `install "nom"`

```
INSTALLATION: Microsoft.VisualStudioCode
═══════════════════════════════════════════════════════════════

INFORMATIONS:
├─ Nom: Microsoft Visual Studio Code
├─ Éditeur: Microsoft Corporation
├─ Version: 1.86.2
├─ Licence: MIT (avec télémétrie Microsoft)
├─ Taille: ~100 MB
└─ Source: winget

DÉJÀ INSTALLÉ?
└─ Version 1.86.0 détectée → Mise à jour vers 1.86.2

OPTIONS D'INSTALLATION:
├─ [x] Mode silencieux (pas de prompts)
├─ [ ] Installation personnalisée (choisir le chemin)
├─ [ ] Ajouter au PATH
├─ [ ] Créer un raccourci bureau
└─ [ ] Lancer après installation

⚠️ Cette installation peut:
├─ Modifier les associations de fichiers
├─ Ajouter des entrées au menu contextuel
└─ Installer des composants supplémentaires

Confirmer l'installation? [O/N]

═══════════════════════════════════════════════════════════════
INSTALLATION EN COURS...

[████████████████████░░░░░░░░░░░░] 55%
Téléchargement: VSCodeSetup-x64-1.86.2.exe (98 MB)

...

✅ Installation terminée!
├─ Version installée: 1.86.2
├─ Chemin: C:\Users\Jean\AppData\Local\Programs\Microsoft VS Code
└─ Commande: code

Lancer VS Code maintenant? [O/N]
```

---

## Mode `update`

```
MISE À JOUR DES PACKAGES
═══════════════════════════════════════════════════════════════

ANALYSE EN COURS...

MISES À JOUR DISPONIBLES:
┌────────────────────────────────┬─────────────┬─────────────┬─────────┐
│ Package                        │ Actuelle    │ Disponible  │ Source  │
├────────────────────────────────┼─────────────┼─────────────┼─────────┤
│ [x] Google.Chrome              │ 122.0.6261  │ 122.0.6273  │ winget  │
│ [x] Mozilla.Firefox            │ 123.0       │ 123.0.1     │ winget  │
│ [x] Microsoft.VisualStudioCode │ 1.86.0      │ 1.86.2      │ winget  │
│ [x] Python.Python.3.12         │ 3.12.1      │ 3.12.2      │ winget  │
│ [x] Git.Git                    │ 2.43.0      │ 2.44.0      │ winget  │
│ [x] nodejs                     │ 20.11.0     │ 20.11.1     │ choco   │
│ [ ] 7zip                       │ 23.01       │ 24.01       │ choco   │
│ [x] notepadplusplus            │ 8.6.2       │ 8.6.4       │ choco   │
└────────────────────────────────┴─────────────┴─────────────┴─────────┘

OPTIONS:
├─ [1] Tout mettre à jour (7 sélectionnés)
├─ [2] Mettre à jour winget uniquement (5)
├─ [3] Mettre à jour chocolatey uniquement (2)
├─ [4] Sélection personnalisée
└─ [5] Annuler

Choix: 1

═══════════════════════════════════════════════════════════════
MISE À JOUR EN COURS...

[1/7] Google.Chrome... ✅ Mis à jour (122.0.6273)
[2/7] Mozilla.Firefox... ✅ Mis à jour (123.0.1)
[3/7] Microsoft.VisualStudioCode... ✅ Mis à jour (1.86.2)
[4/7] Python.Python.3.12... ✅ Mis à jour (3.12.2)
[5/7] Git.Git... ✅ Mis à jour (2.44.0)
[6/7] nodejs (choco)... ✅ Mis à jour (20.11.1)
[7/7] notepadplusplus (choco)... ✅ Mis à jour (8.6.4)

═══════════════════════════════════════════════════════════════
✅ MISE À JOUR TERMINÉE

Résumé:
├─ Packages mis à jour: 7
├─ Échecs: 0
├─ Temps total: 3m 45s
└─ Redémarrage requis: Non

⚠️ Note: Certaines applications doivent être fermées pour la mise à jour.
Fermez Chrome et Firefox si les mises à jour n'ont pas pris effet.
```

---

## Commandes de Référence (Core)

```powershell
# === WINGET ===

# Rechercher
winget search "terme"

# Installer
winget install -e --id Package.ID
winget install -e --id Microsoft.VisualStudioCode

# Mettre à jour
winget upgrade                    # Liste
winget upgrade --all              # Tout mettre à jour
winget upgrade -e --id Package.ID # Un seul package

# Désinstaller
winget uninstall -e --id Package.ID

# === CHOCOLATEY ===

# Rechercher
choco search terme

# Installer
choco install packagename -y

# Mettre à jour
choco upgrade all -y
choco upgrade packagename -y

# Désinstaller
choco uninstall packagename -y
```
