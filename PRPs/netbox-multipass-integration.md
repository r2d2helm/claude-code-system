# PRP: Integration de NetBox dans le stack MultiPass Agency

## Goal

Deployer NetBox v4.5.2 comme composant infrastructure dans le stack Docker MultiPass sur la VM Proxmox (VMID 100, 192.168.1.161), pour servir de **source de verite unique** de l'infrastructure reseau et des deployements clients. L'integration comprend le deploiement Docker, la modelisation de l'infra existante (14 containers, plan IP), l'exposition API via Kong, la creation d'un LangChain tool pour l'Agent Technique, le multi-tenancy client, et les webhooks d'automation.

## Why

- **Chaos d'inventaire** : L'infra MultiPass (14 containers, ports, IPs, services) n'est documentee que dans des notes Obsidian statiques (`C_MultiPass-Stack.md`). Aucune source de verite dynamique ni API interrogeable par les agents.
- **Provisioning manuel** : Chaque nouveau client Enterprise necessite une allocation manuelle d'IPs, de ports, de VMs. Aucun outil de planification de capacite.
- **Agents aveugles** : L'Agent Technique (Docker Manager, Ubuntu SysAdmin, Database Admin) n'a pas de visibilite temps reel sur l'etat de l'infrastructure. Il ne peut pas repondre a "quelles IPs sont disponibles ?" ou "quel container tourne sur quel port ?".
- **Offre Enterprise credible** : Les clients Enterprise (pricing custom) s'attendent a un SLA 99.9%, des audits de securite, et une documentation d'infrastructure. NetBox fournit tout cela nativement.
- **Synergie stack** : NetBox utilise PostgreSQL + Redis, deja dans le stack. Le deploiement Docker est natif. L'API REST s'integre naturellement via Kong et LangChain.

## What

### Comportement attendu

**Phase 1 - Deploiement** :
1. NetBox deploye en 4 containers Docker (app, worker, postgresql-netbox, redis-cache-netbox) integres au docker-compose MultiPass
2. Accessible via Kong sur `/netbox/` (UI) et `/api/netbox/` (API)
3. Infrastructure existante modelisee : VM Proxmox, 14 containers, services, ports, plan IP 192.168.1.0/24

**Phase 2 - Integration agents** :
4. LangChain tool `NetBoxTool` permettant aux agents d'interroger et modifier NetBox via l'API REST
5. L'Agent Technique utilise NetBoxTool pour : inventaire, allocation IP, verification disponibilite, documentation auto

**Phase 3 - Multi-tenancy** :
6. Chaque client (Starter/Business/Enterprise) a un Tenant NetBox isole
7. Prefixes IP, devices et services associes au bon Tenant
8. Dashboard client genere depuis les donnees NetBox

**Phase 4 - Automation** :
9. Webhooks NetBox declenchent des evenements dans le pipeline MultiPass
10. Agent Analytics consomme les donnees infra NetBox pour les rapports

### Success Criteria

- [ ] 4 containers NetBox deployés et healthy (app, worker, postgres-netbox, redis-netbox)
- [ ] NetBox UI accessible via Kong sur `http://192.168.1.161:8000/netbox/`
- [ ] API REST accessible via Kong sur `http://192.168.1.161:8000/api/netbox/`
- [ ] Token API v2 cree avec API_TOKEN_PEPPERS configure
- [ ] Infrastructure actuelle modelisee : 1 Site, 1 Rack virtuel, 14+ Services, plan IP documente
- [ ] LangChain tool `NetBoxTool` fonctionnel avec 6 operations (list_devices, get_ip_availability, create_service, get_device_details, list_prefixes, search)
- [ ] Agent Technique peut repondre a "quelles IPs sont disponibles sur 192.168.1.0/24 ?"
- [ ] Tenants NetBox crees pour isolation client (au moins 1 tenant "MultiPass Internal")
- [ ] Webhook configure pour notifier le pipeline MultiPass lors de creation/modification d'objets
- [ ] Docker-compose existant non casse (regression zero sur les 14 containers)
- [ ] Script de seed initial popule les donnees existantes via API bulk
- [ ] Documentation vault mise a jour avec note `C_NetBox-Integration.md`

## Contexte necessaire

### Documentation & References

```yaml
# MUST READ - Contexte a charger

- file: C:\Users\r2d2\Documents\Knowledge\Concepts\C_MultiPass-Stack.md
  why: "Inventaire actuel des 14 containers Docker avec ports, RAM, images - DONNEES A IMPORTER dans NetBox"

- file: C:\Users\r2d2\Documents\Knowledge\Projets\MultiPass\MultiPass Resources\Agents MultiPass\ARCHITECTURE.md
  why: "Hierarchie des agents - comprendre comment l'Agent Technique et ses sub-agents utiliseront NetBox"

- file: C:\Users\r2d2\Documents\Knowledge\Projets\MultiPass\MultiPass Resources\Agents MultiPass\docker-manager.md
  why: "Patterns Docker du sub-agent Docker Manager - docker-compose, healthchecks, volumes"

- file: C:\Users\r2d2\Documents\Knowledge\Projets\MultiPass\MultiPass Resources\Agents MultiPass\database-admin.md
  why: "Configuration PostgreSQL existante (pgvector, pg_hba.conf) - pour configurer la DB NetBox"

- file: C:\Users\r2d2\Documents\Repos\netbox\netbox\netbox\settings.py
  why: "Settings NetBox - comprendre les parametres requis (ALLOWED_HOSTS, SECRET_KEY, REDIS, DATABASE)"

- file: C:\Users\r2d2\Documents\Repos\netbox\netbox\netbox\urls.py
  why: "Structure URL NetBox - pour configurer le proxy Kong correctement"

- file: C:\Users\r2d2\Documents\Repos\netbox\base_requirements.txt
  why: "Dependances NetBox - confirmer compatibilite PostgreSQL 16+, Redis 7+"

- url: https://github.com/netbox-community/netbox-docker
  why: "Reference officielle netbox-docker - docker-compose.yml, env vars, volumes"

- url: https://docs.netbox.dev/en/stable/integrations/rest-api/
  why: "Documentation API REST - endpoints, authentication, filtering, pagination"

- url: https://python.langchain.com/docs/how_to/custom_tools/
  why: "Creation de custom tools LangChain - pattern pour NetBoxTool"

- vault: "[[C_MultiPass-Stack]]"
  why: "Architecture actuelle a modeliser dans NetBox"

- vault: "[[C_Proxmox-VE]]"
  why: "Infrastructure Proxmox sous-jacente"
```

