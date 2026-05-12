---
name: intel-search
description: Rechercher dans le warehouse
---

# /intel-search - Recherche dans le warehouse

## Cible : $ARGUMENTS

Recherche full-text dans toutes les tables du warehouse.

## Syntaxe

```
/intel-search <query>
/intel-search <query> --category=IT_Tech
/intel-search <query> --score=4+
/intel-search <query> --type=opportunities
/intel-search <query> --days=30
```

## Arguments

| Argument | Description | Defaut |
|----------|-------------|--------|
| `<query>` | Termes de recherche (requis) | - |
| `--category=X` | Filtrer par categorie | toutes |
| `--score=N+` | Score Seldon minimum | 1 |
| `--type=X` | Type : findings, opportunities, threats, all | all |
| `--days=N` | Limiter aux N derniers jours | illimite |

## Processus

### 1. Recherche findings

```sql
SELECT * FROM findings
WHERE (title LIKE '%{query}%' OR summary LIKE '%{query}%'
       OR key_points LIKE '%{query}%' OR tags LIKE '%{query}%'
       OR entities LIKE '%{query}%')
AND ({category_filter})
AND ({score_filter})
AND ({days_filter})
ORDER BY seldon_score DESC, ingested_at DESC
LIMIT 20;
```

### 2. Recherche opportunities (si type = all ou opportunities)

```sql
SELECT * FROM opportunities
WHERE (title LIKE '%{query}%' OR description LIKE '%{query}%'
       OR pitch LIKE '%{query}%')
AND status != 'expired'
ORDER BY urgency DESC;
```

### 3. Recherche threats (si type = all ou threats)

```sql
SELECT * FROM threats
WHERE (title LIKE '%{query}%' OR description LIKE '%{query}%')
AND status = 'active'
ORDER BY severity DESC;
```

## Format de sortie

```
# Recherche : "VMware"

## Findings (5 resultats)
| # | Titre | Cat. | Score | Date |
|---|-------|------|-------|------|
| 42 | Migration VMware Broadcom | IT_Tech | 4/5 | 2026-03-25 |
| 38 | Proxmox 9 alternative VMware | IT_Tech | 4/5 | 2026-03-22 |
| ...

## Opportunities (1 resultat)
| ID | Titre | Urgence | Status |
|----|-------|---------|--------|
| OPP-7 | Pack Migration VMware PME | 4/5 | detected |

## Threats (0 resultats)
Aucune menace active correspondante.
```

## Exemples

```
/intel-search VMware
/intel-search "cheque cyber" --category=Business_Reglementaire
/intel-search Proxmox --score=4+
/intel-search lock-in --type=threats
/intel-search IA souveraine --days=30
```
