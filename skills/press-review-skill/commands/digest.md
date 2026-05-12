# Commande: /press-digest

Resume consolide des revues de presse sur une periode (hebdo ou mensuel).

## Syntaxe

```
/press-digest <weekly|monthly> [--dry-run]
```

## Arguments

| Argument | Description | Requis |
|----------|-------------|--------|
| `weekly` | Resume de la semaine ecoulee | Oui (ou monthly) |
| `monthly` | Resume du mois ecoule | Oui (ou weekly) |
| `--dry-run` | Previsualiser sans ecrire | Non |

## Processus

### 1. Collecter les revues de la periode

- Lire `data/history.json` pour identifier les revues de la periode
- Lire les notes vault correspondantes dans `Knowledge/References/`
- Si aucune revue trouvee : suggerer `/press-review` d'abord

### 2. Agreger les donnees

Pour chaque categorie :
- Compter les articles par score (5/5, 4/5, etc.)
- Extraire les articles score 4+ (les plus pertinents)
- Identifier les themes recurrents (mots-cles les plus frequents)
- Lister les opportunites et menaces

### 3. Generer la note digest

**Chemin** : `Knowledge/References/YYYY-MM-DD_Press-Digest-Weekly.md` ou `...-Monthly.md`

**Structure** :
```markdown
---
title: "Digest Presse - Semaine du {date_debut} au {date_fin}"
date: {YYYY-MM-DD}
type: reference
status: seedling
tags:
  - veille/press-digest
  - business/plan-seldon
related:
  - "[[YYYY-MM-DD_Press-Review]]"
---

# Digest Presse - Semaine {N}

## Chiffres cles
- Revues effectuees : N
- Articles analyses : N
- Score moyen : X/5
- Articles 4+/5 : N

## Top Articles (score 4+)

| Titre | Cat. | Score | Source | Date |
|-------|------|-------|--------|------|

## Tendances par categorie

### IT / Tech
- Theme dominant : ...
- Signal faible : ...

### Business / Reglementaire
- Theme dominant : ...
- Signal faible : ...

### Concurrence
- Theme dominant : ...
- Signal faible : ...

### Strategique
- Theme dominant : ...
- Signal faible : ...

## Pertinence Plan Seldon

### Opportunites detectees
1. ...

### Menaces identifiees
1. ...

### Actions prioritaires
- [ ] ...

## Evolution des scores
[Comparaison avec la periode precedente si disponible]
```

### 4. Lier a la Daily Note

- Ajouter le wikilink `[[YYYY-MM-DD_Press-Digest-Weekly]]` dans la daily note du jour

### 5. Afficher le resume console

```
=== Digest Hebdo - S13 (17-23 mars 2026) ===

Revues : 4 | Articles : 42 | Score moyen : 3.4/5

Top 3 articles :
  [5/5] AI Act : nouvelles obligations pour les PME (Politico EU)
  [5/5] Cheque cyber Wallonie : budget double (Digital Wallonia)
  [4/5] Microsoft admet failles CLOUD Act (Le Monde)

Tendance : hausse de la couverture "souverainete numerique" (+40% vs S12)
Note vault : Knowledge/References/2026-03-23_Press-Digest-Weekly.md
```

## Exemples

### Digest hebdomadaire
```
/press-digest weekly
```

### Digest mensuel en preview
```
/press-digest monthly --dry-run
```
