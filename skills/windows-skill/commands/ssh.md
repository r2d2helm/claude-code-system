# Gestion SSH (OpenSSH Windows)

Administration du serveur et client SSH Windows.

## Mode d'Utilisation
```
/ssh                        → État SSH et connexions
/ssh server                 → Configuration serveur SSH
/ssh keys                   → Gestion des clés SSH
/ssh config                 → Configuration client (~/.ssh/config)
/ssh connect "host"         → Connexion SSH
/ssh tunnel                 → Gestion des tunnels SSH
/ssh agent                  → Agent SSH (ssh-agent)
/ssh known-hosts            → Gestion des known_hosts
/ssh troubleshoot           → Diagnostic SSH
```

Arguments: $ARGUMENTS

---

## État SSH (défaut)

```
🔐 SSH - ÉTAT GÉNÉRAL
═══════════════════════════════════════════════════════════════

SERVEUR SSH (OpenSSH Server):
├─ Service sshd: ✅ Running
├─ Port d'écoute: 22
├─ Version: OpenSSH_for_Windows_9.5p1
├─ Connexions actives: 2
└─ Dernière connexion: 2026-02-03 09:45 (jean@192.168.1.50)

CLIENT SSH:
├─ OpenSSH Client: ✅ Installé (9.5p1)
├─ ssh-agent: ✅ Running (3 clés chargées)
└─ Fichier config: ✅ ~/.ssh/config (5 hôtes)

CLÉS SSH LOCALES:
├─ id_ed25519 (ED25519) - Créée: 2025-06-15
├─ id_rsa (RSA 4096) - Créée: 2024-01-10
└─ github_key (ED25519) - Créée: 2025-08-20

CONNEXIONS ACTIVES (serveur):
┌────────────────┬─────────────┬───────────────┬──────────────┐
│ Utilisateur    │ IP Source   │ Depuis        │ PID          │
├────────────────┼─────────────┼───────────────┼──────────────┤
│ jean           │ 192.168.1.50│ 09:45         │ 4532         │
│ admin          │ 10.0.0.100  │ 08:30         │ 3218         │
└────────────────┴─────────────┴───────────────┴──────────────┘

STATISTIQUES (24h):
├─ Connexions entrantes réussies: 15
├─ Connexions entrantes échouées: 3 ⚠️
└─ Connexions sortantes: 28
```

---

## Mode `server`

```
⚙️ CONFIGURATION SERVEUR SSH
═══════════════════════════════════════════════════════════════

FICHIER: C:\ProgramData\ssh\sshd_config

PARAMÈTRES ACTUELS:
┌─────────────────────────────────────────────────────────────┐
│ # Réseau                                                    │
│ Port 22                                                     │
│ ListenAddress 0.0.0.0                                       │
│ Protocol 2                                                  │
│                                                             │
│ # Authentification                                          │
│ PubkeyAuthentication yes                                    │
│ PasswordAuthentication yes                                  │
│ PermitEmptyPasswords no                                     │
│ PermitRootLogin prohibit-password                           │
│                                                             │
│ # Sécurité                                                  │
│ MaxAuthTries 6                                              │
│ MaxSessions 10                                              │
│ ClientAliveInterval 300                                     │
│ ClientAliveCountMax 3                                       │
│                                                             │
│ # Logging                                                   │
│ SyslogFacility LOCAL0                                       │
│ LogLevel INFO                                               │
│                                                             │
│ # Subsystems                                                │
│ Subsystem sftp sftp-server.exe                              │
└─────────────────────────────────────────────────────────────┘

ANALYSE SÉCURITÉ:
┌──────────────────────────────┬──────────┬──────────────────┐
│ Paramètre                    │ Actuel   │ Recommandé       │
├──────────────────────────────┼──────────┼──────────────────┤
│ PasswordAuthentication       │ yes      │ ⚠️ no (clés only)│
│ PermitRootLogin             │ prohibit │ ✅ OK            │
│ PubkeyAuthentication        │ yes      │ ✅ OK            │
│ MaxAuthTries                │ 6        │ ✅ OK (3-6)      │
│ Port non-standard           │ 22       │ ⚠️ Changer       │
│ AllowUsers défini           │ Non      │ ⚠️ Recommandé    │
└──────────────────────────────┴──────────┴──────────────────┘

SERVICE:
├─ Nom: sshd
├─ État: ✅ Running
├─ Démarrage: Automatique
└─ Compte: LocalSystem

PARE-FEU:
├─ Règle entrante port 22: ✅ Activée
└─ Profils: Domain, Private

ACTIONS:
1. Éditer sshd_config
2. Redémarrer le service SSH
3. Désactiver l'authentification par mot de passe
4. Changer le port SSH
5. Configurer AllowUsers/DenyUsers
6. Voir les logs SSH

Choix: _
```

