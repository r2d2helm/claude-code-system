# Commande: /supa-logs

Logs de tous les services Supabase.

## Syntaxe

```
/supa-logs [service] [options]
```

## Par Service

```bash
# Tous les services
ssh root@192.168.1.163 "docker compose -f /opt/supabase/docker-compose.yml logs --tail 20"

# Service specifique
ssh root@192.168.1.163 "docker logs supabase-db --tail 30"
ssh root@192.168.1.163 "docker logs supabase-auth --tail 30"
ssh root@192.168.1.163 "docker logs supabase-rest --tail 30"
ssh root@192.168.1.163 "docker logs supabase-kong --tail 30"
ssh root@192.168.1.163 "docker logs supabase-realtime --tail 30"
ssh root@192.168.1.163 "docker logs supabase-storage --tail 30"
ssh root@192.168.1.163 "docker logs supabase-studio --tail 30"

# Suivre en temps reel
ssh root@192.168.1.163 "docker logs -f supabase-{service} --tail 10"

# Filtrer les erreurs
ssh root@192.168.1.163 "docker logs supabase-{service} 2>&1 | grep -i 'error\|fatal\|panic' | tail -20"
```

## Logs PostgreSQL

```bash
# Requetes lentes
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c \"SELECT pid, now() - pg_stat_activity.query_start AS duration, query FROM pg_stat_activity WHERE (now() - pg_stat_activity.query_start) > interval '5 seconds' AND state != 'idle';\""
```

## Dozzle (UI)

Pour une vue web des logs : `http://192.168.1.163:8082` (si Dozzle installe sur VM 103).
