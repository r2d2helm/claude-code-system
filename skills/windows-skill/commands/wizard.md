# /win-wizard - Assistants Interactifs Windows

## Description

Wizards de configuration guidée pour Windows 10/11 et Windows Server. Interface conversationnelle avec étapes numérotées, validation à chaque étape et génération de scripts PowerShell.

## Syntaxe

```
/win-wizard <wizard> [--auto] [--export]
```

## Wizards Disponibles

| Wizard | Description | Étapes |
|--------|-------------|--------|
| `setup` | Configuration initiale poste de travail | 10 |
| `security` | Hardening sécurité complet | 8 |
| `developer` | Setup environnement développeur | 7 |
| `server` | Configuration Windows Server | 9 |
| `network` | Configuration réseau avancée | 6 |
| `backup` | Stratégie sauvegarde | 5 |
| `domain` | Jonction domaine Active Directory | 6 |
| `hyperv` | Setup Hyper-V | 5 |
| `wsl` | Configuration WSL2 | 4 |
| `remote` | Accès distant (RDP, SSH, VPN) | 5 |

## Options

| Option | Description |
|--------|-------------|
| `--auto` | Mode automatique avec valeurs par défaut |
| `--export` | Exporter script PowerShell généré |
| `--dry-run` | Afficher commandes sans exécuter |

---

## 🧙 Wizard: Setup Initial (`/win-wizard setup`)

Configuration initiale complète d'un poste Windows.

### Étape 1/10: Informations Système

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD SETUP INITIAL - ÉTAPE 1/10                  ║
║                  Informations Système                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Nom actuel: DESKTOP-ABC123                                  ║
║                                                              ║
║  Nouveau nom de l'ordinateur:                                ║
║  > [PC-DEV-01]                                               ║
║                                                              ║
║  Groupe de travail ou Domaine:                               ║
║  (1) WORKGROUP                                               ║
║  (2) Domaine AD (configurer plus tard)                       ║
║  > [1]                                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
Rename-Computer -NewName "PC-DEV-01" -Force
```

### Étape 2/10: Configuration Réseau

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD SETUP INITIAL - ÉTAPE 2/10                  ║
║                  Configuration Réseau                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Interface détectée: Ethernet (Intel I219-V)                 ║
║                                                              ║
║  Configuration IP:                                           ║
║  (1) DHCP automatique                                        ║
║  (2) IP statique                                             ║
║  > [1]                                                       ║
║                                                              ║
║  Configuration DNS:                                          ║
║  (1) DNS automatique (DHCP)                                  ║
║  (2) DNS personnalisé                                        ║
║  > [2]                                                       ║
║                                                              ║
║  DNS primaire: [1.1.1.1]                                     ║
║  DNS secondaire: [8.8.8.8]                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses "1.1.1.1","8.8.8.8"
```

### Étape 3/10: Windows Update

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD SETUP INITIAL - ÉTAPE 3/10                  ║
║                    Windows Update                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Politique de mise à jour:                                   ║
║  (1) Automatique - Télécharger et installer                  ║
║  (2) Notification - Me prévenir avant                        ║
║  (3) Différé - Retarder de 7 jours                           ║
║  (4) Manuel - Désactiver auto-update                         ║
║  > [3]                                                       ║
║                                                              ║
║  Heures actives (pas de redémarrage):                        ║
║  Début: [08:00]  Fin: [22:00]                                ║
║                                                              ║
║  Installer mises à jour en attente maintenant?               ║
║  (Y)es / (N)o > [N]                                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
# Configurer heures actives
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" -Name "ActiveHoursStart" -Value 8
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" -Name "ActiveHoursEnd" -Value 22