### Architecture actuelle (avant integration)

```
VM r2d2automaker (192.168.1.161) - Ubuntu 24.04 - Proxmox VMID 100
│
├── Docker Network: multipass-network
│   ├── multipass-nextjs          :3000   (frontend)
│   ├── multipass-supabase-studio :3001   (db admin)
│   ├── multipass-langfuse        :3002   (llm observability)
│   ├── multipass-litellm         :4000   (llm proxy)
│   ├── multipass-supabase-kong   :8000   (api gateway)
│   ├── multipass-supabase-db     :5432   (postgresql pgvector)
│   ├── multipass-redis           :6379   (cache/sessions)
│   ├── multipass-supabase-rest   interne (postgrest)
│   ├── multipass-supabase-realtime interne
│   ├── multipass-supabase-storage interne
│   ├── multipass-supabase-auth   interne
│   ├── multipass-supabase-meta   interne
│   ├── multipass-supabase-imgproxy interne
│   └── multipass-langfuse-db     interne (postgres langfuse)
│
├── RAM utilisee: ~5.9 Go / 60.5 Go (9.7%)
└── Ports exposes: 3000-3002, 4000, 5432, 6379, 8000, 8443
```

### Architecture cible (apres integration)

```
VM r2d2automaker (192.168.1.161) - Ubuntu 24.04 - Proxmox VMID 100
│
├── Docker Network: multipass-network
│   ├── [14 containers existants INCHANGES]
│   │
│   ├── netbox                    :8080   (NetBox app via gunicorn)
│   ├── netbox-worker             interne (RQ background worker)
│   ├── netbox-postgres           :5433   (PostgreSQL dedie NetBox)
│   └── netbox-redis              interne (Redis dedie NetBox, DB 0=tasks, DB 1=cache)
│
├── Kong Routes additionnelles:
│   ├── /netbox/*     -> netbox:8080      (UI)
│   └── /api/netbox/* -> netbox:8080/api/ (API REST)
│
├── RAM estimee: ~7.5 Go / 60.5 Go (~12.4%)
└── Nouveaux ports: 5433 (postgres-netbox), 8080 (netbox ui)
```

### Gotchas connus

```
# CRITICAL: NetBox requiert PostgreSQL 13+ avec extension hstore - utiliser une instance DEDIEE (port 5433)
#   Ne PAS partager la DB Supabase (risque de conflit migrations, isolation donnees)
# CRITICAL: NetBox Redis a besoin de 2 databases (tasks + cache) - Redis dedie ou DB numbers separes
# CRITICAL: SECRET_KEY doit avoir 50+ caracteres - generer avec: python3 -c "import secrets; print(secrets.token_urlsafe(64))"
# CRITICAL: API_TOKEN_PEPPERS requis pour tokens v2 - format: {"v1": "random-string-64-chars"}
# CRITICAL: ALLOWED_HOSTS doit inclure le hostname du container ET l'IP de Kong
# CRITICAL: BASE_PATH = "netbox/" si proxy derriere Kong avec prefixe
# CRITICAL: CORS_ORIGIN_WHITELIST doit inclure http://192.168.1.161:3000 (frontend Next.js)
# CRITICAL: Docker netbox-docker utilise des volumes nommes - les declarer dans le compose
# CRITICAL: Le worker NetBox partage la meme config que l'app (meme image, meme volumes)
# CRITICAL: La premiere execution fait les migrations automatiquement - attendre ~2min au premier start
# CRITICAL: Creer le superuser via: docker exec -it netbox python manage.py createsuperuser
# GOTCHA: Kong doit strip le prefix /netbox/ avant de forwarder au container
# GOTCHA: Les fichiers de configuration NetBox sont dans /etc/netbox/config/ dans le container
# GOTCHA: Le healthcheck NetBox attend /login/ pas /api/ (redirect si LOGIN_REQUIRED=True)
```

## Implementation Blueprint

### Structure des fichiers a creer/modifier

