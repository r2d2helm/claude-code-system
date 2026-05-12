---
name: intel-analyze
description: Detecter connexions et patterns dans les findings recents
---

# /intel-analyze - Analyse croisee et detection de patterns

## Cible : $ARGUMENTS

Analyse les findings recents pour detecter des patterns, clusters et generer des Opportunity Cards / Threat Alerts.

## Arguments

- `--days=N` : analyser les N derniers jours (defaut 7)
- `--category=X` : filtrer par categorie (IT_Tech, Business_Reglementaire, Concurrence, Strategique)

## Processus

### 1. Collecte des findings

```sql
SELECT * FROM findings
WHERE seldon_score >= 3
AND ingested_at >= datetime('now', '-{days} days')
ORDER BY seldon_score DESC, ingested_at DESC;
```

Si `--category` est specifie, ajouter le filtre.

### 2. Reconstruction du graphe de connexions

```sql
SELECT c.*, fa.title AS title_a, fb.title AS title_b
FROM connections c
JOIN findings fa ON c.finding_id_a = fa.id
JOIN findings fb ON c.finding_id_b = fb.id
WHERE c.finding_id_a IN ({ids}) OR c.finding_id_b IN ({ids});
```

### 3. Detection de clusters

Identifier les groupes de findings interconnectes (composantes connexes du graphe) :
- Un cluster = groupe de 3+ findings lies par des connexions
- Calculer le score moyen du cluster
- Identifier le theme dominant (tags les plus frequents)

### 4. Analyse de chaque cluster

Pour chaque cluster de 3+ findings :

**a) Skill matching :**
- Charger `data/skill-registry.json`
- Comparer les tags/entites du cluster aux `market_keywords` de chaque skill
- Lister les skills pertinents avec leurs `pack_potential`

**b) Levier financier :**
- Charger les `financial_levers` de `data/connection-rules.json`
- Verifier si des mots-cles financiers apparaissent dans les findings du cluster

**c) Decision :**
- Si convergence skill + levier + score moyen >= 4 -> **Opportunity Card**
- Si menace detectee (lock-in, CVE critique, reglementation contraignante) -> **Threat Alert**
- Sinon -> noter comme pattern a surveiller

### 5. Generation des Opportunity Cards

Pour chaque opportunite detectee :

1. Inserer dans la table `opportunities` :
   - title, category, urgency (base sur le score moyen)
   - potential_value (estime par Claude)
   - description (synthese du cluster)
   - pitch (argumentaire commercial pret a l'emploi)
   - required_skills (skills R2D2 necessaires)
   - financial_levers (leviers disponibles)
   - finding_ids (IDs des findings sources)
   - expires_at (estimation Claude)

2. Creer une note vault avec le template `templates/opportunity-card.md`

### 6. Generation des Threat Alerts

Pour chaque menace detectee :

1. Inserer dans la table `threats` :
   - title, category, severity
   - description, mitigation (proposee par Claude)
   - finding_ids

2. Creer une note vault avec le template `templates/threat-alert.md`

### 7. Intelligence Brief

Generer un resume de l'analyse :
- Nombre de findings analyses
- Clusters detectes
- Opportunities generees
- Threats generees
- Recommandations

## Format de sortie

```
# Intelligence Analysis - 2026-03-25

## Scope
- Periode : 7 derniers jours
- Findings analyses : 15 (score >= 3)
- Connexions : 23

## Clusters detectes

### Cluster 1 : Migration VMware (4 findings, score moy. 4.2)
- #38 "Proxmox 9.0 release" (IT_Tech, 4/5)
- #42 "Broadcom pousse les PME" (IT_Tech, 4/5)
- #35 "Cheque cyber Wallonie" (Business_Regl, 5/5)
- #44 "ESN belges en difficulte VMware" (Concurrence, 4/5)
-> OPPORTUNITY CARD generee : OPP-7 "Pack Migration VMware PME Wallonie"
   Skills : proxmox-skill, backup-skill, security-skill
   Levier : Cheque Cybersecurite 75% (60k EUR)

### Cluster 2 : AI Act compliance (3 findings, score moy. 3.7)
- #40 "AI Act entre en vigueur" (Business_Regl, 4/5)
- #41 "PME belges non preparees" (Strategique, 3/5)
- #43 "LLM souverains demande explose" (IT_Tech, 4/5)
-> OPPORTUNITY CARD generee : OPP-8 "Pack Conformite AI Act"
   Skills : ai-infra-skill, security-skill
   Levier : Cheque Maturite Numerique 50%

## Threat Alerts
- THR-3 "OpenClaw variantes actives" (severity 4/5)

## Recommandations
1. Preparer pitch "Migration VMware" pour la semaine prochaine
2. Surveiller AI Act timeline
3. Mettre a jour le security-skill avec les nouveaux CVE
```

## Exemples

```
/intel-analyze
/intel-analyze --days=14
/intel-analyze --category=IT_Tech
/intel-analyze --days=30 --category=Strategique
```