# Différer mises à jour de 7 jours
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" -Name "DeferFeatureUpdatesPeriodInDays" -Value 7
```

### Étape 4/10: Compte Utilisateur

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD SETUP INITIAL - ÉTAPE 4/10                  ║
║                   Compte Utilisateur                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Utilisateur actuel: r2d2 (Administrateur)                   ║
║                                                              ║
║  Créer un compte administrateur supplémentaire?              ║
║  (Y)es / (N)o > [Y]                                          ║
║                                                              ║
║  Nom d'utilisateur: [admin-backup]                           ║
║  Mot de passe: [********]                                    ║
║  Confirmer: [********]                                       ║
║                                                              ║
║  Désactiver compte Administrator intégré?                    ║
║  (Y)es / (N)o > [Y]                                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
$Password = ConvertTo-SecureString "P@ssw0rd!" -AsPlainText -Force
New-LocalUser -Name "admin-backup" -Password $Password -FullName "Backup Admin" -Description "Compte admin secondaire"
Add-LocalGroupMember -Group "Administrators" -Member "admin-backup"
Disable-LocalUser -Name "Administrator"
```

### Étape 5/10: Sécurité de Base

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD SETUP INITIAL - ÉTAPE 5/10                  ║
║                   Sécurité de Base                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [✓] Activer Windows Defender                                ║
║  [✓] Activer Firewall (tous profils)                         ║
║  [✓] Activer UAC (niveau recommandé)                         ║
║  [✓] Désactiver accès distant (RDP) par défaut               ║
║  [ ] Activer BitLocker (configurer séparément)               ║
║  [✓] Désactiver services inutiles                            ║
║                                                              ║
║  Appliquer ces paramètres? (Y)es / (N)o > [Y]                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
# Windows Defender
Set-MpPreference -DisableRealtimeMonitoring $false

# Firewall tous profils
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# UAC niveau recommandé
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "ConsentPromptBehaviorAdmin" -Value 5

# Désactiver RDP
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 1

# Désactiver services inutiles
$ServicesToDisable = @("DiagTrack", "dmwappushservice", "RemoteRegistry", "RetailDemo")
foreach ($svc in $ServicesToDisable) {
    Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue
    Set-Service -Name $svc -StartupType Disabled -ErrorAction SilentlyContinue
}
```

### Étape 6/10: Applications Essentielles

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD SETUP INITIAL - ÉTAPE 6/10                  ║
║                Applications Essentielles                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Installer via winget:                                       ║
║                                                              ║
║  [✓] 7-Zip                                                   ║
║  [✓] VLC Media Player                                        ║
║  [✓] Firefox ou Chrome                                       ║
║  [✓] Adobe Reader                                            ║
║  [ ] LibreOffice                                             ║
║  [✓] Notepad++                                               ║
║  [ ] Visual Studio Code                                      ║
║                                                              ║
║  Continuer? (Y)es / (N)o / (S)kip > [Y]                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
winget install --id 7zip.7zip -e --silent
winget install --id VideoLAN.VLC -e --silent
winget install --id Mozilla.Firefox -e --silent
winget install --id Adobe.Acrobat.Reader.64-bit -e --silent
winget install --id Notepad++.Notepad++ -e --silent
```

### Étape 7/10: Nettoyage Bloatware

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD SETUP INITIAL - ÉTAPE 7/10                  ║
║                   Nettoyage Bloatware                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Applications préinstallées à supprimer:                     ║
║                                                              ║
║  [✓] Xbox Game Bar                                           ║
║  [✓] Cortana                                                 ║
║  [✓] Feedback Hub                                            ║
║  [✓] Get Help                                                ║
║  [✓] Microsoft News                                          ║
║  [✓] Microsoft Solitaire                                     ║
║  [✓] Mixed Reality Portal                                    ║
║  [ ] OneDrive (conserver)                                    ║
║  [✓] Skype                                                   ║
║  [✓] Tips                                                    ║
║                                                              ║
║  Supprimer sélection? (Y)es / (N)o > [Y]                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
$Bloatware = @(
    "Microsoft.XboxApp",
    "Microsoft.XboxGameOverlay",
    "Microsoft.549981C3F5F10",  # Cortana
    "Microsoft.WindowsFeedbackHub",
    "Microsoft.GetHelp",
    "Microsoft.BingNews",
    "Microsoft.MicrosoftSolitaireCollection",
    "Microsoft.MixedReality.Portal",
    "Microsoft.SkypeApp",
    "Microsoft.Getstarted"
)

