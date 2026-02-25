# Commande: /supa-auth

Gerer l'authentification Supabase (GoTrue).

## Syntaxe

```
/supa-auth [action] [options]
```

## Utilisateurs

```bash
# Lister les users
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c \"SELECT id, email, created_at, last_sign_in_at, role FROM auth.users ORDER BY created_at DESC;\""

# Creer un user
curl -s http://192.168.1.163:8000/auth/v1/admin/users \
  -H "Authorization: Bearer {SERVICE_ROLE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"email": "{email}", "password": "{password}", "email_confirm": true}'

# Supprimer un user
curl -s -X DELETE http://192.168.1.163:8000/auth/v1/admin/users/{user_id} \
  -H "Authorization: Bearer {SERVICE_ROLE_KEY}"

# Nombre d'users
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c 'SELECT count(*) FROM auth.users;'"
```

## Providers

```bash
# Voir les providers configures
ssh root@192.168.1.163 "docker exec supabase-auth env | grep -i 'GOTRUE_EXTERNAL'"
```

## Sessions

```bash
# Sessions actives
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c \"SELECT user_id, created_at, updated_at FROM auth.sessions ORDER BY updated_at DESC LIMIT 10;\""

# Revoquer les sessions d'un user
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c \"DELETE FROM auth.sessions WHERE user_id = '{user_id}';\""
```

## Logs Auth

```bash
ssh root@192.168.1.163 "docker logs supabase-auth --tail 30"
```
