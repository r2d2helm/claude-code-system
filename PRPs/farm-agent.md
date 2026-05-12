# PRP : Farm Agent — Agent IA Agricole Autonome Local

**Score de confiance : 8/10**
**Complexite : Haute (multi-composant, multi-hardware)**
**Duree estimee : 4 phases sur 3 semaines**

---

## Goal

Transformer le POC llamafile (chat passif valide le 7 avril 2026) en un **agent IA autonome local** deployable sur hardware low-cost (i3 + GPU, ~350 EUR) pour cooperatives agricoles. L'agent combine LLM local + base de donnees + vault de connaissances + tool calling pour fournir des reponses personnalisees a chaque ferme, 100% offline.

## Why

- **Le POC est valide** : Qwen3-4B tourne en 30-120 sec/reponse sur CPU, multilingue, interface web integree
- **Gap critique** : le chatbot generique ne connait pas LA ferme — pas de memoire, pas de contexte local
- **Differenciateur UNDP (27 avril)** : "agent qui connait votre ferme" vs "chatbot generique"
- **Distribution virale** : un setup copiable de cooperative en cooperative
- **Convergence LivestockAI** : le codebase existant a deja 44 fichiers AI (sentinel, chat, memory, actions) — on reutilise
- **Souverainete** : zero cloud, zero abonnement, donnees locales, modele europeen (EuroLLM) ou multiligue (Qwen3)

## What

### Tiers de deploiement

| Tier | Hardware | Composants | Temps reponse |
|------|----------|-----------|---------------|
| **T0 — USB Stick** | N'importe quel PC 4Go RAM | Llamafile + chat | 30-120 sec |
| **T1 — Farm Agent** | i3 + GPU + 16Go RAM | Llamafile + SQLite + vault + agent loop | 5-15 sec |
| **T2 — Coop Hub** | T1 + WiFi router + capteurs | T1 + multi-users + mesh LoRa + sync | 5-15 sec |

### Success Criteria

- [ ] T0 : Llamafile avec system prompt agricole, DEMARRER.bat, README 6 langues — **DONE (7 avril)**
- [ ] T1 : Agent loop fonctionnel avec 4 outils (query_db, search_vault, write_journal, calculate)
- [ ] T1 : SQLite schema pour parcelles/recoltes/cooperateurs avec seed data demo
- [ ] T1 : Vault agricole avec 20+ fiches (cultures, maladies, traitements bio)
- [ ] T1 : GPU offload fonctionnel (CUDA ou Vulkan) = < 15 sec/reponse
- [ ] T1 : Script d'installation one-liner (Linux)
- [ ] T2 : Multi-users via WiFi local (--host 0.0.0.0 + --slots)
- [ ] T2 : Sync API vers Eco-Systemes (push observations, pull fiches)
- [ ] Demo UNDP : T1 fonctionnel avec scenario complet (question → agent query DB + vault → reponse personnalisee)

## Contexte necessaire

### Documentation & References
```yaml
- file: C:\Users\r2d2\Projects\farm-assistant\
  why: POC valide (llamafile, DEMARRER.bat, README)

- file: C:\Users\r2d2\Projects\multipass-farmsystems\app\features\ai\
  why: 44 fichiers AI existants — sentinel, chat, memory, actions, thread, domain-knowledge

- file: C:\Users\r2d2\Projects\multipass-farmsystems\app\features\ai\chat-service.ts
  why: Pattern de chat service existant a adapter pour local

- file: C:\Users\r2d2\Projects\multipass-farmsystems\app\features\ai\action-executor.ts
  why: Pattern d'execution d'actions/outils par l'IA

- file: C:\Users\r2d2\Projects\multipass-farmsystems\app\features\ai\memory-service.ts
  why: Pattern de memoire persistante pour l'agent

- file: C:\Users\r2d2\Projects\multipass-farmsystems\app\features\ai\domain-knowledge-service.ts
  why: Pattern de base de connaissances domaine

- file: C:\Users\r2d2\Projects\multipass-farmsystems\app\features\ai\sentinel-service.ts
  why: Pattern monitoring/alertes intelligent

- url: https://github.com/mozilla-ai/llamafile
  why: API serveur, flags, mode --server, OpenAI-compatible endpoints

- url: https://github.com/kessler/gemma-gem
  why: Boucle agent decouplee en 5 fichiers TS (agent-loop, prompt-builder, tool-parser, types, index)

- url: https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md
  why: Function calling / tool use avec llama.cpp (Qwen3 supporte les tools nativement)

- vault: Knowledge/References/2026-04-07_Veille-Korben-42j.md
  why: Opportunites identifiees (Meshtastic, Reticulum, EuroLLM, Promptfoo)
```