foreach ($app in $Bloatware) {
    Get-AppxPackage -Name $app -AllUsers | Remove-AppxPackage -AllUsers -ErrorAction SilentlyContinue
    Get-AppxProvisionedPackage -Online | Where-Object {$_.PackageName -like "*$app*"} | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue
}
```

### Étape 8/10: Personnalisation Interface

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD SETUP INITIAL - ÉTAPE 8/10                  ║
║                Personnalisation Interface                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Thème:                                                      ║
║  (1) Clair                                                   ║
║  (2) Sombre                                                  ║
║  (3) Automatique (selon heure)                               ║
║  > [2]                                                       ║
║                                                              ║
║  Barre des tâches:                                           ║
║  [✓] Masquer Recherche                                       ║
║  [✓] Masquer Widgets                                         ║
║  [✓] Masquer Chat Teams                                      ║
║  [ ] Centrer icônes (Win11)                                  ║
║                                                              ║
║  Explorateur - afficher:                                     ║
║  [✓] Extensions de fichiers                                  ║
║  [✓] Fichiers cachés                                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
# Thème sombre
Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "AppsUseLightTheme" -Value 0
Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "SystemUsesLightTheme" -Value 0

# Barre des tâches
Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Search" -Name "SearchboxTaskbarMode" -Value 0
Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "ShowTaskViewButton" -Value 0
Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "TaskbarDa" -Value 0

# Explorateur
Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "HideFileExt" -Value 0
Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "Hidden" -Value 1

Stop-Process -Name explorer -Force
Start-Process explorer
```

### Étape 9/10: Optimisations Performance

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD SETUP INITIAL - ÉTAPE 9/10                  ║
║               Optimisations Performance                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [✓] Désactiver effets visuels non essentiels                ║
║  [✓] Optimiser plan d'alimentation (Hautes performances)     ║
║  [✓] Désactiver indexation sur SSD                           ║
║  [✓] Configurer fichier d'échange automatique                ║
║  [ ] Désactiver Superfetch (garder pour HDD)                 ║
║  [✓] Désactiver apps en arrière-plan                         ║
║                                                              ║
║  Type de stockage principal:                                 ║
║  (1) SSD/NVMe                                                ║
║  (2) HDD                                                     ║
║  > [1]                                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
# Plan alimentation Hautes performances
powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c

# Désactiver indexation SSD
Stop-Service -Name "WSearch" -Force
Set-Service -Name "WSearch" -StartupType Disabled

# Désactiver apps arrière-plan
Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" -Name "GlobalUserDisabled" -Value 1

# Optimiser pour SSD
fsutil behavior set DisableLastAccess 1
fsutil behavior set EncryptPagingFile 0
```

### Étape 10/10: Résumé et Application

```
╔══════════════════════════════════════════════════════════════╗
║           WIZARD SETUP INITIAL - ÉTAPE 10/10                 ║
║                  Résumé et Application                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✅ Nom ordinateur: PC-DEV-01                                ║
║  ✅ DNS: 1.1.1.1, 8.8.8.8                                    ║
║  ✅ Windows Update: Différé 7 jours                          ║
║  ✅ Utilisateur admin-backup créé                            ║
║  ✅ Sécurité de base configurée                              ║
║  ✅ 5 applications installées                                ║
║  ✅ 10 bloatwares supprimés                                  ║
║  ✅ Thème sombre appliqué                                    ║
║  ✅ Performance optimisée (SSD)                              ║
║                                                              ║
║  Actions requises:                                           ║
║  ⚠️  Redémarrage nécessaire pour nom d'ordinateur            ║
║                                                              ║
║  (A)ppliquer / (E)xporter script / (C)ancel                  ║
║  > [A]                                                       ║
║                                                              ║
║  🔄 Application en cours...                                  ║
║  ████████████████████████████████████████ 100%               ║
║                                                              ║
║  ✅ Configuration terminée!                                  ║
║  📝 Script exporté: C:\Scripts\setup-initial.ps1             ║
║                                                              ║
║  Redémarrer maintenant? (Y)es / (N)o > [Y]                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🧙 Wizard: Security Hardening (`/win-wizard security`)

Hardening sécurité complet selon CIS Benchmarks et Microsoft Security Baselines.

### Étape 1/8: Audit Initial

