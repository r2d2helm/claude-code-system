# /defender - Windows Defender - Avancé

Voir aussi: [[defender]]

Quarantaine, règles ASR, politiques et commandes avancées.

---

## /defender quarantine - Gestion Quarantaine

```
QUARANTAINE WINDOWS DEFENDER
═══════════════════════════════════════════════════════════════

Éléments en Quarantaine (2)
┌─────────────────────────────────────────────────────────────┐
│ 1. Trojan:Win32/Wacatac.B!ml                                │
│    ├─ Fichier original : C:\Users\Jean\Downloads\crack.exe  │
│    ├─ Taille           : 2.3 MB                             │
│    ├─ Date quarantaine : 2026-01-28 14:32:15                │
│    ├─ Sévérité         : Élevée                             │
│    └─ Expire           : 2026-04-28 (90 jours)              │
├─────────────────────────────────────────────────────────────┤
│ 2. Adware:Win32/BrowserModifier                             │
│    ├─ Fichier original : C:\ProgramData\toolbar.dll         │
│    ├─ Taille           : 456 KB                             │
│    ├─ Date quarantaine : 2026-01-15 11:20:00                │
│    ├─ Sévérité         : Faible                             │
│    └─ Expire           : 2026-04-15 (90 jours)              │
└─────────────────────────────────────────────────────────────┘

Espace quarantaine : 2.8 MB / 256 MB

Actions par élément:
├─ [R] Restaurer (⚠️ Risque sécurité)
├─ [S] Supprimer définitivement
└─ [D] Détails (soumettre à Microsoft)

Actions globales:
├─ [1] Supprimer tous les éléments expirés
├─ [2] Vider la quarantaine complètement
└─ [3] Exporter liste (CSV)

Choix: _
```

---

## /defender asr - Règles Attack Surface Reduction

```
RÈGLES ASR (ATTACK SURFACE REDUCTION)
═══════════════════════════════════════════════════════════════

État des Règles
┌───────────────────────────────────────────────────┬─────────┐
│ Règle                                             │ État    │
├───────────────────────────────────────────────────┼─────────┤
│ Bloquer contenu exécutable des emails             │ Block   │
│ Bloquer tous les apps Office créant processus     │ Block   │
│ Bloquer Office injectant dans processus           │ Block   │
│ Bloquer Office créant contenu exécutable          │ Block   │
│ Bloquer JavaScript/VBScript lançant contenu       │ Block   │
│ Bloquer exécution scripts potentiellement obfusqués│ Audit  │
│ Bloquer appels API Win32 depuis macros Office     │ Block   │
│ Bloquer création processus depuis PSExec/WMI      │ Audit  │
│ Bloquer processus non signés depuis USB           │ Block   │
│ Bloquer vol credentials depuis LSASS              │ Block   │
│ Bloquer persistence via WMI                       │ Audit  │
│ Utiliser protection avancée ransomware            │ Block   │
│ Bloquer Adobe Reader créant processus enfants     │ Block   │
└───────────────────────────────────────────────────┴─────────┘

Statistiques ASR (7 jours)
├─ Événements bloqués  : 23
├─ Événements audit    : 156
└─ Faux positifs       : 2 (exclusions ajoutées)

Actions:
├─ [1] Passer règle en mode Block
├─ [2] Passer règle en mode Audit
├─ [3] Désactiver règle
├─ [4] Ajouter exclusion ASR
└─ [5] Voir événements ASR détaillés
```

---

## Commandes PowerShell de Référence (Avancé)

```powershell
# Menaces avancé
Get-MpThreatCatalog | Where-Object {$_.SeverityID -ge 4}

# Quarantaine
Get-MpThreat | Where-Object {$_.IsActive -eq $false}
Remove-MpThreat -ThreatID <ID>
# Restaurer depuis quarantaine (interface graphique recommandée)

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
