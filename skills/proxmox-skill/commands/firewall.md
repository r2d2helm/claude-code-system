# 🔥 /pve-firewall - Firewall Proxmox

## Description
Gestion du firewall intégré Proxmox VE 9+ (iptables/nftables).

## Syntaxe
```
/pve-firewall [action] [options]
```

## Architecture Firewall

```
┌─────────────────────────────────────────────────────┐
│                 Firewall Proxmox                     │
├─────────────────────────────────────────────────────┤
│  NIVEAU DATACENTER (global)                         │
│  ├── Security Groups (réutilisables)                │
│  ├── Alias (IP/réseaux nommés)                     │
│  └── IPSets (groupes IP)                           │
│                                                     │
│  NIVEAU HOST (par node)                             │
│  └── Règles spécifiques au node                    │
│                                                     │
│  NIVEAU VM/CT (par guest)                          │
│  └── Règles par interface réseau                   │
└─────────────────────────────────────────────────────┘
```

## Actions Disponibles

### `status` - État du firewall
```bash
# Status global
pve-firewall status

# Status cluster
pvesh get /cluster/firewall/options

# Règles actives
pve-firewall localinfo
```

### `enable` - Activer le firewall
```bash
# Activer au niveau datacenter
pvesh set /cluster/firewall/options --enable 1

# Activer au niveau host
pvesh set /nodes/{node}/firewall/options --enable 1

# Activer pour une VM
pvesh set /nodes/{node}/qemu/{vmid}/firewall/options --enable 1

# Activer pour un CT
pvesh set /nodes/{node}/lxc/{vmid}/firewall/options --enable 1
```

### `disable` - Désactiver le firewall
```bash
pvesh set /cluster/firewall/options --enable 0
pvesh set /nodes/{node}/qemu/{vmid}/firewall/options --enable 0
```

## Règles Datacenter

### `rules add` - Ajouter règle globale
```bash
# Autoriser SSH depuis management
pvesh create /cluster/firewall/rules \
  --action ACCEPT \
  --type in \
  --proto tcp \
  --dport 22 \
  --source 10.0.0.0/24 \
  --comment "SSH Management"

# Autoriser HTTPS API
pvesh create /cluster/firewall/rules \
  --action ACCEPT \
  --type in \
  --proto tcp \
  --dport 8006 \
  --source 10.0.0.0/24 \
  --comment "Proxmox Web UI"

# Bloquer tout le reste (règle par défaut)
pvesh set /cluster/firewall/options --policy_in DROP
```

### `rules list` - Lister les règles
```bash
# Règles datacenter
pvesh get /cluster/firewall/rules

# Règles d'un node
pvesh get /nodes/{node}/firewall/rules

# Règles d'une VM
pvesh get /nodes/{node}/qemu/{vmid}/firewall/rules
```

### `rules delete` - Supprimer une règle
```bash
# Par position
pvesh delete /cluster/firewall/rules/{pos}
```

## Security Groups

### Créer un groupe
```bash
# Groupe pour serveurs Web
pvesh create /cluster/firewall/groups \
  --group webservers \
  --comment "Web Servers Rules"

# Ajouter règles au groupe
pvesh create /cluster/firewall/groups/webservers \
  --action ACCEPT \
  --type in \
  --proto tcp \
  --dport 80 \
  --comment "HTTP"

pvesh create /cluster/firewall/groups/webservers \
  --action ACCEPT \
  --type in \
  --proto tcp \
  --dport 443 \
  --comment "HTTPS"
```

### Appliquer groupe à une VM
```bash
pvesh create /nodes/{node}/qemu/{vmid}/firewall/rules \
  --action GROUP \
  --type group \
  --comment "webservers"
```

## Alias & IPSets

### Créer un alias
```bash
# Alias réseau
pvesh create /cluster/firewall/aliases \
  --name management \
  --cidr 10.0.0.0/24

# Alias hôte
pvesh create /cluster/firewall/aliases \
  --name jumpbox \
  --cidr 10.0.0.100
```

### Créer un IPSet
```bash
# IPSet serveurs
pvesh create /cluster/firewall/ipset \
  --name trusted_servers

# Ajouter IPs au set
pvesh create /cluster/firewall/ipset/trusted_servers \
  --cidr 10.0.1.10
pvesh create /cluster/firewall/ipset/trusted_servers \
  --cidr 10.0.1.11
pvesh create /cluster/firewall/ipset/trusted_servers \
  --cidr 10.0.1.12
```

