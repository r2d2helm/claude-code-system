# /vpn - Gestion VPN Windows

Gestion complète des connexions VPN : configuration, diagnostic, tunnels.

## Mode d'Utilisation

```
/vpn                        # État connexions VPN
/vpn list                   # Liste toutes les connexions configurées
/vpn status                 # Détail connexion active
/vpn connect "NomVPN"       # Se connecter à un VPN
/vpn disconnect             # Déconnecter VPN actif
/vpn create                 # Assistant création VPN
/vpn delete "NomVPN"        # Supprimer une connexion
/vpn test "NomVPN"          # Tester connectivité VPN
/vpn routes                 # Table routage VPN
/vpn split                  # Configuration split tunneling
/vpn logs                   # Journaux connexion VPN
```

Arguments: $ARGUMENTS

---

## Mode Défaut - État VPN

```
🔐 VPN - ÉTAT DES CONNEXIONS
═══════════════════════════════════════════════════════════════

📡 Connexion Active
┌─────────────────────────────────────────────────────────────┐
│ VPN               : Office-VPN                              │
│ État              : 🟢 Connecté                             │
│ Serveur           : vpn.entreprise.com                      │
│ IP Tunnel         : 10.8.0.45                               │
│ Protocole         : IKEv2                                   │
│ Connecté depuis   : 2h 34m 12s                              │
│ Données           : ↓ 234 MB  ↑ 45 MB                       │
└─────────────────────────────────────────────────────────────┘

📋 Connexions Configurées
┌──────────────────────┬───────────────┬──────────┬───────────┐
│ Nom                  │ Type          │ Serveur  │ État      │
├──────────────────────┼───────────────┼──────────┼───────────┤
│ Office-VPN           │ IKEv2         │ vpn.ent..│ 🟢 Conn.  │
│ Home-Lab             │ L2TP/IPsec    │ 82.45... │ ⚪ Dispo  │
│ Cloud-AWS            │ OpenVPN       │ ec2.aws..│ ⚪ Dispo  │
│ Wireguard-Perso      │ WireGuard     │ wg.my... │ ⚪ Dispo  │
└──────────────────────┴───────────────┴──────────┴───────────┘

🔒 Services VPN
├─ IKEEXT (IKE/AuthIP)    : ✅ Running
├─ RasMan (Remote Access) : ✅ Running
├─ PolicyAgent (IPsec)    : ✅ Running
└─ WireGuard Tunnel       : ✅ Running
```

---

## /vpn status - Détail Connexion Active

```
🔐 VPN ACTIF: Office-VPN
═══════════════════════════════════════════════════════════════

📊 Informations Connexion
┌─────────────────────────────────────────────────────────────┐
│ Nom                 : Office-VPN                            │
│ État                : 🟢 Connecté                           │
│ Durée connexion     : 2h 34m 12s                            │
│ Dernier handshake   : il y a 45 secondes                    │
└─────────────────────────────────────────────────────────────┘

🌐 Configuration Réseau
┌─────────────────────────────────────────────────────────────┐
│ Serveur VPN         : vpn.entreprise.com (203.0.113.50)     │
│ Protocole           : IKEv2/IPsec                           │
│ Chiffrement         : AES-256-GCM                           │
│ Authentification    : EAP-MSCHAPv2                          │
│ Certificat          : ✅ Valide (expire: 2027-03-15)        │
│                                                             │
│ Adresse locale      : 192.168.1.100                         │
│ Adresse tunnel      : 10.8.0.45                             │
│ Passerelle          : 10.8.0.1                              │
│ DNS VPN             : 10.8.0.2, 10.8.0.3                    │
│ Masque              : 255.255.255.0                         │
└─────────────────────────────────────────────────────────────┘

📈 Statistiques
┌─────────────────────────────────────────────────────────────┐
│ Données reçues      : 234.5 MB (↓ 1.2 Mbps moyen)           │
│ Données envoyées    : 45.2 MB  (↑ 0.3 Mbps moyen)           │
│ Paquets reçus       : 185,234                               │
│ Paquets envoyés     : 42,156                                │
│ Erreurs             : 0                                     │
│ Reconnexions        : 0                                     │
└─────────────────────────────────────────────────────────────┘

🛣️ Routes Tunnel (Split Tunneling: ✅ Actif)
├─ 10.0.0.0/8        → Via tunnel (réseau interne)
├─ 172.16.0.0/12     → Via tunnel (réseau interne)
├─ 0.0.0.0/0         → Via connexion locale (Internet direct)
└─ DNS entreprise    → Via tunnel

🔧 Actions:
├─ /vpn disconnect        - Déconnecter
├─ /vpn test "Office-VPN" - Tester connectivité
└─ /vpn routes            - Voir routes complètes
```

