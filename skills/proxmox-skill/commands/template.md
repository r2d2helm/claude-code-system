# 📋 /pve-template - Templates & Cloud-Init

## Description
Création et gestion de templates VM/CT avec Cloud-Init pour Proxmox VE 9+.

## Syntaxe
```
/pve-template [action] [options]
```

## Cloud Images Supportées

### URLs Cloud Images 2025
```bash
# Ubuntu 24.04 LTS (Noble)
https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img

# Debian 12 (Bookworm)
https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-generic-amd64.qcow2

# Rocky Linux 9
https://download.rockylinux.org/pub/rocky/9/images/x86_64/Rocky-9-GenericCloud.latest.x86_64.qcow2

# AlmaLinux 9
https://repo.almalinux.org/almalinux/9/cloud/x86_64/images/AlmaLinux-9-GenericCloud-latest.x86_64.qcow2

# Fedora Cloud
https://download.fedoraproject.org/pub/fedora/linux/releases/40/Cloud/x86_64/images/Fedora-Cloud-Base-Generic.x86_64-40-1.14.qcow2

# Windows Server 2025 (nécessite licence)
# Créer manuellement avec pilotes VirtIO
```

## Créer Template Ubuntu Cloud-Init

### Méthode complète
```bash
#!/bin/bash
# create-ubuntu-template.sh

TEMPLATE_ID=9000
TEMPLATE_NAME="ubuntu-2404-cloud"
STORAGE="local-lvm"
CLOUD_IMAGE_URL="https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"

# 1. Télécharger l'image
wget -O /tmp/ubuntu-cloud.img $CLOUD_IMAGE_URL

# 2. Créer la VM
qm create $TEMPLATE_ID \
  --name $TEMPLATE_NAME \
  --memory 2048 \
  --cores 2 \
  --cpu host \
  --net0 virtio,bridge=vmbr0 \
  --scsihw virtio-scsi-single \
  --ostype l26 \
  --agent enabled=1,fstrim_cloned_disks=1 \
  --machine q35 \
  --bios ovmf \
  --efidisk0 ${STORAGE}:1,efitype=4m,pre-enrolled-keys=1

# 3. Importer le disque
qm set $TEMPLATE_ID --scsi0 ${STORAGE}:0,import-from=/tmp/ubuntu-cloud.img,iothread=1,discard=on

# 4. Configurer Cloud-Init
qm set $TEMPLATE_ID \
  --ide2 ${STORAGE}:cloudinit \
  --boot order=scsi0 \
  --serial0 socket \
  --vga serial0

# 5. Configurer defaults Cloud-Init
qm set $TEMPLATE_ID \
  --ciuser admin \
  --cipassword "$(openssl rand -base64 12)" \
  --sshkeys ~/.ssh/authorized_keys \
  --ipconfig0 ip=dhcp

# 6. Redimensionner le disque
qm disk resize $TEMPLATE_ID scsi0 32G

# 7. Convertir en template
qm template $TEMPLATE_ID

# Cleanup
rm /tmp/ubuntu-cloud.img

echo "Template $TEMPLATE_ID ($TEMPLATE_NAME) created successfully!"
```

## Créer Template Debian Cloud-Init

```bash
#!/bin/bash
# create-debian-template.sh

TEMPLATE_ID=9001
TEMPLATE_NAME="debian-12-cloud"
STORAGE="local-lvm"

# Télécharger
wget -O /tmp/debian-cloud.qcow2 \
  https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-generic-amd64.qcow2

# Créer VM
qm create $TEMPLATE_ID \
  --name $TEMPLATE_NAME \
  --memory 2048 \
  --cores 2 \
  --cpu host \
  --net0 virtio,bridge=vmbr0 \
  --scsihw virtio-scsi-single \
  --ostype l26 \
  --agent enabled=1 \
  --machine q35

# Importer disque
qm importdisk $TEMPLATE_ID /tmp/debian-cloud.qcow2 $STORAGE
qm set $TEMPLATE_ID --scsi0 ${STORAGE}:vm-${TEMPLATE_ID}-disk-0,iothread=1,discard=on

# Cloud-Init
qm set $TEMPLATE_ID \
  --ide2 ${STORAGE}:cloudinit \
  --boot order=scsi0 \
  --serial0 socket

# Template
qm template $TEMPLATE_ID

rm /tmp/debian-cloud.qcow2
```

## Créer Template Windows Server

```bash
#!/bin/bash
# create-windows-template.sh
# Nécessite: ISO Windows + ISO VirtIO drivers

TEMPLATE_ID=9010
TEMPLATE_NAME="windows-2025-template"
STORAGE="local-lvm"

# 1. Créer VM avec TPM pour Windows 11/Server 2025
qm create $TEMPLATE_ID \
  --name $TEMPLATE_NAME \
  --memory 4096 \
  --cores 4 \
  --cpu host \
  --net0 virtio,bridge=vmbr0 \
  --scsihw virtio-scsi-single \
  --ostype win11 \
  --machine q35 \
  --bios ovmf \
  --efidisk0 ${STORAGE}:1,efitype=4m,pre-enrolled-keys=1 \
  --tpmstate0 ${STORAGE}:1,version=v2.0 \
  --agent enabled=1

# 2. Ajouter disque système
qm set $TEMPLATE_ID --scsi0 ${STORAGE}:64,iothread=1,discard=on

# 3. Monter ISOs
qm set $TEMPLATE_ID \
  --ide0 local:iso/Windows_Server_2025.iso,media=cdrom \
  --ide1 local:iso/virtio-win.iso,media=cdrom

# 4. Boot order
qm set $TEMPLATE_ID --boot order="ide0;scsi0"

echo "VM $TEMPLATE_ID created. Install Windows manually, then convert to template."
echo "After install:"
echo "  1. Install VirtIO drivers"
echo "  2. Install QEMU Guest Agent"
echo "  3. Run sysprep /generalize /oobe /shutdown"
echo "  4. qm template $TEMPLATE_ID"
```

