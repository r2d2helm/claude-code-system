---
name: bak-status
description: Dashboard complet de tous les backups du homelab
---

# /bak-status - Dashboard Backup Homelab

## Comportement

Affiche un dashboard complet de l'etat de tous les backups du homelab r2d2.

1. **Verifier les snapshots Proxmox** via SSH :
   - Lister les snapshots de chaque VM (100, 103, 104, 105)
   - Identifier les snapshots anciens (> 7 jours)

2. **Verifier les dumps PostgreSQL** sur VM 104 :
   - Derniere date de dump
   - Taille des dumps
   - Bases couvertes

3. **Verifier le vault Obsidian** :
   - Dernier commit git
   - Fichiers non commites
   - Taille du repo

4. **Verifier l'espace disque** sur les destinations de backup :
   - VM 104 NFS
   - Proxmox local storage

5. **Evaluer la regle 3-2-1** :
   - 3 copies existent ?
   - 2 supports differents ?
   - 1 copie distante ?

## Commandes de collecte

```bash
# --- Proxmox snapshots ---
ssh root@192.168.1.215 "for vmid in 100 103 104 105; do echo '=== VM \$vmid ==='; qm listsnapshot \$vmid 2>/dev/null || echo 'Pas de snapshot'; done"

# --- Derniers vzdump ---
ssh root@192.168.1.215 "ls -lht /var/lib/vz/dump/ | head -20"

# --- PostgreSQL dumps (VM 104) ---
ssh r2d2helm@192.168.1.164 "ls -lht /mnt/nfs/backups/postgresql/ 2>/dev/null || echo 'Repertoire non trouve'"

# --- Vault Obsidian (local) ---
cd C:\Users\r2d2\Documents\Knowledge && git log --oneline -5
git status --short

# --- Espace disque VM 104 ---
ssh r2d2helm@192.168.1.164 "df -h /mnt/nfs/backups/ 2>/dev/null || df -h /"

# --- Espace disque Proxmox ---
ssh root@192.168.1.215 "pvesm status"
```

## Format de sortie

```
# Backup Dashboard - r2d2 Homelab

## Snapshots Proxmox
| VM | Dernier snapshot | Age | Nombre total |
|----|------------------|-----|--------------|
| 100 r2d2-stage | 2026-02-24 | 1j | 3 |
| 103 r2d2-main | 2026-02-25 | 0j | 2 |
| 104 r2d2-store | 2026-02-23 | 2j | 4 |
| 105 r2d2-lab | 2026-02-20 | 5j | 1 |

## Dumps PostgreSQL (VM 104)
| Base | Dernier dump | Taille | Format |
|------|-------------|--------|--------|
| taskyn | 2026-02-25 06:00 | 128 MB | custom |
| supabase | 2026-02-25 06:00 | 450 MB | custom |

## Vault Obsidian
- Dernier commit: 2026-02-25 "daily update"
- Fichiers non commites: 3
- Taille repo: 95 MB

## Espace disponible
| Destination | Utilise | Disponible | % |
|-------------|---------|------------|---|
| VM 104 NFS | 45 GB | 155 GB | 22% |
| Proxmox local | 180 GB | 70 GB | 72% |

## Regle 3-2-1
- [OK] 3 copies: originale + snapshot + NFS
- [OK] 2 supports: SSD Proxmox + HDD NFS
- [WARN] 1 copie distante: vault git OK, VMs pas de offsite
```

## Exemples

```
/bak-status              # Dashboard complet
/bak-status vm           # Seulement les snapshots VM
/bak-status pg           # Seulement PostgreSQL
/bak-status vault        # Seulement le vault Obsidian
/bak-status disk         # Seulement l'espace disque
```
