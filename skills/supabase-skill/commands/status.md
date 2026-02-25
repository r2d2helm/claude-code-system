# Commande: /supa-status

Status complet de la stack Supabase (VM 103).

## Syntaxe

```
/supa-status
```

## Dashboard

```bash
echo "============================================"
echo "  SUPABASE STATUS - $(date +%Y-%m-%d_%H:%M)"
echo "============================================"

# Containers
echo ""
echo "--- Containers ---"
ssh root@192.168.1.163 "docker ps --filter 'name=supabase' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"

# Health checks
echo ""
echo "--- Health ---"
curl -sf http://192.168.1.163:8000/rest/v1/ > /dev/null 2>&1 && echo "REST API: OK" || echo "REST API: DOWN"
curl -sf http://192.168.1.163:8000/auth/v1/health > /dev/null 2>&1 && echo "Auth: OK" || echo "Auth: DOWN"

# DB
echo ""
echo "--- Database ---"
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c \"SELECT count(*) as tables FROM pg_tables WHERE schemaname = 'public';\""

# Storage
echo ""
echo "--- Storage ---"
ssh root@192.168.1.163 "du -sh /opt/supabase/volumes/storage/ 2>/dev/null || echo 'N/A'"

# Disk
echo ""
echo "--- Disk ---"
ssh root@192.168.1.163 "df -h / | tail -1"
```
