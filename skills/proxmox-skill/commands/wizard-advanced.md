> Partie avancee de [[wizard]]. Commandes essentielles dans le fichier principal.

# /pve-wizard - Wizards Interactifs (Avance)

## Description
Wizards avances : creation CT, hardening securite production, et references aux wizards detailles.

---

## 📦 Wizard: CT Creation

Voir fichier separe: `/wizards/ct-create.md`

---

## 🔒 Wizard: Security Hardening

### Questions Interactives

```
🧙 WIZARD: Hardening Sécurité Production
========================================

📍 AUDIT INITIAL
┌─────────────────────────────────────────────────────┐
│ Analyse de sécurité en cours...                     │
│                                                     │
│ [!] SSH: Password authentication enabled            │
│ [!] 2FA: Not configured                             │
│ [!] Fail2ban: Not installed                         │
│ [✓] Firewall: Enabled                               │
│ [!] Updates: 12 packages need updating              │
│ [✓] SSL: Valid certificate                          │
│                                                     │
│ Score sécurité: 45/100 ⚠️                           │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 1/5: SSH Hardening
┌─────────────────────────────────────────────────────┐
│ Q: Appliquer hardening SSH?                         │
│                                                     │
│ Modifications:                                      │
│   • Désactiver password authentication              │
│   • Activer only pubkey authentication              │
│   • Limiter MaxAuthTries à 3                        │
│   • Configurer AllowUsers                           │
│                                                     │
│    [1] Oui, appliquer (⚠️ avoir clé SSH prête!)    │
│    [2] Non, passer                                  │
│                                                     │
│ Votre choix: _                                      │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 2/5: Fail2ban
┌─────────────────────────────────────────────────────┐
│ Q: Installer et configurer Fail2ban?                │
│                                                     │
│ Configuration:                                      │
│   • Jail SSH (bantime: 1h, maxretry: 3)            │
│   • Jail Proxmox WebUI                              │
│   • Whitelist: 10.0.0.0/24                          │
│                                                     │
│    [1] Oui, installer                               │
│    [2] Non, passer                                  │
│                                                     │
│ Votre choix: _                                      │
│                                                     │
│ Réseau à whitelist (CIDR): _                        │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 3/5: 2FA/TOTP
┌─────────────────────────────────────────────────────┐
│ Q: Configurer 2FA pour root@pam?                    │
│                                                     │
│    [1] Oui, configurer TOTP                         │
│    [2] Non, passer                                  │
│                                                     │
│ Votre choix: _                                      │
│                                                     │
│ [QR Code s'affichera ici]                           │
│ Scanner avec Google Authenticator / Authy           │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 4/5: API Tokens
┌─────────────────────────────────────────────────────┐
│ Q: Créer API tokens pour automation?                │
│                                                     │
│    [1] Token Terraform (PVEAdmin)                   │
│    [2] Token Monitoring (PVEAuditor)                │
│    [3] Les deux                                     │
│    [4] Passer                                       │
│                                                     │
│ Votre choix: _                                      │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 5/5: Updates automatiques
┌─────────────────────────────────────────────────────┐
│ Q: Configurer unattended-upgrades?                  │
│                                                     │
│ Configuration:                                      │
│   • Security updates automatiques                   │
│   • Email notification                              │
│   • Pas de reboot automatique                       │
│                                                     │
│    [1] Oui, configurer                              │
│    [2] Non, passer                                  │
│                                                     │
│ Votre choix: _                                      │
│                                                     │
│ Email pour notifications: _                         │
└─────────────────────────────────────────────────────┘

📍 RÉSUMÉ
┌─────────────────────────────────────────────────────┐
│ Actions à effectuer:                                │
│                                                     │
│   ✓ SSH Hardening                                   │
│   ✓ Fail2ban (whitelist: 10.0.0.0/24)              │
│   ✓ 2FA pour root@pam                              │
│   ✓ API Token: terraform@pve!terraform-token       │
│   ✓ API Token: monitoring@pve!prometheus-token     │
│   ✓ Unattended-upgrades                            │
│                                                     │
│ Nouveau score estimé: 92/100 ✅                     │
│                                                     │
│ [1] Appliquer tout                                  │
│ [2] Modifier                                        │
│ [3] Annuler                                         │
│                                                     │
│ Votre choix: _                                      │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Fichiers Wizards Detailles

Voir dossier `/wizards/` pour les wizards complets :
- `setup.md` - Configuration initiale
- `vm-create.md` - Creation VM
- `ct-create.md` - Creation CT
- `template.md` - Templates Cloud-Init
- `cluster.md` - Setup cluster
- `ceph.md` - Deploiement Ceph
- `ha.md` - Haute disponibilite
- `backup.md` - Strategie backup
- `security.md` - Hardening
- `sdn.md` - SDN/VLAN
- `migrate.md` - Migration
