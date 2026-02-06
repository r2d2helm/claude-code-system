# Wizard: Hardening Sécurité Proxmox

## Mode d'emploi
Ce wizard guide le durcissement de sécurité d'une installation Proxmox VE 9+. Suivez les étapes dans l'ordre pour une sécurisation progressive.

---

## Questions Interactives

### 1. Authentification

**Q1.1: Activer l'authentification à deux facteurs (2FA)?**

| Option | Type | Support |
|--------|------|---------|
| A | TOTP | Google Authenticator, Authy |
| B | WebAuthn | Clé FIDO2, Yubikey 5+ |
| C | Yubikey OTP | Yubikey (tous modèles) |
| D | Tous | Maximum de flexibilité |

```
Choix: ___
```

**Q1.2: Rendre le 2FA obligatoire?**
```
[ ] Oui - Pour tous les utilisateurs (recommandé prod)
[ ] Non - Optionnel par utilisateur
```

---

### 2. Gestion des Utilisateurs

**Q2.1: Créer des utilisateurs non-root?**
```
Admin 1: _______________ (ex: admin@pam)
Admin 2: _______________ (optionnel)
```

**Q2.2: Intégration annuaire?**

| Option | Type |
|--------|------|
| A | Pas d'annuaire (PAM local) |
| B | LDAP |
| C | Active Directory |
| D | OpenID Connect |

```
Choix: ___
Server (si B/C/D): _______________
```

**Q2.3: Créer des API tokens?**
```
[ ] Oui - Token pour automatisation (Terraform, Ansible)
[ ] Non
```

---

### 3. Réseau / Firewall

**Q3.1: Activer le firewall cluster Proxmox?**
```
[ ] Oui (recommandé)
[ ] Non
```

**Q3.2: Restreindre l'accès Web GUI?**
```
Sous-réseaux autorisés: _______________
(ex: 10.0.0.0/24, 192.168.1.0/24)
```

**Q3.3: Port SSH personnalisé?**
```
Port: _____ (défaut: 22, recommandé: 2222+)
```

---

### 4. SSH

**Q4.1: Durcissement SSH?**
```
[ ] Désactiver login root par mot de passe
[ ] Autoriser uniquement les clés SSH
[ ] Limiter les utilisateurs SSH (AllowUsers)
```

---

### 5. Certificats TLS

**Q5.1: Certificat pour l'interface web?**

| Option | Type |
|--------|------|
| A | Let's Encrypt (ACME) - Automatique |
| B | Certificat custom (entreprise CA) |
| C | Auto-signé (défaut, non recommandé prod) |

```
Choix: ___
Domaine (si A): _______________
```

---

## Génération de Commandes

### Utilisateurs et Rôles

```bash
# Créer un utilisateur admin
pveum user add admin@pam --comment "Admin principal"
pveum passwd admin@pam

# Créer un rôle custom
pveum role add SysAdmin --privs "Sys.Audit,Sys.Modify,Sys.Console,VM.Allocate,VM.Audit,VM.Clone,VM.Config.CDROM,VM.Config.CPU,VM.Config.Disk,VM.Config.Memory,VM.Config.Network,VM.Config.Options,VM.Console,VM.Migrate,VM.Monitor,VM.PowerMgmt,VM.Snapshot,Datastore.Allocate,Datastore.Audit"

# Assigner le rôle
pveum aclmod / --users admin@pam --roles SysAdmin
```

### 2FA TOTP

```bash
# Activer TOTP pour un utilisateur (via GUI ou API)
pveum user token add admin@pam automation --privsep 0

# Forcer 2FA pour le realm
pveum realm modify pam --tfa type=totp
```

### API Token

```bash
# Créer un token API
pveum user token add admin@pam terraform-token --privsep 1 --expire 0
pveum aclmod / --tokens 'admin@pam!terraform-token' --roles PVEAuditor
```

### Firewall Cluster

```bash
# Activer le firewall cluster
cat > /etc/pve/firewall/cluster.fw << 'EOF'
[OPTIONS]
enable: 1
policy_in: DROP
policy_out: ACCEPT

[RULES]
IN ACCEPT -source +management -p tcp -dport 8006 -log nolog # Web GUI
IN ACCEPT -source +management -p tcp -dport 22 -log nolog   # SSH
IN ACCEPT -p tcp -dport 5900:5999 -log nolog                # VNC consoles
IN ACCEPT -p tcp -dport 3128 -log nolog                     # SPICE proxy

[IPSET management]
10.0.0.0/24
192.168.1.0/24
EOF

# Activer
pve-firewall start
```

### SSH Hardening

```bash
# /etc/ssh/sshd_config.d/hardening.conf
cat > /etc/ssh/sshd_config.d/hardening.conf << 'EOF'
Port 2222
PermitRootLogin prohibit-password
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers admin@pam
EOF

systemctl restart sshd
```

### Let's Encrypt

```bash
# Configurer ACME
pvenode acme account register default admin@example.com
pvenode acme plugin add standalone standalone-plugin

# Commander le certificat
pvenode acme cert order --force
```

---

## Checklist Sécurité

- [ ] Login root SSH par mot de passe désactivé
- [ ] 2FA activé pour tous les admins
- [ ] Firewall cluster activé
- [ ] Accès GUI restreint par IP
- [ ] Certificat TLS valide (pas auto-signé)
- [ ] API tokens avec least privilege
- [ ] Mises à jour automatiques configurées
- [ ] Logs centralisés (syslog)
- [ ] Backup de la config cluster

---

## Commande Associée

Voir `/px-security` pour les opérations de sécurité.
