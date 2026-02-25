# Commande: /devops-env

Gerer les variables d'environnement et fichiers .env.

## Syntaxe

```
/devops-env [action] [service] [vm]
```

## Operations

### Lister les .env d'un service

```bash
ssh root@{IP} "cat /opt/{service}/.env 2>/dev/null || echo 'No .env found'"
```

### Comparer les environnements

```bash
# Comparer staging vs production
diff <(ssh root@192.168.1.162 "cat /opt/{service}/.env" | sort) \
     <(ssh root@192.168.1.163 "cat /opt/{service}/.env" | sort)
```

### Verifier les variables manquantes

```bash
# Comparer .env avec .env.example
ssh root@{IP} "cd /opt/{service} && diff <(grep -oP '^[A-Z_]+' .env.example | sort) <(grep -oP '^[A-Z_]+' .env | sort)"
```

### Securite

```bash
# Verifier les permissions
ssh root@{IP} "ls -la /opt/{service}/.env"

# Corriger (600 = owner only)
ssh root@{IP} "chmod 600 /opt/{service}/.env"

# Chercher des secrets potentiellement exposes
ssh root@{IP} "grep -rn 'password\|secret\|token\|api_key' /opt/{service}/.env"
```

## Convention .env

```bash
# Format standard
COMPOSE_PROJECT_NAME=myapp
APP_ENV=production        # dev|staging|production|lab
APP_PORT=8080

# Base de donnees
DB_HOST=192.168.1.164
DB_PORT=5432
DB_NAME=myapp
DB_USER=myapp
DB_PASSWORD=              # Ne jamais commit

# Services externes
API_KEY=                  # Ne jamais commit
```

## Precautions

- **Jamais** de .env dans git (ajouter dans .gitignore)
- **chmod 600** sur tous les .env
- **Template** .env.example sans valeurs sensibles dans le repo
- **Backup** des .env dans claude-config-backup (protege)
