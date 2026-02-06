# 🧙 /pve-wizard - Wizards Interactifs

## Description
Collection de wizards interactifs pour configuration guidée Proxmox VE 9+.

## Syntaxe
```
/pve-wizard [wizard-name]
```

## Wizards Disponibles

| Wizard | Commande | Description |
|--------|----------|-------------|
| Setup Initial | `/pve-wizard setup` | Configuration post-installation |
| VM Creation | `/pve-wizard vm` | Création VM optimisée |
| CT Creation | `/pve-wizard ct` | Création conteneur |
| Template | `/pve-wizard template` | Création template Cloud-Init |
| Cluster | `/pve-wizard cluster` | Setup cluster multi-nodes |
| Ceph | `/pve-wizard ceph` | Déploiement Ceph |
| HA | `/pve-wizard ha` | Configuration haute dispo |
| Backup | `/pve-wizard backup` | Stratégie backup 3-2-1 |
| Security | `/pve-wizard security` | Hardening production |
| SDN | `/pve-wizard sdn` | Configuration SDN/VLAN |
| Migration | `/pve-wizard migrate` | Migration depuis autre hyperviseur |

---

## 📋 Wizard: Setup Initial

### Questions Interactives

```
🧙 WIZARD: Configuration Initiale Proxmox VE 9+
================================================

📍 ÉTAPE 1/8: Informations Node
┌─────────────────────────────────────────────────────┐
│ Hostname actuel: pve                                │
│                                                     │
│ Q: Souhaitez-vous changer le hostname?              │
│    [1] Oui                                          │
│    [2] Non (garder 'pve')                           │
│                                                     │
│ Votre choix: _                                      │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 2/8: Configuration Réseau
┌─────────────────────────────────────────────────────┐
│ Interface détectée: eth0 (192.168.1.10/24)          │
│                                                     │
│ Q: Type de configuration réseau souhaité?           │
│    [1] Simple - Un seul bridge (lab/test)           │
│    [2] Séparé - Management + VMs (recommandé)       │
│    [3] Complet - Mgmt + VMs + Storage + Corosync    │
│    [4] Personnalisé                                 │
│                                                     │
│ Votre choix: _                                      │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 3/8: Repositories
┌─────────────────────────────────────────────────────┐
│ Q: Type de licence/repository?                      │
│    [1] Enterprise (subscription requise)            │
│    [2] No-Subscription (gratuit, pour test/lab)     │
│    [3] Test (dernières versions, instable)          │
│                                                     │
│ Votre choix: _                                      │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 4/8: Stockage
┌─────────────────────────────────────────────────────┐
│ Disques détectés:                                   │
│   /dev/sda - 256GB (système)                        │
│   /dev/sdb - 1TB                                    │
│   /dev/sdc - 1TB                                    │
│                                                     │
│ Q: Configuration stockage pour VMs?                 │
│    [1] LVM-thin sur /dev/sdb                        │
│    [2] ZFS mirror (sdb + sdc)                       │
│    [3] ZFS RAID-Z1 (besoin 3+ disques)              │
│    [4] Utiliser stockage existant                   │
│    [5] Configurer plus tard                         │
│                                                     │
│ Votre choix: _                                      │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 5/8: Sécurité SSH
┌─────────────────────────────────────────────────────┐
│ Q: Appliquer hardening SSH?                         │
│    [1] Oui - Clés uniquement, pas de password       │
│    [2] Non - Garder config par défaut               │
│                                                     │
│ Votre choix: _                                      │
│                                                     │
│ Si [1]: Collez votre clé SSH publique:              │
│ > _                                                 │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 6/8: Fail2ban
┌─────────────────────────────────────────────────────┐
│ Q: Installer et configurer Fail2ban?                │
│    [1] Oui (recommandé)                             │
│    [2] Non                                          │
│                                                     │
│ Votre choix: _                                      │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 7/8: Email Notifications
┌─────────────────────────────────────────────────────┐
│ Q: Configurer les notifications email?              │
│    [1] Oui                                          │
│    [2] Non                                          │
│                                                     │
│ Si [1]:                                             │
│   Email admin: _                                    │
│   Serveur SMTP: _                                   │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 8/8: Résumé
┌─────────────────────────────────────────────────────┐
│ Configuration à appliquer:                          │
│                                                     │
│   ✓ Hostname: pve1                                  │
│   ✓ Réseau: Séparé (vmbr0 mgmt, vmbr1 VMs)         │
│   ✓ Repository: No-Subscription                    │
│   ✓ Stockage: ZFS mirror (sdb+sdc)                 │
│   ✓ SSH: Hardened (clés uniquement)                │
│   ✓ Fail2ban: Activé                               │
│   ✓ Email: admin@example.com                       │
│                                                     │
│ Q: Appliquer cette configuration?                   │
│    [1] Oui, appliquer                               │
│    [2] Non, recommencer                             │
│    [3] Annuler                                      │
│                                                     │
│ Votre choix: _                                      │
└─────────────────────────────────────────────────────┘
```

---

