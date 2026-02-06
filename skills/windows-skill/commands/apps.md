# Gestion des Programmes et Applications

Administration des logiciels installés.

## Mode d'Utilisation
```
/apps                       → Liste des applications installées
/apps search "nom"          → Rechercher une application
/apps info "nom"            → Détails d'une application
/apps startup               → Programmes au démarrage
/apps recent                → Installations récentes
/apps large                 → Applications les plus volumineuses
/apps uninstall "nom"       → Désinstaller (avec confirmation)
/apps winget                → Mises à jour via winget
```

Arguments: $ARGUMENTS

---

## Liste des Applications (défaut)

```
📦 APPLICATIONS INSTALLÉES
═══════════════════════════════════════════════════════════════

Total: 87 applications

APPLICATIONS PRINCIPALES:
┌────────────────────────────────────┬─────────────┬────────────┐
│ Nom                                │ Version     │ Taille     │
├────────────────────────────────────┼─────────────┼────────────┤
│ Microsoft Office 365               │ 16.0.17126  │ 3.2 GB     │
│ Google Chrome                      │ 122.0.6261  │ 890 MB     │
│ Visual Studio Code                 │ 1.86.0      │ 450 MB     │
│ Mozilla Firefox                    │ 123.0       │ 380 MB     │
│ 7-Zip                              │ 23.01       │ 5 MB       │
│ Adobe Acrobat Reader               │ 24.001      │ 620 MB     │
│ VLC media player                   │ 3.0.20      │ 220 MB     │
│ ...                                │             │            │
└────────────────────────────────────┴─────────────┴────────────┘

APPLICATIONS WINDOWS (Store):
├─ Microsoft Edge: 121.0.2277
├─ Windows Terminal: 1.19.10302
├─ Photos: 2024.11010
└─ (12 autres)

Filtres: /apps large | /apps recent | /apps search "terme"
```

---

## Mode `search "nom"`

```
🔍 RECHERCHE: "visual"
═══════════════════════════════════════════════════════════════

RÉSULTATS:
┌────────────────────────────────────┬─────────────┬────────────┐
│ Nom                                │ Version     │ Éditeur    │
├────────────────────────────────────┼─────────────┼────────────┤
│ Microsoft Visual Studio Code       │ 1.86.0      │ Microsoft  │
│ Microsoft Visual C++ 2015-2022 x64 │ 14.38.33130 │ Microsoft  │
│ Microsoft Visual C++ 2015-2022 x86 │ 14.38.33130 │ Microsoft  │
│ Visual Studio Build Tools 2022     │ 17.8.6      │ Microsoft  │
└────────────────────────────────────┴─────────────┴────────────┘

Actions: /apps info "Visual Studio Code" | /apps uninstall "..."
```

---

## Mode `info "nom"`

```
📋 DÉTAILS: Microsoft Visual Studio Code
═══════════════════════════════════════════════════════════════

Informations générales:
├─ Nom complet: Microsoft Visual Studio Code
├─ Version: 1.86.0
├─ Éditeur: Microsoft Corporation
├─ Date d'installation: 2025-12-15
├─ Taille: ~450 MB

Emplacement:
├─ Installation: C:\Users\Jean\AppData\Local\Programs\Microsoft VS Code
├─ Données utilisateur: C:\Users\Jean\AppData\Roaming\Code
└─ Extensions: C:\Users\Jean\.vscode\extensions (2.1 GB)

Entrées registre:
├─ HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\{...}
└─ Associations fichiers: .js, .ts, .json, .md, ...

Processus associés:
├─ Code.exe (principal)
├─ Code Helper.exe
└─ Code Helper (Renderer).exe

Démarrage automatique: Non

Commande de désinstallation:
"C:\Users\Jean\AppData\Local\Programs\Microsoft VS Code\unins000.exe"

Actions disponibles:
├─ Ouvrir l'emplacement
├─ Désinstaller
└─ Réinitialiser les paramètres
```

---

## Mode `startup`

```
🚀 PROGRAMMES AU DÉMARRAGE
═══════════════════════════════════════════════════════════════

ACTIVÉS:
┌────────────────────────────────┬─────────────┬────────────────┐
│ Nom                            │ Impact      │ Emplacement    │
├────────────────────────────────┼─────────────┼────────────────┤
│ Microsoft OneDrive             │ 🟡 Modéré   │ Registre HKCU  │
│ Windows Security notification  │ 🟢 Faible   │ Registre HKLM  │
│ Spotify                        │ 🟡 Modéré   │ Registre HKCU  │
│ Discord                        │ 🟡 Modéré   │ Registre HKCU  │
│ Steam Client Bootstrapper      │ 🟠 Élevé    │ Registre HKCU  │
└────────────────────────────────┴─────────────┴────────────────┘

DÉSACTIVÉS:
├─ Adobe Creative Cloud (désactivé par utilisateur)
├─ Microsoft Teams (désactivé par utilisateur)
└─ Skype (désactivé par utilisateur)

TÂCHES PLANIFIÉES AU DÉMARRAGE:
├─ GoogleUpdateTaskMachineCore
├─ MicrosoftEdgeUpdateTaskMachine
└─ OneDrive Standalone Update Task

IMPACT ESTIMÉ SUR LE DÉMARRAGE:
├─ Temps ajouté: ~12 secondes
└─ RAM utilisée au démarrage: ~850 MB

⚠️ RECOMMANDATIONS:
├─ Steam: Peut être désactivé si non utilisé quotidiennement (-3 sec)
└─ Discord/Spotify: Désactiver si démarrage manuel acceptable

Désactiver un programme? /apps startup disable "Nom"
```

---

## Mode `recent`

