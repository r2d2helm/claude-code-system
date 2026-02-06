# Wizard: Création de Templates VM/CT

## Mode d'emploi
Ce wizard guide la création de templates réutilisables pour VMs (Cloud-Init) et conteneurs (CT) sur Proxmox VE 9+.

---

## Questions Interactives

### 1. Type de Template

**Q1.1: Quel type de template?**

| Option | Type | Usage |
|--------|------|-------|
| A | VM Cloud-Init | Déploiement automatisé VMs Linux |
| B | VM manuelle | Template depuis VM configurée |
| C | Conteneur (CT) | Template LXC |

```
Choix: ___
```

---

### 2. VM Cloud-Init (si option A)

**Q2.1: Quel OS?**

| Option | OS | Image Cloud |
|--------|----|----|
| A | Ubuntu 24.04 LTS | noble-server-cloudimg-amd64.img |
| B | Ubuntu 22.04 LTS | jammy-server-cloudimg-amd64.img |
| C | Debian 13 | debian-13-generic-amd64.qcow2 |
| D | Debian 12 | debian-12-generic-amd64.qcow2 |
| E | Rocky Linux 9 | Rocky-9-GenericCloud.latest.x86_64.qcow2 |
| F | Alma Linux 9 | AlmaLinux-9-GenericCloud-latest.x86_64.qcow2 |

```
Choix: ___
```

**Q2.2: VMID du template? (9000-9999 recommandé)**
```
VMID: _____
```

**Q2.3: Ressources par défaut?**
```
vCPUs: _____ (défaut: 2)
RAM:   _____ GB (défaut: 2)
Disk:  _____ GB (défaut: 20)
```

**Q2.4: Storage?**
```
Storage: _______________ (ex: local-zfs)
```

**Q2.5: Configuration Cloud-Init?**
```
Utilisateur par défaut: _______________ (ex: admin, ubuntu)
Clé SSH publique: _______________
(ou fichier: ~/.ssh/id_ed25519.pub)
```

**Q2.6: Packages à pré-installer?**
```
[ ] qemu-guest-agent (recommandé)
[ ] curl, wget, git
[ ] docker.io
[ ] Autre: _______________
```

---

### 3. VM Manuelle (si option B)

**Q3.1: VMID de la VM source?**
```
VMID source: _____
```

**Q3.2: La VM est prête à être templatisée?**
```
[ ] OS mis à jour
[ ] Logs nettoyés
[ ] SSH host keys supprimés
[ ] Machine-id vidé
[ ] Utilisateur générique créé
```

---

### 4. Conteneur Template (si option C)

**Q4.1: Image de base?**
```
[ ] Télécharger depuis les repos Proxmox (pveam)
[ ] Importer un fichier tar.gz custom
```

**Q4.2: Quel OS CT?**

| Option | OS | Template |
|--------|----|----|
| A | Ubuntu 24.04 | ubuntu-24.04-standard |
| B | Debian 13 | debian-13-standard |
| C | Alpine 3.20 | alpine-3.20-default |
| D | Rocky Linux 9 | rockylinux-9-default |

```
Choix: ___
```

---

## Génération de Commandes

### Template Cloud-Init Ubuntu

```bash
# 1. Télécharger l'image cloud
wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img

# 2. Créer la VM
qm create 9000 \
  --name "ubuntu-24.04-ci-template" \
  --memory 2048 \
  --cores 2 \
  --cpu cputype=host \
  --machine q35 \
  --bios ovmf \
  --ostype l26 \
  --scsihw virtio-scsi-single \
  --net0 virtio,bridge=vmbr0 \
  --agent enabled=1 \
  --efidisk0 local-zfs:1,efitype=4m

# 3. Importer le disque
qm importdisk 9000 noble-server-cloudimg-amd64.img local-zfs

# 4. Configurer
qm set 9000 --scsi0 local-zfs:vm-9000-disk-0,iothread=1,discard=on,ssd=1
qm set 9000 --ide2 local-zfs:cloudinit
qm set 9000 --boot order=scsi0
qm set 9000 --serial0 socket --vga serial0

# 5. Cloud-Init defaults
qm set 9000 --ciuser admin
qm set 9000 --sshkeys ~/.ssh/id_ed25519.pub
qm set 9000 --ipconfig0 ip=dhcp

# 6. Redimensionner le disque
qm resize 9000 scsi0 +18G  # 2G base + 18G = 20G total

# 7. Convertir en template
qm template 9000
```

### Cloner depuis un Template

```bash
# Clone complet
qm clone 9000 NEW_VMID --name "vm-name" --full 1 --storage local-zfs

# Clone lié (rapide, dépend du template)
qm clone 9000 NEW_VMID --name "vm-name" --full 0

# Personnaliser Cloud-Init
qm set NEW_VMID --ciuser myuser --ipconfig0 ip=10.10.10.50/24,gw=10.10.10.1
qm start NEW_VMID
```

### Template VM Manuelle

```bash
# Préparer la VM (depuis la VM elle-même)
sudo apt update && sudo apt upgrade -y
sudo apt clean
sudo rm -rf /tmp/* /var/tmp/*
sudo truncate -s 0 /var/log/*.log
sudo rm -f /etc/ssh/ssh_host_*
sudo truncate -s 0 /etc/machine-id
sudo cloud-init clean --logs 2>/dev/null
history -c

# Depuis Proxmox
qm shutdown VMID
qm template VMID
```

### Template CT

```bash
# Télécharger le template
pveam update
pveam available | grep ubuntu-24
pveam download local ubuntu-24.04-standard_24.04-1_amd64.tar.zst

# Créer CT depuis template
pct create 200 local:vztmpl/ubuntu-24.04-standard_24.04-1_amd64.tar.zst \
  --hostname ct-template \
  --memory 1024 \
  --cores 2 \
  --rootfs local-zfs:8 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp \
  --unprivileged 1

# Personnaliser puis convertir
pct start 200
# ... installer packages ...
pct stop 200
# Le CT peut servir de base pour pct clone
```

---

## Best Practices 2026

| Règle | Raison |
|-------|--------|
| VMID 9000-9999 pour templates | Convention de rangement |
| Cloud-Init > VM manuelle | Automatisation, reproductibilité |
| Minimiser la taille du template | Clones plus rapides |
| Mettre à jour avant templatisation | Base saine |
| Supprimer les SSH host keys | Clés uniques par clone |
| Documenter les templates | Tags et descriptions dans Proxmox |

---

## Commande Associée

Voir `/px-template` pour les opérations templates.
