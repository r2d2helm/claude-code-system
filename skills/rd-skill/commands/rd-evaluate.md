# /rd-evaluate — Evaluation approfondie

Evaluation detaillee d'une technologie ou projet specifique : WebFetch documentation, analyse technique, avantages/inconvenients, faisabilite R2D2.

## Usage

```
/rd-evaluate {technologie ou URL GitHub}
/rd-evaluate zclaw
/rd-evaluate https://github.com/DaveBben/esp32-llm
/rd-evaluate ROS 2 pour monitoring PME
```

## Processus

### 1. Collecte d'information
- WebSearch + WebFetch sur la documentation officielle
- Lire le README GitHub si applicable
- Chercher benchmarks, retours d'experience, issues connues

### 2. Analyse technique

| Critere | Questions |
|---------|-----------|
| **Architecture** | Comment ca marche ? Quelles dependances ? |
| **Performance** | Benchmarks disponibles ? Latence, debit, consommation ? |
| **Integration R2D2** | Compatible avec notre stack (ESP32, Telegram, MCP, Claude) ? |
| **Courbe d'apprentissage** | Combien de temps pour un premier prototype ? |
| **Communaute** | Stars GitHub, dernier commit, issues ouvertes, contributeurs ? |
| **Licence** | Open source ? Quelle licence ? Usage commercial ? |
| **Cout** | Hardware, licences, infra, maintenance ? |

### 3. Scoring R&D (3 dimensions)
- Maturite (1-5)
- Pertinence (1-5)
- Accessibilite (1-5)

### 4. Recommandation
- **PROTOTYPER** : lancer un test sur VM105 dans la semaine
- **SURVEILLER** : ajouter a la watch-list, re-evaluer dans 1 mois
- **PASSER** : pas aligne avec nos besoins actuels
- **INTEGRER** : pret pour usage en production

### 5. Output
- Note vault : `Knowledge/Concepts/C_RD-{Technologie}.md`
- Mise a jour catalogue : `data/catalog.json`
