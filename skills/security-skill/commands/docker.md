# Commande: /sec-docker

Securite specifique Docker : audit des configurations runtime, images, privileges, secrets, et reseaux.

## Cible : $ARGUMENTS

Accepte : `all` (toutes les VMs Docker), un nom de VM, ou un nom de container.

## Syntaxe

```
/sec-docker [cible] [--check <type>]
```

## Processus

### 1. Audit des Privileges

```bash
# Containers en mode privileged (CRITIQUE)
ssh root@<IP> 'docker ps -q | xargs docker inspect --format "{{.Name}}: privileged={{.HostConfig.Privileged}}" 2>/dev/null | grep "true"'

# Containers avec capabilities ajoutees
ssh root@<IP> 'docker ps -q | xargs docker inspect --format "{{.Name}}: capAdd={{.HostConfig.CapAdd}}" 2>/dev/null | grep -v "capAdd=\[\]"'

# Containers en mode host network
ssh root@<IP> 'docker ps -q | xargs docker inspect --format "{{.Name}}: netMode={{.HostConfig.NetworkMode}}" 2>/dev/null | grep "host"'

# Containers avec PID/IPC host
ssh root@<IP> 'docker ps -q | xargs docker inspect --format "{{.Name}}: pidMode={{.HostConfig.PidMode}} ipcMode={{.HostConfig.IpcMode}}" 2>/dev/null | grep -v "pidMode= ipcMode="'

# Containers qui tournent en root
ssh root@<IP> 'docker ps -q | xargs docker inspect --format "{{.Name}}: user={{.Config.User}}" 2>/dev/null | grep "user=$"'
```

### 2. Audit des Volumes et Montages

```bash
# Volumes montes (attention aux montages sensibles)
ssh root@<IP> 'docker ps -q | xargs docker inspect --format "{{.Name}}:{{range .Mounts}} {{.Source}}->{{.Destination}}(rw={{.RW}}){{end}}" 2>/dev/null'

# Detecter les montages dangereux
# /var/run/docker.sock = acces total au daemon Docker
# / = acces au filesystem hote
# /etc = acces aux configs systeme
ssh root@<IP> 'docker ps -q | xargs docker inspect --format "{{.Name}}:{{range .Mounts}}{{.Source}} {{end}}" 2>/dev/null | grep -E "/var/run/docker.sock|^/\s|/etc\s"'

# Docker socket permissions
ssh root@<IP> "ls -la /var/run/docker.sock"
```

### 3. Audit des Images

```bash
# Images sans tag (dangling = risque de confusion)
ssh root@<IP> "docker images --filter 'dangling=true' -q | wc -l"

# Age des images (>90 jours = rebuild recommande)
ssh root@<IP> 'docker images --format "{{.Repository}}:{{.Tag}}\t{{.CreatedSince}}" | grep -E "months|year"'

# Images avec CVE critiques (si Docker Scout disponible)
ssh root@<IP> 'docker images --format "{{.Repository}}:{{.Tag}}" | while read img; do
  echo "=== $img ==="
  docker scout cves --only-severity critical "$img" 2>/dev/null | head -5
done'

# Taille des images (optimisation)
ssh root@<IP> "docker images --format '{{.Repository}}:{{.Tag}}\t{{.Size}}' | sort -t$'\t' -k2 -h -r | head -10"
```

### 4. Audit des Reseaux

```bash
# Reseaux Docker
ssh root@<IP> "docker network ls"

# Containers sur le reseau bridge par defaut (a eviter)
ssh root@<IP> "docker network inspect bridge --format '{{range .Containers}}{{.Name}} {{end}}' 2>/dev/null"

# Isolation des reseaux (chaque stack devrait avoir son reseau)
ssh root@<IP> 'for net in $(docker network ls -q --filter "driver=bridge"); do
  name=$(docker network inspect $net --format "{{.Name}}")
  containers=$(docker network inspect $net --format "{{range .Containers}}{{.Name}} {{end}}")
  [ -n "$containers" ] && echo "$name: $containers"
done'
```

### 5. Audit des Secrets et Variables

```bash
# Variables d'environnement des containers (chercher des secrets)
ssh root@<IP> 'docker ps -q | xargs docker inspect --format "{{.Name}}:{{range .Config.Env}}{{println .}}{{end}}" 2>/dev/null | grep -iE "password|secret|key|token|api_key" | sed "s/=.*/=***REDACTED***/"'

# Docker secrets utilises
ssh root@<IP> "docker secret ls 2>/dev/null"

# Fichiers .env des stacks compose
ssh root@<IP> "find /opt -name '.env' -exec echo {} \; -exec stat -c '%a %U:%G' {} \; 2>/dev/null"
```

### 6. Audit du Daemon Docker

```bash
# Configuration du daemon
ssh root@<IP> "cat /etc/docker/daemon.json 2>/dev/null || echo 'Pas de daemon.json'"

# Verifier que Docker n'ecoute PAS sur TCP
ssh root@<IP> "ps aux | grep dockerd | grep -v grep"

# Verifier le logging driver
ssh root@<IP> "docker info --format '{{.LoggingDriver}}'"

# Verifier le storage driver
ssh root@<IP> "docker info --format '{{.Driver}}'"
```

### 7. Audit des Healthchecks

```bash
# Containers sans healthcheck
ssh root@<IP> 'docker ps --format "{{.Names}}" | while read c; do
  hc=$(docker inspect --format "{{.Config.Healthcheck}}" "$c" 2>/dev/null)
  [ "$hc" = "<nil>" ] && echo "[WARNING] $c: PAS DE HEALTHCHECK"
done'

# Status des healthchecks existants
ssh root@<IP> 'docker ps --format "{{.Names}}\t{{.Status}}" | grep -i health'
```

## Recommandations Docker Homelab

| Recommandation | Priorite | Justification |
|----------------|----------|---------------|
| Pas de `--privileged` | CRITIQUE | Equivalent a root sur l'hote |
| Non-root dans containers | HAUTE | Limiter l'impact d'une compromission |
| Reseaux isoles par stack | HAUTE | Segmentation reseau |
| Pas de docker.sock expose | HAUTE | Acces total au daemon |
| Healthchecks definis | MOYENNE | Detection de pannes |
| Images taggees (pas :latest) | MOYENNE | Reproductibilite |
| Scan CVE mensuel | MOYENNE | Detecter les vulnerabilites |
| .env en 600 | HAUTE | Proteger les secrets |

## Options

| Option | Description |
|--------|-------------|
| `--check privileges` | Audit privileges/capabilities |
| `--check images` | Audit images (age, CVE, taille) |
| `--check network` | Audit isolation reseau |
| `--check secrets` | Audit variables d'environnement |
| `--check daemon` | Audit configuration daemon |
| `--check health` | Audit healthchecks |

## Exemples

```bash
/sec-docker all                          # Audit Docker complet
/sec-docker vm103 --check privileges     # Privileges VM 103
/sec-docker vm100 --check images         # Images VM 100
/sec-docker all --check secrets          # Secrets toutes VMs
```

## Voir Aussi

- `/dk-security` - Scan CVE detaille par image
- `/dk-ps` - Lister les containers
- `/sec-scan` - Scan vulnerabilites global
