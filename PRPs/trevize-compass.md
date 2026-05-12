---
name: "PRP — Trevize-Compass (Boule de Cristal MultiPass)"
date: 2026-05-04
type: prp
status: ready-to-execute
phase_target: MVP J+21
related:
  - "[[INITIAL_trevize-compass]]"
---

# PRP — TREVIZE-COMPASS (Boule de Cristal → Prim Radiant MultiPass)

## Positionnement final du produit

> **Trevize-Compass est le Prim Radiant de la doctrine MultiPass** — instrument inspiré du Prim Radiant d'Asimov (*Foundation*), où Hari Seldon visualise et manipule les équations psychohistoriques. Pour MultiPass, c'est l'instrument partagé de **Mike-N51** (Première Foundation, terrain) et **Manu-N52** (Seconde Foundation, mentaliste-cachée), où leurs deux flux convergent et co-construisent le Plan.

> **Évolution en 3 actes** :
> - **MVP J+21** = **Boule de Cristal** (lecture, navigation, animation EST-OUEST)
> - **Phase 2.5 J+45** = **Prim Radiant minimal** (manipulation, what-if, Crises Seldon marquées, annotations partagées)
> - **Phase 3 J+90** = **Prim Radiant complet** (Three.js holographique, multi-user simultané, projections paramétriques)

> Voir [[C_Trevize-Compass-Prim-Radiant-N51-N52]] pour la métaphore-cadre complète.

## Goal

Construire **Trevize-Compass**, plate-forme web dédiée de cartographie sémantique spatio-temporelle, alimentée par le vault Obsidian, exposant la doctrine MultiPass sous forme de **graph navigable multi-axe** avec dimension temporelle M-relative et primitive de navigation EST-OUEST.

**Le MVP est la Boule de Cristal.** L'architecture est conçue dès le MVP pour **réserver l'évolution vers Prim Radiant** (Phase 2.5 et Phase 3) sans dette technique.

**État final souhaité (MVP J+21) :**

- Stack Docker opérationnelle sur **VM 105 r2d2-lab** (Sferă-A privée)
- Neo4j Community 5.x + NeoDash + front-end Cytoscape custom
- Script `sync-vault-to-graph.py` parse `~/Documents/Knowledge/Concepts/*.md` et popule Neo4j
- 5 notes Zettelkasten 2026-05-04 visibles avec wikilinks et sémantique d'edges fonctionnels
- Slider temporel multi-échelle (jour / mois / année) opérationnel
- Filtres par tag fonctionnels
- Bouton « Play EST-OUEST » qui anime au moins une boucle Fibonacci
- Documentation complète dans `Projets/Trevize-Compass/`
- Test de récupération après reboot VM 105 validé

## Why

- **Visualisation cardinale** : le réseau de 6 notes Zettelkasten + 6 livrables pilote tissé en session 2026-05-04 demande une carte interactive — le texte tient mais le graph parle d'un coup d'œil.
- **Vrai produit MultiPass** : pas un simple outil de visualisation. Réutilisable pour démos clients, Dossiers-Clients enrichis, fondation des intégrations futures (chatbot doctrinal, MultiPass-app, ntfy).
- **Signature non-copiable** : la dimension temporelle EST-OUEST + bonds Fibonacci sont propres à la doctrine MultiPass. Personne ne va les ajouter spontanément. Couche-24-Transparency + boucle EST-OUEST = combo vendable et défendable.
- **Anticipation Mitza-DETECT** : voir les patterns émerger dans le temps (signaux convergents 2026-04-24 → 2026-05-04) au lieu de relire chaque note séparément.
- **Cohérence avec [[intelligence-warehouse-skill]]** : Trevize-Compass est l'incarnation visuelle de la Loi de Trevize (« 3+ signaux convergents = pattern émergent »).
- **Coordination N51 ↔ N52** : Mike (terrain) et Manu (macro) ont besoin d'un **lieu partagé** où leurs deux flux convergent. Trevize-Compass = leur Prim Radiant — table de coordination opérante.
- **Stress-test de la doctrine** : à terme (Phase 2.5+), le mode what-if permet l'**exercice psychohistorique** sur la stratégie MultiPass — pas pour prédire avec certitude, pour **éprouver** la robustesse de la doctrine face aux scénarios.
- **Distinction Sferă-A privée vs Sferă-C publique** : cohérent pacte Asimov. Sferă-C = Boule de Cristal seule (lecture + storytelling client). Sferă-A = vrai Prim Radiant complet (manipulation + what-if + annotations N51/N52).

## What

Plate-forme web composée de :

1. **Couche données** : 2 instances Neo4j Community physiquement séparées
   - **Sferă-A privée** (VM 105) : vault Knowledge complet, accès Mike + Manu
   - **Sferă-C publique** (VM 103) : sous-ensemble doctrinal, accès clients/prospects via Authentik
2. **Couche dashboards** : NeoDash pour requêtes Cypher rapides côté Mike + Manu
3. **Couche front-end** : Cytoscape.js custom MultiPass-brandé avec :
   - Layout temporel custom (X = M-relative, Y = niveau hiérarchique)
   - Slider multi-échelle (jour / mois / année)
   - Filtres par tag dynamiques
   - Tooltip avec extrait note + lien profond Obsidian
   - Sémantique edges colorée (CONFIRME / ANTICIPE / CONTREDIT / BOUCLE_EST_OUEST)
   - Bouton « Play EST-OUEST » avec bonds Fibonacci
4. **Couche synchronisation** :
   - **Push manuel** : `sync-vault-to-graph.py --mode full|incremental --target sferaA|sferaC`
   - **Watcher temps réel** : `watchdog` Python sur Sferă-A
5. **Couche sécurité** : reverse proxy nginx + Authentik (Sferă-C uniquement)
6. **Couche backup** : intégration backup-skill avec dump Neo4j quotidien

### Success Criteria (MVP J+21)

- [ ] Container `trevize-neo4j-a` opérationnel sur VM 105 (port 7474/7687)
- [ ] Container `trevize-neodash-a` opérationnel (port 5005)
- [ ] Container `trevize-frontend-a` (Cytoscape custom) servi sur port 8090
- [ ] Container `trevize-sync-a` (watcher) actif et stable
- [ ] Script `sync-vault-to-graph.py` parse les 5 notes session 2026-05-04 + leurs wikilinks
- [ ] Slider temporel fonctionnel (3 granularités)
- [ ] Filtres par tag fonctionnels
- [ ] Tooltip + lien profond ouvrant la note dans Obsidian
- [ ] Sémantique edges visible (4 couleurs)
- [ ] Bouton « Play EST-OUEST » + animation Fibonacci sur au moins une boucle
- [ ] README.md complet dans `Projets/Trevize-Compass/`
- [ ] Test reboot VM 105 sans perte de données
- [ ] CLAUDE.md mis à jour (section Warehouses Applications)
- [ ] Note Zettelkasten parente créée : `[[C_Trevize-Compass-Boule-De-Cristal-MultiPass]]`

---

## Contexte nécessaire

### Documentation & Références