---

## Mode `keys`

```
🔑 GESTION DES CLÉS SSH
═══════════════════════════════════════════════════════════════

CLÉS PRIVÉES (~/.ssh/):
┌─────────────────────────────────────────────────────────────────┐
│ 🔐 id_ed25519                                                   │
├─────────────────────────────────────────────────────────────────┤
│ Type        : ED25519 (recommandé)                              │
│ Créée       : 2025-06-15                                        │
│ Fingerprint : SHA256:xYz123ABc456DEf789GHi...                   │
│ Commentaire : jean@desktop                                      │
│ Passphrase  : ✅ Protégée                                       │
│ Agent       : ✅ Chargée                                        │
├─────────────────────────────────────────────────────────────────┤
│ 🔐 id_rsa                                                       │
├─────────────────────────────────────────────────────────────────┤
│ Type        : RSA 4096 bits                                     │
│ Créée       : 2024-01-10                                        │
│ Fingerprint : SHA256:aBc789XyZ123DEf456...                      │
│ Commentaire : jean@old-laptop                                   │
│ Passphrase  : ❌ Non protégée ⚠️                                │
│ Agent       : ❌ Non chargée                                    │
├─────────────────────────────────────────────────────────────────┤
│ 🔐 github_key                                                   │
├─────────────────────────────────────────────────────────────────┤
│ Type        : ED25519                                           │
│ Créée       : 2025-08-20                                        │
│ Fingerprint : SHA256:GhI456JkL789MnO...                         │
│ Commentaire : github-deploy                                     │
│ Passphrase  : ✅ Protégée                                       │
│ Agent       : ✅ Chargée                                        │
└─────────────────────────────────────────────────────────────────┘

CLÉS AUTORISÉES (serveur - authorized_keys):
├─ 3 clés pour l'utilisateur jean
├─ 1 clé pour l'utilisateur admin
└─ Fichier: C:\Users\<user>\.ssh\authorized_keys

ACTIONS:
1. 🆕 Générer une nouvelle clé
   → Type: [ED25519] [RSA 4096] [ECDSA]
   → Nom: ________________
   → Passphrase: ________________

2. 📤 Copier la clé publique vers un serveur
   → ssh-copy-id équivalent

3. 🔓 Ajouter une clé à l'agent
   → ssh-add <keyfile>

4. 📋 Afficher une clé publique
   → Pour copier vers GitHub, GitLab, etc.

5. 🗑️ Supprimer une clé

6. 🔒 Ajouter une passphrase à une clé non protégée

Choix: _
```

---

## Mode `config`

