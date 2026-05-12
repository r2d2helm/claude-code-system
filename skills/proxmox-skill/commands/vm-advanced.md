> Partie avancée de [[vm]]. Commandes essentielles dans le fichier principal.

# /pve-vm - Wizard Interactif et Exemples Avancés

## Description
Wizard interactif de création VM et exemples avancés pour Proxmox VE.

## Wizard Interactif : Création VM

```
/pve-vm create --wizard
```

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  🧙 WIZARD: CRÉATION MACHINE VIRTUELLE                                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Étape 1/8: INFORMATIONS GÉNÉRALES                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  VMID [auto]:        > 100                                                   ║
║  Nom:                > web-server-01                                         ║
║  Node [pve01]:       > pve01                                                 ║
║                                                                              ║
║  Étape 2/8: SYSTÈME D'EXPLOITATION                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Type OS:                                                                    ║
║    [1] Linux (kernel 6.x+)     ← Recommandé                                  ║
║    [2] Linux (kernel 5.x)                                                    ║
║    [3] Windows 11/Server 2025                                                ║
║    [4] Windows 10/Server 2022                                                ║
║    [5] Autre                                                                 ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  ISO d'installation:                                                         ║
║    [1] ubuntu-24.04-live-server-amd64.iso                                    ║
║    [2] debian-12.9-amd64-netinst.iso                                         ║
║    [3] rocky-9.5-x86_64-minimal.iso                                          ║
║    [4] Aucun (PXE boot)                                                      ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Étape 3/8: SYSTÈME (BIOS/Machine)                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Machine type:                                                               ║
║    [1] q35 (moderne, PCIe)     ← Recommandé 2025                             ║
║    [2] i440fx (legacy)                                                       ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  BIOS:                                                                       ║
║    [1] OVMF (UEFI)             ← Recommandé                                  ║
║    [2] SeaBIOS (Legacy)                                                      ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Secure Boot:        [Y/n] > Y                                               ║
║                                                                              ║
║  Étape 4/8: CPU                                                              ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Type CPU:                                                                   ║
║    [1] host (performance max)  ← Recommandé                                  ║
║    [2] x86-64-v3 (compatible)                                                ║
║    [3] kvm64 (très compatible)                                               ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Cores [4]:          > 4                                                     ║
║  Sockets [1]:        > 1                                                     ║
║  NUMA [auto]:        > Y                                                     ║
║                                                                              ║
║  Étape 5/8: MÉMOIRE                                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  RAM (MB) [4096]:    > 8192                                                  ║
║  Ballooning:         [Y/n] > Y                                               ║
║  Min RAM (MB) [2048]:> 4096                                                  ║
║                                                                              ║
║  Étape 6/8: STOCKAGE                                                         ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Storage:                                                                    ║
║    [1] local-zfs (ZFS, 2.1TB free)                                           ║
║    [2] ceph-pool (RBD, 25TB free)                                            ║
║    [3] nfs-data (NFS, 4TB free)                                              ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Taille disque (GB) [50]: > 50                                               ║
║  Controller:                                                                 ║
║    [1] VirtIO SCSI Single      ← Recommandé (iothread)                       ║
║    [2] VirtIO SCSI                                                           ║
║    [3] VirtIO Block                                                          ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Options disque:                                                             ║
║    [x] Discard (TRIM)          ← Recommandé SSD/thin                         ║
║    [x] IO Thread               ← Recommandé                                  ║
║    [x] SSD Emulation           ← Si stockage SSD                             ║
║  Cache [none]:       > none                                                  ║
║                                                                              ║
║  Étape 7/8: RÉSEAU                                                           ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Bridge [vmbr0]:     > vmbr0                                                 ║
║  Model:                                                                      ║
║    [1] VirtIO                  ← Recommandé                                  ║
║    [2] E1000                                                                 ║
║    [3] RTL8139                                                               ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  VLAN Tag [none]:    >                                                       ║
║  Firewall:           [Y/n] > Y                                               ║
║                                                                              ║
║  Étape 8/8: OPTIONS AVANCÉES                                                 ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  QEMU Guest Agent:   [Y/n] > Y                                               ║
║  Start at boot:      [y/N] > Y                                               ║
║  Start after create: [y/N] > N                                               ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  📋 RÉSUMÉ CONFIGURATION                                                     ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  VMID: 100           Name: web-server-01          Node: pve01                ║
║  OS: Linux 6.x       Machine: q35                 BIOS: OVMF (Secure Boot)   ║
║  CPU: host, 4 cores  RAM: 8192 MB (balloon 4096)  Disk: 50GB local-zfs       ║
║  Network: virtio/vmbr0 + firewall                 Agent: enabled             ║
║                                                                              ║
║  Commande générée:                                                           ║
║  qm create 100 --name "web-server-01" --node pve01 --ostype l26 \            ║
║    --machine q35 --bios ovmf --efidisk0 local-zfs:1,efitype=4m \             ║
║    --cpu host --cores 4 --numa 1 --memory 8192 --balloon 4096 \              ║
║    --scsihw virtio-scsi-single \                                             ║
║    --scsi0 local-zfs:50,discard=on,iothread=1,ssd=1 \                        ║
║    --ide2 local:iso/ubuntu-24.04-live-server-amd64.iso,media=cdrom \         ║
║    --net0 virtio,bridge=vmbr0,firewall=1 --agent enabled=1 --onboot 1        ║
║                                                                              ║
║  Confirmer création? [Y/n] > Y                                               ║
║                                                                              ║
║  ✅ VM 100 créée avec succès!                                                ║
║  💡 Démarrez avec: qm start 100                                              ║
║  💡 Console VNC: https://pve01:8006/?console=kvm&vmid=100                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
