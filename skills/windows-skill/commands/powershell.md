# Gestion PowerShell

Administration de PowerShell, modules et profils.

## Mode d'Utilisation
```
/powershell                 → État et version PowerShell
/powershell modules         → Modules installés
/powershell install "module"→ Installer un module
/powershell profile         → Gérer le profil PowerShell
/powershell history         → Historique des commandes
/powershell aliases         → Alias définis
/powershell update          → Mettre à jour PowerShell/modules
```

Arguments: $ARGUMENTS

---

## État PowerShell (défaut)

```
⚡ POWERSHELL - ÉTAT
═══════════════════════════════════════════════════════════════

VERSIONS INSTALLÉES:
├─ PowerShell 7.4.1 (pwsh) ⭐ Recommandé
│  └─ Chemin: C:\Program Files\PowerShell\7\pwsh.exe
├─ Windows PowerShell 5.1.19041.3693
│  └─ Chemin: C:\Windows\System32\WindowsPowerShell\v1.0
└─ Version actuelle: 7.4.1

CONFIGURATION:
├─ Execution Policy (CurrentUser): RemoteSigned
├─ Execution Policy (LocalMachine): Restricted
├─ PSModulePath: 6 chemins configurés
├─ Profil utilisateur: ✅ Existe
└─ Transcription: ❌ Désactivée

MODULES CHARGÉS:
├─ Microsoft.PowerShell.Management
├─ Microsoft.PowerShell.Utility
├─ PSReadLine (2.3.4)
└─ (12 modules au total)

STATISTIQUES:
├─ Modules installés: 28
├─ Modules disponibles (PSGallery): 12,000+
├─ Historique commandes: 1,234 entrées
└─ Aliases personnalisés: 5

💡 Mise à jour disponible: PowerShell 7.4.2
```

---

## Mode `modules`

```
📦 MODULES POWERSHELL
═══════════════════════════════════════════════════════════════

MODULES INSTALLÉS:
┌───────────────────────────────┬──────────┬────────────────────┐
│ Module                        │ Version  │ Source             │
├───────────────────────────────┼──────────┼────────────────────┤
│ Az                            │ 11.2.0   │ PSGallery          │
│ Az.Accounts                   │ 2.15.0   │ PSGallery          │
│ Az.Compute                    │ 7.1.0    │ PSGallery          │
│ ImportExcel                   │ 7.8.6    │ PSGallery          │
│ Pester                        │ 5.5.0    │ PSGallery          │
│ PSReadLine                    │ 2.3.4    │ PSGallery          │
│ PSWindowsUpdate               │ 2.2.1.4  │ PSGallery          │
│ Terminal-Icons                │ 0.11.0   │ PSGallery          │
│ Microsoft.PowerShell.*        │ (intégré)│ Windows            │
│ PackageManagement             │ 1.4.8.1  │ Windows            │
│ PowerShellGet                 │ 2.2.5    │ Windows            │
└───────────────────────────────┴──────────┴────────────────────┘

MISES À JOUR DISPONIBLES:
├─ Az: 11.2.0 → 11.3.0
├─ PSReadLine: 2.3.4 → 2.3.5
└─ Pester: 5.5.0 → 5.6.1

MODULES POPULAIRES (non installés):
├─ oh-my-posh - Thèmes pour le terminal
├─ Carbon - Administration Windows
├─ dbatools - Administration SQL Server
└─ Pode - Serveur web PowerShell

Actions:
1. Installer un module: /powershell install "nom"
2. Mettre à jour: /powershell update modules
3. Désinstaller: /powershell uninstall "nom"
```

---

## Mode `install "module"`

```
📥 INSTALLER UN MODULE: ImportExcel
═══════════════════════════════════════════════════════════════

RECHERCHE SUR PSGALLERY...

TROUVÉ:
├─ Nom: ImportExcel
├─ Version: 7.8.6
├─ Auteur: Doug Finke
├─ Description: PowerShell module to import/export Excel spreadsheets
├─ Downloads: 12.5M
├─ Dernière mise à jour: 2024-01-15
└─ Dépendances: Aucune

PORTÉE D'INSTALLATION:
1. [CurrentUser] Utilisateur actuel (recommandé)
   └─ C:\Users\Jean\Documents\PowerShell\Modules
   
2. [AllUsers] Tous les utilisateurs (nécessite admin)
   └─ C:\Program Files\PowerShell\Modules

Choix: _

INSTALLATION EN COURS...
├─ Téléchargement... ✅
├─ Vérification signature... ✅
├─ Extraction... ✅
└─ Enregistrement... ✅

✅ Module ImportExcel 7.8.6 installé!

Utilisation:
Import-Module ImportExcel
Get-Command -Module ImportExcel
```

---

## Mode `profile`

