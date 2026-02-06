# 🔧 /pve-diag - Diagnostic & Troubleshooting

## Description
Diagnostic complet et résolution de problèmes Proxmox VE 9+.

## Syntaxe
```
/pve-diag [action] [options]
```

## Script Diagnostic Complet

### Installation
```bash
cat > /usr/local/bin/pve-diag << 'SCRIPT'
#!/bin/bash
#===============================================
# PVE-DIAG - Proxmox Diagnostic Tool
# Version: 2.0 (PVE 9+ compatible)
#===============================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_header() {
    echo ""
    echo "=========================================="
    echo " $1"
    echo "=========================================="
}

print_ok() { echo -e "${GREEN}[OK]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

print_header "PROXMOX DIAGNOSTIC REPORT"
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo "PVE Version: $(pveversion)"

print_header "SYSTEM STATUS"
# Uptime
uptime

# Load
LOAD=$(cat /proc/loadavg | awk '{print $1}')
CORES=$(nproc)
if (( $(echo "$LOAD > $CORES" | bc -l) )); then
    print_warn "High load: $LOAD (cores: $CORES)"
else
    print_ok "Load: $LOAD (cores: $CORES)"
fi

# Memory
MEM_TOTAL=$(free -g | awk '/^Mem:/{print $2}')
MEM_USED=$(free -g | awk '/^Mem:/{print $3}')
MEM_PCT=$((MEM_USED * 100 / MEM_TOTAL))
if [ $MEM_PCT -gt 90 ]; then
    print_error "Memory critical: ${MEM_PCT}% used"
elif [ $MEM_PCT -gt 80 ]; then
    print_warn "Memory high: ${MEM_PCT}% used"
else
    print_ok "Memory: ${MEM_PCT}% used (${MEM_USED}G/${MEM_TOTAL}G)"
fi

# Disk root
ROOT_PCT=$(df -h / | awk 'NR==2{print $5}' | tr -d '%')
if [ $ROOT_PCT -gt 90 ]; then
    print_error "Root disk critical: ${ROOT_PCT}%"
elif [ $ROOT_PCT -gt 80 ]; then
    print_warn "Root disk high: ${ROOT_PCT}%"
else
    print_ok "Root disk: ${ROOT_PCT}%"
fi

print_header "CLUSTER STATUS"
if [ -f /etc/pve/corosync.conf ]; then
    pvecm status 2>/dev/null | grep -E "Cluster|Quorum|Node" || print_warn "Cluster status unavailable"
else
    echo "Single node (no cluster)"
fi

print_header "SERVICES STATUS"
for svc in pve-cluster pvedaemon pveproxy pvestatd; do
    if systemctl is-active --quiet $svc; then
        print_ok "$svc is running"
    else
        print_error "$svc is NOT running"
    fi
done

print_header "STORAGE STATUS"
pvesm status 2>/dev/null | while read line; do
    echo "$line"
done

# ZFS
if command -v zpool &> /dev/null; then
    echo ""
    echo "ZFS Pools:"
    zpool list 2>/dev/null || echo "No ZFS pools"
    zpool status -x 2>/dev/null | grep -v "all pools are healthy" && print_warn "ZFS issues detected"
fi

# Ceph
if command -v ceph &> /dev/null && [ -f /etc/pve/ceph.conf ]; then
    echo ""
    echo "Ceph Status:"
    ceph health 2>/dev/null || echo "Ceph not available"
fi

print_header "NETWORK STATUS"
ip -br addr show | grep -v "^lo"
echo ""
echo "Bridges:"
brctl show 2>/dev/null | head -10

print_header "VMs/CTs STATUS"
echo "Running VMs: $(qm list 2>/dev/null | grep running | wc -l)"
echo "Stopped VMs: $(qm list 2>/dev/null | grep stopped | wc -l)"
echo "Running CTs: $(pct list 2>/dev/null | grep running | wc -l)"
echo "Stopped CTs: $(pct list 2>/dev/null | grep stopped | wc -l)"

print_header "RECENT ERRORS (last 1h)"
journalctl --since "1 hour ago" -p err --no-pager | tail -20

print_header "RECOMMENDATIONS"
# Updates
UPDATES=$(apt list --upgradable 2>/dev/null | grep -c upgradable)
if [ $UPDATES -gt 0 ]; then
    print_warn "$UPDATES packages can be updated"
fi

# Subscription
if [ ! -f /etc/apt/sources.list.d/pve-enterprise.list ] || grep -q "^#" /etc/apt/sources.list.d/pve-enterprise.list 2>/dev/null; then
    print_warn "No enterprise subscription detected"
fi

echo ""
echo "Diagnostic completed."
SCRIPT

chmod +x /usr/local/bin/pve-diag
```

