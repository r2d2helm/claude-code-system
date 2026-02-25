---
name: net-wizard setup
description: Configuration reseau initiale d'une VM ou serveur
---

# Wizard : Setup Reseau

Configuration reseau initiale d'une VM ou d'un serveur dans le homelab.

## Questions Prealables

1. **Machine cible** : VM Proxmox, serveur physique, ou PC Windows ?
2. **IP souhaitee** : Statique (recommande) ou DHCP ?
3. **Role** : Monitoring, Dev, Stockage, Lab, Desktop ?
4. **Services a exposer** : Quels ports ouvrir ?

## Etapes

### 1. Verifier la Connectivite de Base

```bash
# Depuis le PC Windows
ping 192.168.1.215                    # Proxmox accessible ?
ssh root@192.168.1.215                # SSH Proxmox OK ?
```

### 2. Configurer l'IP Statique (Linux VM)

```yaml
# /etc/netplan/01-netcfg.yaml (Ubuntu)
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.1.XXX/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```

```bash
# Appliquer
sudo netplan apply

# Verifier
ip addr show eth0
ping 192.168.1.1
ping 8.8.8.8
ping google.com
```

### 3. Configurer SSH

```bash
# Verifier que SSH est installe
sudo apt install openssh-server

# Verifier le service
sudo systemctl status sshd

# Copier la cle SSH depuis le PC Windows
# (depuis PowerShell sur le PC)
ssh-copy-id user@192.168.1.XXX
```

### 4. Configurer le Firewall

```bash
# Activer ufw
sudo ufw enable

# Politique par defaut
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Autoriser SSH depuis le LAN
sudo ufw allow from 192.168.1.0/24 to any port 22

# Autoriser les ports des services
# (adapter selon le role)
sudo ufw status
```

### 5. Mettre a Jour le DNS Local

Ajouter l'entree dans le fichier hosts du PC Windows :

```
# C:\Windows\System32\drivers\etc\hosts
192.168.1.XXX   hostname-vm
```

Et sur les autres VMs si necessaire :

```bash
echo "192.168.1.XXX hostname-vm" | sudo tee -a /etc/hosts
```

### 6. Configurer Docker Networking (si Docker present)

```bash
# Verifier les reseaux Docker
docker network ls

# Creer un reseau custom si necessaire
docker network create --driver bridge app-net

# Verifier que Docker ne bypass pas ufw
# Binder les ports sur l'IP locale
# ports:
#   - "192.168.1.XXX:8080:8080"
```

### 7. Installer l'Agent Monitoring

```bash
# Beszel Agent (Docker)
docker run -d \
  --name beszel-agent \
  --network host \
  --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e KEY="<cle-du-hub>" \
  -e PORT=45876 \
  henrygd/beszel-agent

# Verifier
curl -s http://localhost:45876
```

### 8. Valider la Configuration

```bash
# Depuis le PC Windows, executer :
/net-diag 192.168.1.XXX

# Verifier :
# - [ ] Ping OK
# - [ ] SSH accessible
# - [ ] DNS resolu (si fichier hosts mis a jour)
# - [ ] Ports services accessibles
# - [ ] Firewall actif avec les bonnes regles
# - [ ] Agent monitoring visible dans Beszel Hub
```

### 9. Documenter

Mettre a jour la carte reseau :

```
/net-map export
```

## Checklist Post-Setup

- [ ] IP statique configuree
- [ ] SSH accessible par cle
- [ ] Firewall actif (ufw deny incoming par defaut)
- [ ] Ports services ouverts dans le firewall
- [ ] DNS local mis a jour (fichier hosts)
- [ ] Agent monitoring deploye
- [ ] Carte reseau mise a jour
- [ ] MTU verifie (1500)
