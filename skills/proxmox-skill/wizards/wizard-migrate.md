# Wizard: Migration vers Proxmox

## Mode d'emploi
Ce wizard guide la migration de VMs depuis VMware, Hyper-V ou entre nodes Proxmox VE 9+.

---

## Questions Interactives

### 1. Type de Migration

**Q1.1: D'où migrez-vous?**

| Option | Source | Méthode |
|--------|--------|---------|
| A | VMware ESXi/vCenter | Import OVF/VMDK |
| B | Hyper-V | Conversion VHDX → qcow2 |
| C | Autre Proxmox (entre nodes) | qm migrate (live) |
| D | Machine physique (P2V) | Clonezilla/dd + import |
| E | Fichier disque (VMDK, VHDX, VDI, raw) | qm importdisk |

```
Choix: ___
```

---

### 2. Source VMware (si option A)

**Q2.1: Type d'export?**

| Option | Méthode |
|--------|---------|
| A | Export OVA/OVF depuis vCenter/ESXi |
| B | Copie directe VMDK via SCP/datastore |

```
Choix: ___
Chemin fichier OVA/OVF: _______________
ou IP ESXi: _______________ Username: _______________
```

**Q2.2: VMs à migrer?**
```
VM 1: _______________ (nom)
VM 2: _______________ (nom)
```

---

### 3. Migration entre Proxmox (si option C)

**Q3.1: VMID de la VM à migrer?**
```
VMID: _____
```

**Q3.2: Node destination?**
```
Target: _______________ (ex: pve2)
```

**Q3.3: Type de migration?**

| Option | Type | Downtime |
|--------|------|----------|
| A | Online (live) | Quasi-nul (<1s) |
| B | Offline | Arrêt complet pendant migration |

```
Choix: ___
```

**Q3.4: Migrer le stockage aussi?**
```
[ ] Oui - Déplacer les disques vers le storage du node cible
[ ] Non - Stockage partagé (Ceph, NFS)
Storage cible (si oui): _______________
```

---

### 4. Configuration Cible

**Q4.1: VMID cible? (si import)**
```
VMID: _____ (laisser vide pour auto)
```

**Q4.2: Storage cible?**
```
Storage: _______________ (ex: local-zfs, ceph-pool)
```

**Q4.3: Réseau cible?**
```
Bridge: _______________ (ex: vmbr0)
VLAN (optionnel): _____
```

---

## Génération de Commandes

### Import VMware OVF

```bash
# Import OVF
qm importovf VMID /path/to/vm.ovf STORAGE

# Si OVA, extraire d'abord
tar xvf vm.ova
qm importovf VMID vm.ovf STORAGE

# Post-import: ajuster la config
qm set VMID --machine q35 --bios ovmf --cpu cputype=host
qm set VMID --scsihw virtio-scsi-single
qm set VMID --net0 virtio,bridge=vmbr0
```

### Import Disque VMDK/VHDX

```bash
# Importer un disque
qm importdisk VMID /path/to/disk.vmdk STORAGE --format qcow2

# Attacher le disque importé
qm set VMID --scsi0 STORAGE:vm-VMID-disk-0,iothread=1

# Définir le boot
qm set VMID --boot order=scsi0
```

### Conversion Hyper-V VHDX

```bash
# Convertir VHDX → qcow2
qemu-img convert -f vhdx -O qcow2 disk.vhdx disk.qcow2

# Importer
qm importdisk VMID disk.qcow2 STORAGE
```

### Migration Live entre Nodes

```bash
# Migration live (stockage partagé)
qm migrate VMID TARGET_NODE --online

# Migration avec déplacement de stockage
qm migrate VMID TARGET_NODE --online --with-local-disks --targetstorage STORAGE
```

### Déplacer un Disque

```bash
# Déplacer un disque vers un autre storage
qm move-disk VMID scsi0 STORAGE --delete 1
```

---

## Checklist Post-Migration

- [ ] Installer/vérifier les drivers VirtIO (Windows)
- [ ] Installer qemu-guest-agent (Linux: `apt install qemu-guest-agent`)
- [ ] Ajuster CPU type à `host` pour performance
- [ ] Vérifier le réseau et les IPs
- [ ] Passer en machine q35 + OVMF si possible
- [ ] Supprimer les VMware Tools / Hyper-V Integration Services
- [ ] Tester un snapshot + restore

---

## Best Practices 2026

| Règle | Raison |
|-------|--------|
| Tester avec une VM non-critique d'abord | Valider le processus |
| Snapshot avant migration | Rollback possible |
| Installer VirtIO avant migration Windows | Éviter le boot sur drivers SCSI inconnus |
| Préférer live migration | Zéro downtime |
| Vérifier la compatibilité UEFI/BIOS | Adapter le firmware si nécessaire |

---

## Commande Associée

Voir `/px-migrate` pour les opérations de migration.
