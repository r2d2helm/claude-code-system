# Wizard: Stratégie de Backup

## Mode d'emploi
Ce wizard configure une stratégie de sauvegarde complète pour Proxmox VE 9+ avec support PBS (Proxmox Backup Server), NFS et stockage local.

---

## Questions Interactives

### 1. Cible de Backup

**Q1.1: Où sauvegarder?**

| Option | Cible | Avantages |
|--------|-------|-----------|
| A | Proxmox Backup Server (PBS) | Dédup, incrémental, chiffrement, vérification |
| B | NFS/CIFS | Simple, compatible, partagé |
| C | Stockage local | Rapide, pas de réseau |

```
Choix: ___
```

**Q1.2: Détails de la cible?**
```
Si PBS:  Server: _______________ Datastore: _______________
Si NFS:  Server: _______________ Export: _______________
Si Local: Path: _______________
```

**Q1.3: Activer le chiffrement? (PBS uniquement)**
```
[ ] Oui - Chiffrement AES-256-GCM côté client
[ ] Non
```

---

### 2. Planification

**Q2.1: Fréquence des backups?**

| Option | Fréquence | Cron |
|--------|-----------|------|
| A | Quotidien à 2h | 0 2 * * * |
| B | Quotidien à 22h | 0 22 * * * |
| C | 2x par jour | 0 2,14 * * * |
| D | Hebdomadaire dimanche 3h | 0 3 * * 0 |
| E | Personnalisé | _______________ |

```
Choix: ___
```

---

### 3. Rétention

**Q3.1: Politique de rétention?**
```
keep-daily:   _____ (recommandé: 7)
keep-weekly:  _____ (recommandé: 4)
keep-monthly: _____ (recommandé: 6)
keep-yearly:  _____ (recommandé: 2)
```

---

### 4. VMs/CTs à Sauvegarder

**Q4.1: Quoi sauvegarder?**

| Option | Sélection |
|--------|-----------|
| A | Toutes les VMs/CTs |
| B | Sélection par VMID |
| C | Sélection par pool |
| D | Exclure certains VMIDs |

```
Choix: ___
VMIDs (si B): _______________
Pool (si C): _______________
Exclusions (si D): _______________
```

**Q4.2: Mode de backup?**

| Option | Mode | Impact |
|--------|------|--------|
| A | Snapshot | Pas de downtime (défaut, recommandé) |
| B | Suspend | Courte pause mémoire |
| C | Stop | Arrêt complet (cohérence maximale) |

```
Choix: ___
```

**Q4.3: Compression?**

| Option | Algorithme | Vitesse vs Ratio |
|--------|-----------|------------------|
| A | zstd (défaut) | Meilleur compromis |
| B | lzo | Plus rapide |
| C | gzip | Meilleur ratio |

```
Choix: ___
```

---

## Génération de Commandes

### Ajouter le Storage PBS

```bash
pvesm add pbs PBS_ID \
  --server PBS_IP \
  --port 8007 \
  --datastore DATASTORE \
  --username backup@pbs \
  --password PASSWORD \
  --fingerprint FINGERPRINT \
  --content backup
```

### Ajouter le Storage NFS

```bash
pvesm add nfs NFS_ID \
  --server NFS_IP \
  --export /path/to/export \
  --path /mnt/pve/NFS_ID \
  --content backup,iso,vztmpl
```

### Créer le Job de Backup

```bash
# Via /etc/pve/jobs.cfg
cat >> /etc/pve/jobs.cfg << 'EOF'
vzdump: backup-daily
    enabled 1
    schedule 0 2 * * *
    storage PBS_ID
    mode snapshot
    compress zstd
    all 1
    notes-template {{guestname}} - {{cluster}}
    prune-backups keep-daily=7,keep-weekly=4,keep-monthly=6,keep-yearly=2
EOF
```

### Backup Manuel

```bash
# Toutes les VMs
vzdump --all --storage PBS_ID --mode snapshot --compress zstd

# VMs spécifiques
vzdump 100 101 200 --storage PBS_ID --mode snapshot --compress zstd

# Avec notification email
vzdump --all --storage PBS_ID --mode snapshot --mailnotification always --mailto admin@example.com
```

### Vérifier

```bash
# Lister les backups
pvesm list PBS_ID --content backup

# Vérifier un backup (PBS)
proxmox-backup-client verify BACKUP_ID --repository user@pbs:DATASTORE
```

---

## Best Practices 2026

| Règle | Raison |
|-------|--------|
| Règle 3-2-1 | 3 copies, 2 médias, 1 offsite |
| Tester les restores | Un backup non testé n'est pas un backup |
| PBS > NFS | Dédup, incrémental, vérification intégrée |
| Snapshot mode | Pas de downtime pour les VMs |
| Chiffrement PBS | Protection des données sensibles |
| Rétention progressive | Granularité décroissante dans le temps |
| Monitorer les jobs | Alertes email sur échec |

---

## Commande Associée

Voir `/px-backup` pour les opérations de sauvegarde.
