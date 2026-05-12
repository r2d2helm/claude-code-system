---
name: intel-stats
description: Dashboard du warehouse
---

# /intel-stats - Dashboard du warehouse

## Cible : $ARGUMENTS

Affiche un dashboard complet de l'etat du warehouse.

## Processus

### 1. Findings

```sql
-- Total
SELECT COUNT(*) FROM findings;

-- Par categorie
SELECT category, COUNT(*) as cnt FROM findings GROUP BY category;

-- Par score
SELECT seldon_score, COUNT(*) as cnt FROM findings GROUP BY seldon_score ORDER BY seldon_score DESC;

-- Cette semaine
SELECT COUNT(*) FROM findings WHERE ingested_at >= datetime('now', '-7 days');

-- Ce mois
SELECT COUNT(*) FROM findings WHERE ingested_at >= datetime('now', '-30 days');
```

### 2. Connexions

```sql
-- Total
SELECT COUNT(*) FROM connections;

-- Par type
SELECT connection_type, COUNT(*) as cnt FROM connections GROUP BY connection_type;

-- Force moyenne
SELECT AVG(strength) FROM connections;
```

### 3. Opportunities

```sql
SELECT status, COUNT(*) as cnt FROM opportunities GROUP BY status;
```

### 4. Threats

```sql
SELECT status, COUNT(*) as cnt FROM threats GROUP BY status;
```

### 5. Top tags

Extraire tous les tags JSON des findings, compter les occurrences, afficher top 10.

### 6. Coverage

Verifier quelles categories ont au moins un finding cette semaine :
- IT_Tech, Business_Reglementaire, Concurrence, Strategique, Operationnel
- Calculer le % de couverture

## Format de sortie

```
# Intelligence Warehouse Dashboard

## Vue d'ensemble
| Metrique | Valeur |
|----------|--------|
| Findings total | 45 |
| Findings (7j) | 12 |
| Findings (30j) | 38 |
| Connexions | 67 |
| Force moyenne | 0.54 |
| Clusters (3+) | 5 |

## Findings par categorie
| Categorie | Count | % |
|-----------|-------|---|
| IT_Tech | 18 | 40% |
| Business_Reglementaire | 12 | 27% |
| Strategique | 9 | 20% |
| Concurrence | 4 | 9% |
| Operationnel | 2 | 4% |

## Findings par score
| Score | Count |
|-------|-------|
| 5/5 | 3 |
| 4/5 | 12 |
| 3/5 | 15 |
| 2/5 | 10 |
| 1/5 | 5 |

## Connexions par type
| Type | Count |
|------|-------|
| thematic | 28 |
| temporal | 15 |
| complementary | 14 |
| causal | 10 |

## Opportunity Cards
| Status | Count |
|--------|-------|
| detected | 2 |
| validated | 1 |
| activated | 0 |
| expired | 1 |

## Threat Alerts
| Status | Count |
|--------|-------|
| active | 1 |
| mitigated | 2 |

## Top 10 Tags
1. cybersecurite (12)
2. VMware (8)
3. souverainete (7)
4. PME (6)
5. IA (5)
...

## Coverage cette semaine : 80% (4/5 categories)
- IT_Tech : 5 findings
- Business_Reglementaire : 3 findings
- Strategique : 2 findings
- Concurrence : 2 findings
- Operationnel : 0 findings (MANQUANT)
```

## Exemples

```
/intel-stats
```
