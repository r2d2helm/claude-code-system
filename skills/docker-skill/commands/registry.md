# Commande: /dk-registry

Operations sur les registries Docker (login, push, pull, tag).

## Syntaxe

```
/dk-registry [action] [options]
```

## Actions

### Authentification

```bash
# Login sur Docker Hub
docker login

# Login sur un registry prive
docker login registry.example.com

# Login avec credentials (CI/CD)
echo $TOKEN | docker login -u username --password-stdin registry.example.com

# Logout
docker logout registry.example.com
```

### Tagging et Push

```bash
# Tagger une image pour un registry
docker tag myapp:latest registry.example.com/myapp:1.0.0

# Pousser une image
docker push registry.example.com/myapp:1.0.0

# Pousser toutes les versions d'une image
docker push --all-tags registry.example.com/myapp
```

### Pull et inspection

```bash
# Tirer une image
docker pull registry.example.com/myapp:1.0.0

# Inspecter le manifest distant (sans pull)
docker manifest inspect registry.example.com/myapp:1.0.0

# Lister les tags disponibles (Docker Hub API)
curl -s "https://hub.docker.com/v2/repositories/library/nginx/tags?page_size=20" | python -m json.tool
```

### Registry local

```bash
# Lancer un registry local
docker run -d -p 5000:5000 --name registry --restart always registry:2

# Pousser vers le registry local
docker tag myapp:latest localhost:5000/myapp:latest
docker push localhost:5000/myapp:latest

# Lister les images du registry local
curl -s http://localhost:5000/v2/_catalog
curl -s http://localhost:5000/v2/myapp/tags/list
```

## Options

| Option | Description |
|--------|-------------|
| `login` | Authentification sur un registry |
| `push` | Pousser une image |
| `pull` | Tirer une image |
| `tag` | Tagger une image |
| `local` | Operations registry local |

## Exemples

```bash
/dk-registry login ghcr.io          # Login GitHub Container Registry
/dk-registry push myapp:1.0         # Push vers registry par defaut
/dk-registry local setup             # Lancer un registry local
```

## Voir Aussi

- `/dk-images` - Gestion des images locales
- `/dk-build` - Build d'images
