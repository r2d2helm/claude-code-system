# Wizard: Remote Access Setup

Configuration accès distant sécurisé Windows 11/Server 2025.

## Déclenchement

```
/win-wizard remote-access
```

## Étapes du Wizard (5)

### Étape 1: Type d'Accès

```
╔══════════════════════════════════════════════════════════════╗
║           🔐 WIZARD REMOTE ACCESS                            ║
║               Étape 1/5 : Type d'Accès                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Quel type d'accès distant configurer ?                      ║
║                                                              ║
║  [1] RDP (Remote Desktop) - Bureau à distance                ║
║  [2] SSH - Ligne de commande sécurisée                       ║
║  [3] VPN - Accès réseau complet                              ║
║  [4] WinRM/PowerShell Remoting                               ║
║  [5] Configuration complète (tous)                           ║
║                                                              ║
║  État actuel:                                                ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ RDP      : ⚠️ Activé (NLA désactivé - non sécurisé)     │ ║
║  │ SSH      : ❌ Non installé                              │ ║
║  │ WinRM    : ❌ Désactivé                                 │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 2: Configuration RDP Sécurisé

```
╔══════════════════════════════════════════════════════════════╗
║           🔐 WIZARD REMOTE ACCESS                            ║
║                Étape 2/5 : RDP Sécurisé                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🖥️ CONFIGURATION RDP SÉCURISÉE:                             ║
║                                                              ║
║  [x] Activer Remote Desktop                                  ║
║  [x] Exiger NLA (Network Level Authentication)               ║
║  [x] Niveau de chiffrement : Élevé                           ║
║  [x] Limiter aux utilisateurs spécifiques                    ║
║  [ ] Changer le port (3389 → personnalisé)                   ║
║  [x] Activer règles firewall                                 ║
║                                                              ║
║  Utilisateurs autorisés:                                     ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ • Administrators (groupe)                               │ ║
║  │ + Ajouter: ________________________________             │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Appliquer  [2] Avancé  [3] Suivant                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes RDP:**
```powershell
# Activer RDP
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0

# Exiger NLA
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "UserAuthentication" -Value 1

# Niveau de chiffrement élevé
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "MinEncryptionLevel" -Value 3

# Activer firewall RDP
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"

# Ajouter utilisateur au groupe Remote Desktop Users
Add-LocalGroupMember -Group "Remote Desktop Users" -Member "domain\user"

# Changer port (optionnel)
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "PortNumber" -Value 3390
New-NetFirewallRule -DisplayName "RDP Custom Port" -Direction Inbound -LocalPort 3390 -Protocol TCP -Action Allow
```

### Étape 3: Configuration SSH

```
╔══════════════════════════════════════════════════════════════╗
║           🔐 WIZARD REMOTE ACCESS                            ║
║                 Étape 3/5 : SSH Server                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔑 CONFIGURATION OPENSSH SERVER:                            ║
║                                                              ║
║  [x] Installer OpenSSH Server                                ║
║  [x] Démarrage automatique                                   ║
║  [x] Authentification par clé (recommandé)                   ║
║  [ ] Désactiver authentification mot de passe                ║
║  [x] Configurer firewall (port 22)                           ║
║                                                              ║
║  Shell par défaut:                                           ║
║  [1] PowerShell 7 (recommandé)                               ║
║  [2] PowerShell 5.1                                          ║
║  [3] CMD                                                     ║
║                                                              ║
║  Clé publique à autoriser (optionnel):                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ssh-ed25519 AAAA...______________________________       │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes SSH:**
```powershell
# Installer OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Démarrer et configurer démarrage auto
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic

# Firewall
New-NetFirewallRule -Name "SSH" -DisplayName "OpenSSH Server" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22

# Shell par défaut PowerShell 7
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\Program Files\PowerShell\7\pwsh.exe" -PropertyType String -Force

# Ajouter clé publique (pour admin)
$AuthKeysPath = "$env:ProgramData\ssh\administrators_authorized_keys"
"ssh-ed25519 AAAA..." | Add-Content $AuthKeysPath
icacls $AuthKeysPath /inheritance:r /grant "Administrators:F" /grant "SYSTEM:F"
```

### Étape 4: WinRM/PowerShell Remoting

```
╔══════════════════════════════════════════════════════════════╗
║           🔐 WIZARD REMOTE ACCESS                            ║
║               Étape 4/5 : WinRM                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ⚡ CONFIGURATION WINRM:                                     ║
║                                                              ║
║  [x] Activer WinRM                                           ║
║  [x] Configurer HTTPS (certificat auto-signé)                ║
║  [x] Authentification Kerberos (domaine)                     ║
║  [ ] Authentification Basic (non recommandé)                 ║
║  [x] Trusted Hosts (pour workgroup)                          ║
║                                                              ║
║  Trusted Hosts:                                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 192.168.1.*, admin-pc.local_________________________    │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  [1] Configuration rapide  [2] Configuration HTTPS           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes WinRM:**
```powershell
# Configuration rapide
Enable-PSRemoting -Force

# Configurer Trusted Hosts
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "192.168.1.*,admin-pc.local" -Force

# Configuration HTTPS
$Cert = New-SelfSignedCertificate -DnsName $env:COMPUTERNAME -CertStoreLocation Cert:\LocalMachine\My
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * -CertificateThumbPrint $Cert.Thumbprint -Force

# Firewall HTTPS
New-NetFirewallRule -DisplayName "WinRM HTTPS" -Direction Inbound -LocalPort 5986 -Protocol TCP -Action Allow

# Tester
Test-WSMan -ComputerName localhost
```

### Étape 5: Résumé et Test

```
╔══════════════════════════════════════════════════════════════╗
║           🔐 WIZARD REMOTE ACCESS                            ║
║               Étape 5/5 : Validation                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✅ CONFIGURATION TERMINÉE:                                   ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✓ RDP          : Port 3389, NLA activé                  │ ║
║  │ ✓ SSH          : Port 22, clé + mot de passe            │ ║
║  │ ✓ WinRM HTTP   : Port 5985                              │ ║
║  │ ✓ WinRM HTTPS  : Port 5986                              │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  🧪 TESTS:                                                   ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✅ RDP listener     : Actif                             │ ║
║  │ ✅ SSH daemon       : Running                           │ ║
║  │ ✅ WinRM service    : Running                           │ ║
║  │ ✅ Firewall rules   : Configurées                       │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📋 Commandes de connexion:                                  ║
║  RDP   : mstsc /v:192.168.1.50                               ║
║  SSH   : ssh user@192.168.1.50                               ║
║  PS    : Enter-PSSession -ComputerName 192.168.1.50          ║
║                                                              ║
║  [1] Terminer  [2] Exporter configuration                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
