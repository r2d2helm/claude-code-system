# Wizard: Création de Machine Virtuelle

## Mode d'emploi
Ce wizard guide la création d'une VM optimisée pour Proxmox VE 9+. Répondez aux questions pour générer la commande personnalisée.

---

## Questions Interactives

### 1. Informations de Base

**Q1.1: Quel nom pour la VM?**
```
Nom: _______________
(ex: web-server-01, dc-primary, dev-ubuntu)
```

**Q1.2: Quel VMID? (100-999999)**
```
VMID: _____ (laisser vide pour auto)
```

**Q1.3: Sur quel node?**
```
Node: _______________
(ex: pve1, pve-node-01)
```

---

### 2. Système d'Exploitation

**Q2.1: Quel OS installer?**

| Option | OS | ISO suggéré |
|--------|----|----|
| A | Windows 11/Server 2025 | windows11.iso |
| B | Windows 10/Server 2022 | windows10.iso |
| C | Ubuntu 24.04 LTS | ubuntu-24.04-server.iso |
| D | Debian 13 | debian-13-netinst.iso |
| E | Rocky/Alma Linux 9 | rocky-9-minimal.iso |
| F | Autre Linux | [spécifier] |
| G | Cloud-Init Template | [aucun ISO] |

```
Choix: ___ ISO: _______________
```

**Q2.2: Architecture?**
```
[ ] x86_64 (défaut)
[ ] aarch64 (ARM)
```

---

### 3. Ressources Compute

**Q3.1: Combien de vCPUs?**
```
vCPUs: _____ (recommandé: 2-8 pour serveur, 4-16 pour desktop)
```

**Q3.2: Type de CPU?**

| Option | Type | Usage |
|--------|------|-------|
| A | host | Performance max (défaut recommandé) |
| B | x86-64-v3 | Migration entre CPUs similaires |
| C | x86-64-v2-AES | Compatibilité large |
| D | kvm64 | Compatibilité maximale |

```
Choix: ___ (A recommandé)
```

**Q3.3: Combien de RAM (GB)?**
```
RAM: _____ GB (ex: 4, 8, 16, 32)
```

**Q3.4: Activer le ballooning?**
```
[ ] Oui - Mémoire dynamique (défaut pour Linux)
[ ] Non - Mémoire fixe (Windows, databases)
```

---

### 4. Stockage

**Q4.1: Sur quel storage le disque système?**
```
Storage: _______________
(ex: local-zfs, ceph-pool, nfs-data)
```

**Q4.2: Taille du disque système (GB)?**
```
Taille: _____ GB (ex: 32 Linux, 64 Windows)
```

**Q4.3: Format de disque?**

| Option | Format | Recommandation |
|--------|--------|----------------|
| A | raw | Performance (ZFS, Ceph, LVM) |
| B | qcow2 | Snapshots (dir storage) |

```
Choix: ___
```

**Q4.4: Activer SSD emulation / Discard?**
```
[ ] Oui - SSD avec TRIM (défaut pour SSD/NVMe)
[ ] Non - HDD classique
```

---

### 5. Réseau

**Q5.1: Quel bridge réseau?**
```
Bridge: _______________
(ex: vmbr0, vmbr1)
```

**Q5.2: VLAN tag? (optionnel)**
```
VLAN: _____ (laisser vide si aucun)
```

**Q5.3: Modèle carte réseau?**
```
[ ] VirtIO (défaut - meilleure perf)
[ ] E1000 (compatibilité Windows sans drivers)
[ ] vmxnet3 (migration VMware)
```

---

### 6. Options Avancées

**Q6.1: Machine Type?**
```
[ ] q35 (défaut - moderne, PCIe)
[ ] i440fx (legacy, rare)
```

**Q6.2: BIOS/Firmware?**
```
[ ] OVMF/UEFI (défaut - moderne, Secure Boot)
[ ] SeaBIOS (legacy, MBR)
```

**Q6.3: TPM 2.0? (requis Windows 11)**
```
[ ] Oui - vTPM 2.0 qcow2 (PVE 9+)
[ ] Non
```

**Q6.4: Activer l'agent QEMU?**
```
[ ] Oui (défaut - shutdown propre, freeze backup)
[ ] Non
```

**Q6.5: Ajouter à un groupe HA?**
```
[ ] Non
[ ] Oui - Groupe: _______________
```

---

## Génération de Commande

### Template Commande Base

