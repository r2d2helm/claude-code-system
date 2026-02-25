# Wizard: Pipeline Creation

Creation guidee d'un pipeline de deploiement automatise.

## Questions

1. **Projet** : Quel projet/service ?
2. **Declencheur** : Git push, cron, manuel ?
3. **Etapes** : Build, test, deploy ? Quelles VMs ?
4. **Notifications** : ntfy, Telegram ?

## Pipeline Standard

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Build  │ →  │  Test   │ →  │ Deploy  │ →  │ Verify  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### Script Pipeline

```bash
#!/bin/bash
set -euo pipefail

SERVICE=$1
VM_IP=$2
NTFY_URL="http://192.168.1.162:8084/deploys"

notify() { curl -sf -d "$1" "$NTFY_URL" > /dev/null 2>&1 || true; }

# Build
echo "=== BUILD ==="
notify "Starting deploy of $SERVICE"
ssh root@$VM_IP "cd /opt/$SERVICE && docker compose pull"

# Pre-deploy backup
echo "=== BACKUP ==="
ssh root@$VM_IP "cd /opt/$SERVICE && docker compose exec -T db pg_dump -Fc > /tmp/pre-deploy.dump" 2>/dev/null || true

# Deploy
echo "=== DEPLOY ==="
ssh root@$VM_IP "cd /opt/$SERVICE && docker compose up -d --remove-orphans"

# Verify
echo "=== VERIFY ==="
sleep 10
if ssh root@$VM_IP "cd /opt/$SERVICE && docker compose ps | grep -q 'Up'"; then
  notify "$SERVICE deployed successfully"
  echo "SUCCESS"
else
  notify "$SERVICE deploy FAILED - rolling back"
  ssh root@$VM_IP "cd /opt/$SERVICE && docker compose down"
  echo "FAILED"
  exit 1
fi
```

## Pipeline par Type

### Service Simple (stateless)
Build → Pull → Up → Health check

### Service avec DB
Backup DB → Pull → Migrate → Up → Health check → Verify data

### Multi-VM
Deploy staging (100) → Test → Deploy prod (103) → Verify
