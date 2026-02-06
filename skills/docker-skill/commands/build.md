# Commande: /dk-build

Build d'images Docker.

## Syntaxe

```
/dk-build [options]
```

## Actions

```bash
# Build simple
docker build -t <name>:<tag> .

# Build avec Dockerfile specifique
docker build -f Dockerfile.prod -t <name>:<tag> .

# Build avec args
docker build --build-arg ENV=production -t <name>:<tag> .

# Build sans cache
docker build --no-cache -t <name>:<tag> .

# Build multi-platform
docker buildx build --platform linux/amd64,linux/arm64 -t <name>:<tag> .
```

## Options

| Option | Description |
|--------|-------------|
| `-t name:tag` | Nom et tag de l'image |
| `-f Dockerfile` | Fichier Dockerfile specifique |
| `--build-arg` | Variables de build |
| `--no-cache` | Ignorer le cache |
| `--target` | Stage cible (multi-stage) |

## Exemples

```bash
/dk-build                                # Build avec Dockerfile local
/dk-build -t myapp:v2 --no-cache         # Build sans cache
/dk-build -f Dockerfile.prod -t app:prod # Dockerfile custom
```
