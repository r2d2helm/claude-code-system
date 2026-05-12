name: "PRP - R2D2 SaaS Complet"
description: |
  Blueprint pour transformer le R2D2 Agent MVP (bot Telegram + FastAPI)
  en plateforme SaaS complete multi-tenant pour PME europeennes.

---

## Goal

Transformer le R2D2 Agent existant (~1800 lignes Python, bot Telegram live)
en une plateforme SaaS complete avec :
- Frontend web Next.js 14 (10 pages)
- Auth multi-tenant via Supabase
- Ticketing complet (creation, suivi, conversation)
- Assistant IA integre (chat web)
- Billing via Stripe (10 packs x 3 tiers)
- Dashboard client + admin
- Notifications email
- Deploy Docker multi-service

Etat final : un client PME peut s'inscrire, ouvrir un ticket, parler a l'IA,
voir son monitoring, payer son abonnement, et evaluer le service.

## Why

- **Revenue** : 10 packs commerciaux prets (GPS 150-350 EUR, Boussole 500-2500 EUR, Ancrage 1500-15000 EUR)
- **Deadline NIS2** : 18 avril 2026 (24 jours) - les PME ont BESOIN d'aide maintenant
- **Runway** : juin 2026 - le premier client doit signer VITE
- **Differentiation** : 0 concurrent open source+cyber en Flandre
- **Subsides** : cheque wallon 75%, KMO-portefeuille 45%, Bruxelles 25-70%
- **Infrastructure existante** : Supabase, LiteLLM, PostgreSQL, Beszel deja deployes sur les VMs

## What

### Success Criteria
- [ ] Un prospect peut s'inscrire en 3 etapes (Entreprise/Contact/Besoins)
- [ ] Un client connecte voit son dashboard (tickets, status systeme, IA, RDV)
- [ ] Un client peut creer un ticket et suivre la conversation
- [ ] Un client peut chatter avec l'assistant IA
- [ ] Un client peut voir ses factures et son abonnement
- [ ] Stripe Checkout fonctionne pour les 3 tiers (GPS/Boussole/Ancrage)
- [ ] Les notifications email sont envoyees (bienvenue, ticket, resolution)
- [ ] Multi-langue FR/NL/EN fonctionne
- [ ] Le tout deploye en containers Docker sur VM 103
- [ ] Health checks et monitoring Beszel/Uptime Kuma operationnels

## Contexte necessaire

### Documentation & References
```yaml
# MUST READ - Existant a etendre
- file: C:\Users\r2d2\Documents\Projets\R2D2-Agent\src\gateway\app.py
  why: Backend FastAPI existant - a etendre avec routes clients/tickets/billing

- file: C:\Users\r2d2\Documents\Projets\R2D2-Agent\src\models\schemas.py
  why: Modeles Pydantic existants - a etendre

- file: C:\Users\r2d2\Documents\Projets\R2D2-Agent\src\gateway\config.py
  why: Configuration - ajouter Supabase/Stripe vars

- file: C:\Users\r2d2\Documents\Projets\R2D2-Agent\src\gateway\audit.py
  why: Pattern PostgreSQL existant - a suivre pour les nouvelles tables

- file: C:\Users\r2d2\Documents\Projets\R2D2-Agent\src\gateway\router.py
  why: Routeur skills existant

- file: C:\Users\r2d2\Documents\Projets\R2D2-Agent\src\gateway\llm_client.py
  why: Client LLM existant - reutiliser pour le chat web

- file: C:\Users\r2d2\Documents\Projets\R2D2-Agent\src\channels\telegram_bot.py
  why: Pattern channel existant - le web channel suivra le meme pattern

- file: C:\Users\r2d2\Documents\Projets\R2D2-Agent\src\mcp_bridge\client.py
  why: Bridge MCP existant - reutiliser

# MUST READ - Specs UI completes
- file: C:\Users\r2d2\Documents\Knowledge\Projets\MultiPass\MultiPass-Interface-Client-Specs.md
  why: 724 lignes de specs UI detaillees (10 pages, wireframes ASCII, champs, flows)

# MUST READ - Offres commerciales
- file: C:\Users\r2d2\Documents\Knowledge\Projets\R2D2-Catalogue-Commercial-2026.md
  why: 10 packs x 3 tiers avec prix, subsides, livrables

# REFERENCE - Pages marketing existantes
- dir: C:\Users\r2d2\Documents\Knowledge\Projets\MultiPass\html\
  why: 8 pages HTML marketing (landing, packs, dossiers) - a integrer ou lier
```