```
📝 CONFIGURATION CLIENT SSH
═══════════════════════════════════════════════════════════════

FICHIER: C:\Users\Jean\.ssh\config

CONTENU ACTUEL:
┌─────────────────────────────────────────────────────────────┐
│ # Configuration globale                                     │
│ Host *                                                      │
│     AddKeysToAgent yes                                      │
│     IdentitiesOnly yes                                      │
│     ServerAliveInterval 60                                  │
│     ServerAliveCountMax 3                                   │
│                                                             │
│ # Serveurs                                                  │
│ Host server1                                                │
│     HostName 192.168.1.100                                  │
│     User admin                                              │
│     Port 22                                                 │
│     IdentityFile ~/.ssh/id_ed25519                          │
│                                                             │
│ Host github.com                                             │
│     HostName github.com                                     │
│     User git                                                │
│     IdentityFile ~/.ssh/github_key                          │
│                                                             │
│ Host dev-server                                             │
│     HostName dev.example.com                                │
│     User deploy                                             │
│     Port 2222                                               │
│     IdentityFile ~/.ssh/deploy_key                          │
│     ProxyJump bastion                                       │
│                                                             │
│ Host bastion                                                │
│     HostName bastion.example.com                            │
│     User jump                                               │
│     IdentityFile ~/.ssh/bastion_key                         │
│                                                             │
│ Host prod-*                                                 │
│     User deploy                                             │
│     IdentityFile ~/.ssh/prod_key                            │
│     StrictHostKeyChecking yes                               │
└─────────────────────────────────────────────────────────────┘

HÔTES CONFIGURÉS:
├─ server1 → 192.168.1.100:22 (admin)
├─ github.com → github.com:22 (git)
├─ dev-server → dev.example.com:2222 (via bastion)
├─ bastion → bastion.example.com:22 (jump)
└─ prod-* → wildcard pour serveurs de production

ACTIONS:
1. Ajouter un nouvel hôte
2. Modifier un hôte existant
3. Supprimer un hôte
4. Tester une connexion
5. Éditer le fichier manuellement

Choix: _
```

---

## Mode `tunnel`

```
🚇 TUNNELS SSH
═══════════════════════════════════════════════════════════════

TUNNELS ACTIFS:
┌─────────────────────────────────────────────────────────────────┐
│ 🔵 Tunnel Local #1                                              │
├─────────────────────────────────────────────────────────────────┤
│ Type        : Local (-L)                                        │
│ Local       : localhost:8080                                    │
│ Remote      : 192.168.1.100:80                                  │
│ Via         : server1                                           │
│ PID         : 5432                                              │
│ Depuis      : 2h 30m                                            │
│ Usage       : Accès web interne via SSH                         │
│ Commande    : ssh -L 8080:192.168.1.100:80 server1             │
├─────────────────────────────────────────────────────────────────┤
│ 🟢 Tunnel Remote #2                                             │
├─────────────────────────────────────────────────────────────────┤
│ Type        : Remote (-R)                                       │
│ Remote      : server1:9000                                      │
│ Local       : localhost:3000                                    │
│ PID         : 5678                                              │
│ Depuis      : 45m                                               │
│ Usage       : Exposer app locale au serveur                     │
│ Commande    : ssh -R 9000:localhost:3000 server1               │
├─────────────────────────────────────────────────────────────────┤
│ 🟣 SOCKS Proxy #3                                               │
├─────────────────────────────────────────────────────────────────┤
│ Type        : Dynamic (-D)                                      │
│ Local       : localhost:1080                                    │
│ Via         : bastion                                           │
│ PID         : 6789                                              │
│ Depuis      : 1h 15m                                            │
│ Usage       : Proxy SOCKS5 pour navigation                      │
│ Commande    : ssh -D 1080 bastion                              │
└─────────────────────────────────────────────────────────────────┘

CRÉER UN NOUVEAU TUNNEL:

Type de tunnel:
[L] Local  → Accéder à un port distant via localhost
[R] Remote → Exposer un port local vers le serveur distant
[D] Dynamic → Proxy SOCKS5

Pour tunnel Local (-L):
├─ Port local: ____
├─ Hôte destination: ________________
├─ Port destination: ____
├─ Serveur SSH: ________________
└─ Options: [ ] Compression [ ] Background [ ] Persistent

Exemples courants:
1. Accès base de données: -L 5432:db-server:5432 bastion
2. Accès web interne: -L 8080:intranet:80 vpn-server
3. Proxy SOCKS: -D 1080 jump-server

ACTIONS:
1. Créer un tunnel local
2. Créer un tunnel remote
3. Créer un proxy SOCKS
4. Fermer un tunnel
5. Sauvegarder un tunnel comme alias

Choix: _
```

---

## Mode `agent`

