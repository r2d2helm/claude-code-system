# Algorithme de Scoring Seldon

## Principe

Le scoring Seldon mesure la pertinence d'un finding pour le Plan Seldon R2D2. Il est identique a celui utilise par le press-review-skill pour assurer la coherence.

## Calcul

### Etape 1 : Comptage des mots-cles

**Haute pertinence (+2 chacun) :**
- souverainete, local-first, open source, lock-in, CLOUD Act
- subsides, cheque cybersecurite, cheque maturite numerique
- PME, Wallonie, Belgique, migration
- Proxmox, self-hosted, on-premise

**Moyenne pertinence (+1 chacun) :**
- Docker, LLM, AI Act, RGPD
- ESN, integrateur, MSP
- agents IA, agentique, automatisation
- cybersecurite, conformite, audit

**Boosters contexte (+1 chacun) :**
- Europe, Afrique, digitalisation
- micro-entreprise, auto-entrepreneur, freelance
- ransomware, breach, CVE critique

### Etape 2 : Score brut

```
score_brut = somme_haute * 2 + somme_moyenne * 1 + somme_boosters * 1
```

### Etape 3 : Normalisation

```
score_final = min(5, ceil(score_brut / 2))
```

## Interpretation

| Score | Signification | Action warehouse |
|-------|---------------|------------------|
| 5/5 | Actionnable immediatement | Ingerer + creer note vault + detection connexions prioritaire |
| 4/5 | Tres pertinent | Ingerer + creer note vault + detection connexions |
| 3/5 | Pertinent | Ingerer + detection connexions |
| 2/5 | Interessant | Ingerer (pas de note vault par defaut) |
| 1/5 | General | Ingerer si source fiable |

## Scoring des Opportunity Cards

L'urgence d'une Opportunity Card est calculee differemment :

```
urgence = ceil(score_moyen_cluster * facteur_levier * facteur_temporel)
```

- **facteur_levier** : 1.0 (pas de levier), 1.2 (levier disponible), 1.5 (levier avec deadline)
- **facteur_temporel** : 1.0 (pas de deadline), 1.3 (deadline < 3 mois), 1.5 (deadline < 1 mois)
- **urgence finale** : min(5, valeur calculee)

## Scoring des connexions

La force d'une connexion est definie par les regles dans `connection-rules.json` :

| Regle | Force | Justification |
|-------|-------|---------------|
| shared_tags | 0.5 | Lien thematique modere |
| same_entity | 0.6 | Meme acteur = lien fort |
| temporal_proximity | 0.3 | Correlation temporelle faible |
| complementary_categories | 0.7 | Cross-domain = insight riche |
| opportunity_trigger | 0.9 | Convergence actionnable |

Quand plusieurs regles s'appliquent entre deux findings, la force finale est :
```
force_finale = min(1.0, max(forces_individuelles) + 0.1 * (nb_regles - 1))
```
