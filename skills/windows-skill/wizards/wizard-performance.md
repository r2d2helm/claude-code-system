# Wizard: Performance Tuning

Optimisation performances Windows 11/Server 2025.

## Déclenchement

```
/win-wizard performance
```

## Étapes du Wizard (4)

### Étape 1: Analyse Performances

```
╔══════════════════════════════════════════════════════════════╗
║           ⚡ WIZARD PERFORMANCE TUNING                       ║
║                Étape 1/4 : Analyse                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔍 ANALYSE EN COURS...                                      ║
║                                                              ║
║  📊 RÉSULTATS:                                               ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ CPU        : 45% moyen | Pic: 92%    ⚠️                 │ ║
║  │ RAM        : 78% utilisé (25/32 GB)  ⚠️                 │ ║
║  │ Disque C:  : 85% plein              ❌                  │ ║
║  │ I/O Disque : Latence 15ms           ✅                  │ ║
║  │ Réseau     : 120 Mbps / 1 Gbps      ✅                  │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  🔥 TOP PROCESSUS:                                           ║
║  1. Chrome.exe          - 4.2 GB RAM                         ║
║  2. MsMpEng.exe         - 1.1 GB RAM (Defender)              ║
║  3. Teams.exe           - 890 MB RAM                         ║
║                                                              ║
║  Problèmes détectés: 3                                       ║
║                                                              ║
║  [1] Voir recommandations  [2] Analyse détaillée             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes analyse:**
```powershell
# Analyse CPU/RAM
Get-Counter '\Processor(_Total)\% Processor Time','\Memory\% Committed Bytes In Use' -SampleInterval 2 -MaxSamples 5

# Top processus par RAM
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 Name, @{N='RAM_MB';E={[math]::Round($_.WorkingSet64/1MB,2)}}

# Espace disque
Get-Volume | Select-Object DriveLetter, FileSystemLabel, @{N='Used_GB';E={[math]::Round(($_.Size-$_.SizeRemaining)/1GB,2)}}, @{N='Free_GB';E={[math]::Round($_.SizeRemaining/1GB,2)}}

# Latence disque
Get-Counter '\PhysicalDisk(*)\Avg. Disk sec/Read','\PhysicalDisk(*)\Avg. Disk sec/Write'
```

### Étape 2: Optimisation Disque

```
╔══════════════════════════════════════════════════════════════╗
║           ⚡ WIZARD PERFORMANCE TUNING                       ║
║              Étape 2/4 : Optimisation Disque                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  💾 NETTOYAGE DISQUE:                                        ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Fichiers temporaires     : 8.5 GB    [x]                │ ║
║  │ Windows Update cache     : 12.3 GB   [x]                │ ║
║  │ Corbeille                : 2.1 GB    [x]                │ ║
║  │ Logs système             : 1.8 GB    [x]                │ ║
║  │ Anciennes versions Win   : 15.2 GB   [x]                │ ║
║  │ ─────────────────────────────────────────               │ ║
║  │ Total récupérable        : 39.9 GB                      │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  Optimisations supplémentaires:                              ║
║  [x] Défragmenter HDD (pas SSD)                              ║
║  [x] Optimiser SSD (TRIM)                                    ║
║  [x] Désactiver indexation sur D:                            ║
║  [ ] Déplacer fichier page vers D:                           ║
║                                                              ║
║  [1] Nettoyer et optimiser  [2] Configurer  [3] Suivant      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes nettoyage:**
```powershell
# Nettoyage disque automatisé
cleanmgr /d C /sageset:1
cleanmgr /d C /sagerun:1

# Nettoyage DISM
Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase

# Vider cache Windows Update
Stop-Service wuauserv
Remove-Item -Path "C:\Windows\SoftwareDistribution\*" -Recurse -Force
Start-Service wuauserv

# Optimiser SSD
Optimize-Volume -DriveLetter C -ReTrim -Verbose

# Désactiver indexation
Set-Service WSearch -StartupType Disabled
Stop-Service WSearch
```

