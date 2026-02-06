# Gestion du Pare-feu Windows

Administration avancée du pare-feu Windows Defender.

## Mode d'Utilisation
```
/firewall                   → État et vue d'ensemble
/firewall rules             → Liste des règles actives
/firewall ports             → Ports ouverts et services
/firewall block "app"       → Bloquer une application
/firewall allow "app"       → Autoriser une application
/firewall logs              → Journaux du pare-feu
/firewall profiles          → Configuration par profil
/firewall export            → Sauvegarder la configuration
/firewall reset             → Réinitialiser aux valeurs par défaut
```

Arguments: $ARGUMENTS

---

## État Général (défaut)

```
🔥 PARE-FEU WINDOWS DEFENDER
═══════════════════════════════════════════════════════════════

ÉTAT PAR PROFIL:
┌─────────────┬──────────┬─────────────┬─────────────┬───────────┐
│ Profil      │ État     │ Entrant     │ Sortant     │ Actif     │
├─────────────┼──────────┼─────────────┼─────────────┼───────────┤
│ Domain      │ ✅ On    │ Bloquer     │ Autoriser   │           │
│ Private     │ ✅ On    │ Bloquer     │ Autoriser   │ ⭐ Actuel │
│ Public      │ ✅ On    │ Bloquer     │ Autoriser   │           │
└─────────────┴──────────┴─────────────┴─────────────┴───────────┘

RÉSUMÉ DES RÈGLES:
├─ Règles entrantes: 342 (89 actives)
├─ Règles sortantes: 156 (45 actives)
├─ Règles personnalisées: 12
└─ Règles bloquées: 8

CONNEXIONS RÉCENTES BLOQUÉES (si logs activés):
┌──────────────────┬───────────────┬────────┬───────────────────┐
│ Heure            │ IP Source     │ Port   │ Application       │
├──────────────────┼───────────────┼────────┼───────────────────┤
│ 10:45:12         │ 192.168.1.105 │ 445    │ -                 │
│ 10:42:08         │ 45.33.32.156  │ 3389   │ -                 │
│ 10:38:55         │ 192.168.1.1   │ 137    │ -                 │
└──────────────────┴───────────────┴────────┴───────────────────┘

ALERTES:
├─ ⚠️ Tentative RDP externe bloquée (45.33.32.156)
└─ ℹ️ Logging désactivé (activer pour plus de visibilité)
```

---

## Mode `rules`

```
📋 RÈGLES DE PARE-FEU
═══════════════════════════════════════════════════════════════

FILTRE: $ARGUMENTS
Options: all, inbound, outbound, enabled, disabled, custom, "nom"

RÈGLES ENTRANTES ACTIVES (principales):
┌────────────────────────────────────────┬────────┬───────────┬─────────┐
│ Nom                                    │ Port   │ Protocol  │ Action  │
├────────────────────────────────────────┼────────┼───────────┼─────────┤
│ Core Networking - DNS (UDP-In)         │ 53     │ UDP       │ Allow   │
│ Core Networking - DHCP (UDP-In)        │ 68     │ UDP       │ Allow   │
│ File and Printer Sharing (SMB-In)      │ 445    │ TCP       │ Allow   │
│ Remote Desktop (TCP-In)                │ 3389   │ TCP       │ Allow   │
│ Windows Remote Management (HTTP-In)    │ 5985   │ TCP       │ Allow   │
│ mDNS (UDP-In)                          │ 5353   │ UDP       │ Allow   │
│ Chrome (TCP-In)                        │ Any    │ TCP       │ Allow   │
│ Docker Desktop Backend                 │ Any    │ TCP       │ Allow   │
└────────────────────────────────────────┴────────┴───────────┴─────────┘

RÈGLES PERSONNALISÉES:
┌────────────────────────────────────────┬────────┬───────────┬─────────┐
│ Nom                                    │ Port   │ Protocol  │ Action  │
├────────────────────────────────────────┼────────┼───────────┼─────────┤
│ [Custom] Block Telemetry               │ 443    │ TCP       │ Block   │
│ [Custom] Allow PostgreSQL              │ 5432   │ TCP       │ Allow   │
│ [Custom] Block suspicious.exe          │ Any    │ Any       │ Block   │
└────────────────────────────────────────┴────────┴───────────┴─────────┘

ACTIONS:
1. Voir détails d'une règle
2. Activer/Désactiver une règle
3. Créer une nouvelle règle
4. Supprimer une règle personnalisée

Choix: _
```

---

## Mode `ports`