```
╔══════════════════════════════════════════════════════════════╗
║         WIZARD SECURITY HARDENING - ÉTAPE 1/8                ║
║                     Audit Initial                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔍 Scan sécurité en cours...                                ║
║  ████████████████████████████████████████ 100%               ║
║                                                              ║
║  RÉSULTATS AUDIT:                                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Catégorie              │ Score  │ Status                │ ║
║  ├─────────────────────────────────────────────────────────┤ ║
║  │ Windows Defender       │ 70%    │ ⚠️  Améliorable       │ ║
║  │ Firewall               │ 85%    │ ✅ Bon                │ ║
║  │ Comptes utilisateurs   │ 40%    │ ❌ Critique           │ ║
║  │ Services               │ 60%    │ ⚠️  Améliorable       │ ║
║  │ Réseau                 │ 55%    │ ⚠️  Améliorable       │ ║
║  │ Mises à jour           │ 90%    │ ✅ Bon                │ ║
║  │ Chiffrement            │ 0%     │ ❌ Non configuré      │ ║
║  │ Audit/Logging          │ 30%    │ ❌ Insuffisant        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Score global: 54% - AMÉLIORATION RECOMMANDÉE                ║
║                                                              ║
║  Continuer avec hardening? (Y)es / (N)o > [Y]                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 2/8: Windows Defender Avancé

```
╔══════════════════════════════════════════════════════════════╗
║         WIZARD SECURITY HARDENING - ÉTAPE 2/8                ║
║                 Windows Defender Avancé                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Configuration recommandée:                                  ║
║                                                              ║
║  [✓] Protection temps réel                                   ║
║  [✓] Protection cloud (MAPS)                                 ║
║  [✓] Soumission automatique échantillons                     ║
║  [✓] Protection contre falsification                         ║
║  [✓] Controlled Folder Access                                ║
║  [✓] Network Protection                                      ║
║  [✓] PUA Protection (apps indésirables)                      ║
║                                                              ║
║  Attack Surface Reduction (ASR) Rules:                       ║
║  [✓] Bloquer exécutables email                               ║
║  [✓] Bloquer Office créant processus enfants                 ║
║  [✓] Bloquer Office créant contenu exécutable                ║
║  [✓] Bloquer appels API Win32 depuis macros                  ║
║  [✓] Bloquer scripts obfusqués                               ║
║  [✓] Bloquer téléchargements exécutables                     ║
║                                                              ║
║  Appliquer? (Y)es / (N)o > [Y]                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
# Protection avancée
Set-MpPreference -DisableRealtimeMonitoring $false
Set-MpPreference -MAPSReporting Advanced
Set-MpPreference -SubmitSamplesConsent SendAllSamples
Set-MpPreference -EnableControlledFolderAccess Enabled
Set-MpPreference -EnableNetworkProtection Enabled
Set-MpPreference -PUAProtection Enabled

# ASR Rules (Block mode)
$ASRRules = @{
    "BE9BA2D9-53EA-4CDC-84E5-9B1EEEE46550" = 1  # Block executable content from email
    "D4F940AB-401B-4EFC-AADC-AD5F3C50688A" = 1  # Block Office child process
    "3B576869-A4EC-4529-8536-B80A7769E899" = 1  # Block Office creating executable
    "75668C1F-73B5-4CF0-BB93-3ECF5CB7CC84" = 1  # Block Office injecting into processes
    "5BEB7EFE-FD9A-4556-801D-275E5FFC04CC" = 1  # Block obfuscated scripts
    "D3E037E1-3EB8-44C8-A917-57927947596D" = 1  # Block JavaScript/VBScript launching
}

