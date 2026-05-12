# /rd-scan — Scan technologique

Effectue un scan rapide sur un sujet technologique : recherche web, evaluation, scoring R&D, et sauvegarde optionnelle dans le catalogue.

## Usage

```
/rd-scan {sujet}
/rd-scan ESP32 voice assistant
/rd-scan robotique industrielle PME
/rd-scan LLM quantise edge inference
```

## Processus

### 1. Recherche web
- 2-3 WebSearch ciblees sur le sujet
- Focus : projets open source, GitHub, benchmarks, couts
- Priorite aux sources techniques (GitHub, arxiv, HackerNews, CNX Software)

### 2. Evaluation
Pour chaque technologie trouvee, evaluer :

| Dimension | Question |
|-----------|----------|
| **Maturite** (1-5) | Est-ce pret a l'emploi ou encore experimental ? |
| **Pertinence** (1-5) | Est-ce aligne avec les axes R2D2 (edge, frugal, souverain, PME) ? |
| **Accessibilite** (1-5) | Peut-on le tester avec nos moyens (budget ~0-100 EUR, VM105) ? |

### 3. Scoring
- Score R&D = moyenne des 3 dimensions
- Score >= 4 : **A PROTOTYPER** (ajouter au backlog)
- Score >= 3 : **A SURVEILLER** (ajouter a la watch-list)
- Score < 3 : **ARCHIVE** (noter mais pas prioritaire)

### 4. Output
- Tableau recapitulatif en console
- Si score >= 4 : proposer creation d'une note vault `C_RD-{Technologie}.md`
- Mise a jour du catalogue (`data/catalog.json`)

## Exemple de sortie

```
=== RD-SCAN : ESP32 voice assistant ===

| Projet | Maturite | Pertinence | Accessibilite | Score | Status |
|--------|----------|------------|---------------|-------|--------|
| zclaw | 4 | 5 | 5 | 4.7 | A PROTOTYPER |
| ESP32-AI | 3 | 4 | 5 | 4.0 | A PROTOTYPER |
| ESP32 Agent Dev Kit | 4 | 4 | 3 | 3.7 | SURVEILLER |

Recommandation : Prototyper zclaw sur VM105 avec ESP32-S3
Budget estime : 5-15 EUR (board) + 0 EUR (software open source)
```