```
🔑 SSH AGENT
═══════════════════════════════════════════════════════════════

SERVICE SSH-AGENT:
├─ État: ✅ Running
├─ PID: 1234
├─ Type de démarrage: Automatique
└─ Socket: \\.\pipe\openssh-ssh-agent

CLÉS CHARGÉES DANS L'AGENT:
┌─────────────────────────────────────────────────────────────┐
│ # │ Type    │ Bits │ Fingerprint              │ Commentaire │
├───┼─────────┼──────┼──────────────────────────┼─────────────┤
│ 1 │ ED25519 │ 256  │ SHA256:xYz123ABc456DE... │ jean@desktop│
│ 2 │ ED25519 │ 256  │ SHA256:GhI456JkL789Mn... │ github-deploy│
│ 3 │ RSA     │ 4096 │ SHA256:MnO789PqR012St... │ legacy-key  │
└───┴─────────┴──────┴──────────────────────────┴─────────────┘

Durée de vie des clés: Illimitée (défaut)

ACTIONS:
1. Lister les clés (ssh-add -l)
2. Ajouter une clé (ssh-add <keyfile>)
3. Ajouter toutes les clés (~/.ssh/id_*)
4. Supprimer une clé (ssh-add -d <keyfile>)
5. Supprimer toutes les clés (ssh-add -D)
6. Définir un timeout (ssh-add -t <seconds>)
7. Verrouiller l'agent (ssh-add -x)
8. Déverrouiller l'agent (ssh-add -X)

Choix: _
```

---

## Mode `troubleshoot`

```
🔧 DIAGNOSTIC SSH
═══════════════════════════════════════════════════════════════

TEST DE LA CONFIGURATION:

1. CLIENT SSH
   ├─ OpenSSH installé: ✅ Version 9.5p1
   ├─ Fichier config: ✅ Syntaxe valide
   ├─ Permissions ~/.ssh: ✅ Correctes
   └─ ssh-agent: ✅ Running

2. SERVEUR SSH
   ├─ Service sshd: ✅ Running
   ├─ Port 22 en écoute: ✅ Oui
   ├─ sshd_config: ✅ Syntaxe valide
   └─ Pare-feu: ✅ Port ouvert

3. CLÉS
   ├─ Clé privée trouvée: ✅ id_ed25519
   ├─ Permissions clé: ✅ 600
   └─ Agent chargé: ✅ 3 clés

═══════════════════════════════════════════════════════════════
RÉSULTAT: ✅ Configuration OK

TEST DE CONNEXION:
Hôte à tester: ________________

ssh -vvv user@host (mode verbose pour diagnostic)

PROBLÈMES COURANTS:

❓ "Permission denied (publickey)"
   → Vérifier que la clé publique est dans authorized_keys
   → Vérifier les permissions: chmod 600 ~/.ssh/*
   → ssh-add pour charger la clé dans l'agent

❓ "Connection refused"
   → Service sshd non démarré
   → Pare-feu bloque le port
   → Mauvais port

❓ "Host key verification failed"
   → Clé du serveur a changé (ou attaque MITM)
   → Supprimer l'ancienne entrée: ssh-keygen -R <host>

❓ "Connection timed out"
   → Problème réseau / routage
   → Pare-feu distant bloque
   → Hôte inaccessible

❓ Connexion très lente
   → DNS inversé: ajouter "UseDNS no" dans sshd_config
   → GSSAPI: ajouter "GSSAPIAuthentication no"
```

---

## Commandes de Référence

```powershell
# Installation OpenSSH (si pas installé)
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Service SSH
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic

# Générer une clé
ssh-keygen -t ed25519 -C "commentaire"
ssh-keygen -t rsa -b 4096 -C "commentaire"

# Agent SSH
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
ssh-add ~/.ssh/id_ed25519

# Copier clé vers serveur (PowerShell)
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh user@host "cat >> ~/.ssh/authorized_keys"

# Tunnels
ssh -L 8080:localhost:80 user@host      # Local
ssh -R 9000:localhost:3000 user@host    # Remote
ssh -D 1080 user@host                    # SOCKS

# Debug
ssh -vvv user@host

# Known hosts
ssh-keygen -R hostname
ssh-keyscan hostname >> ~/.ssh/known_hosts
```