foreach ($rule in $ASRRules.GetEnumerator()) {
    Add-MpPreference -AttackSurfaceReductionRules_Ids $rule.Key -AttackSurfaceReductionRules_Actions $rule.Value
}
```

### Étape 3/8: Comptes et Authentification

```
╔══════════════════════════════════════════════════════════════╗
║         WIZARD SECURITY HARDENING - ÉTAPE 3/8                ║
║               Comptes et Authentification                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Politique de mots de passe:                                 ║
║  • Longueur minimale: [14] caractères                        ║
║  • Complexité requise: [✓]                                   ║
║  • Historique: [24] mots de passe                            ║
║  • Âge maximum: [90] jours (0=jamais)                        ║
║                                                              ║
║  Verrouillage compte:                                        ║
║  • Seuil: [5] tentatives                                     ║
║  • Durée: [30] minutes                                       ║
║  • Réinitialisation compteur: [30] minutes                   ║
║                                                              ║
║  Comptes à désactiver:                                       ║
║  [✓] Administrator (intégré)                                 ║
║  [✓] Guest                                                   ║
║  [✓] DefaultAccount                                          ║
║                                                              ║
║  Windows Hello:                                              ║
║  [✓] Activer PIN                                             ║
║  [ ] Activer biométrie (si disponible)                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
# Politique mots de passe (via secedit)
$SecPolicy = @"
[System Access]
MinimumPasswordLength = 14
PasswordComplexity = 1
PasswordHistorySize = 24
MaximumPasswordAge = 90
LockoutBadCount = 5
LockoutDuration = 30
ResetLockoutCount = 30
"@
$SecPolicy | Out-File "$env:TEMP\secpol.inf"
secedit /configure /db "$env:TEMP\secedit.sdb" /cfg "$env:TEMP\secpol.inf" /areas SECURITYPOLICY

# Désactiver comptes intégrés
Disable-LocalUser -Name "Administrator" -ErrorAction SilentlyContinue
Disable-LocalUser -Name "Guest" -ErrorAction SilentlyContinue
Disable-LocalUser -Name "DefaultAccount" -ErrorAction SilentlyContinue
```

### Étape 4/8: Firewall Avancé

```
╔══════════════════════════════════════════════════════════════╗
║         WIZARD SECURITY HARDENING - ÉTAPE 4/8                ║
║                   Firewall Avancé                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Profils firewall:                                           ║
║  ┌──────────────────────────────────────────────────────┐    ║
║  │ Profil    │ Entrant   │ Sortant   │ Log             │    ║
║  ├──────────────────────────────────────────────────────┤    ║
║  │ Domain    │ Block     │ Allow     │ Blocked only    │    ║
║  │ Private   │ Block     │ Allow     │ Blocked only    │    ║
║  │ Public    │ Block     │ Block     │ All             │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                                                              ║
║  Règles à créer:                                             ║
║  [✓] Bloquer LLMNR (UDP 5355)                                ║
║  [✓] Bloquer NetBIOS (UDP 137-138, TCP 139)                  ║
║  [✓] Bloquer SMBv1 (TCP 445 entrant sauf DC)                 ║
║  [✓] Bloquer WinRM public (TCP 5985-5986)                    ║
║                                                              ║
║  Logging:                                                    ║
║  Chemin: [%SystemRoot%\System32\LogFiles\Firewall\]          ║
║  Taille max: [16384] KB                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
# Configuration profils
Set-NetFirewallProfile -Profile Domain -DefaultInboundAction Block -DefaultOutboundAction Allow -LogBlocked True
Set-NetFirewallProfile -Profile Private -DefaultInboundAction Block -DefaultOutboundAction Allow -LogBlocked True
Set-NetFirewallProfile -Profile Public -DefaultInboundAction Block -DefaultOutboundAction Block -LogAllowed True -LogBlocked True

# Bloquer LLMNR
New-NetFirewallRule -DisplayName "Block LLMNR" -Direction Inbound -Protocol UDP -LocalPort 5355 -Action Block

# Bloquer NetBIOS
New-NetFirewallRule -DisplayName "Block NetBIOS-NS" -Direction Inbound -Protocol UDP -LocalPort 137,138 -Action Block
New-NetFirewallRule -DisplayName "Block NetBIOS-SSN" -Direction Inbound -Protocol TCP -LocalPort 139 -Action Block

