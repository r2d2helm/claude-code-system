# Wizard: Supabase Setup

Installation et configuration initiale de Supabase self-hosted.

## Questions

1. **VM cible** : Ou installer ? (VM 103 recommande)
2. **PostgreSQL** : Utiliser le PostgreSQL integre ou externe (VM 104) ?
3. **Studio** : Activer le dashboard web ?
4. **Storage** : Besoin de stockage fichiers ?

## Processus

### Etape 1 : Preparer la VM

```bash
ssh root@192.168.1.163 "mkdir -p /opt/supabase && cd /opt/supabase"
```

### Etape 2 : Telecharger la config

```bash
ssh root@192.168.1.163 "cd /opt/supabase && \
  curl -sL https://raw.githubusercontent.com/supabase/supabase/master/docker/docker-compose.yml -o docker-compose.yml && \
  curl -sL https://raw.githubusercontent.com/supabase/supabase/master/docker/.env.example -o .env"
```

### Etape 3 : Configurer le .env

```bash
# Generer les secrets
JWT_SECRET=$(openssl rand -base64 32)
POSTGRES_PASSWORD=$(openssl rand -base64 24)

# Editer le .env avec les valeurs
ssh root@192.168.1.163 "nano /opt/supabase/.env"
ssh root@192.168.1.163 "chmod 600 /opt/supabase/.env"
```

### Etape 4 : Demarrer

```bash
ssh root@192.168.1.163 "cd /opt/supabase && docker compose pull && docker compose up -d"
```

### Etape 5 : Verifier

```bash
# Containers
ssh root@192.168.1.163 "docker ps --filter 'name=supabase'"

# API
curl -s http://192.168.1.163:8000/rest/v1/ -H "apikey: {ANON_KEY}"

# Studio
# http://192.168.1.163:3000
```

### Etape 6 : Securiser

- Changer les mots de passe par defaut
- Configurer les RLS policies
- Limiter l'acces reseau (ufw)
- Sauvegarder les credentials dans claude-config-backup