```yaml
# === SUR LA VM (192.168.1.161) via SSH ===

Fichier 1:
  path: /opt/multipass/docker/netbox/docker-compose.netbox.yml
  role: "Docker Compose pour les 4 containers NetBox (extension du compose principal)"
  pattern: "docker-compose existant MultiPass + reference netbox-docker officiel"

Fichier 2:
  path: /opt/multipass/docker/netbox/env/netbox.env
  role: "Variables d'environnement NetBox (DB, Redis, secret key, allowed hosts)"
  pattern: "netbox-docker .env template"

Fichier 3:
  path: /opt/multipass/docker/netbox/env/postgres-netbox.env
  role: "Variables PostgreSQL dedie NetBox"

Fichier 4:
  path: /opt/multipass/docker/netbox/configuration/configuration.py
  role: "Configuration Python NetBox (settings override)"
  pattern: "netbox/netbox/configuration_example.py"

Fichier 5:
  path: /opt/multipass/docker/netbox/scripts/seed_infrastructure.py
  role: "Script Python pour peupler NetBox avec l'infra existante via API REST"
  pattern: "API bulk create NetBox"

Fichier 6:
  path: /opt/multipass/docker/netbox/scripts/setup_kong_routes.sh
  role: "Script pour configurer les routes Kong vers NetBox"
  pattern: "Kong Admin API (curl)"

# === CODE MULTIPASS (agents) ===

Fichier 7:
  path: /opt/multipass/app/agents/tools/netbox_tool.py
  role: "LangChain custom tool pour l'Agent Technique"
  pattern: "LangChain BaseTool + requests vers API REST NetBox"

Fichier 8:
  path: /opt/multipass/app/agents/tools/netbox_client.py
  role: "Client Python wrapper pour l'API REST NetBox"
  pattern: "requests + dataclasses"

# === VAULT OBSIDIAN (documentation) ===

Fichier 9:
  path: C:\Users\r2d2\Documents\Knowledge\Concepts\C_NetBox-Integration.md
  role: "Note concept vault documentant l'integration"
  pattern: "C_MultiPass-Stack.md (meme structure)"

Fichier 10 (MODIFIE):
  path: C:\Users\r2d2\Documents\Knowledge\Concepts\C_MultiPass-Stack.md
  role: "Ajouter NetBox dans l'architecture documentee"
```

### Liste des taches ordonnees