```
📅 INSTALLATIONS RÉCENTES (30 derniers jours)
═══════════════════════════════════════════════════════════════

┌────────────────┬────────────────────────────────┬─────────────┐
│ Date           │ Application                    │ Action      │
├────────────────┼────────────────────────────────┼─────────────┤
│ 2026-02-01     │ Visual Studio Code             │ Mise à jour │
│ 2026-01-28     │ Google Chrome                  │ Mise à jour │
│ 2026-01-25     │ 7-Zip 23.01                    │ Installation│
│ 2026-01-20     │ Node.js 20.11.0                │ Installation│
│ 2026-01-18     │ Python 3.12.1                  │ Installation│
│ 2026-01-15     │ Git 2.43.0                     │ Installation│
│ 2026-01-10     │ Zoom Workplace                 │ Désinstallé │
└────────────────┴────────────────────────────────┴─────────────┘

Résumé:
├─ Nouvelles installations: 4
├─ Mises à jour: 8
└─ Désinstallations: 2
```

---

## Mode `large`

```
💾 APPLICATIONS LES PLUS VOLUMINEUSES
═══════════════════════════════════════════════════════════════

TOP 15 (espace disque):
┌────┬────────────────────────────────────┬───────────┬─────────┐
│ #  │ Application                        │ Taille    │ % Total │
├────┼────────────────────────────────────┼───────────┼─────────┤
│ 1  │ Microsoft Office 365               │ 3.2 GB    │ 12.8%   │
│ 2  │ Visual Studio 2022                 │ 2.8 GB    │ 11.2%   │
│ 3  │ Adobe Creative Cloud               │ 2.1 GB    │ 8.4%    │
│ 4  │ Windows SDK                        │ 1.9 GB    │ 7.6%    │
│ 5  │ .NET SDK Collection                │ 1.5 GB    │ 6.0%    │
│ 6  │ Google Chrome                      │ 890 MB    │ 3.5%    │
│ 7  │ Microsoft Edge                     │ 750 MB    │ 3.0%    │
│ 8  │ Adobe Acrobat Reader               │ 620 MB    │ 2.5%    │
│ 9  │ Zoom Workplace                     │ 580 MB    │ 2.3%    │
│ 10 │ Visual Studio Code                 │ 450 MB    │ 1.8%    │
└────┴────────────────────────────────────┴───────────┴─────────┘

Espace total utilisé par les applications: ~25 GB

DONNÉES UTILISATEUR ASSOCIÉES:
├─ VS Code extensions: 2.1 GB
├─ Chrome profil + cache: 1.8 GB
├─ npm cache: 1.2 GB
└─ pip cache: 0.8 GB

💡 Suggestions d'économie:
├─ Nettoyer le cache npm: npm cache clean --force (~1.2 GB)
├─ Nettoyer le cache Chrome: Paramètres > Effacer données (~1 GB)
└─ Désinstaller Visual Studio si VS Code suffit (~2.8 GB)
```

---

## Mode `uninstall "nom"`

⚠️ DEMANDER CONFIRMATION

```
🗑️ DÉSINSTALLATION: Zoom Workplace
═══════════════════════════════════════════════════════════════

Application: Zoom Workplace
Version: 6.0.0
Taille: 580 MB
Éditeur: Zoom Video Communications, Inc.
Installé le: 2025-11-20

Cette application va être désinstallée.
Données utilisateur conservées: Oui (dans %AppData%\Zoom)

⚠️ VÉRIFICATIONS:
├─ L'application n'est pas en cours d'exécution: ✅
├─ Aucun processus dépendant: ✅
└─ Point de restauration disponible: ✅

Confirmer la désinstallation? [O/N]

Pour supprimer aussi les données utilisateur:
/apps uninstall "Zoom" --purge
```

---

## Mode `winget`

```
📦 MISES À JOUR DISPONIBLES (winget)
═══════════════════════════════════════════════════════════════

Vérification des sources winget...
Sources: winget, msstore

MISES À JOUR DISPONIBLES:
┌────────────────────────────────────┬─────────────┬─────────────┐
│ Application                        │ Actuelle    │ Disponible  │
├────────────────────────────────────┼─────────────┼─────────────┤
│ Google.Chrome                      │ 122.0.6261  │ 122.0.6273  │
│ Mozilla.Firefox                    │ 123.0       │ 123.0.1     │
│ Python.Python.3.12                 │ 3.12.1      │ 3.12.2      │
│ Git.Git                            │ 2.43.0      │ 2.44.0      │
│ Microsoft.VisualStudioCode         │ 1.86.0      │ 1.86.2      │
└────────────────────────────────────┴─────────────┴─────────────┘

Total: 5 mises à jour disponibles

Options:
1. Tout mettre à jour: winget upgrade --all
2. Mise à jour sélective: winget upgrade <id>
3. Voir les détails: winget show <id>

Mettre à jour maintenant?
[ ] Toutes les applications
[ ] Sélection: Chrome, Firefox, VS Code
[O/N]
```

---

## Commandes de Référence

```powershell
# Liste des applications installées
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*,
                 HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*,
                 HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |
    Select-Object DisplayName, DisplayVersion, Publisher, InstallDate, EstimatedSize |
    Sort-Object DisplayName

# Applications Windows Store
Get-AppxPackage | Select-Object Name, Version

# Programmes au démarrage
Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location

# Winget
winget list
winget upgrade
winget upgrade --all
winget uninstall "Nom"

# Désinstallation silencieuse
$app = Get-ItemProperty HKLM:\Software\...\Uninstall\* | Where-Object {$_.DisplayName -like "*Nom*"}
Start-Process -FilePath $app.UninstallString -ArgumentList "/S" -Wait
```
