# Commande: /sec-firewall

Gerer les regles firewall sur les machines de l'infrastructure. Vue unifiee des firewalls ufw (VMs), iptables (Proxmox), et Windows Defender Firewall.

## Cible : $ARGUMENTS

Accepte : un nom de VM, `all` pour un status global, ou `proxmox`/`windows` pour les hotes specifiques.

## Syntaxe

```
/sec-firewall [cible] [action] [options]
```

## Actions

### Status Global

```bash
# Status de toutes les machines
for vm in "root@192.168.1.162" "root@192.168.1.163" "r2d2helm@192.168.1.164" "r2d2helm@192.168.1.161"; do
  echo "=== $vm ==="
  ssh $vm "ufw status 2>/dev/null || echo 'ufw non installe'" 2>/dev/null
done

# Proxmox (iptables)
ssh root@192.168.1.215 "pve-firewall status; iptables -L -n --line-numbers | head -30"

# Windows
# powershell: Get-NetFirewallProfile | Select Name, Enabled
```

### Configurer ufw (VMs Ubuntu)

```bash
# Activer avec politique deny par defaut
ssh root@<IP> "ufw default deny incoming && ufw default allow outgoing && ufw enable"

# Regles de base homelab
ssh root@<IP> "ufw allow from 192.168.1.0/24 to any port 22 proto tcp comment 'SSH LAN'"

# Regles specifiques par VM
# VM 100 (monitoring)
ssh root@192.168.1.162 "ufw allow from 192.168.1.0/24 to any port 8091 proto tcp comment 'Beszel Hub'"
ssh root@192.168.1.162 "ufw allow from 192.168.1.0/24 to any port 3003 proto tcp comment 'Uptime Kuma'"
ssh root@192.168.1.162 "ufw allow from 192.168.1.0/24 to any port 19999 proto tcp comment 'Netdata'"
ssh root@192.168.1.162 "ufw allow from 192.168.1.0/24 to any port 8082 proto tcp comment 'Dozzle'"
ssh root@192.168.1.162 "ufw allow from 192.168.1.0/24 to any port 8084 proto tcp comment 'ntfy'"
ssh root@192.168.1.162 "ufw allow from 192.168.1.0/24 to any port 45876 proto tcp comment 'Beszel Agent'"

# VM 103 (dev principal)
ssh root@192.168.1.163 "ufw allow from 192.168.1.0/24 to any port 8020 proto tcp comment 'Taskyn API'"
ssh root@192.168.1.163 "ufw allow from 192.168.1.0/24 to any port 3020 proto tcp comment 'Taskyn Web'"

# VM 104 (stockage)
ssh r2d2helm@192.168.1.164 "sudo ufw allow from 192.168.1.0/24 to any port 5432 proto tcp comment 'PostgreSQL'"
```

### Gerer les regles

```bash
# Lister les regles numerotees
ssh root@<IP> "ufw status numbered"

# Supprimer une regle par numero
ssh root@<IP> "ufw delete <number>"

# Supprimer une regle par specification
ssh root@<IP> "ufw delete allow 8080/tcp"

# Inserer une regle a une position
ssh root@<IP> "ufw insert 1 deny from <IP_malveillante>"

# Recharger
ssh root@<IP> "ufw reload"
```

### Firewall Proxmox

```bash
# Status du firewall Proxmox
ssh root@192.168.1.215 "pve-firewall status"

# Activer
ssh root@192.168.1.215 "pve-firewall start"

# Regles via fichier de config
ssh root@192.168.1.215 "cat /etc/pve/firewall/cluster.fw"

# Ajouter une regle via pvesh
ssh root@192.168.1.215 "pvesh create /cluster/firewall/rules --type in --action ACCEPT --source 192.168.1.0/24 --dest 192.168.1.215 --dport 8006 --proto tcp --comment 'Web UI LAN'"
```

### Windows Defender Firewall

```powershell
# Status
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction

# Bloquer un port
New-NetFirewallRule -DisplayName "Block Port X" -Direction Inbound -LocalPort X -Protocol TCP -Action Block

# Autoriser un port
New-NetFirewallRule -DisplayName "Allow Beszel Agent" -Direction Inbound -LocalPort 45876 -Protocol TCP -Action Allow

# Lister les regles actives entrantes
Get-NetFirewallRule -Direction Inbound -Enabled True | Select-Object DisplayName, Action | Sort-Object DisplayName
```

## Matrice des Ports Autorises

| Machine | Port | Service | Source |
|---------|------|---------|--------|
| Toutes VMs | 22/tcp | SSH | 192.168.1.0/24 |
| VM 100 | 8091/tcp | Beszel Hub | 192.168.1.0/24 |
| VM 100 | 3003/tcp | Uptime Kuma | 192.168.1.0/24 |
| VM 100 | 19999/tcp | Netdata | 192.168.1.0/24 |
| VM 100 | 8082/tcp | Dozzle | 192.168.1.0/24 |
| VM 100 | 8084/tcp | ntfy | 192.168.1.0/24 |
| Toutes VMs | 45876/tcp | Beszel Agent | 192.168.1.0/24 |
| VM 103 | 8020/tcp | Taskyn API | 192.168.1.0/24 |
| VM 103 | 3020/tcp | Taskyn Web | 192.168.1.0/24 |
| VM 104 | 5432/tcp | PostgreSQL | 192.168.1.0/24 |
| Proxmox | 8006/tcp | Web UI | 192.168.1.0/24 |

## Options

| Option | Description |
|--------|-------------|
| `status` | Afficher les regles actuelles |
| `setup` | Appliquer les regles de base recommandees |
| `allow <port>` | Ouvrir un port |
| `deny <port>` | Fermer un port |
| `reset` | Reinitialiser le firewall (attention) |
| `--source <CIDR>` | Restreindre la source (defaut: 192.168.1.0/24) |

## Exemples

```bash
/sec-firewall all status                # Status global
/sec-firewall vm100 setup               # Regles recommandees VM 100
/sec-firewall vm103 allow 9090          # Ouvrir port 9090 VM 103
/sec-firewall proxmox status            # Regles Proxmox
/sec-firewall windows status            # Regles Windows
```

## Voir Aussi

- `/lx-firewall` - Gestion detaillee ufw/firewalld
- `/pve-firewall` - Firewall Proxmox
- `/win-security` - Securite Windows
- `/sec-audit` - Audit incluant le firewall
