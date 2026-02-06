# /bluetooth - Gestion Bluetooth Windows

Gestion des périphériques Bluetooth : appariement, connexion, audio, dépannage.

## Mode d'Utilisation

```
/bluetooth                  # État Bluetooth et appareils
/bluetooth scan             # Rechercher appareils à proximité
/bluetooth devices          # Liste appareils appairés
/bluetooth connect "Nom"    # Connecter un appareil
/bluetooth disconnect "Nom" # Déconnecter un appareil
/bluetooth pair             # Mode appariement
/bluetooth remove "Nom"     # Supprimer un appareil
/bluetooth audio            # Configuration audio Bluetooth
/bluetooth troubleshoot     # Dépannage Bluetooth
/bluetooth drivers          # État pilotes Bluetooth
/bluetooth settings         # Paramètres Bluetooth
```

Arguments: $ARGUMENTS

---

## Mode Défaut - État Bluetooth

```
📶 BLUETOOTH - ÉTAT GÉNÉRAL
═══════════════════════════════════════════════════════════════

📡 Adaptateur Bluetooth
┌─────────────────────────────────────────────────────────────┐
│ Adaptateur         : Intel AX201 Bluetooth                  │
│ État               : ✅ Activé                              │
│ Adresse MAC        : A4:C3:F0:XX:XX:XX                      │
│ Version BT         : 5.2                                    │
│ Mode               : Découvrable (2 min restantes)          │
│ LMP Version        : 11                                     │
└─────────────────────────────────────────────────────────────┘

🔗 Appareils Connectés (3)
┌──────────────────────────────┬──────────┬────────┬──────────┐
│ Appareil                     │ Type     │ Batterie│ État    │
├──────────────────────────────┼──────────┼────────┼──────────┤
│ 🎧 Sony WH-1000XM5           │ Audio    │ 75%    │ 🟢 Conn. │
│ ⌨️ Logitech MX Keys          │ Clavier  │ 90%    │ 🟢 Conn. │
│ 🖱️ Logitech MX Master 3     │ Souris   │ 45%    │ 🟢 Conn. │
└──────────────────────────────┴──────────┴────────┴──────────┘

📋 Appareils Appairés (non connectés)
├─ 📱 iPhone de Jean           │ Téléphone│ -      │ ⚪ Dispo
├─ 🎮 Xbox Controller          │ Manette  │ -      │ ⚪ Dispo
└─ 🔊 JBL Flip 5               │ Enceinte │ -      │ ⚪ Dispo

📊 Services Bluetooth
├─ Bluetooth Support Service  : ✅ Running
├─ Bluetooth Audio Gateway    : ✅ Running
└─ Bluetooth User Support     : ✅ Running

⚠️ Alertes
└─ 🟡 Logitech MX Master 3 : Batterie faible (45%)
```

---

## /bluetooth scan - Rechercher Appareils

```
🔍 RECHERCHE APPAREILS BLUETOOTH
═══════════════════════════════════════════════════════════════

🔄 Scan en cours... (30 secondes)

████████████████░░░░░░░░░░░░░░░░ 52%

📡 Appareils Détectés (8)
┌──────────────────────────────┬──────────┬────────┬──────────┐
│ Nom                          │ Type     │ Signal │ État     │
├──────────────────────────────┼──────────┼────────┼──────────┤
│ 🎧 AirPods Pro              │ Audio    │ ████░  │ Nouveau  │
│ 📱 Samsung Galaxy S24       │ Téléphone│ ███░░  │ Nouveau  │
│ 🔊 Bose SoundLink           │ Enceinte │ ███░░  │ Nouveau  │
│ ⌚ Apple Watch              │ Montre   │ ██░░░  │ Nouveau  │
│ 🖨️ HP OfficeJet            │ Imprimant│ ██░░░  │ Nouveau  │
├──────────────────────────────┼──────────┼────────┼──────────┤
│ 🎧 Sony WH-1000XM5          │ Audio    │ █████  │ Appairé  │
│ ⌨️ Logitech MX Keys         │ Clavier  │ █████  │ Appairé  │
│ 📱 iPhone de Jean           │ Téléphone│ ████░  │ Appairé  │
└──────────────────────────────┴──────────┴────────┴──────────┘

Signal: █████ Excellent | ████░ Bon | ███░░ Moyen | ██░░░ Faible

🔧 Actions:
├─ /bluetooth pair "AirPods Pro"     - Appairer
├─ /bluetooth connect "Sony WH-1000" - Connecter appairé
└─ [Esc] Arrêter le scan
```

