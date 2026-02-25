# Commande: /supa-storage

Gerer le stockage Supabase (S3-compatible).

## Syntaxe

```
/supa-storage [action] [options]
```

## Buckets

```bash
# Lister les buckets
curl -s http://192.168.1.163:8000/storage/v1/bucket \
  -H "Authorization: Bearer {SERVICE_ROLE_KEY}" | python3 -m json.tool

# Creer un bucket
curl -s -X POST http://192.168.1.163:8000/storage/v1/bucket \
  -H "Authorization: Bearer {SERVICE_ROLE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name": "{bucket}", "public": false, "file_size_limit": 52428800}'

# Supprimer un bucket (doit etre vide)
curl -s -X DELETE http://192.168.1.163:8000/storage/v1/bucket/{bucket} \
  -H "Authorization: Bearer {SERVICE_ROLE_KEY}"
```

## Fichiers

```bash
# Lister les fichiers d'un bucket
curl -s http://192.168.1.163:8000/storage/v1/object/list/{bucket} \
  -H "Authorization: Bearer {SERVICE_ROLE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"prefix": "", "limit": 100}' | python3 -m json.tool

# Uploader un fichier
curl -s -X POST http://192.168.1.163:8000/storage/v1/object/{bucket}/{path} \
  -H "Authorization: Bearer {SERVICE_ROLE_KEY}" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @{local_file}

# Telecharger un fichier
curl -s http://192.168.1.163:8000/storage/v1/object/{bucket}/{path} \
  -H "Authorization: Bearer {SERVICE_ROLE_KEY}" -o {output_file}

# Supprimer un fichier
curl -s -X DELETE http://192.168.1.163:8000/storage/v1/object/{bucket}/{path} \
  -H "Authorization: Bearer {SERVICE_ROLE_KEY}"
```

## Taille du Stockage

```bash
# Espace utilise
ssh root@192.168.1.163 "du -sh /opt/supabase/volumes/storage/"

# Par bucket (dans PostgreSQL)
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c \"SELECT bucket_id, count(*), pg_size_pretty(sum(metadata->>'size')::bigint) FROM storage.objects GROUP BY bucket_id;\""
```
