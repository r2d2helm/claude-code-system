# Commande: /devops-infra

Vue d'ensemble de l'infrastructure (VMs, services, sante).

## Syntaxe

```
/devops-infra [action]
```

## Dashboard Infrastructure

```bash
echo "============================================"
echo "  INFRASTRUCTURE STATUS"
echo "  $(date +%Y-%m-%d_%H:%M)"
echo "============================================"

# Proxmox Host
echo ""
echo "--- Proxmox Host (192.168.1.215) ---"
ssh -o ConnectTimeout=3 root@192.168.1.215 "qm list" 2>/dev/null || echo "UNREACHABLE"

# VMs
for entry in "root@192.168.1.162:VM100-stage" "root@192.168.1.163:VM103-main" "r2d2helm@192.168.1.164:VM104-store" "r2d2helm@192.168.1.161:VM105-lab"; do
  SSH="${entry%%:*}"
  NAME="${entry##*:}"
  echo ""
  echo "--- $NAME ---"
  ssh -o ConnectTimeout=3 $SSH "uptime && df -h / | tail -1 && docker ps --format '{{.Names}}: {{.Status}}' 2>/dev/null | head -10" 2>/dev/null || echo "UNREACHABLE"
done
```

## Inventaire Rapide

```bash
# Compter les containers par VM
for IP in 192.168.1.162 192.168.1.163 192.168.1.164 192.168.1.161; do
  COUNT=$(ssh -o ConnectTimeout=3 root@$IP "docker ps -q | wc -l" 2>/dev/null || echo "?")
  echo "$IP: $COUNT containers"
done
```

## Verifications

```bash
# Espace disque critique (> 80%)
ssh root@{IP} "df -h / | awk 'NR==2 {if (int(\$5) > 80) print \"WARNING: \" \$5 \" used\"; else print \"OK: \" \$5}'"

# Memoire
ssh root@{IP} "free -h | awk 'NR==2 {print \"RAM: \" \$3 \"/\" \$2}'"

# Load average
ssh root@{IP} "uptime | awk -F'load average:' '{print \"Load:\" \$2}'"
```