```
🔌 PORTS OUVERTS ET SERVICES
═══════════════════════════════════════════════════════════════

PORTS EN ÉCOUTE (LISTENING):
┌────────┬──────────┬─────────────────────────────┬────────────────────┐
│ Port   │ Protocol │ Processus                   │ Règle Pare-feu     │
├────────┼──────────┼─────────────────────────────┼────────────────────┤
│ 80     │ TCP      │ nginx.exe (12456)           │ ✅ Autorisé        │
│ 135    │ TCP      │ svchost.exe (RPC)           │ ⚠️ Privé seulement │
│ 443    │ TCP      │ nginx.exe (12456)           │ ✅ Autorisé        │
│ 445    │ TCP      │ System (SMB)                │ ⚠️ Privé seulement │
│ 3000   │ TCP      │ node.exe (15678)            │ ❌ Non autorisé    │
│ 3389   │ TCP      │ svchost.exe (RDP)           │ ⚠️ Privé seulement │
│ 5432   │ TCP      │ postgres.exe (9876)         │ ✅ Autorisé        │
│ 5985   │ TCP      │ svchost.exe (WinRM)         │ ⚠️ Privé seulement │
│ 6379   │ TCP      │ redis-server.exe            │ ❌ Non autorisé    │
│ 8080   │ TCP      │ java.exe (23456)            │ ❌ Non autorisé    │
└────────┴──────────┴─────────────────────────────┴────────────────────┘

LÉGENDE:
├─ ✅ Autorisé: Règle entrante active pour tous les profils
├─ ⚠️ Privé seulement: Autorisé uniquement sur réseau privé
└─ ❌ Non autorisé: Aucune règle entrante (bloqué par défaut)

PORTS SENSIBLES DÉTECTÉS:
├─ 🔴 Port 3389 (RDP) - Exposé sur réseau privé
├─ 🟠 Port 445 (SMB) - Vérifier si nécessaire
└─ 🟠 Port 135 (RPC) - Exposé localement

ACTIONS:
1. Créer une règle pour autoriser un port
2. Bloquer un port spécifique
3. Voir les connexions établies
```

---

## Mode `block/allow "app"`

```
🚫 BLOQUER UNE APPLICATION
═══════════════════════════════════════════════════════════════

Application: $ARGUMENTS

RECHERCHE DE L'APPLICATION...

TROUVÉ:
├─ Nom: suspicious-app.exe
├─ Chemin: C:\Users\Jean\Downloads\suspicious-app.exe
├─ Éditeur: Non signé ⚠️
├─ Processus actif: Non
└─ Règles existantes: Aucune

CRÉER UNE RÈGLE DE BLOCAGE:

Direction:
[x] Entrant (connexions vers cette app)
[x] Sortant (connexions depuis cette app)

Profils:
[x] Domain
[x] Private  
[x] Public

Nom de la règle: Block_suspicious-app

⚠️ Cette règle va empêcher l'application de:
├─ Recevoir des connexions entrantes
└─ Établir des connexions sortantes (Internet)

Créer la règle? [O/N]

---

✅ AUTORISER UNE APPLICATION
═══════════════════════════════════════════════════════════════

Application: node.exe

TROUVÉ:
├─ Chemin: C:\Program Files\nodejs\node.exe
├─ Éditeur: Node.js Foundation ✅
└─ Règles existantes: 1 (sortant uniquement)

CRÉER UNE RÈGLE D'AUTORISATION:

Direction: [Entrant]
Port(s): [Spécifique: 3000] ou [Tous]
Profils: [Private uniquement] - Recommandé

Nom de la règle: Allow_Node_Dev_Server

Créer la règle? [O/N]
```

---

## Mode `logs`

```
📋 JOURNAUX DU PARE-FEU
═══════════════════════════════════════════════════════════════

ÉTAT DU LOGGING:
├─ Logging des paquets autorisés: ❌ Désactivé
├─ Logging des paquets bloqués: ❌ Désactivé
├─ Fichier log: %systemroot%\system32\LogFiles\Firewall\pfirewall.log
└─ Taille max: 4096 KB

⚠️ Le logging est désactivé. Activer pour voir l'activité.

ACTIVER LE LOGGING:
1. [drops] Logger uniquement les paquets bloqués (recommandé)
2. [success] Logger uniquement les paquets autorisés
3. [all] Logger tout (génère beaucoup de données)

Choix: _

---

(Si logging activé)

DERNIÈRES ENTRÉES:
┌──────────────────┬────────┬────────────────┬────────────────┬────────┐
│ Date/Heure       │ Action │ Source         │ Destination    │ Port   │
├──────────────────┼────────┼────────────────┼────────────────┼────────┤
│ 10:45:12         │ DROP   │ 45.33.32.156   │ 192.168.1.45   │ 3389   │
│ 10:45:10         │ DROP   │ 45.33.32.156   │ 192.168.1.45   │ 22     │
│ 10:44:58         │ DROP   │ 192.168.1.105  │ 192.168.1.45   │ 445    │
│ 10:44:30         │ ALLOW  │ 192.168.1.45   │ 8.8.8.8        │ 53     │
│ 10:44:25         │ ALLOW  │ 192.168.1.45   │ 151.101.1.140  │ 443    │
└──────────────────┴────────┴────────────────┴────────────────┴────────┘

STATISTIQUES (dernière heure):
├─ Paquets bloqués: 156
├─ Paquets autorisés: 12,456
├─ IP sources bloquées uniques: 8
└─ Tentatives suspectes: 3 (RDP scans)

TOP IP BLOQUÉES:
├─ 45.33.32.156 - 45 tentatives (scan de ports)
├─ 185.220.100.252 - 23 tentatives
└─ 192.168.1.105 - 12 tentatives (SMB)
```