```yaml
# === MUST READ — Contexte à charger ===

- file: ~/.claude/PRPs/INITIAL_trevize-compass.md
  why: Spécification source — 7 dimensions cardinales tranchées avec Mike

- file: ~/.claude/CLAUDE.md
  why: Conventions globales système r2d2 (encodage, vault, infra VMs)

- file: ~/Documents/Knowledge/Concepts/C_Amsterdam-Moment-Tabac-Cloud-Anticipation.md
  why: Note de référence — schéma temporel + 7 signaux convergents à représenter

- file: ~/Documents/Knowledge/Concepts/C_DeepSeek-V4-Commoditisation-LLM.md
  why: Frontmatter type pour parser (date, type, status, tags, related)

- skill: intelligence-warehouse-skill
  why: Trevize-Compass est l'incarnation visuelle de Trevize. Cohérence brand + Loi Trevize.

- skill: docker-skill
  why: Patterns docker-compose, healthchecks, conventions container naming

- skill: obsidian-skill
  why: Conventions vault, frontmatter YAML, gestion wikilinks

- skill: ai-infra-skill
  why: Patterns LiteLLM/Mistral pour Phase 3 (chatbot doctrinal)

- skill: backup-skill
  why: Intégration dump Neo4j dans la routine /bak-*

- skill: monitoring-skill
  why: Intégration Beszel + ntfy pour alertes Trevize-Compass

- url: https://neo4j.com/docs/operations-manual/current/docker/introduction/
  why: Configuration Docker production-ready Neo4j Community

- url: https://neo4j.com/docs/cypher-manual/current/
  why: Référence Cypher pour requêtes MERGE, MATCH, paths

- url: https://github.com/neo4j-labs/neodash
  why: Déploiement NeoDash et configuration dashboards

- url: https://js.cytoscape.org/#getting-started
  why: API Cytoscape — layouts, événements, styles

- url: https://js.cytoscape.org/#layouts/cose-bilkent
  why: Extension layout cose-bilkent (alternative au layout temporal custom)

- url: https://github.com/cytoscape/cytoscape.js-popper
  why: Tooltips riches sur nodes (extrait + lien profond)

- url: https://docs.python.org/3/library/pathlib.html
  why: Parser markdown — pathlib + frontmatter parsing

- url: https://python-watchdog.readthedocs.io/
  why: FileSystemWatcher pour sync temps réel

- vault: [[C_DeepSeek-V4-Commoditisation-LLM]]
- vault: [[C_AI-Code-Generation-Supply-Chain-Risk]]
- vault: [[C_Iran-AWS-Middle-East-Validation-Souverainete-Onprem]]
- vault: [[C_Cas-Etude-Mitza-Detect-Vauban-IPO-SpaceX]]
- vault: [[C_Amsterdam-Moment-Tabac-Cloud-Anticipation]]
  why: Les 5 notes seed du graph initial

- vault: [[C_Pacte-De-Verite]]
- vault: [[C_Couche-24-Transparency]]
- vault: [[C_Empire-Funds-Its-Own-Defeat]]
  why: Concepts cardinaux référencés dans les wikilinks

- vault: [[2026-05-04_Pilot-HVAC-RO_v1]]
- vault: [[2026-05-04_Pilot-HVAC-RO_Kit-Kickoff-J7]]
  why: Documents projet pilote intégrables dans le graph
```

### Arbre actuel du système

```
~/.claude/
├── PRPs/
│   ├── INITIAL_trevize-compass.md      # spec source (déjà rédigée)
│   ├── templates/prp_base.md           # template PRP
│   └── trevize-compass.md              # CE FICHIER
├── skills/
│   ├── intelligence-warehouse-skill/   # cohérence brand Trevize
│   ├── docker-skill/                   # patterns docker
│   ├── obsidian-skill/                 # patterns vault
│   ├── ai-infra-skill/                 # patterns LLM Mistral
│   └── ...
├── mcp-servers/
│   └── knowledge-assistant/            # MCP vault déjà branché
└── CLAUDE.md                           # à mettre à jour

~/Documents/Knowledge/                  # vault Obsidian (source du graph)
├── Concepts/                           # notes Zettelkasten cardinales
├── Projets/MultiPass/                  # docs projet pilote
└── ...

VM 105 r2d2-lab (192.168.1.161)         # cible POC Sferă-A
├── 3 containers existants (rag-indexer, taskyn-web, taskyn-core)

VM 103 r2d2-main (192.168.1.163)        # cible Phase 2 Sferă-C
├── 29 containers (MultiPass + Taskyn + monitoring)
```

### Arbre souhaité avec nouveaux fichiers (MVP J+21)

```
~/Documents/Knowledge/Projets/Trevize-Compass/      # dossier projet vault
├── README.md                                       # documentation utilisateur
├── decisions/                                      # log des décisions
│   └── 2026-05-04_initial-spec.md
├── architecture/
│   └── schema-neo4j.md                            # modèle de données
└── deployment/
    └── operations.md                               # runbook opérationnel

~/Documents/Knowledge/Concepts/
└── C_Trevize-Compass-Boule-De-Cristal-MultiPass.md # note Zettelkasten parente

# Code sur VM 105 (déployé via SSH)
/opt/trevize-compass/                               # racine projet
├── docker-compose.sfera-a.yml                     # stack Sferă-A
├── .env                                           # NEO4J_PASSWORD, NFS_VAULT_PATH
├── neo4j/
│   └── plugins/                                   # APOC etc.
├── neodash/
│   └── dashboards/
│       ├── doctrine-2026.json                     # dashboard prêt à l'emploi
│       └── moment-tabac.json
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── main.js                                # bootstrap Cytoscape
│       ├── api.js                                 # fetch Neo4j via REST/HTTP
│       ├── layout-temporal.js                     # layout custom EST-OUEST
│       ├── slider.js                              # slider multi-échelle
│       ├── filters.js                             # filtres par tag
│       ├── tooltip.js                             # tooltip + deep link
│       ├── play-east-west.js                      # animation Fibonacci
│       └── styles.css                             # MultiPass branding
├── sync/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── parse_vault.py                             # parser markdown → dict
│   ├── sync_to_neo4j.py                           # writer Neo4j
│   ├── watcher.py                                 # FileSystemWatcher
│   └── sync-vault-to-graph.py                     # CLI entry-point
└── scripts/
    ├── deploy.sh                                  # bootstrap initial
    ├── backup.sh                                  # dump Neo4j
    └── restore.sh                                 # restore from dump
```

### Gotchas connus du système

```
# CRITICAL — Encodage
# - .md / .json / .py / .js / .yml / .conf : UTF-8 SANS BOM
# - .ps1 / .psm1 : UTF-8 AVEC BOM (compat PS 5.1)
# - utiliser [System.IO.File]::WriteAllText avec encodage explicite
#   JAMAIS Set-Content sans -Encoding utf8NoBOM

# CRITICAL — Wikilinks
# - Tolérer 4 variantes : [[Note]], [[Note|Alias]], [[Note#Section]], [[Note^block-id]]
# - Le parser doit extraire le target uniquement, ignorer alias/section/block

# CRITICAL — Frontmatter YAML
# - Toujours présent dans les notes vault
# - Champs requis : title, date (ISO 8601), type, status, tags
# - Champ optionnel : related (liste de wikilinks)

# CRITICAL — Race conditions sync
# - Obsidian peut sauvegarder pendant que le watcher lit
# - Utiliser un mutex ou une queue avec debounce 500ms

# CRITICAL — Neo4j Community
# - Pas de clustering — single instance par Sferă
# - Volume vault < 10 000 nodes = OK Community sans souci
# - APOC plugin requis pour fonctions utilitaires

# CRITICAL — Layout temporel Cytoscape
# - Pas natif — à coder. Pattern : layout: { name: 'preset', positions: fn }
# - Calculer x = M_days * pixel_per_day, y = level * row_height
# - Recalculer à chaque changement de granularité

# CRITICAL — Authentik intégration
# - À VÉRIFIER en début de Phase 2 : Authentik est-il déployé sur VM 103 ?
# - Si non : prévoir 1 jour pour le mettre en place AVANT d'exposer Sferă-C

# CRITICAL — Pacte de vérité
# - Notes seedling marquées visuellement comme telles (couleur + icône)
# - Notes anticipation distinguées des validations (forme différente)
# - Pas d'embellissement automatique du contenu
# - Si une note est obsolète, marquage `ARCHIVED`, pas suppression

# CRITICAL — Vault accessible depuis VM 105
# - VM 105 doit accéder au vault Windows. Options :
#   1. NFS export depuis Windows (rclone-nfs ou Windows NFS server)
#   2. Sync via Syncthing
#   3. Git push/pull (vault est git-init depuis 2026-02-11)
# - RECOMMANDATION : Git pull périodique côté VM 105 (le plus simple, le plus auditable)
```

