# /wifi - Gestion WiFi et Réseaux Sans Fil

Gestion complète du WiFi : connexions, profils, diagnostic, sécurité.

## Mode d'Utilisation

```
/wifi                       # État WiFi actuel
/wifi scan                  # Scanner réseaux disponibles
/wifi connect "SSID"        # Se connecter à un réseau
/wifi disconnect            # Déconnecter WiFi actuel
/wifi profiles              # Lister profils enregistrés
/wifi password "SSID"       # Afficher mot de passe d'un profil
/wifi forget "SSID"         # Supprimer un profil
/wifi hotspot               # Configurer point d'accès mobile
/wifi analyze               # Analyse canaux et interférences
/wifi troubleshoot          # Dépannage WiFi
/wifi drivers               # Info pilotes WiFi
/wifi export                # Exporter profils WiFi
```

Arguments: $ARGUMENTS

---

## Mode Défaut - État WiFi

```
📶 WIFI - ÉTAT ACTUEL
═══════════════════════════════════════════════════════════════

🔌 Adaptateur WiFi
┌─────────────────────────────────────────────────────────────┐
│ Adaptateur         : Intel Wi-Fi 6 AX201 160MHz             │
│ État               : ✅ Connecté                            │
│ MAC                : A4:C3:F0:XX:XX:XX                      │
│ Mode               : Infrastructure                         │
│ Radio              : ✅ Activé                              │
└─────────────────────────────────────────────────────────────┘

📡 Connexion Actuelle
┌─────────────────────────────────────────────────────────────┐
│ SSID               : Maison-5G                              │
│ Bande              : 5 GHz (802.11ax)                       │
│ Canal              : 36 (5180 MHz)                          │
│ Signal             : ████████░░ 85% (Excellent)             │
│ Vitesse liaison    : 1201 Mbps                              │
│ Sécurité           : WPA3-Personal                          │
│ BSSID              : 00:1A:2B:XX:XX:XX                      │
│ Connecté depuis    : 2h 15m                                 │
└─────────────────────────────────────────────────────────────┘

🌐 Configuration IP
├─ Adresse IPv4      : 192.168.1.100
├─ Masque            : 255.255.255.0
├─ Passerelle        : 192.168.1.1
├─ DNS               : 192.168.1.1, 8.8.8.8
└─ DHCP              : ✅ Activé

📊 Statistiques Session
├─ Données reçues    : 1.2 GB
├─ Données envoyées  : 345 MB
├─ Paquets perdus    : 0.01%
└─ Latence passerelle: 2ms
```

---

## /wifi scan - Réseaux Disponibles

```
🔍 RÉSEAUX WIFI DISPONIBLES
═══════════════════════════════════════════════════════════════

Scan: 12 réseaux détectés

5 GHz (moins d'interférences, plus rapide):
┌──────────────────────┬────────┬───────┬──────────┬──────────┐
│ SSID                 │ Signal │ Canal │ Sécurité │ Vitesse  │
├──────────────────────┼────────┼───────┼──────────┼──────────┤
│ ★ Maison-5G          │ 85%    │ 36    │ WPA3     │ 1201 Mbps│
│   Office-Guest       │ 72%    │ 44    │ WPA2     │ 867 Mbps │
│   Voisin-5G          │ 45%    │ 149   │ WPA2     │ 433 Mbps │
│   FreeWifi_secure    │ 38%    │ 36    │ WPA2-Ent │ 867 Mbps │
└──────────────────────┴────────┴───────┴──────────┴──────────┘

2.4 GHz (meilleure portée):
┌──────────────────────┬────────┬───────┬──────────┬──────────┐
│ SSID                 │ Signal │ Canal │ Sécurité │ Bande    │
├──────────────────────┼────────┼───────┼──────────┼──────────┤
│   Maison-2G          │ 92%    │ 6     │ WPA3     │ 802.11n  │
│   Livebox-A3F2       │ 55%    │ 1     │ WPA2     │ 802.11n  │
│   DIRECT-TV-Samsung  │ 48%    │ 6     │ WPA2     │ 802.11n  │
│   Freebox-B1C3       │ 42%    │ 11    │ WPA2     │ 802.11n  │
│   AndroidAP          │ 35%    │ 6     │ WPA2     │ 802.11n  │
│   ⚠️ OPEN_NETWORK    │ 30%    │ 1     │ Aucune   │ 802.11n  │
│   HP-Print-A1        │ 25%    │ 6     │ WPA2     │ 802.11n  │
│   🔒 Réseau masqué   │ 20%    │ 11    │ WPA2     │ -        │
└──────────────────────┴────────┴───────┴──────────┴──────────┘

★ = Connecté actuellement
⚠️ = Réseau ouvert (non sécurisé)
🔒 = SSID masqué
```

---

## /wifi profiles - Profils Enregistrés