---

## Mode `profiles`

```
⚙️ CONFIGURATION PAR PROFIL
═══════════════════════════════════════════════════════════════

PROFIL ACTUEL: Private ⭐

┌─────────────────────────────────────────────────────────────────────────┐
│ DOMAIN PROFILE (Réseau d'entreprise)                                    │
├─────────────────────────────────────────────────────────────────────────┤
│ État: ✅ Activé                                                         │
│ Comportement entrant: Bloquer (par défaut)                             │
│ Comportement sortant: Autoriser (par défaut)                           │
│ Connexions sécurisées: Bloquer si non sécurisé                         │
│ Notifications: Oui                                                      │
│ Logging: Non                                                            │
├─────────────────────────────────────────────────────────────────────────┤
│ PRIVATE PROFILE (Réseau domestique/travail) ⭐                         │
├─────────────────────────────────────────────────────────────────────────┤
│ État: ✅ Activé                                                         │
│ Comportement entrant: Bloquer (par défaut)                             │
│ Comportement sortant: Autoriser (par défaut)                           │
│ Connexions sécurisées: Bloquer si non sécurisé                         │
│ Notifications: Oui                                                      │
│ Logging: Non                                                            │
├─────────────────────────────────────────────────────────────────────────┤
│ PUBLIC PROFILE (Réseau public - café, aéroport) 🔒                     │
├─────────────────────────────────────────────────────────────────────────┤
│ État: ✅ Activé                                                         │
│ Comportement entrant: Bloquer tout                                      │
│ Comportement sortant: Autoriser (par défaut)                           │
│ Connexions sécurisées: Bloquer si non sécurisé                         │
│ Notifications: Non (silencieux)                                         │
│ Logging: Non                                                            │
└─────────────────────────────────────────────────────────────────────────┘

MODIFIER UN PROFIL:
1. Changer le comportement par défaut
2. Activer/désactiver le logging
3. Configurer les notifications
4. Basculer le réseau actuel vers un autre profil
```

---

## Mode `export/reset`

```
💾 EXPORT CONFIGURATION PARE-FEU
═══════════════════════════════════════════════════════════════

Cette action va sauvegarder:
├─ Toutes les règles (système et personnalisées)
├─ Configuration des profils
├─ Paramètres de logging
└─ Règles de sécurité de connexion

Format: .wfw (Windows Firewall with Advanced Security)
Destination: C:\Backups\firewall-backup-2026-02-03.wfw

Exporter? [O/N]

---

🔄 RÉINITIALISATION PARE-FEU
═══════════════════════════════════════════════════════════════

⚠️ ATTENTION: Cette action va:
├─ Supprimer TOUTES les règles personnalisées
├─ Restaurer les règles par défaut de Windows
├─ Réinitialiser tous les profils
└─ Activer le pare-feu sur tous les profils

Vos règles personnalisées actuelles:
├─ [Custom] Block Telemetry
├─ [Custom] Allow PostgreSQL
└─ [Custom] Block suspicious.exe

💡 Conseil: Exportez d'abord la configuration actuelle

Réinitialiser le pare-feu? [O/N]
(Tapez RESET pour confirmer)
```

---

## Commandes de Référence

```powershell
# État du pare-feu
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction

# Liste des règles
Get-NetFirewallRule | Where-Object {$_.Enabled -eq 'True'} | Select-Object DisplayName, Direction, Action

# Ports en écoute
Get-NetTCPConnection -State Listen | Select-Object LocalPort, OwningProcess

# Créer une règle
New-NetFirewallRule -DisplayName "Allow App" -Direction Inbound -Program "C:\app.exe" -Action Allow

# Bloquer une application
New-NetFirewallRule -DisplayName "Block App" -Direction Outbound -Program "C:\app.exe" -Action Block

# Activer/désactiver une règle
Enable-NetFirewallRule -DisplayName "Nom"
Disable-NetFirewallRule -DisplayName "Nom"

# Logging
Set-NetFirewallProfile -Profile Private -LogBlocked True -LogFileName "C:\Logs\firewall.log"

# Export/Import
netsh advfirewall export "C:\backup.wfw"
netsh advfirewall import "C:\backup.wfw"

# Réinitialiser
netsh advfirewall reset
```
