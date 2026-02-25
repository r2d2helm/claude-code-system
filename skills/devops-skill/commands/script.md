# Commande: /devops-script

Generer des scripts d'automatisation.

## Syntaxe

```
/devops-script [type] [options]
```

## Templates

### Script Bash Standard

```bash
#!/bin/bash
set -euo pipefail

# Description: {description}
# Usage: {script}.sh [args]

LOG="/var/log/{script}.log"
DATE=$(date +%Y-%m-%d_%H:%M:%S)

log() { echo "[$DATE] $1" | tee -a "$LOG"; }

log "Starting {script}..."

# --- Logic here ---

log "Done."
```

### Script de Deploy

```bash
#!/bin/bash
set -euo pipefail

SERVICE=${1:?"Usage: deploy.sh <service>"}
COMPOSE_DIR="/opt/$SERVICE"

echo "=== Deploying $SERVICE ==="

cd "$COMPOSE_DIR"
docker compose pull
docker compose up -d --remove-orphans

sleep 5
docker compose ps
echo "=== Deploy complete ==="
```

### Script de Health Check

```bash
#!/bin/bash
# Health check avec notification ntfy

SERVICES=(
  "Beszel|http://192.168.1.162:8091"
  "Uptime Kuma|http://192.168.1.162:3003"
  "Netdata|http://192.168.1.162:19999"
  "Taskyn|http://192.168.1.163:8020"
)

for entry in "${SERVICES[@]}"; do
  NAME="${entry%%|*}"
  URL="${entry##*|}"
  if ! curl -sf --max-time 5 "$URL" > /dev/null 2>&1; then
    echo "$(date) - $NAME DOWN at $URL"
    curl -s -d "$NAME is DOWN" http://192.168.1.162:8084/alerts
  fi
done
```

## Conventions

- Shebang `#!/bin/bash` + `set -euo pipefail`
- Logs dans `/var/log/`
- Variables en MAJUSCULES pour les constantes
- Fonctions pour la logique reutilisable
- Exit codes : 0 succes, 1 erreur