---

## /vpn create - Assistant Création VPN

```
🆕 ASSISTANT CRÉATION VPN
═══════════════════════════════════════════════════════════════

📝 Type de VPN:

1️⃣ IKEv2/IPsec (Recommandé Windows)
   ├─ Plus rapide et stable
   ├─ Reconnexion automatique
   └─ Support mobile natif

2️⃣ L2TP/IPsec
   ├─ Compatible tous appareils
   └─ Nécessite clé pré-partagée ou certificat

3️⃣ SSTP (SSL VPN)
   ├─ Passe pare-feux restrictifs
   └─ Utilise port 443

4️⃣ PPTP (Non recommandé)
   └─ ⚠️ Obsolète, non sécurisé

Choix: [1]

═══════════════════════════════════════════════════════════════

📋 Configuration IKEv2:

Nom connexion     : [Office-VPN_____________]
Adresse serveur   : [vpn.entreprise.com_____]

Authentification:
○ EAP-MSCHAPv2 (nom d'utilisateur/mot de passe)
○ Certificat machine
● Smart Card ou certificat utilisateur

Identifiants:
Utilisateur       : [jean.dupont@entreprise.com]
Domaine           : [ENTREPRISE]

Options avancées:
☑️ Mémoriser identifiants
☑️ Reconnexion automatique
☑️ Split tunneling
☐ Utiliser passerelle par défaut

═══════════════════════════════════════════════════════════════

📋 Résumé:
┌─────────────────────────────────────────────────────────────┐
│ Nom        : Office-VPN                                     │
│ Type       : IKEv2/IPsec                                    │
│ Serveur    : vpn.entreprise.com                             │
│ Auth       : EAP-MSCHAPv2                                   │
│ Split      : Activé                                         │
└─────────────────────────────────────────────────────────────┘

⚠️ Créer cette connexion VPN? [O/N]
```

---

## /vpn test "NomVPN" - Test Connectivité

```
🔍 TEST VPN: Office-VPN
═══════════════════════════════════════════════════════════════

📡 Test de Connectivité
┌─────────────────────────────────────────────────────────────┐
│ 1. Résolution DNS serveur                                   │
│    vpn.entreprise.com → 203.0.113.50          ✅ OK         │
│                                                             │
│ 2. Connectivité serveur VPN                                 │
│    Port 500 (ISAKMP)                          ✅ Ouvert     │
│    Port 4500 (NAT-T)                          ✅ Ouvert     │
│                                                             │
│ 3. Latence serveur                                          │
│    Ping: 25ms (min: 22, max: 34, avg: 26)     ✅ OK         │
│                                                             │
│ 4. Certificat serveur                                       │
│    Émetteur: DigiCert Global Root CA          ✅ Valide     │
│    Expire: 2027-03-15                         ✅ OK         │
│                                                             │
│ 5. Services locaux                                          │
│    IKEEXT                                     ✅ Running    │
│    RasMan                                     ✅ Running    │
└─────────────────────────────────────────────────────────────┘

🌐 Test Post-Connexion (si connecté)
┌─────────────────────────────────────────────────────────────┐
│ 6. Route tunnel                                             │
│    10.8.0.0/24 via 10.8.0.1                   ✅ OK         │
│                                                             │
│ 7. DNS interne                                              │
│    srv-ad01.entreprise.local                  ✅ Résolu     │
│                                                             │
│ 8. Ressources internes                                      │
│    \\fileserver\partage                       ✅ Accessible │
│    intranet.entreprise.local                  ✅ Accessible │
└─────────────────────────────────────────────────────────────┘

📊 RÉSULTAT: ✅ Tous les tests passés - VPN opérationnel
```

---

## /vpn routes - Table Routage VPN

```
🛣️ ROUTES VPN
═══════════════════════════════════════════════════════════════

📍 Connexion: Office-VPN (10.8.0.45)

ROUTES ACTIVES VIA TUNNEL:
┌────────────────────┬─────────────────┬─────────┬─────────────┐
│ Destination        │ Masque          │ Métrique│ État        │
├────────────────────┼─────────────────┼─────────┼─────────────┤
│ 10.0.0.0           │ 255.0.0.0       │ 1       │ 🟢 Active   │
│ 172.16.0.0         │ 255.240.0.0     │ 1       │ 🟢 Active   │
│ 192.168.100.0      │ 255.255.255.0   │ 1       │ 🟢 Active   │
│ 10.8.0.0           │ 255.255.255.0   │ 1       │ 🟢 Active   │
└────────────────────┴─────────────────┴─────────┴─────────────┘

ROUTES INTERNET (connexion locale):
┌────────────────────┬─────────────────┬─────────┬─────────────┐
│ Destination        │ Passerelle      │ Métrique│ Interface   │
├────────────────────┼─────────────────┼─────────┼─────────────┤
│ 0.0.0.0            │ 192.168.1.1     │ 25      │ WiFi        │
└────────────────────┴─────────────────┴─────────┴─────────────┘

🔀 Split Tunneling: ✅ ACTIF
├─ Trafic interne (10.x, 172.16.x) → Via VPN
└─ Trafic Internet → Via connexion locale

💡 Modifier routes:
├─ Ajouter    : Add-VpnConnectionRoute -Name "Office-VPN" -DestinationPrefix "10.0.0.0/8"
└─ Supprimer  : Remove-VpnConnectionRoute -Name "Office-VPN" -DestinationPrefix "10.0.0.0/8"
```