---

## Implementation Blueprint

### Modèle de données Neo4j (schema)

```cypher
// === LABELS ===
:Note            // Note Zettelkasten ou doc projet
:Tag             // Tag hiérarchique
:Source          // Article externe cité
:Concept         // Concept cardinal MultiPass (sous-ensemble de :Note)
:Project         // Document projet (offre, kit, sourcing)
:Event           // Événement daté externe (ex : "frappe Iran×AWS")

// === RELATIONSHIPS ===
(:Note)-[:CONFIRME]->(:Note)              // sémantique validation
(:Note)-[:ANTICIPE]->(:Note)              // sémantique prédiction
(:Note)-[:CONTREDIT]->(:Note)             // sémantique opposition
(:Note)-[:BOUCLE_EST_OUEST {fibonacci_distance: int}]->(:Note)
(:Note)-[:RELATED_TO]->(:Note)            // wikilink sans sémantique
(:Note)-[:DERIVES_FROM]->(:Note)          // mise à jour
(:Note)-[:TAGGED_WITH]->(:Tag)
(:Note)-[:CITES]->(:Source)

// === PROPRIÉTÉS NODE :Note ===
// Note : champs marqués [PR] sont réservés pour le Prim Radiant (Phase 2.5+)
// mais déclarés DÈS LE MVP dans le schema pour éviter la dette architecturale.
{
  id: string                  // ex: "C_DeepSeek-V4-Commoditisation-LLM"
  title: string
  path: string                // chemin vault relatif
  date_absolute: date         // ISO 8601
  M_days: int                 // (date - T0) en jours, T0=2026-05-01
  M_months: int               // M_days / 30.44 arrondi
  M_years: float              // M_days / 365.25 arrondi 2 décimales
  cardinal_axis: string       // "EST" | "OUEST" | "M0"
  level: int                  // 1-6 si applicable (étape moment-tabac)
  pacte_status: string        // "validated" | "anticipated" | "case-study" | "seedling" | "growing" | "evergreen" | "archived"
  tags: list<string>
  body_excerpt: string        // 300 premiers caractères pour tooltip
  content_hash: string        // SHA-256 pour sync incrémental
  publish_to_sferaC: bool     // marqueur publication publique
  // === Réservations Prim Radiant (Phase 2.5+) — déclarés dès le MVP ===
  is_seldon_crisis: bool      // [PR] node marqué Crise Seldon (étoile dorée UI)
  crisis_probability: float   // [PR] 0.0-1.0, pour les Crises anticipées
  crisis_status: string       // [PR] "confirmed" | "anticipated" | "active"
  branch_id: string           // [PR] ID de branche what-if (null en MVP, valeur en P2.5)
  annotations: list<map>      // [PR] [{author: string, date: date, text: string}]
  parametric_law: map         // [PR] équation paramétrique (laws cardinal MultiPass)
}

// === Labels supplémentaires pour le Prim Radiant ===
:Crisis           // [PR] sous-label des nodes Crise Seldon
:Branch           // [PR] sous-label des nodes appartenant à une branche what-if
:Law              // [PR] équations paramétriques (Loi de la Membrane, Empire-Funds, etc.)

// === CONSTRAINTS ===
CREATE CONSTRAINT note_id_unique IF NOT EXISTS
FOR (n:Note) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT tag_name_unique IF NOT EXISTS
FOR (t:Tag) REQUIRE t.name IS UNIQUE;

// === INDEX ===
CREATE INDEX note_date IF NOT EXISTS FOR (n:Note) ON (n.date_absolute);
CREATE INDEX note_M_days IF NOT EXISTS FOR (n:Note) ON (n.M_days);
CREATE INDEX note_status IF NOT EXISTS FOR (n:Note) ON (n.pacte_status);
```

### Structure des fichiers à créer

```yaml
File 1:
  path: /opt/trevize-compass/docker-compose.sfera-a.yml
  rôle: Stack Docker complète Sferă-A (Neo4j + NeoDash + Frontend + Sync)
  pattern: Voir patterns docker-compose dans intelligence-warehouse-skill et docker-skill

File 2:
  path: /opt/trevize-compass/.env.template
  rôle: Variables d'environnement template (NEO4J_PASSWORD, VAULT_PATH, etc.)
  pattern: ~/.claude/skills/credentials-skill/

File 3:
  path: /opt/trevize-compass/sync/parse_vault.py
  rôle: Parser markdown → dict (frontmatter + wikilinks + sémantique)
  pattern: Lecture frontmatter YAML standard Python (PyYAML)

File 4:
  path: /opt/trevize-compass/sync/sync_to_neo4j.py
  rôle: Writer Neo4j via driver Python neo4j
  pattern: MERGE-only pour idempotence

File 5:
  path: /opt/trevize-compass/sync/watcher.py
  rôle: FileSystemWatcher avec debounce 500ms
  pattern: watchdog.observers.Observer + queue.Queue

File 6:
  path: /opt/trevize-compass/sync/sync-vault-to-graph.py
  rôle: CLI entry-point (--mode, --target, --vault)
  pattern: argparse standard

File 7:
  path: /opt/trevize-compass/frontend/src/main.js
  rôle: Bootstrap Cytoscape, fetch données, init UI
  pattern: ES modules vanilla JS (pas de framework lourd)

File 8:
  path: /opt/trevize-compass/frontend/src/layout-temporal.js
  rôle: Layout custom Cytoscape (X = M_days, Y = level)
  pattern: layout: { name: 'preset', positions: fn }

File 9:
  path: /opt/trevize-compass/frontend/src/play-east-west.js
  rôle: Animation Fibonacci EST→OUEST
  pattern: setInterval + cy.elements.style transitions

File 10:
  path: /opt/trevize-compass/frontend/src/styles.css
  rôle: Branding MultiPass (couleurs Couche-24, sémantique edges)
  pattern: variables CSS + classes sémantiques

File 11:
  path: /opt/trevize-compass/frontend/Dockerfile
  rôle: Build nginx + assets statiques
  pattern: multi-stage build (alpine)

File 12:
  path: /opt/trevize-compass/scripts/deploy.sh
  rôle: Bootstrap initial complet
  pattern: bash strict (set -euo pipefail)

File 13:
  path: /opt/trevize-compass/scripts/backup.sh
  rôle: Dump Neo4j quotidien (intégration backup-skill)
  pattern: cron + rotation 7 jours

File 14:
  path: ~/Documents/Knowledge/Projets/Trevize-Compass/README.md
  rôle: Documentation utilisateur Mike + Manu
  pattern: ~/Documents/Knowledge/Projets/MultiPass/MultiPass-Dossier-Clients-FR.md

File 15:
  path: ~/Documents/Knowledge/Concepts/C_Trevize-Compass-Boule-De-Cristal-MultiPass.md
  rôle: Note Zettelkasten parente (créée à fin MVP)
  pattern: Notes Concepts/ existantes
```