### Arbre actuel
```
Projects/
├── farm-assistant/              # POC T0 (DONE)
│   ├── Qwen_Qwen3-4B-Q4_K_M.llamafile
│   ├── Qwen_Qwen3-4B-Q4_K_M.exe
│   ├── DEMARRER.bat
│   ├── start.sh
│   └── README.txt
│
└── multipass-farmsystems/       # LivestockAI (codebase existant)
    └── app/features/ai/         # 44 fichiers AI reutilisables
```

### Arbre souhaite (T1 Farm Agent)
```
Projects/farm-agent/
├── README.md                    # Documentation complete
├── install.sh                   # Installation one-liner Linux
├── install.bat                  # Installation Windows
│
├── models/                      # Modeles LLM
│   └── .gitkeep                 # Qwen3-4B.gguf telecharge par install.sh
│
├── vault/                       # Connaissances agricoles (Markdown)
│   ├── cultures/
│   │   ├── tomate.md
│   │   ├── manioc.md
│   │   ├── cafe-arabica.md
│   │   ├── banane.md
│   │   └── ... (20+ fiches)
│   ├── maladies/
│   │   ├── mildiou.md
│   │   ├── rouille.md
│   │   └── ... (10+ fiches)
│   ├── techniques/
│   │   ├── compostage.md
│   │   ├── purin-ortie.md
│   │   ├── rotation-cultures.md
│   │   ├── associations-plantes.md
│   │   └── ... (10+ fiches)
│   └── cooperative/
│       ├── fixation-prix.md
│       ├── achat-groupe.md
│       └── gestion-fonds.md
│
├── data/                        # Base de donnees
│   ├── schema.sql               # Schema SQLite
│   ├── seed-demo.sql            # Donnees demo (Ferme des Arondes)
│   └── farm.db                  # SQLite DB (genere)
│
├── agent/                       # Boucle agent (coeur du systeme)
│   ├── agent-loop.ts            # Boucle principale (inspire Gemma Gem)
│   ├── prompt-builder.ts        # Construction du prompt avec contexte
│   ├── tool-parser.ts           # Parse les appels d'outils du LLM
│   ├── tool-executor.ts         # Execute les outils (DB, vault, etc.)
│   ├── tools/
│   │   ├── query-database.ts    # Outil : requete SQLite
│   │   ├── search-vault.ts      # Outil : recherche dans le vault Markdown
│   │   ├── write-journal.ts     # Outil : ajouter une observation
│   │   ├── calculate.ts         # Outil : calculs agricoles (rendements, couts)
│   │   ├── get-sensors.ts       # Outil : lire capteurs (T2, stub en T1)
│   │   └── index.ts             # Registry des outils
│   ├── types.ts                 # Types TypeScript
│   └── index.ts                 # Point d'entree
│
├── server/                      # Serveur web
│   ├── index.ts                 # Serveur HTTP (Bun/Node)
│   ├── api.ts                   # Endpoints API (chat, history, sync)
│   ├── llm-client.ts            # Client OpenAI-compatible vers llamafile
│   └── static/                  # Interface web custom (optionnel T2)
│       └── index.html
│
├── sync/                        # Synchronisation (T2)
│   ├── push-observations.ts     # Push vers Eco-Systemes
│   ├── pull-knowledge.ts        # Pull nouvelles fiches
│   └── sync-manager.ts          # Orchestrateur sync
│
├── scripts/
│   ├── start-llm.sh             # Demarre llamafile avec GPU offload
│   ├── start-agent.sh           # Demarre le serveur agent
│   ├── start-all.sh             # Demarre tout (LLM + agent)
│   └── backup-db.sh             # Backup SQLite
│
├── package.json
├── tsconfig.json
└── bunfig.toml                  # Config Bun runtime
```

### Gotchas connus
```
# CRITICAL: llamafile --server expose une API OpenAI-compatible sur /v1/chat/completions
# CRITICAL: Qwen3 supporte le function calling natif (format tool_call dans la reponse)
# CRITICAL: SQLite pas PostgreSQL — zero config, un fichier, copiable
# CRITICAL: Vault = fichiers Markdown simples, pas besoin d'Obsidian installe
# CRITICAL: GPU offload = -ngl 999 pour CUDA, --gpu auto pour Vulkan
# CRITICAL: Windows exe limit 4 Go — Qwen3-4B Q4_K_M = 2.7 Go, ca passe
# CRITICAL: Bun prefere a Node.js (plus rapide, moins de deps, un seul binaire)
# ATTENTION: Lingala non supporte par aucun LLM — utiliser francais comme fallback
# ATTENTION: llamafile n'a PAS de flag --system-prompt (valide POC 7 avril)
```