### Infrastructure existante (VMs)
```
VM 103 (r2d2-main, 192.168.1.163) — Hote principal SaaS
├── Supabase (Auth + DB + Realtime + Storage)  ← DEJA LA
│   ├── supabase-auth
│   ├── supabase-db (PostgreSQL 15)
│   ├── supabase-realtime
│   ├── supabase-storage
│   ├── supabase-rest (PostgREST)
│   └── supabase-studio (:3000)
├── LiteLLM (:4000)                            ← DEJA LA
├── Langfuse                                    ← DEJA LA
├── Frontend container (a creer)               ← A FAIRE
├── R2D2 Agent (a deployer)                    ← A FAIRE
└── Monitoring stack                            ← DEJA LA

VM 104 (r2d2-store, 192.168.1.164) — Stockage
├── postgres-shared (:5432)                     ← DEJA LA (r2d2_audit table)
└── NFS                                         ← DEJA LA
```

### Arbre actuel du projet
```
R2D2-Agent/
├── src/
│   ├── main.py                  # Uvicorn entry point
│   ├── gateway/
│   │   ├── app.py              # FastAPI (175 lines, 6 routes)
│   │   ├── agent.py            # R2D2Agent orchestrator (148 lines)
│   │   ├── router.py           # Intent detection 7 skills (142 lines)
│   │   ├── config.py           # Settings pydantic (48 lines)
│   │   ├── llm_client.py       # LiteLLM client (149 lines)
│   │   └── audit.py            # PostgreSQL audit (131 lines)
│   ├── channels/
│   │   ├── telegram_bot.py     # Telegram handler (~300 lines)
│   │   ├── stt.py              # Whisper STT (61 lines)
│   │   └── tts.py              # edge-tts TTS (146 lines)
│   ├── models/
│   │   └── schemas.py          # Pydantic models (79 lines)
│   └── mcp_bridge/
│       └── client.py           # MCP bridge (169 lines)
├── config/
│   └── .env.example            # Empty template
├── deploy/
│   ├── docker-compose.yml      # Single service
│   └── docker-compose.bot.yml  # Legacy
├── Dockerfile                  # Python 3.12-slim
├── pyproject.toml              # Dependencies
└── test_bot_live.py            # Live test (hardcoded creds)
```