### Liste des tâches ordonnées (MVP J+21)

```yaml
# === Phase 0 : Préparation (J+1) ===

Task 0.1:
  action: VERIFY
  description: VM 105 accessible SSH, Docker installé, espace disque ≥ 50 Go
  validation: ssh r2d2helm@192.168.1.161 "docker --version && df -h /"

Task 0.2:
  action: VERIFY
  description: Vault Knowledge accessible depuis VM 105 (git pull ou NFS)
  validation: ssh r2d2helm@192.168.1.161 "ls /mnt/vault/Concepts/ | head"

Task 0.3:
  action: CREATE
  path: ~/Documents/Knowledge/Projets/Trevize-Compass/
  description: Dossier projet vault + decisions + architecture + deployment
  pattern: structure existante autres projets

# === Phase 1 : Stack Docker base (J+2 à J+4) ===

Task 1.1:
  action: CREATE
  path: /opt/trevize-compass/.env.template
  description: Variables d'environnement (NEO4J_PASSWORD, VAULT_PATH, etc.)
  encoding: UTF-8 sans BOM

Task 1.2:
  action: CREATE
  path: /opt/trevize-compass/docker-compose.sfera-a.yml
  description: 4 services (neo4j-sfera-a, neodash-a, frontend-a, sync-a)
  pattern: docker-skill best practices (healthchecks, restart policies)
  encoding: UTF-8 sans BOM

Task 1.3:
  action: DEPLOY
  description: docker compose up -d sur VM 105
  validation: docker ps montre 4 containers UP (au moins neo4j et neodash)

Task 1.4:
  action: TEST
  description: Neo4j accessible sur http://192.168.1.161:7474
  validation: curl -u neo4j:$PWD http://192.168.1.161:7474/db/neo4j/query/v2

Task 1.5:
  action: APPLY
  description: Schema Neo4j (constraints + index) via cypher-shell
  validation: SHOW CONSTRAINTS retourne note_id_unique

# === Phase 2 : Parser vault et sync (J+5 à J+8) ===

Task 2.1:
  action: CREATE
  path: /opt/trevize-compass/sync/requirements.txt
  description: neo4j, watchdog, pyyaml, python-frontmatter
  encoding: UTF-8 sans BOM

Task 2.2:
  action: CREATE
  path: /opt/trevize-compass/sync/parse_vault.py
  description: Parser markdown — voir pseudocode §Pseudocode
  encoding: UTF-8 sans BOM

Task 2.3:
  action: CREATE
  path: /opt/trevize-compass/sync/sync_to_neo4j.py
  description: Writer Neo4j MERGE-only — voir pseudocode §Pseudocode
  encoding: UTF-8 sans BOM

Task 2.4:
  action: CREATE
  path: /opt/trevize-compass/sync/sync-vault-to-graph.py
  description: CLI entry-point argparse
  encoding: UTF-8 sans BOM

Task 2.5:
  action: TEST
  description: Premier import des 5 notes session 2026-05-04 + leurs concepts liés
  validation: |
    cypher-shell "MATCH (n:Note) RETURN count(n)" >= 5
    cypher-shell "MATCH ()-[r]->() RETURN count(r)" >= 10

Task 2.6:
  action: CREATE
  path: /opt/trevize-compass/sync/watcher.py
  description: FileSystemWatcher debounce 500ms
  encoding: UTF-8 sans BOM

Task 2.7:
  action: TEST
  description: Modifier une note dans le vault → graph mis à jour < 5s
  validation: timestamp Neo4j vs timestamp file

# === Phase 3 : Front-end Cytoscape (J+9 à J+15) ===

Task 3.1:
  action: CREATE
  path: /opt/trevize-compass/frontend/package.json
  description: Dépendances cytoscape, cytoscape-popper, popper-core
  pattern: package.json minimal vanilla JS

Task 3.2:
  action: CREATE
  path: /opt/trevize-compass/frontend/public/index.html
  description: Layout HTML 3 zones (header MultiPass, graph principal, sidebar contrôles)

Task 3.3:
  action: CREATE
  path: /opt/trevize-compass/frontend/src/api.js
  description: fetch /api/graph (Neo4j HTTP query API)
  pattern: fetch + Cypher query côté client

Task 3.4:
  action: CREATE
  path: /opt/trevize-compass/frontend/src/main.js
  description: Bootstrap Cytoscape + chargement données
  encoding: UTF-8 sans BOM

Task 3.5:
  action: CREATE
  path: /opt/trevize-compass/frontend/src/layout-temporal.js
  description: Layout custom (X = M_days, Y = level)
  voir: §Pseudocode layout-temporal

Task 3.6:
  action: CREATE
  path: /opt/trevize-compass/frontend/src/styles.css
  description: Branding MultiPass + sémantique edges (4 couleurs)

Task 3.7:
  action: CREATE
  path: /opt/trevize-compass/frontend/src/slider.js
  description: Slider HTML5 multi-échelle (jour / mois / année)

Task 3.8:
  action: CREATE
  path: /opt/trevize-compass/frontend/src/filters.js
  description: Checkboxes par tag, filtre cy.elements

Task 3.9:
  action: CREATE
  path: /opt/trevize-compass/frontend/src/tooltip.js
  description: Tooltip popper avec extrait + lien obsidian://vault/...

Task 3.10:
  action: CREATE
  path: /opt/trevize-compass/frontend/src/play-east-west.js
  description: Animation EST→OUEST avec bonds Fibonacci
  voir: §Pseudocode play-east-west

Task 3.11:
  action: CREATE
  path: /opt/trevize-compass/frontend/Dockerfile
  description: Build nginx + assets

Task 3.12:
  action: TEST
  description: Front-end accessible http://192.168.1.161:8090
  validation: les 5 notes s'affichent + slider fonctionne + tooltip OK

# === Phase 4 : Dashboard NeoDash et documentation (J+16 à J+19) ===

Task 4.1:
  action: CONFIGURE
  description: Dashboard NeoDash "Doctrine 2026" avec 4 reports principaux
    - Liste notes par status (table)
    - Distribution M_days (histogram)
    - Top tags (bar chart)
    - Graph Cypher visualisation

Task 4.2:
  action: CREATE
  path: ~/Documents/Knowledge/Projets/Trevize-Compass/README.md
  description: Documentation utilisateur (frontmatter YAML, sections install/usage/API)
  encoding: UTF-8 sans BOM
  pattern: ~/Documents/Knowledge/Projets/MultiPass/MultiPass-Dossier-Clients-FR.md

Task 4.3:
  action: CREATE
  path: ~/Documents/Knowledge/Projets/Trevize-Compass/architecture/schema-neo4j.md
  description: Documentation modèle de données

Task 4.4:
  action: CREATE
  path: ~/Documents/Knowledge/Projets/Trevize-Compass/deployment/operations.md
  description: Runbook (start/stop/backup/restore)

# === Phase 5 : Backup et résilience (J+20) ===

Task 5.1:
  action: CREATE
  path: /opt/trevize-compass/scripts/backup.sh
  description: Dump Neo4j (neo4j-admin database dump) + rotation 7 jours
  pattern: backup-skill conventions

Task 5.2:
  action: CONFIGURE
  description: Cron quotidien 03:00 sur VM 105
  validation: crontab -l montre l'entrée

Task 5.3:
  action: TEST
  description: Reboot VM 105 → tous les containers reviennent UP, données intactes
  validation: ssh && docker ps && cypher count

# === Phase 6 : Intégration finale (J+21) ===

Task 6.1:
  action: MODIFY
  path: ~/.claude/CLAUDE.md
  description: Ajouter Trevize-Compass dans section "Warehouses Applications"
  pattern: lignes existantes pour Eco-Systèmes / SaaS MultiPass

Task 6.2:
  action: CREATE
  path: ~/Documents/Knowledge/Concepts/C_Trevize-Compass-Boule-De-Cristal-MultiPass.md
  description: Note Zettelkasten parente (frontmatter + thèse atomique + wikilinks)
  encoding: UTF-8 sans BOM
  pattern: notes Concepts/ existantes

Task 6.3:
  action: TEST
  description: Validation finale 3 niveaux (voir Validation Loop)

# ====================================================================
# === Phase 2.5 — PRIM RADIANT MINIMAL (J+22 à J+45, post-MVP) ===
# ====================================================================
# OBJECTIF : passer de Boule de Cristal (lecture seule) à Prim Radiant
# (manipulation + what-if + Crises Seldon + annotations partagées).
# Voir [[C_Trevize-Compass-Prim-Radiant-N51-N52]] pour la métaphore-cadre.

Task PR.1:
  action: EXTEND
  path: /opt/trevize-compass/sync/sync_to_neo4j.py
  description: Ajouter le support des labels :Crisis, :Branch, :Law
    et le upsert des champs is_seldon_crisis, crisis_probability, crisis_status
  pattern: les champs sont déjà déclarés dans le schema MVP (réservés)

Task PR.2:
  action: CREATE
  path: /opt/trevize-compass/api/server.py
  description: API HTTP minimale (FastAPI) pour mutations
    - POST /branch (clone du graph en branche what-if)
    - POST /annotation (ajout annotation utilisateur)
    - POST /crisis/mark (marquage Crise Seldon)
    - POST /crisis/probability (mise à jour probabilité)
  pattern: FastAPI standard, auth basic en MVP

Task PR.3:
  action: EXTEND
  path: /opt/trevize-compass/frontend/src/main.js
  description: Activer les événements Cytoscape de manipulation
    - drag temporel d'un node (modifier M_days en branche éphémère)
    - shift+click → marquer Crise Seldon
    - alt+click → ouvrir modal annotation

Task PR.4:
  action: CREATE
  path: /opt/trevize-compass/frontend/src/whatif.js
  description: Mode what-if (branche éphémère + comparaison côte-à-côte)

Task PR.5:
  action: CREATE
  path: /opt/trevize-compass/frontend/src/crisis.js
  description: Marquage visuel Crises Seldon (étoiles dorées,
    gradient de probabilité, animation pulsation)

Task PR.6:
  action: CREATE
  path: /opt/trevize-compass/frontend/src/annotation.js
  description: Modal annotation + auteur (Mike-N51 / Manu-N52)
    + opacité par auteur sur le graph

Task PR.7:
  action: CREATE
  path: /opt/trevize-compass/sync/push_annotations.py
  description: Push optionnel des annotations validées vers
    le frontmatter de la note vault correspondante

Task PR.8:
  action: DOCUMENT
  path: ~/Documents/Knowledge/Projets/Trevize-Compass/architecture/prim-radiant-spec.md
  description: Documentation complète des capacités Prim Radiant minimal

# ====================================================================
# === Phase 3 — PRIM RADIANT COMPLET (J+46 à J+90, optionnel) ===
# ====================================================================
# OBJECTIF : 3D holographique Three.js + multi-user + projections paramétriques

Task P3.1:
  action: PROTOTYPE
  description: POC Three.js d'un graph 3D (équivalent Cytoscape mais en vraie 3D)
  effort: 1 semaine

Task P3.2:
  action: DESIGN
  description: Multi-user simultané avec WebSockets
    (Mike + Manu modifient en même temps avec présence visible)
  effort: 1 semaine

Task P3.3:
  action: IMPLEMENT
  description: Projections paramétriques sur les :Law
    (sliders pour modifier les paramètres des équations)
  effort: 1 semaine

# Phase 3 N'EST PAS dans le MVP J+21. Elle est documentée ici pour
# que l'architecture MVP la rende possible sans refactor majeur.
```