---

## /bluetooth devices - Appareils Appairés

```
📋 APPAREILS BLUETOOTH APPAIRÉS
═══════════════════════════════════════════════════════════════

🎧 AUDIO (2)
┌─────────────────────────────────────────────────────────────┐
│ Sony WH-1000XM5                                             │
│ ├─ État          : 🟢 Connecté                              │
│ ├─ Batterie      : 75% 🔋                                   │
│ ├─ Profils       : A2DP, AVRCP, HFP                         │
│ ├─ Codec audio   : LDAC (Hi-Res)                            │
│ ├─ Dernière conn.: Maintenant                               │
│ └─ MAC           : 00:1A:2B:XX:XX:XX                        │
├─────────────────────────────────────────────────────────────┤
│ JBL Flip 5                                                  │
│ ├─ État          : ⚪ Non connecté                          │
│ ├─ Profils       : A2DP, AVRCP                              │
│ ├─ Dernière conn.: Il y a 3 jours                           │
│ └─ MAC           : 00:2B:3C:XX:XX:XX                        │
└─────────────────────────────────────────────────────────────┘

⌨️ PÉRIPHÉRIQUES INPUT (2)
┌─────────────────────────────────────────────────────────────┐
│ Logitech MX Keys                                            │
│ ├─ État          : 🟢 Connecté                              │
│ ├─ Batterie      : 90% 🔋                                   │
│ ├─ Profil        : HID                                      │
│ └─ Dernière conn.: Maintenant                               │
├─────────────────────────────────────────────────────────────┤
│ Logitech MX Master 3                                        │
│ ├─ État          : 🟢 Connecté                              │
│ ├─ Batterie      : 45% ⚠️                                   │
│ ├─ Profil        : HID                                      │
│ └─ Dernière conn.: Maintenant                               │
└─────────────────────────────────────────────────────────────┘

📱 TÉLÉPHONES (1)
┌─────────────────────────────────────────────────────────────┐
│ iPhone de Jean                                              │
│ ├─ État          : ⚪ Non connecté                          │
│ ├─ Profils       : OBEX, PBAP, MAP                          │
│ ├─ Dernière conn.: Hier 18:45                               │
│ └─ MAC           : 00:3C:4D:XX:XX:XX                        │
└─────────────────────────────────────────────────────────────┘

🎮 GAMING (1)
┌─────────────────────────────────────────────────────────────┐
│ Xbox Wireless Controller                                    │
│ ├─ État          : ⚪ Non connecté                          │
│ ├─ Profil        : HID (Gaming)                             │
│ └─ Dernière conn.: Il y a 1 semaine                         │
└─────────────────────────────────────────────────────────────┘

Total: 6 appareils (3 connectés, 3 disponibles)
```

---

## /bluetooth audio - Configuration Audio Bluetooth

