# Wizard: Création de Conteneur LXC

## Mode d'emploi
Ce wizard guide la création d'un conteneur LXC optimisé pour Proxmox VE 9+, incluant les nouvelles fonctionnalités OCI (PVE 9.1).

---

## Questions Interactives

### 1. Type de Conteneur

**Q1.1: Quel type de conteneur créer?**

| Option | Type | Description |
|--------|------|-------------|
| A | System Container | OS complet (init, services) - défaut |
| B | Application Container | OCI/Docker image (PVE 9.1+) |

```
Choix: ___
```

---

### 2. Informations de Base

**Q2.1: Quel nom pour le conteneur?**
```
Nom: _______________
(ex: nginx-proxy, pihole, dev-node)
```

**Q2.2: Quel CTID? (100-999999)**
```
CTID: _____ (laisser vide pour auto)
```

**Q2.3: Sur quel node?**
```
Node: _______________
```

---

### 3a. Template OS (System Container)

**Q3a.1: Quel OS/distribution?**

| Option | Distribution | Template suggéré |
|--------|--------------|------------------|
| A | Debian 13 | debian-13-standard |
| B | Ubuntu 24.04 | ubuntu-24.04-standard |
| C | Alpine 3.20 | alpine-3.20-default |
| D | Rocky Linux 9 | rockylinux-9-default |
| E | Arch Linux | archlinux-base |

```
Choix: ___
```

**Q3a.2: Template disponible ou à télécharger?**
```bash
# Lister templates disponibles
pveam list local

# Télécharger template
pveam update
pveam download local debian-13-standard_13.0-1_amd64.tar.zst
```

---

### 3b. Image OCI (Application Container - PVE 9.1+)

**Q3b.1: Quelle image Docker Hub?**
```
Image: _______________
(ex: nginx:latest, postgres:16, redis:7-alpine)
```

**Q3b.2: Registry (défaut: docker.io)?**
```
[ ] docker.io (Docker Hub - défaut)
[ ] ghcr.io (GitHub Container Registry)
[ ] quay.io (Red Hat Quay)
[ ] Autre: _______________
```

---

### 4. Ressources Compute

**Q4.1: Combien de vCPUs?**
```
vCPUs: _____ (ex: 1, 2, 4)
```

**Q4.2: Limite CPU (cores)?**
```
[ ] Illimité (défaut)
[ ] Limité à: _____ cores
```

**Q4.3: Combien de RAM (MB)?**
```
RAM: _____ MB (ex: 512, 1024, 2048)
```

**Q4.4: SWAP (MB)?**
```
SWAP: _____ MB (ex: 512, 0 pour désactiver)
```

---

### 5. Stockage

**Q5.1: Sur quel storage le rootfs?**
```
Storage: _______________
(ex: local-zfs, local-lvm)
```

**Q5.2: Taille du rootfs (GB)?**
```
Taille: _____ GB (ex: 8, 16, 32)
```

**Q5.3: Mount points additionnels?**
```
[ ] Non
[ ] Oui - Détails:
    - mp0: Storage=_____ Size=_____ Path=_____
    - mp1: Storage=_____ Size=_____ Path=_____
```

**Q5.4: Bind mounts (dossiers hôte)?**
```
[ ] Non
[ ] Oui - Détails:
    - mp0: /host/path,mp=/container/path,ro=0
```

---

### 6. Réseau

**Q6.1: Quel bridge réseau?**
```
Bridge: _______________
(ex: vmbr0)
```

**Q6.2: Configuration IP?**
```
[ ] DHCP (défaut)
[ ] Statique - IP: ___.___.___.___/__ GW: ___.___.___.___
```

**Q6.3: VLAN tag? (optionnel)**
```
VLAN: _____ (laisser vide si aucun)
```

**Q6.4: Hostname DNS?**
```
Hostname: _______________
```

---

### 7. Sécurité & Features

**Q7.1: Conteneur privilégié ou non?**
```
[ ] Unprivileged (défaut - plus sécurisé)
[ ] Privileged (accès matériel complet)
```

**Q7.2: Activer nesting? (Docker/LXC dans LXC)**
```
[ ] Non (défaut)
[ ] Oui - nesting=1
```

**Q7.3: Activer keyctl? (requis pour Docker)**
```
[ ] Non (défaut)
[ ] Oui - keyctl=1
```

**Q7.4: FUSE mount? (pour rclone, etc.)**
```
[ ] Non (défaut)
[ ] Oui - fuse=1
```

**Q7.5: Mot de passe root?**
```
Password: _______________
(ou laisser vide pour SSH key only)
```

**Q7.6: Clé SSH publique?**
```
SSH Key: _______________
(ex: ssh-ed25519 AAAA... user@host)
```

---

### 8. Démarrage

**Q8.1: Démarrer automatiquement au boot hôte?**
```
[ ] Non (défaut)
[ ] Oui - onboot=1
```

**Q8.2: Ordre de démarrage?**
```
Order: _____ (1-100, plus petit = démarre en premier)
```

**Q8.3: Démarrer maintenant après création?**
```
[ ] Non
[ ] Oui
```

---

## Génération de Commande

### Template System Container

```bash
pct create CTID STORAGE:vztmpl/TEMPLATE.tar.zst \
  --hostname "HOSTNAME" \
  --memory RAM_MB \
  --swap SWAP_MB \
  --cores VCPUS \
  --rootfs STORAGE:SIZE_GB \
  --net0 name=eth0,bridge=BRIDGE,ip=dhcp,firewall=1 \
  --unprivileged 1 \
  --features nesting=0 \
  --password \
  --start 0
```

