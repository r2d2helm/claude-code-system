---
name: intelligence-warehouse-skill
description: "Departement Trevize — Intelligence strategique : ingestion, analyse croisee, detection de patterns, Opportunity Cards, Threat Alerts. Cerveau analytique R2D2."
prefix: /intel-*
---

# Departement Trevize — Intelligence Warehouse

> **Loi Fondamentale de Trevize : Les patterns emergent AVANT que la realite les confirme.**

Nomme d'apres Golan Trevize (Foundation, Asimov) : le Don de predire juste a partir de donnees incompletes. Gaia l'a choisi pour ca.

## Philosophie

> "L'ANTICIPATION est le coeur de tout -- On ne vend pas le poisson, on montre ou il sera demain."

Le Warehouse ne stocke pas des articles. Il detecte des CONVERGENCES et les transforme en ACTIONS.

### Corollaires de la Loi Trevize
1. La completude des donnees n'est pas necessaire. La qualite des CONNEXIONS l'est.
2. Un signal = bruit. Deux = coincidence. Trois qui convergent = PATTERN. Le pattern EST la prediction.
3. L'intervalle entre pattern et confirmation = fenetre d'action.
4. Seldon (equations, macro) + Trevize (intuition, terrain) = anticipation complete.

## Architecture 5 couches (v2)

```
COUCHE 1 - COLLECTE (automatique, quotidienne)
   Press-review 8h + 4 agents thematiques 12h + sources RSS + WebSearch
          |
COUCHE 2 - VERIFICATION (qualite, confiance)
   Score confiance source (1-5) + cross-ref + detection contradictions
          |
COUCHE 3 - ANALYSE (connexions, patterns)
   Warehouse SQLite + connexions auto + clustering thematique
   LOI TREVIZE : 3+ signaux convergents = pattern emergent
          |
COUCHE 4 - SYNTHESE (actionnable)
   Opportunity Cards + Threat Alerts + Weekly Brief + Dashboard SaaS
          |
COUCHE 5 - FEEDBACK (apprentissage)
   Table actions + ROI mesure + ajustement scoring Seldon
```

### Pipeline automatise (Task Scheduler Windows)
| Tache | Horaire | Script |
|-------|---------|--------|
| Press Review | Lun-Ven 8h | `automation/press-review-daily.ps1` |
| Intel Ingest | Lun-Ven 8h30 | `automation/intel-ingest-daily.ps1` |
| Agents Trevize | Lun-Ven 12h | `automation/trevize-agents-daily.ps1` |
| Weekly Brief | Lundi 9h | `automation/intel-weekly-brief.ps1` |

### Agents thematiques (4 agents P1)
| Agent | Theme | Focus |
|-------|-------|-------|
| agent-souverainete | CLOUD Act, alternatives EU | Politique + migrations + open source |
| agent-nis2 | Conformite NIS2 Belgique | Deadline + amendes + supply chain |
| agent-ia | IA agentique + multi-agents | ROI + echecs + democratisation |
| agent-saaspocalypse | Mort du SaaS par licence | Migration + self-hosted + TCO |

## Sources d'ingestion

| Source | Methode | Commande |
|--------|---------|----------|
| Press-review vault | Parse note existante | `/intel-ingest --from-press-review` |
| Texte manuel | Mike colle un article | `/intel-ingest` |
| Note vault | Ingere une note | `/intel-ingest --from-vault <path>` |

## Commandes Slash

### Ingestion & Recherche

| Commande | Description |
|----------|-------------|
| `/intel-ingest` | Ingerer des trouvailles (press-review, manuel, vault) |
| `/intel-search` | Rechercher dans le warehouse (full-text, filtres) |

### Analyse & Detection

| Commande | Description |
|----------|-------------|
| `/intel-analyze` | Detecter connexions et patterns dans les findings recents |
| `/intel-weekly` | Brief strategique hebdomadaire complet |

### Opportunities & Threats

| Commande | Description |
|----------|-------------|
| `/intel-opportunities` | Gerer les Opportunity Cards (list, create, validate, activate, expire) |
| `/intel-threats` | Gerer les Threat Alerts (list, create, mitigate) |

### Visualisation & Export

| Commande | Description |
|----------|-------------|
| `/intel-graph` | Visualiser les clusters de connexions |
| `/intel-export` | Exporter vers R2D2 Agent (JSON structure) |
| `/intel-stats` | Dashboard du warehouse |

### Trevize (v2)

