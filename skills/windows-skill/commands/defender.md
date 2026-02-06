# /defender - Windows Defender Avancé

Gestion complète de Microsoft Defender : protection, scans, menaces, exclusions.

## Mode d'Utilisation

```
/defender                   # État protection et résumé
/defender status            # État détaillé tous composants
/defender scan              # Scan rapide
/defender scan full         # Scan complet
/defender scan custom "C:\" # Scan personnalisé
/defender threats           # Menaces détectées
/defender history           # Historique détections
/defender quarantine        # Gestion quarantaine
/defender exclusions        # Gérer exclusions
/defender update            # Mettre à jour définitions
/defender firewall          # État pare-feu intégré
/defender asr               # Règles ASR (Attack Surface Reduction)
/defender settings          # Tous les paramètres
```

Arguments: $ARGUMENTS

---

## Mode Défaut - État Protection

```
🛡️ WINDOWS DEFENDER - ÉTAT PROTECTION
═══════════════════════════════════════════════════════════════

📊 Protection en Temps Réel
┌─────────────────────────────────────────────────────────────┐
│ État global          : 🟢 PROTÉGÉ                           │
│ Protection temps réel: ✅ Activée                           │
│ Protection cloud     : ✅ Activée                           │
│ Soumission auto      : ✅ Activée                           │
│ Dernière analyse     : Il y a 2 heures (Rapide)             │
│ Définitions          : ✅ À jour (1.403.789.0)              │
│ Mise à jour déf.     : Aujourd'hui 08:15                    │
└─────────────────────────────────────────────────────────────┘

🔒 Composants de Protection
├─ Protection réseau        : ✅ Activée (Mode blocage)
├─ Protection web           : ✅ Activée
├─ Protection PUA           : ✅ Activée
├─ Accès contrôlé dossiers  : ⚠️ Mode audit uniquement
├─ Protection exploits      : ✅ Activée
├─ Protection altération    : ✅ Activée
└─ SmartScreen              : ✅ Activé (Avertir)

📈 Statistiques (30 derniers jours)
┌─────────────────────────────────────────────────────────────┐
│ Fichiers analysés    : 1,234,567                            │
│ Menaces détectées    : 3                                    │
│ Menaces bloquées     : 3 (100%)                             │
│ Faux positifs        : 1 (restauré)                         │
│ Scans effectués      : 45                                   │
└─────────────────────────────────────────────────────────────┘

⚠️ Actions Recommandées
└─ 🟡 Envisager d'activer "Accès contrôlé aux dossiers" en mode blocage
```

---

## /defender status - État Détaillé

```
🛡️ DEFENDER - ÉTAT COMPLET
═══════════════════════════════════════════════════════════════

📊 Service Antimalware
┌─────────────────────────────────────────────────────────────┐
│ Service              : WinDefend                            │
│ État                 : ✅ Running                           │
│ Type démarrage       : Automatique                          │
│ PID                  : 4532                                 │
│ Mémoire              : 245 MB                               │
│ Engine version       : 1.1.24010.10                         │
│ Product version      : 4.18.24010.12                        │
└─────────────────────────────────────────────────────────────┘

📦 Définitions Virus
┌─────────────────────────────────────────────────────────────┐
│ Version définitions  : 1.403.789.0                          │
│ Date création        : 2026-02-03                           │
│ Dernière MàJ         : 2026-02-03 08:15:32                  │
│ Signatures           : 456,789                              │
│ Source               : Microsoft Update                     │
│ État                 : ✅ À jour                            │
└─────────────────────────────────────────────────────────────┘

🔒 Protection Temps Réel
┌─────────────────────────────────────────────────────────────┐
│ État                 : ✅ Activée                           │
│ Analyse comportement : ✅ Activée                           │
│ Analyse heuristique  : ✅ Niveau élevé                      │
│ Analyse fichiers     : Tous les fichiers                    │
│ Analyse télécharg.   : ✅ Activée                           │
│ IOAV (Office)        : ✅ Activée                           │
│ Scripts              : ✅ Analyse activée                   │
└─────────────────────────────────────────────────────────────┘

☁️ Protection Cloud
┌─────────────────────────────────────────────────────────────┐
│ Niveau protection    : Élevé+ (Zero-Day)                    │
│ Soumission auto      : ✅ Fichiers suspects uniquement      │
│ Timeout cloud        : 60 secondes                          │
│ Connexion cloud      : ✅ Connecté                          │
└─────────────────────────────────────────────────────────────┘

🌐 Protection Réseau
┌─────────────────────────────────────────────────────────────┐
│ Network Protection   : ✅ Mode blocage                      │
│ Web Protection       : ✅ Activée                           │
│ Sites bloqués (24h)  : 2                                    │
│ Connexions bloquées  : 15                                   │
└─────────────────────────────────────────────────────────────┘

📁 Accès Contrôlé aux Dossiers
┌─────────────────────────────────────────────────────────────┐
│ État                 : ⚠️ Mode audit                        │
│ Dossiers protégés    : Documents, Images, Bureau, etc.      │
│ Apps autorisées      : 12                                   │
│ Blocages (7 jours)   : 0 (audit: 3 alertes)                │
└─────────────────────────────────────────────────────────────┘
```