# Configurer logging
Set-NetFirewallProfile -Profile Domain,Private,Public -LogFileName "%SystemRoot%\System32\LogFiles\Firewall\pfirewall.log" -LogMaxSizeKilobytes 16384
```

### Étape 5/8: Services et Fonctionnalités

```
╔══════════════════════════════════════════════════════════════╗
║         WIZARD SECURITY HARDENING - ÉTAPE 5/8                ║
║               Services et Fonctionnalités                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Services à désactiver (risque sécurité):                    ║
║  [✓] RemoteRegistry - Registre à distance                    ║
║  [✓] lfsvc - Service de localisation                         ║
║  [✓] MapsBroker - Gestionnaire cartes téléchargées           ║
║  [✓] SharedAccess - Partage connexion Internet               ║
║  [✓] WMPNetworkSvc - Partage Windows Media                   ║
║  [✓] XblAuthManager - Xbox Live Auth                         ║
║  [✓] XblGameSave - Xbox Live Game Save                       ║
║                                                              ║
║  Fonctionnalités Windows à désactiver:                       ║
║  [✓] SMB 1.0/CIFS                                            ║
║  [✓] PowerShell 2.0                                          ║
║  [✓] Telnet Client                                           ║
║  [✓] TFTP Client                                             ║
║                                                              ║
║  Désactiver sélection? (Y)es / (N)o > [Y]                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
# Désactiver services
$ServicesToDisable = @(
    "RemoteRegistry",
    "lfsvc", 
    "MapsBroker",
    "SharedAccess",
    "WMPNetworkSvc",
    "XblAuthManager",
    "XblGameSave"
)
foreach ($svc in $ServicesToDisable) {
    Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue
    Set-Service -Name $svc -StartupType Disabled -ErrorAction SilentlyContinue
}

# Désactiver fonctionnalités
Disable-WindowsOptionalFeature -Online -FeatureName "SMB1Protocol" -NoRestart
Disable-WindowsOptionalFeature -Online -FeatureName "MicrosoftWindowsPowerShellV2Root" -NoRestart
Disable-WindowsOptionalFeature -Online -FeatureName "TelnetClient" -NoRestart
Disable-WindowsOptionalFeature -Online -FeatureName "TFTP" -NoRestart
```

### Étape 6/8: BitLocker

```
╔══════════════════════════════════════════════════════════════╗
║         WIZARD SECURITY HARDENING - ÉTAPE 6/8                ║
║                       BitLocker                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Statut TPM: ✅ TPM 2.0 détecté et activé                    ║
║                                                              ║
║  Configuration BitLocker:                                    ║
║  • Algorithme: [XTS-AES 256]                                 ║
║  • Protecteur: TPM + PIN                                     ║
║                                                              ║
║  Volumes à chiffrer:                                         ║
║  [✓] C: (System) - 237 GB - Non chiffré                      ║
║  [ ] D: (Data) - 931 GB - Non chiffré                        ║
║                                                              ║
║  PIN BitLocker (6-20 chiffres): [******]                     ║
║  Confirmer PIN: [******]                                     ║
║                                                              ║
║  Sauvegarde clé de récupération:                             ║
║  (1) Azure AD                                                ║
║  (2) Fichier local (USB recommandé)                          ║
║  (3) Imprimer                                                ║
║  > [2]                                                       ║
║                                                              ║
║  ⚠️  IMPORTANT: Sauvegardez la clé de récupération!          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
# Configurer politique BitLocker (XTS-AES 256)
$BitLockerPolicy = "HKLM:\SOFTWARE\Policies\Microsoft\FVE"
New-Item -Path $BitLockerPolicy -Force | Out-Null
Set-ItemProperty -Path $BitLockerPolicy -Name "EncryptionMethod" -Value 7  # XTS-AES 256
Set-ItemProperty -Path $BitLockerPolicy -Name "UseTPMPIN" -Value 1

# Activer BitLocker sur C:
$PIN = ConvertTo-SecureString "123456" -AsPlainText -Force
Enable-BitLocker -MountPoint "C:" -EncryptionMethod XtsAes256 -Pin $PIN -TPMandPinProtector

