# Wizard: Setup Initial Windows

Assistant interactif pour configuration post-installation Windows 11/Server 2025.

## Déclenchement

```
/win-wizard setup
```

## Étapes du Wizard (8)

### Étape 1: Informations Système

```
╔══════════════════════════════════════════════════════════════╗
║           🖥️  WIZARD SETUP INITIAL WINDOWS                   ║
║                    Étape 1/8 : Système                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📋 SYSTÈME DÉTECTÉ:                                         ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ OS        : Windows 11 Pro 23H2                         │ ║
║  │ Hostname  : DESKTOP-ABC123                              │ ║
║  │ CPU       : Intel Core i7-12700K                        │ ║
║  │ RAM       : 32 GB                                       │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Souhaitez-vous renommer cet ordinateur ?                    ║
║                                                              ║
║  [1] Oui, définir un nouveau nom                             ║
║  [2] Non, garder le nom actuel                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Renommer l'ordinateur
Rename-Computer -NewName "WORKSTATION-01" -Force -Restart
```

### Étape 2: Configuration Réseau

```
╔══════════════════════════════════════════════════════════════╗
║                   Étape 2/8 : Réseau                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [1] DHCP (automatique)                                      ║
║  [2] IP Statique                                             ║
║  [3] Garder configuration actuelle                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes IP Statique:**
```powershell
$Adapter = Get-NetAdapter | Where-Object Status -eq "Up" | Select-Object -First 1
New-NetIPAddress -InterfaceIndex $Adapter.ifIndex -IPAddress "192.168.1.50" -PrefixLength 24 -DefaultGateway "192.168.1.1"
Set-DnsClientServerAddress -InterfaceIndex $Adapter.ifIndex -ServerAddresses "8.8.8.8","8.8.4.4"
```

### Étape 3: Windows Update

```
╔══════════════════════════════════════════════════════════════╗
║                 Étape 3/8 : Mises à jour                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [1] Installer toutes les mises à jour                       ║
║  [2] Télécharger sans installer                              ║
║  [3] Passer                                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
Install-Module PSWindowsUpdate -Force
Get-WindowsUpdate -AcceptAll -Install -AutoReboot
```

### Étape 4: Compte Administrateur

```
╔══════════════════════════════════════════════════════════════╗
║                Étape 4/8 : Compte Admin                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [1] Créer nouveau compte admin                              ║
║  [2] Renommer Administrator                                  ║
║  [3] Passer                                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
$Password = Read-Host -AsSecureString "Mot de passe"
New-LocalUser -Name "localadmin" -Password $Password -PasswordNeverExpires
Add-LocalGroupMember -Group "Administrators" -Member "localadmin"
```

### Étape 5: PowerShell 7

```
╔══════════════════════════════════════════════════════════════╗
║                Étape 5/8 : PowerShell                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [1] Installer PowerShell 7 + modules                        ║
║  [2] Configurer Execution Policy                             ║
║  [3] Passer                                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
winget install Microsoft.PowerShell
Set-ExecutionPolicy RemoteSigned -Scope LocalMachine -Force
Install-Module PSReadLine, Terminal-Icons, posh-git -Force
```

### Étape 6: Outils Essentiels

```
╔══════════════════════════════════════════════════════════════╗
║                  Étape 6/8 : Outils                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [x] Windows Terminal    [x] 7-Zip                           ║
║  [x] Notepad++           [ ] VS Code                         ║
║  [ ] Git                 [ ] Python                          ║
║  [x] Sysinternals                                            ║
║                                                              ║
║  [1] Installer sélection  [2] Tout  [3] Passer               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
$Apps = @("Microsoft.WindowsTerminal","7zip.7zip","Notepad++.Notepad++","Microsoft.Sysinternals")
$Apps | ForEach-Object { winget install $_ --silent }
```

### Étape 7: Sécurité de Base

```
╔══════════════════════════════════════════════════════════════╗
║                 Étape 7/8 : Sécurité                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✓ Activer Windows Defender temps réel                       ║
║  ✓ Activer Firewall tous profils                             ║
║  ✓ Désactiver SMBv1                                          ║
║  ✓ Configurer UAC                                            ║
║                                                              ║
║  [1] Appliquer tout  [2] Configurer  [3] Passer              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
Set-MpPreference -DisableRealtimeMonitoring $false
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart
```

### Étape 8: Finalisation

```
╔══════════════════════════════════════════════════════════════╗
║               Étape 8/8 : Finalisation                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✅ RÉSUMÉ:                                                   ║
║  ✓ Ordinateur renommé                                        ║
║  ✓ Réseau configuré                                          ║
║  ✓ Mises à jour installées                                   ║
║  ✓ Compte admin créé                                         ║
║  ✓ PowerShell 7 installé                                     ║
║  ✓ Outils installés                                          ║
║  ✓ Sécurité appliquée                                        ║
║                                                              ║
║  [1] Redémarrer  [2] Plus tard  [3] Exporter rapport         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
