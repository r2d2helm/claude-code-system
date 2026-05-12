---
name: intel-graph
description: Visualiser les clusters de connexions
---

# /intel-graph - Visualisation des clusters

## Cible : $ARGUMENTS

Affiche une vue du graphe de connexions : stats globales, clusters, et relations entre findings.

## Processus

### 1. Stats globales

```sql
SELECT COUNT(*) as total FROM findings;
SELECT COUNT(*) as total FROM connections;
SELECT COUNT(*) as total FROM opportunities WHERE status != 'expired';
SELECT COUNT(*) as total FROM threats WHERE status = 'active';
```

### 2. Identifier les clusters

Recuperer toutes les connexions et construire les composantes connexes :
- Un cluster = groupe de findings lies par au moins une connexion
- Ignorer les findings isoles (pas de connexion)

Pour chaque cluster :
- Nombre de findings
- Score moyen
- Theme dominant (tags les plus frequents)
- Connexion la plus forte
- Opportunities liees

### 3. Top 5 clusters

Trier les clusters par :
1. Nombre de findings (desc)
2. Score moyen (desc)
3. Force maximale de connexion (desc)

### 4. Graphe textuel

Pour chaque cluster du top 5, afficher une representation textuelle :

```
Cluster "Migration VMware" (4 findings, score moy. 4.2)
  [#38 Proxmox 9.0] --thematic(0.6)--> [#42 Broadcom PME]
  [#42 Broadcom PME] --causal(0.9)--> [#35 Cheque cyber]
  [#35 Cheque cyber] --complementary(0.7)--> [#44 ESN belges]
  -> OPP-7 "Pack Migration VMware PME"
```

## Format de sortie

```
# Intelligence Graph

## Stats globales
- Findings : 45
- Connexions : 67
- Clusters : 8 (dont 5 de 3+ findings)
- Opportunities actives : 3
- Threats actifs : 1
- Findings isoles : 12

## Top 5 Clusters

### 1. Migration VMware (4 findings, score moy. 4.2)
Theme : VMware, Proxmox, migration, lock-in
[#38] --thematic(0.6)--> [#42] --causal(0.9)--> [#35] --complementary(0.7)--> [#44]
-> OPP-7 "Pack Migration VMware PME" (detected)

### 2. AI Act Compliance (3 findings, score moy. 3.7)
Theme : AI Act, LLM, conformite, PME
[#40] --thematic(0.5)--> [#41] --complementary(0.7)--> [#43]
-> OPP-8 "Pack Conformite AI Act" (validated)

### 3. Cybersecurite PME (3 findings, score moy. 3.3)
Theme : CVE, audit, cybersecurite
[#33] --thematic(0.5)--> [#36] --temporal(0.3)--> [#39]
-> Pas d'opportunity liee

...
```

## Arguments

- `--all` : afficher tous les clusters (pas seulement top 5)
- `--cluster=N` : detail d'un cluster specifique

## Exemples

```
/intel-graph
/intel-graph --all
/intel-graph --cluster=1
```