# Sauvegarder clé de récupération
$RecoveryKey = (Get-BitLockerVolume -MountPoint "C:").KeyProtector | Where-Object {$_.KeyProtectorType -eq "RecoveryPassword"}
$RecoveryKey.RecoveryPassword | Out-File "F:\BitLocker-Recovery-Key.txt"
```

### Étape 7/8: Audit et Logging

```
╔══════════════════════════════════════════════════════════════╗
║         WIZARD SECURITY HARDENING - ÉTAPE 7/8                ║
║                    Audit et Logging                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Politique d'audit avancée:                                  ║
║                                                              ║
║  Connexion compte:                                           ║
║  [✓] Succès [✓] Échec - Validation identifiants              ║
║  [✓] Succès [✓] Échec - Service authentification Kerberos    ║
║                                                              ║
║  Connexion/Déconnexion:                                      ║
║  [✓] Succès [✓] Échec - Ouverture de session                 ║
║  [ ] Succès [✓] Échec - Fermeture de session                 ║
║  [✓] Succès [✓] Échec - Verrouillage compte                  ║
║                                                              ║
║  Accès objets:                                               ║
║  [ ] Succès [✓] Échec - Système de fichiers                  ║
║  [ ] Succès [✓] Échec - Registre                             ║
║                                                              ║
║  Gestion compte:                                             ║
║  [✓] Succès [✓] Échec - Gestion compte utilisateur           ║
║  [✓] Succès [✓] Échec - Gestion groupe de sécurité           ║
║                                                              ║
║  Changement de stratégie:                                    ║
║  [✓] Succès [✓] Échec - Modification stratégie audit         ║
║  [✓] Succès [✓] Échec - Modification stratégie authent.      ║
║                                                              ║
║  Taille logs Event Viewer:                                   ║
║  • Security: [1048576] KB (1 GB)                             ║
║  • Application: [131072] KB (128 MB)                         ║
║  • System: [131072] KB (128 MB)                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes générées:**
```powershell
# Activer audit avancé
auditpol /set /subcategory:"Credential Validation" /success:enable /failure:enable
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"Account Lockout" /success:enable /failure:enable
auditpol /set /subcategory:"User Account Management" /success:enable /failure:enable
auditpol /set /subcategory:"Security Group Management" /success:enable /failure:enable
auditpol /set /subcategory:"Audit Policy Change" /success:enable /failure:enable
auditpol /set /subcategory:"Authentication Policy Change" /success:enable /failure:enable

# Configurer taille logs
wevtutil sl Security /ms:1073741824
wevtutil sl Application /ms:134217728
wevtutil sl System /ms:134217728
```

### Étape 8/8: Résumé et Rapport

```
╔══════════════════════════════════════════════════════════════╗
║         WIZARD SECURITY HARDENING - ÉTAPE 8/8                ║
║                   Résumé et Rapport                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  MODIFICATIONS APPLIQUÉES:                                   ║
║  ✅ Windows Defender: ASR rules, Network Protection          ║
║  ✅ Comptes: Politique mdp renforcée, comptes désactivés     ║
║  ✅ Firewall: Profils configurés, règles bloquage            ║
║  ✅ Services: 7 services risqués désactivés                  ║
║  ✅ BitLocker: C: chiffré XTS-AES 256 + TPM+PIN              ║
║  ✅ Audit: Politique avancée configurée                      ║
║                                                              ║
║  NOUVEAU SCORE SÉCURITÉ:                                     ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Avant: 54%  ➜  Après: 92%                               │ ║
║  │ ████████████████████████████████████████░░░░            │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ⚠️  ACTIONS MANUELLES REQUISES:                             ║
║  • Sauvegarder clé BitLocker en lieu sûr                     ║
║  • Configurer MFA pour comptes admin                         ║
║  • Planifier audits sécurité réguliers                       ║
║                                                              ║
║  📝 Rapport exporté: C:\Security\hardening-report.html       ║
║  📝 Script exporté: C:\Scripts\security-hardening.ps1        ║
║                                                              ║
║  Redémarrage recommandé. Redémarrer? (Y)es / (N)o > [N]      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🧙 Wizard: Developer Setup (`/win-wizard developer`)

Configuration environnement développeur complet.

### Aperçu des Étapes

| Étape | Description |
|-------|-------------|
| 1/7 | Choix profil développeur (Web, Backend, DevOps, Data, Mobile) |
| 2/7 | Installation outils de base (Git, VS Code, Terminal) |
| 3/7 | Configuration WSL2 et distribution Linux |
| 4/7 | Setup Docker Desktop |
| 5/7 | Installation langages et runtimes |
| 6/7 | Configuration Git et SSH |
| 7/7 | Personnalisation terminal (Oh My Posh, fonts) |

### Profils Disponibles

```
╔══════════════════════════════════════════════════════════════╗
║         WIZARD DEVELOPER SETUP - ÉTAPE 1/7                   ║
║                   Profil Développeur                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Sélectionnez votre profil principal:                        ║
║                                                              ║
║  (1) 🌐 Web Frontend                                         ║
║      Node.js, npm/pnpm, React/Vue, TypeScript                ║
║                                                              ║
║  (2) ⚙️  Backend/API                                         ║
║      Python, Node.js, Docker, PostgreSQL, Redis              ║
║                                                              ║
║  (3) 🔧 DevOps/SRE                                           ║
║      Docker, Kubernetes, Terraform, Ansible, AWS/Azure CLI   ║
║                                                              ║
║  (4) 📊 Data/ML                                              ║
║      Python, Jupyter, pandas, scikit-learn, CUDA             ║
║                                                              ║
║  (5) 📱 Mobile                                               ║
║      Flutter, React Native, Android Studio                   ║
║                                                              ║
║  (6) 🎯 Full Stack (Web + Backend)                           ║
║                                                              ║
║  > [6]                                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🧙 Wizard: Windows Server (`/win-wizard server`)

