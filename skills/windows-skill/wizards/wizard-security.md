# Wizard: Security Hardening Windows

Assistant interactif pour sécurisation avancée Windows 11/Server 2025.

## Déclenchement

```
/win-wizard security
```

## Étapes du Wizard (6)

### Étape 1: Audit Sécurité Initial

```
╔══════════════════════════════════════════════════════════════╗
║           🔒 WIZARD SECURITY HARDENING                       ║
║                 Étape 1/6 : Audit Initial                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔍 ANALYSE DE SÉCURITÉ EN COURS...                          ║
║                                                              ║
║  RÉSULTATS:                                                  ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Windows Defender    : ✅ Actif                          │ ║
║  │ Firewall            : ⚠️  Profil Public désactivé       │ ║
║  │ BitLocker           : ❌ Non configuré                  │ ║
║  │ SMBv1               : ❌ Activé (vulnérable)            │ ║
║  │ UAC                 : ⚠️  Niveau bas                    │ ║
║  │ Credential Guard    : ❌ Désactivé                      │ ║
║  │ RDP                 : ⚠️  Activé sans NLA               │ ║
║  │ Comptes Guest       : ✅ Désactivé                      │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Score sécurité: 45/100 ██████░░░░░░░░░░░░░░                 ║
║                                                              ║
║  [1] Continuer avec les recommandations                      ║
║  [2] Exporter le rapport d'audit                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes audit:**
```powershell
# Script d'audit complet
$Audit = @{
    Defender = (Get-MpComputerStatus).RealTimeProtectionEnabled
    Firewall = (Get-NetFirewallProfile | Where Enabled -eq $false).Count -eq 0
    BitLocker = (Get-BitLockerVolume -MountPoint "C:").ProtectionStatus -eq "On"
    SMBv1 = (Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol).State -eq "Enabled"
    UAC = (Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System).ConsentPromptBehaviorAdmin
    CredGuard = (Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard).SecurityServicesRunning -contains 1
}
```

### Étape 2: Windows Defender Avancé

```
╔══════════════════════════════════════════════════════════════╗
║           🔒 WIZARD SECURITY HARDENING                       ║
║               Étape 2/6 : Windows Defender                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🛡️ CONFIGURATION DEFENDER RECOMMANDÉE:                      ║
║                                                              ║
║  [x] Protection temps réel                                   ║
║  [x] Protection cloud (MAPS)                                 ║
║  [x] Soumission automatique échantillons                     ║
║  [x] Protection contre falsification                         ║
║  [x] Analyse comportementale                                 ║
║  [x] Protection réseau                                       ║
║  [ ] Controlled Folder Access (peut bloquer apps)            ║
║  [x] Attack Surface Reduction (ASR) rules                    ║
║                                                              ║
║  [1] Appliquer configuration recommandée                     ║
║  [2] Configuration personnalisée                             ║
║  [3] Passer                                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Configuration Defender avancée
Set-MpPreference -DisableRealtimeMonitoring $false
Set-MpPreference -MAPSReporting Advanced
Set-MpPreference -SubmitSamplesConsent SendAllSamples
Set-MpPreference -DisableTamperProtection $false
Set-MpPreference -DisableBehaviorMonitoring $false
Set-MpPreference -EnableNetworkProtection Enabled

# ASR Rules (Attack Surface Reduction)
$ASRRules = @{
    "BE9BA2D9-53EA-4CDC-84E5-9B1EEEE46550" = 1  # Block executable from email
    "D4F940AB-401B-4EFC-AADC-AD5F3C50688A" = 1  # Block Office child processes
    "3B576869-A4EC-4529-8536-B80A7769E899" = 1  # Block Office from creating executables
    "75668C1F-73B5-4CF0-BB93-3ECF5CB7CC84" = 1  # Block Office injection
    "D3E037E1-3EB8-44C8-A917-57927947596D" = 1  # Block JS/VBS launching executables
    "5BEB7EFE-FD9A-4556-801D-275E5FFC04CC" = 1  # Block obfuscated scripts
    "92E97FA1-2EDF-4476-BDD6-9DD0B4DDDC7B" = 1  # Block Win32 from macros
}
foreach ($Rule in $ASRRules.GetEnumerator()) {
    Add-MpPreference -AttackSurfaceReductionRules_Ids $Rule.Key -AttackSurfaceReductionRules_Actions $Rule.Value
}
```

### Étape 3: BitLocker

```
╔══════════════════════════════════════════════════════════════╗
║           🔒 WIZARD SECURITY HARDENING                       ║
║                 Étape 3/6 : BitLocker                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  💾 ÉTAT BITLOCKER:                                          ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ C: (System)  : Non chiffré                              │ ║
║  │ D: (Data)    : Non chiffré                              │ ║
║  │ TPM          : ✅ Version 2.0 présent                   │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Mode de protection :                                        ║
║                                                              ║
║  [1] TPM seul (démarrage automatique)                        ║
║  [2] TPM + PIN (recommandé haute sécurité)                   ║
║  [3] TPM + clé USB                                           ║
║  [4] Ne pas configurer BitLocker                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes TPM+PIN:**
```powershell
# Activer BitLocker avec TPM + PIN
$PIN = Read-Host "Entrez le PIN BitLocker (6-20 chiffres)" -AsSecureString
Enable-BitLocker -MountPoint "C:" -EncryptionMethod XtsAes256 -TpmAndPinProtector -Pin $PIN

# Sauvegarder la clé de récupération
$RecoveryKey = (Get-BitLockerVolume -MountPoint "C:").KeyProtector | Where-Object {$_.KeyProtectorType -eq "RecoveryPassword"}
$RecoveryKey.RecoveryPassword | Out-File "$env:USERPROFILE\Desktop\BitLocker-Recovery-Key.txt"
Write-Host "⚠️ Sauvegardez la clé de récupération en lieu sûr!"
```