### Arbre souhaite (nouveaux fichiers)
```
R2D2-Agent/
├── src/
│   ├── main.py                          # MODIFY: ajout startup events
│   ├── gateway/
│   │   ├── app.py                      # MODIFY: nouvelles routes
│   │   ├── agent.py                    # AS-IS
│   │   ├── router.py                   # AS-IS
│   │   ├── config.py                   # MODIFY: +Supabase, +Stripe, +SMTP
│   │   ├── llm_client.py              # AS-IS
│   │   ├── audit.py                    # AS-IS
│   │   ├── auth.py                     # NEW: Supabase JWT validation
│   │   ├── clients.py                  # NEW: CRUD clients PostgreSQL
│   │   ├── tickets.py                  # NEW: Ticketing complet
│   │   ├── billing.py                  # NEW: Stripe integration
│   │   └── email_service.py           # NEW: SMTP notifications
│   ├── channels/
│   │   ├── telegram_bot.py            # AS-IS
│   │   ├── web_channel.py             # NEW: WebSocket chat pour frontend
│   │   ├── stt.py                     # AS-IS
│   │   └── tts.py                     # AS-IS
│   ├── models/
│   │   ├── schemas.py                 # MODIFY: +Client, +Ticket, +Billing models
│   │   └── database.py               # NEW: SQLAlchemy/asyncpg schemas
│   └── mcp_bridge/
│       └── client.py                  # AS-IS
├── frontend/                           # NEW: Next.js 14 app
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── Dockerfile                     # NEW: Node 20 Alpine
│   ├── public/
│   │   └── logo.svg
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx             # Root layout (FR/NL/EN)
│   │   │   ├── page.tsx               # Landing page (port from HTML)
│   │   │   ├── login/page.tsx         # Connexion
│   │   │   ├── register/
│   │   │   │   └── page.tsx           # Inscription 3 etapes
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx           # Dashboard client
│   │   │   │   ├── tickets/
│   │   │   │   │   ├── page.tsx       # Liste tickets
│   │   │   │   │   ├── new/page.tsx   # Nouveau ticket
│   │   │   │   │   └── [id]/page.tsx  # Vue ticket conversation
│   │   │   │   ├── ai/page.tsx        # Assistant IA chat
│   │   │   │   ├── billing/page.tsx   # Factures & abonnement
│   │   │   │   ├── settings/page.tsx  # Profil & parametres
│   │   │   │   └── layout.tsx         # Dashboard layout (sidebar)
│   │   │   ├── evaluate/[id]/page.tsx # Evaluation service
│   │   │   └── api/
│   │   │       └── stripe-webhook/route.ts  # Stripe webhook handler
│   │   ├── components/
│   │   │   ├── ui/                    # shadcn/ui components
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── TicketCard.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── StatusBadge.tsx
│   │   │   ├── RegistrationWizard.tsx
│   │   │   └── LanguageSwitcher.tsx
│   │   ├── lib/
│   │   │   ├── supabase.ts            # Supabase client (browser + server)
│   │   │   ├── api.ts                 # FastAPI client wrapper
│   │   │   ├── stripe.ts              # Stripe client
│   │   │   └── i18n.ts               # Internationalization FR/NL/EN
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useTickets.ts
│   │   │   └── useChat.ts
│   │   └── types/
│   │       └── index.ts              # TypeScript types
│   └── messages/
│       ├── fr.json                    # Traductions FR
│       ├── nl.json                    # Traductions NL
│       └── en.json                    # Traductions EN
├── sql/                               # NEW: Migration SQL
│   ├── 001_clients.sql
│   ├── 002_tickets.sql
│   ├── 003_billing.sql
│   └── 004_rls_policies.sql
├── config/
│   ├── .env.example                   # MODIFY: template complet
│   └── .env.production               # NEW: production values template
├── deploy/
│   ├── docker-compose.yml            # MODIFY: multi-service
│   ├── docker-compose.dev.yml        # NEW: dev environment
│   ├── nginx.conf                    # NEW: reverse proxy
│   └── Caddyfile                     # NEW: alternative (auto-SSL)
├── Dockerfile                         # AS-IS (backend)
├── pyproject.toml                     # MODIFY: +stripe, +emails
└── README.md                          # NEW: documentation
```

### Gotchas connus
```
# CRITICAL: Encodage UTF-8 sans BOM pour .md/.json/.ts/.tsx
# CRITICAL: Supabase sur VM 103 (192.168.1.163) - verifier les ports exposes
# CRITICAL: PostgreSQL shared sur VM 104 (192.168.1.164:5432) - user r2d2agent
# CRITICAL: PAS d'interaction VMs sans autorisation explicite
# CRITICAL: Ne PAS hardcoder les credentials (utiliser .env)
# CRITICAL: CORS stricte en production (plus de allow_origins=["*"])
# INFO: LiteLLM sur VM 103:4000
# INFO: Beszel sur VM 100:8091 (pas VM 103)
# INFO: Next.js peut utiliser le Supabase deja sur VM 103
# INFO: Stripe en mode test d'abord (cles test)
```

## Implementation Blueprint

### Phase 1 : Database Schema (SQL migrations)

```yaml
Task 1.1:
  action: CREATE
  path: R2D2-Agent/sql/001_clients.sql
  description: |
    Tables clients et users.
    - companies: id, name, vat_number, sector, employees, region, postal_code, tier, created_at
    - users: id, company_id (FK), email, first_name, last_name, phone, role, language, supabase_uid
    - Index sur company_id, email, supabase_uid

Task 1.2:
  action: CREATE
  path: R2D2-Agent/sql/002_tickets.sql
  description: |
    Tables ticketing complet.
    - tickets: id, company_id (FK), user_id (FK), ticket_number (MP-YYYY-NNNN), category, subject,
      description, urgency (low/normal/high/critical), status (open/in_progress/resolved/closed),
      created_at, updated_at, resolved_at
    - ticket_messages: id, ticket_id (FK), sender_type (client/agent/ai), sender_name, content,
      attachments JSONB, created_at
    - ticket_evaluations: id, ticket_id (FK), satisfaction INT, speed INT, clarity INT,
      resolved BOOL, nps INT, comment TEXT, created_at

Task 1.3:
  action: CREATE
  path: R2D2-Agent/sql/003_billing.sql
  description: |
    Tables billing.
    - subscriptions: id, company_id (FK), pack_name, tier (gps/boussole/ancrage),
      stripe_subscription_id, stripe_customer_id, status, monthly_amount, subsidy_rate,
      effective_amount, started_at, next_billing
    - invoices: id, company_id (FK), subscription_id (FK), stripe_invoice_id,
      amount, status, period_start, period_end, pdf_url, created_at

Task 1.4:
  action: CREATE
  path: R2D2-Agent/sql/004_rls_policies.sql
  description: |
    Row Level Security pour Supabase.
    - Chaque company ne voit que SES donnees
    - Admin voit tout
    - Policies sur companies, users, tickets, ticket_messages, subscriptions, invoices
```