```
📋 PROFILS WIFI ENREGISTRÉS
═══════════════════════════════════════════════════════════════

┌──────────────────────┬───────────┬──────────┬─────────────────┐
│ SSID                 │ Sécurité  │ Auto     │ Dernière connex.│
├──────────────────────┼───────────┼──────────┼─────────────────┤
│ ★ Maison-5G          │ WPA3      │ ✅ Oui   │ Maintenant      │
│   Maison-2G          │ WPA3      │ ✅ Oui   │ Hier            │
│   Office-Entreprise  │ WPA2-Ent  │ ✅ Oui   │ 2026-01-31      │
│   Hotel-Paris        │ WPA2      │ ❌ Non   │ 2026-01-15      │
│   Starbucks-Guest    │ Ouvert    │ ❌ Non   │ 2025-12-20      │
│   AirportFree        │ Captive   │ ❌ Non   │ 2025-11-05      │
└──────────────────────┴───────────┴──────────┴─────────────────┘

Total: 6 profils (45 KB)

💡 Actions:
├─ /wifi password "SSID"  - Voir mot de passe
├─ /wifi forget "SSID"    - Supprimer profil
└─ /wifi export           - Sauvegarder tous les profils
```

---

## /wifi password "SSID" - Afficher Mot de Passe

```
🔑 MOT DE PASSE WIFI: Maison-5G
═══════════════════════════════════════════════════════════════

⚠️ Information sensible - ne pas partager publiquement

┌─────────────────────────────────────────────────────────────┐
│ SSID               : Maison-5G                              │
│ Type sécurité      : WPA3-Personal                          │
│ Chiffrement        : AES-CCMP                               │
│                                                             │
│ Mot de passe       : MonSuperM0tDePasse!2024                │
│                                                             │
│ Type clé           : Clé réseau                             │
└─────────────────────────────────────────────────────────────┘

📋 Copié dans le presse-papiers

💡 QR Code pour partage:
┌─────────────────────────────────────────────────────────────┐
│  ██████████████  ████  ██████████████                       │
│  ██          ██  ██    ██          ██                       │
│  ██  ██████  ████████████  ██████  ██                       │
│  ██  ██████  ██  ██  ████  ██████  ██                       │
│  ...                                                        │
└─────────────────────────────────────────────────────────────┘
Scanner avec téléphone pour connecter automatiquement
```

---

## /wifi analyze - Analyse Canaux

```
📊 ANALYSE WIFI - CANAUX ET INTERFÉRENCES
═══════════════════════════════════════════════════════════════

🔵 BANDE 2.4 GHz
┌─────────────────────────────────────────────────────────────┐
│ Canal  1    2    3    4    5    6    7    8    9   10   11  │
│        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                     │
│ Réseaux: 2       Chevauchement avec canaux 1-5              │
│                                                             │
│                             ████████████████████            │
│                       Réseaux: 5  (ENCOMBRÉ!)               │
│                                                             │
│                                          ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │
│                                   Réseaux: 2                │
└─────────────────────────────────────────────────────────────┘

Occupation canaux 2.4 GHz:
├─ Canal 1  : ██░░░░░░░░ 20% (2 réseaux)
├─ Canal 6  : ██████████ 100% (5 réseaux) ⚠️ Saturé
├─ Canal 11 : ██░░░░░░░░ 20% (2 réseaux)
└─ Recommandation: Utiliser Canal 1 ou 11

🟢 BANDE 5 GHz
┌─────────────────────────────────────────────────────────────┐
│ Canal 36  40  44  48 | 52  56  60  64 | 149 153 157 161 165 │
│       ████                                                  │
│       2 réseaux                                             │
│                 ██                                          │
│                 1 réseau                                    │
│                                         ██                  │
│                                         1 réseau            │
└─────────────────────────────────────────────────────────────┘

Occupation canaux 5 GHz:
├─ Canal 36 : ██░░░░░░░░ 20% (2 réseaux) ← Vous êtes ici
├─ Canal 44 : █░░░░░░░░░ 10% (1 réseau)
├─ Canal 149: █░░░░░░░░░ 10% (1 réseau)
└─ Canaux DFS (52-64): Libres mais risque radar

📈 QUALITÉ SIGNAL DANS LE TEMPS (5 dernières minutes)
┌─────────────────────────────────────────────────────────────┐
│ 100% │                    ████████                          │
│  80% │ ████████████████████        ████████████████████     │
│  60% │                                                      │
│  40% │                                                      │
│  20% │                                                      │
│      └──────────────────────────────────────────────────────│
│        1min          2min         3min         4min    5min │
└─────────────────────────────────────────────────────────────┘

🎯 RECOMMANDATIONS:
├─ ✅ Bon choix de canal 5 GHz (36) - peu encombré
├─ ⚠️ 2.4 GHz canal 6 très saturé - éviter
└─ 💡 Pour meilleure performance: rester sur 5 GHz
```

---

## /wifi hotspot - Point d'Accès Mobile

