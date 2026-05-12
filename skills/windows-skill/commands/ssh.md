# Gestion SSH (OpenSSH Windows)

Voir aussi: [[ssh-advanced]]

Administration du serveur et client SSH Windows.

## Mode d'Utilisation
```
/ssh                        → État SSH et connexions
/ssh server                 → Configuration serveur SSH
/ssh keys                   → Gestion des clés SSH
/ssh config                 → Configuration client (~/.ssh/config)
/ssh connect "host"         → Connexion SSH
/ssh tunnel                 → Gestion des tunnels (voir ssh-advanced)
/ssh agent                  → Agent SSH (voir ssh-advanced)
/ssh known-hosts            → Gestion des known_hosts (voir ssh-advanced)
/ssh troubleshoot           → Diagnostic SSH (voir ssh-advanced)
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
│ Passphrase  : Non protégée ⚠️                                   │
│ Agent       : Non chargée                                       │
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
1. Générer une nouvelle clé
   → Type: [ED25519] [RSA 4096] [ECDSA]
   → Nom: ________________
   → Passphrase: ________________

2. Copier la clé publique vers un serveur
   → ssh-copy-id équivalent

3. Ajouter une clé à l'agent
   → ssh-add <keyfile>

4. Afficher une clé publique
   → Pour copier vers GitHub, GitLab, etc.

5. Supprimer une clé

6. Ajouter une passphrase à une clé non protégée

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

## Commandes de Référence (Core)

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
```
