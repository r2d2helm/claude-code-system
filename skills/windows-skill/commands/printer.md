# /printer - Gestion Imprimantes Windows

Gestion complète des imprimantes : installation, file d'attente, dépannage.

## Mode d'Utilisation

```
/printer                    # État imprimantes + file d'attente
/printer list               # Liste toutes les imprimantes
/printer status "Nom"       # État détaillé d'une imprimante
/printer queue              # File d'attente toutes imprimantes
/printer clear "Nom"        # Vider file d'attente
/printer default "Nom"      # Définir imprimante par défaut
/printer add                # Assistant ajout imprimante
/printer remove "Nom"       # Supprimer imprimante
/printer test "Nom"         # Page de test
/printer troubleshoot       # Dépannage imprimantes
/printer drivers            # Gestion pilotes d'impression
/printer ports              # Configuration ports
```

Arguments: $ARGUMENTS

---

## Mode Défaut - État Imprimantes

```
🖨️ IMPRIMANTES - ÉTAT GÉNÉRAL
═══════════════════════════════════════════════════════════════

📋 Imprimantes Installées (5)
┌─────────────────────────────┬──────────┬─────────┬──────────┐
│ Nom                         │ État     │ File    │ Type     │
├─────────────────────────────┼──────────┼─────────┼──────────┤
│ ★ HP LaserJet Pro MFP       │ 🟢 Prête │ 0       │ Réseau   │
│   Brother HL-L2350DW        │ 🟢 Prête │ 2       │ WiFi     │
│   Canon PIXMA MG3650        │ 🟡 Veille│ 0       │ USB      │
│   Microsoft Print to PDF    │ 🟢 Prête │ 0       │ Virtuel  │
│   OneNote                   │ 🟢 Prête │ 0       │ Virtuel  │
└─────────────────────────────┴──────────┴─────────┴──────────┘

★ = Imprimante par défaut

📊 File d'Attente Active (2 travaux)
┌─────────────────────────────────────────────────────────────┐
│ Brother HL-L2350DW                                          │
├─────────────────────────────────────────────────────────────┤
│ 📄 Rapport_Annuel.pdf      │ En cours │ 45% │ Jean        │
│ 📄 Facture_2026-001.docx   │ En attente│ -  │ Marie       │
└─────────────────────────────────────────────────────────────┘

🔧 Service Spooler
├─ État        : ✅ Running
├─ Type        : Automatique
└─ Mémoire     : 45 MB

⚠️ Alertes
└─ 🟡 Canon PIXMA: Niveau encre couleur bas (15%)
```

---

## /printer status "Nom" - État Détaillé

```
🖨️ IMPRIMANTE: HP LaserJet Pro MFP M428fdw
═══════════════════════════════════════════════════════════════

📊 État Général
┌─────────────────────────────────────────────────────────────┐
│ État               : 🟢 Prête                               │
│ Par défaut         : ✅ Oui                                 │
│ Partagée           : ✅ Oui (\\PC-BUREAU\HP-LaserJet)       │
│ Disponibilité      : Toujours                               │
└─────────────────────────────────────────────────────────────┘

🔌 Connexion
┌─────────────────────────────────────────────────────────────┐
│ Type               : Réseau (TCP/IP)                        │
│ Adresse IP         : 192.168.1.50                           │
│ Port               : IP_192.168.1.50                        │
│ Ping               : ✅ 2ms                                 │
│ Interface Web      : http://192.168.1.50                    │
└─────────────────────────────────────────────────────────────┘

⚙️ Configuration
┌─────────────────────────────────────────────────────────────┐
│ Pilote             : HP Universal Print Driver (v7.0.1.25)  │
│ Processeur         : winprint                               │
│ Bac par défaut     : Auto                                   │
│ Recto-verso        : ✅ Activé                              │
│ Couleur            : Noir & Blanc (économie)                │
│ Qualité            : 600 dpi                                │
│ Format papier      : A4                                     │
└─────────────────────────────────────────────────────────────┘

📈 Statistiques
┌─────────────────────────────────────────────────────────────┐
│ Pages imprimées    : 12,456 (ce mois: 234)                  │
│ Travaux ce jour    : 15                                     │
│ Travaux échoués    : 0                                      │
│ Dernier travail    : Il y a 25 minutes                      │
└─────────────────────────────────────────────────────────────┘

🎨 Consommables (via SNMP)
┌─────────────────────────────────────────────────────────────┐
│ Toner Noir         : ████████░░ 78%                         │
│ Tambour            : ██████████ 95%                         │
│ Kit maintenance    : ████████░░ 82%                         │
└─────────────────────────────────────────────────────────────┘

🔧 Actions:
├─ /printer queue "HP LaserJet Pro MFP" - Voir file
├─ /printer test "HP LaserJet Pro MFP"  - Page de test
├─ /printer default "HP LaserJet Pro MFP" - Définir par défaut
└─ http://192.168.1.50 - Interface web imprimante
```