```
🎧 AUDIO BLUETOOTH
═══════════════════════════════════════════════════════════════

📊 Appareil Audio Actif
┌─────────────────────────────────────────────────────────────┐
│ 🎧 Sony WH-1000XM5                                          │
│                                                             │
│ Sortie audio       : ✅ Défaut système                      │
│ Entrée micro       : ✅ Défaut communications               │
│                                                             │
│ Profil actif       : A2DP (Haute qualité)                   │
│ Codec              : LDAC (990 kbps)                        │
│ Qualité            : Hi-Res Audio                           │
│ Latence            : ~40ms                                  │
│                                                             │
│ 🎤 Microphone      : Actif (mode casque)                    │
│ 🔊 Volume          : ████████░░ 80%                         │
│ 🔋 Batterie        : ███████░░░ 75%                         │
└─────────────────────────────────────────────────────────────┘

⚙️ Profils Audio Disponibles
┌─────────────────────────────────────────────────────────────┐
│ ● A2DP (Advanced Audio)                                     │
│   └─ Haute qualité stéréo, pas de micro                     │
│                                                             │
│ ○ HFP (Hands-Free Profile)                                  │
│   └─ Qualité téléphone, micro actif                         │
│                                                             │
│ ○ HSP (Headset Profile)                                     │
│   └─ Qualité basique, mono                                  │
└─────────────────────────────────────────────────────────────┘

📈 Codecs Supportés
├─ ✅ LDAC (Hi-Res, 990 kbps) - Actif
├─ ✅ AAC (256 kbps)
├─ ✅ aptX HD (576 kbps)
├─ ✅ aptX (352 kbps)
└─ ✅ SBC (328 kbps) - Fallback

🔧 Actions:
├─ [1] Changer profil (A2DP ↔ HFP)
├─ [2] Définir comme sortie par défaut
├─ [3] Définir comme entrée par défaut
├─ [4] Ouvrir paramètres son Windows
└─ [5] Test audio
```

---

## /bluetooth troubleshoot - Dépannage

```
🔧 DÉPANNAGE BLUETOOTH
═══════════════════════════════════════════════════════════════

📋 DIAGNOSTIC AUTOMATIQUE

1. Adaptateur Bluetooth
   ├─ Présent                              ✅ OK
   ├─ Pilote installé                      ✅ OK
   ├─ Radio activée                        ✅ OK
   └─ Service Bluetooth                    ✅ Running

2. Services Windows
   ├─ Bluetooth Support Service            ✅ Running
   ├─ Bluetooth Audio Gateway              ✅ Running
   ├─ Bluetooth User Support               ✅ Running
   └─ Device Association Service           ✅ Running

3. Mode Avion
   └─ Désactivé                            ✅ OK

4. Appareils
   ├─ Appareils appairés                   ✅ 6 appareils
   ├─ Connexions actives                   ✅ 3 connectés
   └─ Conflits détectés                    ✅ Aucun

═══════════════════════════════════════════════════════════════

📊 RÉSULTAT: ✅ Aucun problème détecté

═══════════════════════════════════════════════════════════════

🛠️ PROBLÈMES COURANTS ET SOLUTIONS

Appareil non détecté lors du scan:
├─ 1. Mettre appareil en mode appairage
├─ 2. Rapprocher l'appareil (< 1m pour appairage)
├─ 3. Redémarrer Bluetooth (désactiver/réactiver)
└─ 4. Vérifier que l'appareil n'est pas déjà appairé ailleurs

Connexion qui échoue:
├─ 1. Supprimer l'appareil et réappairer
├─ 2. Redémarrer le service Bluetooth
│     Restart-Service bthserv
├─ 3. Mettre à jour pilote Bluetooth
└─ 4. Réinitialiser l'appareil Bluetooth distant

Audio Bluetooth saccadé:
├─ 1. Rapprocher du PC
├─ 2. Réduire interférences WiFi 2.4 GHz
├─ 3. Changer codec audio (SBC plus stable)
├─ 4. Fermer applications gourmandes
└─ 5. Vérifier pilotes audio

Casque connecté mais pas de son:
├─ 1. Vérifier sortie audio par défaut
│     Paramètres > Son > Sortie
├─ 2. Basculer profil A2DP ↔ HFP
├─ 3. Reconnecter l'appareil
└─ 4. Redémarrer service audio
     Restart-Service Audiosrv

═══════════════════════════════════════════════════════════════

🔄 Actions de réparation:

[1] Redémarrer services Bluetooth
[2] Réinitialiser adaptateur Bluetooth
[3] Supprimer et réappairer tous les appareils
[4] Mettre à jour pilotes Bluetooth
[5] Exécuter dépannage Windows

Choix: _
```

