# Wizard: Network Setup Windows

Configuration réseau entreprise Windows 11/Server 2025.

## Déclenchement

```
/win-wizard network
```

## Étapes du Wizard (5)

### Étape 1: Détection Adaptateurs

```
╔══════════════════════════════════════════════════════════════╗
║           🌐 WIZARD NETWORK SETUP                            ║
║                Étape 1/5 : Adaptateurs                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📡 ADAPTATEURS DÉTECTÉS:                                    ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ [1] Ethernet (Intel I225-V) - Connecté                  │ ║
║  │     MAC: 00:1A:2B:3C:4D:5E | Speed: 1 Gbps              │ ║
║  │                                                         │ ║
║  │ [2] Wi-Fi (Intel AX211) - Déconnecté                    │ ║
║  │     MAC: 00:1A:2B:3C:4D:5F                              │ ║
║  │                                                         │ ║
║  │ [3] vEthernet (WSL) - Connecté                          │ ║
║  │     MAC: 00:15:5D:XX:XX:XX | Virtual                    │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Sélectionnez l'adaptateur à configurer: [1-3]               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, MacAddress, LinkSpeed | Format-Table
```

### Étape 2: Configuration IP

```
╔══════════════════════════════════════════════════════════════╗
║           🌐 WIZARD NETWORK SETUP                            ║
║                  Étape 2/5 : Adresse IP                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Type de configuration :                                     ║
║                                                              ║
║  [1] DHCP automatique                                        ║
║  [2] IP Statique                                             ║
║                                                              ║
║  Si IP Statique, entrez:                                     ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Adresse IP    : 192.168.1.___                           │ ║
║  │ Masque (CIDR) : /24                                     │ ║
║  │ Passerelle    : 192.168.1.1                             │ ║
║  │ DNS primaire  : 8.8.8.8                                 │ ║
║  │ DNS secondaire: 8.8.4.4                                 │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# DHCP
Set-NetIPInterface -InterfaceAlias "Ethernet" -Dhcp Enabled
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ResetServerAddresses

# IP Statique
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress "192.168.1.50" -PrefixLength 24 -DefaultGateway "192.168.1.1"
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses "8.8.8.8","8.8.4.4"
```

### Étape 3: Configuration DNS

```
╔══════════════════════════════════════════════════════════════╗
║           🌐 WIZARD NETWORK SETUP                            ║
║                   Étape 3/5 : DNS                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Configuration DNS :                                         ║
║                                                              ║
║  [1] DNS Public (Google: 8.8.8.8, 8.8.4.4)                  ║
║  [2] DNS Public (Cloudflare: 1.1.1.1, 1.0.0.1)              ║
║  [3] DNS Entreprise (Active Directory)                       ║
║  [4] DNS Personnalisé                                        ║
║                                                              ║
║  Options avancées:                                           ║
║  [x] Activer DNS over HTTPS (DoH)                            ║
║  [ ] Désactiver résolution multicast (LLMNR)                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes DoH:**
```powershell
# Activer DNS over HTTPS
Set-DnsClientDohServerAddress -ServerAddress "8.8.8.8" -DohTemplate "https://dns.google/dns-query" -AllowFallbackToUdp $false
Set-DnsClientDohServerAddress -ServerAddress "1.1.1.1" -DohTemplate "https://cloudflare-dns.com/dns-query" -AllowFallbackToUdp $false

# Désactiver LLMNR
New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" -Name "EnableMulticast" -Value 0 -PropertyType DWORD -Force
```

### Étape 4: Profil Réseau

```
╔══════════════════════════════════════════════════════════════╗
║           🌐 WIZARD NETWORK SETUP                            ║
║                Étape 4/5 : Profil Réseau                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Profil réseau actuel : Public                               ║
║                                                              ║
║  [1] Privé (Home/Work) - Découverte activée                  ║
║  [2] Domaine - Géré par GPO                                  ║
║  [3] Public - Maximum sécurité                               ║
║                                                              ║
║  Options partage:                                            ║
║  [ ] Découverte réseau                                       ║
║  [ ] Partage fichiers et imprimantes                         ║
║  [ ] Partage dossier public                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Définir profil Privé
Set-NetConnectionProfile -InterfaceAlias "Ethernet" -NetworkCategory Private

# Activer découverte réseau (profil privé)
Set-NetFirewallRule -DisplayGroup "Network Discovery" -Enabled True -Profile Private

# Activer partage fichiers
Set-NetFirewallRule -DisplayGroup "File and Printer Sharing" -Enabled True -Profile Private
```

### Étape 5: Test et Validation

```
╔══════════════════════════════════════════════════════════════╗
║           🌐 WIZARD NETWORK SETUP                            ║
║               Étape 5/5 : Validation                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🧪 TESTS DE CONNECTIVITÉ:                                   ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✅ Passerelle (192.168.1.1)    : OK (1ms)               │ ║
║  │ ✅ DNS (8.8.8.8)               : OK (15ms)              │ ║
║  │ ✅ Internet (google.com)       : OK (25ms)              │ ║
║  │ ✅ Résolution DNS              : OK                     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📋 CONFIGURATION FINALE:                                    ║
║  IP: 192.168.1.50/24 | GW: 192.168.1.1                       ║
║  DNS: 8.8.8.8, 8.8.4.4 (DoH activé)                          ║
║  Profil: Privé | Découverte: Activée                         ║
║                                                              ║
║  [1] Terminer  [2] Exporter config  [3] Recommencer          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes test:**
```powershell
# Tests connectivité
Test-NetConnection -ComputerName 192.168.1.1 -InformationLevel Quiet
Test-NetConnection -ComputerName 8.8.8.8 -InformationLevel Quiet
Test-NetConnection -ComputerName google.com -InformationLevel Quiet
Resolve-DnsName google.com

# Exporter configuration
Get-NetIPConfiguration | Out-File "$env:USERPROFILE\Desktop\network-config.txt"
```
