# Wizard: Service Deployment

Deploiement guide d'un nouveau service Docker sur le homelab.

## Questions

1. **Service** : Quel service deployer ? (nom, image Docker)
2. **VM cible** : Sur quelle VM ? (100 staging, 103 prod, 104 store, 105 lab)
3. **Ports** : Quels ports exposer ?
4. **Volumes** : Donnees persistantes ?
5. **Dependances** : Base de donnees, services lies ?

## Processus

### Etape 1 : Preparer le repertoire

```bash
ssh root@{IP} "mkdir -p /opt/{service}"
```

### Etape 2 : Creer le docker-compose.yml

```yaml
version: '3.8'
services:
  {service}:
    image: {image}:{tag}
    container_name: {service}
    restart: unless-stopped
    ports:
      - "{port}:{port}"
    volumes:
      - ./data:/data
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{port}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Etape 3 : Creer le .env

```bash
ssh root@{IP} "cat > /opt/{service}/.env << 'EOF'
# {service} configuration
APP_ENV=production
EOF"
ssh root@{IP} "chmod 600 /opt/{service}/.env"
```

### Etape 4 : Deployer

```bash
ssh root@{IP} "cd /opt/{service} && docker compose up -d"
```

### Etape 5 : Verifier et monitorer

- Ajouter dans Uptime Kuma
- Verifier les logs
- Documenter dans le vault
