---
name: wizard-setup
description: Configuration initiale du warehouse
---

# Wizard : Setup Intelligence Warehouse

## Declencheur

```
/intel-wizard setup
```

## Etapes

### Etape 1 : Verifier les prerequis

1. Verifier que SQLite est accessible (via Python ou PowerShell)
2. Verifier que le vault Obsidian est accessible :
   - `C:\Users\r2d2\Documents\Knowledge\References\` existe
3. Verifier que press-review-skill est installe :
   - `~/.claude/skills/press-review-skill/SKILL.md` existe

Afficher :
```
## Prerequis
- SQLite : OK
- Vault Obsidian : OK
- Press-review-skill : OK
```

### Etape 2 : Creer la structure vault

Creer les dossiers si inexistants :
- `C:\Users\r2d2\Documents\Knowledge\References\Intel\`
- `C:\Users\r2d2\Documents\Knowledge\References\Intel\Briefs\`

### Etape 3 : Initialiser la base SQLite

Chemin : `~/.claude/skills/intelligence-warehouse-skill/data/warehouse.db`

```sql
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    source TEXT,
    url TEXT,
    category TEXT CHECK(category IN ('IT_Tech','Business_Reglementaire','Concurrence','Strategique','Operationnel')),
    summary TEXT,
    key_points TEXT,
    seldon_score INTEGER CHECK(seldon_score BETWEEN 1 AND 5),
    tags TEXT,
    entities TEXT,
    vault_note_path TEXT,
    ingested_at TEXT DEFAULT (datetime('now')),
    source_type TEXT CHECK(source_type IN ('press_review','manual','vault','mcp'))
);

CREATE TABLE IF NOT EXISTS connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    finding_id_a INTEGER REFERENCES findings(id),
    finding_id_b INTEGER REFERENCES findings(id),
    connection_type TEXT CHECK(connection_type IN ('thematic','temporal','complementary','causal')),
    strength REAL CHECK(strength BETWEEN 0 AND 1),
    rule_name TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    urgency INTEGER CHECK(urgency BETWEEN 1 AND 5),
    potential_value TEXT,
    description TEXT,
    pitch TEXT,
    required_skills TEXT,
    financial_levers TEXT,
    finding_ids TEXT,
    status TEXT CHECK(status IN ('detected','validated','activated','expired')) DEFAULT 'detected',
    vault_note_path TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    expires_at TEXT
);

CREATE TABLE IF NOT EXISTS threats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    severity INTEGER CHECK(severity BETWEEN 1 AND 5),
    description TEXT,
    mitigation TEXT,
    finding_ids TEXT,
    status TEXT CHECK(status IN ('active','mitigated','expired')) DEFAULT 'active',
    vault_note_path TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Index pour la recherche
CREATE INDEX IF NOT EXISTS idx_findings_category ON findings(category);
CREATE INDEX IF NOT EXISTS idx_findings_score ON findings(seldon_score);
CREATE INDEX IF NOT EXISTS idx_findings_date ON findings(ingested_at);
CREATE INDEX IF NOT EXISTS idx_connections_findings ON connections(finding_id_a, finding_id_b);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_threats_status ON threats(status);
```

### Etape 4 : Verifier les fichiers data

Confirmer que les fichiers suivants existent :
- `data/skill-registry.json`
- `data/connection-rules.json`

### Etape 5 : Test d'ingestion

Proposer un test rapide :
1. Inserer un finding de test
2. Verifier qu'il est bien stocke
3. Le supprimer

### Etape 6 : Resume

```
## Setup termine

- Base SQLite : ~/.claude/skills/intelligence-warehouse-skill/data/warehouse.db
- Tables : findings, connections, opportunities, threats
- Vault : Knowledge/References/Intel/ + Intel/Briefs/
- Fichiers data : skill-registry.json, connection-rules.json
- Status : OPERATIONNEL

Prochaine etape : /intel-ingest --from-press-review
```