### Pseudocode des tâches critiques

#### parse_vault.py

```python
# /opt/trevize-compass/sync/parse_vault.py
"""
Parse les fichiers .md du vault Obsidian → liste de dicts prêts pour Neo4j.
"""
import re
import hashlib
import datetime
from pathlib import Path
import frontmatter  # python-frontmatter

T0 = datetime.date(2026, 5, 1)

WIKILINK_RE = re.compile(r'\[\[([^\]|#^]+)(?:[|#^][^\]]*)?\]\]')

# Patterns sémantiques détectables dans le corps de la note
SEMANTIC_PATTERNS = [
    (re.compile(r'→\s*\*\*?Confirme\*?\*?\s*:?\s*\[\[([^\]]+)\]\]', re.I), 'CONFIRME'),
    (re.compile(r'→\s*\*\*?Anticipe\*?\*?\s*:?\s*\[\[([^\]]+)\]\]', re.I), 'ANTICIPE'),
    (re.compile(r'→\s*\*\*?Contredit\*?\*?\s*:?\s*\[\[([^\]]+)\]\]', re.I), 'CONTREDIT'),
    (re.compile(r'→\s*\*\*?Lien\*?\*?\s*:?\s*\[\[([^\]]+)\]\]', re.I), 'RELATED_TO'),
]

# Patterns BOUCLE_EST_OUEST détectables (ex: "M-5 → M+5", "EST-OUEST")
EST_OUEST_RE = re.compile(r'(?:M[-+]\d+|EST.OUEST|EAST.WEST)', re.I)


def compute_M_relative(date_absolute):
    delta_days = (date_absolute - T0).days
    return {
        'M_days': delta_days,
        'M_months': round(delta_days / 30.44),
        'M_years': round(delta_days / 365.25, 2),
        'cardinal_axis': 'EST' if delta_days < 0 else ('OUEST' if delta_days > 0 else 'M0'),
    }


def parse_note(filepath: Path, vault_root: Path) -> dict:
    """Parse une note → dict node + relations."""
    text = filepath.read_text(encoding='utf-8')
    post = frontmatter.loads(text)
    metadata = post.metadata
    body = post.content

    # Date absolue
    date_field = metadata.get('date')
    if isinstance(date_field, str):
        date_absolute = datetime.date.fromisoformat(date_field)
    elif isinstance(date_field, datetime.date):
        date_absolute = date_field
    else:
        # Fallback : mtime du fichier
        date_absolute = datetime.date.fromtimestamp(filepath.stat().st_mtime)

    M = compute_M_relative(date_absolute)

    # Wikilinks bruts
    wikilinks = list(set(WIKILINK_RE.findall(body)))

    # Sémantique détectée
    semantic_links = []
    for pattern, sem_type in SEMANTIC_PATTERNS:
        for match in pattern.finditer(body):
            target = match.group(1).split('|')[0].split('#')[0].strip()
            semantic_links.append({'target': target, 'type': sem_type})

    # Detect EST-OUEST loops
    is_est_ouest_node = bool(EST_OUEST_RE.search(body))

    return {
        'node': {
            'id': filepath.stem,
            'title': metadata.get('title', filepath.stem),
            'path': str(filepath.relative_to(vault_root)),
            'date_absolute': date_absolute.isoformat(),
            **M,
            'level': metadata.get('level'),  # optionnel
            'pacte_status': metadata.get('status', 'seedling'),
            'tags': metadata.get('tags', []) or [],
            'body_excerpt': body[:300].strip(),
            'content_hash': hashlib.sha256(text.encode('utf-8')).hexdigest(),
            'publish_to_sferaC': metadata.get('publish_to_sferaC', False),
            'is_est_ouest_node': is_est_ouest_node,
        },
        'wikilinks': wikilinks,
        'semantic_links': semantic_links,
    }


def parse_vault_concepts(vault_root: Path) -> list[dict]:
    """Parse tous les .md dans Concepts/ + Projets/."""
    notes = []
    for sub in ['Concepts', 'Projets/MultiPass']:
        target = vault_root / sub
        if not target.exists():
            continue
        for md_file in target.rglob('*.md'):
            try:
                notes.append(parse_note(md_file, vault_root))
            except Exception as e:
                print(f"WARN: failed to parse {md_file}: {e}")
    return notes
```