---

## /defender scan - Lancer Scan

```
🔍 SCAN WINDOWS DEFENDER
═══════════════════════════════════════════════════════════════

Type de scan: RAPIDE

📊 Progression
┌─────────────────────────────────────────────────────────────┐
│ ████████████████████░░░░░░░░░░░░░░░░░░░░ 52%               │
│                                                             │
│ Éléments analysés   : 45,234 / ~85,000                      │
│ Temps écoulé        : 2m 34s                                │
│ Temps estimé restant: 2m 15s                                │
│                                                             │
│ Analyse en cours    : C:\Windows\System32\drivers\...       │
│ Menaces détectées   : 0                                     │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════

✅ SCAN TERMINÉ

📋 Résultats:
┌─────────────────────────────────────────────────────────────┐
│ Durée totale        : 4m 52s                                │
│ Éléments analysés   : 85,234                                │
│ Menaces détectées   : 0                                     │
│ Fichiers ignorés    : 12 (exclusions)                       │
│ Erreurs             : 0                                     │
└─────────────────────────────────────────────────────────────┘

🟢 Votre appareil est protégé - Aucune menace détectée

💡 Prochain scan planifié: Demain 03:00 (Rapide automatique)
```

---

## /defender threats - Menaces Détectées

```
⚠️ MENACES DÉTECTÉES
═══════════════════════════════════════════════════════════════

📋 Menaces Actives (0)
└─ ✅ Aucune menace active

📋 Menaces Récentes (30 jours)
┌─────────────────────────────────────────────────────────────┐
│ 🔴 Trojan:Win32/Wacatac.B!ml                                │
│ ├─ Date          : 2026-01-28 14:32:15                      │
│ ├─ Fichier       : C:\Users\Jean\Downloads\crack.exe        │
│ ├─ Sévérité      : Élevée                                   │
│ ├─ Catégorie     : Trojan                                   │
│ ├─ Action        : ✅ Quarantaine                           │
│ └─ État          : Résolu                                   │
├─────────────────────────────────────────────────────────────┤
│ 🟡 PUA:Win32/Presenoker                                     │
│ ├─ Date          : 2026-01-25 09:15:42                      │
│ ├─ Fichier       : C:\Temp\installer.exe                    │
│ ├─ Sévérité      : Faible                                   │
│ ├─ Catégorie     : Application potentiellement indésirable  │
│ ├─ Action        : ✅ Supprimé                              │
│ └─ État          : Résolu                                   │
├─────────────────────────────────────────────────────────────┤
│ 🟡 HackTool:Win32/Keygen                                    │
│ ├─ Date          : 2026-01-20 16:45:00                      │
│ ├─ Fichier       : D:\Logiciels\keygen.exe                  │
│ ├─ Sévérité      : Moyenne                                  │
│ ├─ Catégorie     : Outil de piratage                        │
│ ├─ Action        : ⚠️ Autorisé par utilisateur             │
│ └─ État          : Ignoré                                   │
└─────────────────────────────────────────────────────────────┘

📊 Statistiques
├─ Total détections : 3
├─ Quarantaine      : 1
├─ Supprimés        : 1
└─ Ignorés          : 1

🔧 Actions:
├─ /defender quarantine        - Gérer quarantaine
└─ /defender history          - Historique complet
```