### Étape 3: Optimisation Système

```
╔══════════════════════════════════════════════════════════════╗
║           ⚡ WIZARD PERFORMANCE TUNING                       ║
║              Étape 3/4 : Optimisation Système                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ⚙️ OPTIMISATIONS SYSTÈME:                                   ║
║                                                              ║
║  Démarrage:                                                  ║
║  [x] Désactiver apps démarrage inutiles (12 détectées)       ║
║  [x] Réduire délai menu boot (10s → 3s)                      ║
║  [x] Activer démarrage rapide                                ║
║                                                              ║
║  Services:                                                   ║
║  [x] Désactiver services inutilisés (8 détectés)             ║
║      • Fax, Xbox services, Print Spooler (si pas imprimante) ║
║                                                              ║
║  Mémoire:                                                    ║
║  [x] Optimiser fichier page (géré par système)               ║
║  [ ] Désactiver Superfetch (SSD uniquement)                  ║
║  [x] Vider mémoire standby périodiquement                    ║
║                                                              ║
║  Visuel (impact minimal):                                    ║
║  [ ] Désactiver animations                                   ║
║  [ ] Désactiver transparence                                 ║
║                                                              ║
║  [1] Appliquer recommandations  [2] Personnaliser            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes optimisation:**
```powershell
# Désactiver apps démarrage
Get-CimInstance Win32_StartupCommand | Where-Object {$_.Location -eq "HKCU"} | Select-Object Name, Command

# Réduire délai boot
bcdedit /timeout 3

# Désactiver services inutiles
$ServicesToDisable = @("Fax", "XblAuthManager", "XblGameSave", "XboxNetApiSvc")
foreach ($Svc in $ServicesToDisable) {
    Set-Service -Name $Svc -StartupType Disabled -ErrorAction SilentlyContinue
}

# Optimiser pour performances
$Path = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
Set-ItemProperty -Path $Path -Name VisualFXSetting -Value 2

# Plan d'alimentation haute performance
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
```

### Étape 4: Résumé et Monitoring

```
╔══════════════════════════════════════════════════════════════╗
║           ⚡ WIZARD PERFORMANCE TUNING                       ║
║              Étape 4/4 : Résumé                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✅ OPTIMISATIONS APPLIQUÉES:                                 ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ✓ Espace disque libéré   : 39.9 GB                      │ ║
║  │ ✓ Services désactivés    : 8                            │ ║
║  │ ✓ Apps démarrage         : 12 → 4                       │ ║
║  │ ✓ SSD optimisé           : TRIM exécuté                 │ ║
║  │ ✓ Plan alimentation      : Haute performance            │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                              ║
║  📈 AMÉLIORATION ESTIMÉE:                                    ║
║  • Démarrage : -35% temps                                    ║
║  • RAM disponible : +2.5 GB                                  ║
║  • Réactivité : Améliorée                                    ║
║                                                              ║
║  📊 Configurer monitoring continu ?                          ║
║  [1] Oui (Performance Monitor)                               ║
║  [2] Non, terminer                                           ║
║  [3] Planifier maintenance automatique                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Commandes monitoring:**
```powershell
# Créer collecteur Performance Monitor
$DataCollectorSet = New-Object -ComObject Pla.DataCollectorSet
$DataCollectorSet.DisplayName = "System Performance"
$DataCollectorSet.Duration = 3600
$DataCollectorSet.Commit("System Performance", $null, 0x0003)
$DataCollectorSet.Start($false)

# Tâche planifiée maintenance
$Action = New-ScheduledTaskAction -Execute "cleanmgr.exe" -Argument "/sagerun:1"
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 3am
Register-ScheduledTask -TaskName "Weekly Cleanup" -Action $Action -Trigger $Trigger -RunLevel Highest
```