#### sync_to_neo4j.py

```python
# /opt/trevize-compass/sync/sync_to_neo4j.py
"""
Sync les dicts produits par parse_vault.py vers Neo4j (MERGE-only).
"""
from neo4j import GraphDatabase

class Neo4jSync:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def apply_constraints(self):
        with self.driver.session() as s:
            s.run("CREATE CONSTRAINT note_id_unique IF NOT EXISTS FOR (n:Note) REQUIRE n.id IS UNIQUE")
            s.run("CREATE CONSTRAINT tag_name_unique IF NOT EXISTS FOR (t:Tag) REQUIRE t.name IS UNIQUE")
            s.run("CREATE INDEX note_date IF NOT EXISTS FOR (n:Note) ON (n.date_absolute)")
            s.run("CREATE INDEX note_M_days IF NOT EXISTS FOR (n:Note) ON (n.M_days)")
            s.run("CREATE INDEX note_status IF NOT EXISTS FOR (n:Note) ON (n.pacte_status)")

    def upsert_note(self, node):
        with self.driver.session() as s:
            s.run("""
                MERGE (n:Note {id: $id})
                SET n += $props
            """, id=node['id'], props=node)
            # Tags
            for tag in node.get('tags', []):
                s.run("""
                    MERGE (t:Tag {name: $name})
                    WITH t
                    MATCH (n:Note {id: $id})
                    MERGE (n)-[:TAGGED_WITH]->(t)
                """, name=tag, id=node['id'])

    def upsert_relationships(self, source_id, wikilinks, semantic_links):
        with self.driver.session() as s:
            # Wikilinks par défaut → RELATED_TO
            for target in wikilinks:
                s.run("""
                    MATCH (a:Note {id: $a})
                    MERGE (b:Note {id: $b})
                    MERGE (a)-[:RELATED_TO]->(b)
                """, a=source_id, b=target)
            # Sémantique explicite
            for link in semantic_links:
                # Cypher ne peut pas paramétrer le type de relation → string injection contrôlée
                rel_type = link['type']
                if rel_type not in ('CONFIRME', 'ANTICIPE', 'CONTREDIT', 'RELATED_TO', 'BOUCLE_EST_OUEST', 'DERIVES_FROM'):
                    continue  # safelist
                s.run(f"""
                    MATCH (a:Note {{id: $a}})
                    MERGE (b:Note {{id: $b}})
                    MERGE (a)-[:{rel_type}]->(b)
                """, a=source_id, b=link['target'])
```

#### layout-temporal.js (Cytoscape)

```javascript
// frontend/src/layout-temporal.js
/**
 * Layout custom : X = M_days * pixel_per_day, Y = level * row_height
 * + dispersion gaussienne sur Y pour les nodes au même niveau
 */
export function temporalLayoutPositions(node, opts) {
  const M = node.data('M_days') ?? 0;
  const level = node.data('level') ?? 0;
  const ppd = opts.pixelPerDay ?? 8;
  const rh = opts.rowHeight ?? 120;

  const x = M * ppd;
  const baseY = level * rh;
  // Dispersion stable basée sur hash de l'id
  const id = node.data('id') || '';
  const hash = [...id].reduce((a, c) => a + c.charCodeAt(0), 0);
  const yJitter = (hash % 40) - 20;
  return { x, y: baseY + yJitter };
}

export function applyTemporalLayout(cy, opts = {}) {
  cy.layout({
    name: 'preset',
    positions: (node) => temporalLayoutPositions(node, opts),
    fit: true,
    padding: 80,
  }).run();
}

// Granularité multi-échelle
export function setGranularity(cy, granularity) {
  // granularity: 'day' | 'month' | 'year'
  const ppd = { day: 8, month: 0.5, year: 0.04 }[granularity];
  applyTemporalLayout(cy, { pixelPerDay: ppd });
}
```

#### play-east-west.js

```javascript
// frontend/src/play-east-west.js
/**
 * Animation EST→OUEST avec bonds Fibonacci.
 * Phase 1 : révèle les nodes par ordre M_days croissant (passé → futur)
 * Phase 2 : trace les boucles EST-OUEST en bonds Fibonacci (1, 1, 2, 3, 5, 8, 13...)
 */
const FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34];

export async function playEastWest(cy, { speed = 200 } = {}) {
  // Phase 1 : révélation chronologique
  cy.elements().style('opacity', 0.1);
  const sortedNodes = cy.nodes().sort((a, b) =>
    (a.data('M_days') ?? 0) - (b.data('M_days') ?? 0)
  );
  for (const n of sortedNodes) {
    n.style('opacity', 1);
    await sleep(speed);
  }

  // Phase 2 : boucles Fibonacci
  const estouest = cy.edges('[type="BOUCLE_EST_OUEST"]');
  for (let i = 0; i < estouest.length; i++) {
    const edge = estouest[i];
    const fibStep = FIB[i % FIB.length];
    edge.style('line-color', '#d97706');
    edge.style('width', 2 + fibStep / 4);
    edge.style('curve-style', 'bezier');
    edge.flashClass('fib-pulse', speed * fibStep);
    await sleep(speed * fibStep);
  }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
```

#### docker-compose.sfera-a.yml (extrait critique)

```yaml
# /opt/trevize-compass/docker-compose.sfera-a.yml
# PATTERN: docker-skill best practices
# GOTCHA: Réseau dédié pour isolation des services
services:
  neo4j-sfera-a:
    image: neo4j:5-community
    container_name: trevize-neo4j-a
    ports:
      - "7474:7474"   # HTTP browser
      - "7687:7687"   # Bolt
    environment:
      NEO4J_AUTH: "neo4j/${NEO4J_PASSWORD}"
      NEO4J_PLUGINS: '["apoc"]'
      NEO4J_dbms_security_procedures_unrestricted: "apoc.*"
    volumes:
      - ./data/neo4j-a/data:/data
      - ./data/neo4j-a/logs:/logs
      - ./data/neo4j-a/import:/import
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:7474"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped
    networks: [trevize-net]

  neodash-a:
    image: neo4jlabs/neodash:latest
    container_name: trevize-neodash-a
    ports:
      - "5005:5005"
    environment:
      ssoEnabled: "false"
      standalone: "true"
      standaloneProtocol: "bolt"
      standaloneHost: "neo4j-sfera-a"
      standalonePort: "7687"
      standaloneDatabase: "neo4j"
    depends_on:
      neo4j-sfera-a:
        condition: service_healthy
    restart: unless-stopped
    networks: [trevize-net]

  frontend-a:
    build: ./frontend
    container_name: trevize-frontend-a
    ports:
      - "8090:80"
    environment:
      NEO4J_HTTP: "http://neo4j-sfera-a:7474"
    depends_on:
      neo4j-sfera-a:
        condition: service_healthy
    restart: unless-stopped
    networks: [trevize-net]

  sync-a:
    build: ./sync
    container_name: trevize-sync-a
    volumes:
      - ${VAULT_PATH}:/vault:ro
    environment:
      NEO4J_URI: "bolt://neo4j-sfera-a:7687"
      NEO4J_USER: "neo4j"
      NEO4J_PASSWORD: "${NEO4J_PASSWORD}"
      MODE: "watcher"
      VAULT_ROOT: "/vault"
    depends_on:
      neo4j-sfera-a:
        condition: service_healthy
    restart: unless-stopped
    networks: [trevize-net]

networks:
  trevize-net:
    driver: bridge
```

