# Gestion Remote Desktop (RDP)

Administration du Bureau à distance Windows.

## Mode d'Utilisation
```
/rdp                        → État et configuration RDP
/rdp enable                 → Activer le Bureau à distance
/rdp disable                → Désactiver le Bureau à distance
/rdp sessions               → Sessions actives et historique
/rdp users                  → Gérer les utilisateurs autorisés
/rdp firewall               → Configuration pare-feu RDP
/rdp security               → Paramètres de sécurité
/rdp gateway                → Configuration RD Gateway
/rdp troubleshoot           → Dépannage connexions RDP
```

Arguments: $ARGUMENTS

---

## État Général (défaut)

```
🖥️ REMOTE DESKTOP - ÉTAT GÉNÉRAL
═══════════════════════════════════════════════════════════════

STATUT RDP:
├─ Bureau à distance: ✅ Activé
├─ Service TermService: ✅ Running
├─ Port d'écoute: 3389
├─ NLA (Network Level Auth): ✅ Requis
└─ Certificat: Auto-signé (expire: 2027-01-15)

RÉSEAU:
├─ Écoute sur: 0.0.0.0:3389
├─ Pare-feu Windows: ✅ Règle active (profil: Private)
├─ IP locale: 192.168.1.45
└─ Nom d'hôte: DESKTOP-ABC123

UTILISATEURS AUTORISÉS:
├─ Administrateurs (groupe)
├─ Remote Desktop Users:
│  ├─ Jean.Dupont
│  └─ Marie.Martin
└─ Total: 2 utilisateurs + admins

SESSIONS:
┌───────┬────────────────┬─────────────┬───────────────┬──────────┐
│ ID    │ Utilisateur    │ État        │ Depuis        │ Client   │
├───────┼────────────────┼─────────────┼───────────────┼──────────┤
│ 1     │ Jean.Dupont    │ Active      │ 09:15         │ Console  │
│ 2     │ Marie.Martin   │ Disconnected│ Hier 18:30    │ RDP      │
└───────┴────────────────┴─────────────┴───────────────┴──────────┘

ALERTES:
├─ ⚠️ Session déconnectée depuis 14h (Marie.Martin)
└─ ℹ️ Certificat auto-signé (considérer certificat CA)
```

---

## Mode `enable/disable`

```
✅ ACTIVER LE BUREAU À DISTANCE
═══════════════════════════════════════════════════════════════

Cette action va:
├─ Activer le service Bureau à distance
├─ Ouvrir le port 3389 dans le pare-feu (profil: Private)
├─ Activer l'authentification NLA (recommandé)
└─ Permettre les connexions à distance

OPTIONS DE SÉCURITÉ:
[x] Exiger NLA (Network Level Authentication)
[x] Autoriser uniquement profil réseau "Private"
[ ] Autoriser également profil "Public" (⚠️ non recommandé)

⚠️ AVERTISSEMENT SÉCURITÉ:
├─ N'exposez JAMAIS RDP directement sur Internet
├─ Utilisez un VPN ou RD Gateway pour l'accès externe
└─ Limitez les utilisateurs autorisés

Activer le Bureau à distance? [O/N]

---

❌ DÉSACTIVER LE BUREAU À DISTANCE
═══════════════════════════════════════════════════════════════

Cette action va:
├─ Désactiver le service Bureau à distance
├─ Fermer le port 3389 dans le pare-feu
└─ Déconnecter toutes les sessions actives

⚠️ Sessions actives qui seront déconnectées:
└─ Marie.Martin (déconnectée depuis 14h)

Désactiver? [O/N]
```

---

## Mode `sessions`

