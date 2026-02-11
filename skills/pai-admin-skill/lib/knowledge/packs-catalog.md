# Catalogue Packs PAI v2.5

## Vue d'ensemble

23 packs au total : 5 infrastructure + 18 skills. Chaque pack est un répertoire avec README.md, INSTALL.md, VERIFY.md et src/.

## Ordre d'installation

```
Requis (installer en premier) :
1. pai-hook-system            ← Fondation (pas de dépendances)
2. pai-core-install           ← Dépend de hooks, inclut MEMORY

Infrastructure (installer ensuite) :
3. pai-statusline             ← Dépend de core-install
4. pai-voice-system           ← Dépend de hooks, core-install
5. pai-observability-server   ← Dépend de hooks

Skills (installer selon besoins) :
6+. pai-*-skill               ← La plupart dépendent de core-install uniquement
```

## Packs Infrastructure (5)

### pai-hook-system
- **Version** : 2.3.0
- **Catégorie** : Foundation
- **Dépendances** : aucune (ou pai-core-install selon version)
- **Contenu** : 15 hooks, 12 libs, 4 handlers
- **Description** : Framework automation événementiel — fondation de toutes les capacités hook

### pai-core-install
- **Version** : 2.3.0
- **Catégorie** : Core
- **Dépendances** : aucune
- **Contenu** : SKILL.md, 19 docs SYSTEM/, templates USER/, 4 workflows, 4 tools
- **Description** : Skills + Identity + Architecture — fondation complète avec routage, format réponse, système MEMORY

### pai-voice-system
- **Version** : 2.3.0
- **Catégorie** : Notifications
- **Dépendances** : Bun, ElevenLabs API key (optionnel)
- **Contenu** : server.ts, scripts start/stop/status, voices.json
- **Port** : 8888
- **Description** : Notifications vocales TTS ElevenLabs avec amélioration prosodie
- **Linux** : mpg123/mpv au lieu de afplay, notify-send au lieu de osascript

### pai-observability-server
- **Version** : 2.3.0
- **Catégorie** : Observability
- **Dépendances** : pai-hook-system
- **Contenu** : Backend Bun+TS, Frontend Vue 3+Vite, scripts manage.sh
- **Port** : 4000
- **Description** : Dashboard monitoring temps réel multi-agents avec WebSocket

### pai-statusline
- **Version** : non spécifiée
- **Catégorie** : Display
- **Dépendances** : core-install
- **Description** : Status line 4 modes avec signal apprentissage, usage contexte, indicateurs tendance

## Packs Skills (18)

### pai-agents-skill
- **Catégorie** : Delegation
- **Description** : Composition dynamique d'agents avec personnalités uniques, voix et combinaisons de traits

### pai-algorithm-skill
- **Catégorie** : Methodology
- **Description** : Implémentation The Algorithm — gestion ISC, classification effort, itération vérifiable

### pai-annualreports-skill
- **Catégorie** : Research
- **Description** : Agrégation rapports sécurité annuels et analyse paysage menaces

### pai-art-skill
- **Catégorie** : Creativity
- **Description** : Génération contenu visuel avec support multi-référence images et diagrammes techniques

### pai-brightdata-skill
- **Catégorie** : Scraping
- **Description** : Scraping progressif URLs avec intégration Bright Data et escalade tiers

### pai-browser-skill
- **Catégorie** : Automation
- **Description** : Automation navigateur debug-first avec Playwright — diagnostics always-on, auto-start session

### pai-council-skill
- **Catégorie** : Analysis
- **Description** : Système débat multi-agents pour explorer perspectives et atteindre consensus

### pai-createcli-skill
- **Catégorie** : Development
- **Description** : Génération outils CLI TypeScript avec runtime Bun

### pai-createskill-skill
- **Catégorie** : Development
- **Description** : Création et validation skills PAI avec structure correcte

### pai-firstprinciples-skill
- **Catégorie** : Analysis
- **Description** : Décomposition premiers principes et analyse cause racine

### pai-osint-skill
- **Catégorie** : Research
- **Description** : Collecte intelligence sources ouvertes et due diligence

### pai-privateinvestigator-skill
- **Catégorie** : Research
- **Description** : Recherche éthique de personnes pour reconnexion et vérification

### pai-prompting-skill
- **Catégorie** : Methodology
- **Description** : Système meta-prompting avec templates Handlebars et bonnes pratiques Claude

### pai-recon-skill
- **Catégorie** : Security
- **Description** : Reconnaissance sécurité, bug bounty, cartographie surface attaque

### pai-redteam-skill
- **Catégorie** : Security
- **Description** : Analyse adversariale avec 32 agents spécialisés pour stress-test idées

### pai-research-skill
- **Catégorie** : Research
- **Description** : Recherche multi-sources avec exécution agents parallèle et patterns Fabric

### pai-system-skill
- **Catégorie** : Maintenance
- **Description** : Vérifications intégrité système, mises à jour documentation, scan sécurité

### pai-telos-skill
- **Catégorie** : Life OS
- **Description** : Framework capture objectifs profonds — mission, objectifs, croyances, stratégies, apprentissages

## Structure d'un pack

```
pack-name/
├── README.md           # Vue d'ensemble, architecture, problème résolu
├── INSTALL.md          # Instructions installation étape par étape (wizard)
├── VERIFY.md           # Checklist vérification obligatoire
└── src/                # Code source réel
    ├── hooks/          # Implémentations hooks
    ├── tools/          # Outils CLI
    ├── skills/         # Définitions skills
    └── config/         # Fichiers configuration
```

## Installation d'un pack

### Via DA (recommandé)
```
Installe le pack pai-hook-system depuis /home/r2d2helm/Personal_AI_Infrastructure/Packs/pai-hook-system/.
Utilise PAI_DIR="~/.claude" et DA="R2D2".
```

### Manuelle
1. Lire README.md du pack
2. Suivre INSTALL.md étape par étape
3. Copier fichiers depuis src/
4. Compléter checklist VERIFY.md

## Chemins dans le dépôt

```
/home/r2d2helm/Personal_AI_Infrastructure/Packs/
├── pai-agents-skill/
├── pai-algorithm-skill/
├── pai-annualreports-skill/
├── pai-art-skill/
├── pai-brightdata-skill/
├── pai-browser-skill/
├── pai-core-install/
├── pai-council-skill/
├── pai-createcli-skill/
├── pai-createskill-skill/
├── pai-firstprinciples-skill/
├── pai-hook-system/
├── pai-observability-server/
├── pai-osint-skill/
├── pai-privateinvestigator-skill/
├── pai-prompting-skill/
├── pai-recon-skill/
├── pai-redteam-skill/
├── pai-research-skill/
├── pai-statusline/
├── pai-system-skill/
├── pai-telos-skill/
├── pai-voice-system/
└── README.md
```