### Points d'intégration

```yaml
ROUTER:
  # Trevize-Compass est un PRODUIT, pas un skill standard.
  # Pas de keywords slash à ajouter au meta-router pour le MVP.
  # Phase 2 : éventuellement une commande utilitaire /trevize-sync
  optional_phase2:
    - keyword: "trevize"
      action: "commande utilitaire pour déclencher sync ou ouvrir UI"

VAULT:
  - Créer dossier projet : Knowledge/Projets/Trevize-Compass/
  - Créer note parente Concepts/C_Trevize-Compass-Boule-De-Cristal-MultiPass.md
  - Tags hiérarchiques :
    * doctrine/multipass
    * principes/trevize
    * principes/boule-de-cristal
    * tech/neo4j
    * tech/cytoscape

MCP:
  - Pas d'impact sur knowledge-assistant pour le MVP
  - Phase 3 : possibilité d'ajouter un MCP server "trevize-compass" exposant
    des queries Cypher pré-définies aux skills

CLAUDE.MD:
  - Ajouter section "Warehouses Applications" :
    * Trevize-Compass | /opt/trevize-compass/ (VM 105) | Neo4j + Cytoscape | POC

INTELLIGENCE_WAREHOUSE:
  - Trevize-Compass devient l'incarnation visuelle de la Loi Trevize
  - Cohérence brand : "Departement Trevize — Intelligence Warehouse" + "Trevize-Compass — Boule de Cristal"

BACKUP:
  - Intégration backup-skill : ajouter target trevize-compass dans /bak-* commands
  - Cron quotidien 03:00 sur VM 105 : neo4j-admin database dump

MONITORING:
  - Intégration monitoring-skill :
    * Beszel agent déjà sur VM 105 (à vérifier)
    * Ajouter Uptime Kuma checks pour ports 7474, 5005, 8090
    * ntfy alerte si un container down > 2 min
```

---

## Validation Loop

### Niveau 1 : Structure & Syntax (J+21)

```powershell
# === Côté Windows (vault) ===

# Frontmatter notes vault valides
$paths = @(
    "C:\Users\r2d2\Documents\Knowledge\Projets\Trevize-Compass\README.md",
    "C:\Users\r2d2\Documents\Knowledge\Concepts\C_Trevize-Compass-Boule-De-Cristal-MultiPass.md"
)
foreach ($p in $paths) {
    if (-not (Test-Path $p)) { Write-Error "MISSING: $p"; continue }
    $content = Get-Content $p -Raw
    if ($content -notmatch "^---\r?\n") { Write-Warning "Frontmatter manquant : $p" }
    $bytes = [System.IO.File]::ReadAllBytes($p)
    if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        Write-Warning "BOM detecte (devrait etre UTF-8 sans BOM) : $p"
    }
}

# CLAUDE.md mis à jour
$claude = Get-Content "C:\Users\r2d2\.claude\CLAUDE.md" -Raw
if ($claude -notmatch "Trevize-Compass") { Write-Error "CLAUDE.md non mis a jour" }
```

```bash
# === Côté VM 105 ===
# Fichiers présents
test -f /opt/trevize-compass/docker-compose.sfera-a.yml || echo "MISSING compose"
test -f /opt/trevize-compass/.env || echo "MISSING env"
test -f /opt/trevize-compass/sync/parse_vault.py || echo "MISSING parser"
test -f /opt/trevize-compass/sync/sync_to_neo4j.py || echo "MISSING sync"
test -f /opt/trevize-compass/frontend/src/main.js || echo "MISSING frontend main"
test -f /opt/trevize-compass/frontend/src/layout-temporal.js || echo "MISSING layout"
test -f /opt/trevize-compass/frontend/src/play-east-west.js || echo "MISSING play-east-west"

# Python syntax OK
python3 -m py_compile /opt/trevize-compass/sync/*.py

# YAML valide
python3 -c "import yaml; yaml.safe_load(open('/opt/trevize-compass/docker-compose.sfera-a.yml'))"
```

### Niveau 2 : Fonctionnel (J+21)

```bash
# Stack containers UP
docker ps --filter "name=trevize-" --format "table {{.Names}}\t{{.Status}}"
# Doit montrer : trevize-neo4j-a, trevize-neodash-a, trevize-frontend-a, trevize-sync-a (tous Up)

# Neo4j accepte connexions
curl -s -u neo4j:$NEO4J_PASSWORD http://192.168.1.161:7474/db/neo4j/cluster/overview | grep -q "neo4j" \
  && echo "OK Neo4j" || echo "FAIL Neo4j"

# NeoDash accessible
curl -sf http://192.168.1.161:5005 > /dev/null && echo "OK NeoDash" || echo "FAIL NeoDash"

# Front-end servi
curl -sf http://192.168.1.161:8090 | grep -q "Trevize" && echo "OK Front-end" || echo "FAIL Front-end"

# Données importées
docker exec trevize-neo4j-a cypher-shell -u neo4j -p $NEO4J_PASSWORD \
  "MATCH (n:Note) RETURN count(n) AS notes"
# Doit retourner >= 5

docker exec trevize-neo4j-a cypher-shell -u neo4j -p $NEO4J_PASSWORD \
  "MATCH ()-[r]->() RETURN type(r), count(r) ORDER BY count(r) DESC"
# Doit montrer RELATED_TO + au moins 1 CONFIRME ou ANTICIPE

# Sync incrémental fonctionne
echo "test" >> /vault/Concepts/C_DeepSeek-V4-Commoditisation-LLM.md
sleep 3
docker logs --tail 10 trevize-sync-a | grep -q "C_DeepSeek-V4" && echo "OK watcher" || echo "FAIL watcher"
git checkout -- /vault/Concepts/C_DeepSeek-V4-Commoditisation-LLM.md  # rollback
```

### Niveau 3 : Intégration (J+21)

```bash
# === Test reboot ===
ssh r2d2helm@192.168.1.161 "sudo reboot"
sleep 90
ssh r2d2helm@192.168.1.161 "docker ps --filter name=trevize-" \
  | grep -c "Up" \
  | awk '{ if ($1 >= 4) print "OK reboot"; else print "FAIL reboot" }'

# Données toujours là après reboot
docker exec trevize-neo4j-a cypher-shell -u neo4j -p $NEO4J_PASSWORD \
  "MATCH (n:Note) RETURN count(n)"

# Backup fonctionne
/opt/trevize-compass/scripts/backup.sh
ls -la /opt/trevize-compass/backups/ | tail -3
```

```powershell
# === Validation côté Windows ===

# Health vault
# /guardian-health --quick
# Health score doit rester ≥ 0.85

# Ouverture deep-link Obsidian
$testUrl = "obsidian://vault/Knowledge/Concepts/C_DeepSeek-V4-Commoditisation-LLM"
Start-Process $testUrl  # doit ouvrir Obsidian sur la note
```

---

## Checklist de validation finale

### Phase 0 — Préparation
- [ ] VM 105 SSH OK, Docker installé, espace ≥ 50 Go
- [ ] Vault accessible (git pull périodique sur VM 105)
- [ ] Dossier `Knowledge/Projets/Trevize-Compass/` créé

