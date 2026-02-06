# Gestion du Registre Windows

Navigation et modification sécurisée du registre.

## Mode d'Utilisation
```
/registry                   → Navigateur de registre
/registry search "terme"    → Rechercher dans le registre
/registry backup            → Sauvegarder une branche
/registry export "clé"      → Exporter en fichier .reg
/registry startup           → Programmes au démarrage
/registry uninstall         → Entrées de désinstallation
/registry recent            → Fichiers/dossiers récents
/registry troubleshoot      → Diagnostics courants
```

Arguments: $ARGUMENTS

---

## Navigateur (défaut)

```
📂 REGISTRE WINDOWS - NAVIGATEUR
═══════════════════════════════════════════════════════════════

BRANCHES PRINCIPALES:
├─ 📁 HKEY_CLASSES_ROOT (HKCR)
│  └─ Associations de fichiers, classes COM
├─ 📁 HKEY_CURRENT_USER (HKCU)
│  └─ Paramètres utilisateur actuel
├─ 📁 HKEY_LOCAL_MACHINE (HKLM)
│  └─ Paramètres système (tous utilisateurs)
├─ 📁 HKEY_USERS (HKU)
│  └─ Profils de tous les utilisateurs
└─ 📁 HKEY_CURRENT_CONFIG (HKCC)
   └─ Configuration matérielle actuelle

RACCOURCIS UTILES:
├─ /registry startup      → HKCU/HKLM\...\Run
├─ /registry uninstall    → HKLM\...\Uninstall
├─ /registry services     → HKLM\SYSTEM\...\Services
└─ /registry network      → HKLM\SYSTEM\...\Tcpip

Navigation: Entrez un chemin (ex: HKLM\SOFTWARE\Microsoft)
```

---

## Mode `search "terme"`

```
🔍 RECHERCHE: "OneDrive"
═══════════════════════════════════════════════════════════════

RÉSULTATS (23 trouvés, affichage des 10 premiers):

CLÉS:
├─ HKCU\Software\Microsoft\OneDrive
├─ HKLM\SOFTWARE\Microsoft\OneDrive
├─ HKLM\SOFTWARE\WOW6432Node\Microsoft\OneDrive
└─ HKCU\Software\Classes\CLSID\{...}\OneDrive

VALEURS:
┌─────────────────────────────────────────┬────────┬──────────────────────┐
│ Chemin                                  │ Nom    │ Valeur               │
├─────────────────────────────────────────┼────────┼──────────────────────┤
│ HKCU\Software\Microsoft\Windows\...Run  │OneDrive│ "C:\...\OneDrive.exe"│
│ HKLM\SOFTWARE\Microsoft\OneDrive        │Version │ "24.010.0114.0001"   │
│ HKCU\Software\Microsoft\OneDrive        │UserFolder│ "C:\Users\Jean\One.."│
└─────────────────────────────────────────┴────────┴──────────────────────┘

Actions:
1. Afficher plus de résultats
2. Exporter les résultats
3. Naviguer vers une clé
```

---

## Mode `startup`

```
🚀 PROGRAMMES AU DÉMARRAGE (Registre)
═══════════════════════════════════════════════════════════════

UTILISATEUR ACTUEL (HKCU\...\Run):
┌─────────────────────────┬────────────────────────────────────────────┐
│ Nom                     │ Commande                                   │
├─────────────────────────┼────────────────────────────────────────────┤
│ OneDrive                │ "C:\Users\Jean\AppData\Local\...\OneDr..." │
│ Discord                 │ "C:\Users\Jean\AppData\Local\Discord\U..." │
│ Spotify                 │ "C:\Users\Jean\AppData\Roaming\Spotify..." │
│ ⚠️ SuspiciousApp       │ "C:\Users\Jean\Downloads\app.exe /silent"  │
└─────────────────────────┴────────────────────────────────────────────┘

TOUS LES UTILISATEURS (HKLM\...\Run):
┌─────────────────────────┬────────────────────────────────────────────┐
│ Nom                     │ Commande                                   │
├─────────────────────────┼────────────────────────────────────────────┤
│ SecurityHealth          │ %ProgramFiles%\Windows Defender\MSASCuiL..│
│ iTunesHelper            │ "C:\Program Files\iTunes\iTunesHelper.exe"│
└─────────────────────────┴────────────────────────────────────────────┘

RUNONCE (exécution unique au prochain démarrage):
└─ (vide)

⚠️ ALERTES:
├─ SuspiciousApp: Chemin dans Downloads, flag /silent
└─ Vérifier la légitimité de cette entrée

ACTIONS:
1. Supprimer une entrée de démarrage
2. Désactiver temporairement (renommer)
3. Ajouter une entrée
4. Exporter la liste
```