---

## /printer queue - File d'Attente

```
📋 FILE D'ATTENTE D'IMPRESSION
═══════════════════════════════════════════════════════════════

🖨️ Brother HL-L2350DW (2 travaux)
┌─────┬────────────────────────┬──────────┬────────┬──────────┐
│ #   │ Document               │ État     │ Pages  │ Utilisat.│
├─────┼────────────────────────┼──────────┼────────┼──────────┤
│ 1   │ Rapport_Annuel.pdf     │ 🔄 45%   │ 12/26  │ Jean     │
│ 2   │ Facture_2026-001.docx  │ ⏳ Attente│ 2     │ Marie    │
└─────┴────────────────────────┴──────────┴────────┴──────────┘

🖨️ HP LaserJet Pro MFP (0 travaux)
└─ File vide

🖨️ Canon PIXMA MG3650 (1 travail - ERREUR)
┌─────┬────────────────────────┬──────────┬────────┬──────────┐
│ #   │ Document               │ État     │ Pages  │ Utilisat.│
├─────┼────────────────────────┼──────────┼────────┼──────────┤
│ 1   │ Photo_Vacances.jpg     │ ❌ Erreur│ 0/1   │ Pierre   │
└─────┴────────────────────────┴──────────┴────────┴──────────┘
     ⚠️ Erreur: Plus de papier dans le bac photo

═══════════════════════════════════════════════════════════════

📊 Résumé: 3 travaux total (1 en cours, 1 en attente, 1 erreur)

🔧 Actions:
├─ /printer clear "Brother"     - Vider file Brother
├─ /printer clear all           - Vider toutes les files
└─ Annuler travail spécifique   - Via interface graphique
```

---

## /printer add - Assistant Ajout

```
➕ ASSISTANT AJOUT IMPRIMANTE
═══════════════════════════════════════════════════════════════

📋 Type de connexion:

1️⃣ Imprimante réseau (IP)
   └─ Imprimante avec adresse IP fixe

2️⃣ Imprimante USB
   └─ Connectée directement à ce PC

3️⃣ Imprimante partagée (réseau Windows)
   └─ Partagée depuis un autre PC

4️⃣ Imprimante Bluetooth
   └─ Connexion sans fil Bluetooth

5️⃣ Imprimante WiFi Direct
   └─ Connexion WiFi sans routeur

Choix: [1]

═══════════════════════════════════════════════════════════════

📡 Recherche Imprimantes Réseau...

Imprimantes détectées:
┌─────────────────────────────┬────────────────┬──────────────┐
│ Nom                         │ Adresse IP     │ Modèle       │
├─────────────────────────────┼────────────────┼──────────────┤
│ EPSON-L3150                 │ 192.168.1.55   │ EcoTank L315 │
│ HP-LaserJet-Bureau          │ 192.168.1.60   │ LaserJet M15 │
└─────────────────────────────┴────────────────┴──────────────┘

Ou saisir manuellement: [192.168.1.__]

═══════════════════════════════════════════════════════════════

⚙️ Configuration:
├─ Nom affiché    : [EPSON EcoTank L3150___]
├─ Port           : IP_192.168.1.55 (créé)
├─ Pilote         : [Télécharger auto ▼]
├─ Partager       : ☐ Partager sur le réseau
└─ Par défaut     : ☐ Définir comme imprimante par défaut

⚠️ Installer cette imprimante? [O/N]
```

---

## /printer troubleshoot - Dépannage

```
🔧 DÉPANNAGE IMPRIMANTES
═══════════════════════════════════════════════════════════════

📋 DIAGNOSTIC AUTOMATIQUE

1. Service Spooler
   ├─ État                                 ✅ Running
   ├─ Type démarrage                       ✅ Automatique
   └─ Répondant                            ✅ OK

2. Imprimante par défaut: HP LaserJet Pro MFP
   ├─ État                                 ✅ Prête
   ├─ Port valide                          ✅ IP_192.168.1.50
   ├─ Pilote installé                      ✅ v7.0.1.25
   └─ Connectivité réseau                  ✅ Ping OK (2ms)

3. File d'attente
   ├─ Travaux bloqués                      ❌ 1 travail
   └─ Espace disque spool                  ✅ 45 GB libre

═══════════════════════════════════════════════════════════════

⚠️ PROBLÈMES DÉTECTÉS:

❌ Canon PIXMA MG3650 - Travail bloqué
┌─────────────────────────────────────────────────────────────┐
│ Cause probable: Plus de papier dans le bac photo            │
│                                                             │
│ Solutions:                                                  │
│ 1. Ajouter du papier photo dans le bac dédié               │
│ 2. Ou annuler le travail d'impression                       │
│                                                             │
│ 🔧 /printer clear "Canon PIXMA" pour vider la file         │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════

🛠️ SOLUTIONS GÉNÉRALES

Imprimante ne répond pas:
├─ 1. Redémarrer le service Spooler
│     net stop spooler && net start spooler
├─ 2. Vérifier connexion (USB/réseau)
├─ 3. Vider le dossier spool
│     Supprimer C:\Windows\System32\spool\PRINTERS\*
└─ 4. Réinstaller le pilote

Qualité d'impression médiocre:
├─ 1. Lancer nettoyage têtes (imprimante jet d'encre)
├─ 2. Calibrer les couleurs
└─ 3. Vérifier niveaux encre/toner

Impression lente:
├─ 1. Réduire qualité d'impression
├─ 2. Désactiver l'impression recto-verso
├─ 3. Imprimer en noir & blanc
└─ 4. Mettre à jour le pilote

═══════════════════════════════════════════════════════════════

🔄 Actions de réparation:

[1] Redémarrer service Spooler
[2] Vider toutes les files d'attente
[3] Réinitialiser imprimante par défaut
[4] Réinstaller pilote imprimante problématique
[5] Exécuter dépannage Windows automatique

Choix: _
```

