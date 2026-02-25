---
name: backup-skill
description: "Backup et restauration : snapshots Proxmox, rsync, PostgreSQL dumps, vault Obsidian, retention, disaster recovery."
prefix: /bak-*
---

# Super Agent Backup & Recovery

Agent intelligent pour la sauvegarde et restauration du homelab r2d2 : VMs Proxmox, bases PostgreSQL, fichiers via rsync, vault Obsidian, avec gestion de retention et disaster recovery.

## Philosophie

> "Un backup non teste est un backup qui n'existe pas."

## Perimetre

| Cible | Methode | Destination | Frequence |
|-------|---------|-------------|-----------|
| VMs Proxmox (100-105) | vzdump snapshot | Proxmox storage | Quotidien |
| PostgreSQL (VM 104) | pg_dump --format=custom | NFS + local | Toutes les 6h |
| Vault Obsidian | git push + rsync | Remote git + NFS | A chaque commit |
| Fichiers critiques | rsync incremental | VM 104 NFS | Quotidien |
| Config Claude Code | rsync / copie | claude-config-backup | Hebdomadaire |
| Docker volumes | docker cp + tar | NFS | Hebdomadaire |

## Infrastructure

| Machine | IP | Role backup |
|---------|-----|-------------|
| Proxmox Host | 192.168.1.215 | vzdump, snapshots ZFS |
| VM 100 r2d2-stage | 192.168.1.162 | Monitoring (source) |
| VM 103 r2d2-main | 192.168.1.163 | Dev principal (source critique) |
| VM 104 r2d2-store | 192.168.1.164 | PostgreSQL + NFS (destination principale) |
| VM 105 r2d2-lab | 192.168.1.161 | Lab (source) |
| Windows r2d2 | locale | Vault Obsidian, config Claude Code |

## Commandes Slash

### Operations

| Commande | Description |
|----------|-------------|
| `/bak-status` | Dashboard de tous les backups (dates, tailles, sante) |
| `/bak-create` | Creer un backup (vm-snapshot, pg-dump, files-rsync, vault-git) |
| `/bak-restore` | Restaurer depuis un backup |
| `/bak-list` | Lister les backups par type, VM ou date |

### PostgreSQL

| Commande | Description |
|----------|-------------|
| `/bak-pg` | Backup/restore specifique PostgreSQL (pg_dump, pg_restore) |

### Planification & Maintenance

| Commande | Description |
|----------|-------------|
| `/bak-schedule` | Gerer les planifications (cron, Task Scheduler) |
| `/bak-verify` | Verifier l'integrite d'un backup |
| `/bak-prune` | Nettoyer les vieux backups selon la politique de retention |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/bak-wizard setup` | Configuration initiale d'une strategie de backup (regle 3-2-1) |
| `/bak-wizard strategy` | Aide au choix de la strategie (retention, frequence, destinations) |

## Regle 3-2-1

La regle fondamentale de tout plan de backup :

- **3 copies** de chaque donnee (1 originale + 2 sauvegardes)
- **2 supports differents** (SSD/HDD, local/NFS, disque/cloud)
- **1 copie hors-site** (NFS distant, git remote, cloud storage)

### Application au homelab r2d2

| Donnee | Copie 1 (originale) | Copie 2 (locale) | Copie 3 (distante) |
|--------|---------------------|-------------------|---------------------|
| VMs | Proxmox ZFS | vzdump local | vzdump NFS (VM 104) |
| PostgreSQL | VM 104 live | pg_dump local | pg_dump NFS |
| Vault Obsidian | PC Windows | git local (.git) | git remote |
| Config Claude | PC Windows | claude-config-backup | rsync VM 104 |

## Politique de Retention

### Standard (recommandee)

| Granularite | Conservation | Exemple |
|-------------|-------------|---------|
| Quotidien | 7 jours | lun-dim de la semaine courante |
| Hebdomadaire | 4 semaines | 4 derniers dimanches |
| Mensuel | 12 mois | 1er de chaque mois |
| Annuel | 2 ans | 1er janvier (optionnel) |

### Par type de donnee

| Type | Quotidien | Hebdo | Mensuel | Taille estimee/backup |
|------|-----------|-------|---------|----------------------|
| VM snapshot | 7j | 4sem | 6mois | 2-10 GB |
| pg_dump | 7j | 4sem | 12mois | 50 MB - 2 GB |
| Vault Obsidian | illimite (git) | - | - | ~100 MB |
| Docker volumes | - | 4sem | 6mois | 500 MB - 5 GB |

## Conventions

### Nommage des fichiers de backup

```
# VM snapshots
vzdump-qemu-{vmid}-{YYYY_MM_DD-HH_MM_SS}.vma.zst

# PostgreSQL dumps
pg-{dbname}-{YYYY-MM-DD_HHMMSS}.dump         # format custom
pg-{dbname}-{YYYY-MM-DD_HHMMSS}.sql.gz       # format SQL compresse

# Fichiers rsync
rsync-{source}-{YYYY-MM-DD}/                  # repertoire incremental

# Docker volumes
docker-vol-{container}-{volume}-{YYYY-MM-DD}.tar.gz
```

### Repertoires de destination (VM 104 NFS)

```
/mnt/nfs/backups/
├── proxmox/          # vzdump exports
├── postgresql/       # pg_dump files
├── rsync/            # rsync incrementaux
├── docker-volumes/   # exports de volumes Docker
└── config/           # configurations systeme
```

### Verification

- **Toujours tester les restaurations** au moins une fois par mois
- **Verifier les checksums** apres transfert (md5sum, sha256sum)
- **Monitorer l'espace disque** (P2 a 74% sur certaines VMs)
- **Logger chaque operation** de backup/restore avec timestamp et statut

## Integration avec les autres skills

| Skill | Integration |
|-------|-------------|
| **proxmox-skill** | `/pve-backup`, `/pve-snapshot` pour les operations Proxmox natives |
| **docker-skill** | `/dk-volume` pour identifier les volumes a sauvegarder |
| **monitoring-skill** | `/mon-status` pour verifier l'espace disque avant backup |
| **linux-skill** | `/lx-*` pour les operations systeme sur les VMs |
| **obsidian-skill** | `/obs-backup` pour le vault Obsidian |

## Troubleshooting

### Backup vzdump echoue
1. Verifier l'espace disque : `pvesm status`
2. Verifier les locks : `qm unlock {vmid}`
3. Verifier les logs : `/var/log/vzdump/*.log`
4. Tester le storage : `pvesm alloc {storage} test 1G`

### pg_dump echoue
1. Verifier la connexion : `pg_isready -h 192.168.1.164`
2. Verifier les droits : l'utilisateur doit avoir CONNECT + SELECT
3. Verifier l'espace disque local et distant
4. Tester un dump minimal : `pg_dump -Fc -t petite_table dbname`

### rsync lent ou echoue
1. Verifier la bande passante : `iperf3 -c {destination}`
2. Verifier les permissions SSH : key-based auth recommandee
3. Utiliser `--partial --progress` pour reprendre apres interruption
4. Exclure les fichiers temporaires : `--exclude='*.tmp' --exclude='.cache'`

### Espace disque insuffisant
1. Identifier les gros backups : `du -sh /mnt/nfs/backups/*`
2. Executer `/bak-prune` pour appliquer la retention
3. Verifier les snapshots orphelins : `qm listsnapshot {vmid}`
4. Nettoyer Docker : `/dk-prune`