## Implementation Blueprint

### Phase 1 : Foundation (Semaine 1, jours 1-3)
**Objectif : SQLite + vault + agent loop basique**

```yaml
Task 1.1:
  action: CREATE
  path: Projects/farm-agent/data/schema.sql
  description: |
    Schema SQLite avec tables : parcelles, recoltes, rotations,
    cooperateurs, finances, inventaire, journal.
    Types simples, pas d'ORM — requetes SQL directes.
  pattern: multipass-farmsystems/app/lib/db/types.ts (pour inspiration)

Task 1.2:
  action: CREATE
  path: Projects/farm-agent/data/seed-demo.sql
  description: |
    Donnees demo : "Ferme des Arondes, Profondeville"
    5 parcelles (maraichage, elevage bovin, verger, champignons, vannerie)
    3 cooperateurs, 2 ans d'historique recoltes
    Quelques lignes finances et inventaire

Task 1.3:
  action: CREATE
  path: Projects/farm-agent/vault/ (20+ fichiers .md)
  description: |
    Fiches agricoles en francais. Format :
    ---
    title: "Tomate"
    type: culture | maladie | technique
    regions: [wallonie, madeira, congo]
    ---
    # Contenu pratique, concret, low-cost
    Contenu inspire du forum Community d'Eco-Systemes (15 discussions existantes)
  pattern: Knowledge/_Templates/Template-Concept.md (frontmatter)

Task 1.4:
  action: CREATE
  path: Projects/farm-agent/agent/ (7 fichiers TS)
  description: |
    Boucle agent inspiree de Gemma Gem (5 fichiers decouples)
    + 2 fichiers supplementaires (tool-executor, tools/index)
    
    Flow :
    1. User message arrive
    2. prompt-builder construit le prompt avec :
       - System prompt agricole
       - Description des outils disponibles (format Qwen3 tool calling)
       - Contexte recent (derniers messages)
    3. Envoie au LLM via API OpenAI-compatible (localhost:8080)
    4. tool-parser detecte si la reponse contient un tool_call
    5. Si oui : tool-executor execute l'outil, resultat reinjecte, retour a 3
    6. Si non : reponse finale renvoyee a l'utilisateur
    
    Max iterations : 5 (eviter boucles infinies)
  pattern: kessler/gemma-gem/agent/ (architecture)
  pattern: multipass-farmsystems/app/features/ai/action-executor.ts (execution)

Task 1.5:
  action: CREATE
  path: Projects/farm-agent/agent/tools/*.ts (5 fichiers)
  description: |
    Outils de l'agent :
    - query_database : execute SELECT sur SQLite, retourne resultats JSON
    - search_vault : grep/fuzzy search dans les fichiers .md du vault
    - write_journal : INSERT dans la table journal (date, observation)
    - calculate : calculs simples (rendement/ha, cout/kg, projection)
    - get_sensors : STUB pour T1, retourne donnees fictives
    
    Chaque outil : { name, description, parameters (JSON Schema), execute(params) }
  pattern: format tool calling Qwen3 (function calling OpenAI-style)
```

### Phase 2 : Server + Integration (Semaine 1, jours 4-5)
**Objectif : serveur web qui orchestre LLM + agent**

```yaml
Task 2.1:
  action: CREATE
  path: Projects/farm-agent/server/llm-client.ts
  description: |
    Client HTTP vers llamafile (localhost:8080/v1/chat/completions)
    - Format OpenAI Chat Completions API
    - Support streaming (SSE)
    - Timeout configurable (60 sec default)
    - Retry avec backoff (max 3)
    - Injection des tools dans la requete (format Qwen3)

Task 2.2:
  action: CREATE
  path: Projects/farm-agent/server/index.ts + api.ts
  description: |
    Serveur Bun HTTP sur port 3000 :
    - GET / → interface web (static/index.html ou redirect vers llamafile UI)
    - POST /api/chat → envoie message, retourne reponse agent (SSE stream)
    - GET /api/history → historique des conversations
    - GET /api/farm → infos de la ferme (parcelles, cooperateurs)
    - POST /api/journal → ajouter observation directe
    
    Le serveur agent (port 3000) parle au serveur LLM (port 8080)

Task 2.3:
  action: CREATE
  path: Projects/farm-agent/server/static/index.html
  description: |
    Interface web minimaliste (1 fichier HTML + CSS + JS inline)
    - Chat conversationnel
    - Affiche les tool calls en cours ("Recherche dans la base...")
    - Responsive (telephone)
    - Fonctionne sans framework, vanilla JS
    - Branding Eco-Systemes
    - Multiligue (FR par defaut, detection navigateur)

Task 2.4:
  action: CREATE
  path: Projects/farm-agent/scripts/start-all.sh + start-all.bat
  description: |
    Script qui demarre tout :
    1. Verifie que le modele GGUF existe, sinon telecharge
    2. Initialise SQLite si farm.db n'existe pas (schema + seed)
    3. Demarre llamafile en arriere-plan (--server -ngl 999 --port 8080)
    4. Attend que le LLM soit pret (poll /health)
    5. Demarre le serveur agent (port 3000)
    6. Ouvre le navigateur sur localhost:3000
```