```yaml
# =============================================
# PHASE 1 : DEPLOIEMENT NETBOX (Taches 1-8)
# =============================================

Task 1:
  action: CREATE
  path: /opt/multipass/docker/netbox/env/postgres-netbox.env
  description: |
    Variables d'environnement PostgreSQL dedie NetBox.
    POSTGRES_USER=netbox
    POSTGRES_PASSWORD=[generer mot de passe fort]
    POSTGRES_DB=netbox
  ssh: true

Task 2:
  action: CREATE
  path: /opt/multipass/docker/netbox/env/netbox.env
  description: |
    Variables d'environnement NetBox.
    Generer SECRET_KEY (50+ chars) et API_TOKEN_PEPPERS.
    Configurer:
    - DB_HOST=netbox-postgres, DB_PORT=5432, DB_NAME=netbox
    - REDIS_HOST=netbox-redis, REDIS_PORT=6379
    - ALLOWED_HOSTS=*, localhost, netbox, 192.168.1.161
    - CORS_ORIGIN_WHITELIST=http://192.168.1.161:3000
    - LOGIN_REQUIRED=true
    - BASE_PATH=netbox/
    - SUPERUSER_NAME=admin
    - SUPERUSER_EMAIL=r2d2helm@gmail.com
    - SUPERUSER_PASSWORD=[generer]
  ssh: true

Task 3:
  action: CREATE
  path: /opt/multipass/docker/netbox/configuration/configuration.py
  description: |
    Fichier configuration.py NetBox.
    Override les settings par defaut:
    - ALLOWED_HOSTS
    - DATABASE (pointant vers netbox-postgres)
    - REDIS (pointant vers netbox-redis, DB 0=tasks, DB 1=cache)
    - SECRET_KEY (depuis env var)
    - API_TOKEN_PEPPERS (depuis env var)
    - BASE_PATH = 'netbox/'
    - CORS_ORIGIN_WHITELIST
    - LOGIN_REQUIRED = True
    - TIME_ZONE = 'Europe/Paris'
    - DEFAULT_LANGUAGE = 'fr-fr'
  pattern: |
    Voir netbox/netbox/configuration_example.py dans le repo clone
    C:\Users\r2d2\Documents\Repos\netbox\netbox\netbox\
  ssh: true

Task 4:
  action: CREATE
  path: /opt/multipass/docker/netbox/docker-compose.netbox.yml
  description: |
    Docker Compose pour NetBox (4 services).
    IMPORTANT: Utiliser extends ou merge avec le compose principal.

    Services:
    1. netbox-postgres:
       - image: postgres:17-alpine
       - env_file: env/postgres-netbox.env
       - volumes: netbox-postgres-data:/var/lib/postgresql/data
       - port: 5433:5432
       - healthcheck: pg_isready -U netbox
       - networks: multipass-network

    2. netbox-redis:
       - image: valkey/valkey:9.0-alpine
       - command: valkey-server --appendonly yes --requirepass [password]
       - volumes: netbox-redis-data:/data
       - networks: multipass-network
       - healthcheck: valkey-cli ping

    3. netbox:
       - image: netboxcommunity/netbox:v4.5-4.0.0
       - env_file: env/netbox.env
       - depends_on: netbox-postgres (healthy), netbox-redis (healthy)
       - volumes:
           - ./configuration:/etc/netbox/config:ro
           - netbox-media:/opt/netbox/netbox/media
           - netbox-reports:/opt/netbox/netbox/reports
           - netbox-scripts:/opt/netbox/netbox/scripts
       - ports: 8080:8080
       - healthcheck: curl -f http://localhost:8080/netbox/login/ || exit 1
       - networks: multipass-network
       - restart: unless-stopped

    4. netbox-worker:
       - image: netboxcommunity/netbox:v4.5-4.0.0
       - command: /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py rqworker high default low
       - env_file: env/netbox.env
       - depends_on: netbox (healthy)
       - volumes: (memes que netbox)
       - networks: multipass-network
       - restart: unless-stopped

    Volumes nommes:
    - netbox-postgres-data
    - netbox-redis-data
    - netbox-media
    - netbox-reports
    - netbox-scripts

    Network:
    - multipass-network (external: true)
  pattern: "Reference: https://github.com/netbox-community/netbox-docker/blob/release/docker-compose.yml"
  ssh: true

Task 5:
  action: EXECUTE
  description: |
    Deployer NetBox via SSH sur la VM.
    Commandes:
    ```bash
    ssh r2d2helm@192.168.1.161
    cd /opt/multipass/docker/netbox
    docker compose -f docker-compose.netbox.yml up -d
    # Attendre ~2-3 min pour migrations initiales
    docker compose -f docker-compose.netbox.yml ps
    # Verifier que tous les containers sont healthy
    docker logs netbox 2>&1 | tail -20
    ```
  validation: "Tous les 4 containers en status 'healthy' ou 'running'"
  ssh: true

Task 6:
  action: CREATE
  path: /opt/multipass/docker/netbox/scripts/setup_kong_routes.sh
  description: |
    Script pour configurer 2 routes Kong:
    1. Route UI: /netbox/* -> netbox:8080
    2. Route API: /api/netbox/* -> netbox:8080/api/

    Utiliser l'API Admin Kong (port 8001 interne):
    ```bash
    # Service NetBox
    curl -i -X POST http://multipass-supabase-kong:8001/services/ \
      --data "name=netbox" \
      --data "url=http://netbox:8080"

    # Route UI
    curl -i -X POST http://multipass-supabase-kong:8001/services/netbox/routes \
      --data "name=netbox-ui" \
      --data "paths[]=/netbox" \
      --data "strip_path=false"

    # Route API (strip /api/netbox -> /api)
    curl -i -X POST http://multipass-supabase-kong:8001/services/netbox/routes \
      --data "name=netbox-api" \
      --data "paths[]=/api/netbox" \
      --data "strip_path=true"

    # Rate limiting plugin
    curl -i -X POST http://multipass-supabase-kong:8001/services/netbox/plugins \
      --data "name=rate-limiting" \
      --data "config.minute=60" \
      --data "config.policy=local"
    ```
  ssh: true

Task 7:
  action: EXECUTE
  description: |
    Executer le script de configuration Kong et verifier.
    ```bash
    bash /opt/multipass/docker/netbox/scripts/setup_kong_routes.sh
    # Tester l'acces via Kong
    curl -s http://192.168.1.161:8000/netbox/login/ | head -5
    curl -s http://192.168.1.161:8000/api/netbox/ -H "Authorization: Token xxx"
    ```
  validation: "HTTP 200 sur /netbox/login/ et /api/netbox/"
  ssh: true

Task 8:
  action: CREATE
  path: /opt/multipass/docker/netbox/scripts/seed_infrastructure.py
  description: |
    Script Python pour peupler NetBox avec l'infra existante.
    Utilise l'API REST NetBox (requests + token).

    Donnees a creer (dans cet ordre pour respecter les FK):

    1. Tenant: "MultiPass Internal"
    2. Site: "Homelab r2d2" (physical_address="Local", time_zone="Europe/Paris")
    3. Rack: "VM-100-Rack" (site=Homelab, type=virtual)
    4. Manufacturer: "Proxmox"
    5. DeviceType: "VM Ubuntu 24.04" (manufacturer=Proxmox, u_height=0)
    6. DeviceRole: "Application Server"
    7. Device: "r2d2automaker" (device_type=VM, role=AppServer, site=Homelab, tenant=MultiPass)
       custom_fields: { vmid: 100, ip: "192.168.1.161", os: "Ubuntu 24.04.3 LTS", ram_gb: 60.5 }
    8. Prefix: "192.168.1.0/24" (site=Homelab, description="LAN Homelab")
    9. IPAddress: "192.168.1.161/24" (assigned_object=r2d2automaker, tenant=MultiPass)

    10. Services (14 containers comme Services sur le Device):
        | Nom | Protocol | Port | Description |
        |-----|----------|------|-------------|
        | multipass-nextjs | TCP | 3000 | Next.js frontend |
        | multipass-supabase-studio | TCP | 3001 | Supabase Studio |
        | multipass-langfuse | TCP | 3002 | Langfuse observability |
        | multipass-litellm | TCP | 4000 | LiteLLM proxy |
        | multipass-kong | TCP | 8000 | Kong API Gateway |
        | multipass-kong-ssl | TCP | 8443 | Kong HTTPS |
        | multipass-postgres | TCP | 5432 | PostgreSQL pgvector |
        | multipass-redis | TCP | 6379 | Redis cache |
        | netbox | TCP | 8080 | NetBox DCIM/IPAM |
        | netbox-postgres | TCP | 5433 | PostgreSQL NetBox |

    11. Services internes (sans port expose):
        | Nom | Description |
        |-----|-------------|
        | multipass-supabase-rest | PostgREST API |
        | multipass-supabase-realtime | Supabase Realtime |
        | multipass-supabase-storage | Supabase Storage |
        | multipass-supabase-auth | Supabase GoTrue Auth |
        | multipass-supabase-meta | Postgres Meta |
        | multipass-supabase-imgproxy | Image Proxy |
        | multipass-langfuse-db | PostgreSQL Langfuse |
        | netbox-worker | NetBox RQ Worker |
        | netbox-redis | Valkey Cache NetBox |
  pattern: |
    Utiliser l'API REST NetBox:
    POST /api/dcim/sites/ { name, slug, ... }
    POST /api/dcim/devices/ { name, device_type, role, site, ... }
    POST /api/ipam/prefixes/ { prefix, site, ... }
    POST /api/ipam/services/ { device, name, ports, protocol, ... }
    Headers: Authorization: Token {api_token}, Content-Type: application/json
  ssh: true

# =============================================
# PHASE 2 : INTEGRATION AGENTS (Taches 9-12)
# =============================================

Task 9:
  action: CREATE
  path: /opt/multipass/app/agents/tools/netbox_client.py
  description: |
    Client Python pour l'API REST NetBox.
    Classe NetBoxClient avec:
    - __init__(base_url, token): configure session requests
    - list_devices(filters=None) -> list[dict]: GET /api/dcim/devices/
    - get_device(id) -> dict: GET /api/dcim/devices/{id}/
    - list_services(device_id=None) -> list[dict]: GET /api/ipam/services/
    - list_prefixes(site_id=None) -> list[dict]: GET /api/ipam/prefixes/
    - get_prefix_available_ips(prefix_id) -> list[dict]: GET /api/ipam/prefixes/{id}/available-ips/
    - list_ip_addresses(filters=None) -> list[dict]: GET /api/ipam/ip-addresses/
    - create_service(device_id, name, ports, protocol) -> dict: POST /api/ipam/services/
    - create_ip_address(address, tenant_id=None) -> dict: POST /api/ipam/ip-addresses/
    - search(query) -> list[dict]: GET /api/dcim/devices/?q=... (multi-endpoint)
    - list_tenants() -> list[dict]: GET /api/tenancy/tenants/

    Gestion d'erreurs: raise NetBoxAPIError avec message et status_code
    Pagination automatique: suivre next_url tant que non null
  pattern: "requests.Session + dataclasses + typing"

Task 10:
  action: CREATE
  path: /opt/multipass/app/agents/tools/netbox_tool.py
  description: |
    LangChain custom tool pour NetBox.
    Importe NetBoxClient.

    Classe NetBoxTool(BaseTool):
      name = "netbox_infrastructure"
      description = """Query and manage network infrastructure in NetBox.
      Use this tool to:
      - List devices, services, IP addresses
      - Check IP availability in a prefix
      - Create new services or IP allocations
      - Search infrastructure by name/keyword
      - Get device details with all interfaces and services

      Input format: JSON with 'action' and 'params' keys.
      Actions: list_devices, get_device, list_services, list_prefixes,
               get_ip_availability, create_service, create_ip, search, list_tenants
      """

      def _run(self, query: str) -> str:
          # Parse JSON input
          # Route to appropriate NetBoxClient method
          # Return formatted results as string

    Configuration:
      NETBOX_URL = os.getenv("NETBOX_URL", "http://netbox:8080")
      NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")
  pattern: |
    LangChain BaseTool pattern:
    from langchain.tools import BaseTool
    class MyTool(BaseTool):
        name: str = "tool_name"
        description: str = "..."
        def _run(self, query: str) -> str: ...

Task 11:
  action: MODIFY
  path: /opt/multipass/app/agents/technique.py (ou equivalent)
  description: |
    Ajouter NetBoxTool dans la liste des tools de l'Agent Technique.
    L'Agent Technique et ses sub-agents (Docker Manager, Ubuntu SysAdmin, Database Admin)
    doivent avoir acces au tool.

    Ajouter dans l'initialisation:
    from agents.tools.netbox_tool import NetBoxTool
    netbox_tool = NetBoxTool()
    tools = [...existing_tools, netbox_tool]

    Ajouter dans le system prompt de l'Agent Technique:
    "Tu as acces a NetBox, la source de verite de l'infrastructure.
    Utilise le tool netbox_infrastructure pour interroger l'etat de l'infra,
    verifier les IPs disponibles, documenter les nouveaux deployements."
  depends_on: [Task 10]

Task 12:
  action: MODIFY
  path: /opt/multipass/docker/.env (ou docker-compose principal)
  description: |
    Ajouter les variables d'environnement pour le NetBox tool:
    NETBOX_URL=http://netbox:8080
    NETBOX_TOKEN=[token genere dans NetBox]
    Ces vars doivent etre accessibles par le container des agents.
  depends_on: [Task 5]

# =============================================
# PHASE 3 : MULTI-TENANCY (Taches 13-14)
# =============================================

Task 13:
  action: EXECUTE
  description: |
    Configurer les tenants NetBox via API pour isoler les donnees client.
    Creer via le script seed ou manuellement:
    1. TenantGroup: "Clients MultiPass"
    2. Tenant: "MultiPass Internal" (groupe=Clients)
    3. Tenant: "Client Demo" (groupe=Clients) - pour les demonstrations
    Associer les objets existants au tenant "MultiPass Internal".
  depends_on: [Task 8]

Task 14:
  action: MODIFY
  path: /opt/multipass/app/agents/tools/netbox_tool.py
  description: |
    Ajouter le filtrage par tenant dans les operations.
    Quand un agent travaille pour un client specifique,
    filtrer automatiquement par tenant_id.
    Ajouter: list_tenant_devices(tenant_name), create_tenant(name, group)
  depends_on: [Task 13]

# =============================================
# PHASE 4 : AUTOMATION (Taches 15-17)
# =============================================

Task 15:
  action: CONFIGURE
  description: |
    Configurer un webhook NetBox qui notifie MultiPass.
    Via l'UI NetBox ou API:
    1. Creer un Webhook:
       - URL: http://multipass-nextjs:3000/api/webhooks/netbox
       - Content-Type: application/json
       - Events: create, update, delete
       - Object Types: Device, Service, IPAddress
    2. Creer un EventRule associe au webhook
  depends_on: [Task 5]

Task 16:
  action: CREATE
  path: /opt/multipass/app/api/webhooks/netbox.py (ou route Next.js)
  description: |
    Endpoint webhook pour recevoir les notifications NetBox.
    Parse le payload NetBox (model, event, data, snapshots).
    Actions possibles:
    - Notifier l'Agent Analytics pour mise a jour des dashboards
    - Logger dans Langfuse pour tracabilite
    - Alerter si un device passe en status "failed"
  depends_on: [Task 15]

Task 17:
  action: MODIFY
  path: /opt/multipass/app/agents/analytics.py (ou equivalent)
  description: |
    Ajouter NetBoxTool dans les tools de l'Agent Analytics.
    L'agent peut maintenant generer des rapports infra:
    - Utilisation des IPs par tenant
    - Inventaire des services par device
    - Croissance de l'infra dans le temps
  depends_on: [Task 10]

# =============================================
# PHASE 5 : DOCUMENTATION (Taches 18-19)
# =============================================

Task 18:
  action: CREATE
  path: C:\Users\r2d2\Documents\Knowledge\Concepts\C_NetBox-Integration.md
  description: |
    Note vault documentant l'integration NetBox.
    Frontmatter:
    ---
    title: "NetBox Integration MultiPass"
    date: 2026-02-13
    type: concept
    status: seedling
    tags:
      - projet/multipass
      - infra/netbox
      - dev/python
    related:
      - "[[C_MultiPass-Stack]]"
      - "[[C_Proxmox-VE]]"
    ---
    Contenu: architecture, endpoints, credentials reference, usage par les agents

Task 19:
  action: MODIFY
  path: C:\Users\r2d2\Documents\Knowledge\Concepts\C_MultiPass-Stack.md
  description: |
    Ajouter NetBox dans l'architecture documentee:
    - 4 nouveaux containers dans le tableau (netbox, netbox-worker, netbox-postgres, netbox-redis)
    - Nouveau port :8080 dans l'architecture
    - MAJ total RAM estime
    - Lien vers [[C_NetBox-Integration]]
```