### Phase 2 : Backend API (Python/FastAPI)

```yaml
Task 2.1:
  action: MODIFY
  path: R2D2-Agent/src/gateway/config.py
  description: |
    Ajouter variables Supabase, Stripe, SMTP :
    - supabase_url, supabase_anon_key, supabase_service_key
    - stripe_secret_key, stripe_webhook_secret, stripe_publishable_key
    - smtp_host, smtp_port, smtp_user, smtp_password, smtp_from
    - frontend_url (pour CORS et emails)

Task 2.2:
  action: CREATE
  path: R2D2-Agent/src/gateway/auth.py
  description: |
    Auth middleware Supabase JWT.
    - verify_supabase_token(authorization: str) -> dict (user info)
    - get_current_user() dependency FastAPI
    - get_current_company() dependency (join user -> company)
    - Garder verify_api_key() existant pour les channels (Telegram, API)

Task 2.3:
  action: CREATE
  path: R2D2-Agent/src/gateway/clients.py
  description: |
    CRUD clients via asyncpg (pas ORM, meme pattern que audit.py).
    Routes :
    - POST /api/register (3-step: company + user + needs -> ticket auto)
    - GET /api/me (profil utilisateur + company)
    - PATCH /api/me (update profil)
    - GET /api/me/usage (stats du mois)
    - GET /api/me/infrastructure (monitoring Beszel du client)

Task 2.4:
  action: CREATE
  path: R2D2-Agent/src/gateway/tickets.py
  description: |
    Ticketing complet.
    Routes :
    - POST /api/tickets (creer un ticket)
    - GET /api/tickets (lister mes tickets, filtres status/urgency)
    - GET /api/tickets/{id} (detail + messages)
    - POST /api/tickets/{id}/messages (ajouter message)
    - PATCH /api/tickets/{id} (update status)
    - POST /api/tickets/{id}/evaluate (evaluation NPS)
    Logique :
    - Numero auto-increment MP-YYYY-NNNN
    - Notification email a chaque changement de status
    - L'IA peut repondre automatiquement (si auto_actions=True)

Task 2.5:
  action: CREATE
  path: R2D2-Agent/src/gateway/billing.py
  description: |
    Stripe integration.
    Routes :
    - POST /api/billing/checkout (creer Stripe Checkout Session)
    - GET /api/billing/subscription (abonnement actuel)
    - GET /api/billing/invoices (historique factures)
    - POST /api/billing/portal (Stripe Customer Portal URL)
    Webhook (dans le frontend Next.js api route) :
    - checkout.session.completed -> creer subscription
    - invoice.paid -> creer invoice record
    - customer.subscription.deleted -> desactiver

Task 2.6:
  action: CREATE
  path: R2D2-Agent/src/gateway/email_service.py
  description: |
    Service email SMTP.
    Templates :
    - welcome(user, company) -> email bienvenue
    - ticket_created(user, ticket) -> confirmation ticket
    - ticket_updated(user, ticket, message) -> nouvelle reponse
    - ticket_resolved(user, ticket) -> resolution + upsell
    - invoice_paid(user, invoice) -> recu
    Utiliser string templates Python (pas de dependance lourde).

Task 2.7:
  action: CREATE
  path: R2D2-Agent/src/channels/web_channel.py
  description: |
    WebSocket channel pour le chat IA frontend.
    - /ws/chat endpoint WebSocket
    - Auth via Supabase JWT dans le handshake
    - Meme pipeline que Telegram : message -> detect_intent -> MCP -> LLM -> response
    - Support streaming (token par token)

Task 2.8:
  action: MODIFY
  path: R2D2-Agent/src/models/schemas.py
  description: |
    Ajouter modeles Pydantic :
    - CompanyCreate, CompanyResponse
    - UserCreate, UserResponse
    - TicketCreate, TicketResponse, TicketMessageCreate, TicketMessageResponse
    - TicketEvaluation
    - SubscriptionResponse, InvoiceResponse
    - RegisterRequest (3 steps combined)

Task 2.9:
  action: MODIFY
  path: R2D2-Agent/src/gateway/app.py
  description: |
    Integrer les nouveaux routers FastAPI :
    - app.include_router(clients_router, prefix="/api")
    - app.include_router(tickets_router, prefix="/api")
    - app.include_router(billing_router, prefix="/api")
    - Ajouter WebSocket route pour chat
    - Restreindre CORS (frontend_url seulement)
    - Initialiser email_service dans lifespan

Task 2.10:
  action: MODIFY
  path: R2D2-Agent/pyproject.toml
  description: |
    Ajouter dependencies :
    - stripe>=11
    - python-jose[cryptography]>=3.3 (JWT validation)
    - aiosmtplib>=3 (async SMTP)
    - websockets>=13
    - python-multipart>=0.0.9 (file uploads)

Task 2.11:
  action: MODIFY
  path: R2D2-Agent/config/.env.example
  description: |
    Template complet avec toutes les variables :
    R2D2_SUPABASE_URL, R2D2_SUPABASE_ANON_KEY, R2D2_SUPABASE_SERVICE_KEY,
    R2D2_STRIPE_SECRET_KEY, R2D2_STRIPE_WEBHOOK_SECRET, R2D2_STRIPE_PUBLISHABLE_KEY,
    R2D2_SMTP_HOST, R2D2_SMTP_PORT, R2D2_SMTP_USER, R2D2_SMTP_PASSWORD, R2D2_SMTP_FROM,
    R2D2_FRONTEND_URL
```

