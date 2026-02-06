# Wizard: Docker Host Setup

Assistant de configuration d'un serveur Linux comme hote Docker.

## Questions

1. **Distribution** : Ubuntu 24.04, Debian 12, Rocky 9
2. **Docker Compose** : Oui (recommande)
3. **Registry prive** : Oui/Non
4. **Monitoring** : Portainer, ctop, aucun
5. **Log driver** : json-file (default), journald
6. **Reverse proxy** : Traefik, Nginx Proxy Manager, aucun

## Installation

```bash
# Prerequis
sudo apt update
sudo apt install -y ca-certificates curl gnupg

# Docker repo
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list

# Installer Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Utilisateur
sudo usermod -aG docker deploy

# Daemon config
sudo tee /etc/docker/daemon.json << 'EOF'
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "default-address-pools": [
    {"base": "172.17.0.0/12", "size": 24}
  ],
  "live-restore": true,
  "userland-proxy": false
}
EOF
sudo systemctl restart docker
```

## Portainer (optionnel)

```bash
docker volume create portainer_data
docker run -d -p 9443:9443 --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

## Traefik (optionnel)

```bash
mkdir -p /opt/traefik
# Creer docker-compose.yml avec /dk-wizard compose
```

## Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 9443/tcp    # Portainer (si utilise)
sudo ufw enable
```