| Commande | Description |
|----------|-------------|
| `/intel-trevize` | Detecter patterns emergents (Loi Trevize : 3+ signaux = pattern) |
| `/intel-confidence` | Auditer et ajuster les scores de confiance des sources |
| `/intel-contradictions` | Lister les contradictions detectees entre findings |
| `/intel-tracking` | Suivi temporel des stats cles (evolution dans le temps) |
| `/intel-feedback` | Enregistrer une action et son resultat (feedback loop) |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/intel-wizard setup` | Configuration initiale (init SQLite, verif vault, test) |
| `/intel-wizard cross-ref` | Assistant interactif de cross-referencing |
| `/intel-wizard agents` | Lancer manuellement les 4 agents thematiques |

## Schema SQLite (warehouse.db)

La base est creee par le wizard setup. Mode WAL pour la concurrence.

### Table findings (v2)
```sql
CREATE TABLE findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    source TEXT,
    url TEXT,
    category TEXT CHECK(category IN ('IT_Tech','Business_Reglementaire','Concurrence','Strategique','Operationnel')),
    summary TEXT,
    key_points TEXT,       -- JSON array
    seldon_score INTEGER CHECK(seldon_score BETWEEN 1 AND 5),
    confidence INTEGER DEFAULT 3 CHECK(confidence BETWEEN 1 AND 5),  -- v2: score confiance source
    tags TEXT,              -- JSON array
    entities TEXT,          -- JSON array
    deep_analysis TEXT,     -- v2: analyse approfondie (JSON, pour findings score 5)
    vault_note_path TEXT,
    ingested_at TEXT NOT NULL,
    article_date TEXT,
    source_type TEXT CHECK(source_type IN ('press_review','manual','vault','mcp','agent_search'))
);
-- Impact = seldon_score * confidence / 5
```

### Table connections
```sql
CREATE TABLE connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    finding_id_a INTEGER REFERENCES findings(id),
    finding_id_b INTEGER REFERENCES findings(id),
    connection_type TEXT CHECK(connection_type IN ('thematic','temporal','complementary','causal')),
    strength REAL CHECK(strength BETWEEN 0 AND 1),
    rule_name TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
```

### Table opportunities
```sql
CREATE TABLE opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    urgency INTEGER CHECK(urgency BETWEEN 1 AND 5),
    potential_value TEXT,
    description TEXT,
    pitch TEXT,
    required_skills TEXT,   -- JSON array
    financial_levers TEXT,  -- JSON array
    finding_ids TEXT,       -- JSON array
    status TEXT CHECK(status IN ('detected','validated','activated','expired')) DEFAULT 'detected',
    vault_note_path TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    expires_at TEXT
);
```

### Table threats
```sql
CREATE TABLE threats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    severity INTEGER CHECK(severity BETWEEN 1 AND 5),
    description TEXT,
    mitigation TEXT,
    finding_ids TEXT,       -- JSON array
    status TEXT CHECK(status IN ('active','mitigated','expired')) DEFAULT 'active',
    vault_note_path TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
```

## Scoring Seldon

Reutilise le meme scoring que press-review-skill :

| Score | Signification | Action |
|-------|---------------|--------|
| 5/5 | Actionnable immediatement | Agir dans les 24h |
| 4/5 | Tres pertinent, argument commercial | Integrer au pitch |
| 3/5 | Pertinent, contexte strategique | Surveiller |
| 2/5 | Interessant | Archiver |
| 1/5 | Information generale | Ignorer sauf tendance |

## Skill Matching

Le fichier `data/skill-registry.json` mappe les 22 skills R2D2 vers leurs capabilities et mots-cles marche. Lors de l'analyse, chaque cluster de findings est croise avec ce registre pour identifier quels packs R2D2 sont pertinents.

## Detection de connexions

Le fichier `data/connection-rules.json` definit 5 regles deterministes :

1. **shared_tags** : 2+ tags identiques (strength 0.5)
2. **same_entity** : meme entreprise/technologie (strength 0.6)
3. **temporal_proximity** : meme semaine + meme categorie (strength 0.3)
4. **complementary_categories** : IT + Business sur meme sujet (strength 0.7)
5. **opportunity_trigger** : score 4-5 + levier financier (strength 0.9)

## Workflow principal

```
/intel-ingest (quotidien, apres press-review)
    |
    v
findings stockes + connexions detectees
    |
    v
/intel-analyze (2-3x par semaine)
    |
    v
Opportunity Cards + Threat Alerts generes
    |
    v
/intel-weekly (chaque lundi)
    |
    v
Brief strategique pour Mike
    |
    v
/intel-export (si opportunite actionnable)
    |
    v
JSON vers R2D2 Agent Telegram
```

## Conventions

### Notes vault
- **Findings** : `Knowledge/References/Intel/YYYY-MM-DD_Intel_Title.md`
- **Briefs** : `Knowledge/References/Intel/Briefs/YYYY-MM-DD_Brief_Title.md`
- **Opportunities** : `Knowledge/References/Intel/OPP-{id}_Title.md`
- **Threats** : `Knowledge/References/Intel/THR-{id}_Title.md`
- **Frontmatter** : type `reference`, tags `intel/finding`, `intel/opportunity`, `intel/brief`, `intel/threat`
- **Wikilinks** : lien vers `[[MOC-Intelligence]]`
- **Template** : voir `templates/`

### Donnees
- **warehouse.db** : SQLite WAL, cree par wizard setup
- **skill-registry.json** : mapping skills -> capabilities (MAJ manuelle)
- **connection-rules.json** : regles de detection (MAJ manuelle)

### Integration press-review-skill
Le warehouse est le consommateur naturel des notes press-review :
```
/press-review -> note vault -> /intel-ingest --from-press-review -> warehouse
```

## References

- Algorithme de scoring : `references/scoring-algorithm.md`
- Integration vault : `references/vault-integration.md`
- Registre des skills : `data/skill-registry.json`
- Regles de connexion : `data/connection-rules.json`
- Templates : `templates/`