### Phase 3 : Polish + GPU (Semaine 2)
**Objectif : GPU offload, system prompt optimise, tests**

```yaml
Task 3.1:
  action: CREATE
  path: Projects/farm-agent/agent/system-prompt.md
  description: |
    System prompt agricole optimise :
    - Role : "Tu es l'Agent Agricole de [NOM_FERME]"
    - Contexte : resume de la ferme (injecte dynamiquement depuis DB)
    - Outils : description precise de chaque outil
    - Regles : concret, low-cost, local, langue de l'utilisateur
    - Securite : ne pas inventer de donnees, dire quand on ne sait pas
    Tester avec Promptfoo (3 scenarios x 3 langues)

Task 3.2:
  action: CONFIGURE
  description: |
    Tester GPU offload :
    - NVIDIA : -ngl 999 (CUDA)
    - AMD : --gpu vulkan -ngl 999
    - Mesurer tokens/sec avec et sans GPU
    - Documenter la procedure dans README

Task 3.3:
  action: CREATE
  path: Projects/farm-agent/tests/
  description: |
    Tests de base :
    - agent-loop.test.ts : mock LLM, verifie tool calling loop
    - tools.test.ts : chaque outil avec SQLite in-memory
    - prompt-builder.test.ts : verifie format du prompt
    Pattern : multipass-farmsystems vitest setup

Task 3.4:
  action: CREATE
  path: Projects/farm-agent/install.sh
  description: |
    Script d'installation one-liner :
    curl -fsSL https://raw.githubusercontent.com/.../install.sh | bash
    - Detecte OS et architecture
    - Installe Bun si absent
    - Telecharge le modele GGUF
    - npm install / bun install
    - Initialise la DB
    - Cree un service systemd (optionnel)
```

### Phase 4 : Sync + Demo UNDP (Semaine 3)
**Objectif : synchronisation Eco-Systemes + scenario demo**

```yaml
Task 4.1:
  action: CREATE
  path: Projects/farm-agent/sync/
  description: |
    Module de synchronisation opportuniste :
    - sync-manager : detecte la connectivite, orchestre push/pull
    - push-observations : POST journal entries vers API Eco-Systemes
    - pull-knowledge : GET nouvelles fiches depuis Eco-Systemes, ecrit dans vault/
    Format API : REST JSON, auth par token cooperative

Task 4.2:
  action: CREATE
  description: |
    Scenario demo UNDP (script de demo) :
    1. "Bonjour, je suis Sebastien de la Ferme des Arondes"
    2. Agent : query DB → "Bonjour Sebastien, vos 5 parcelles..."
    3. "Mes tomates sur la parcelle B2 jaunissent"
    4. Agent : search_vault("tomates jaunissent") + query_database(parcelle B2 historique)
    5. Reponse personnalisee avec historique
    6. "Combien ai-je recolte l'an dernier ?"
    7. Agent : query_database(recoltes 2025) → calculate(rendement/ha)
    8. Tableau avec chiffres
    
    Tout en offline, sur un PC a 350 EUR.
```

### Points d'integration
```yaml
ECOSYSTEMES:
  - API sync bidirectionnelle (T2)
  - Forum Community : observations partagees
  - Marketplace : produits de la ferme

LIVESTOCKAI:
  - Reutiliser patterns : sentinel, chat-service, memory-service, domain-knowledge
  - Meme stack technique (TypeScript, Bun)
  - Convergence future : LivestockAI IS le Farm Agent (meme codebase)

MESHTASTIC (T2+):
  - Capteurs terrain → donnees injectees dans la DB
  - get_sensors tool lit les dernieres valeurs

R2D2 SYSTEM:
  - PAS un skill Claude Code (c'est un produit standalone)
  - Note vault : Knowledge/Projets/Farm-Agent.md
  - Taskyn : creer un projet "Farm Agent" pour le tracking
```

