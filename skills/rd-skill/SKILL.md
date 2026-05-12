# Departement R&D — Recherche et Developpement

Veille technologique, evaluation et prototypage des technologies emergentes pour l'ecosysteme R2D2. Couvre l'edge AI, la robotique, les modeles frugaux, l'IoT industriel et la souverainete technique.

## Philosophie

> "R2D2 : Recherche & Developpement. C'etait dans le nom depuis le debut."

Le departement R&D ne produit pas — il **anticipe**. Il explore les technologies emergentes, evalue leur potentiel, et prepare le terrain pour que R2D2 soit pret quand le marche l'est.

**Principes :**
- Frugalite : maximiser le resultat avec le minimum de ressources
- Open source first : pas de dependance proprietaire
- Local-first : tout ce qui peut tourner sans cloud DOIT tourner sans cloud
- Prototypage rapide : VM105 (r2d2-lab) est le terrain d'experimentation

## Axes de recherche

| Axe | Focus | Priorite |
|-----|-------|----------|
| **Edge AI / TinyML** | LLM quantises, inference locale, MCU, ESP32 | HAUTE |
| **Robotique** | Frameworks open source, robots DIY, embodied AI | HAUTE |
| **Modeles frugaux** | Bon modele = bonne tache, ratio cout/performance | HAUTE |
| **IoT industriel** | Capteurs, monitoring, maintenance predictive | MOYENNE |
| **Souverainete tech** | Self-hosted, chiffrement, zero cloud | HAUTE |
| **Hardware** | Arduino, ESP32, Raspberry Pi, MCU, impression 3D | MOYENNE |

## Commandes

| Commande | Description |
|----------|-------------|
| `/rd-scan` | Scan technologique : recherche web + evaluation + scoring |
| `/rd-evaluate` | Evaluation approfondie d'une technologie ou projet |
| `/rd-benchmark` | Benchmark comparatif (modeles, frameworks, hardware) |
| `/rd-prototype` | Guide de prototypage rapide sur VM105 |
| `/rd-watch` | Ajouter/gerer les sujets de veille technologique |
| `/rd-catalog` | Consulter le catalogue des technologies evaluees |
| `/rd-report` | Rapport R&D periodique (hebdo/mensuel) |

## Wizards

| Wizard | Description |
|--------|-------------|
| `/rd-wizard setup` | Configuration initiale du departement R&D |
| `/rd-wizard project` | Lancer un nouveau projet R&D structure |

## Scoring R&D

Chaque technologie evaluee recoit un score sur 3 dimensions :

| Dimension | Description | Echelle |
|-----------|-------------|---------|
| **Maturite** | Prete a l'emploi ou experimentale ? | 1-5 (1=recherche, 5=production) |
| **Pertinence** | Alignee avec les axes R2D2 ? | 1-5 (1=hors scope, 5=coeur de cible) |
| **Accessibilite** | Cout, complexite, prerequis ? | 1-5 (1=inaccessible, 5=plug-and-play) |

**Score R&D** = moyenne des 3 dimensions. Score >= 4 = a prototyper. Score >= 3 = a surveiller.

## Catalogue technologies (initial)

### Edge AI / TinyML

| Technologie | Maturite | Pertinence | Accessibilite | Score | Status |
|-------------|----------|------------|---------------|-------|--------|
| ESP32 + zclaw (agent IA 35KB) | 4 | 5 | 5 | **4.7** | A PROTOTYPER |
| MimiClaw (ESP32-S3 + Claude + Telegram) | 3 | 5 | 5 | **4.3** | A PROTOTYPER |
| ESP32-LLM (LLM local 19 tok/s) | 3 | 4 | 5 | **4.0** | A PROTOTYPER |
| MountAIn (TinyML cameras) | 4 | 3 | 2 | 3.0 | SURVEILLER |
| TensorFlow Lite Micro | 5 | 4 | 3 | 4.0 | A EVALUER |

### Robotique