### Utiliser dans règles
```bash
# Règle avec alias
pvesh create /cluster/firewall/rules \
  --action ACCEPT \
  --type in \
  --proto tcp \
  --dport 22 \
  --source +management

# Règle avec IPSet
pvesh create /cluster/firewall/rules \
  --action ACCEPT \
  --type in \
  --proto tcp \
  --dport 3306 \
  --source +trusted_servers
```

## Configuration VM/CT

### Activer firewall sur interface
```bash
# VM - activer FW sur net0
qm set 100 --net0 virtio,bridge=vmbr0,firewall=1

# CT - activer FW sur eth0
pct set 200 --net0 name=eth0,bridge=vmbr0,firewall=1
```

### Règles spécifiques VM
```bash
# Autoriser port spécifique
pvesh create /nodes/{node}/qemu/100/firewall/rules \
  --action ACCEPT \
  --type in \
  --proto tcp \
  --dport 8080 \
  --comment "App Port"

# Autoriser ICMP
pvesh create /nodes/{node}/qemu/100/firewall/rules \
  --action ACCEPT \
  --type in \
  --proto icmp \
  --comment "Ping"
```

### Options VM
```bash
# Configurer options VM
pvesh set /nodes/{node}/qemu/100/firewall/options \
  --enable 1 \
  --policy_in DROP \
  --policy_out ACCEPT \
  --log_level_in info \
  --macfilter 1 \
  --ipfilter 1
```

## Configuration Fichiers

### /etc/pve/firewall/cluster.fw
```ini
[OPTIONS]
enable: 1
policy_in: DROP
policy_out: ACCEPT
log_level_in: info

[ALIASES]
management = 10.0.0.0/24
monitoring = 10.0.10.0/24

[IPSET trusted]
10.0.0.10
10.0.0.11
10.0.0.12

[RULES]
IN ACCEPT -source +management -p tcp -dport 22 # SSH
IN ACCEPT -source +management -p tcp -dport 8006 # WebUI
IN ACCEPT -source +monitoring -p tcp -dport 9100 # Prometheus
IN ACCEPT -p icmp # Ping

[group webservers]
IN ACCEPT -p tcp -dport 80 # HTTP
IN ACCEPT -p tcp -dport 443 # HTTPS
```

### /etc/pve/firewall/{vmid}.fw
```ini
[OPTIONS]
enable: 1
policy_in: DROP
policy_out: ACCEPT
macfilter: 1
ipfilter: 1

[RULES]
GROUP webservers
IN ACCEPT -source 10.0.0.0/24 -p tcp -dport 22
```

## Macros Prédéfinies

### Utiliser une macro
```bash
# Macro SSH
pvesh create /cluster/firewall/rules \
  --action ACCEPT \
  --type in \
  --macro SSH \
  --source 10.0.0.0/24

# Macro Web
pvesh create /cluster/firewall/rules \
  --action ACCEPT \
  --type in \
  --macro Web
```

### Macros disponibles
| Macro | Ports |
|-------|-------|
| `SSH` | TCP 22 |
| `Web` | TCP 80,443 |
| `DNS` | TCP/UDP 53 |
| `HTTPS` | TCP 443 |
| `HTTP` | TCP 80 |
| `NFS` | TCP/UDP 111,2049 |
| `SMB` | TCP 139,445 |
| `RDP` | TCP 3389 |
| `Ping` | ICMP |

## Diagnostics

### Debug firewall
```bash
# Voir règles iptables générées
iptables -L -n -v
iptables -t nat -L -n -v

# Logs firewall
journalctl -u pve-firewall -f

# Tester règle
pve-firewall simulate --from 10.0.0.1 --to 192.168.1.100 --dport 22 --proto tcp

# Compiler sans appliquer
pve-firewall compile
```

### Logs
```bash
# Activer logging
pvesh set /cluster/firewall/options --log_level_in info

# Voir logs
dmesg | grep -i pve-fw
tail -f /var/log/pve-firewall.log
```

## Best Practices 2025-2026

1. **Policy DROP par défaut**: Toujours pour production
2. **Security Groups**: Réutiliser pour consistance
3. **Alias**: Nommer les réseaux pour clarté
4. **MAC/IP filter**: Activer sur VMs publiques
5. **Logging**: Activer pour troubleshooting
6. **Cluster sync**: Les règles se propagent automatiquement

## Ports Proxmox à Autoriser

| Service | Port | Protocol |
|---------|------|----------|
| Web UI/API | 8006 | TCP |
| VNC Console | 5900-5999 | TCP |
| SPICE Console | 3128 | TCP |
| SSH | 22 | TCP |
| Corosync | 5405-5412 | UDP |
| Live Migration | 60000-60050 | TCP |
| Ceph MON | 6789 | TCP |
| Ceph OSD | 6800-7300 | TCP |
