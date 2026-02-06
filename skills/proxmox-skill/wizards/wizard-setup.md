# Wizard: Setup Initial Proxmox

## Mode d'emploi
Ce wizard guide la configuration initiale d'un serveur Proxmox VE 9+ fraîchement installé. À exécuter après l'installation et le premier accès à la web GUI.

---

## Questions Interactives

### 1. Informations Système

**Q1.1: Hostname?**
```
Hostname: _______________ (ex: pve1, proxmox-prod-01)
```

**Q1.2: Configuration réseau?**
```
Interface: _______________ (ex: eno1, enp0s25)
IP statique: _______________ (ex: 10.10.10.10/24)
Gateway: _______________
DNS 1: _______________
DNS 2: _______________
Domaine: _______________ (ex: home.lab, corp.local)
```

**Q1.3: Serveur NTP?**
```
[ ] pool.ntp.org (défaut)
[ ] Serveur custom: _______________
```

---

### 2. Dépôts APT

**Q2.1: Type de souscription?**

| Option | Dépôt | Accès |
|--------|-------|-------|
| A | Enterprise (payant) | Stable, support officiel |
| B | No-Subscription (gratuit) | Stable, communauté |
| C | Test (gratuit) | Dernières fonctionnalités, moins stable |

```
Choix: ___
```

---

### 3. Stockage

**Q3.1: Configuration stockage principal?**

| Option | Type | Usage |
|--------|------|-------|
| A | ZFS (recommandé) | Déjà configuré à l'installation |
| B | LVM-Thin | Thin provisioning |
| C | Directory | Stockage simple sur partition |
| D | Ajouter NFS/CIFS/iSCSI | Stockage réseau |

```
Choix: ___
```

**Q3.2: Si NFS - Configuration?**
```
Serveur NFS: _______________
Export: _______________
Mountpoint: _______________
Content: [ ] images [ ] iso [ ] vztmpl [ ] backup [ ] snippets
```

---

### 4. Alertes Email

**Q4.1: Configurer les alertes email?**
```
[ ] Oui
[ ] Non (configurer plus tard)

Email admin: _______________
SMTP Server: _______________ (ex: smtp.gmail.com)
SMTP Port: _____ (ex: 587)
SMTP User: _______________
```

---

### 5. Interface Web

**Q5.1: Activer le thème sombre?**
```
[ ] Oui (PVE Dark Theme)
[ ] Non (thème par défaut)
```

**Q5.2: Supprimer la popup "No valid subscription"?**
```
[ ] Oui (patch JavaScript, reset après update)
[ ] Non
```

---

## Génération de Commandes

### Étape 1: Configurer les Dépôts

```bash
# Désactiver le dépôt enterprise (si pas de souscription)
sed -i 's/^deb/#deb/' /etc/apt/sources.list.d/pve-enterprise.list

# Ajouter le dépôt no-subscription
echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list

# Mettre à jour
apt update && apt full-upgrade -y
```

### Étape 2: Réseau

```bash
# /etc/network/interfaces (déjà configuré normalement)
cat /etc/network/interfaces

# Vérifier
ip addr show
ip route show
```

### Étape 3: Hostname et DNS

```bash
# Hostname
hostnamectl set-hostname HOSTNAME

# /etc/hosts
cat > /etc/hosts << 'EOF'
127.0.0.1 localhost
IP_ADDRESS HOSTNAME.DOMAIN HOSTNAME

# IPv6
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
EOF
```

### Étape 4: NTP

```bash
# Configurer chrony
apt install chrony -y
cat > /etc/chrony/chrony.conf << 'EOF'
server NTP_SERVER iburst
driftfile /var/lib/chrony/drift
makestep 1.0 3
rtcsync
EOF
systemctl restart chronyd
chronyc tracking
```

### Étape 5: Stockage NFS (optionnel)

```bash
pvesm add nfs NFS_NAME \
  --server NFS_IP \
  --export /export/path \
  --path /mnt/pve/NFS_NAME \
  --content images,iso,vztmpl,backup
```

### Étape 6: Email Alerts

```bash
# Installer les outils mail
apt install libsasl2-modules mailutils -y

# Configurer Postfix relay
cat >> /etc/postfix/main.cf << 'EOF'
relayhost = [smtp.gmail.com]:587
smtp_use_tls = yes
smtp_sasl_auth_enable = yes
smtp_sasl_security_options = noanonymous
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
EOF

# Credentials
echo "[smtp.gmail.com]:587 user@gmail.com:app-password" > /etc/postfix/sasl_passwd
chmod 600 /etc/postfix/sasl_passwd
postmap /etc/postfix/sasl_passwd
systemctl restart postfix

# Test
echo "Test alert from Proxmox" | mail -s "PVE Alert Test" admin@example.com
```

### Étape 7: Thème Sombre (optionnel)

```bash
# Via la GUI: Datacenter -> Options -> Style -> Dark
# Ou via API
pvesh set /cluster/options --console html5
```

### Étape 8: Télécharger les ISOs/Templates

```bash
# Mettre à jour les templates disponibles
pveam update

# Télécharger des templates CT courants
pveam download local ubuntu-24.04-standard_24.04-1_amd64.tar.zst
pveam download local debian-13-standard_13.0-1_amd64.tar.zst

# Les ISOs doivent être uploadés via la GUI ou SCP
# scp ubuntu-24.04-server.iso root@pve:/var/lib/vz/template/iso/
```

---

## Checklist Post-Setup

- [ ] Dépôts APT configurés et mis à jour
- [ ] Hostname et DNS corrects
- [ ] IP statique configurée
- [ ] NTP synchronisé
- [ ] Stockage configuré (local + réseau si besoin)
- [ ] Alertes email fonctionnelles
- [ ] ISOs/templates téléchargés
- [ ] Backup de la configuration
- [ ] Utilisateur admin non-root créé (voir wizard-security)

---

## Best Practices 2026

| Règle | Raison |
|-------|--------|
| Toujours mettre à jour après install | Correctifs de sécurité |
| IP statique obligatoire | Stabilité du cluster |
| NTP synchronisé | Essentiel pour cluster et Ceph |
| No-subscription pour homelab | Gratuit et stable |
| Enterprise pour production | Support officiel |
| Backup config `/etc/pve/` | Recovery en cas de problème |

---

## Commande Associée

Voir `/px-setup` pour les opérations de configuration initiale.