### Template OCI Container (PVE 9.1+)

```bash
pct create CTID STORAGE:SIZE_GB \
  --hostname "HOSTNAME" \
  --memory RAM_MB \
  --cores VCPUS \
  --ostype unmanaged \
  --net0 name=eth0,bridge=BRIDGE,ip=dhcp \
  --unprivileged 1 \
  --start 0

# Pull OCI image
pct pull CTID docker.io/library/IMAGE:TAG
```

---

## Configurations Prêtes à l'Emploi

### Serveur Web Nginx (System)

```bash
pct create 200 local:vztmpl/debian-13-standard_13.0-1_amd64.tar.zst \
  --hostname "nginx-proxy" \
  --memory 512 \
  --swap 256 \
  --cores 1 \
  --rootfs local-zfs:8 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp,firewall=1 \
  --unprivileged 1 \
  --start 1

# Post-install
pct exec 200 -- apt update && apt install -y nginx
```

### Nginx OCI (Application - PVE 9.1+)

```bash
pct create 201 local-zfs:4 \
  --hostname "nginx-oci" \
  --memory 256 \
  --cores 1 \
  --ostype unmanaged \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp \
  --unprivileged 1 \
  --start 0

# Pull et configure
pct pull 201 docker.io/library/nginx:latest
pct set 201 --mp0 /var/www/html,mp=/usr/share/nginx/html
pct start 201
```

### Docker Host (Debian + Docker)

```bash
pct create 210 local:vztmpl/debian-13-standard_13.0-1_amd64.tar.zst \
  --hostname "docker-host" \
  --memory 4096 \
  --swap 1024 \
  --cores 4 \
  --rootfs local-zfs:32 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp,firewall=1 \
  --unprivileged 1 \
  --features nesting=1,keyctl=1 \
  --start 1

# Post-install Docker
pct exec 210 -- bash -c '
  apt update && apt install -y ca-certificates curl gnupg
  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  chmod a+r /etc/apt/keyrings/docker.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo $VERSION_CODENAME) stable" > /etc/apt/sources.list.d/docker.list
  apt update && apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
'
```

### Pi-hole DNS (Alpine - Léger)

```bash
pct create 220 local:vztmpl/alpine-3.20-default_20240607_amd64.tar.xz \
  --hostname "pihole" \
  --memory 256 \
  --swap 0 \
  --cores 1 \
  --rootfs local-zfs:4 \
  --net0 name=eth0,bridge=vmbr0,ip=192.168.1.53/24,gw=192.168.1.1,firewall=1 \
  --nameserver 1.1.1.1 \
  --unprivileged 1 \
  --start 1

# Note: Installer Pi-hole via script officiel
```

### PostgreSQL Database

```bash
pct create 230 local:vztmpl/debian-13-standard_13.0-1_amd64.tar.zst \
  --hostname "postgres-db" \
  --memory 2048 \
  --swap 512 \
  --cores 2 \
  --rootfs local-zfs:16 \
  --mp0 local-zfs:50,mp=/var/lib/postgresql \
  --net0 name=eth0,bridge=vmbr0,ip=192.168.1.100/24,gw=192.168.1.1,firewall=1 \
  --unprivileged 1 \
  --start 1

# Post-install PostgreSQL
pct exec 230 -- bash -c '
  apt update && apt install -y postgresql-16
  systemctl enable postgresql
'
```

### Development Container (Ubuntu + Tools)

```bash
pct create 240 local:vztmpl/ubuntu-24.04-standard_24.04-1_amd64.tar.zst \
  --hostname "dev-box" \
  --memory 8192 \
  --swap 2048 \
  --cores 8 \
  --rootfs local-zfs:64 \
  --mp0 /home/user/projects,mp=/projects \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp,firewall=1 \
  --unprivileged 1 \
  --features nesting=1,keyctl=1 \
  --ssh-public-keys /root/.ssh/authorized_keys \
  --start 1

# Post-install dev tools
pct exec 240 -- bash -c '
  apt update && apt install -y git vim curl wget build-essential python3-pip nodejs npm
'
```

---

## Best Practices Conteneurs 2026

### Sécurité

| Paramètre | Recommandation |
|-----------|----------------|
| unprivileged | Toujours 1 sauf besoin spécifique |
| nesting | Uniquement si Docker/LXC requis |
| keyctl | Uniquement avec nesting pour Docker |
| rootfs | Séparé des données applicatives |

### Performance

| Paramètre | Recommandation |
|-----------|----------------|
| Storage | ZFS ou LVM pour rootfs |
| Mount points | Volumes séparés pour data |
| Memory | Adapter au workload, pas de sur-allocation |
| CPU | Limiter uniquement si multi-tenant |

### OCI Containers (PVE 9.1+)

- **Application containers**: Sans init system, une seule app
- **System containers**: Init complet, multiples services
- Privilégier OCI pour apps stateless simples
- System containers pour services complexes

### Docker dans LXC

```bash
# Features requises
--features nesting=1,keyctl=1

# AppArmor profile (si problèmes)
--apparmor lxc-container-default-with-nesting

# Vérifier cgroups v2
pct exec CTID -- cat /sys/fs/cgroup/cgroup.controllers
```

---

## Commande Associée

Voir `/pve-ct` pour toutes les opérations conteneurs.