### Phase 1 — Stack Docker
- [ ] `docker-compose.sfera-a.yml` créé (UTF-8 sans BOM)
- [ ] `.env` configuré (`NEO4J_PASSWORD`, `VAULT_PATH`)
- [ ] 4 containers UP et healthy
- [ ] Schema Neo4j (constraints + index) appliqué

### Phase 2 — Sync
- [ ] `parse_vault.py` parse les 5 notes session sans erreur
- [ ] `sync_to_neo4j.py` MERGE sans casser les nodes existants
- [ ] CLI `sync-vault-to-graph.py` fonctionnelle (modes full + incremental)
- [ ] Watcher détecte modifs < 5s

### Phase 3 — Front-end
- [ ] Cytoscape rend les 5 notes + leurs liens
- [ ] Layout temporel correct (X = M_days, Y = level)
- [ ] Slider 3 granularités (jour/mois/année) fonctionnel
- [ ] Filtres par tag fonctionnels
- [ ] Tooltip + lien profond Obsidian
- [ ] 4 couleurs sémantiques visibles
- [ ] « Play EST-OUEST » anime au moins une boucle Fibonacci

### Phase 4 — Documentation
- [ ] README.md vault complet (frontmatter + install + usage)
- [ ] schema-neo4j.md documenté
- [ ] operations.md runbook complet

### Phase 5 — Backup
- [ ] `backup.sh` produit un dump valide
- [ ] Cron 03:00 actif
- [ ] Reboot VM 105 → données intactes

### Phase 6 — Intégration
- [ ] CLAUDE.md mis à jour (section Warehouses)
- [ ] `C_Trevize-Compass-Boule-De-Cristal-MultiPass.md` créée
- [ ] Aucun skill existant cassé
- [ ] `/guardian-health --quick` ≥ 0.85

---

## Anti-Patterns à éviter

- ❌ **Ne pas ajouter Bloom** (commercial) au lieu de NeoDash + Cytoscape custom — décision tranchée 2026-05-04
- ❌ **Ne pas fusionner Sferă-A et Sferă-C** sous prétexte de simplification — étanchéité physique = doctrine
- ❌ **Ne pas couper la dimension EST-OUEST** en MVP sous prétexte de scope — c'est la signature non-copiable
- ❌ **Ne pas hardcoder les paths** : utiliser `${VAULT_PATH}` et `.env`
- ❌ **Ne pas embellir** automatiquement le contenu des notes — pacte de vérité
- ❌ **Ne pas oublier** le marquage visuel des notes `seedling` / `anticipated` (UI distinguante)
- ❌ **Ne pas exposer** Sferă-A directement sur Internet — SSH only ou WireGuard
- ❌ **Ne pas livrer** sans READ-ME et runbook (Mike + Manu doivent pouvoir opérer sans docs externes)
- ❌ **Ne pas utiliser** `Set-Content` sans `-Encoding utf8NoBOM` côté Windows
- ❌ **Ne pas inventer** de chiffres dans la doc — tous les benchmarks viennent du vrai déploiement
- ❌ **Ne pas oublier que MVP = étape vers Prim Radiant** — déclarer dès le schema initial les champs `is_seldon_crisis`, `branch_id`, `annotations`, `parametric_law` même s'ils ne sont pas utilisés en MVP. Le but est d'éviter le refactor schema en Phase 2.5.
- ❌ **Ne pas exposer en Sferă-C publique** les capacités Prim Radiant (manipulation, what-if). Sferă-C reste Boule de Cristal — Sferă-A garde le Prim Radiant complet (cohérent pacte Asimov : la Seconde Foundation est opérante mais cachée).
- ❌ **Ne pas confondre** la métaphore Prim Radiant (prescriptive UX) avec une affirmation ontologique sur Mike-N51 / Manu-N52. La métaphore guide les choix produit, elle n'est pas un discours sur la nature des personnes.

---

## Risques projet identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Layout temporel Cytoscape complexe à styliser | Moyenne | Moyen | Réserver 2 jours dédiés J+11/J+12 ; fallback sur cose-bilkent si blocage |
| Race condition sync watcher × Obsidian | Moyenne | Faible | Debounce 500ms + queue + try/except resilient |
| Authentik non déployé sur VM 103 (Phase 2) | À vérifier | Moyen | Vérification J+22 ; sinon prévoir 1 jour install Authentik |
| Volume vault > 10 000 nodes en Phase 3 | Faible | Faible | Neo4j Community OK jusqu'à ~100 000, monitoring metrics |
| Adoption Mike + Manu | Moyenne | Élevé | Cas d'usage hebdomadaire dès J+21 (rituel "lundi Trevize") |
| Dilution doctrine | Moyenne | Moyen | Couche-24 transparency assumée + UI affichant `pacte_status` |
| Dérive scope (Phase 3 dans le MVP) | Élevée | Élevé | Discipline : Phase 3 est explicitement OUT pour le MVP J+21 |

---

## Score de confiance pour implémentation single-pass

**Score MVP J+21 (Boule de Cristal) : 7/10**
**Score Phase 2.5 J+45 (Prim Radiant minimal) : 6/10**
**Score Phase 3 J+90 (Prim Radiant complet) : 4/10** — créatif, à itérer

**Forces :**
- ✅ INITIAL.md riche et déjà tranché sur 7 dimensions
- ✅ Stack 100 % open-source documentée
- ✅ Pseudocode des morceaux critiques fourni dans le PRP
- ✅ Pattern docker-compose et conventions r2d2 connus
- ✅ Vault et notes seed déjà gravés (5 notes session 2026-05-04)
- ✅ Critères de succès clairs et mesurables
- ✅ Validation 3 niveaux exécutable

**Risques de single-pass :**
- ⚠️ Layout temporel Cytoscape custom = 1-2 itérations probables sur le rendu visuel
- ⚠️ Sync watcher robustesse à éprouver (race conditions Obsidian)
- ⚠️ Authentik intégration Phase 2 dépend de l'état actuel sur VM 103 — non-vérifié dans le PRP
- ⚠️ Animation Play EST-OUEST avec bonds Fibonacci = créatif, peut nécessiter 2-3 itérations UX

**Pour passer à 9/10**, il faudrait :
1. Vérifier l'état Authentik VM 103 avant de démarrer
2. Avoir un mock/wireframe UI validé avec Mike avant Phase 3
3. Avoir testé le parser sur 100 % du vault Concepts/ en dry-run avant l'import réel

**Recommandation pour /execute-prp :** procéder par phases avec validation explicite à chaque jalon, ne pas tout livrer en bloc à J+21. **Le MVP (Phases 0-6) est strict. La Phase 2.5 ne démarre que si le MVP est validé en usage par Mike + Manu** (rituel hebdomadaire stable au moins 1 mois). La Phase 3 reste optionnelle, à arbitrer après la Phase 2.5.

---

## Notes pour /execute-prp

L'agent qui exécute ce PRP doit :

1. **Respecter strictement l'ordre des phases** — pas de Phase 3 avant Phase 2
2. **Valider à chaque jalon** avant de passer au suivant (ne pas accumuler des dettes de validation)
3. **Documenter les écarts** au PRP dans `Projets/Trevize-Compass/decisions/` (date + raison + impact)
4. **Demander confirmation** avant les actions risquées (reboot VM, modification CLAUDE.md, suppression)
5. **Préserver l'esprit** : Trevize-Compass est une **boule de cristal**, pas un dashboard de DRH. La métaphore guide les choix UX.

Bonne route, agent. La doctrine MultiPass attend sa boule de cristal. 🔮🦉🌹
