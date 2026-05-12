---
name: press-review-skill
description: "Revue de presse automatisee : veille IT/Tech, Business/Reglementaire, Concurrence, Strategique. Scan web + analyse Plan Seldon."
prefix: /press-*
---

# Super Agent Press Review

Agent intelligent de veille strategique : scan web automatise, analyse par categorie, scoring Plan Seldon, generation de notes vault.

## Philosophie

> "L'ANTICIPATION est le coeur de tout -- On ne vend pas le poisson, on montre ou il sera demain."

La revue de presse n'est pas une simple agregation de news. C'est un outil d'anticipation strategique qui :
1. Detecte les signaux faibles (subsides, reglementations, mouvements de marche)
2. Identifie les opportunites commerciales pour R2D2
3. Cartographie les menaces (lock-in, concurrence, reglementation)
4. Alimente l'argumentaire Plan Seldon avec des preuves concretes

## Categories de veille

| Categorie | Focus | Couleur |
|-----------|-------|---------|
| **IT / Tech** | IA, LLM, CVE, Docker, Proxmox, open source, souverainete | Bleu |
| **Business / Reglementaire** | Subsides wallons, AI Act, RGPD, aides PME | Vert |
| **Concurrence** | ESN Belgique, MSP, integrateurs open source | Orange |
| **Strategique** | Microsoft lock-in, CLOUD Act, Big Tech, Gaia-X | Rouge |

## Commandes Slash

### Revue

| Commande | Description |
|----------|-------------|
| `/press-review` | Revue complete : scan + analyse + note vault |
| `/press-quick` | Scan rapide console (titres + liens, pas de vault) |
| `/press-digest` | Resume consolide hebdo/mensuel |

### Gestion

| Commande | Description |
|----------|-------------|
| `/press-sources` | Gerer les sources (list, add, remove, enable/disable) |
| `/press-history` | Historique des revues passees |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/press-wizard setup` | Configuration initiale des sources et preferences |

## Scoring Plan Seldon

Chaque article est score sur sa pertinence pour le Plan Seldon R2D2.
Les mots-cles sont definis dans `data/seldon-keywords.json`.

| Score | Signification | Action |
|-------|---------------|--------|
| 5/5 | Actionnable immediatement pour R2D2 | Agir dans les 24h |
| 4/5 | Tres pertinent, argument commercial | Integrer au pitch |
| 3/5 | Pertinent, contexte strategique | Surveiller |
| 2/5 | Interessant, a surveiller | Archiver |
| 1/5 | Information generale | Ignorer sauf tendance |

### Calcul du score

1. **Mots-cles haute pertinence** (+2 chacun) : souverainete, local-first, open source, lock-in, CLOUD Act, subsides, cheque cybersecurite, PME, Wallonie, RGPD, AI Act, Proxmox, migration
2. **Mots-cles moyenne pertinence** (+1 chacun) : Docker, LLM, self-hosted, on-premise, ESN, integrateur, agents IA, agentique
3. **Boosters contexte** (+1 chacun) : Belgique, Europe, Afrique, digitalisation, micro-entreprise, auto-entrepreneur
4. **Score final** = min(5, somme / 2 arrondi superieur)

## Workflow principal

```
/press-review
    |
    v
1. Charger sources.json (sources actives par categorie)
    |
    v
2. WebSearch par categorie (mots-cles + date du jour)
    |
    v
3. WebFetch sur les articles les plus pertinents
    |
    v
4. Analyse : resume, points cles, score Seldon (1-5)
    |
    v
5. Generer note vault : Knowledge/References/YYYY-MM-DD_Press-Review.md
    |
    v
6. Lien dans la Daily Note du jour
    |
    v
7. Tableau recapitulatif console
```

## Conventions

### Notes vault
- **Chemin** : `C:\Users\r2d2\Documents\Knowledge\References\`
- **Nommage** : `YYYY-MM-DD_Press-Review.md` (ou `YYYY-MM-DD_Press-Review-IT.md` si filtre)
- **Frontmatter** : type `reference`, tags `veille/press-review` + `business/plan-seldon`
- **Wikilinks** : lien vers `[[YYYY-MM-DD]]` (daily note)
- **Template** : voir `templates/press-review-note.md`

### Donnees
- **sources.json** : sources actives par categorie avec requetes de recherche
- **history.json** : log des revues effectuees (date, articles trouves, scores)
- **seldon-keywords.json** : mots-cles pour le scoring

### Limites par defaut
- `/press-review` : max 5 WebSearch + 10 WebFetch par execution
- `/press-quick` : max 4 WebSearch (1 par categorie), 0 WebFetch
- `/press-digest` : agregation des notes vault existantes, pas de nouveau scan

## References

- Catalogue des sources : `references/source-catalog.md`
- Template note vault : `templates/press-review-note.md`
- Keywords Seldon : `data/seldon-keywords.json`
