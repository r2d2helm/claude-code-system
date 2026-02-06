# Wizard: Troubleshooting Guide

Diagnostic et résolution de problèmes Windows 11/Server 2025.

## Déclenchement

```
/win-wizard troubleshoot
```

## Étapes du Wizard (5)

### Étape 1: Catégorie de Problème

```
╔══════════════════════════════════════════════════════════════╗
║           🔧 WIZARD TROUBLESHOOTING                          ║
║               Étape 1/5 : Catégorie                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Quel type de problème rencontrez-vous ?                     ║
║                                                              ║
║  [1] 🖥️  Démarrage / Boot                                    ║
║  [2] 🌐 Réseau / Internet                                    ║
║  [3] 💾 Disque / Stockage                                    ║
║  [4] 🔵 Écran bleu (BSOD)                                    ║
║  [5] ⚡ Performances lentes                                   ║
║  [6] 🔊 Audio / Son                                          ║
║  [7] 🖨️  Imprimante                                          ║
║  [8] 🔄 Windows Update                                       ║
║  [9] 🔐 Authentification / Login                             ║
║  [10] 📦 Application qui plante                              ║
║                                                              ║
║  [0] Diagnostic automatique complet                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 2: Diagnostic Automatique

```
╔══════════════════════════════════════════════════════════════╗
║           🔧 WIZARD TROUBLESHOOTING                          ║
║             Étape 2/5 : Diagnostic                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔍 DIAGNOSTIC RÉSEAU EN COURS...                            ║
║                                                              ║
║  [████████████████████████░░░░░░] 80%                        ║
║                                                              ║
║  Tests effectués:                                            ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✅ Adaptateur réseau        : Actif                     │ ║
║  │ ✅ Adresse IP               : 192.168.1.50              │ ║
║  │ ✅ Passerelle               : Accessible                │ ║
║  │ ❌ DNS                      : Timeout                   │ ║
║  │ ⚠️  Internet                : Échec résolution          │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  🎯 PROBLÈME IDENTIFIÉ:                                      ║
║  Configuration DNS incorrecte ou serveur DNS injoignable     ║
║                                                              ║
║  [1] Voir solutions recommandées                             ║
║  [2] Diagnostic avancé                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes diagnostic réseau:**
```powershell
# Diagnostic complet réseau
$Results = @{
    Adapter = Get-NetAdapter | Where-Object Status -eq "Up"
    IP = Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*"}
    Gateway = Test-NetConnection -ComputerName (Get-NetRoute -DestinationPrefix "0.0.0.0/0").NextHop -InformationLevel Quiet
    DNS = Test-NetConnection -ComputerName 8.8.8.8 -Port 53 -InformationLevel Quiet
    Internet = Test-NetConnection -ComputerName google.com -InformationLevel Quiet
}
$Results

# Test DNS spécifique
Resolve-DnsName google.com -DnsOnly -ErrorAction SilentlyContinue
nslookup google.com
```

### Étape 3: Solutions Recommandées

```
╔══════════════════════════════════════════════════════════════╗
║           🔧 WIZARD TROUBLESHOOTING                          ║
║              Étape 3/5 : Solutions                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  💡 SOLUTIONS RECOMMANDÉES (par ordre de probabilité):       ║
║                                                              ║
║  [1] 🔄 Réinitialiser la configuration DNS                   ║
║      Succès estimé: 75%                                      ║
║      → Flush DNS cache et reconfigurer serveurs              ║
║                                                              ║
║  [2] 🔌 Réinitialiser la pile TCP/IP                         ║
║      Succès estimé: 60%                                      ║
║      → Reset complet Winsock et TCP/IP                       ║
║                                                              ║
║  [3] 🔧 Réinstaller le pilote réseau                         ║
║      Succès estimé: 40%                                      ║
║      → Désinstaller et réinstaller l'adaptateur              ║
║                                                              ║
║  [4] 📞 Contacter l'administrateur réseau                    ║
║      → Problème potentiel côté infrastructure                ║
║                                                              ║
║  Appliquer quelle solution ? [1-4] ou [A] pour toutes        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes solutions:**
```powershell
# Solution 1: Reset DNS
ipconfig /flushdns
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses "8.8.8.8","8.8.4.4"
ipconfig /registerdns

