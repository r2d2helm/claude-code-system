# Commande: /dk-security

Scan de securite des images et containers Docker.

## Syntaxe

```
/dk-security [action] [target] [options]
```

## Actions

### Scan d'image avec Docker Scout

```bash
# Scanner une image (vulnerabilites)
docker scout cves <image>

# Recommandations de mise a jour
docker scout recommendations <image>

# Quickview (resume)
docker scout quickview <image>

# Comparer deux versions
docker scout compare <image:old> --to <image:new>
```

### Scan avec Trivy (alternative open source)

```bash
# Scanner une image
trivy image <image>

# Scanner avec severite minimale
trivy image --severity HIGH,CRITICAL <image>

# Scanner un filesystem
trivy fs /path/to/project

# Format JSON
trivy image --format json -o results.json <image>
```

### Audit de configuration

```bash
# Verifier les permissions du socket Docker
ls -la /var/run/docker.sock

# Lister les containers en mode privileged
docker ps -q | xargs docker inspect --format '{{.Name}}: privileged={{.HostConfig.Privileged}}' 2>/dev/null

# Containers avec PID host
docker ps -q | xargs docker inspect --format '{{.Name}}: pidMode={{.HostConfig.PidMode}}' 2>/dev/null

# Verifier les capabilities
docker ps -q | xargs docker inspect --format '{{.Name}}: capAdd={{.HostConfig.CapAdd}}' 2>/dev/null

# Images sans tag (dangling)
docker images --filter "dangling=true"

# Containers sans healthcheck
docker ps --format '{{.Names}}' | while read c; do
  hc=$(docker inspect --format '{{.Config.Healthcheck}}' "$c" 2>/dev/null)
  [ "$hc" = "<nil>" ] && echo "$c: NO HEALTHCHECK"
done
```

### Best Practices Dockerfile

```bash
# Verifier un Dockerfile avec hadolint
hadolint Dockerfile

# Regles principales :
# - DL3006: Tag explicite (pas :latest)
# - DL3008: Pin les versions apt (apt-get install pkg=version)
# - DL3009: Supprimer les listes apt apres install
# - DL3025: Utiliser JSON pour CMD ["cmd", "arg"]
# - DL4006: Set SHELL pour pipefail
```

## Options

| Option | Description |
|--------|-------------|
| `scan` | Scanner une image (CVE) |
| `audit` | Auditer la configuration |
| `dockerfile` | Verifier un Dockerfile |
| `--severity` | Filtrer par severite (LOW/MEDIUM/HIGH/CRITICAL) |

## Exemples

```bash
/dk-security scan nginx:latest      # Scanner nginx
/dk-security audit                   # Auditer tous les containers
/dk-security dockerfile ./Dockerfile # Verifier un Dockerfile
```

## Voir Aussi

- `/dk-images` - Gestion des images
- `/dk-ps` - Lister les containers
