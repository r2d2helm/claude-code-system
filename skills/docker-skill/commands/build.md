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

Build simple avec tag :
```bash
docker build -t myapp:latest .
```

Build d'un stage specifique (multi-stage) :
```bash
docker build --target builder -t myapp:build .
```

Rebuild complet sans cache :
```bash
docker build --no-cache -t myapp:latest .
```

Build avec variables d'environnement :
```bash
docker build --build-arg NODE_ENV=production --build-arg VERSION=2.1.0 -t myapp:prod .
```
