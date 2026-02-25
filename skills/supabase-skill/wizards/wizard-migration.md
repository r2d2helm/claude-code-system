# Wizard: Migration Creation

Creation guidee d'une migration Supabase.

## Questions

1. **Type** : Creer table, modifier table, ajouter index, RLS policy ?
2. **Table** : Nom de la table cible ?
3. **Colonnes** : Quelles colonnes (nom, type, contraintes) ?
4. **RLS** : Quelles regles d'acces ?

## Templates

### Nouvelle Table

```sql
-- Migration: create_{table}
-- Date: {YYYY-MM-DD}

CREATE TABLE IF NOT EXISTS public.{table} (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL,
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  -- colonnes metier
  name text NOT NULL,
  description text
);

-- Index
CREATE INDEX IF NOT EXISTS idx_{table}_user_id ON public.{table}(user_id);

-- RLS
ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own data" ON public.{table}
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own data" ON public.{table}
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own data" ON public.{table}
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own data" ON public.{table}
  FOR DELETE USING (auth.uid() = user_id);

-- Trigger updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON public.{table}
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Ajouter une Colonne

```sql
-- Migration: add_{column}_to_{table}
ALTER TABLE public.{table}
  ADD COLUMN IF NOT EXISTS {column} {type} {constraints};
```

### Ajouter un Index

```sql
-- Migration: add_index_{table}_{column}
CREATE INDEX IF NOT EXISTS idx_{table}_{column}
  ON public.{table}({column});
```

## Processus

1. Choisir le template
2. Adapter les noms et types
3. Sauvegarder dans `/opt/supabase/migrations/`
4. Tester : `/supa-migration apply`
5. Verifier : `/supa-db`
