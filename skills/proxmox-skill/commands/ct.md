# /pve-ct - Gestion Conteneurs LXC

## Description
Gestion complète des conteneurs LXC sur Proxmox VE, incluant support OCI (PVE 9.1+),
templates, Docker-in-LXC, et conteneurs applicatifs.

## Syntaxe
```
/pve-ct <action> [ctid] [options]
```

## Actions Disponibles

| Action | Syntaxe | Description |
|--------|---------|-------------|
| `list` | `/pve-ct list [node]` | Lister conteneurs |
| `info` | `/pve-ct info <ctid>` | Détails conteneur |
| `create` | `/pve-ct create [--wizard]` | Créer conteneur |
| `start` | `/pve-ct start <ctid>` | Démarrer CT |
| `stop` | `/pve-ct stop <ctid>` | Arrêter CT |
| `shutdown` | `/pve-ct shutdown <ctid>` | Arrêt gracieux |
| `reboot` | `/pve-ct reboot <ctid>` | Redémarrer CT |
| `enter` | `/pve-ct enter <ctid>` | Console CT |
| `exec` | `/pve-ct exec <ctid> <cmd>` | Exécuter commande |
| `push` | `/pve-ct push <ctid> <src> <dst>` | Copier fichier vers CT |
| `pull` | `/pve-ct pull <ctid> <src> <dst>` | Copier fichier depuis CT |
| `snapshot` | `/pve-ct snapshot <ctid>` | Créer snapshot |
| `rollback` | `/pve-ct rollback <ctid> <snap>` | Restaurer snapshot |
| `clone` | `/pve-ct clone <ctid>` | Cloner CT |
| `migrate` | `/pve-ct migrate <ctid> <node>` | Migrer CT |
| `template` | `/pve-ct template <ctid>` | Convertir en template |
| `delete` | `/pve-ct delete <ctid>` | Supprimer CT |

## Options Communes

| Option | Description |
|--------|-------------|
| `--node <n>` | Spécifier le node |
| `--wizard` | Mode assistant interactif |
| `--unprivileged` | Conteneur non-privilégié (défaut) |
| `--json` | Sortie JSON |

## Affichage Liste Conteneurs

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║  📦 LXC CONTAINERS                                                               ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  ┌──────┬─────────────────────┬────────┬─────────┬────────┬──────────┬────────┐ ║
║  │ CTID │ Name                │ Node   │ Status  │ CPU    │ Memory   │ Disk   │ ║
║  ├──────┼─────────────────────┼────────┼─────────┼────────┼──────────┼────────┤ ║
║  │ 1000 │ dns-pihole          │ pve01  │ 🟢 run  │ 1c/2%  │ 512M/35% │ 8G     │ ║
║  │ 1001 │ proxy-nginx         │ pve01  │ 🟢 run  │ 2c/8%  │ 1G/42%   │ 10G    │ ║
║  │ 1002 │ docker-host-01      │ pve02  │ 🟢 run  │ 4c/25% │ 8G/68%   │ 100G   │ ║
║  │ 1003 │ monitoring-grafana  │ pve02  │ 🟢 run  │ 2c/5%  │ 2G/38%   │ 20G    │ ║
║  │ 1004 │ influxdb            │ pve03  │ 🟢 run  │ 2c/12% │ 4G/55%   │ 50G    │ ║
║  │ 1005 │ homeassistant       │ pve01  │ 🟢 run  │ 2c/3%  │ 2G/28%   │ 16G    │ ║
║  │ 1100 │ oci-nginx-app       │ pve01  │ 🟢 run  │ 1c/1%  │ 256M/15% │ 2G     │ ║
║  │ 1010 │ dev-alpine          │ pve01  │ 🟡 stop │ 1c/-   │ 256M/-   │ 4G     │ ║
║  └──────┴─────────────────────┴────────┴─────────┴────────┴──────────┴────────┘ ║
║                                                                                  ║
║  📊 Total: 8 | Running: 7 | Stopped: 1 | OCI: 1                                 ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

## Commandes Bash

### Templates LXC

```bash
# Lister templates disponibles
pveam available --section system

# Télécharger templates standards
pveam download local debian-12-standard_12.7-1_amd64.tar.zst
pveam download local ubuntu-24.04-standard_24.04-2_amd64.tar.zst
pveam download local alpine-3.20-default_20240908_amd64.tar.xz
pveam download local rockylinux-9-default_20240911_amd64.tar.xz

# Templates turnkey
pveam available --section turnkeylinux
pveam download local turnkey-wordpress_18.0-1_amd64.tar.zst

# Lister templates locaux
pveam list local

# Supprimer template
pveam remove local:vztmpl/old-template.tar.zst
```

### OCI Containers (PVE 9.1+ - Tech Preview)