### Phase 3 : Frontend Next.js

```yaml
Task 3.1:
  action: CREATE
  path: R2D2-Agent/frontend/
  description: |
    Initialiser le projet Next.js 14 avec :
    - npx create-next-app@latest --typescript --tailwind --eslint --app --src-dir
    - npx shadcn-ui@latest init (New York style, slate colors)
    - Installer: @supabase/supabase-js, @stripe/stripe-js, next-intl
    - Configurer next.config.js (output: standalone, i18n)

Task 3.2:
  action: CREATE
  path: R2D2-Agent/frontend/src/lib/supabase.ts
  description: |
    Clients Supabase :
    - createBrowserClient() pour les composants client
    - createServerClient() pour les Server Components
    - Middleware auth (redirect /login si pas connecte)

Task 3.3:
  action: CREATE
  path: R2D2-Agent/frontend/src/lib/api.ts
  description: |
    Client API FastAPI :
    - Wrapper fetch avec auth header (Supabase JWT)
    - Fonctions typees : getTickets(), createTicket(), getUsage(), etc.
    - Base URL configurable (NEXT_PUBLIC_API_URL)

Task 3.4:
  action: CREATE
  path: R2D2-Agent/frontend/src/app/page.tsx
  description: |
    Landing page.
    Port depuis html/index.html existant.
    Sections : Hero, 3 offres, trust signals (RGPD, NIS2, pas de cloud US),
    secteurs, footer.
    CTA : "Prendre rendez-vous" + "Voir nos offres"

Task 3.5:
  action: CREATE
  path: R2D2-Agent/frontend/src/app/register/page.tsx
  description: |
    Inscription 3 etapes (wizard).
    Etape 1: Entreprise (nom, TVA, secteur, employes, region, code postal)
    Etape 2: Contact (prenom, nom, email, phone, fonction, langue, mot de passe)
    Etape 3: Besoins (type[], description, urgence, source, RGPD consent)
    -> POST /api/register -> Supabase signup + company + ticket auto
    -> Redirect /dashboard

Task 3.6:
  action: CREATE
  path: R2D2-Agent/frontend/src/app/login/page.tsx
  description: |
    Page connexion.
    Email + mot de passe -> Supabase signInWithPassword
    "Se souvenir de moi" checkbox
    Liens: mot de passe oublie, creer un compte

Task 3.7:
  action: CREATE
  path: R2D2-Agent/frontend/src/app/dashboard/
  description: |
    Dashboard client complet.
    Layout : sidebar (Accueil, Tickets, IA, Docs, Factures, Profil)
    Page principale :
    - 4 cards (tickets ouverts, status systeme, prochain RDV, assistant IA)
    - Liste tickets recents
    - Boutons : nouveau ticket, parler a l'IA

Task 3.8:
  action: CREATE
  path: R2D2-Agent/frontend/src/app/dashboard/tickets/
  description: |
    Ticketing :
    - page.tsx : liste tickets avec filtres (status, urgence)
    - new/page.tsx : formulaire nouveau ticket (categorie, sujet, description, PJ, urgence)
    - [id]/page.tsx : vue conversation (messages, reponses IA/technicien, actions)
    Realtime via Supabase Realtime (nouveau message = notification live)

Task 3.9:
  action: CREATE
  path: R2D2-Agent/frontend/src/app/dashboard/ai/page.tsx
  description: |
    Chat IA.
    Interface type ChatGPT :
    - Messages scrollables
    - Input + bouton envoyer + micro (voice)
    - Suggestions rapides contextuelles
    - WebSocket vers /ws/chat
    - Indicateur "IA ecrit..."

Task 3.10:
  action: CREATE
  path: R2D2-Agent/frontend/src/app/dashboard/billing/page.tsx
  description: |
    Facturation.
    - Abonnement actuel (pack, tier, montant, subside)
    - Prochaine facture
    - Historique factures (telecharger PDF)
    - Bouton "Gerer mon abonnement" -> Stripe Portal

Task 3.11:
  action: CREATE
  path: R2D2-Agent/frontend/src/app/dashboard/settings/page.tsx
  description: |
    Profil & parametres.
    Sections : infos entreprise, contact principal, acces distance,
    infra monitoree, abonnement.
    Formulaires editables.

Task 3.12:
  action: CREATE
  path: R2D2-Agent/frontend/src/app/evaluate/[id]/page.tsx
  description: |
    Evaluation service (apres resolution ticket).
    Formulaire : satisfaction, rapidite, clarte (etoiles),
    resolu (oui/partiel/non), NPS 0-10, commentaire.

Task 3.13:
  action: CREATE
  path: R2D2-Agent/frontend/messages/
  description: |
    Fichiers i18n :
    - fr.json : toutes les chaines en francais
    - nl.json : traduction neerlandais
    - en.json : traduction anglais
    Utiliser next-intl pour le routing /fr /nl /en

Task 3.14:
  action: CREATE
  path: R2D2-Agent/frontend/src/components/
  description: |
    Composants reutilisables :
    - Header.tsx (logo, nav, langue, profil)
    - Sidebar.tsx (menu dashboard)
    - TicketCard.tsx (preview ticket dans la liste)
    - ChatMessage.tsx (bulle message client/IA)
    - StatusBadge.tsx (online/offline/warning avec couleurs)
    - RegistrationWizard.tsx (stepper 3 etapes)
    - LanguageSwitcher.tsx (FR/NL/EN dropdown)
    Utiliser shadcn/ui : Button, Card, Input, Select, Badge, Dialog, Tabs, Avatar

Task 3.15:
  action: CREATE
  path: R2D2-Agent/frontend/Dockerfile
  description: |
    Multi-stage build :
    Stage 1: node:20-alpine, npm ci, npm run build
    Stage 2: node:20-alpine, copy standalone, EXPOSE 3000
    Healthcheck sur /api/health
```