### Pseudocode par tache critique

```python
# === Task 4: docker-compose.netbox.yml ===
# PATTERN: Suivre la structure netbox-docker officielle
# GOTCHA: Les volumes doivent etre declares comme 'volumes:' top-level
# GOTCHA: Le healthcheck doit inclure BASE_PATH (/netbox/login/)
# GOTCHA: Le worker n'a PAS de healthcheck sur HTTP, mais sur le process rqworker

services:
  netbox-postgres:
    image: postgres:17-alpine
    env_file: ./env/postgres-netbox.env
    volumes:
      - netbox-postgres-data:/var/lib/postgresql/data
    ports:
      - "5433:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U netbox"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s
    networks:
      - multipass-network
    restart: unless-stopped

  netbox-redis:
    image: valkey/valkey:9.0-alpine
    command: valkey-server --appendonly yes --requirepass ${NETBOX_REDIS_PASSWORD}
    volumes:
      - netbox-redis-data:/data
    healthcheck:
      test: ["CMD", "valkey-cli", "-a", "${NETBOX_REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - multipass-network
    restart: unless-stopped

  netbox:
    image: netboxcommunity/netbox:v4.5-4.0.0
    env_file: ./env/netbox.env
    depends_on:
      netbox-postgres:
        condition: service_healthy
      netbox-redis:
        condition: service_healthy
    volumes:
      - ./configuration:/etc/netbox/config:ro
      - netbox-media:/opt/netbox/netbox/media
      - netbox-reports:/opt/netbox/netbox/reports
      - netbox-scripts:/opt/netbox/netbox/scripts
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/netbox/login/"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 120s  # migrations initiales
    networks:
      - multipass-network
    restart: unless-stopped

  netbox-worker:
    image: netboxcommunity/netbox:v4.5-4.0.0
    command: /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py rqworker high default low
    env_file: ./env/netbox.env
    depends_on:
      netbox:
        condition: service_healthy
    volumes:
      - ./configuration:/etc/netbox/config:ro
      - netbox-media:/opt/netbox/netbox/media
      - netbox-reports:/opt/netbox/netbox/reports
      - netbox-scripts:/opt/netbox/netbox/scripts
    healthcheck:
      test: ["CMD-SHELL", "ps aux | grep -v grep | grep rqworker"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - multipass-network
    restart: unless-stopped

volumes:
  netbox-postgres-data:
    driver: local
  netbox-redis-data:
    driver: local
  netbox-media:
    driver: local
  netbox-reports:
    driver: local
  netbox-scripts:
    driver: local

networks:
  multipass-network:
    external: true
```