```
📝 PROFIL POWERSHELL
═══════════════════════════════════════════════════════════════

FICHIERS DE PROFIL:
┌─────────────────────────┬────────────────────────────────────┬────────┐
│ Type                    │ Chemin                             │ Existe │
├─────────────────────────┼────────────────────────────────────┼────────┤
│ Current User, All Hosts │ $HOME\Documents\PowerShell\profile│ ✅     │
│ Current User, Current H.│ $HOME\...\Microsoft.PowerShell_pr.│ ❌     │
│ All Users, All Hosts    │ $PSHOME\profile.ps1               │ ❌     │
│ All Users, Current Host │ $PSHOME\Microsoft.PowerShell_pro..│ ❌     │
└─────────────────────────┴────────────────────────────────────┴────────┘

CONTENU ACTUEL (Current User, All Hosts):
```powershell
# Oh My Posh theme
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\paradox.omp.json" | Invoke-Expression

# Modules
Import-Module Terminal-Icons
Import-Module PSReadLine

# Aliases
Set-Alias -Name g -Value git
Set-Alias -Name k -Value kubectl
Set-Alias -Name d -Value docker

# PSReadLine config
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle ListView

# Custom functions
function ll { Get-ChildItem -Force }
function which { Get-Command $args | Select-Object -ExpandProperty Source }
```

ACTIONS:
1. Éditer le profil (ouvre VS Code)
2. Recharger le profil
3. Créer un backup du profil
4. Ajouter un alias
5. Ajouter un module à l'auto-import
```

---

## Mode `history`

```
📜 HISTORIQUE DES COMMANDES
═══════════════════════════════════════════════════════════════

STATISTIQUES:
├─ Commandes totales: 1,234
├─ Sessions uniques: 89
├─ Période: 2025-06-01 à aujourd'hui
└─ Fichier: $HOME\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

COMMANDES RÉCENTES:
┌─────┬────────────────────────────────────────────────────────────┐
│ #   │ Commande                                                   │
├─────┼────────────────────────────────────────────────────────────┤
│ 1   │ Get-Process | Where-Object CPU -gt 50                      │
│ 2   │ docker ps -a                                               │
│ 3   │ git status                                                 │
│ 4   │ code .                                                     │
│ 5   │ Get-ChildItem -Recurse -Filter "*.log"                     │
│ 6   │ Invoke-WebRequest https://api.example.com                  │
│ 7   │ Get-Service | Where-Object Status -eq 'Running'            │
│ 8   │ kubectl get pods -n production                             │
│ 9   │ npm install                                                │
│ 10  │ python -m venv .venv                                       │
└─────┴────────────────────────────────────────────────────────────┘

TOP COMMANDES:
├─ git (234 fois)
├─ docker (156 fois)
├─ Get-ChildItem (89 fois)
├─ code (78 fois)
└─ npm (67 fois)

ACTIONS:
1. Rechercher dans l'historique
2. Effacer l'historique
3. Exporter l'historique
4. Configurer la taille de l'historique
```

---

## Mode `aliases`

```
🏷️ ALIAS POWERSHELL
═══════════════════════════════════════════════════════════════

ALIAS PERSONNALISÉS:
┌─────────┬───────────────────────────────────────┬───────────────┐
│ Alias   │ Définition                            │ Source        │
├─────────┼───────────────────────────────────────┼───────────────┤
│ g       │ git                                   │ Profile       │
│ k       │ kubectl                               │ Profile       │
│ d       │ docker                                │ Profile       │
│ ll      │ Get-ChildItem -Force                  │ Profile       │
│ which   │ Get-Command ... | Select Source       │ Profile       │
└─────────┴───────────────────────────────────────┴───────────────┘

ALIAS SYSTÈME (sélection):
┌─────────┬───────────────────────────────────────┐
│ Alias   │ Définition                            │
├─────────┼───────────────────────────────────────┤
│ cat     │ Get-Content                           │
│ cd      │ Set-Location                          │
│ cls     │ Clear-Host                            │
│ cp      │ Copy-Item                             │
│ curl    │ Invoke-WebRequest                     │
│ diff    │ Compare-Object                        │
│ echo    │ Write-Output                          │
│ ls      │ Get-ChildItem                         │
│ man     │ help                                  │
│ mkdir   │ New-Item -ItemType Directory          │
│ mv      │ Move-Item                             │
│ rm      │ Remove-Item                           │
│ wget    │ Invoke-WebRequest                     │
└─────────┴───────────────────────────────────────┘

ACTIONS:
1. Créer un nouvel alias
2. Supprimer un alias
3. Rendre un alias permanent (ajouter au profil)
```

---

## Commandes de Référence

```powershell
# Version
$PSVersionTable

# Modules
Get-Module -ListAvailable
Install-Module -Name ModuleName -Scope CurrentUser
Update-Module -Name ModuleName
Remove-Module -Name ModuleName
Uninstall-Module -Name ModuleName

# Profil
$PROFILE | Format-List * -Force
code $PROFILE
. $PROFILE  # Recharger

# Execution Policy
Get-ExecutionPolicy -List
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Historique
Get-History
Get-Content (Get-PSReadLineOption).HistorySavePath
Clear-History

# Aliases
Get-Alias
New-Alias -Name myalias -Value Get-Process
Set-Alias -Name g -Value git
Export-Alias -Path aliases.csv

# Mise à jour PowerShell
winget upgrade Microsoft.PowerShell

# PSReadLine
Get-PSReadLineOption
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
```
