---
name: intel-weekly
description: Brief strategique hebdomadaire complet
---

# /intel-weekly - Brief strategique hebdomadaire

## Cible : $ARGUMENTS

Genere un brief strategique hebdomadaire complet, agrege de toute l'activite du warehouse.

## Processus

### 1. Agreger les findings de la semaine

```sql
SELECT * FROM findings
WHERE ingested_at >= datetime('now', '-7 days')
ORDER BY seldon_score DESC, category;
```

Regrouper par categorie. Compter par score.

### 2. Nouvelles connexions

```sql
SELECT c.*, fa.title AS title_a, fb.title AS title_b
FROM connections c
JOIN findings fa ON c.finding_id_a = fa.id
JOIN findings fb ON c.finding_id_b = fb.id
WHERE c.created_at >= datetime('now', '-7 days')
ORDER BY c.strength DESC;
```

### 3. Opportunity Cards actives

```sql
SELECT * FROM opportunities
WHERE status IN ('detected', 'validated')
ORDER BY urgency DESC;
```

### 4. Threat Alerts actifs

```sql
SELECT * FROM threats
WHERE status = 'active'
ORDER BY severity DESC;
```

### 5. Tendances

Analyser les tags les plus frequents cette semaine vs la semaine precedente :
- Tags en hausse (nouveaux ou +50%)
- Tags en baisse
- Entites recurrentes

### 6. Recommandations

Claude genere 3-5 recommandations actionnables basees sur :
- Les opportunities a valider
- Les threats a mitiger
- Les tendances emergentes
- Les actions de la semaine precedente (si brief precedent existe)

### 7. Generer la note vault

- Chemin : `Knowledge/References/Intel/Briefs/YYYY-MM-DD_Brief_Hebdo.md`
- Template : `templates/intelligence-brief.md`
- Ajouter wikilink vers `[[MOC-Intelligence]]`

## Format de sortie

```
# Intelligence Brief Hebdomadaire - Semaine du 2026-03-18

## Chiffres cles
- Findings ingeres : 18
- Connexions detectees : 12
- Opportunity Cards : 2 nouvelles, 3 actives
- Threat Alerts : 1 nouveau, 1 actif

## Top findings (score >= 4)
| # | Titre | Cat. | Score |
|---|-------|------|-------|
| 42 | Migration VMware Broadcom | IT_Tech | 4/5 |
| 35 | Cheque cyber Wallonie | Business | 5/5 |
| ...

## Opportunities actives
| ID | Titre | Urgence | Status |
|----|-------|---------|--------|
| OPP-7 | Pack Migration VMware PME | 4/5 | detected |
| OPP-8 | Pack Conformite AI Act | 3/5 | validated |

## Threats actifs
| ID | Titre | Severite | Status |
|----|-------|----------|--------|
| THR-3 | OpenClaw variantes | 4/5 | active |

## Tendances
- En hausse : VMware migration, AI Act, souverainete
- Stable : cybersecurite PME
- En baisse : Docker Desktop licensing

## Recommandations
1. Valider OPP-7 et preparer le pitch cette semaine
2. Surveiller l'evolution AI Act (deadline Q2)
3. Mettre a jour la veille sur les variantes OpenClaw
```

## Exemples

```
/intel-weekly
```
