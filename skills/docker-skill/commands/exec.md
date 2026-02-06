# Commande: /dk-exec

Executer des commandes dans un container.

## Syntaxe

```
/dk-exec [container] [command]
```

## Actions

```bash
# Shell interactif
docker exec -it <container> /bin/bash
docker exec -it <container> /bin/sh

# Executer une commande
docker exec <container> ls -la /app

# En tant que root
docker exec -u root <container> apt update

# Copier fichier vers container
docker cp localfile.txt <container>:/path/

# Copier fichier depuis container
docker cp <container>:/path/file.txt ./
```

## Options

| Option | Description |
|--------|-------------|
| `-it` | Mode interactif + terminal |
| `-u user` | Executer en tant que user |
| `-w dir` | Repertoire de travail |
| `-e VAR=val` | Variable d'environnement |

## Exemples

```bash
/dk-exec myapp bash              # Shell dans myapp
/dk-exec myapp cat /etc/hosts    # Lire un fichier
/dk-exec db pg_dump mydb > dump.sql  # Dump database
```
