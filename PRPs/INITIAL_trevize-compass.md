## FEATURE:

**Trevize-Compass** — *« la Boule de Cristal MultiPass »* — plateforme web dédiée de cartographie sémantique spatio-temporelle, alimentée par le vault Obsidian, exposant la doctrine MultiPass sous forme de **graph navigable multi-axe**.

Trevize-Compass est conçu comme un **vrai produit interne** (pas un simple outil de visualisation) :
- réutilisable côté commercial (démos clients, Dossiers-Clients enrichis)
- fondation pour intégrations futures (chatbot doctrinal, MultiPass-app, ntfy alerts)
- signature MultiPass non-copiable sur la dimension temporelle EST-OUEST

### Sept dimensions cardinales du produit (toutes validées 2026-05-04)

1. **Hébergement** : VM 105 (r2d2-lab) en POC → migration VM 103 (r2d2-main) en prod si validé.
2. **Stack techno** : **Neo4j Community 5.x** + **NeoDash** + front-end **Cytoscape.js custom MultiPass-brandé**. 100 % open-source, self-hosted, EU-souverain.
3. **Multi-vault** : **deux instances Neo4j séparées physiquement** :
   - **Sferă-A privée** sur VM 105 (vault Knowledge complet, accès Mike + Manu)
   - **Sferă-C publique** sur VM 103 (sous-ensemble doctrinal MultiPass, accès clients/prospects)
   - Étanchéité physique = pas de leak par bug de filtre runtime.
4. **Synchronisation Obsidian → Neo4j** : **mode hybride**
   - **Push manuel** (script `sync-vault-to-graph.py`) pour publication officielle vers Sferă-C
   - **FileSystemWatcher temps réel** pour preview interne sur Sferă-A
