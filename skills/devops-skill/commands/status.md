# Commande: /devops-status

Statut des deploiements et services sur l'infrastructure.

## Syntaxe

```
/devops-status [vm|all]
```

## Dashboard Complet

```bash
echo "============================================"
echo "  DEVOPS STATUS - $(date +%Y-%m-%d_%H:%M)"
echo "============================================"

for VM in "root@192.168.1.162" "root@192.168.1.163" "r2d2helm@192.168.1.164" "r2d2helm@192.168.1.161"; do
  IP=$(echo $VM | cut -d@ -f2)
  echo ""
  echo "--- $IP ---"
  ssh -o ConnectTimeout=3 $VM "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'" 2>/dev/null || echo "UNREACHABLE"
done
```

## Status par VM

```bash
# VM specifique
ssh root@{IP} "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"

# Avec utilisation ressources
ssh root@{IP} "docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'"

# Espace disque
ssh root@{IP} "df -h / && docker system df"
```

## Checks Rapides

```bash
# Services critiques - health check
curl -sf http://192.168.1.162:8091 > /dev/null && echo "Beszel: OK" || echo "Beszel: DOWN"
curl -sf http://192.168.1.162:3003 > /dev/null && echo "Uptime Kuma: OK" || echo "Uptime Kuma: DOWN"
curl -sf http://192.168.1.163:8020 > /dev/null && echo "Taskyn: OK" || echo "Taskyn: DOWN"
curl -sf http://192.168.1.162:19999 > /dev/null && echo "Netdata: OK" || echo "Netdata: DOWN"
```