Configuration Windows Server 2022/2025.

### Aperçu des Étapes

| Étape | Description |
|-------|-------------|
| 1/9 | Type serveur (DC, File, Web, App, Hyper-V) |
| 2/9 | Nom et configuration réseau |
| 3/9 | Rôles et fonctionnalités |
| 4/9 | Configuration stockage |
| 5/9 | Sécurité et hardening |
| 6/9 | Remote management (WinRM, SSH) |
| 7/9 | Monitoring et alerting |
| 8/9 | Backup et recovery |
| 9/9 | Documentation et validation |

---

## 🧙 Wizards Supplémentaires

### `/win-wizard network` - Configuration Réseau (6 étapes)
1. Interfaces et adressage IP
2. DNS et résolution
3. Routage et passerelles
4. VPN configuration
5. Firewall avancé
6. Test et validation

### `/win-wizard backup` - Stratégie Sauvegarde (5 étapes)
1. Inventaire données critiques
2. Choix solution (Windows Backup, Veeam, etc.)
3. Configuration planification
4. Test restauration
5. Documentation procédures

### `/win-wizard domain` - Jonction Domaine AD (6 étapes)
1. Prérequis et validation DNS
2. Informations domaine
3. Compte jonction
4. OU et GPO cible
5. Jonction et redémarrage
6. Validation post-jonction

### `/win-wizard hyperv` - Setup Hyper-V (5 étapes)
1. Activation rôle Hyper-V
2. Configuration réseau virtuel
3. Stockage VMs
4. Paramètres par défaut VMs
5. Première VM test

### `/win-wizard wsl` - Configuration WSL2 (4 étapes)
1. Activation WSL2 et Virtual Machine Platform
2. Installation distribution (Ubuntu, Debian)
3. Configuration utilisateur et sudo
4. Intégration VS Code et Docker

### `/win-wizard remote` - Accès Distant (5 étapes)
1. Configuration RDP sécurisé
2. Setup OpenSSH Server
3. Configuration VPN client/serveur
4. Firewall rules
5. Test et documentation

---

## Utilisation

```powershell
# Lancer un wizard spécifique
/win-wizard setup

# Mode automatique (valeurs par défaut)
/win-wizard security --auto

# Exporter script sans exécuter
/win-wizard developer --export --dry-run

# Aide sur un wizard
/win-wizard server --help
```

## Références

- [Microsoft Security Baselines](https://docs.microsoft.com/windows/security/threat-protection/windows-security-baselines)
- [CIS Benchmarks Windows](https://www.cisecurity.org/benchmark/microsoft_windows_desktop)
- [PowerShell Documentation](https://docs.microsoft.com/powershell)
