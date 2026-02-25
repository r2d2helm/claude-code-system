# Commande: /supa-rls

Gerer les Row Level Security policies Supabase.

## Syntaxe

```
/supa-rls [action] [table]
```

## Voir les Policies

```bash
# Toutes les policies
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c \"SELECT tablename, policyname, cmd, qual FROM pg_policies WHERE schemaname = 'public';\""

# Pour une table specifique
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c \"SELECT * FROM pg_policies WHERE tablename = '{table}';\""

# Tables sans RLS
ssh root@192.168.1.163 "docker exec supabase-db psql -U supabase_admin -d postgres -c \"SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename NOT IN (SELECT tablename FROM pg_policies WHERE schemaname = 'public') ORDER BY tablename;\""
```

## Creer des Policies

```sql
-- Activer RLS sur la table
ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY;

-- Lecture pour les users authentifies
CREATE POLICY "Authenticated read" ON public.{table}
  FOR SELECT USING (auth.role() = 'authenticated');

-- Ecriture par le proprietaire
CREATE POLICY "Owner insert" ON public.{table}
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Owner update" ON public.{table}
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Owner delete" ON public.{table}
  FOR DELETE USING (auth.uid() = user_id);

-- Acces public (anon)
CREATE POLICY "Public read" ON public.{table}
  FOR SELECT USING (true);

-- Admin full access
CREATE POLICY "Admin all" ON public.{table}
  USING (auth.jwt() ->> 'role' = 'admin');
```

## Supprimer

```sql
DROP POLICY IF EXISTS "{policy_name}" ON public.{table};
```

## Patterns Courants

| Pattern | Usage |
|---------|-------|
| `auth.uid() = user_id` | Proprietaire uniquement |
| `auth.role() = 'authenticated'` | Tous les users connectes |
| `true` | Acces public |
| `auth.jwt() ->> 'role' = 'admin'` | Admin via JWT custom claim |