---

## /printer drivers - Gestion Pilotes

```
🔧 PILOTES D'IMPRESSION
═══════════════════════════════════════════════════════════════

📋 Pilotes Installés
┌────────────────────────────────────┬─────────────┬──────────┐
│ Pilote                             │ Version     │ Utilisé  │
├────────────────────────────────────┼─────────────┼──────────┤
│ HP Universal Print Driver          │ 7.0.1.25    │ 1 imp.   │
│ Brother HL-L2350DW series          │ 1.20.0.0    │ 1 imp.   │
│ Canon PIXMA MG3600 series          │ 1.10        │ 1 imp.   │
│ Microsoft Print To PDF             │ 10.0.22621  │ 1 imp.   │
│ Microsoft XPS Document Writer      │ 10.0.22621  │ 0 imp.   │
│ Send to Microsoft OneNote          │ 16.0.14326  │ 1 imp.   │
│ HP LaserJet 1020 (obsolète)        │ 5.8.0.0     │ 0 imp.   │
└────────────────────────────────────┴─────────────┴──────────┘

⚠️ Pilotes inutilisés: 2 (récupérable: 15 MB)

📦 Mises à jour disponibles:
├─ Brother HL-L2350DW: 1.20.0.0 → 1.25.0.0
└─ Canon PIXMA: 1.10 → 1.12

🔧 Actions:
├─ [1] Mettre à jour pilote Brother
├─ [2] Mettre à jour pilote Canon
├─ [3] Supprimer pilotes inutilisés
├─ [4] Télécharger pilote manuel (URL)
└─ [5] Ajouter pilote depuis fichier .inf
```

---

## Commandes PowerShell de Référence

```powershell
# Lister imprimantes
Get-Printer
Get-Printer | Format-Table Name, DriverName, PortName, PrinterStatus

# État imprimante
Get-Printer -Name "NomImprimante" | Format-List *
Get-PrintJob -PrinterName "NomImprimante"

# File d'attente
Get-PrintJob -PrinterName "NomImprimante"
Remove-PrintJob -PrinterName "NomImprimante" -ID 1
# Vider file complète
Get-PrintJob -PrinterName "NomImprimante" | Remove-PrintJob

# Imprimante par défaut
Get-CimInstance -ClassName Win32_Printer | Where-Object {$_.Default -eq $true}
# Définir par défaut
(Get-CimInstance -ClassName Win32_Printer -Filter "Name='NomImprimante'").SetDefaultPrinter()
# Ou via rundll32
rundll32 printui.dll,PrintUIEntry /y /n "NomImprimante"

# Ajouter imprimante réseau
Add-Printer -Name "NouvelleImprimante" -DriverName "HP Universal Print Driver" -PortName "IP_192.168.1.50"
Add-PrinterPort -Name "IP_192.168.1.50" -PrinterHostAddress "192.168.1.50"

# Supprimer imprimante
Remove-Printer -Name "NomImprimante"

# Page de test
$printer = Get-CimInstance -ClassName Win32_Printer -Filter "Name='NomImprimante'"
$printer | Invoke-CimMethod -MethodName PrintTestPage

# Service Spooler
Get-Service Spooler
Restart-Service Spooler -Force

# Vider spool (si bloqué)
Stop-Service Spooler
Remove-Item C:\Windows\System32\spool\PRINTERS\* -Force
Start-Service Spooler

# Pilotes
Get-PrinterDriver
Add-PrinterDriver -Name "HP Universal Print Driver"
Remove-PrinterDriver -Name "NomPilote"

# Ports
Get-PrinterPort
Add-PrinterPort -Name "IP_192.168.1.50" -PrinterHostAddress "192.168.1.50"

# Partage imprimante
Set-Printer -Name "NomImprimante" -Shared $true -ShareName "PartageImprimante"

# Dépannage automatique
msdt.exe /id PrinterDiagnostic

# Interface graphique
control printers
rundll32 printui.dll,PrintUIEntry /il  # Ajouter imprimante
```
