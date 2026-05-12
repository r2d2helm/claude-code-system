> Partie avancee de [[diag]]. Commandes essentielles dans le fichier principal.

# /pve-diag - Diagnostic & Troubleshooting (Avance)

## Description
Problemes courants, procedures de recovery, logs importants et commandes rapides.

## Problemes Courants

### VM ne demarre pas
```bash
# 1. Vérifier erreur
qm start {vmid} 2>&1

# 2. Vérifier ressources
pvesh get /cluster/resources --type vm | grep {vmid}

# 3. Vérifier stockage
pvesm status

# 4. Vérifier lock
qm unlock {vmid}

# 5. Vérifier logs
journalctl -u "qemu-server@{vmid}" -n 50
```

### Cluster partition/split brain
```bash
# 1. Vérifier quorum
pvecm status | grep -i quorum

# 2. Vérifier réseau corosync
corosync-cfgtool -s

# 3. Si node isolé, forcer quorum local
pvecm expected 1

# 4. Resync config cluster
systemctl restart pve-cluster

# 5. Vérifier /etc/pve monté
ls -la /etc/pve/
```

### Stockage full
```bash
# 1. Identifier le problème
df -h
zfs list

# 2. Nettoyer snapshots anciens
pvesm prune-backups {storage}

# 3. Supprimer fichiers temporaires
rm -rf /var/tmp/vzdumptmp*

# 4. Analyser usage
du -sh /var/lib/vz/*
ncdu /var

# 5. ZFS: supprimer snapshots
zfs list -t snapshot
zfs destroy tank/data@old_snapshot
```

### Migration echoue
```bash
# 1. Vérifier connectivité entre nodes
ssh {target_node} "echo ok"

# 2. Vérifier stockage partagé
pvesm status | grep shared

# 3. Vérifier ressources cible
pvesh get /nodes/{target}/status

# 4. Migration avec verbose
qm migrate {vmid} {target} --online --with-local-disks 2>&1

# 5. Logs migration
journalctl -u pveproxy --since "10 minutes ago" | grep migrate
```

### Ceph degraded
```bash
# 1. Status
ceph health detail

# 2. OSDs down
ceph osd tree | grep down

# 3. PGs problématiques
ceph pg dump_stuck

# 4. Rebalancing progress
ceph -w

# 5. Réparer OSD
ceph osd repair {osd_id}
```

## Logs Importants

```bash
# Logs système
journalctl -p err --since "24 hours ago"

# Logs Proxmox
tail -f /var/log/daemon.log
journalctl -u pvedaemon -f
journalctl -u pveproxy -f

# Logs VM/CT
journalctl -u "qemu-server@*" --since "1 hour ago"
journalctl -u "pve-container@*" --since "1 hour ago"

# Logs cluster
journalctl -u pve-cluster -f
journalctl -u corosync -f

# Logs Ceph
journalctl -u "ceph-*" --since "1 hour ago"

# Logs backup
cat /var/log/vzdump/*.log
```

## Recovery Procedures

### Recuperer cluster casse
```bash
# Sur node survivant
systemctl stop pve-cluster corosync

# Forcer mode local
pmxcfs -l

# Éditer /etc/pve sans cluster
# Puis redémarrer
systemctl start pve-cluster
```

### Recuperer VM locked
```bash
# Identifier le lock
ls -la /var/lock/qemu-server/

# Forcer unlock
rm /var/lock/qemu-server/lock-{vmid}.conf
qm unlock {vmid}
```

### Recuperer config VM
```bash
# Depuis backup PBS
proxmox-backup-client restore {backup_id} qemu-server.conf /tmp/

# Depuis snapshot ZFS
zfs rollback tank/vm-{vmid}-disk-0@{snapshot}
```

## Commandes Rapides

```bash
# Health check rapide
pve-diag

# Services
systemctl status pve-cluster pvedaemon pveproxy

# Cluster
pvecm status

# Resources
pvesh get /cluster/resources

# Logs erreurs
journalctl -p err --since "1 hour ago"
```