```
📋 SESSIONS REMOTE DESKTOP
═══════════════════════════════════════════════════════════════

SESSIONS ACTIVES:
┌──────────────────────────────────────────────────────────────────────┐
│ Session #1 - Jean.Dupont                                             │
├──────────────────────────────────────────────────────────────────────┤
│ État: ✅ Active                                                      │
│ Type: Console (local)                                                │
│ Connecté depuis: 2026-02-03 09:15                                   │
│ Idle: 5 minutes                                                      │
│ Résolution: 1920x1080                                               │
│ Client: Local                                                        │
├──────────────────────────────────────────────────────────────────────┤
│ Session #2 - Marie.Martin                                            │
├──────────────────────────────────────────────────────────────────────┤
│ État: 🔌 Disconnected                                                │
│ Type: RDP                                                            │
│ Connecté: 2026-02-02 18:30 | Déconnecté: 2026-02-02 18:45           │
│ Idle: 14 heures                                                      │
│ Client: LAPTOP-XYZ (192.168.1.100)                                  │
└──────────────────────────────────────────────────────────────────────┘

ACTIONS:
1. Envoyer un message à un utilisateur
2. Déconnecter une session (garde programmes ouverts)
3. Fermer une session (logoff)
4. Shadow (observer/contrôler une session)

Choix: _

---

HISTORIQUE DES CONNEXIONS (7 jours):
┌──────────────────┬────────────────┬─────────────┬───────────────────┐
│ Date             │ Utilisateur    │ Client      │ Résultat          │
├──────────────────┼────────────────┼─────────────┼───────────────────┤
│ 2026-02-03 09:15 │ Jean.Dupont    │ Console     │ ✅ Succès         │
│ 2026-02-02 18:30 │ Marie.Martin   │ LAPTOP-XYZ  │ ✅ Succès         │
│ 2026-02-02 15:00 │ admin          │ 192.168.1.55│ ❌ Échec (pwd)    │
│ 2026-02-01 10:00 │ Marie.Martin   │ LAPTOP-XYZ  │ ✅ Succès         │
└──────────────────┴────────────────┴─────────────┴───────────────────┘

⚠️ Tentative échouée détectée (admin depuis 192.168.1.55)
```

---

## Mode `users`

```
👥 UTILISATEURS RDP AUTORISÉS
═══════════════════════════════════════════════════════════════

GROUPE "Remote Desktop Users":
┌────────────────┬─────────────────────────────────────────────┐
│ Utilisateur    │ Dernière connexion RDP                      │
├────────────────┼─────────────────────────────────────────────┤
│ Jean.Dupont    │ 2026-02-03 09:15 (active)                   │
│ Marie.Martin   │ 2026-02-02 18:30                            │
└────────────────┴─────────────────────────────────────────────┘

ADMINISTRATEURS (accès automatique):
├─ Administrateur (désactivé)
└─ Jean.Dupont

ACTIONS:
1. Ajouter un utilisateur au groupe RDP
2. Retirer un utilisateur du groupe RDP
3. Voir les tentatives de connexion par utilisateur

Choix: _

---

AJOUTER UN UTILISATEUR:
Nom d'utilisateur: _____

⚠️ Vérifications:
├─ L'utilisateur existe: ✅
├─ Compte actif: ✅
├─ Mot de passe défini: ✅
└─ Déjà membre: ❌

Ajouter au groupe "Remote Desktop Users"? [O/N]
```

---

## Mode `security`

```
🔐 SÉCURITÉ REMOTE DESKTOP
═══════════════════════════════════════════════════════════════

CONFIGURATION ACTUELLE:
┌─────────────────────────────────────────┬─────────┬────────────┐
│ Paramètre                               │ Valeur  │ Recommandé │
├─────────────────────────────────────────┼─────────┼────────────┤
│ Network Level Authentication (NLA)      │ ✅ Oui  │ ✅ Oui     │
│ Niveau de chiffrement                   │ High    │ High       │
│ Certificat                              │ Auto    │ CA signé   │
│ Port RDP                                │ 3389    │ Personnalisé│
│ Verrouillage après échecs              │ ❌ Non  │ ✅ Oui     │
│ Timeout session inactive                │ ❌ Aucun│ 30 min     │
│ Déconnexion sessions déconnectées      │ ❌ Jamais│ 1 jour     │
└─────────────────────────────────────────┴─────────┴────────────┘

SCORE SÉCURITÉ: 65/100 ⚠️

RECOMMANDATIONS:
1. 🔴 Changer le port par défaut (3389)
   → Réduit les attaques automatisées
   → Nouveau port suggéré: 33890

2. 🟠 Activer le verrouillage de compte
   → Verrouiller après 5 tentatives échouées
   → Durée: 30 minutes

3. 🟠 Configurer timeout de session
   → Déconnecter sessions inactives > 30 min
   → Fermer sessions déconnectées > 24h

4. 🟡 Utiliser un certificat signé
   → Évite les avertissements de sécurité
   → Vérifie l'identité du serveur

5. 🟢 NLA déjà activé ✅

APPLIQUER LES RECOMMANDATIONS:
[ ] 1. Changer le port RDP
[ ] 2. Activer verrouillage de compte
[ ] 3. Configurer timeouts
[ ] Tout appliquer

Sélection: _
```