```bash
qm create VMID \
  --name "NAME" \
  --memory RAM_MB \
  --cores VCPUS \
  --cpu cputype=CPU_TYPE \
  --machine q35 \
  --bios ovmf \
  --ostype OS_TYPE \
  --scsihw virtio-scsi-single \
  --scsi0 STORAGE:DISK_SIZE,iothread=1,discard=on,ssd=1 \
  --net0 virtio,bridge=BRIDGE,firewall=1 \
  --agent enabled=1 \
  --efidisk0 STORAGE:1,efitype=4m,pre-enrolled-keys=1 \
  --start 0
```

---

## Configurations Prêtes à l'Emploi

### Windows 11 / Server 2025 (Optimisé)

```bash
qm create 100 \
  --name "win11-desktop" \
  --memory 8192 \
  --cores 4 \
  --cpu cputype=host \
  --machine q35 \
  --bios ovmf \
  --ostype win11 \
  --scsihw virtio-scsi-single \
  --scsi0 local-zfs:64,iothread=1,discard=on,ssd=1 \
  --ide2 local:iso/Win11_24H2.iso,media=cdrom \
  --net0 virtio,bridge=vmbr0,firewall=1 \
  --agent enabled=1 \
  --tpmstate0 local-zfs:1,version=v2.0 \
  --efidisk0 local-zfs:1,efitype=4m,pre-enrolled-keys=1 \
  --start 0

# Post-install: Installer VirtIO drivers depuis virtio-win.iso
```

### Ubuntu 24.04 Server (Optimisé)

```bash
qm create 101 \
  --name "ubuntu-server" \
  --memory 4096 \
  --cores 2 \
  --cpu cputype=host \
  --machine q35 \
  --bios ovmf \
  --ostype l26 \
  --scsihw virtio-scsi-single \
  --scsi0 local-zfs:32,iothread=1,discard=on,ssd=1 \
  --ide2 local:iso/ubuntu-24.04-live-server-amd64.iso,media=cdrom \
  --net0 virtio,bridge=vmbr0,firewall=1 \
  --agent enabled=1 \
  --efidisk0 local-zfs:1,efitype=4m \
  --start 0

# Post-install: apt install qemu-guest-agent && systemctl enable qemu-guest-agent
```

### Cloud-Init Template (Ubuntu)

```bash
# Télécharger image cloud
wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img

# Créer VM template
qm create 9000 \
  --name "ubuntu-24.04-template" \
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

# Importer disque
qm importdisk 9000 noble-server-cloudimg-amd64.img local-zfs

# Attacher disque et cloud-init
qm set 9000 --scsi0 local-zfs:vm-9000-disk-0,iothread=1,discard=on,ssd=1
qm set 9000 --ide2 local-zfs:cloudinit
qm set 9000 --boot order=scsi0
qm set 9000 --serial0 socket --vga serial0

# Convertir en template
qm template 9000
```

### VM Haute Performance (Base de Données)

```bash
qm create 102 \
  --name "postgres-primary" \
  --memory 32768 \
  --balloon 0 \
  --cores 8 \
  --cpu cputype=host \
  --numa 1 \
  --machine q35 \
  --bios ovmf \
  --ostype l26 \
  --scsihw virtio-scsi-single \
  --scsi0 local-zfs:50,iothread=1,discard=on,ssd=1,cache=none \
  --scsi1 local-zfs:200,iothread=1,discard=on,ssd=1,cache=none \
  --net0 virtio,bridge=vmbr0,firewall=1 \
  --agent enabled=1 \
  --efidisk0 local-zfs:1,efitype=4m \
  --start 0

# scsi0 = système, scsi1 = data PostgreSQL
# balloon=0 = mémoire fixe pour DB
# numa=1 = optimisation NUMA
```

---

## Best Practices VM 2026

### Configuration Recommandée

| Paramètre | Valeur | Raison |
|-----------|--------|--------|
| Machine | q35 | Support PCIe natif |
| BIOS | OVMF | UEFI moderne, Secure Boot |
| CPU | host | Performance maximale |
| SCSI | virtio-scsi-single | Meilleur I/O avec iothread |
| iothread | 1 | Thread dédié par disque |
| discard | on | Support TRIM/unmap |
| Agent | enabled | Shutdown propre, freeze backup |

### Windows Spécifique

- **TPM 2.0**: Obligatoire Windows 11, recommandé Server 2025
- **Drivers VirtIO**: Installer depuis virtio-win.iso
- **Guest Agent**: Installer QEMU Guest Agent (qemu-ga-x64.msi)

### Linux Spécifique

- **qemu-guest-agent**: `apt install qemu-guest-agent`
- **Cloud-Init**: Idéal pour templates et automation

---

## Commande Associée

Voir `/pve-vm` pour toutes les opérations VM.