```python
# === Task 9: netbox_client.py ===
# PATTERN: requests.Session avec auth header persistent
# GOTCHA: Pagination NetBox retourne {"count":N,"next":"url","results":[...]}
# GOTCHA: Token v2 utilise "Bearer" prefix, Token v1 utilise "Token" prefix

import os
import requests
from dataclasses import dataclass
from typing import Optional

class NetBoxAPIError(Exception):
    def __init__(self, message, status_code=None):
        self.status_code = status_code
        super().__init__(message)

class NetBoxClient:
    def __init__(self, base_url=None, token=None):
        self.base_url = (base_url or os.getenv("NETBOX_URL", "http://netbox:8080")).rstrip("/")
        self.token = token or os.getenv("NETBOX_TOKEN")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _get(self, endpoint, params=None):
        """GET avec pagination automatique."""
        url = f"{self.base_url}/api/{endpoint.lstrip('/')}"
        results = []
        while url:
            resp = self.session.get(url, params=params)
            if resp.status_code != 200:
                raise NetBoxAPIError(resp.text, resp.status_code)
            data = resp.json()
            results.extend(data.get("results", [data]))
            url = data.get("next")
            params = None  # next URL inclut deja les params
        return results

    def _post(self, endpoint, payload):
        url = f"{self.base_url}/api/{endpoint.lstrip('/')}"
        resp = self.session.post(url, json=payload)
        if resp.status_code not in (200, 201):
            raise NetBoxAPIError(resp.text, resp.status_code)
        return resp.json()

    def list_devices(self, **filters):
        return self._get("dcim/devices/", params=filters)

    def get_device(self, device_id):
        return self._get(f"dcim/devices/{device_id}/")[0]

    def list_services(self, device_id=None):
        params = {"device_id": device_id} if device_id else {}
        return self._get("ipam/services/", params=params)

    def list_prefixes(self, site_id=None):
        params = {"site_id": site_id} if site_id else {}
        return self._get("ipam/prefixes/", params=params)

    def get_prefix_available_ips(self, prefix_id, limit=50):
        return self._get(f"ipam/prefixes/{prefix_id}/available-ips/", params={"limit": limit})

    def list_ip_addresses(self, **filters):
        return self._get("ipam/ip-addresses/", params=filters)

    def create_service(self, device_id, name, ports, protocol="tcp"):
        return self._post("ipam/services/", {
            "device": device_id, "name": name,
            "ports": ports, "protocol": protocol,
        })

    def create_ip_address(self, address, tenant_id=None, description=""):
        payload = {"address": address, "description": description}
        if tenant_id:
            payload["tenant"] = tenant_id
        return self._post("ipam/ip-addresses/", payload)

    def search(self, query):
        return self._get("dcim/devices/", params={"q": query})

    def list_tenants(self):
        return self._get("tenancy/tenants/")
```

