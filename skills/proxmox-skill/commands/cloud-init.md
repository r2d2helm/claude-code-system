# /pve-cloud-init - Configuration Cloud-Init

## Description
Gestion de Cloud-Init pour le provisionnement automatique des VMs Proxmox.
Configuration reseau, utilisateurs, cles SSH et scripts de demarrage.

## Syntaxe
```
/pve-cloud-init <action> <vmid> [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `config` | `/pve-cloud-init config <vmid>` | Voir configuration |
| `set` | `/pve-cloud-init set <vmid>` | Configurer Cloud-Init |
| `dump` | `/pve-cloud-init dump <vmid>` | Voir les fichiers generes |
| `regenerate` | `/pve-cloud-init regenerate <vmid>` | Regenerer l'image |
| `template` | `/pve-cloud-init template` | Creer template Cloud-Init |

## Exemples

### Creer un template Cloud-Init

```bash
# Telecharger image cloud Ubuntu 24.04
wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img

# Creer VM depuis l'image cloud
qm create 9000 --name "template-ubuntu2404" --memory 2048 --cores 2 \
  --net0 virtio,bridge=vmbr0 --machine q35 --bios ovmf \
  --efidisk0 local-zfs:1,efitype=4m

# Importer le disque
qm importdisk 9000 noble-server-cloudimg-amd64.img local-zfs

# Attacher le disque importe
qm set 9000 --scsihw virtio-scsi-single \
  --scsi0 local-zfs:vm-9000-disk-1,discard=on,iothread=1,ssd=1

# Ajouter drive Cloud-Init
qm set 9000 --ide2 local-zfs:cloudinit

# Configurer le boot
qm set 9000 --boot order=scsi0 --serial0 socket --vga serial0

# Configurer Cloud-Init par defaut
qm set 9000 --ciuser admin --cipassword "changeme" \
  --sshkeys ~/.ssh/authorized_keys \
  --ipconfig0 ip=dhcp

# Convertir en template
qm template 9000
```

### Configurer Cloud-Init sur une VM

```bash
# Utilisateur et mot de passe
qm set 100 --ciuser admin
qm set 100 --cipassword "secure-password"

# Cles SSH (depuis fichier)
qm set 100 --sshkeys ~/.ssh/authorized_keys

# Cles SSH (depuis URL)
qm set 100 --sshkeys <(curl -s https://github.com/user.keys)

# Configuration IP statique
qm set 100 --ipconfig0 ip=10.0.0.50/24,gw=10.0.0.1

# Configuration DHCP
qm set 100 --ipconfig0 ip=dhcp

# Double stack IPv4 + IPv6
qm set 100 --ipconfig0 ip=10.0.0.50/24,gw=10.0.0.1,ip6=fd00::50/64,gw6=fd00::1

# DNS
qm set 100 --nameserver "10.0.0.1 1.1.1.1"
qm set 100 --searchdomain "example.com"

# Plusieurs interfaces reseau
qm set 100 --ipconfig0 ip=10.0.0.50/24,gw=10.0.0.1
qm set 100 --ipconfig1 ip=10.0.1.50/24
```

### Custom Cloud-Init (snippets)

```bash
# Activer snippets sur le stockage
pvesm set local --content images,rootdir,vztmpl,backup,iso,snippets

# Appliquer un snippet user-data custom
qm set 100 --cicustom "user=local:snippets/user-data.yml"

# Snippet user + vendor
qm set 100 --cicustom "user=local:snippets/user-data.yml,vendor=local:snippets/vendor-data.yml"
```

### Deployer depuis template

```bash
# Cloner template
qm clone 9000 100 --name "web-01" --full

# Configurer l'instance
qm set 100 --ipconfig0 ip=10.0.0.50/24,gw=10.0.0.1
qm set 100 --ciuser deploy --sshkeys ~/.ssh/id_ed25519.pub

# Regenerer Cloud-Init et demarrer
qm cloudinit update 100
qm start 100

# Deploiement en masse (boucle)
for i in $(seq 1 5); do
  qm clone 9000 "$((100+i))" --name "web-0$i" --full
  qm set "$((100+i))" --ipconfig0 "ip=10.0.0.$((50+i))/24,gw=10.0.0.1"
  qm cloudinit update "$((100+i))" && qm start "$((100+i))"
done
```

### Voir la configuration generee

```bash
# Voir la config Cloud-Init
qm cloudinit dump 100 user
qm cloudinit dump 100 network
qm cloudinit dump 100 meta

# Voir les parametres en attente
qm cloudinit pending 100
```

## Notes

- Cloud-Init s'execute uniquement au premier boot (ou apres regeneration)
- Les modifications Cloud-Init necessitent `qm cloudinit update` puis reboot
- Le drive Cloud-Init est un petit disque ISO monte automatiquement
- Privilegier les cles SSH au mot de passe pour la securite
- Les snippets custom permettent d'installer des paquets et executer des scripts
- Toujours inclure qemu-guest-agent dans le user-data

## Voir Aussi
- `/pve-template` - Gestion des templates
- `/pve-vm` - Gestion des machines virtuelles
- `/pve-network` - Configuration reseau