### Phase 4 : DevOps & Deploy

```yaml
Task 4.1:
  action: MODIFY
  path: R2D2-Agent/deploy/docker-compose.yml
  description: |
    Multi-service complet :
    services:
      r2d2-api:       # Backend FastAPI (:8030)
      r2d2-frontend:  # Next.js (:3000)
      r2d2-bot:       # Telegram bot (standalone)
      nginx:          # Reverse proxy (:80/:443)
    networks: r2d2-net
    Volumes pour data persistance.
    Env_file pour chaque service.

Task 4.2:
  action: CREATE
  path: R2D2-Agent/deploy/nginx.conf
  description: |
    Reverse proxy :
    - / -> frontend:3000
    - /api -> api:8030
    - /ws -> api:8030 (WebSocket upgrade)
    - /healthz -> api:8030/healthz
    Rate limiting, security headers, gzip.

Task 4.3:
  action: CREATE
  path: R2D2-Agent/deploy/docker-compose.dev.yml
  description: |
    Dev environment (overrides) :
    - Volumes mounts pour hot-reload
    - Pas de nginx (ports directs)
    - Variables dev (Stripe test keys, etc.)
```

### Phase 5 : Integration & Polish

```yaml
Task 5.1:
  action: CONFIGURE
  description: |
    Stripe Products/Prices setup (mode test) :
    - 10 products (un par pack)
    - 3 prices par product (GPS/Boussole/Ancrage)
    - Webhook endpoint configure

Task 5.2:
  action: CONFIGURE
  description: |
    Supabase setup :
    - Creer les tables via SQL migrations
    - Activer RLS
    - Configurer l'auth (email/password, redirect URLs)
    - Activer Realtime sur la table ticket_messages

Task 5.3:
  action: CONFIGURE
  description: |
    Monitoring :
    - Ajouter les containers dans Beszel
    - Ajouter les URLs dans Uptime Kuma
    - Configurer alertes Telegram
```

