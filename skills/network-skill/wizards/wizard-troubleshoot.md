# Wizard: Network Troubleshooting

Diagnostic reseau guide pas a pas pour identifier et resoudre les problemes de connectivite.

## Questions

1. **Symptome** : Quel est le probleme ? (pas de connexion, lent, port inaccessible, DNS)
2. **Source** : Depuis quelle machine ? (PC Windows, VM specifique)
3. **Destination** : Vers quelle machine/service ?
4. **Depuis quand** : Le probleme est-il nouveau ou intermittent ?

## Arbre de Diagnostic

### Niveau 1 : Connectivite de base

```bash
# Depuis Windows
ping 192.168.1.1          # Gateway
ping 192.168.1.215        # Proxmox host
ping 8.8.8.8              # Internet

# Depuis Linux
ping -c 3 192.168.1.1
ping -c 3 192.168.1.215
ping -c 3 8.8.8.8
```

**Si gateway KO** → Probleme reseau local (cable, switch, WiFi)
**Si gateway OK mais Proxmox KO** → Probleme bridge ou VM
**Si tout OK mais Internet KO** → Probleme DNS ou routeur

### Niveau 2 : Resolution DNS

```bash
# Windows
Resolve-DnsName google.com
nslookup google.com

# Linux
dig google.com
dig @8.8.8.8 google.com
cat /etc/resolv.conf
```

**Si DNS externe OK mais local KO** → Verifier /etc/hosts ou DNS local
**Si tout DNS KO** → Verifier resolv.conf, serveur DNS

### Niveau 3 : Port specifique

```bash
# Windows
Test-NetConnection -ComputerName 192.168.1.162 -Port 8091

# Linux
ss -tlnp | grep :{PORT}       # Service ecoute ?
nc -zv {IP} {PORT}            # Port accessible ?
curl -s http://{IP}:{PORT}/   # Service repond ?
```

**Si service n'ecoute pas** → Container arrete, service crash
**Si service ecoute mais pas accessible** → Firewall (ufw, iptables, Docker)
**Si accessible localement mais pas a distance** → Firewall ou binding 127.0.0.1

### Niveau 4 : Firewall

```bash
# Linux
ufw status
iptables -L -n
iptables -L -n -t nat       # Docker NAT rules

# Windows
Get-NetFirewallRule | Where-Object { $_.Enabled -eq 'True' -and $_.Direction -eq 'Inbound' } | Select-Object DisplayName, LocalPort

# Docker specifique (bypass ufw!)
docker port {container}
docker inspect {container} --format '{{range $p, $conf := .NetworkSettings.Ports}}{{$p}} -> {{$conf}}{{end}}'
```

### Niveau 5 : Performance

```bash
# Latence
mtr {destination}

# Bandwidth
iperf3 -s                    # Sur le serveur
iperf3 -c {server_ip}       # Depuis le client

# Connexions actives
ss -s                        # Resume
ss -tnp                      # Connexions TCP
```

## Problemes Frequents Homelab

| Probleme | Cause probable | Solution |
|----------|---------------|----------|
| VM inaccessible | VM arretee | `qm start {vmid}` |
| Port refuse | Firewall ufw | `ufw allow {port}` |
| Docker port KO | Container arrete | `docker start {name}` |
| DNS lent | resolv.conf mal configure | Ajouter `nameserver 8.8.8.8` |
| SSH timeout | fail2ban ban | `fail2ban-client set sshd unbanip {IP}` |
| Ping OK mais HTTP KO | Service crash | Verifier logs container |