### Étape 4: Firewall et Réseau

```
╔══════════════════════════════════════════════════════════════╗
║           🔒 WIZARD SECURITY HARDENING                       ║
║               Étape 4/6 : Firewall/Réseau                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🌐 CONFIGURATION RÉSEAU SÉCURISÉE:                          ║
║                                                              ║
║  [x] Activer Firewall tous profils                           ║
║  [x] Bloquer connexions entrantes par défaut                 ║
║  [x] Désactiver SMBv1                                        ║
║  [x] Forcer SMB signing                                      ║
║  [x] Désactiver NetBIOS over TCP/IP                          ║
║  [x] Désactiver LLMNR                                        ║
║  [x] Activer TLS 1.3 uniquement                              ║
║  [ ] Désactiver IPv6 (si non utilisé)                        ║
║                                                              ║
║  [1] Appliquer tout  [2] Configurer  [3] Passer              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Firewall tous profils
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True -DefaultInboundAction Block

# Désactiver SMBv1
Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart

# Forcer SMB signing
Set-SmbServerConfiguration -RequireSecuritySignature $true -Force
Set-SmbClientConfiguration -RequireSecuritySignature $true -Force

# Désactiver LLMNR
New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" -Name "EnableMulticast" -Value 0

# TLS 1.3 uniquement
# Désactiver TLS 1.0/1.1
@("TLS 1.0","TLS 1.1") | ForEach-Object {
    New-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\$_\Client" -Force
    Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\$_\Client" -Name "Enabled" -Value 0
}
```

### Étape 5: Credential Guard et HVCI

```
╔══════════════════════════════════════════════════════════════╗
║           🔒 WIZARD SECURITY HARDENING                       ║
║              Étape 5/6 : Credential Guard                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔐 PROTECTION AVANCÉE CREDENTIALS:                          ║
║                                                              ║
║  Credential Guard protège contre :                           ║
║  • Pass-the-Hash attacks                                     ║
║  • Pass-the-Ticket attacks                                   ║
║  • Credential dumping (Mimikatz)                             ║
║                                                              ║
║  Prérequis :                                                 ║
║  ✅ UEFI Secure Boot                                         ║
║  ✅ TPM 2.0                                                   ║
║  ✅ Virtualization (VT-x/AMD-V)                               ║
║  ✅ Windows 11 Pro/Enterprise                                 ║
║                                                              ║
║  [1] Activer Credential Guard + HVCI                         ║
║  [2] Activer HVCI uniquement                                 ║
║  [3] Passer                                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes:**
```powershell
# Activer Credential Guard et HVCI
$RegistryPath = "HKLM:\SYSTEM\CurrentControlSet\Control\DeviceGuard"
Set-ItemProperty -Path $RegistryPath -Name "EnableVirtualizationBasedSecurity" -Value 1
Set-ItemProperty -Path $RegistryPath -Name "RequirePlatformSecurityFeatures" -Value 3

# Credential Guard
$CredGuardPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa"
Set-ItemProperty -Path $CredGuardPath -Name "LsaCfgFlags" -Value 1

# HVCI (Hypervisor-protected Code Integrity)
Set-ItemProperty -Path $RegistryPath -Name "HypervisorEnforcedCodeIntegrity" -Value 1

Write-Host "⚠️ Redémarrage requis pour activer Credential Guard"
```

### Étape 6: Résumé et Actions Finales

```
╔══════════════════════════════════════════════════════════════╗
║           🔒 WIZARD SECURITY HARDENING                       ║
║               Étape 6/6 : Finalisation                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✅ ACTIONS EFFECTUÉES:                                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✓ Windows Defender configuré (ASR activé)               │ ║
║  │ ✓ BitLocker C: activé (TPM+PIN)                         │ ║
║  │ ✓ Firewall renforcé tous profils                        │ ║
║  │ ✓ SMBv1 désactivé, SMB signing activé                   │ ║
║  │ ✓ TLS 1.0/1.1 désactivé                                 │ ║
║  │ ✓ Credential Guard activé                               │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📊 NOUVEAU SCORE: 92/100 ██████████████████░░               ║
║                                                              ║
║  ⚠️ Actions manuelles recommandées:                          ║
║  • Configurer LAPS si domaine AD                             ║
║  • Activer AppLocker/WDAC                                    ║
║  • Configurer audit logging avancé                           ║
║                                                              ║
║  [1] Redémarrer  [2] Exporter rapport  [3] Terminer          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
