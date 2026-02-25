# Commande: /supa-edge

Edge Functions Supabase (Deno runtime).

## Syntaxe

```
/supa-edge [action] [function]
```

## Lister les Functions

```bash
# Repertoire des functions
ssh root@192.168.1.163 "ls -la /opt/supabase/volumes/functions/"
```

## Creer une Function

```bash
# Creer le repertoire
ssh root@192.168.1.163 "mkdir -p /opt/supabase/volumes/functions/{name}"

# Creer le fichier
ssh root@192.168.1.163 "cat > /opt/supabase/volumes/functions/{name}/index.ts << 'EOF'
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'

serve(async (req) => {
  const { name } = await req.json()
  const data = { message: \`Hello \${name}!\` }

  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' },
  })
})
EOF"
```

## Deployer

```bash
# Redemarrer le container functions
ssh root@192.168.1.163 "docker restart supabase-functions"
```

## Tester

```bash
# Invoquer la function
curl -s http://192.168.1.163:8000/functions/v1/{name} \
  -H "Authorization: Bearer {ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name": "test"}'
```

## Logs

```bash
ssh root@192.168.1.163 "docker logs supabase-functions --tail 20"
```
