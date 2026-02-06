# Gestion des Packages (Winget & Chocolatey)

Administration des gestionnaires de packages Windows.

## Mode d'Utilisation
```
/pkg                        → État des gestionnaires et mises à jour
/pkg search "nom"           → Rechercher un package
/pkg install "nom"          → Installer un package
/pkg update                 → Mettre à jour tous les packages
/pkg list                   → Liste des packages installés
/pkg info "nom"             → Informations sur un package
/pkg remove "nom"           → Désinstaller un package
/pkg export                 → Exporter la liste des packages
/pkg import                 → Importer/Installer depuis une liste
/pkg cleanup                → Nettoyage du cache
```

Arguments: $ARGUMENTS

---

## État des Gestionnaires (défaut)

```
📦 GESTIONNAIRES DE PACKAGES
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
🔍 RECHERCHE: "vscode"
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
📥 INSTALLATION: Microsoft.VisualStudioCode
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

[██████████████████░░░░░░░░░░░░░░] 55%
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
🔄 MISE À JOUR DES PACKAGES
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

## Mode `list`

```
📋 PACKAGES INSTALLÉS
═══════════════════════════════════════════════════════════════

WINGET (45 packages):
┌────────────────────────────────────────┬─────────────┬────────────┐
│ Nom                                    │ Version     │ Source     │
├────────────────────────────────────────┼─────────────┼────────────┤
│ 7zip.7zip                              │ 23.01       │ winget     │
│ Discord.Discord                        │ 1.0.9035    │ winget     │
│ Docker.DockerDesktop                   │ 4.27.1      │ winget     │
│ Git.Git                                │ 2.44.0      │ winget     │
│ Google.Chrome                          │ 122.0.6273  │ winget     │
│ Microsoft.PowerShell                   │ 7.4.1       │ winget     │
│ Microsoft.VisualStudioCode             │ 1.86.2      │ winget     │
│ Microsoft.WindowsTerminal              │ 1.19.10302  │ winget     │
│ Mozilla.Firefox                        │ 123.0.1     │ winget     │
│ Notepad++.Notepad++                    │ 8.6.4       │ winget     │
│ OpenJS.NodeJS                          │ 20.11.1     │ winget     │
│ Python.Python.3.12                     │ 3.12.2      │ winget     │
│ ... (33 autres)                        │             │            │
└────────────────────────────────────────┴─────────────┴────────────┘

CHOCOLATEY (23 packages):
┌────────────────────────────────────────┬─────────────┬────────────┐
│ Nom                                    │ Version     │ Source     │
├────────────────────────────────────────┼─────────────┼────────────┤
│ chocolatey                             │ 2.2.2       │ choco      │
│ chocolatey-core.extension              │ 1.4.0       │ choco      │
│ curl                                   │ 8.6.0       │ choco      │
│ fzf                                    │ 0.46.1      │ choco      │
│ jq                                     │ 1.7.1       │ choco      │
│ neovim                                 │ 0.9.5       │ choco      │
│ ripgrep                                │ 14.1.0      │ choco      │
│ wget                                   │ 1.21.4      │ choco      │
│ ... (15 autres)                        │             │            │
└────────────────────────────────────────┴─────────────┴────────────┘

RÉSUMÉ:
├─ Total packages: 68
├─ Winget: 45
├─ Chocolatey: 23
└─ Dernière mise à jour: 2026-02-03 10:30
```

---

## Mode `export`

```
📤 EXPORTER LA LISTE DES PACKAGES
═══════════════════════════════════════════════════════════════

FORMAT D'EXPORT:

1. WINGET JSON (recommandé)
   → winget export -o packages.json
   → Restaurable avec: winget import -i packages.json
   → Inclut les sources et versions

2. CHOCOLATEY PACKAGES.CONFIG
   → Format XML standard Chocolatey
   → Restaurable avec: choco install packages.config

3. SCRIPT POWERSHELL
   → Script qui installe tous les packages
   → Fonctionne sur nouvelle machine

4. LISTE TEXTE
   → Simple liste de noms de packages
   → Pour référence/documentation

5. TOUT EXPORTER
   → Exporte dans tous les formats
   → Destination: C:\Backups\Packages\

Choix: 5

═══════════════════════════════════════════════════════════════
EXPORT EN COURS...

✅ Fichiers créés:
├─ C:\Backups\Packages\winget-packages.json (45 packages)
├─ C:\Backups\Packages\choco-packages.config (23 packages)
├─ C:\Backups\Packages\install-all.ps1 (script)
└─ C:\Backups\Packages\packages-list.txt (liste)

Pour restaurer sur une nouvelle machine:
1. Winget: winget import -i winget-packages.json
2. Choco: choco install packages.config -y
3. Ou: .\install-all.ps1
```

---

## Mode `cleanup`

```
🧹 NETTOYAGE DU CACHE
═══════════════════════════════════════════════════════════════

ANALYSE DU CACHE:

WINGET:
├─ Cache installateurs: 234 MB
├─ Cache sources: 45 MB
├─ Logs: 12 MB
└─ Total: 291 MB

CHOCOLATEY:
├─ Packages téléchargés: 512 MB
├─ Cache nupkg: 156 MB
├─ Logs: 8 MB
└─ Total: 676 MB

ESPACE TOTAL RÉCUPÉRABLE: 967 MB

OPTIONS:
├─ [1] Nettoyer le cache Winget (291 MB)
├─ [2] Nettoyer le cache Chocolatey (676 MB)
├─ [3] Tout nettoyer (967 MB)
├─ [4] Nettoyage agressif (+ anciens packages)
└─ [5] Annuler

Choix: 3

═══════════════════════════════════════════════════════════════
NETTOYAGE EN COURS...

Nettoyage Winget... ✅ 291 MB libérés
Nettoyage Chocolatey... ✅ 676 MB libérés

✅ Nettoyage terminé!
Espace total récupéré: 967 MB
```

---

## Commandes de Référence

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

# Lister
winget list

# Désinstaller
winget uninstall -e --id Package.ID

# Export/Import
winget export -o packages.json
winget import -i packages.json

# === CHOCOLATEY ===

# Rechercher
choco search terme

# Installer
choco install packagename -y

# Mettre à jour
choco upgrade all -y
choco upgrade packagename -y

# Lister
choco list --local-only

# Désinstaller
choco uninstall packagename -y

# Export
choco export packages.config

# Installer depuis config
choco install packages.config -y

# Nettoyage
choco cache remove

# === SCOOP (Alternative) ===
# Installation: irm get.scoop.sh | iex
scoop search terme
scoop install package
scoop update *
```