## Diagnostics Spécifiques

### `cluster` - Diagnostic Cluster
```bash
# Status cluster
pvecm status

# Nodes
pvecm nodes

# Quorum
pvecm expected 1  # Vérifier quorum

# Corosync
corosync-cfgtool -s

# Logs cluster
journalctl -u pve-cluster -f
journalctl -u corosync -f
```

### `storage` - Diagnostic Stockage
```bash
# Status tous storages
pvesm status

# ZFS health
zpool status -v
zpool list -v
zfs list -o name,used,avail,refer,mountpoint

# Ceph health
ceph -s
ceph health detail
ceph osd tree
ceph df

# SMART disques
for disk in /dev/sd?; do
    echo "=== $disk ==="
    smartctl -H $disk 2>/dev/null | grep -E "SMART|overall"
done

# I/O stats
iostat -xz 1 5
```

### `vm` - Diagnostic VM
```bash
# Status VM
qm status {vmid}

# Config VM
qm config {vmid}

# Logs VM
journalctl -u "qemu-server@{vmid}" --since "1 hour ago"

# Process QEMU
ps aux | grep "qemu.*{vmid}"

# Ressources VM
qm monitor {vmid} -c "info status"
qm monitor {vmid} -c "info block"

# Débloquer VM locked
qm unlock {vmid}
```

### `ct` - Diagnostic CT
```bash
# Status CT
pct status {vmid}

# Config CT
pct config {vmid}

# Entrer dans CT
pct enter {vmid}

# Logs CT
journalctl -u "pve-container@{vmid}" --since "1 hour ago"

# Ressources CT
pct exec {vmid} -- free -h
pct exec {vmid} -- df -h
```

### `network` - Diagnostic Réseau
```bash
# Interfaces
ip addr show
ip -s link show

# Routes
ip route show

# Bridges
brctl show
bridge link show

# SDN status
pvesh get /cluster/sdn/status

# Connectivity test
ping -c 3 {gateway}
ping -c 3 8.8.8.8

# DNS
nslookup google.com

# Ports ouverts
ss -tulpn | grep LISTEN
```

### `ha` - Diagnostic HA
```bash
# Status HA
ha-manager status

# Config HA
cat /etc/pve/ha/resources.cfg
cat /etc/pve/ha/groups.cfg

# Logs HA
journalctl -u pve-ha-crm --since "1 hour ago"
journalctl -u pve-ha-lrm --since "1 hour ago"

# Fencing test
ha-manager fencing status
```

## Problèmes Courants

### VM ne démarre pas
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

### Migration échoue
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

### Récupérer cluster cassé
```bash
# Sur node survivant
systemctl stop pve-cluster corosync

# Forcer mode local
pmxcfs -l

# Éditer /etc/pve sans cluster
# Puis redémarrer
systemctl start pve-cluster
```

### Récupérer VM locked
```bash
# Identifier le lock
ls -la /var/lock/qemu-server/

# Forcer unlock
rm /var/lock/qemu-server/lock-{vmid}.conf
qm unlock {vmid}
```

### Récupérer config VM
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