---

## /bluetooth settings - Paramètres

```
⚙️ PARAMÈTRES BLUETOOTH
═══════════════════════════════════════════════════════════════

📡 Adaptateur
┌─────────────────────────────────────────────────────────────┐
│ Bluetooth                    : [✅ Activé]                  │
│ Nom de l'appareil            : PC-BUREAU                    │
│ Découvrable                  : [⏱️ 2 min] [Toujours] [Jamais]│
└─────────────────────────────────────────────────────────────┘

🔗 Connexion
┌─────────────────────────────────────────────────────────────┐
│ Connexion auto appareils     : [✅ Activé]                  │
│ Autoriser téléchargement     : [☐ Désactivé]                │
│   via Bluetooth                                             │
│ Afficher icône zone notif    : [✅ Activé]                  │
│ Alerter nouvel appareil      : [✅ Activé]                  │
└─────────────────────────────────────────────────────────────┘

🔊 Audio
┌─────────────────────────────────────────────────────────────┐
│ Codec préféré                : [LDAC ▼]                     │
│ Qualité vs Latence           : [Équilibré ▼]                │
│   ○ Qualité max (latence haute)                             │
│   ● Équilibré                                               │
│   ○ Latence min (qualité réduite)                           │
│                                                             │
│ Basculer auto A2DP/HFP       : [✅ Activé]                  │
│ lors d'appels                                               │
└─────────────────────────────────────────────────────────────┘

🔒 Sécurité
┌─────────────────────────────────────────────────────────────┐
│ Niveau de sécurité           : [Élevé ▼]                    │
│ Chiffrement obligatoire      : [✅ Activé]                  │
│ Refuser appareils inconnus   : [☐ Désactivé]                │
└─────────────────────────────────────────────────────────────┘

💡 Ouvrir Paramètres Windows Bluetooth:
   ms-settings:bluetooth
```

---

## Commandes PowerShell de Référence

```powershell
# État Bluetooth
Get-PnpDevice -Class Bluetooth
Get-NetAdapter | Where-Object {$_.InterfaceDescription -like "*Bluetooth*"}

# Service Bluetooth
Get-Service bthserv, BthAvctpSvc, BTAGService
Start-Service bthserv
Restart-Service bthserv

# Appareils Bluetooth appairés
Get-PnpDevice | Where-Object {$_.Class -eq "Bluetooth"}

# Informations adaptateur
Get-PnpDevice -FriendlyName "*Bluetooth*" | Format-List *

# Activer/Désactiver Bluetooth
# Via PowerShell (nécessite module spécial ou API Windows)
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$adapter = [Windows.Devices.Bluetooth.BluetoothAdapter]::GetDefaultAsync()

# Interface utilisateur
Start-Process "ms-settings:bluetooth"
Start-Process "ms-settings:bluetooth-devices"

# Appareil audio par défaut
Get-AudioDevice -List  # Nécessite module AudioDeviceCmdlets
Set-AudioDevice -ID "{...}"  # Définir par défaut

# Supprimer appareil Bluetooth
$device = Get-PnpDevice | Where-Object {$_.FriendlyName -like "*NomAppareil*"}
pnputil /remove-device $device.InstanceId

# Pilotes Bluetooth
Get-WmiObject Win32_PnPSignedDriver | Where-Object {$_.DeviceClass -eq "Bluetooth"}
pnputil /enum-drivers /class Bluetooth

# Diagnostic
Get-WinEvent -LogName "Microsoft-Windows-Bluetooth-BthLEPrepairing/Operational" -MaxEvents 20

# Désactiver/Activer adaptateur
Disable-PnpDevice -InstanceId (Get-PnpDevice -FriendlyName "*Bluetooth*").InstanceId -Confirm:$false
Enable-PnpDevice -InstanceId (Get-PnpDevice -FriendlyName "*Bluetooth*").InstanceId -Confirm:$false

# Mode avion
Get-NetAdapterAdvancedProperty -Name "*" -DisplayName "Airplane*"
```