---

## /defender quarantine - Gestion Quarantaine

```
🔒 QUARANTAINE WINDOWS DEFENDER
═══════════════════════════════════════════════════════════════

📋 Éléments en Quarantaine (2)
┌─────────────────────────────────────────────────────────────┐
│ 1. Trojan:Win32/Wacatac.B!ml                                │
│    ├─ Fichier original : C:\Users\Jean\Downloads\crack.exe  │
│    ├─ Taille           : 2.3 MB                             │
│    ├─ Date quarantaine : 2026-01-28 14:32:15                │
│    ├─ Sévérité         : 🔴 Élevée                          │
│    └─ Expire           : 2026-04-28 (90 jours)              │
├─────────────────────────────────────────────────────────────┤
│ 2. Adware:Win32/BrowserModifier                             │
│    ├─ Fichier original : C:\ProgramData\toolbar.dll         │
│    ├─ Taille           : 456 KB                             │
│    ├─ Date quarantaine : 2026-01-15 11:20:00                │
│    ├─ Sévérité         : 🟡 Faible                          │
│    └─ Expire           : 2026-04-15 (90 jours)              │
└─────────────────────────────────────────────────────────────┘

💾 Espace quarantaine : 2.8 MB / 256 MB

🔧 Actions par élément:
├─ [R] Restaurer (⚠️ Risque sécurité)
├─ [S] Supprimer définitivement
└─ [D] Détails (soumettre à Microsoft)

🔧 Actions globales:
├─ [1] Supprimer tous les éléments expirés
├─ [2] Vider la quarantaine complètement
└─ [3] Exporter liste (CSV)

Choix: _
```

---

## /defender exclusions - Gérer Exclusions

```
⚙️ EXCLUSIONS WINDOWS DEFENDER
═══════════════════════════════════════════════════════════════

📁 Exclusions de Dossiers (4)
├─ C:\Dev\Projects\                    (Développement)
├─ D:\VMs\                             (Machines virtuelles)
├─ C:\Tools\SysInternals\              (Outils admin)
└─ C:\Temp\BuildOutput\                (Compilation)

📄 Exclusions de Fichiers (2)
├─ C:\Tools\mimikatz.exe               ⚠️ Outil sensible
└─ D:\Games\anticcheat.dll             (Anti-cheat jeu)

🔧 Exclusions d'Extensions (3)
├─ .vhdx                               (Disques virtuels)
├─ .iso                                (Images ISO)
└─ .vmdk                               (VMware)

⚡ Exclusions de Processus (2)
├─ C:\Program Files\Docker\*           (Docker)
└─ C:\Program Files\JetBrains\*        (IDE)

═══════════════════════════════════════════════════════════════

⚠️ AVERTISSEMENTS SÉCURITÉ:
├─ 🔴 mimikatz.exe - Outil de récupération credentials
│     Recommandation: Supprimer si plus utilisé
└─ 🟡 6 exclusions au total - Vérifier régulièrement

🔧 Actions:
├─ [1] Ajouter exclusion dossier
├─ [2] Ajouter exclusion fichier
├─ [3] Ajouter exclusion extension
├─ [4] Ajouter exclusion processus
├─ [5] Supprimer une exclusion
└─ [6] Exporter liste exclusions

Choix: _
```

---

## /defender asr - Règles Attack Surface Reduction

