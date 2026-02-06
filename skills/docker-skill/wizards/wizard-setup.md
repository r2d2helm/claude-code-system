# Wizard: Docker Setup

Assistant d'installation et configuration de Docker.

## Questions

1. **Plateforme** : Windows (Desktop), Linux (Engine), WSL2
2. **Usage** : Developpement, Production, CI/CD
3. **Compose** : Installer Docker Compose v2 ?
4. **Buildx** : Installer Docker Buildx ?

## Installation Windows (Docker Desktop)

```powershell
# Via winget
winget install Docker.DockerDesktop

# Verifier WSL2
wsl --update
wsl --set-default-version 2

# Redemarrer apres installation
```

## Installation Linux (Ubuntu/Debian)

```bash
# Prerequis
sudo apt update
sudo apt install -y ca-certificates curl gnupg

# Ajouter le repo Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list

# Installer
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER

# Verifier
docker --version
docker compose version
```

## Post-installation

```bash
# Tester
docker run hello-world

# Configurer le daemon
# /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "10m", "max-file": "3" },
  "default-address-pools": [{"base":"172.17.0.0/12","size":24}]
}

# Redemarrer
sudo systemctl restart docker
```