## Pseudocode par tache critique

### Auth middleware (Task 2.2)
```python
# PATTERN: Suivre verify_api_key() dans app.py
# GOTCHA: Supabase JWT contient sub (user_id), email, role
import httpx
from jose import jwt, JWTError

async def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    # Verifier le JWT avec la cle publique Supabase
    # GOTCHA: utiliser supabase_url + /auth/v1/token?grant_type=... pour refresh
    payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
    user_id = payload.get("sub")
    # Chercher le user dans notre table users (pas Supabase auth)
    user = await db.fetchrow("SELECT * FROM users WHERE supabase_uid = $1", user_id)
    if not user:
        raise HTTPException(401)
    return user
```

### Registration flow (Task 2.3)
```python
# PATTERN: 1 endpoint, 3 steps combined
# GOTCHA: Creer user Supabase PUIS notre user+company, rollback si echec
async def register(data: RegisterRequest):
    # 1. Creer user dans Supabase Auth
    supabase_user = await supabase_admin.auth.create_user(email=data.email, password=data.password)

    # 2. Creer company dans notre DB
    company_id = await db.execute("INSERT INTO companies ...")

    # 3. Creer user dans notre DB (lie a supabase_uid + company_id)
    user_id = await db.execute("INSERT INTO users ...")

    # 4. Creer ticket automatique depuis les besoins
    if data.needs_description:
        ticket = await create_ticket(company_id, user_id, data)

    # 5. Email de bienvenue
    await email_service.welcome(user, company)

    return {"user_id": user_id, "company_id": company_id, "ticket": ticket}
```

### WebSocket chat (Task 2.7)
```python
# PATTERN: Meme pipeline que telegram_bot.py
# GOTCHA: Auth dans le WebSocket handshake (query param ou first message)
@app.websocket("/ws/chat")
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    # Auth: premier message = JWT token
    token_msg = await ws.receive_text()
    user = verify_token(token_msg)

    while True:
        data = await ws.receive_json()
        # Pipeline identique au Telegram handler
        message = IncomingMessage(
            channel=Channel.WEB,
            client_id=user.company_id,
            sender_id=user.id,
            text=data["text"],
        )
        response = await agent.handle_message(message)
        await ws.send_json({"text": response.text, "skill": response.skill_used})
```

### Stripe Checkout (Task 2.5)
```python
# GOTCHA: Stripe en mode test d'abord (sk_test_...)
# GOTCHA: Subsides = reduction manuelle (pas Stripe coupon)
import stripe

async def create_checkout(company_id: str, pack: str, tier: str):
    company = await get_company(company_id)
    price_id = PACK_PRICES[pack][tier]  # mapping pack+tier -> Stripe Price ID

    session = stripe.checkout.Session.create(
        customer_email=company.contact_email,
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription" if tier != "gps" else "payment",
        success_url=f"{FRONTEND_URL}/dashboard/billing?success=true",
        cancel_url=f"{FRONTEND_URL}/dashboard/billing?canceled=true",
        metadata={"company_id": company_id, "pack": pack, "tier": tier},
    )
    return {"checkout_url": session.url}
```

## Validation Loop

