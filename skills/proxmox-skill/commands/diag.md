# /pve-diag - Diagnostic & Troubleshooting

## Description
Diagnostic complet et resolution de problemes Proxmox VE 9+.

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

## Diagnostics Specifiques

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

### `network` - Diagnostic Reseau
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

> Voir aussi : [[diag-advanced]]
