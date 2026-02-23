# Gestion SSH - Avancé

Voir aussi: [[ssh]]

Tunnels SSH, agent, known_hosts et dépannage.

---

## Mode `tunnel`

```
🚇 TUNNELS SSH
═══════════════════════════════════════════════════════════════

TUNNELS ACTIFS:
┌─────────────────────────────────────────────────────────────────┐
│ Tunnel Local #1                                                 │
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
│ Tunnel Remote #2                                                │
├─────────────────────────────────────────────────────────────────┤
│ Type        : Remote (-R)                                       │
│ Remote      : server1:9000                                      │
│ Local       : localhost:3000                                    │
│ PID         : 5678                                              │
│ Depuis      : 45m                                               │
│ Usage       : Exposer app locale au serveur                     │
│ Commande    : ssh -R 9000:localhost:3000 server1               │
├─────────────────────────────────────────────────────────────────┤
│ SOCKS Proxy #3                                                  │
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

## Commandes de Référence (Avancé)

```powershell
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