## 🖥️ Wizard: VM Creation

### Questions Interactives

```
🧙 WIZARD: Création Machine Virtuelle
======================================

📍 ÉTAPE 1/7: Informations de base
┌─────────────────────────────────────────────────────┐
│ Nom de la VM: _                                     │
│ VMID [auto]: _                                      │
│ Description (optionnel): _                          │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 2/7: Type de système
┌─────────────────────────────────────────────────────┐
│ Q: Quel système d'exploitation?                     │
│    [1] Linux (Ubuntu, Debian, RHEL...)              │
│    [2] Windows Server 2022/2025                     │
│    [3] Windows 10/11 Desktop                        │
│    [4] FreeBSD                                      │
│    [5] Autre                                        │
│                                                     │
│ Votre choix: _                                      │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 3/7: Méthode d'installation
┌─────────────────────────────────────────────────────┐
│ Q: Comment installer le système?                    │
│    [1] Cloner depuis template (recommandé)          │
│    [2] ISO (installation manuelle)                  │
│    [3] Importer disque existant                     │
│    [4] PXE Boot                                     │
│                                                     │
│ Votre choix: _                                      │
│                                                     │
│ Si [1] - Templates disponibles:                     │
│    [a] ubuntu-2404-cloud (ID: 9000)                │
│    [b] debian-12-cloud (ID: 9001)                  │
│    [c] windows-2025-template (ID: 9010)            │
│                                                     │
│ Template: _                                         │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 4/7: Ressources
┌─────────────────────────────────────────────────────┐
│ Q: Profil de ressources?                            │
│    [1] Minimal  - 1 CPU, 1GB RAM, 16GB disk         │
│    [2] Small    - 2 CPU, 2GB RAM, 32GB disk         │
│    [3] Medium   - 4 CPU, 4GB RAM, 64GB disk         │
│    [4] Large    - 8 CPU, 8GB RAM, 128GB disk        │
│    [5] Custom   - Définir manuellement              │
│                                                     │
│ Votre choix: _                                      │
│                                                     │
│ Si [5] Custom:                                      │
│   CPU cores: _                                      │
│   RAM (GB): _                                       │
│   Disk (GB): _                                      │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 5/7: Réseau
┌─────────────────────────────────────────────────────┐
│ Q: Configuration réseau?                            │
│    [1] DHCP (automatique)                           │
│    [2] IP statique                                  │
│    [3] Plusieurs interfaces                         │
│                                                     │
│ Votre choix: _                                      │
│                                                     │
│ Si [2] Statique:                                    │
│   IP: _                                             │
│   Masque: _                                         │
│   Gateway: _                                        │
│   DNS: _                                            │
│                                                     │
│ Bridge: [vmbr0] _                                   │
│ VLAN tag (optionnel): _                             │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 6/7: Options avancées
┌─────────────────────────────────────────────────────┐
│ Q: Options supplémentaires?                         │
│    [x] QEMU Guest Agent (recommandé)                │
│    [x] Démarrage automatique                        │
│    [ ] Haute disponibilité (HA)                     │
│    [ ] Firewall activé                              │
│    [ ] Backup automatique                           │
│                                                     │
│ Sélectionnez avec espace, Entrée pour continuer    │
└─────────────────────────────────────────────────────┘

📍 ÉTAPE 7/7: Confirmation
┌─────────────────────────────────────────────────────┐
│ VM à créer:                                         │
│                                                     │
│   Nom: web-server-01                                │
│   VMID: 100                                         │
│   Template: ubuntu-2404-cloud                       │
│   CPU: 4 cores (type: host)                         │
│   RAM: 4 GB                                         │
│   Disk: 64 GB (local-lvm, VirtIO SCSI)             │
│   Réseau: 192.168.1.100/24 (vmbr0)                 │
│   Agent: Oui                                        │
│   Start on boot: Oui                                │
│                                                     │
│ Commande générée:                                   │
│ qm clone 9000 100 --name web-server-01 --full 1    │
│ qm set 100 --cores 4 --memory 4096                 │
│ qm set 100 --ipconfig0 ip=192.168.1.100/24,gw=...  │
│                                                     │
│ [1] Créer la VM                                     │
│ [2] Créer et démarrer                               │
│ [3] Modifier                                        │
│ [4] Annuler                                         │
│                                                     │
│ Votre choix: _                                      │
└─────────────────────────────────────────────────────┘
```

---

## 📦 Wizard: CT Creation

Voir fichier séparé: `/wizards/ct-create.md`

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

## 📁 Fichiers Wizards Détaillés

Voir dossier `/wizards/` pour les wizards complets :
- `setup.md` - Configuration initiale
- `vm-create.md` - Création VM
- `ct-create.md` - Création CT
- `template.md` - Templates Cloud-Init
- `cluster.md` - Setup cluster
- `ceph.md` - Déploiement Ceph
- `ha.md` - Haute disponibilité
- `backup.md` - Stratégie backup
- `security.md` - Hardening
- `sdn.md` - SDN/VLAN
- `migrate.md` - Migration