---

## Mode `backup`

```
💾 SAUVEGARDE DU REGISTRE
═══════════════════════════════════════════════════════════════

OPTIONS DE SAUVEGARDE:

1. [full] Registre complet (⚠️ très long, ~500 MB)

2. [system] Branches système importantes:
   ├─ HKLM\SYSTEM
   ├─ HKLM\SOFTWARE
   └─ Estimé: ~150 MB

3. [user] Paramètres utilisateur:
   ├─ HKCU (tout)
   └─ Estimé: ~20 MB

4. [custom] Branche spécifique:
   └─ Chemin: _____

5. [recommended] Sauvegarde recommandée:
   ├─ HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion
   ├─ HKCU\Software\Microsoft\Windows\CurrentVersion
   ├─ HKLM\SYSTEM\CurrentControlSet\Services
   └─ Estimé: ~50 MB

Destination: C:\Backups\Registry\backup-2026-02-03.reg

Choix: _
```

---

## Mode `troubleshoot`

```
🔧 DIAGNOSTICS REGISTRE COURANTS
═══════════════════════════════════════════════════════════════

VÉRIFICATIONS:

1. ASSOCIATIONS DE FICHIERS
   ├─ .txt → txtfile (notepad.exe) ✅
   ├─ .pdf → AcroExch.Document ✅
   ├─ .jpg → jpegfile (Photos) ✅
   └─ État: OK

2. PROGRAMMES PAR DÉFAUT
   ├─ Navigateur: Chrome ✅
   ├─ Email: Outlook ✅
   └─ État: OK

3. SHELL EXTENSIONS
   ├─ Context menu entries: 45
   ├─ Problématiques: 2
   │  ├─ {ABC123...} - Fichier DLL manquant
   │  └─ {DEF456...} - Référence invalide
   └─ Suggestion: Nettoyer entrées orphelines

4. DÉSINSTALLATION INCOMPLÈTE
   ├─ Entrées orphelines trouvées: 8
   └─ Espace registre gaspillé: ~2 MB

ACTIONS CORRECTIVES:
1. Réparer associations de fichiers
2. Nettoyer shell extensions orphelines
3. Supprimer entrées désinstallation obsolètes
4. Exporter rapport détaillé

⚠️ Toujours sauvegarder avant modification
```

---

## Commandes de Référence

```powershell
# Lire une valeur
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion"

# Créer une clé
New-Item -Path "HKCU:\Software\MonApp"

# Définir une valeur
Set-ItemProperty -Path "HKCU:\Software\MonApp" -Name "Setting" -Value "1"

# Supprimer
Remove-ItemProperty -Path "HKCU:\Software\MonApp" -Name "Setting"
Remove-Item -Path "HKCU:\Software\MonApp" -Recurse

# Rechercher
Get-ChildItem -Path "HKLM:\SOFTWARE" -Recurse | Where-Object {$_.Name -like "*terme*"}

# Exporter
reg export "HKCU\Software\MonApp" "C:\backup.reg"

# Importer
reg import "C:\backup.reg"

# Programmes démarrage
Get-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
```
