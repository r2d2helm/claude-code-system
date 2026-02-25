# Commande: /sec-passwords

Audit des mots de passe et credentials dans l'infrastructure.

## Syntaxe

```
/sec-passwords [action] [cible]
```

## Audit des Credentials

### Fichiers sensibles exposes

```bash
# Chercher des fichiers .env sur une VM
ssh {user}@{ip} "find / -name '.env' -o -name '*.env' -o -name 'credentials*' -o -name '*secret*' 2>/dev/null | head -20"

# Verifier les permissions des .env
ssh {user}@{ip} "find / -name '.env' -exec ls -la {} \; 2>/dev/null"

# Chercher des secrets dans docker-compose
ssh {user}@{ip} "grep -r 'password\|secret\|token\|api_key' /opt/*/docker-compose*.yml 2>/dev/null"
```

### Mots de passe par defaut

```bash
# Verifier les comptes sans mot de passe (Linux)
ssh {user}@{ip} "sudo awk -F: '(\$2 == \"\" || \$2 == \"!\") {print \$1}' /etc/shadow"

# Comptes PostgreSQL
ssh r2d2helm@192.168.1.164 "psql -U postgres -h localhost -c \"SELECT usename, passwd IS NOT NULL as has_password FROM pg_shadow;\""
```

### Permissions des fichiers credentials

```bash
# Les fichiers credentials doivent etre en 600
ssh {user}@{ip} "find /opt -name '.env' -exec stat -c '%a %U %n' {} \;"

# Corriger les permissions
ssh {user}@{ip} "find /opt -name '.env' -exec chmod 600 {} \;"
```

## Fichiers Credentials Connus (r2d2)

| Fichier | Emplacement | Protection |
|---------|-------------|------------|
| vm100-credentials.md | claude-config-backup/ | path_guard hook |
| .env (containers) | /opt/*/  sur chaque VM | chmod 600 |
| SSH keys | ~/.ssh/ | chmod 600/700 |
| Beszel password | Variable env | Docker secret |

## Bonnes Pratiques

- **Jamais** de mots de passe dans le code source ou git
- **chmod 600** sur tous les fichiers contenant des secrets
- **Variables d'environnement** plutot que fichiers en clair
- **Rotation** tous les 90 jours pour les credentials critiques
- **Mots de passe uniques** par service (pas de reutilisation)
- **Longueur minimum** : 16 caracteres pour les services