```
🛡️ RÈGLES ASR (ATTACK SURFACE REDUCTION)
═══════════════════════════════════════════════════════════════

📋 État des Règles
┌───────────────────────────────────────────────────┬─────────┐
│ Règle                                             │ État    │
├───────────────────────────────────────────────────┼─────────┤
│ Bloquer contenu exécutable des emails             │ 🟢 Block│
│ Bloquer tous les apps Office créant processus     │ 🟢 Block│
│ Bloquer Office injectant dans processus           │ 🟢 Block│
│ Bloquer Office créant contenu exécutable          │ 🟢 Block│
│ Bloquer JavaScript/VBScript lançant contenu       │ 🟢 Block│
│ Bloquer exécution scripts potentiellement obfusqués│ 🟡 Audit│
│ Bloquer appels API Win32 depuis macros Office     │ 🟢 Block│
│ Bloquer création processus depuis PSExec/WMI      │ 🟡 Audit│
│ Bloquer processus non signés depuis USB           │ 🟢 Block│
│ Bloquer vol credentials depuis LSASS              │ 🟢 Block│
│ Bloquer persistence via WMI                       │ 🟡 Audit│
│ Utiliser protection avancée ransomware            │ 🟢 Block│
│ Bloquer Adobe Reader créant processus enfants     │ 🟢 Block│
└───────────────────────────────────────────────────┴─────────┘

📊 Statistiques ASR (7 jours)
├─ Événements bloqués  : 23
├─ Événements audit    : 156
└─ Faux positifs       : 2 (exclusions ajoutées)

🔧 Actions:
├─ [1] Passer règle en mode Block
├─ [2] Passer règle en mode Audit
├─ [3] Désactiver règle
├─ [4] Ajouter exclusion ASR
└─ [5] Voir événements ASR détaillés
```

---

## Commandes PowerShell de Référence

```powershell
# État Defender
Get-MpComputerStatus
Get-MpPreference

# Protection temps réel
Set-MpPreference -DisableRealtimeMonitoring $false

# Mise à jour définitions
Update-MpSignature

# Scans
Start-MpScan -ScanType QuickScan
Start-MpScan -ScanType FullScan
Start-MpScan -ScanPath "C:\Chemin" -ScanType CustomScan

# Menaces
Get-MpThreat
Get-MpThreatDetection
Get-MpThreatCatalog | Where-Object {$_.SeverityID -ge 4}

# Quarantaine
Get-MpThreat | Where-Object {$_.IsActive -eq $false}
Remove-MpThreat -ThreatID <ID>
# Restaurer depuis quarantaine (interface graphique recommandée)

# Exclusions
Get-MpPreference | Select-Object -ExpandProperty ExclusionPath
Get-MpPreference | Select-Object -ExpandProperty ExclusionExtension
Get-MpPreference | Select-Object -ExpandProperty ExclusionProcess

Add-MpPreference -ExclusionPath "C:\Dossier"
Add-MpPreference -ExclusionExtension ".ext"
Add-MpPreference -ExclusionProcess "process.exe"

Remove-MpPreference -ExclusionPath "C:\Dossier"

# Règles ASR
Get-MpPreference | Select-Object -ExpandProperty AttackSurfaceReductionRules_Ids
Get-MpPreference | Select-Object -ExpandProperty AttackSurfaceReductionRules_Actions

# Activer ASR (0=Disabled, 1=Block, 2=Audit)
Set-MpPreference -AttackSurfaceReductionRules_Ids <GUID> -AttackSurfaceReductionRules_Actions 1

# Protection cloud
Set-MpPreference -MAPSReporting Advanced
Set-MpPreference -SubmitSamplesConsent SendSafeSamples

# Protection réseau
Set-MpPreference -EnableNetworkProtection Enabled

# Accès contrôlé dossiers
Set-MpPreference -EnableControlledFolderAccess Enabled
Add-MpPreference -ControlledFolderAccessAllowedApplications "C:\App\app.exe"

# Événements Defender
Get-WinEvent -LogName "Microsoft-Windows-Windows Defender/Operational" -MaxEvents 50

# Interface graphique
Start-Process "windowsdefender://threat"
Start-Process "windowsdefender://threatsettings"
```