# Solution 2: Reset TCP/IP
netsh winsock reset
netsh int ip reset
netsh interface ipv4 reset
netsh interface ipv6 reset

# Solution 3: Réinstaller pilote
$Adapter = Get-NetAdapter | Where-Object Status -eq "Up" | Select-Object -First 1
Disable-NetAdapter -Name $Adapter.Name -Confirm:$false
Enable-NetAdapter -Name $Adapter.Name

# Ou réinstallation complète via Device Manager
pnputil /scan-devices
```

### Étape 4: Vérification

```
╔══════════════════════════════════════════════════════════════╗
║           🔧 WIZARD TROUBLESHOOTING                          ║
║             Étape 4/5 : Vérification                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🧪 VÉRIFICATION APRÈS CORRECTION...                         ║
║                                                              ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✅ DNS Cache         : Vidé                             │ ║
║  │ ✅ Serveurs DNS      : 8.8.8.8, 8.8.4.4                 │ ║
║  │ ✅ Résolution DNS    : google.com → 142.250.x.x         │ ║
║  │ ✅ Ping Internet     : OK (25ms)                        │ ║
║  │ ✅ Navigation Web    : OK                               │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  ✅ PROBLÈME RÉSOLU!                                         ║
║                                                              ║
║  Le problème était causé par:                                ║
║  → Cache DNS corrompu avec entrées invalides                 ║
║                                                              ║
║  [1] Terminer  [2] Créer point de restauration               ║
║  [3] Exporter rapport diagnostic                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Étape 5: Rapport et Prévention

```
╔══════════════════════════════════════════════════════════════╗
║           🔧 WIZARD TROUBLESHOOTING                          ║
║             Étape 5/5 : Rapport                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📋 RAPPORT DE DIAGNOSTIC:                                   ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Date       : 2026-02-03 19:45                           │ ║
║  │ Catégorie  : Réseau                                     │ ║
║  │ Problème   : Pas d'accès Internet                       │ ║
║  │ Cause      : Cache DNS corrompu                         │ ║
║  │ Solution   : Flush DNS + reconfiguration                │ ║
║  │ Statut     : RÉSOLU                                     │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  🛡️ PRÉVENTION:                                              ║
║  • Planifier flush DNS hebdomadaire                          ║
║  • Configurer DNS secondaire fiable                          ║
║  • Activer DNS over HTTPS                                    ║
║                                                              ║
║  [1] Appliquer mesures préventives                           ║
║  [2] Exporter rapport (PDF)                                  ║
║  [3] Terminer                                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes rapport:**
```powershell
# Générer rapport diagnostic
$Report = @"
# Rapport Diagnostic Windows
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm")
Ordinateur: $env:COMPUTERNAME

## Problème
Catégorie: Réseau
Description: Pas d'accès Internet

## Diagnostic
- Adaptateur: OK
- IP: OK  
- Passerelle: OK
- DNS: ÉCHEC

## Solution appliquée
- Flush DNS cache
- Reconfiguration serveurs DNS (8.8.8.8, 8.8.4.4)

## Résultat
PROBLÈME RÉSOLU

## Recommandations
- Planifier maintenance DNS
- Configurer DNS over HTTPS
"@

$Report | Out-File "$env:USERPROFILE\Desktop\diagnostic-report.md"

# Tâche préventive
$Action = New-ScheduledTaskAction -Execute "ipconfig" -Argument "/flushdns"
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 4am
Register-ScheduledTask -TaskName "Weekly DNS Flush" -Action $Action -Trigger $Trigger
```

## Diagnostics Rapides par Catégorie

### BSOD (Écran Bleu)
```powershell
# Analyser minidumps
Get-ChildItem C:\Windows\Minidump\*.dmp | Sort-Object LastWriteTime -Descending | Select-Object -First 5

# Event Viewer erreurs critiques
Get-WinEvent -FilterHashtable @{LogName='System';Level=1,2} -MaxEvents 20 | Format-List
```

### Windows Update
```powershell
# Diagnostic Windows Update
Get-WindowsUpdateLog
DISM /Online /Cleanup-Image /CheckHealth
sfc /scannow
```

### Performances
```powershell
# Rapport performances
perfmon /report
```