## Cloner depuis Template

### Clone lié (rapide, dépendant)
```bash
# Clone lié (utilise backing file)
qm clone 9000 100 --name "web-01" --full 0
```

### Clone complet (indépendant)
```bash
# Clone complet
qm clone 9000 100 \
  --name "web-01" \
  --full 1 \
  --storage local-lvm

# Personnaliser Cloud-Init
qm set 100 \
  --ipconfig0 ip=192.168.1.100/24,gw=192.168.1.1 \
  --nameserver 8.8.8.8 \
  --searchdomain example.com \
  --ciuser webadmin \
  --sshkeys ~/.ssh/web_server.pub

# Démarrer
qm start 100
```

## Templates Conteneurs LXC

### Télécharger templates CT
```bash
# Lister templates disponibles
pveam available

# Télécharger
pveam download local debian-12-standard_12.7-1_amd64.tar.zst
pveam download local ubuntu-24.04-standard_24.04-2_amd64.tar.zst
pveam download local alpine-3.20-default_20240729_amd64.tar.xz

# Lister templates locaux
pveam list local
```

### OCI Images (PVE 9.1+)
```bash
# Créer CT depuis image Docker Hub
pct create 300 docker:debian:12 \
  --hostname debian-oci \
  --storage local-lvm \
  --rootfs local-lvm:8 \
  --memory 512 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp \
  --unprivileged 1

# Images supportées
# docker:nginx:latest
# docker:redis:alpine
# docker:postgres:16
```

## Configuration Cloud-Init

### Paramètres disponibles
```bash
# Utilisateur et authentification
qm set {vmid} \
  --ciuser admin \
  --cipassword "secure_password" \
  --sshkeys /root/.ssh/authorized_keys

# Réseau
qm set {vmid} \
  --ipconfig0 ip=192.168.1.100/24,gw=192.168.1.1 \
  --ipconfig1 ip=10.0.0.100/24 \
  --nameserver "8.8.8.8 8.8.4.4" \
  --searchdomain example.com

# Custom Cloud-Init (snippets)
qm set {vmid} --cicustom "user=local:snippets/user-data.yml"
```

### Custom Cloud-Init Snippets
```yaml
# /var/lib/vz/snippets/user-data.yml
#cloud-config
package_update: true
package_upgrade: true

packages:
  - qemu-guest-agent
  - htop
  - vim
  - curl

users:
  - name: admin
    groups: sudo
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... admin@workstation

runcmd:
  - systemctl enable --now qemu-guest-agent
  - echo "Cloud-Init completed" > /var/log/cloud-init-done
```

### Activer snippets storage
```bash
# Éditer storage
pvesm set local --content images,rootdir,vztmpl,backup,iso,snippets
```

## Gestion Templates

### Lister templates
```bash
# VMs templates
qm list | grep template

# Via API
pvesh get /cluster/resources --type vm | jq '.[] | select(.template==1)'
```

### Supprimer template
```bash
# Supprimer (attention aux clones liés!)
qm destroy 9000
```

### Exporter/Importer
```bash
# Exporter template
vzdump 9000 --storage backup --compress zstd --mode stop

# Importer
qmrestore /var/lib/vz/dump/vzdump-qemu-9000-*.vma.zst 9000 --unique
qm template 9000
```

## Automation Templates

### Script batch cloning
```bash
#!/bin/bash
# batch-clone.sh

TEMPLATE=9000
STORAGE="local-lvm"
START_VMID=100
COUNT=5
PREFIX="web"

for i in $(seq 1 $COUNT); do
    VMID=$((START_VMID + i - 1))
    NAME="${PREFIX}-$(printf '%02d' $i)"
    IP="192.168.1.$((100 + i - 1))"
    
    echo "Creating $NAME ($VMID) with IP $IP..."
    
    qm clone $TEMPLATE $VMID --name $NAME --full 1 --storage $STORAGE
    qm set $VMID --ipconfig0 ip=${IP}/24,gw=192.168.1.1
    qm start $VMID
done
```

### Terraform templates
```hcl
resource "proxmox_virtual_environment_vm" "servers" {
  count     = 5
  name      = "web-${format("%02d", count.index + 1)}"
  node_name = "pve1"
  vm_id     = 100 + count.index

  clone {
    vm_id = 9000
  }

  initialization {
    ip_config {
      ipv4 {
        address = "192.168.1.${100 + count.index}/24"
        gateway = "192.168.1.1"
      }
    }
  }
}
```

## Best Practices

1. **Nommage**: template-{os}-{version}-{date}
2. **VMID**: Réserver plage 9000-9099 pour templates
3. **Agent**: Toujours installer qemu-guest-agent
4. **Minimal**: Templates légers, personnaliser via Cloud-Init
5. **Documentation**: Maintenir liste des templates et leurs configs
6. **Mise à jour**: Recréer templates mensuellement