```python
# === Task 10: netbox_tool.py ===
# PATTERN: LangChain BaseTool
# GOTCHA: _run() recoit un string, pas un dict - parser le JSON
# GOTCHA: Retourner un string formate, pas un dict

import json
from langchain.tools import BaseTool
from agents.tools.netbox_client import NetBoxClient, NetBoxAPIError

class NetBoxTool(BaseTool):
    name: str = "netbox_infrastructure"
    description: str = """Query and manage network infrastructure via NetBox API.

    Input: JSON string with 'action' and optional 'params'.

    Available actions:
    - list_devices: List all devices. Params: name, role, site, tenant (all optional)
    - get_device: Get device details. Params: id (required)
    - list_services: List services. Params: device_id (optional)
    - list_prefixes: List IP prefixes. Params: site_id (optional)
    - get_ip_availability: Get available IPs in prefix. Params: prefix_id (required)
    - create_service: Create a service. Params: device_id, name, ports[], protocol
    - create_ip: Allocate IP. Params: address, tenant_id, description
    - search: Search infrastructure. Params: query (required)
    - list_tenants: List all tenants. No params.

    Example: {"action": "get_ip_availability", "params": {"prefix_id": 1}}
    """

    def _run(self, query: str) -> str:
        try:
            data = json.loads(query)
            action = data.get("action")
            params = data.get("params", {})
            client = NetBoxClient()

            actions = {
                "list_devices": lambda: client.list_devices(**params),
                "get_device": lambda: client.get_device(params["id"]),
                "list_services": lambda: client.list_services(params.get("device_id")),
                "list_prefixes": lambda: client.list_prefixes(params.get("site_id")),
                "get_ip_availability": lambda: client.get_prefix_available_ips(params["prefix_id"]),
                "create_service": lambda: client.create_service(**params),
                "create_ip": lambda: client.create_ip_address(**params),
                "search": lambda: client.search(params["query"]),
                "list_tenants": lambda: client.list_tenants(),
            }

            if action not in actions:
                return f"Unknown action: {action}. Available: {list(actions.keys())}"

            result = actions[action]()
            return json.dumps(result, indent=2, default=str)

        except NetBoxAPIError as e:
            return f"NetBox API Error ({e.status_code}): {e}"
        except Exception as e:
            return f"Error: {e}"
```

### Points d'integration

```yaml
ROUTER:
  - Non applicable (pas un skill Claude Code, c'est une integration infra)

VAULT:
  - Creer: Knowledge/Concepts/C_NetBox-Integration.md
  - Modifier: Knowledge/Concepts/C_MultiPass-Stack.md (ajouter 4 containers)
  - Template: _Templates/Template-Concept.md
  - Tags: projet/multipass, infra/netbox, dev/python

MCP:
  - Impacte knowledge-assistant: oui (nouvelle note C_NetBox-Integration indexee)

CLAUDE.MD:
  - Non necessaire (pas de modification du systeme r2d2 Claude Code)
  - Optionnel: ajouter NetBox dans les "Chemins importants" si utilise frequemment
```

## Validation Loop

### Niveau 1 : Structure & Deploiement

```bash
# Verifier que les containers sont up (SSH sur la VM)
ssh r2d2helm@192.168.1.161 "docker ps --filter 'name=netbox' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
# Attendu: 4 containers (netbox, netbox-worker, netbox-postgres, netbox-redis)

# Verifier les healthchecks
ssh r2d2helm@192.168.1.161 "docker inspect --format='{{.Name}} {{.State.Health.Status}}' netbox netbox-postgres netbox-redis"
# Attendu: healthy pour les 3

# Verifier l'acces direct
ssh r2d2helm@192.168.1.161 "curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/netbox/login/"
# Attendu: 200

# Verifier l'acces via Kong
ssh r2d2helm@192.168.1.161 "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/netbox/login/"
# Attendu: 200
```

### Niveau 2 : Fonctionnel