## Validation Loop

### Niveau 1 : Structure
```bash
# Verifier les fichiers crees
test -f Projects/farm-agent/package.json
test -f Projects/farm-agent/data/schema.sql
test -f Projects/farm-agent/agent/agent-loop.ts
test -f Projects/farm-agent/server/index.ts
test -d Projects/farm-agent/vault/cultures
ls Projects/farm-agent/vault/cultures/*.md | wc -l  # >= 10

# Verifier que SQLite se cree
sqlite3 Projects/farm-agent/data/farm.db ".tables"
# Doit afficher : parcelles recoltes rotations cooperateurs finances inventaire journal
```

### Niveau 2 : Fonctionnel
```bash
# Demarrer llamafile + agent
cd Projects/farm-agent && bash scripts/start-all.sh

# Tester l'API agent
curl -s http://localhost:3000/api/farm | jq .
# Doit retourner les infos de la ferme demo

curl -s -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Quelles sont mes parcelles ?"}' | jq .
# Doit retourner une reponse avec les 5 parcelles de la demo

# Tester le tool calling
curl -s -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Combien ai-je recolte de tomates en 2025 ?"}' | jq .
# L'agent doit avoir fait un query_database + calculate
```

### Niveau 3 : Integration
```bash
# GPU offload
# Demarrer avec -ngl 999 et mesurer
time curl -s -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Bonjour"}' > /dev/null
# Doit etre < 15 sec avec GPU

# Multi-users (T2)
# Ouvrir 2 navigateurs sur localhost:3000, chatter en parallele

# Sync (T2)
# curl -s http://localhost:3000/api/sync/status
```

## Checklist de validation finale

- [ ] T0 fonctionne (USB stick, chat simple) — **DONE**
- [ ] Schema SQLite cree avec seed demo
- [ ] 20+ fiches vault agricoles (cultures, maladies, techniques)
- [ ] Agent loop fonctionnel : question → tool calls → reponse
- [ ] 4 outils operationnels (query_db, search_vault, write_journal, calculate)
- [ ] Interface web accessible sur localhost:3000
- [ ] GPU offload documente et teste
- [ ] Script start-all.sh demarre tout en une commande
- [ ] Scenario demo UNDP reproductible
- [ ] Tests passes (agent-loop, tools, prompt-builder)
- [ ] README complet avec instructions d'installation

## Anti-Patterns a eviter

- **Ne pas re-inventer LivestockAI** : Farm Agent est un sous-ensemble offline, pas une reecriture
- **Ne pas complexifier le schema DB** : SQLite simple, pas d'ORM, pas de migrations
- **Ne pas dependre d'Internet** : tout doit fonctionner debranche
- **Ne pas optimiser prematurement** : CPU lent mais fonctionnel > GPU rapide mais instable
- **Ne pas ignorer le multilingue** : tester FR + PT + NL a chaque etape
- **Ne pas creer de framework** : code direct, pas d'abstraction inutile
- **Ne pas oublier Windows** : beaucoup de PC reconditionnes sont sous Windows

## Decision log

| Decision | Choix | Pourquoi |
|----------|-------|----------|
| DB | SQLite (pas PostgreSQL) | Zero config, un fichier, copiable, suffisant pour une ferme |
| Runtime | Bun (pas Node) | Plus rapide, moins de deps, aligne avec LivestockAI |
| LLM | Qwen3-4B Q4_K_M | 119 langues, 2.7 Go, sous limite Windows 4 Go, pre-built Mozilla |
| Agent loop | TypeScript custom | Inspire Gemma Gem, decouplee, testable, reutilisable |
| Interface | HTML vanilla (pas React) | Zero build, un fichier, fonctionne partout |
| Vault | Markdown simples (pas Obsidian) | Pas besoin d'Obsidian installe, editable avec n'importe quel editeur |
| Sync | REST API optionnel | Offline-first, sync quand Internet dispo |
| Licence | Apache 2.0 | Compatible commercial, aligne avec EuroLLM et Eco-Systemes |

---

**PRP Score : 8/10**
- Points forts : contexte exhaustif, codebase existant reutilisable, POC valide, hardware specs concretes
- Risques : function calling Qwen3 peut etre imprevisible, GPU setup varie par machine, vault content quality
- Mitigation : Phase 1 CPU-only d'abord, GPU en Phase 3, tester avec Promptfoo
