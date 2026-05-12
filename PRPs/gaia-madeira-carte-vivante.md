name: "PRP — GAIA Madeira : Carte Vivante (MVP Phase 0)"
description: |
  Web app PWA carte interactive de Madeira avec 130+ acteurs locaux geolocalises.
  Recherche en langage naturel, meteo temps reel, filtres par zone/type.
  Stack : Next.js 14 + FastAPI + Supabase + Leaflet. Deploy VM 103.
confidence: 8/10

---

## Goal

Deployer une **Progressive Web App** accessible sur mobile qui affiche une carte interactive
de Madeira avec tous les acteurs locaux (pecheurs, fermiers, artisans, restaurants, spots caches)
geolocalises. Le touriste ouvre la carte, voit ce qui est autour de lui, filtre par type/zone,
et contacte directement le local. Zero intermediaire, zero commission.

**Etat final :** `gaia.multipass.agency` accessible depuis un smartphone, carte Madeira avec
130+ marqueurs, profils riches, filtres, meteo, recherche IA, PWA installable.

## Why

- **2,2M touristes/an** perdus dans TripAdvisor — aucune plateforme locale unifiee
- **130+ acteurs identifies** par nom avec contacts — donnees pretes
- **Infrastructure existante** sur VM 103 (Supabase, Docker, domaine)
- **Gouvernement de Madere** cherche activement deconcentration et innovation digitale
- Premiere brique concrete du projet GAIA Madeira (Territoire #1)
- Prouve le concept avant Phase 1 (assistant LIVE, GAIA Pass)

## What

### Success Criteria

- [ ] Carte interactive de Madeira avec Leaflet + OSM fonctionnelle sur mobile
- [ ] 130+ acteurs charges dans Supabase avec profils complets
- [ ] Filtres par zone (Nord/Sud/Est/Ouest/Montagne) et type (12 categories)
- [ ] Geolocalisation "autour de moi" fonctionnelle
- [ ] Meteo temps reel par zone (OpenWeatherMap API)
- [ ] Recherche en langage naturel via LiteLLM/Claude
- [ ] Multilingue : FR, EN, PT (DE stretch goal)
- [ ] PWA installable, mobile-first, fonctionne offline (cache)
- [ ] Deploy sur VM 103, accessible via `gaia.multipass.agency`
- [ ] Temps de chargement < 3s sur 4G

## Contexte necessaire

### Documentation & References
```yaml
- file: C:\Users\r2d2\Documents\Projets\Marketplace-GAIA\madeira\INITIAL.md
  why: Spec complete du MVP, schema JSON des acteurs, contraintes

- file: C:\Users\r2d2\Documents\R2D2-Memory\projets\madeira-gaia.md
  why: Vision, modele economique, decisions strategiques

- file: C:\Users\r2d2\Downloads\Documents\MultiPass\multipass-backend-reference.md
  why: Patterns FastAPI, structure verticale, Pydantic models

- file: C:\Users\r2d2\Downloads\Documents\MultiPass\multipass-frontend-reference.md
  why: Patterns Next.js 14, shadcn/ui, Tailwind

- file: C:\Users\r2d2\Downloads\Documents\MultiPass\multipass-architecture.md
  why: Architecture globale, patterns reutilisables

- url: https://leafletjs.com/reference.html
  why: API Leaflet pour la carte interactive

- url: https://openweathermap.org/api
  why: API meteo gratuite (1000 calls/jour)

- url: https://nextjs.org/docs/app
  why: Next.js 14 App Router patterns
```

### Arbre souhaite (nouveau projet standalone)
```
C:\Users\r2d2\Documents\Projets\Marketplace-GAIA\madeira\
├── INITIAL.md                      # Deja cree
├── docker-compose.yml              # Orchestration locale (pour deploy VM 103)
├── backend/
│   ├── requirements.txt
│   ├── main.py                     # FastAPI app
│   ├── config.py                   # Settings (env vars)
│   ├── models/
│   │   ├── actor.py                # Modele Actor (Pydantic)
│   │   ├── spot.py                 # Modele HiddenSpot
│   │   └── weather.py              # Modele Weather
│   ├── api/
│   │   ├── router.py               # Router principal
│   │   ├── actors.py               # CRUD + search acteurs
│   │   ├── spots.py                # CRUD spots caches
│   │   ├── weather.py              # Proxy meteo
│   │   ├── search.py               # Recherche IA langage naturel
│   │   └── health.py               # Health check
│   ├── services/
│   │   ├── actor_service.py        # Logique metier acteurs
│   │   ├── weather_service.py      # Cache + proxy OpenWeatherMap
│   │   └── search_service.py       # Recherche IA via LiteLLM
│   └── seed/
│       ├── seed_actors.py          # Script de seed
│       └── data/
│           ├── fishermen.json      # Donnees peche
│           ├── farms.json          # Donnees agriculture
│           ├── artisans.json       # Donnees artisanat
│           ├── spots.json          # Tresors caches
│           ├── restaurants.json    # Restaurants locaux
│           └── markets.json        # Marches
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── public/
│   │   ├── manifest.json           # PWA manifest
│   │   ├── icons/                  # PWA icons
│   │   └── images/                 # Placeholder images acteurs
│   └── src/
│       ├── app/
│       │   ├── layout.tsx          # Root layout (multilingue)
│       │   ├── page.tsx            # Home → redirect to /map
│       │   ├── map/
│       │   │   └── page.tsx        # Page carte principale
│       │   ├── actor/
│       │   │   └── [id]/
│       │   │       └── page.tsx    # Page profil acteur
│       │   ├── search/
│       │   │   └── page.tsx        # Page recherche IA
│       │   └── api/
│       │       └── revalidate/
│       │           └── route.ts    # ISR revalidation
│       ├── components/
│       │   ├── Map.tsx             # Carte Leaflet (client component)
│       │   ├── MapMarker.tsx       # Marqueur personnalise par type
│       │   ├── ActorCard.tsx       # Card preview acteur
│       │   ├── ActorProfile.tsx    # Profil complet acteur
│       │   ├── FilterBar.tsx       # Barre de filtres zone/type
│       │   ├── SearchBar.tsx       # Recherche langage naturel
│       │   ├── WeatherWidget.tsx   # Widget meteo par zone
│       │   ├── LocateMe.tsx        # Bouton geolocalisation
│       │   ├── LanguageSwitcher.tsx # FR/EN/PT
│       │   └── ui/                 # shadcn/ui components
│       ├── lib/
│       │   ├── api.ts              # Client API backend
│       │   ├── supabase.ts         # Client Supabase
│       │   ├── i18n.ts             # Config i18n
│       │   └── constants.ts        # Types de categories, zones, etc.
│       ├── hooks/
│       │   ├── useGeolocation.ts   # Hook GPS
│       │   ├── useActors.ts        # Hook fetch acteurs
│       │   └── useWeather.ts       # Hook meteo
│       └── locales/
│           ├── fr.json             # Traductions FR
│           ├── en.json             # Traductions EN
│           └── pt.json             # Traductions PT
└── supabase/
    └── migrations/
        └── 001_initial_schema.sql  # Schema initial
```

### Gotchas connus
```
# CRITICAL: Leaflet ne fonctionne PAS en SSR — utiliser dynamic import avec ssr: false
# CRITICAL: next.config.js doit avoir output: 'standalone' pour Docker
# CRITICAL: OpenWeatherMap free tier = 1000 calls/jour → CACHER les resultats (TTL 30min)
# CRITICAL: Geolocation API necessite HTTPS (sauf localhost)
# CRITICAL: Les coordonnees de Madere sont ~32.6N, -16.9W — centrer la carte correctement
# CRITICAL: UTF-8 sans BOM pour tous les fichiers .md, .json, .ts, .py
# CRITICAL: PWA necessite manifest.json + service worker + HTTPS
# NOTE: Leaflet CSS doit etre importe explicitement (pas auto-inclus)
# NOTE: Les images placeholder suffiront pour le MVP — photos reelles en Phase 1
```

## Implementation Blueprint

### Schema de base de donnees (Supabase PostgreSQL)

```sql
-- 001_initial_schema.sql

-- Extension pour calcul de distance geographique
CREATE EXTENSION IF NOT EXISTS postgis;

-- Table des acteurs locaux
CREATE TABLE actors (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  type TEXT NOT NULL CHECK (type IN (
    'fisherman', 'farmer', 'winemaker', 'cheesemaker',
    'artisan', 'restaurant', 'cafe', 'food_producer',
    'guide', 'market', 'museum', 'distillery'
  )),
  sub_type TEXT,
  description_fr TEXT NOT NULL,
  description_en TEXT,
  description_pt TEXT,
  story_fr TEXT,          -- Histoire longue (le recit)
  story_en TEXT,
  story_pt TEXT,
  latitude DOUBLE PRECISION NOT NULL,
  longitude DOUBLE PRECISION NOT NULL,
  geom GEOMETRY(Point, 4326),  -- PostGIS point
  municipality TEXT NOT NULL,
  region TEXT NOT NULL CHECK (region IN ('north', 'south', 'east', 'west', 'mountain', 'funchal')),
  address TEXT,
  contact_phone TEXT,
  contact_email TEXT,
  website TEXT,
  social_media JSONB DEFAULT '{}',
  opening_hours TEXT,
  seasonal BOOLEAN DEFAULT FALSE,
  season_start INTEGER,   -- Mois (1-12)
  season_end INTEGER,
  price_range TEXT CHECK (price_range IN ('free', 'low', 'medium', 'high')),
  avg_price_eur DECIMAL(8,2),
  accepts_cash BOOLEAN DEFAULT TRUE,
  accepts_card BOOLEAN DEFAULT FALSE,
  accepts_mbway BOOLEAN DEFAULT FALSE,
  languages TEXT[] DEFAULT ARRAY['pt'],
  photos TEXT[] DEFAULT ARRAY[]::TEXT[],
  tags TEXT[] DEFAULT ARRAY[]::TEXT[],
  source_url TEXT,
  verified BOOLEAN DEFAULT FALSE,
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger pour auto-update geom depuis lat/lng
CREATE OR REPLACE FUNCTION update_geom()
RETURNS TRIGGER AS $$
BEGIN
  NEW.geom = ST_SetSRID(ST_MakePoint(NEW.longitude, NEW.latitude), 4326);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_geom
  BEFORE INSERT OR UPDATE OF latitude, longitude ON actors
  FOR EACH ROW EXECUTE FUNCTION update_geom();

-- Trigger pour auto-update updated_at
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_timestamp
  BEFORE UPDATE ON actors
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- Table des spots caches (pas des acteurs, des lieux)
CREATE TABLE spots (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  type TEXT NOT NULL CHECK (type IN (
    'viewpoint', 'swimming', 'hiking', 'beach',
    'waterfall', 'cave', 'stargazing', 'surf', 'cultural'
  )),
  description_fr TEXT NOT NULL,
  description_en TEXT,
  description_pt TEXT,
  latitude DOUBLE PRECISION NOT NULL,
  longitude DOUBLE PRECISION NOT NULL,
  geom GEOMETRY(Point, 4326),
  municipality TEXT NOT NULL,
  region TEXT NOT NULL,
  difficulty TEXT CHECK (difficulty IN ('easy', 'moderate', 'hard')),
  duration_minutes INTEGER,
  access_info TEXT,       -- Comment y acceder
  safety_notes TEXT,      -- Avertissements securite
  best_time TEXT,         -- Meilleur moment de la journee/saison
  seasonal BOOLEAN DEFAULT FALSE,
  season_start INTEGER,
  season_end INTEGER,
  free BOOLEAN DEFAULT TRUE,
  price_eur DECIMAL(8,2),
  photos TEXT[] DEFAULT ARRAY[]::TEXT[],
  tags TEXT[] DEFAULT ARRAY[]::TEXT[],
  source_url TEXT,
  verified BOOLEAN DEFAULT FALSE,
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Meme triggers pour spots
CREATE TRIGGER trigger_update_geom_spots
  BEFORE INSERT OR UPDATE OF latitude, longitude ON spots
  FOR EACH ROW EXECUTE FUNCTION update_geom();

CREATE TRIGGER trigger_update_timestamp_spots
  BEFORE UPDATE ON spots
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- Index pour recherche geographique rapide
CREATE INDEX idx_actors_geom ON actors USING GIST(geom);
CREATE INDEX idx_spots_geom ON spots USING GIST(geom);
CREATE INDEX idx_actors_region ON actors(region);
CREATE INDEX idx_actors_type ON actors(type);
CREATE INDEX idx_actors_active ON actors(active) WHERE active = TRUE;
CREATE INDEX idx_spots_region ON spots(region);
CREATE INDEX idx_spots_type ON spots(type);

-- Vue pour recherche "autour de moi" (fonction helper)
CREATE OR REPLACE FUNCTION nearby_actors(
  user_lat DOUBLE PRECISION,
  user_lng DOUBLE PRECISION,
  radius_km DOUBLE PRECISION DEFAULT 5.0,
  actor_type TEXT DEFAULT NULL
)
RETURNS TABLE (
  id UUID,
  name TEXT,
  type TEXT,
  sub_type TEXT,
  description_fr TEXT,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  municipality TEXT,
  region TEXT,
  distance_km DOUBLE PRECISION,
  opening_hours TEXT,
  price_range TEXT,
  photos TEXT[],
  tags TEXT[]
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    a.id, a.name, a.type, a.sub_type, a.description_fr,
    a.latitude, a.longitude, a.municipality, a.region,
    ST_Distance(
      a.geom::geography,
      ST_SetSRID(ST_MakePoint(user_lng, user_lat), 4326)::geography
    ) / 1000.0 AS distance_km,
    a.opening_hours, a.price_range, a.photos, a.tags
  FROM actors a
  WHERE a.active = TRUE
    AND ST_DWithin(
      a.geom::geography,
      ST_SetSRID(ST_MakePoint(user_lng, user_lat), 4326)::geography,
      radius_km * 1000
    )
    AND (actor_type IS NULL OR a.type = actor_type)
  ORDER BY distance_km;
END;
$$ LANGUAGE plpgsql;

-- Meme pour spots
CREATE OR REPLACE FUNCTION nearby_spots(
  user_lat DOUBLE PRECISION,
  user_lng DOUBLE PRECISION,
  radius_km DOUBLE PRECISION DEFAULT 5.0,
  spot_type TEXT DEFAULT NULL
)
RETURNS TABLE (
  id UUID,
  name TEXT,
  type TEXT,
  description_fr TEXT,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  municipality TEXT,
  region TEXT,
  distance_km DOUBLE PRECISION,
  difficulty TEXT,
  free BOOLEAN,
  photos TEXT[],
  tags TEXT[]
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    s.id, s.name, s.type, s.description_fr,
    s.latitude, s.longitude, s.municipality, s.region,
    ST_Distance(
      s.geom::geography,
      ST_SetSRID(ST_MakePoint(user_lng, user_lat), 4326)::geography
    ) / 1000.0 AS distance_km,
    s.difficulty, s.free, s.photos, s.tags
  FROM spots s
  WHERE s.active = TRUE
    AND ST_DWithin(
      s.geom::geography,
      ST_SetSRID(ST_MakePoint(user_lng, user_lat), 4326)::geography,
      radius_km * 1000
    )
    AND (spot_type IS NULL OR s.type = spot_type)
  ORDER BY distance_km;
END;
$$ LANGUAGE plpgsql;

-- RLS (Row Level Security) : lecture publique, ecriture admin uniquement
ALTER TABLE actors ENABLE ROW LEVEL SECURITY;
ALTER TABLE spots ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read actors" ON actors FOR SELECT USING (active = TRUE);
CREATE POLICY "Public read spots" ON spots FOR SELECT USING (active = TRUE);
```

### Liste des taches ordonnees

```yaml
Task 1:
  action: CREATE
  path: supabase/migrations/001_initial_schema.sql
  description: |
    Creer le schema PostgreSQL avec PostGIS.
    Tables actors et spots avec triggers geom auto.
    Fonctions nearby_actors() et nearby_spots().
    Index GiST pour recherche spatiale.
    RLS public read.
  validation: Schema deploye, tables accessibles via Supabase client

Task 2:
  action: CREATE
  path: backend/seed/data/*.json
  description: |
    Structurer les 130+ acteurs identifies par les agents de recherche
    en fichiers JSON par categorie. Chaque acteur doit avoir au minimum :
    name, type, description_fr, latitude, longitude, municipality, region.
    Les coordonnees GPS doivent etre recherchees via geocoding si non connues.
    IMPORTANT: Utiliser les rapports des 8 agents comme source.
  validation: Fichiers JSON valides, 130+ entrees au total

Task 3:
  action: CREATE
  path: backend/**
  description: |
    Backend FastAPI complet :
    - main.py : app FastAPI avec CORS, lifespan
    - config.py : settings via pydantic-settings (env vars)
    - models/ : Pydantic models Actor, Spot, Weather, SearchQuery
    - api/actors.py : GET /actors, GET /actors/{id}, GET /actors/nearby
    - api/spots.py : GET /spots, GET /spots/{id}, GET /spots/nearby
    - api/weather.py : GET /weather/{region} (proxy cache OpenWeatherMap)
    - api/search.py : POST /search (langage naturel via LiteLLM)
    - api/health.py : GET /health
    - services/ : logique metier, cache meteo (TTL 30min), search IA
    - seed/seed_actors.py : script pour charger les JSON dans Supabase
  pattern: Vertical slice, Pydantic v2, async
  validation: curl localhost:8000/health retourne OK

Task 4:
  action: CREATE
  path: frontend/**
  description: |
    Frontend Next.js 14 App Router :
    - Carte Leaflet pleine page (dynamic import, ssr:false)
    - Marqueurs colores par type d'acteur
    - Popup preview au clic sur marqueur
    - FilterBar : filtres zone + type + "ouvert maintenant"
    - SearchBar : recherche langage naturel
    - ActorProfile page : photo, histoire, contact direct, carte mini
    - WeatherWidget : meteo par zone en haut de page
    - LocateMe : bouton GPS "autour de moi"
    - LanguageSwitcher : FR/EN/PT
    - Mobile-first responsive design (Tailwind)
    - PWA : manifest.json, service worker, icons
  pattern: shadcn/ui, Tailwind CSS, App Router
  validation: npm run build reussit, page carte s'affiche

Task 5:
  action: CREATE
  path: docker-compose.yml
  description: |
    Docker Compose pour deploiement VM 103 :
    - Service backend (FastAPI, port 8030)
    - Service frontend (Next.js, port 3030)
    - Reseau interne
    - Env vars via .env
    Note : Supabase est DEJA sur VM 103, pas besoin de le dockeriser
  validation: docker compose up -d demarre les 2 services

Task 6:
  action: CONFIGURE
  path: VM 103 Nginx
  description: |
    Configurer reverse proxy Nginx sur VM 103 pour :
    - gaia.multipass.agency → frontend (port 3030)
    - gaia.multipass.agency/api → backend (port 8030)
    - SSL via Let's Encrypt (certbot)
  validation: https://gaia.multipass.agency accessible

Task 7:
  action: EXECUTE
  path: backend/seed/seed_actors.py
  description: |
    Lancer le script de seed pour charger les 130+ acteurs dans Supabase.
    Verifier que tous les acteurs apparaissent sur la carte.
  validation: SELECT count(*) FROM actors retourne 130+
```

### Pseudocode composants cles

```
# Map.tsx — Composant carte Leaflet (CLIENT COMPONENT)
# GOTCHA: dynamic import obligatoire, pas de SSR
#
# import dynamic from 'next/dynamic'
# const Map = dynamic(() => import('@/components/Map'), { ssr: false })
#
# Centre: [32.65, -16.91] (Madeira)
# Zoom initial: 11 (toute l'ile visible)
# Tiles: OpenStreetMap (gratuit)
# Marqueurs: icones colorees par type (L.divIcon avec Tailwind colors)
# Cluster: react-leaflet-cluster pour eviter surcharge visuelle
# Popup: ActorCard en preview

# SearchService — Recherche IA langage naturel
#
# Input: "Je veux manger du poisson frais pres de Sao Vicente"
# 1. Envoyer a LiteLLM/Claude avec contexte:
#    - Liste des types d'acteurs
#    - Liste des regions/municipalites
#    - Instruction: extraire type, region, mots-cles
# 2. Recevoir JSON structure: {type: "restaurant", region: "north", tags: ["fish", "fresh"]}
# 3. Query Supabase avec ces filtres
# 4. Retourner resultats tries par pertinence

# WeatherService — Proxy meteo avec cache
#
# Regions Madeira (5 points meteo):
#   north: [32.80, -17.00] (Sao Vicente)
#   south: [32.63, -16.91] (Funchal)
#   east: [32.72, -16.73] (Machico)
#   west: [32.72, -17.17] (Calheta)
#   mountain: [32.76, -16.95] (Pico Ruivo area)
#
# Cache Redis ou dict en memoire, TTL 30 min
# OpenWeatherMap free: 1000 calls/jour → 5 regions × 48 updates = 240 calls/jour OK
```

### Points d'integration

```yaml
ROUTER:
  - Non applicable (projet standalone, pas un skill)

VAULT:
  - Note existante : R2D2-Memory/projets/madeira-gaia.md (deja a jour)
  - Note existante : R2D2-Memory/sessions/2026-04-01_madeira-gaia.md
  - Pas de nouvelle note vault necessaire pour le MVP

MCP:
  - Non impacte

CLAUDE.MD:
  - Ajouter dans la section "Services par VM" le nouveau service GAIA sur VM 103
  - Ajouter URL gaia.multipass.agency dans les chemins importants

DNS:
  - Creer sous-domaine gaia.multipass.agency pointant vers VM 103
```

## Validation Loop

### Niveau 1 : Structure & Syntax
```bash
# Verifier que le projet existe
ls -la C:/Users/r2d2/Documents/Projets/Marketplace-GAIA/madeira/backend/main.py
ls -la C:/Users/r2d2/Documents/Projets/Marketplace-GAIA/madeira/frontend/package.json
ls -la C:/Users/r2d2/Documents/Projets/Marketplace-GAIA/madeira/docker-compose.yml

# Verifier les fichiers seed
ls C:/Users/r2d2/Documents/Projets/Marketplace-GAIA/madeira/backend/seed/data/

# Verifier que le frontend build
cd C:/Users/r2d2/Documents/Projets/Marketplace-GAIA/madeira/frontend && npm run build

# Verifier que le backend demarre
cd C:/Users/r2d2/Documents/Projets/Marketplace-GAIA/madeira/backend && python -c "from main import app; print('OK')"
```

### Niveau 2 : Fonctionnel
```bash
# Backend API repond
curl http://localhost:8030/health
curl http://localhost:8030/api/actors | python -m json.tool | head -20
curl http://localhost:8030/api/actors/nearby?lat=32.65&lng=-16.91&radius=5
curl http://localhost:8030/api/weather/south
curl -X POST http://localhost:8030/api/search -H "Content-Type: application/json" \
  -d '{"query": "poisson frais nord"}'

# Frontend s'affiche
curl -s http://localhost:3030 | grep -c "GAIA"

# Nombre d'acteurs en base
# Via Supabase: SELECT count(*) FROM actors WHERE active = true;
```

### Niveau 3 : Integration
```bash
# Depuis l'exterieur (apres deploy VM 103 + DNS)
curl -I https://gaia.multipass.agency
curl https://gaia.multipass.agency/api/health

# PWA valide (Lighthouse)
# Ouvrir Chrome DevTools > Application > Manifest = OK
# Service Worker = registered

# Mobile test : ouvrir sur telephone, carte s'affiche, GPS fonctionne
```

## Checklist de validation finale

- [ ] Schema Supabase deploye avec PostGIS et fonctions nearby_*
- [ ] 130+ acteurs charges dans la base (seed data)
- [ ] Backend FastAPI operationnel (6 endpoints)
- [ ] Frontend Next.js 14 build et fonctionne
- [ ] Carte Leaflet avec marqueurs colores par type
- [ ] Filtres zone + type fonctionnels
- [ ] Geolocalisation "autour de moi" fonctionne
- [ ] Meteo par zone affichee (cache 30min)
- [ ] Recherche langage naturel retourne des resultats pertinents
- [ ] Multilingue FR/EN/PT fonctionne
- [ ] PWA installable (manifest + service worker)
- [ ] Docker Compose fonctionnel
- [ ] Deploye sur VM 103
- [ ] Accessible via gaia.multipass.agency (HTTPS)
- [ ] Mobile-first, < 3s chargement
- [ ] CLAUDE.md mis a jour

## Anti-Patterns a eviter

- NE PAS utiliser Google Maps (payant) — Leaflet + OSM suffit
- NE PAS creer de systeme d'auth pour le MVP (acces public)
- NE PAS implementer de paiement/reservation (hors scope MVP)
- NE PAS sur-engineerer le backend — FastAPI simple, pas de microservices
- NE PAS hardcoder les coordonnees — tout en base de donnees
- NE PAS oublier le dynamic import de Leaflet (SSR crash garanti)
- NE PAS depasser 1000 calls/jour OpenWeatherMap (cacher !)
- NE PAS creer d'app native — PWA uniquement
- NE PAS stocker de photos en base — URLs vers Supabase Storage
- NE PAS traduire via Google Translate — traductions manuelles FR/EN/PT

## Notes pour l'agent d'execution

1. **Les donnees des acteurs viennent des 8 rapports de recherche** de la session du 2026-04-01.
   Ces rapports sont dans les outputs des agents (temporaires). Il faudra les re-rechercher
   ou utiliser les informations de la session pour reconstruire les fichiers seed JSON.
   Priorite : commencer par 30-50 acteurs bien documentes, completer ensuite.

2. **Les coordonnees GPS** des acteurs ne sont pas toutes connues. Utiliser :
   - Nominatim API (gratuit) pour geocoder les adresses connues
   - Coordonnees approximatives des municipalites pour les autres
   - Marqueur `verified: false` pour les positions estimees

3. **La VM 103** (192.168.1.163) a deja Docker, Supabase, et Nginx.
   Se connecter en SSH (root) pour deployer. Verifier les ports disponibles.

4. **Le domaine multipass.agency** est deja configure. Il faut ajouter le sous-domaine
   `gaia` dans le DNS (Cloudflare ou registrar).

5. **LiteLLM** est deja configure sur VM 103 pour la recherche IA.
   Endpoint : verifier dans docker-compose existant.

---

**Confidence: 8/10** — Stack bien connu, donnees disponibles, infra existante. Points de risque :
PostGIS sur Supabase managed (verifier disponibilite extension), coordonnees GPS des acteurs
(effort de geocoding), et deploy DNS/SSL (dependance externe).