```bash
# Generer un token API et tester l'API REST
NETBOX_TOKEN="..."  # Token genere dans l'UI NetBox

# Lister les devices
ssh r2d2helm@192.168.1.161 "curl -s http://localhost:8080/api/dcim/devices/ -H 'Authorization: Token ${NETBOX_TOKEN}' | python3 -m json.tool | head -20"
# Attendu: JSON avec le device r2d2automaker

# Verifier les IPs
ssh r2d2helm@192.168.1.161 "curl -s http://localhost:8080/api/ipam/ip-addresses/ -H 'Authorization: Token ${NETBOX_TOKEN}' | python3 -m json.tool | head -20"
# Attendu: JSON avec 192.168.1.161/24

# Verifier les services
ssh r2d2helm@192.168.1.161 "curl -s http://localhost:8080/api/ipam/services/ -H 'Authorization: Token ${NETBOX_TOKEN}' | python3 -m json.tool | head -20"
# Attendu: JSON avec les 14+ services documentes

# Verifier les prefixes
ssh r2d2helm@192.168.1.161 "curl -s 'http://localhost:8080/api/ipam/prefixes/1/available-ips/?limit=5' -H 'Authorization: Token ${NETBOX_TOKEN}' | python3 -m json.tool"
# Attendu: Liste d'IPs disponibles dans 192.168.1.0/24

# Tester le LangChain tool (si Python disponible sur la VM)
ssh r2d2helm@192.168.1.161 "cd /opt/multipass && python3 -c \"
from app.agents.tools.netbox_tool import NetBoxTool
tool = NetBoxTool()
result = tool._run('{\"action\": \"list_devices\"}')
print(result[:500])
\""
# Attendu: JSON des devices
```

### Niveau 3 : Integration

```bash
# Verifier que les 14 containers originaux sont toujours healthy
ssh r2d2helm@192.168.1.161 "docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -v netbox"
# Attendu: Tous les 14 containers originaux running

# Verifier la consommation RAM totale
ssh r2d2helm@192.168.1.161 "free -h | grep Mem"
# Attendu: < 10 Go utilises (avant: 5.9 Go, delta ~1.5 Go)

# Verifier les tenants
ssh r2d2helm@192.168.1.161 "curl -s http://localhost:8080/api/tenancy/tenants/ -H 'Authorization: Token ${NETBOX_TOKEN}' | python3 -m json.tool"
# Attendu: Tenant "MultiPass Internal" present

# Verifier le webhook (si configure)
ssh r2d2helm@192.168.1.161 "curl -s http://localhost:8080/api/extras/webhooks/ -H 'Authorization: Token ${NETBOX_TOKEN}' | python3 -m json.tool"
# Attendu: Webhook configure vers le pipeline MultiPass
```

```powershell
# Verification vault (depuis Windows)
Test-Path "C:\Users\r2d2\Documents\Knowledge\Concepts\C_NetBox-Integration.md"
# Attendu: True

# Verifier le frontmatter
Select-String -Path "C:\Users\r2d2\Documents\Knowledge\Concepts\C_NetBox-Integration.md" -Pattern "^---" | Measure-Object
# Attendu: Count = 2 (ouverture + fermeture)

# Verifier les wikilinks dans C_MultiPass-Stack
Select-String -Path "C:\Users\r2d2\Documents\Knowledge\Concepts\C_MultiPass-Stack.md" -Pattern "C_NetBox-Integration"
# Attendu: Match found
```

## Checklist de validation finale

- [ ] 4 containers NetBox deployed et healthy
- [ ] PostgreSQL dedie NetBox sur port 5433 (isole de Supabase)
- [ ] Redis dedie NetBox (ou DB numbers separes)
- [ ] Kong routes configurees (/netbox/ et /api/netbox/)
- [ ] API Token v2 genere avec API_TOKEN_PEPPERS
- [ ] Infrastructure modelisee: Site, Device, Prefix, IPs, 14+ Services
- [ ] Tenant "MultiPass Internal" cree et associe
- [ ] LangChain NetBoxTool fonctionnel avec 9 actions
- [ ] Agent Technique a acces au tool NetBox
- [ ] Webhook NetBox configure (optionnel Phase 4)
- [ ] 14 containers originaux non impactes (regression zero)
- [ ] RAM totale < 10 Go
- [ ] Note vault C_NetBox-Integration.md creee avec frontmatter
- [ ] Note C_MultiPass-Stack.md mise a jour
- [ ] Tous les fichiers en UTF-8 sans BOM

## Anti-Patterns a eviter

- Ne PAS partager la base PostgreSQL Supabase - utiliser une instance dediee
- Ne PAS exposer NetBox directement sur Internet - toujours derriere Kong
- Ne PAS hardcoder le token API dans le code - utiliser des variables d'environnement
- Ne PAS oublier le BASE_PATH quand NetBox est derriere un reverse proxy
- Ne PAS ignorer le start_period du healthcheck (migrations prennent 2+ min au premier demarrage)
- Ne PAS creer de volumes anonymes - toujours utiliser des volumes nommes
- Ne PAS oublier de declarer le network comme external si le compose NetBox est separe du compose principal

---

## Scoring

**Confiance implementation reussie en un seul passage : 8/10**

Points forts:
- Contexte exhaustif (stack existante, architecture agents, repo NetBox analyse)
- Pseudocode detaille pour les fichiers critiques (docker-compose, client, tool)
- Validations executables a chaque niveau
- Gotchas documentes (BASE_PATH, healthcheck, migrations, pagination)
- Phases progressives (deploy -> integrate -> multi-tenant -> automate)

Points d'incertitude:
- Configuration exacte de Kong (version 2.8.1 peut avoir des specificites pour le routing)
- Chemin exact du code agents MultiPass sur la VM (/opt/multipass/app/agents/ est une hypothese)
- Le format exact du docker-compose principal MultiPass n'a pas ete lu (merge vs compose multi-file)
- Variables d'environnement NetBox Docker peuvent varier entre versions
