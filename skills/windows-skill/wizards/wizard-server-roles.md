# Wizard: Server Roles Installation

Installation rôles Windows Server 2022/2025.

## Déclenchement

```
/win-wizard server-roles
```

## Étapes du Wizard (5)

### Étape 1: Détection Serveur

```
╔══════════════════════════════════════════════════════════════╗
║           🖥️ WIZARD SERVER ROLES                             ║
║                Étape 1/5 : Détection                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📋 SERVEUR DÉTECTÉ:                                         ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ OS      : Windows Server 2025 Standard                  │ ║
║  │ Édition : Standard (GUI)                                │ ║
║  │ Licence : Activée                                       │ ║
║  │ Cores   : 8 | RAM : 32 GB | Disque : 500 GB            │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Rôles actuellement installés:                               ║
║  • File and Storage Services                                 ║
║                                                              ║
║  [1] Continuer avec l'installation de rôles                  ║
║  [2] Voir les fonctionnalités installées                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
Get-WindowsFeature | Where-Object Installed -eq $true
Get-ComputerInfo | Select-Object WindowsProductName, WindowsEditionId
```

### Étape 2: Sélection Rôles

```
╔══════════════════════════════════════════════════════════════╗
║           🖥️ WIZARD SERVER ROLES                             ║
║                Étape 2/5 : Sélection                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Sélectionnez les rôles à installer:                         ║
║                                                              ║
║  Infrastructure:                                             ║
║  [ ] Active Directory Domain Services (AD DS)                ║
║  [ ] DNS Server                                              ║
║  [ ] DHCP Server                                             ║
║  [ ] File Server (avec DFS)                                  ║
║                                                              ║
║  Applications:                                               ║
║  [ ] Web Server (IIS)                                        ║
║  [ ] Remote Desktop Services                                 ║
║  [ ] Windows Server Update Services (WSUS)                   ║
║  [ ] Hyper-V                                                 ║
║                                                              ║
║  Sécurité:                                                   ║
║  [ ] Active Directory Certificate Services                   ║
║  [ ] Network Policy and Access Services                      ║
║                                                              ║
║  [1-10] Toggle sélection  [A] Tout  [C] Continuer            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 3: Configuration Rôle

```
╔══════════════════════════════════════════════════════════════╗
║           🖥️ WIZARD SERVER ROLES                             ║
║              Étape 3/5 : Configuration                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔧 CONFIGURATION: Active Directory Domain Services          ║
║                                                              ║
║  Type de déploiement:                                        ║
║  [1] Nouveau contrôleur dans forêt existante                 ║
║  [2] Nouvelle forêt (premier DC)                             ║
║  [3] Nouveau domaine enfant                                  ║
║                                                              ║
║  Si nouvelle forêt:                                          ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Nom de domaine : corp.local_____________________        │ ║
║  │ Niveau fonctionnel : Windows Server 2025                │ ║
║  │ Mot de passe DSRM : ****************************        │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes AD DS:**
```powershell
# Installer le rôle AD DS
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools

# Promouvoir en DC (nouvelle forêt)
Install-ADDSForest `
    -DomainName "corp.local" `
    -DomainNetbiosName "CORP" `
    -ForestMode "WinThreshold" `
    -DomainMode "WinThreshold" `
    -InstallDns:$true `
    -SafeModeAdministratorPassword (ConvertTo-SecureString "P@ssw0rd!" -AsPlainText -Force) `
    -Force
```

### Étape 4: Installation

```
╔══════════════════════════════════════════════════════════════╗
║           🖥️ WIZARD SERVER ROLES                             ║
║              Étape 4/5 : Installation                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📦 INSTALLATION EN COURS...                                 ║
║                                                              ║
║  [██████████████░░░░░░░░░░░░░░░░] 45%                        ║
║                                                              ║
║  Rôles:                                                      ║
║  ✅ AD-Domain-Services                    Installé           ║
║  🔄 DNS                                   En cours...        ║
║  ⏳ DHCP                                  En attente         ║
║                                                              ║
║  Fonctionnalités:                                            ║
║  ✅ RSAT-AD-Tools                         Installé           ║
║  ✅ RSAT-DNS-Server                       Installé           ║
║                                                              ║
║  ⚠️ Un redémarrage sera nécessaire                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes installation batch:**
```powershell
# Installer plusieurs rôles
$Roles = @(
    "AD-Domain-Services",
    "DNS",
    "DHCP",
    "Web-Server"
)

foreach ($Role in $Roles) {
    Write-Host "Installation de $Role..."
    Install-WindowsFeature -Name $Role -IncludeManagementTools -Verbose
}
```

### Étape 5: Post-Installation

```
╔══════════════════════════════════════════════════════════════╗
║           🖥️ WIZARD SERVER ROLES                             ║
║             Étape 5/5 : Post-Installation                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✅ INSTALLATION TERMINÉE:                                    ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✓ AD-Domain-Services (promotion requise)                │ ║
║  │ ✓ DNS Server                                            │ ║
║  │ ✓ DHCP Server (autorisation requise)                    │ ║
║  │ ✓ Web Server (IIS)                                      │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ⚠️ ACTIONS POST-INSTALLATION REQUISES:                      ║
║  • Promouvoir ce serveur en contrôleur de domaine           ║
║  • Autoriser le serveur DHCP dans AD                         ║
║  • Configurer les étendues DHCP                              ║
║  • Configurer les sites IIS                                  ║
║                                                              ║
║  [1] Lancer assistant promotion AD DS                        ║
║  [2] Redémarrer maintenant                                   ║
║  [3] Exporter rapport et terminer                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes post-install:**
```powershell
# Autoriser DHCP dans AD
Add-DhcpServerInDC -DnsName "dc01.corp.local" -IPAddress "192.168.1.10"

# Configurer étendue DHCP
Add-DhcpServerv4Scope -Name "LAN" -StartRange 192.168.1.100 -EndRange 192.168.1.200 -SubnetMask 255.255.255.0 -LeaseDuration 8.00:00:00
Set-DhcpServerv4OptionValue -ScopeId 192.168.1.0 -Router 192.168.1.1 -DnsServer 192.168.1.10

# Rapport installation
Get-WindowsFeature | Where-Object Installed | Export-Csv "C:\roles-installed.csv"
```
