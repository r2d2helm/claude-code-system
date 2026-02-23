# /pve-gpu - GPU et PCI Passthrough

## Description
Configuration du passthrough GPU et peripheriques PCI vers les VMs Proxmox.
Inclut IOMMU, vfio, passthrough complet et mediated devices (vGPU/SR-IOV).

## Syntaxe
```
/pve-gpu <action> [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `list` | `/pve-gpu list` | Lister GPU et PCI disponibles |
| `iommu` | `/pve-gpu iommu` | Verifier groupes IOMMU |
| `passthrough` | `/pve-gpu passthrough <vmid> <pci>` | Configurer passthrough |
| `vgpu` | `/pve-gpu vgpu` | Gestion mediated devices |
| `status` | `/pve-gpu status` | Etat des GPU assignees |

## Exemples

### Prerequis IOMMU

```bash
# Verifier support IOMMU
dmesg | grep -i iommu

# Activer IOMMU dans GRUB (Intel)
# Editer /etc/default/grub :
# GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt"
update-grub

# Activer IOMMU dans GRUB (AMD)
# GRUB_CMDLINE_LINUX_DEFAULT="quiet amd_iommu=on iommu=pt"
update-grub

# Charger modules VFIO
cat >> /etc/modules <<EOF
vfio
vfio_iommu_type1
vfio_pci
EOF

# Appliquer et redemarrer
update-initramfs -u -k all
# NECESSITE UN REBOOT
```

### Lister les peripheriques PCI

```bash
# Lister tous les GPU
lspci -nn | grep -i 'vga\|3d\|display'

# Lister groupes IOMMU
find /sys/kernel/iommu_groups/ -type l | sort -V | \
  while read f; do
    echo "IOMMU Group $(basename $(dirname $f)):"
    lspci -nns "$(basename $f)"
  done

# Identifier le PCI ID d'un GPU
lspci -nn -s 01:00
# Ex: 01:00.0 VGA compatible controller [0300]: NVIDIA Corporation [10de:2684]
# Ex: 01:00.1 Audio device [0403]: NVIDIA Corporation [10de:22ba]
```

### Blacklister le driver hote

```bash
# Blacklister le driver NVIDIA sur l'hote
echo "blacklist nouveau" >> /etc/modprobe.d/blacklist.conf
echo "blacklist nvidia" >> /etc/modprobe.d/blacklist.conf

# Forcer VFIO pour le GPU (remplacer IDs par les votres)
echo "options vfio-pci ids=10de:2684,10de:22ba" > /etc/modprobe.d/vfio.conf

# Appliquer
update-initramfs -u -k all
# NECESSITE UN REBOOT
```

### Passthrough GPU vers VM

```bash
# Passthrough GPU complet (tout le groupe IOMMU)
qm set 100 --hostpci0 0000:01:00,pcie=1,x-vga=1

# GPU NVIDIA avec audio
qm set 100 --hostpci0 0000:01:00,pcie=1,x-vga=1

# Machine q35 requise pour PCIe passthrough
qm set 100 --machine q35

# BIOS OVMF requis
qm set 100 --bios ovmf

# Desactiver display VNC (GPU prend le relais)
qm set 100 --vga none

# Multi-GPU passthrough
qm set 100 --hostpci0 0000:01:00,pcie=1,x-vga=1
qm set 100 --hostpci1 0000:02:00,pcie=1
```

### USB Passthrough

```bash
# Lister peripheriques USB
lsusb

# Passthrough par vendor:product ID
qm set 100 --usb0 host=1234:5678

# Passthrough par port USB (physique)
qm set 100 --usb0 host=1-2

# USB3 passthrough (XHCI)
qm set 100 --usb0 host=1234:5678,usb3=1
```

### SR-IOV (PVE 9+)

```bash
# Verifier support SR-IOV
lspci -vvv -s 01:00.0 | grep -i "sr-iov"

# Activer Virtual Functions
echo 4 > /sys/class/net/enp1s0f0/device/sriov_numvfs

# Rendre persistant
echo "enp1s0f0 4" >> /etc/pve/sriov.conf

# Assigner VF a une VM
qm set 100 --hostpci0 0000:01:00.1,pcie=1
```

## Notes

- Machine q35 et BIOS OVMF obligatoires pour PCIe passthrough
- Tout le groupe IOMMU est assigne (verifier les peripheriques inclus)
- NVIDIA : le driver detecte la virtualisation, utiliser le flag `x-vga=1`
- Un seul GPU passthrough par VM (sauf multi-GPU explicite)
- Hot-plug PCI non supporte : la VM doit etre arretee pour modifier
- SR-IOV permet de partager un GPU entre plusieurs VMs (si supporte)
- Sauvegarder la configuration GRUB et modules avant modification

## Voir Aussi
- `/pve-vm` - Gestion machines virtuelles
- `/pve-node` - Configuration node
- `/pve-diag` - Diagnostic materiel
