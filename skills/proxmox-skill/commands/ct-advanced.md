> Partie avancée de [[ct]]. Commandes essentielles dans le fichier principal.

# /pve-ct - Configuration Avancée, Wizard et Docker

## Description
Configuration avancée des conteneurs LXC, wizard interactif et setup Docker-in-LXC.

### Configuration Avancée

```bash
# Modifier ressources
pct set 1000 --cores 4 --memory 4096

# Ajouter mount point
pct set 1000 --mp1 /mnt/data,mp=/data,backup=0

# Ajouter disque
pct set 1000 --rootfs local-zfs:50

# Redimensionner rootfs
pct resize 1000 rootfs +10G

# Modifier réseau
pct set 1000 --net0 name=eth0,bridge=vmbr0,ip=10.0.0.101/24,gw=10.0.0.1

# Features avancées
pct set 1000 --features nesting=1,keyctl=1,fuse=1

# Limites I/O
pct set 1000 --cpulimit 2 --cpuunits 1024

# Protection contre suppression
pct set 1000 --protection 1
```

## Wizard Interactif : Création CT

```
/pve-ct create --wizard
```

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  🧙 WIZARD: CRÉATION CONTENEUR LXC                                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Étape 1/7: INFORMATIONS GÉNÉRALES                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  CTID [auto]:        > 1000                                                  ║
║  Hostname:           > web-container                                         ║
║  Node [pve01]:       > pve01                                                 ║
║  Password:           > ********                                              ║
║  SSH Public Key:     > ~/.ssh/id_rsa.pub                                     ║
║                                                                              ║
║  Étape 2/7: TYPE DE CONTENEUR                                               ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Source:                                                                     ║
║    [1] Template LXC standard   ← Recommandé                                  ║
║    [2] Image OCI (Docker Hub)  ← PVE 9.1+ Tech Preview                       ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Template:                                                                   ║
║    [1] debian-12-standard      ← Stable, léger                               ║
║    [2] ubuntu-24.04-standard   ← Populaire                                   ║
║    [3] alpine-3.20             ← Ultra-léger (5MB)                           ║
║    [4] rockylinux-9            ← RHEL compatible                             ║
║  Choix:              > 2                                                     ║
║                                                                              ║
║  Étape 3/7: RESSOURCES                                                       ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Cores [2]:          > 2                                                     ║
║  RAM (MB) [2048]:    > 2048                                                  ║
║  Swap (MB) [512]:    > 512                                                   ║
║                                                                              ║
║  Étape 4/7: STOCKAGE                                                         ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Storage:                                                                    ║
║    [1] local-zfs (ZFS, 2.1TB free)                                           ║
║    [2] ceph-pool (RBD, 25TB free)                                            ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Taille rootfs (GB) [20]: > 20                                               ║
║                                                                              ║
║  Mount points additionnels?                                                  ║
║    [1] Non                                                                   ║
║    [2] Oui, ajouter                                                          ║
║  Choix:              > 1                                                     ║
║                                                                              ║
║  Étape 5/7: RÉSEAU                                                           ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Bridge [vmbr0]:     > vmbr0                                                 ║
║  IP:                                                                         ║
║    [1] DHCP                                                                  ║
║    [2] Statique                                                              ║
║  Choix:              > 2                                                     ║
║  IP Address:         > 10.0.0.100/24                                         ║
║  Gateway:            > 10.0.0.1                                              ║
║  DNS Server:         > 10.0.0.1                                              ║
║  Firewall:           [Y/n] > Y                                               ║
║                                                                              ║
║  Étape 6/7: FEATURES                                                         ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Unprivileged:       [Y/n] > Y    ← Toujours recommandé                      ║
║                                                                              ║
║  Utilisation prévue:                                                         ║
║    [1] Services standard (web, db, etc.)                                     ║
║    [2] Docker host                                                           ║
║    [3] Kubernetes node                                                       ║
║    [4] Development                                                           ║
║  Choix:              > 2                                                     ║
║                                                                              ║
║  ➜ Features Docker activées: nesting=1, keyctl=1                             ║
║                                                                              ║
║  Étape 7/7: OPTIONS                                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  Start at boot:      [Y/n] > Y                                               ║
║  Start after create: [y/N] > Y                                               ║
║  Protection:         [y/N] > N                                               ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  📋 RÉSUMÉ CONFIGURATION                                                     ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  CTID: 1000          Hostname: web-container       Node: pve01               ║
║  Template: ubuntu-24.04-standard                                             ║
║  CPU: 2 cores        RAM: 2048 MB                  Swap: 512 MB              ║
║  Disk: 20GB local-zfs                              Features: nesting,keyctl  ║
║  Network: 10.0.0.100/24 via vmbr0                  Firewall: enabled         ║
║                                                                              ║
║  Confirmer création? [Y/n] > Y                                               ║
║                                                                              ║
║  ✅ CT 1000 créé avec succès!                                                ║
║  ✅ CT 1000 démarré                                                          ║
║  💡 Console: pct enter 1000                                                  ║
║  💡 Pour Docker: apt update && curl -fsSL https://get.docker.com | sh        ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Configuration Docker dans CT

```bash
# Script post-création pour Docker
pct exec 1002 -- bash -c '
# Mettre à jour système
apt update && apt upgrade -y

# Installer prérequis
apt install -y curl ca-certificates gnupg

# Installer Docker
curl -fsSL https://get.docker.com | sh

# Ajouter utilisateur au groupe docker (si non root)
# usermod -aG docker $USER

# Activer Docker au démarrage
systemctl enable docker

# Vérifier installation
docker --version
docker run hello-world
'
```