### Niveau 1 : Structure & Syntax
```bash
# Backend
ls R2D2-Agent/src/gateway/auth.py
ls R2D2-Agent/src/gateway/clients.py
ls R2D2-Agent/src/gateway/tickets.py
ls R2D2-Agent/src/gateway/billing.py
ls R2D2-Agent/src/gateway/email_service.py
ls R2D2-Agent/src/channels/web_channel.py
ls R2D2-Agent/sql/*.sql

# Frontend
ls R2D2-Agent/frontend/package.json
ls R2D2-Agent/frontend/src/app/page.tsx
ls R2D2-Agent/frontend/src/app/login/page.tsx
ls R2D2-Agent/frontend/src/app/register/page.tsx
ls R2D2-Agent/frontend/src/app/dashboard/page.tsx
ls R2D2-Agent/frontend/src/app/dashboard/tickets/page.tsx
ls R2D2-Agent/frontend/src/app/dashboard/ai/page.tsx
ls R2D2-Agent/frontend/src/app/dashboard/billing/page.tsx

# Docker
ls R2D2-Agent/deploy/docker-compose.yml
ls R2D2-Agent/deploy/nginx.conf
ls R2D2-Agent/frontend/Dockerfile
```

### Niveau 2 : Fonctionnel
```bash
# Backend compile
cd R2D2-Agent && pip install -e . && python -c "from src.gateway.app import app; print('OK')"

# Frontend build
cd R2D2-Agent/frontend && npm run build

# SQL valid
cat R2D2-Agent/sql/*.sql | head -5  # pas d'erreur de syntaxe

# Docker build
cd R2D2-Agent && docker compose -f deploy/docker-compose.yml config
```

### Niveau 3 : Integration
```bash
# API healthcheck
curl http://localhost:8030/healthz

# Frontend accessible
curl http://localhost:3000

# Auth flow
curl -X POST http://localhost:8030/api/register -d '...'

# Stripe webhook
stripe listen --forward-to localhost:8030/api/billing/webhook
```

## Checklist de validation finale
- [ ] SQL migrations executees sans erreur sur PostgreSQL VM 104
- [ ] Backend FastAPI demarre avec toutes les nouvelles routes
- [ ] Frontend Next.js build et sert les 10 pages
- [ ] Inscription 3 etapes fonctionne (Supabase + DB + ticket auto)
- [ ] Login/logout via Supabase Auth
- [ ] Dashboard affiche les vrais donnees (tickets, usage, status)
- [ ] Chat IA fonctionne via WebSocket
- [ ] Ticketing complet (create, list, view, respond, evaluate)
- [ ] Stripe Checkout redirige correctement
- [ ] Emails envoyes (au moins en log si pas de SMTP)
- [ ] FR/NL/EN switch fonctionne
- [ ] Docker compose up lance tous les services
- [ ] Nginx route correctement (/, /api, /ws)
- [ ] Bot Telegram toujours fonctionnel (pas de regression)
- [ ] CORS restrictif (frontend URL seulement)
- [ ] Pas de credentials hardcodes

## Ordre d'execution recommande

```
Phase 1 (SQL)     ████████░░  2 sessions
Phase 2 (Backend) ████████████████░░  4 sessions
Phase 3 (Frontend)████████████████████████░░  6 sessions
Phase 4 (DevOps)  ████████░░  2 sessions
Phase 5 (Integr.) ████░░  1 session
                                        Total: ~15 sessions
```

IMPORTANT : Chaque phase est testable independamment.
On peut deployer Phase 1+2 et tester avec curl avant de toucher au frontend.

## Anti-Patterns a eviter
- Ne PAS utiliser un ORM lourd (SQLAlchemy) - rester sur asyncpg raw (meme pattern que audit.py)
- Ne PAS creer un monolithe frontend - chaque page est un Server Component independant
- Ne PAS hardcoder les prix Stripe - les mettre dans la config/DB
- Ne PAS toucher au bot Telegram existant - il continue de tourner en parallele
- Ne PAS deployer sur les VMs sans backup prealable
- Ne PAS oublier les RLS policies Supabase (securite multi-tenant)
- Ne PAS creer de fichiers .env avec des vraies credentials dans le repo

---

## Score de confiance : 8/10

Points forts :
- Infrastructure existante solide (Supabase, PostgreSQL, LiteLLM deja deployes)
- Specs UI detaillees (724 lignes de wireframes)
- Backend existant bien structure et extensible
- Catalogue commercial complet

Risques :
- Stripe integration necessite des cles et config (dependance externe)
- SMTP peut necessiter un service tiers (SendGrid, etc.)
- Le front Next.js est le plus gros morceau (6 sessions)
- Coordination multi-VM necessite des tests d'integration