```bash
# ═══════════════════════════════════════════════════════════════════════════
# OCI IMAGES - Support Docker Hub/Registries (PVE 9.1+)
# ═══════════════════════════════════════════════════════════════════════════

# Télécharger image OCI depuis Docker Hub
pveam download local docker://docker.io/library/nginx:latest
pveam download local docker://docker.io/library/redis:alpine
pveam download local docker://docker.io/library/postgres:16

# Depuis registry privé
pveam download local docker://myregistry.local/myapp:v1.0

# Créer CT depuis image OCI (Application Container)
pct create 1100 local:vztmpl/oci-nginx-latest.tar.zst \
  --hostname nginx-app \
  --cores 1 \
  --memory 256 \
  --rootfs local-zfs:2 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp

# ══ NOTES OCI ══
# - Tech preview PVE 9.1
# - Application containers = microservices légers
# - System containers = comme templates classiques
# - Images Docker converties en LXC
```

### Création Conteneur Standard

```bash
# ═══════════════════════════════════════════════════════════════════════════
# CRÉATION CT STANDARD
# ═══════════════════════════════════════════════════════════════════════════

pct create 1000 local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
  --hostname myserver \
  --cores 2 \
  --memory 2048 \
  --swap 512 \
  --rootfs local-zfs:20 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp,firewall=1 \
  --unprivileged 1 \
  --features nesting=0 \
  --onboot 1 \
  --start 0 \
  --password "SecurePassword123!" \
  --ssh-public-keys ~/.ssh/authorized_keys

# ═══════════════════════════════════════════════════════════════════════════
# CRÉATION CT DOCKER-READY
# ═══════════════════════════════════════════════════════════════════════════

pct create 1002 local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst \
  --hostname docker-host \
  --cores 4 \
  --memory 8192 \
  --swap 2048 \
  --rootfs local-zfs:100 \
  --mp0 /mnt/docker-data,mp=/var/lib/docker,backup=0 \
  --net0 name=eth0,bridge=vmbr0,ip=10.0.0.50/24,gw=10.0.0.1 \
  --nameserver "8.8.8.8 8.8.4.4" \
  --searchdomain "local.domain" \
  --unprivileged 1 \
  --features nesting=1,keyctl=1 \
  --onboot 1

# Après création, installer Docker:
pct exec 1002 -- bash -c "
  apt update && apt install -y curl
  curl -fsSL https://get.docker.com | sh
  systemctl enable docker
"

# ═══════════════════════════════════════════════════════════════════════════
# CT AVEC IP STATIQUE ET DNS
# ═══════════════════════════════════════════════════════════════════════════

pct create 1003 local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst \
  --hostname webserver \
  --cores 2 \
  --memory 2048 \
  --rootfs local-zfs:20 \
  --net0 name=eth0,bridge=vmbr0,ip=10.0.0.100/24,gw=10.0.0.1,firewall=1 \
  --nameserver "10.0.0.1" \
  --searchdomain "example.local" \
  --unprivileged 1 \
  --features nesting=1 \
  --onboot 1

# ═══════════════════════════════════════════════════════════════════════════
# BEST PRACTICES CT 2025-2026
# ═══════════════════════════════════════════════════════════════════════════
#
# unprivileged: TOUJOURS 1 (sécurité, isolation)
# nesting: 1 si Docker/LXC dans CT requis
# keyctl: 1 requis pour certaines apps Docker
# cgroup: v2 uniquement sur PVE 9+ (cgroupv1 non supporté)
# memory: prévoir swap pour éviter OOM
# rootfs: sizing suffisant, extension facile
```

### Opérations CT

```bash
# Démarrer
pct start 1000

# Arrêter (graceful)
pct shutdown 1000

# Arrêter (force)
pct stop 1000

# Redémarrer
pct reboot 1000

# Console interactive
pct enter 1000

# Exécuter commande
pct exec 1000 -- apt update
pct exec 1000 -- systemctl status nginx
pct exec 1000 -- cat /etc/os-release

# Copier fichiers
pct push 1000 /local/file /container/path
pct pull 1000 /container/path /local/file

# Mount points temporaires
pct mount 1000
ls /var/lib/lxc/1000/rootfs/
pct unmount 1000
```

### Snapshots CT

```bash
# Créer snapshot
pct snapshot 1000 pre-upgrade --description "Before upgrade"

# Lister snapshots
pct listsnapshot 1000

# Rollback
pct rollback 1000 pre-upgrade

# Supprimer snapshot
pct delsnapshot 1000 pre-upgrade
```

### Migration et Clonage

```bash
# Migration online (restart mode par défaut)
pct migrate 1000 pve02

# Migration avec restart
pct migrate 1000 pve02 --restart

# Clone complet
pct clone 1000 1001 --hostname clone-server --full

# Clone lié
pct clone 1000 1001 --hostname clone-server
```

## Voir Aussi
- `/pve-vm` - Gestion machines virtuelles
- `/pve-template` - Gestion templates
- `/pve-storage` - Gestion stockage
- `/pve-wizard ct` - Assistant création CT complet

> Voir aussi : [[ct-advanced]]