```
📱 POINT D'ACCÈS MOBILE
═══════════════════════════════════════════════════════════════

📊 État Actuel: ❌ Désactivé

CONFIGURATION:
┌─────────────────────────────────────────────────────────────┐
│ Nom réseau (SSID)  : MonPC-Hotspot                          │
│ Mot de passe       : ********** (8+ caractères)             │
│ Bande              : 5 GHz (recommandé)                     │
│ Partage connexion  : Ethernet                               │
│ Appareils max      : 8                                      │
└─────────────────────────────────────────────────────────────┘

🔧 Actions:
├─ [1] Activer le hotspot
├─ [2] Modifier le nom/mot de passe
├─ [3] Changer la bande (2.4/5 GHz)
└─ [4] Voir appareils connectés

═══════════════════════════════════════════════════════════════

📱 HOTSPOT ACTIF (si activé):
┌─────────────────────────────────────────────────────────────┐
│ État               : 🟢 Actif                               │
│ SSID               : MonPC-Hotspot                          │
│ Bande              : 5 GHz                                  │
│ Canal              : 36                                     │
│                                                             │
│ Appareils connectés (2/8):                                  │
│ ├─ iPhone-Jean     : 192.168.137.10 (45 min)               │
│ └─ iPad-Bureau     : 192.168.137.11 (12 min)               │
│                                                             │
│ Données partagées  : ↓ 234 MB  ↑ 45 MB                     │
└─────────────────────────────────────────────────────────────┘
```

---

## /wifi troubleshoot - Dépannage

```
🔧 DÉPANNAGE WIFI
═══════════════════════════════════════════════════════════════

📋 DIAGNOSTIC AUTOMATIQUE

1. Adaptateur WiFi
   ├─ Présent                              ✅ OK
   ├─ Pilote installé                      ✅ OK
   ├─ Radio activée                        ✅ OK
   └─ État adaptateur                      ✅ Fonctionnel

2. Connexion Réseau
   ├─ Profil enregistré                    ✅ Oui
   ├─ Association SSID                     ✅ Connecté
   ├─ Authentification                     ✅ Réussie
   └─ Signal                               ✅ 85% (Bon)

3. Configuration IP
   ├─ DHCP                                 ✅ Activé
   ├─ Adresse IP obtenue                   ✅ 192.168.1.100
   ├─ Passerelle                           ✅ Accessible
   └─ DNS                                  ✅ Fonctionnel

4. Connectivité Internet
   ├─ Ping passerelle                      ✅ 2ms
   ├─ Ping DNS public                      ✅ 15ms
   ├─ Résolution DNS                       ✅ OK
   └─ Accès Internet                       ✅ OK

═══════════════════════════════════════════════════════════════

📊 RÉSULTAT: ✅ Aucun problème détecté

═══════════════════════════════════════════════════════════════

Si problème détecté, solutions proposées:

PROBLÈME: Signal faible
├─ Rapprocher du routeur
├─ Vérifier obstacles (murs épais, métal)
├─ Changer de bande (2.4 GHz = meilleure portée)
└─ Envisager répéteur WiFi

PROBLÈME: Déconnexions fréquentes
├─ Mettre à jour pilotes: /wifi drivers
├─ Désactiver économie d'énergie adaptateur
├─ Changer canal routeur (interférences)
└─ Oublier et reconnecter profil

PROBLÈME: Pas d'adresse IP
├─ netsh winsock reset
├─ ipconfig /release && ipconfig /renew
├─ Vérifier DHCP routeur
└─ Configurer IP statique
```

---

## Commandes PowerShell de Référence

```powershell
# État WiFi
netsh wlan show interfaces
Get-NetAdapter -Name "Wi-Fi" | Format-List *

# Scanner réseaux
netsh wlan show networks mode=bssid
explorer.exe ms-availablenetworks:

# Profils
netsh wlan show profiles
netsh wlan show profile name="SSID" key=clear

# Connecter/Déconnecter
netsh wlan connect name="SSID" ssid="SSID"
netsh wlan disconnect

# Supprimer profil
netsh wlan delete profile name="SSID"

# Exporter/Importer profils
netsh wlan export profile folder="C:\WiFiBackup" key=clear
netsh wlan add profile filename="profile.xml"

# Hotspot mobile
netsh wlan set hostednetwork mode=allow ssid="NomHotspot" key="MotDePasse"
netsh wlan start hostednetwork
netsh wlan stop hostednetwork

# Windows 10/11 Mobile Hotspot
# Via Paramètres > Réseau > Point d'accès mobile
# Ou PowerShell (API)
[Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager]::CreateFromConnectionProfile(...)

# Diagnostic
netsh wlan show drivers
netsh wlan show wlanreport
# Génère rapport HTML dans C:\ProgramData\Microsoft\Windows\WlanReport\

# Réinitialiser WiFi
netsh winsock reset
netsh int ip reset
ipconfig /release
ipconfig /renew
ipconfig /flushdns

# Pilotes
Get-NetAdapter -Name "Wi-Fi" | Get-NetAdapterAdvancedProperty
pnputil /enum-drivers /class Net

# Désactiver économie énergie
$adapter = Get-NetAdapter -Name "Wi-Fi"
Set-NetAdapterPowerManagement -Name $adapter.Name -AllowComputerToTurnOffDevice Disabled
```