| Technologie | Maturite | Pertinence | Accessibilite | Score | Status |
|-------------|----------|------------|---------------|-------|--------|
| ROS 2 (framework standard) | 5 | 4 | 3 | **4.0** | A EVALUER |
| Gazebo (simulateur 3D) | 5 | 3 | 3 | 3.7 | SURVEILLER |
| OpenCat/Petoi (quadrupede) | 4 | 4 | 4 | **4.0** | A PROTOTYPER |
| Berkeley Humanoid Lite (5k USD) | 3 | 3 | 2 | 2.7 | SURVEILLER |
| Salvius (humanoide recycle) | 2 | 4 | 5 | 3.7 | INTERESSANT |
| Poppy Humanoid (education) | 4 | 3 | 2 | 3.0 | SURVEILLER |

### Modeles frugaux

| Technologie | Maturite | Pertinence | Accessibilite | Score | Status |
|-------------|----------|------------|---------------|-------|--------|
| Qwen3-30B-A3B (quantise) | 4 | 5 | 4 | **4.3** | A PROTOTYPER |
| DeepSeek-V3.2 (raisonnement) | 4 | 5 | 3 | 4.0 | A EVALUER |
| GLM-4.5-Air | 4 | 4 | 4 | 4.0 | A EVALUER |
| Ollama (inference locale) | 5 | 5 | 5 | **5.0** | EN USAGE |
| llama.cpp (inference CPU) | 5 | 5 | 4 | **4.7** | A PROTOTYPER |

### Protocoles & Integration

| Technologie | Maturite | Pertinence | Accessibilite | Score | Status |
|-------------|----------|------------|---------------|-------|--------|
| MCP over MQTT (ESP32 + LLM) | 3 | 5 | 4 | **4.0** | A PROTOTYPER |
| CrewAI (orchestration agents) | 4 | 5 | 4 | **4.3** | A EVALUER |
| Mastra (agents TypeScript) | 4 | 4 | 4 | 4.0 | A EVALUER |
| OpenClaw (agents crypto/edge) | 3 | 3 | 3 | 3.0 | SURVEILLER |

## Ressources GitHub

### Listes curatees
- [awesome-robotics-projects](https://github.com/mjyc/awesome-robotics-projects) — Projets robotique abordables et visionnaires
- [awesome-open-source-robots](https://github.com/stephane-caron/awesome-open-source-robots) — 100+ robots open source
- [awesome-tinyml](https://github.com/umitkacar/awesome-tinyml) — TinyML, edge AI, on-device inference
- [awesome-weekly-robotics](https://github.com/msadowski/awesome-weekly-robotics) — Newsletter robotique

### Projets cles
- [zclaw](https://abit.ee/en/artificial-intelligence/zclaw-esp32-ai-agent-microcontroller-open-source-freertos-smart-home-iot-en) — Agent IA sur ESP32 (35KB, 5 EUR, Telegram + Claude)
- [MimiClaw](https://www.cnx-software.com/2026/02/13/mimiclaw-is-an-openclaw-like-ai-assistant-for-esp32-s3-boards/) — ESP32-S3 + Claude + Telegram + GPIO
- [esp32-llm](https://github.com/DaveBben/esp32-llm) — LLM sur ESP32 (19 tok/s)
- [Berkeley Humanoid Lite](https://github.com/HybridRobotics/Berkeley-Humanoid-Lite) — Humanoide open source 5k USD
- [Roboto Origin](https://github.com/Roboparty/roboto_origin) — Humanoide DIY complet

## Infrastructure R&D

| Ressource | Usage |
|-----------|-------|
| **VM105 r2d2-lab** (192.168.1.161) | Prototypage, tests, experimentation |
| **ESP32 boards** | Hardware edge AI (a acquérir) |
| **Ollama sur VM105** | Inference LLM locale |
| **Vault Knowledge** | Documentation R&D dans `Concepts/C_RD-*.md` |

## Conventions

### Notes vault
- **Chemin evaluations** : `Knowledge/Concepts/C_RD-{Technologie}.md`
- **Chemin benchmarks** : `Knowledge/References/YYYY-MM-DD_RD-Benchmark-{Sujet}.md`
- **Tags** : `rd/edge-ai`, `rd/robotique`, `rd/modeles-frugaux`, `rd/iot`, `rd/souverainete`

### Donnees
- **catalog.json** : Catalogue des technologies evaluees avec scores
- **watch-list.json** : Sujets de veille active
- **projects.json** : Projets R&D en cours

### Nommage commandes
- Prefix : `/rd-`
- Format : `/rd-{action}` (scan, evaluate, benchmark, prototype, watch, catalog, report)