---

## Mode `firewall`

```
🔥 PARE-FEU - RÈGLES RDP
═══════════════════════════════════════════════════════════════

RÈGLES ACTUELLES:
┌─────────────────────────────────────────┬─────────┬───────────┐
│ Règle                                   │ Profils │ État      │
├─────────────────────────────────────────┼─────────┼───────────┤
│ Bureau à distance (TCP-In)              │ Private │ ✅ Activée│
│ Bureau à distance (UDP-In)              │ Private │ ✅ Activée│
│ Bureau à distance - Shadow (TCP-In)     │ Private │ ❌ Désact.│
└─────────────────────────────────────────┴─────────┴───────────┘

DÉTAILS DE LA RÈGLE PRINCIPALE:
├─ Port: 3389/TCP
├─ Action: Autoriser
├─ Profils: Private uniquement
├─ Adresses distantes: Toutes
└─ Programme: %SystemRoot%\system32\svchost.exe

RECOMMANDATIONS SÉCURITÉ:
⚠️ La règle autorise TOUTES les adresses distantes.

OPTIONS:
1. Restreindre aux adresses IP spécifiques
   → Ex: 192.168.1.0/24 (réseau local uniquement)
   
2. Activer pour le profil "Domain"
   → Si ordinateur joint à un domaine AD

3. Désactiver pour le profil "Public"
   → ✅ Déjà désactivé (bonne pratique)

4. Activer le logging des connexions bloquées

Appliquer restriction IP:
IP/Subnet autorisées: _____
(ex: 192.168.1.0/24, 10.0.0.100)
```

---

## Mode `troubleshoot`

```
🔧 DÉPANNAGE REMOTE DESKTOP
═══════════════════════════════════════════════════════════════

DIAGNOSTIC EN COURS...

SERVICE RDP:
├─ TermService: ✅ Running
├─ SessionEnv: ✅ Running
├─ UmRdpService: ✅ Running
└─ Port 3389 en écoute: ✅

CONFIGURATION:
├─ RDP activé: ✅
├─ NLA requis: ✅
├─ Utilisateurs autorisés: 2
└─ Certificat valide: ✅

RÉSEAU:
├─ Pare-feu règle active: ✅
├─ Port 3389 accessible (local): ✅
├─ IP locale: 192.168.1.45
└─ Ping gateway: ✅

TEST DE CONNEXION LOCALE:
├─ Connexion localhost:3389: ✅ OK
└─ Handshake TLS: ✅ OK

PROBLÈMES COURANTS:

1. "Le PC distant n'est pas accessible"
   ├─ Vérifier que le PC cible est allumé
   ├─ Vérifier la connectivité réseau (ping)
   ├─ Vérifier le pare-feu (port 3389)
   └─ Commande: Test-NetConnection -ComputerName <IP> -Port 3389

2. "Connexion refusée"
   ├─ Vérifier que RDP est activé sur le PC cible
   ├─ Vérifier les droits utilisateur
   └─ Vérifier NLA (essayer sans si problème)

3. "Certificat non approuvé"
   ├─ Normal avec certificat auto-signé
   ├─ Ajouter l'exception ou installer certificat CA
   └─ Option: Désactiver vérification (non recommandé)

4. "CredSSP encryption oracle"
   ├─ Mise à jour de sécurité incompatible
   └─ Mettre à jour les deux machines

5. "Session se déconnecte immédiatement"
   ├─ Vérifier les licences RDS (si serveur)
   ├─ Vérifier les GPO de session
   └─ Vérifier le profil utilisateur

RÉSULTAT: ✅ Aucun problème détecté
Service prêt à accepter les connexions.
```

---

## Commandes de Référence

```powershell
# Activer/Désactiver RDP
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0  # Activer
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 1  # Désactiver

# Activer NLA
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "UserAuthentication" -Value 1

# Sessions
query session
query user
logoff <session_id>
msg <user> "Message"

# Ajouter utilisateur au groupe RDP
Add-LocalGroupMember -Group "Remote Desktop Users" -Member "NomUtilisateur"

# Pare-feu
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
Get-NetFirewallRule -DisplayName "*Remote Desktop*"

# Changer le port RDP
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "PortNumber" -Value 33890

# Test connexion
Test-NetConnection -ComputerName <IP> -Port 3389

# Événements
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-TerminalServices-LocalSessionManager/Operational'} -MaxEvents 50
```