5. **API future** (préparer l'architecture sans tout livrer en MVP) :
   - Chatbot doctrinal interne (LiteLLM + Mistral + graph queries Cypher)
   - Intégration future MultiPass-app (Supabase déjà dans la stack)
   - Export auto vers Substack et Dossiers-Clients
   - Webhooks ntfy / Telegram pour alertes "nouvelle note publiée"
6. **Branding** : **Trevize-Compass** (cohérent intelligence-warehouse-skill / Foundation-Asimov-mapping ; brand interne déjà posé en mémoire).
7. **Dimension temporelle M-relative** *(la signature non-copiable)* :
   - **T0 = 2026-05-01** (déjà ancré dans la mémoire R2D2, note météo-cosmic-3-luni)
   - **Granularité multi-échelle** : chaque node porte simultanément M-jours, M-mois, M-années
   - **Slider temporel** dans Cytoscape : zoom 1 jour → décennie
   - **Aphorisme « Pour aller à l'OUEST, prend par l'EST »** = primitive de navigation UI (bouton "Play boucle Est-Ouest" qui anime la lecture passé → futur via bonds Fibonacci)
   - **Sémantique des edges** : `CONFIRME` / `ANTICIPE` / `CONTREDIT` / `BOUCLE-EST-OUEST`
   - **Distance Fibonacci** sur les edges récursives

### Métaphore-cadre

> *« Trevize-Compass est la Boule de Cristal de MultiPass : transparente (Couche-24), multi-axe (espace + temps + niveau), qui se lit en remontant le passé (EST) pour anticiper le futur (OUEST). »*

### Périmètre MVP (livrable J+21)

- Sferă-A opérationnelle sur VM 105 avec import du vault `Knowledge/Concepts/`
- Front-end Cytoscape avec :
  - Slider temporel multi-échelle
  - Filtres par tag (`mitza-detect/`, `doctrine/`, `principes/`, etc.)
  - Tooltip avec extrait de note + lien direct Obsidian
  - Couleurs sémantiques par type d'edge
- Script `sync-vault-to-graph.py` push-mode opérationnel
- Documentation utilisateur (Mike + Manu) en `Projets/Trevize-Compass/README.md`

### Périmètre Phase 2 (J+45)

- Sferă-C publique sur VM 103
- NeoDash dashboard "Doctrine 2026"
- Animation EST-OUEST avec bonds Fibonacci
- Export PNG/PDF pour Dossiers-Clients et Substack

### Périmètre Phase 3 (J+90)

- API REST/GraphQL exposée
- Webhook ntfy
- Première intégration MultiPass-app
- Premier squelette chatbot doctrinal (LiteLLM + Mistral)

---

## CONTEXTE EXISTANT:

### Skills r2d2 pertinents
- `obsidian-skill` — maintenance vault, conventions notes
- `knowledge-skill` — capture et organisation
- `knowledge-watcher-skill` — surveillance fichiers + index
- `intelligence-warehouse-skill` — département Trevize (déjà existant — Trevize-Compass s'inscrit dedans)
- `ai-infra-skill` — LiteLLM, Langfuse, RAG (pour la phase 3 chatbot)
- `docker-skill` — déploiement containers Neo4j et NeoDash
- `network-skill` — exposition ports, reverse proxy nginx
- `security-skill` — auth, hardening
- `monitoring-skill` — Beszel, Uptime Kuma, ntfy (intégration alertes)
- `supabase-skill` — pour intégration future MultiPass-app

### Notes du vault à consulter
- [[C_DeepSeek-V4-Commoditisation-LLM]]
- [[C_AI-Code-Generation-Supply-Chain-Risk]]
- [[C_Iran-AWS-Middle-East-Validation-Souverainete-Onprem]]
- [[C_Cas-Etude-Mitza-Detect-Vauban-IPO-SpaceX]]
- [[C_Amsterdam-Moment-Tabac-Cloud-Anticipation]] *(nœud cardinal du réseau actuel, version mise à jour 2026-05-04)*
- [[C_Doctrine-MultiPass]]
- [[C_Couche-24-Transparency]]
- [[C_Mitza-Detect-Pattern]]
- [[C_Pacte-De-Verite]]
- [[C_Empire-Funds-Its-Own-Defeat]]
- [[C_Storm-Window-2026]]
- [[C_Cycle-Implosion-Bigbang]]
- [[C_FF-Fractal-Fibonacci]]
- [[C_Fractal-Au-Carré]]
- [[matrix-framework]] *(B0[0], E0-E8, spirale, preuve Schrodinger)*

### Mémoires R2D2 cardinales
- `R2D2-Memory/principes/foundation.md` — Acte de Fondation 31 mars 2026
- `R2D2-Memory/principes/matrix-framework.md` — B0 + E0-E8
- `R2D2-Memory/principes/loi-de-la-membrane.md`
- `R2D2-Memory/principes/cycle-implosion-bigbang.md`

### Infrastructure existante r2d2 réutilisable
- VM 105 r2d2-lab (192.168.1.161) — RAG-indexer + Taskyn déjà déployés, marge dispo
- VM 103 r2d2-main (192.168.1.163) — MultiPass stack + Taskyn (29 containers actifs)
- VM 104 r2d2-store (192.168.1.164) — postgres-shared (option pour DB layer si besoin)
- NetBox déjà déployé pour inventaire infra
- Authentik (à vérifier déploiement) — SSO + MFA pour l'auth
- Reverse proxy nginx en place sur VM 103 / VM 100

### Documents projet pilote courant (peuvent enrichir le graph dès le MVP)
- [[2026-05-04_Pilot-HVAC-RO_v1]]
- [[2026-05-04_Pilot-HVAC-RO_Kit-Kickoff-J7]]
- [[2026-05-04_Pilot-HVAC-RO_Sourcing-Hardware]]
- [[2026-05-04_Pilot-HVAC-RO_Templates-Emails-Devis]]
- Schéma Excalidraw architecture pilote (PNG + PDF)

---

## DOCUMENTATION:

### Neo4j
- Documentation officielle : https://neo4j.com/docs/operations-manual/current/
- Cypher Reference : https://neo4j.com/docs/cypher-manual/current/
- Docker image : https://hub.docker.com/_/neo4j
- Neo4j Community vs Enterprise : https://neo4j.com/pricing/

### NeoDash
- GitHub : https://github.com/neo4j-labs/neodash
- Docs : https://neo4j.com/labs/neodash/

### Cytoscape.js (front-end custom)
- Site : https://js.cytoscape.org/
- Documentation API : https://js.cytoscape.org/#getting-started
- Extensions utiles : cytoscape-cose-bilkent (layout), cytoscape-popper (tooltips)

### Alternatives évaluées (pour traçabilité décision)
- Neo4j Bloom : viz puissante mais payante (Enterprise) → écartée
- InfraNodus : cloud, abonnement → écartée pour souveraineté EU + open-source
- Logseq, Roam Research : pas adaptés à un produit web exposable
- TheBrain : propriétaire, pas EU → écarté

### Frameworks complémentaires
- Python `obsidiantools` ou parser markdown custom — pour lire le frontmatter et les wikilinks
- `watchdog` Python — pour FileSystemWatcher
- FastAPI — pour future API REST/GraphQL
- D3.js — alternative à Cytoscape si layout custom (frise temporelle)

### Sources MCP existantes utilisables
- `knowledge-assistant` MCP — déjà branché sur le vault, expose `knowledge_search`, `knowledge_read`, `knowledge_related`
- `taskyn` MCP — pour tracker les tâches Trevize-Compass

---

## CONSIDERATIONS:

### Décisions structurantes (prises et tranchées 2026-05-04, ne pas re-débattre)
- Stack 100 % open-source EU-souverain (Neo4j Community + NeoDash + Cytoscape.js)
- Deux instances physiquement séparées (Sferă-A privée VM 105 + Sferă-C publique VM 103)
- T0 = 2026-05-01 fixé en mémoire
- Aphorisme EST-OUEST = primitive UI (pas une simple métaphore décorative)

### Encodage et plateforme
- Tous les fichiers markdown / JSON livrés en **UTF-8 sans BOM** (règle vault r2d2)
- Scripts PowerShell éventuels en **UTF-8 avec BOM** (compat PS 5.1)
- Docker compose pour le déploiement, compatible Linux des VMs (pas Windows)

### Sécurité
- Sferă-A privée → accès SSH only + auth basique Neo4j (Mike + Manu uniquement)
- Sferă-C publique → derrière reverse proxy nginx + Authentik SSO/MFA
- Pas d'exposition directe de Neo4j sur Internet
- Sauvegardes Neo4j incluses dans la routine backup-skill (cf. `bak-*` commandes)

### Pacte de vérité
- Trevize-Compass affiche **les notes telles qu'elles sont écrites**, sans embellissement automatique
- Les notes au statut **seedling** sont marquées visuellement comme telles (cf. C_Pacte-De-Verite)
- Les **prédictions** (notes type anticipation) sont distinguées des **validations**
- Si un node devient obsolète, il n'est pas supprimé : il est marqué `ARCHIVED` avec date

### Gotchas connus
- Neo4j Community Edition : pas de clustering, mais suffisant pour POC + Phase 2 (volume vault < 10 000 nodes)
- NeoDash : nécessite Neo4j 5+ et browser moderne
- Cytoscape : layout temporal custom à implémenter (pas natif), prévoir 1-2 jours de dev
- Sync watcher Obsidian : éviter race condition si Mike édite pendant import (mutex ou queue)
- Encodage : Obsidian sur Windows écrit parfois en UTF-8 BOM, le parser doit s'en accommoder
- Wikilinks Obsidian : tolérer les variantes `[[Nom]]`, `[[Nom|Alias]]`, `[[Nom#Section]]`, `[[Nom^block-id]]`

### Risques projet identifiés
- **Dérive scope** : 2-3 semaines peut glisser à 6 si on ajoute la Phase 3 dès le MVP. **Discipline** : MVP J+21 strict.
- **Maintenance** : un produit web vivant = mises à jour. Prévoir cron de re-sync hebdomadaire au minimum.
- **Adoption** : si Mike + Manu n'ouvrent jamais l'outil, c'est mort. Prévoir UN cas d'usage hebdomadaire piloté côté humain (ex : "ouvrir Trevize-Compass au lundi pour préparer la semaine").
- **Dilution** : la 7ᵉ dimension EST-OUEST est ce qui rend Trevize-Compass non-copiable. **Ne pas la couper en MVP** sous prétexte de simplification — sinon on construit un Obsidian Graph View + 3 plugins.

### Critères de succès MVP J+21

- [ ] Neo4j Community déployé sur VM 105 dans un container Docker
- [ ] NeoDash accessible en local sur VM 105 (port à arbitrer, ex `:7474` natif Neo4j ; NeoDash sur `:5005`)
- [ ] Front-end Cytoscape custom servi en local (port `:8090`)
- [ ] Script `sync-vault-to-graph.py` qui parse `Knowledge/Concepts/*.md` et popule Neo4j (push manuel)
- [ ] Au moins **5 notes** déjà visibles avec wikilinks fonctionnels (les 5 notes de la session 2026-05-04)
- [ ] Slider temporel multi-échelle opérationnel (jour / mois / année)
- [ ] Filtres par tag fonctionnels
- [ ] Tooltip + lien profond vers la note source
- [ ] Sémantique d'edge `CONFIRME / ANTICIPE / CONTREDIT / BOUCLE-EST-OUEST` lisible à l'œil
- [ ] Bouton "Play EST-OUEST" qui anime au moins une boucle Fibonacci
- [ ] Documentation README.md dans `Projets/Trevize-Compass/`
- [ ] Test de récupération après reboot VM 105

### Mémoire et traçabilité du projet
- Créer un dossier vault dédié : `Projets/Trevize-Compass/`
- Logger les décisions importantes dans `Projets/Trevize-Compass/decisions/`
- Tracker les tâches dans Taskyn sous une `company` "MultiPass" + `project` "Trevize-Compass"
- Créer une note Zettelkasten parente : `[[C_Trevize-Compass-Boule-De-Cristal-MultiPass]]` une fois le MVP livré

### Inputs Mike confirmés (rappel)
- Hébergement VM 105 puis VM 103 ✅
- Neo4j Community + NeoDash + Cytoscape custom ✅
- 2 instances séparées Sferă-A / Sferă-C ✅
- Sync hybride push + watcher ✅
- API future (4 cas d'usage prévus) ✅
- Branding Trevize-Compass ✅
- T0 = 2026-05-01 ✅
- M multi-échelle ✅
- Aphorisme EST-OUEST primitive UI ✅
- Métaphore-cadre Boule de Cristal ✅