---

## /vpn logs - Journaux VPN

```
📜 JOURNAUX VPN
═══════════════════════════════════════════════════════════════

📅 Dernières 24 heures

CONNEXIONS:
┌─────────────────────┬──────────────────┬─────────┬───────────┐
│ Date/Heure          │ VPN              │ Action  │ Durée     │
├─────────────────────┼──────────────────┼─────────┼───────────┤
│ 2026-02-03 08:15:32 │ Office-VPN       │ Connect │ En cours  │
│ 2026-02-02 22:45:10 │ Office-VPN       │ Disconn │ 8h 32m    │
│ 2026-02-02 14:12:55 │ Office-VPN       │ Connect │ -         │
│ 2026-02-02 09:00:00 │ Office-VPN       │ Auto-rec│ -         │
└─────────────────────┴──────────────────┴─────────┴───────────┘

ÉVÉNEMENTS:
├─ 08:15:35 ✅ IKE SA établi avec vpn.entreprise.com
├─ 08:15:34 ✅ Authentification EAP réussie
├─ 08:15:33 ✅ Certificat serveur validé
├─ 08:15:32 🔄 Initialisation connexion IKEv2
├─ 22:45:10 ⚪ Déconnexion utilisateur
├─ 14:13:00 ✅ Tunnel Child SA établi
├─ 09:00:05 ⚠️ Reconnexion après perte signal WiFi
└─ 09:00:00 🔴 Connexion interrompue (réseau)

ERREURS (7 jours):
├─ 2026-02-01 15:30 ❌ Échec auth - mauvais mot de passe
└─ 2026-01-29 10:15 ❌ Serveur inaccessible (timeout)
```

---

## Commandes PowerShell de Référence

```powershell
# Lister connexions VPN
Get-VpnConnection
Get-VpnConnection -AllUserConnection

# État connexion
(Get-VpnConnection -Name "NomVPN").ConnectionStatus
rasdial

# Connecter/Déconnecter
rasdial "NomVPN" username password
rasdial "NomVPN" /disconnect

# PowerShell natif
Connect-VpnConnection -Name "NomVPN"
Disconnect-VpnConnection -Name "NomVPN"

# Créer VPN IKEv2
Add-VpnConnection -Name "NomVPN" `
    -ServerAddress "vpn.server.com" `
    -TunnelType Ikev2 `
    -EncryptionLevel Required `
    -AuthenticationMethod Eap `
    -RememberCredential

# Créer VPN L2TP
Add-VpnConnection -Name "NomVPN" `
    -ServerAddress "vpn.server.com" `
    -TunnelType L2tp `
    -L2tpPsk "SharedSecret" `
    -AuthenticationMethod Pap

# Supprimer VPN
Remove-VpnConnection -Name "NomVPN" -Force

# Routes VPN (split tunneling)
Add-VpnConnectionRoute -ConnectionName "NomVPN" -DestinationPrefix "10.0.0.0/8"
Remove-VpnConnectionRoute -ConnectionName "NomVPN" -DestinationPrefix "10.0.0.0/8"
Get-VpnConnectionRoute -ConnectionName "NomVPN"

# Split tunneling complet
Set-VpnConnection -Name "NomVPN" -SplitTunneling $true

# Diagnostics
Get-Service RasMan, IKEEXT, PolicyAgent
Get-WinEvent -FilterHashtable @{LogName='Application'; ProviderName='RasClient'} -MaxEvents 20

# Test ports VPN
Test-NetConnection -ComputerName "vpn.server.com" -Port 500
Test-NetConnection -ComputerName "vpn.server.com" -Port 4500
Test-NetConnection -ComputerName "vpn.server.com" -Port 1701

# WireGuard (si installé)
& "C:\Program Files\WireGuard\wireguard.exe" /installtunnelservice "C:\path\tunnel.conf"
wg show
```
